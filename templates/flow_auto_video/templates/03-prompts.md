# Template — 3 lớp prompt cho Google Flow

Prompt viết tiếng Anh (model hiểu mô tả hình ổn định hơn). Cụm `[STYLE]` là đúng 1 cụm phong cách đã chốt ở kịch bản — dán nguyên văn vào cả 3 lớp, đừng diễn đạt lại.

## Lớp 1 — Character reference sheet (Image mode, 1 prompt / nhân vật)

```
CHARACTER REF — [Tên]:
Character reference sheet for [mô tả loại nhân vật] named [Tên]: [tuổi], [ngoại hình + trang phục chép từ Character Bible]. Multiple angles (front, 3/4, side), full body and close-up face, consistent [STYLE], neutral background, consistent soft lighting, no text.
```

## Lớp 2 — Storyboard từng cảnh (Image mode, đính kèm reference nhân vật)

```
STORYBOARD — CẢNH [N] (attach: [tên các character ref]):
Single cinematic frame for [bối cảnh + hành động cảnh N], featuring [Tên] exactly as in the attached reference. [Góc máy: wide / medium / close-up]. Consistent [STYLE], consistent lighting and color palette with the character reference, [tỉ lệ 9:16 / 16:9], no text.
```

## Lớp 3 — Video từ storyboard (Video mode, ảnh storyboard làm frame đầu)

```
VIDEO — CẢNH [N]:
Animate this frame into a [T]-second cinematic clip. CRITICAL: preserve EXACTLY the same [STYLE], lighting, and color palette shown. Scene: [hành động chi tiết + ngôn ngữ máy quay: slow push-in / tracking shot / rack focus]. [Dialogue nếu có: the character says "..."]. Smooth natural motion, no jump cuts, no text.
```

---
Ghi chú: "preserve EXACTLY" là câu giữ cho video không tự đổi phong cách so với ảnh tĩnh. Nếu Flow vẫn lệch, thêm 2–3 từ màu chủ đạo cụ thể vào cuối prompt.
