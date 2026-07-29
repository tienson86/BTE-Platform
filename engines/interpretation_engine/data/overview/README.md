# Overview Rule Database

## Mục đích

Module **overview** chịu trách nhiệm tạo phần **Tổng quan** của báo cáo Bát Tự.

Đây là chương đầu tiên trong Interpretation Engine.

---

## Thứ tự xử lý

1. Đọc rules.csv
2. RuleMatcher kiểm tra điều kiện
3. Chọn các Rule phù hợp
4. Lấy Template tương ứng
5. Sinh câu
6. Ghép đoạn
7. Sinh chương "Tổng quan"

---

## Quy tắc đặt mã

| Prefix | Ý nghĩa |
|---------|----------|
| OVR | Rule |
| TMP_OVR | Template |

Ví dụ:

OVR001

↓

TMP_OVR001

---

## Các section

| Section | Nội dung |
|----------|----------|
| basic | Giới thiệu |
| strength | Thân vượng / thân nhược |
| season | Ảnh hưởng mùa sinh |
| pattern | Cách cục |
| useful_god | Dụng thần |
| favorable | Hỷ thần |
| unfavorable | Kỵ thần |
| summary | Tổng kết |

---

## Điều kiện

Điều kiện được lưu dưới dạng JSON.

Ví dụ:

```json
{
    "operator": "AND",
    "conditions": [
        {
            "field": "strength",
            "operator": "eq",
            "value": "Strong"
        }
    ]
}
```

---

## Liên kết

Rules

↓

Templates

↓

Sentences

↓

Paragraphs

↓

Overview Chapter

---

## Version

Current Version

1.0.0
