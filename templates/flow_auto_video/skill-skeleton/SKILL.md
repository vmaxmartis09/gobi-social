---
name: flow-auto-video
description: "Biến một ý tưởng kịch bản ngắn thành video hoàn chỉnh trên Google Flow: tự viết kịch bản nhiều cảnh, character bible, prompt character ref / storyboard / video, rồi tự điều khiển trình duyệt (labs.google/flow) tạo nhân vật → storyboard → video từng cảnh. Dùng khi user đưa ý tưởng + lưu ý và muốn 'tạo video tự động qua Google Flow'. KHÔNG ghép/edit video cuối — đó là bước CapCut của user."
disable-model-invocation: true
---

# Flow Auto Video

<!-- SKELETON: giữ cấu trúc 7 bước, điền các chỗ [...]. Cú pháp frontmatter theo docs Claude Code (code.claude.com/docs/en/skills). Đặt file tại ~/.claude/skills/flow-auto-video/SKILL.md, gọi bằng /flow-auto-video -->

## Nguyên tắc: in từng lớp ra chat, không chạy ngầm
Mỗi lớp text (kịch bản, character bible, 3 loại prompt) in ra ngay khi xong để user duyệt. Khi thao tác trên Flow, báo tiến độ theo từng hành động ("đã submit nhân vật A, đang chờ render") — không im lặng tới cuối.

## Yêu cầu
- Có Claude in Chrome (hoặc trình duyệt tích hợp) đã đăng nhập Google Flow. Chưa có → xin phép trước.
- Nói rõ số lượt generate dự kiến trước khi chạy hàng loạt (>6 cảnh hoặc >2 nhân vật).
- Giao diện Flow có thể đã đổi: luôn screenshot / đọc trang để xác nhận nút trước khi bấm.

## Bước 0 — Chốt thông tin
Từ ý tưởng + lưu ý user đưa, hỏi phần còn thiếu: phong cách · tỉ lệ · số cảnh · thời lượng/cảnh · voiceover. In bảng xác nhận, chờ ok.

## Bước 1 — Kịch bản
Theo template: [dán cấu trúc cảnh từ templates/01-script.md]. In ra, chờ duyệt.

## Bước 2 — Character Bible
Theo template: [dán từ templates/02-character-bible.md]. In ra, chờ duyệt.

## Bước 3 — Prompt character reference
Khuôn: [dán Lớp 1 từ templates/03-prompts.md]. In ra.

## Bước 4 — Prompt storyboard từng cảnh
Khuôn: [dán Lớp 2]. Ghi rõ cảnh nào attach reference nào. In ra.

## Bước 5 — Prompt video từng cảnh
Khuôn: [dán Lớp 3]. In ra. Đến đây user đã thấy đủ 5 lớp trước khi tốn credit.

## Bước 6 — Tự động hoá trên Flow
Chuyển từng dòng trong templates/04-flow-manual-checklist.md thành hành động:
1. Mở labs.google/flow → New project. Báo.
2. Nút chế độ thanh dưới → Image, chọn tỉ lệ. Xác nhận model.
3. Với mỗi character ref: nhập prompt vào ô soạn thảo ([ghi cách bạn tìm ô nhập: element contenteditable / data-slate-editor]), gửi, screenshot xác nhận ô trống + đang render. Chờ xong. Đặt tên ảnh. Báo.
4. Với mỗi cảnh: mở đính kèm → chọn đúng reference → Add to prompt → nhập prompt storyboard → gửi → chờ. Báo.
5. Chuyển Video mode, chọn tỉ lệ + thời lượng. Với mỗi cảnh: chọn ảnh storyboard làm frame đầu → (Voices nếu cần) → nhập prompt video → gửi → chờ. Báo.
6. Thất bại lặp lại 3 lần ở 1 nút → dừng, báo user, không thử vô hạn.

## Bước 7 — Bàn giao
Tổng kết + link project. Nhắc user tải video, ghép trong CapCut, thêm phụ đề/nhạc.

## Lưu ý
- Nhắc lại đúng 1 cụm phong cách trong mọi prompt.
- Kết quả sai nhân vật/lệch phong cách → regenerate cảnh đó, không đi tiếp.
- User chỉ muốn bộ prompt copy-paste → dừng sau Bước 5.
