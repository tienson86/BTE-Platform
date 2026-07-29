# JSON_STYLE_GUIDE.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: JSON Style Guide
>
> BTE Platform

---

# 1. Mục đích

Tài liệu này quy định chuẩn trình bày JSON trong Knowledge Base.

Mục tiêu:

- Dễ đọc.
- Dễ Review.
- Dễ Diff.
- Dễ Merge.
- Dễ tự động hóa.

---

# 2. Encoding

Tất cả file JSON phải sử dụng:

- UTF-8
- Không BOM

---

# 3. Indentation

Sử dụng:

- 4 spaces
- Không dùng Tab

---

# 4. Line Ending

Chuẩn:

```
LF
```

---

# 5. Root Object

Mỗi file phải có đúng một Root Object hoặc Root Array.

Không được trộn nhiều Root.

---

# 6. Key Naming

JSON Key:

- snake_case
- tiếng Anh
- chữ thường

Ví dụ:

```json
{
    "rule_id": "",
    "priority": ""
}
```

---

# 7. Key Order

Thứ tự Key phải cố định.

Ví dụ Rule:

```text
id
code
name

classification

source

target

conditions

evaluation

priority

lifecycle

metadata
```

Không tự ý đổi thứ tự.

---

# 8. Array

Array:

- Không để null.
- Nếu không có dữ liệu dùng `[]`.
- Mỗi phần tử cùng kiểu.

---

# 9. Object

Object:

- Không để `{}` nếu không được phép.
- Không lồng quá sâu nếu không cần thiết.

---

# 10. Boolean

Sử dụng:

```json
true

false
```

Không dùng:

```text
Yes

No

1

0
```

---

# 11. Null

Chỉ sử dụng `null` khi Schema cho phép.

Ưu tiên:

- `[]`
- `""`
- `{}`

nếu phù hợp với Schema.

---

# 12. Number

Number:

- Không dùng dấu phân cách hàng nghìn.
- Không dùng chuỗi thay cho số.

Đúng:

```json
100
```

Sai:

```json
"100"

1,000
```

---

# 13. String

String:

- UTF-8.
- Không khoảng trắng đầu/cuối.
- Không xuống dòng nếu không cần.

---

# 14. Comment

JSON không được chứa comment.

Sai:

```json
// comment

/* comment */
```

---

# 15. Duplicate Keys

Không được phép tồn tại Duplicate Key.

---

# 16. Empty Value

Không dùng:

```json
{
    "name": null
}
```

nếu Schema yêu cầu String.

---

# 17. File Size

Khuyến nghị:

- ≤ 2 MB mỗi file JSON.

Nếu lớn hơn nên chia nhỏ theo Module hoặc Category.

---

# 18. Formatting

Nên sử dụng formatter thống nhất trước khi Commit.

Không chỉnh sửa thủ công chỉ để thay đổi định dạng.

---

# 19. Governance

Mọi JSON mới phải:

- Đúng Style Guide.
- Đúng Schema.
- Đúng Validation.

---

# 20. Kết luận

JSON Style Guide đảm bảo toàn bộ Knowledge Base có định dạng thống nhất, giúp Review, Diff, Merge và tự động hóa trở nên đơn giản và đáng tin cậy.