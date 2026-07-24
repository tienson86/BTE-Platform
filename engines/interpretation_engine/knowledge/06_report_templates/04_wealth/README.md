# 04_wealth

## Mục đích

Module `04_wealth` định nghĩa khung Template Framework cho phần **Tài Chính** trong báo cáo BTE.

Đây **không** phải nơi viết nội dung luận giải.
Đây **không** sinh dữ liệu luận giải.
Chỉ cung cấp cấu trúc để Report Engine render phần `wealth`.

---

## Vai trò

```text
Interpretation Engine  →  nội dung luận giải Tài Chính
Priority Engine        →  chọn kết quả ưu tiên
Report Engine          →  chọn template từ module này
04_wealth/              →  cấu trúc sections / blocks / placeholders
Final Report           →  phần Tài Chính trong báo cáo
```

---

## Cấu trúc

```text
04_wealth/

├── README.md
├── metadata.json
├── template_index.json
├── template_labels.json
└── template_examples.json
```

Schema dùng chung nằm ở:

```text
../template_schema.json
```

---

## Ý nghĩa từng file

| File | Vai trò |
|------|---------|
| `metadata.json` | Metadata module (id, version, status, schema_version) |
| `template_index.json` | Mục lục template (lookup nhẹ, chưa có template thật ở V1.0) |
| `template_labels.json` | Dictionary kiểu block (title, paragraph, warning, ...) |
| `template_examples.json` | 1 example minh họa schema (không phải luận giải) |
| `README.md` | Tài liệu module |

---

## Quy ước ID (Architecture Review)

- `section_id`: semantic — ví dụ `wealth_intro`, `wealth_body`
- `block_id`: semantic — ví dụ `wealth_B001`, `wealth_B002`
- `label_ref`: logical `label_code` — ví dụ `title`, `paragraph`, `recommendation`
- `condition_group`: `AND` (mặc định) hoặc `OR` (V2-ready)
- `render_config`: cấu hình render (`layout`, `max_blocks`, `theme`)
- `render_style`: style theo output (PDF / HTML / Markdown / ...)

Metadata bổ sung:

- `dependencies`: interpretation_engine, priority_engine, report_engine
- `supported_output`: pdf, html, markdown, json
- `render_version`: 1.0.0 (không thay `schema_version`)

---

## Quy tắc đặt template (tương lai)

```text
wealth_NNN.json

Ví dụ:
  wealth_001.json
  wealth_002.json
```

Khi thêm template thật:

1. Tạo file JSON tuân thủ `../template_schema.json`
2. Thêm entry vào `template_index.json`
3. Không nhúng text luận giải — dùng `content_ref` và `placeholders`
4. Không copy schema vào thư mục module

---

## Quy tắc mở rộng

1. Giữ nguyên schema V1.0.
2. Field mới đặt trong `extensions`.
3. Labels mới thêm vào `template_labels.json` với `id` tăng dần.
4. Không xóa field đã ổn định.
5. Không hard-code rule luận giải.
6. Encoding UTF-8, JSON hợp lệ.

---

## Metadata nhanh

| Trường | Giá trị |
|--------|---------|
| module_id | 04_wealth |
| module_title | Tài Chính |
| version | 1.0.0 |
| schema_version | 1.0.0 |
| render_version | 1.0.0 |
| supported_output | pdf, html, markdown, json |
| status | active |
| language | vi |

---

END
