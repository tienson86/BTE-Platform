# 06_health

## Mục đích

Module `06_health` định nghĩa khung Template Framework cho phần **Sức Khỏe** trong báo cáo BTE.

Đây **không** phải nơi viết nội dung luận giải.
Đây **không** sinh dữ liệu luận giải.
Chỉ cung cấp cấu trúc để Report Engine render phần `health`.

---

## Vai trò

```text
Interpretation Engine  →  nội dung luận giải Sức Khỏe
Priority Engine        →  chọn kết quả ưu tiên
Report Engine          →  chọn template từ module này
06_health/              →  cấu trúc sections / blocks / placeholders
Final Report           →  phần Sức Khỏe trong báo cáo
```

---

## Cấu trúc

```text
06_health/

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

## Quy tắc đặt template (tương lai)

```text
health_NNN.json

Ví dụ:
  health_001.json
  health_002.json
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
| module_id | 06_health |
| module_title | Sức Khỏe |
| version | 1.0.0 |
| schema_version | 1.0.0 |
| status | active |
| language | vi |

---

END
