# Checklist — thao tác Google Flow bằng tay

Làm tay ít nhất 1 lần trước khi tự động hoá. Ghi tên nút, không ghi toạ độ — giao diện Flow đổi thường xuyên (xem labs.google/fx/tools/flow/changelogs).

## Chuẩn bị
- [ ] Đăng nhập labs.google/flow bằng tài khoản có credit (free ít; AI Pro/Ultra nhiều hơn).
- [ ] Đếm số lượt generate dự kiến: số nhân vật + số cảnh × 2 (ảnh + video). Mỗi lượt tốn credit kể cả kết quả xấu.

## A. Tạo project
- [ ] **New project**, đặt tên theo tên video.

## B. Image mode — character reference
- [ ] Nút chế độ ở thanh dưới (mặc định hiện "Video · Ns") → chọn **Image**, chọn tỉ lệ khung hình đã chốt, xác nhận model ảnh (Nano Banana) hiện đúng.
- [ ] Dán prompt Lớp 1 của nhân vật 1 → gửi. Xác nhận ô nhập trống lại và thumbnail đang render.
- [ ] Chờ render xong (theo % trên thumbnail) mới làm nhân vật kế. Ảnh xấu → generate lại, đừng đi tiếp.
- [ ] Đặt tên ảnh reference theo tên nhân vật (mặc định là "Untitled" — sẽ nhầm khi có 2–3 nhân vật).

## C. Image mode — storyboard
- [ ] Trong ô prompt, mở phần đính kèm reference → chọn đúng ảnh nhân vật của cảnh → **Add to prompt**.
- [ ] Dán prompt Lớp 2 cảnh 1 → gửi → chờ xong. Lặp cho từng cảnh.
- [ ] Kiểm nhanh: mặt/trang phục nhân vật có khớp reference không. Lệch → regenerate ngay.

## D. Video mode — sinh video
- [ ] Nút chế độ → **Video**, chọn lại tỉ lệ + thời lượng/cảnh (4/6/8s tuỳ model).
- [ ] Trên ảnh storyboard cảnh 1, bấm **+** → dùng làm frame đầu (Frames to Video).
- [ ] (Nếu có voiceover) mở **Voices** ở sidebar chọn giọng trước khi gửi.
- [ ] Dán prompt Lớp 3 cảnh 1 → gửi → chờ. Lặp cho từng cảnh.

## E. Tải về
- [ ] Tải từng video cảnh (hoặc mở Scenebuilder để xếp thứ tự rồi tải).
- [ ] Ghi lại link project.

## Ghi chú cho bước tự động hoá sau này
Mỗi dòng bạn vừa tick là 1 hành động Claude sẽ phải làm qua trình duyệt. Chỗ nào bạn phải "nhìn rồi mới quyết" (ảnh ổn chưa, đã render xong chưa) → skill phải có bước screenshot/đọc trang tương ứng. Ghi lại ngay các chỗ đó vào đây:
-
-
