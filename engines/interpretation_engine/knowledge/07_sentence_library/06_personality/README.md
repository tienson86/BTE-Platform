# 06_personality

## Mục đích

Module `06_personality` định nghĩa khung Sentence Framework cho phần **Tính Cách**.

Đây **không** phải nơi viết câu luận giải thật.
Đây **không** chứa Rule.
Chỉ cung cấp cấu trúc để Interpretation Engine chọn / compose câu thuộc nhóm `personality`.

---

## Vai trò

```text
Rule Database
        ↓
Sentence Library / 06_personality
        ↓
Interpretation Engine
        ↓
Priority Engine → Report Template → Report Engine → Final Report
```

---

## Cấu trúc

```text
06_personality/

├── README.md
├── metadata.json
├── sentence_index.json
├── sentence_labels.json
└── sentence_examples.json
```

Schema dùng chung:

```text
../sentence_schema.json
```

---

## Ý nghĩa từng file

| File | Vai trò |
|------|---------|
| `metadata.json` | Metadata module |
| `sentence_index.json` | Mục lục sentence (lookup nhẹ) |
| `sentence_labels.json` | Dictionary loại câu |
| `sentence_examples.json` | 1 example minh họa schema |
| `README.md` | Tài liệu module |

---

## Quy ước ID

- `sentence_id`: `personality_NNN` — ví dụ `personality_001`
- `label_ref`: logical `label_code` — ví dụ `description`, `recommendation`
- `condition_group`: `AND` (mặc định) hoặc `OR` (V2-ready)

---

## Quy tắc đặt sentence (tương lai)

```text
personality_NNN.json

Ví dụ:
  personality_001.json
  personality_002.json
```

Khi thêm sentence thật:

1. Tuân thủ `../sentence_schema.json`
2. Cập nhật `sentence_index.json`
3. Không hard-code Rule / Bát Tự
4. Không copy schema vào thư mục module

---

## Quy tắc mở rộng

1. Giữ nguyên schema V1.0.
2. Field mới đặt trong `extensions`.
3. Labels mới thêm vào `sentence_labels.json`.
4. Không xóa field đã ổn định.
5. Encoding UTF-8, JSON hợp lệ.

---

## Metadata nhanh

| Trường | Giá trị |
|--------|---------|
| module_id | 06_personality |
| module_title | Tính Cách |
| version | 1.0.0 |
| schema_version | 1.0.0 |
| render_version | 1.0.0 |
| supported_output | pdf, html, markdown, json |
| status | active |
| language | vi |

---

END
