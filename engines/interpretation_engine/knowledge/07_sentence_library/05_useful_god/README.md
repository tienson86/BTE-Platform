# 05_useful_god

## Mục đích

Module `05_useful_god` định nghĩa khung Sentence Framework cho phần **Dụng Thần**.

Đây **không** phải nơi viết câu luận giải thật.
Đây **không** chứa Rule.
Chỉ cung cấp cấu trúc để Interpretation Engine chọn / compose câu thuộc nhóm `useful_god`.

---

## Vai trò

```text
Rule Database
        ↓
Sentence Library / 05_useful_god
        ↓
Interpretation Engine
        ↓
Priority Engine → Report Template → Report Engine → Final Report
```

---

## Cấu trúc

```text
05_useful_god/

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

- `sentence_id`: `useful_god_NNN` — ví dụ `useful_god_001`
- `label_ref`: logical `label_code` — ví dụ `description`, `recommendation`
- `condition_group`: `AND` (mặc định) hoặc `OR` (V2-ready)

---

## Quy tắc đặt sentence (tương lai)

```text
useful_god_NNN.json

Ví dụ:
  useful_god_001.json
  useful_god_002.json
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
| module_id | 05_useful_god |
| module_title | Dụng Thần |
| version | 1.0.0 |
| schema_version | 1.0.0 |
| render_version | 1.0.0 |
| supported_output | pdf, html, markdown, json |
| status | active |
| language | vi |

---

END
