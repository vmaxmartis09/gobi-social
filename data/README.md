# data/ — Data Source

Phần dữ liệu của người dùng: hồ sơ nhân vật, video, ảnh, giọng, tài khoản, kết quả render. **Chỉ khung thư mục và README nằm trong git**, mọi nội dung thật bị gitignore.

```
data/
├── _shared/            # dùng chung mọi project: models, voices, templates
└── projects/
    ├── _template/      # khung chuẩn để tạo project mới
    └── <project>/      # mỗi project một bộ dữ liệu riêng (characters, library, products, accounts, social, knowledge, ...)
```

- Tạo project mới: `python -m gobi project new <tên>` (copy khung chuẩn).
- Chọn project: `--project <tên>`, biến `GOBI_PROJECT`, hoặc `python -m gobi project use <tên>`.
- Đặt data ngoài repo: biến `GOBI_DATA_DIR=/đường/dẫn/data`.
- Code tool luôn lấy đường dẫn qua `gobi.paths`, không tự ghép đường dẫn.
