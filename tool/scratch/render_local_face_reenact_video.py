import os
import cv2
import time
import subprocess
import insightface
from insightface.app import FaceAnalysis

def main():
    video_in = "scratch/thanhhang_clean.mp4"
    temp_video_out = "output/mimic_workflow/gobi_lyly_swapped_temp.mp4"
    final_video_out = "output/mimic_workflow/gobi_lyly_local_reenact_final.mp4"
    dna_img_path = "assets/characters/lyly_master_portrait.png"

    os.makedirs("output/mimic_workflow", exist_ok=True)

    print("[*] Initializing InsightFace Buffalo_L & Inswapper...")
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(512, 512))

    swapper = insightface.model_zoo.get_model("models/weights/inswapper_128.onnx", providers=["CPUExecutionProvider"])

    print(f"[*] Extracting Gobi LyLy DNA from {dna_img_path}...")
    source_img = cv2.imread(dna_img_path)
    source_faces = app.get(source_img)
    if not source_faces:
        print("[!] Error: No face in LyLy DNA!")
        return
    source_face = source_faces[0]
    print("[+] LyLy DNA face embedding extracted successfully!")

    cap = cv2.VideoCapture(video_in)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"[*] Input Video: {width}x{height} @ {fps}fps, Total frames: {total_frames} (~{total_frames/fps:.1f}s)")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(temp_video_out, fourcc, fps, (width, height))

    frame_idx = 0
    swapped_count = 0
    t0 = time.time()

    print("[*] Processing frames with Gobi LyLy reenactment...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        faces = app.get(frame)
        if faces:
            # Pick largest/primary face in frame
            primary_face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0]) * (f.bbox[3]-f.bbox[1]))
            frame = swapper.get(frame, primary_face, source_face, paste_back=True)
            swapped_count += 1

        writer.write(frame)

        if frame_idx % 60 == 0 or frame_idx == total_frames:
            elapsed = time.time() - t0
            speed = frame_idx / elapsed if elapsed > 0 else 0
            print(f"  -> Frame {frame_idx}/{total_frames} ({frame_idx/total_frames*100:.1f}%) | Swapped: {swapped_count} | Speed: {speed:.1f} fps")

    cap.release()
    writer.release()
    print(f"[+] All frames processed in {time.time()-t0:.1f}s! Swapped {swapped_count}/{total_frames} frames.")

    print("[*] Muxing original audio back with FFmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-i", temp_video_out,
        "-i", video_in,
        "-c:v", "libx264",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:a", "copy",
        final_video_out
    ]
    subprocess.run(cmd, check=True)

    if os.path.exists(temp_video_out):
        os.remove(temp_video_out)

    print(f"[🎉] HOÀN TẤT VIDEO CLONE GOBI LYLY THẬT 100%: {final_video_out}")

if __name__ == "__main__":
    main()
