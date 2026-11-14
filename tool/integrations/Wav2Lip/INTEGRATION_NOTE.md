# INTEGRATION NOTE — Wav2Lip (ONNX)

## Nguồn gốc
- Repo vendor: [instant-high/wav2lip-onnx-HQ](https://github.com/instant-high/wav2lip-onnx-HQ) — bản chuyển đổi ONNX của [Wav2Lip gốc](https://github.com/Rudrabha/Wav2Lip).
- Lý do chọn bản ONNX thay vì Wav2Lip gốc (PyTorch): dự án đã dùng `onnxruntime` + `CoreMLExecutionProvider` cho face-swap ([inswapper_128.onnx](../../models/weights/inswapper_128.onnx)), nên tái dùng cùng stack thay vì cài thêm PyTorch/MPS riêng cho lip-sync — ít rủi ro tương thích hơn trên Apple Silicon.

## Mục đích sử dụng
Khớp lại khẩu hình (môi) trong video đã swap mặt Gô Bi theo audio MỚI (giọng clone), dùng trong bước 5 của `MotionMimicWorkflow` khi `--audio omnivoice`.

## Model checkpoint
- `checkpoints/wav2lip_gan.onnx` (138MB) — tải từ mirror [bluefoxcreation/Wav2lip-Onnx](https://huggingface.co/bluefoxcreation/Wav2lip-Onnx) trên Hugging Face (repo gốc host model qua Google Drive, hay bị rate-limit khi tải qua gdown).
- `faceID/recognition.onnx` (92MB) — tải từ folder Google Drive chính thức của wav2lip-onnx-HQ.
- Cả hai **không commit vào git** (xem `.gitignore` trong thư mục này) — cần tải lại thủ công nếu clone máy mới. `utils/scrfd_2.5g_bnkps.onnx` (face detection) đã có sẵn trong repo vendor nên không cần tải thêm.

## Patch đã áp dụng vào `inference_onnxModel.py` (đánh dấu `[GOBI PATCH]`)
1. Bỏ 3 lệnh gọi `cv2.selectROI(...)` (GUI chọn vùng/mặt bằng tay) — script gốc được thiết kế chạy tương tác trên desktop có màn hình. Thay bằng mặc định "dùng toàn bộ khung hình" / "nhận diện mặt đầu tiên" vì pipeline của ta luôn đưa vào đúng 1 video đã swap mặt sẵn (không cần chọn tay).
2. Đổi tên input tensor `'mel_spectrogram'`/`'video_frames'` → `'mel'`/`'vid'` để khớp đúng checkpoint `wav2lip_gan.onnx` tải từ mirror HF (khác tên input so với checkpoint gốc của repo vendor mà ta không tải được).
3. Đổi `providers=["CPUExecutionProvider"]` → thêm `CoreMLExecutionProvider` ưu tiên trước (cho cả model Wav2Lip chính và RetinaFace detector) — tận dụng GPU/Neural Engine M4, tự fallback CPU nếu CoreML không hỗ trợ một op nào đó.
4. Sửa `ffmpeg.exe` (Windows) → `ffmpeg` (macOS/Linux) ở bước mux video/audio cuối.

## Môi trường chạy
Venv riêng tại `.venv/` (Python 3.12, tạo bằng `uv venv --python 3.12 .venv`), KHÔNG dùng chung với `.venv` gốc của `gobi-social` — tránh xung đột `opencv-python`/`onnxruntime` version giữa 2 dự án. Cài đặt: `uv pip install --python .venv/bin/python opencv-python numpy tqdm librosa numba imutils onnxruntime pillow`.

## Giới hạn đã biết
- Chỉ test với clip ngắn 5-6s trên Mac Mini M4; chưa benchmark video dài.
- Không dùng các tính năng mở rộng của fork này (face enhancer, denoiser, face mask/occluder) — các model nặng đó (`blendmasker.onnx` 257MB, v.v.) **không được tải/dùng** để giữ dung lượng tối thiểu.
- `--face_mode`, `--pads` dùng giá trị mặc định của repo vendor — có thể cần chỉnh nếu khẩu hình lệch quá nhiều so với gương mặt gốc Gô Bi.

## Wrapper adapter
`src/gobi/adapters/integrations/wav2lip_adapter.py` — class `Wav2LipAdapter.run(video_path, audio_path, output_path)`, gọi `inference_onnxModel.py` qua subprocess trong venv riêng ở trên.
