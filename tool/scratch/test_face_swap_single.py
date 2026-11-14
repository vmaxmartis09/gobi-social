import os
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

print("[*] Initializing FaceAnalysis (buffalo_l)...")
app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(640, 640))

print("[*] Loading inswapper_128.onnx...")
swapper_path = "models/weights/inswapper_128.onnx"
swapper = insightface.model_zoo.get_model(swapper_path, providers=["CPUExecutionProvider"])

source_img_path = "assets/characters/lyly_master_portrait.png"
print(f"[*] Reading source character DNA: {source_img_path}...")
source_img = cv2.imread(source_img_path)
source_faces = app.get(source_img)
if not source_faces:
    print("[!] Error: No face found in source image!")
    exit(1)
source_face = source_faces[0]
print(f"[+] Found source face (LyLy DNA)! Embedding shape: {source_face.embedding.shape}")

target_frame_path = "scratch/thanhhang_frames/frame_004.jpg"
print(f"[*] Reading target frame: {target_frame_path}...")
target_img = cv2.imread(target_frame_path)
target_faces = app.get(target_img)
if not target_faces:
    print("[!] Error: No face found in target frame!")
    exit(1)

target_face = target_faces[0]
print("[*] Performing Face Reenactment / Swap...")
res_img = swapper.get(target_img, target_face, source_face, paste_back=True)

out_preview = "shots/gobi_lyly_swapped_preview.jpg"
cv2.imwrite(out_preview, res_img)
print(f"[🎉] Successfully swapped face! Preview saved to: {out_preview}")
