# BTE Interpretation Engine Schema

## Mục đích

Thư mục `schema/` định nghĩa chuẩn dữ liệu (Data Contract)
cho toàn bộ Interpretation Engine.

Tất cả các module:

- overview
- personality
- career
- wealth
- marriage
- health
- useful_god
- pattern
- shensha
- luck

đều sử dụng chung bộ schema này.

---

## Quy trình

CSV / JSON

↓

Loader

↓

Schema Validator

↓

Python Models

↓

Rule Matcher

↓

Sentence Builder

↓

Renderer

---

## Danh sách schema

| File | Chức năng |
|------|-----------|
| common_schema.json | Kiểu dữ liệu dùng chung |
| rule_schema.json | Quy tắc Rule |
| template_schema.json | Template |
| sentence_schema.json | Câu diễn giải |
| paragraph_schema.json | Đoạn văn |
| chapter_schema.json | Chương |
| metadata_schema.json | Metadata |
| glossary_schema.json | Thuật ngữ |

---

## Version

1.0.0
