# 07_sentence_library

## Tổng quan

`07_sentence_library` là **thư viện câu luận giải (Sentence Library Framework)** của BTE Platform.

Module này **không** chứa Rule.

Module này **không** chứa Report Template.

Module này **không** chứa nội dung luận giải thật.

Module này chỉ định nghĩa:

- Schema chuẩn của Sentence
- Metadata từng nhóm câu
- Index để lookup sentence
- Labels (loại câu / mục đích hiển thị)
- Examples minh họa cấu trúc

Đây là tầng **Sentence Structure** trong pipeline luận giải.

---

## Vai trò trong hệ thống

```text
Rule Database
        │
        ▼
Sentence Library   ← Module này (07_sentence_library)
        │
        ▼
Interpretation Engine
        │
        ▼
Priority Engine
        │
        ▼
Report Template
        │
        ▼
Report Engine
        │
        ▼
Final Report
```

| Tầng | Trách nhiệm |
|------|-------------|
| Rule Database | Quy tắc nghiệp vụ Bát Tự |
| Sentence Library | Khung câu / schema / index / labels |
| Interpretation Engine | Compose luận giải từ rule + sentence |
| Priority Engine | Quyết định ưu tiên / ghi đè |
| Report Template | Cấu trúc hiển thị báo cáo |
| Report Engine | Render báo cáo |
| Final Report | Kết quả đầu ra |

**Nguyên tắc tách biệt:**

- Rule = **What is true**
- Sentence = **How to say**
- Interpretation = **What to compose**
- Priority = **What wins**
- Template / Report = **How to present**

---

## Trách nhiệm của module

Sentence Library **chỉ** chịu trách nhiệm:

1. Quản lý sentence schema
2. Quản lý metadata
3. Sentence index
4. Sentence labels
5. Sentence examples

**Không:**

- Sinh interpretation
- Render report
- Quyết định priority
- Hard-code Rule / Bát Tự / Thập Thần / Dụng Thần

---

## Cấu trúc thư mục

```text
07_sentence_library/

├── README.md
├── sentence_schema.json          ⭐ Schema dùng chung (DUY NHẤT)
│
├── 01_intro/
├── 02_transition/
├── 03_strength/
├── 04_pattern/
├── 05_useful_god/
├── 06_personality/
├── 07_career/
├── 08_wealth/
├── 09_relationship/
├── 10_health/
├── 11_children/
├── 12_luck_cycle/
├── 13_yearly/
└── 14_conclusion/
```

Mỗi module con:

```text
0X_module_name/

├── README.md
├── metadata.json
├── sentence_index.json
├── sentence_labels.json
└── sentence_examples.json
```

---

## 1. sentence_schema.json

Schema chuẩn cho **mọi** sentence:

- `sentence_id`, `sentence_name`, `module`, `category`
- `intent`, `tone`, `priority`
- `condition_group`, `conditions`
- `placeholders`, `variables`, `sentence_pattern`
- `language`, `enabled`, `schema_version`
- `created_at`, `updated_at`, `author`, `notes`, `extensions`

**Intent:** introduce, describe, explain, compare, warn, recommend, summarize, transition, conclude

**Tone:** neutral, positive, negative, professional, friendly, serious

**Quy tắc:**

- Chỉ một schema ở thư mục gốc
- Không copy schema vào từng module
- Framework hoàn toàn generic
- Hướng V2 qua `extension_hooks`

---

## 2. metadata.json

Bao gồm:

- `module_id`, `module_name`, `module_title`
- `description`, `version`, `status`
- `language`, `encoding`, `author`
- `created_at`, `updated_at`, `schema_version`
- `render_version`
- `dependencies`
- `supported_output`

---

## 3. sentence_index.json

Index nhẹ:

- `sentence_id`
- `sentence_name`
- `category`
- `priority`
- `version`
- `enabled`
- `file_ref`

**Không** chứa nội dung sentence.

---

## 4. sentence_labels.json

Dictionary loại câu:

- `intro`, `transition`, `description`, `analysis`
- `comparison`, `recommendation`, `warning`
- `summary`, `conclusion`, `emphasis`
- `neutral`, `positive`, `negative`

`label_ref` dùng logical `label_code`, không dùng ID kỹ thuật.

---

## 5. sentence_examples.json

Chỉ **một** schema example:

- `enabled=false`
- `is_real_content=false`
- Không dùng để render

---

## Quy trình dữ liệu

```text
1. Rule Database
   → cung cấp kết quả rule / context

2. Sentence Library
   → cung cấp schema + index + labels
   → (tương lai) cung cấp sentence_pattern đã chọn

3. Interpretation Engine
   → bind placeholders
   → compose đoạn luận giải

4. Priority Engine
   → resolve ưu tiên giữa các interpretation

5. Report Template + Report Engine
   → đưa nội dung vào khung báo cáo và render
```

---

## Nguyên tắc thiết kế

1. Không sinh câu thật trong Framework V1.0.
2. Không sinh nội dung luận giải.
3. Không hard-code Rule / Bát Tự / Thập Thần / Dụng Thần.
4. Một schema dùng chung.
5. Module đồng nhất.
6. Index tách khỏi nội dung.
7. UTF-8, JSON hợp lệ.
8. Thiết kế hướng V2 (`extensions`, `condition_group` OR).

---

## Quy tắc mở rộng

Khi thêm sentence thật (sau Freeze):

1. Tạo file `{module_short}_{nnn}.json` tuân thủ `sentence_schema.json`
2. Cập nhật `sentence_index.json`
3. Dùng `content` qua `sentence_pattern` + `placeholders`
4. Không copy schema vào module
5. Field mới đặt trong `extensions`

---

## Quy tắc Freeze

Trước khi Freeze V1.0:

- Không tạo thư viện câu thật
- Không đổi cấu trúc thư mục
- Không đổi `schema_version` trừ khi có breaking change đã duyệt
- Không sửa module Frozen khác (`01`–`06`)

Sau Freeze:

- Chỉ bổ sung sentence data theo schema đã chốt
- Không redesign Framework trừ khi mở V2

---

## Trạng thái

| Mục | Giá trị |
|-----|---------|
| Framework version | 1.0.0 |
| Schema version | 1.0.0 |
| Render version | 1.0.0 |
| Status | active (ready for Architecture Review) |
| Encoding | UTF-8 |
| Language | vi |

---

END
