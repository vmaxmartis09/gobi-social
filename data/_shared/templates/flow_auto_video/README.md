# Claude × Google Flow — Starter Kit

Đi kèm bài "Để Claude tự làm video trên Google Flow — cách mình dựng bộ skill".
Guide đầy đủ: https://tienleai.com/guides/claude-google-flow-auto-video

Kit này là **bộ khung để bạn tự dựng skill của riêng mình**: template cho từng lớp text (kịch bản → character bible → 3 loại prompt), checklist thao tác Flow, và skeleton SKILL.md có sẵn cấu trúc 7 bước. Bộ skill hoàn chỉnh mình dùng (đã tinh chỉnh 3 tiếng) không nằm trong kit — liên hệ qua email như trong video.

```
claude-flow-starter-kit/
├── README.md
├── inputs/
│   └── idea-brief.md              ← 2 thứ bạn cần chuẩn bị: ý tưởng + lưu ý
├── templates/
│   ├── 01-script.md               ← kịch bản theo cảnh (bối cảnh · hành động · thoại · âm thanh · ghi chú)
│   ├── 02-character-bible.md      ← hồ sơ nhân vật để giữ mặt/dáng nhất quán
│   ├── 03-prompts.md              ← 3 khuôn prompt: character ref · storyboard · video
│   └── 04-flow-manual-checklist.md ← thao tác Flow bằng tay (làm tay 1 lần trước khi tự động hoá)
├── skill-skeleton/
│   └── SKILL.md                   ← khung skill Claude Code 7 bước, chỗ trống để bạn điền
└── example/
    └── mot-buoi-sang-o-tiem-pho.md ← 1 ý tưởng chạy hết 5 lớp text, để bạn thấy đầu ra trông thế nào
```

## Bắt đầu

1. Điền `inputs/idea-brief.md` (5 phút).
2. Dán brief vào Claude cùng 3 file template, bảo: "Viết theo đúng template, in từng lớp ra cho mình duyệt".
3. Làm tay trên Flow theo `templates/04-flow-manual-checklist.md` ít nhất 1 lần — để biết nút nào ở đâu trước khi bắt Claude tự bấm.
4. Khi 5 lớp text và thao tác tay đã ổn, copy `skill-skeleton/` vào `~/.claude/skills/<tên-skill>/`, điền chỗ trống, chạy `/<tên-skill>`.

Cập nhật 09/2026. Giao diện Flow đổi thường xuyên — checklist ghi tên nút, không ghi toạ độ.
