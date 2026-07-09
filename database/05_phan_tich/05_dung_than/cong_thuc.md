# Module 05 - DỤNG THẦN

## Mục đích

Module này xác định:

- Nhật chủ
- Thân vượng / thân nhược
- Điều Hậu
- Cách Cục
- Tòng Cách
- Dụng Thần
- Hỷ Thần
- Kỵ Thần

Module hoạt động theo Rule Engine.

Không sử dụng if-else cố định.

---

# Quy trình suy luận

Bước 1

Xác định Nhật Chủ

↓

Bước 2

Đánh giá mùa sinh

↓

Bước 3

Đánh giá Điều Hậu

↓

Bước 4

Đánh giá Thân Vượng / Thân Nhược

↓

Bước 5

Đánh giá Cách Cục

↓

Bước 6

Kiểm tra Tòng Cách

↓

Bước 7

Giải quyết xung đột Rule

↓

Bước 8

Chọn Dụng Thần

↓

Bước 9

Sinh Hỷ Thần

↓

Bước 10

Sinh Kỵ Thần

---

# Công thức Điều Hậu

Ưu tiên xét khí hậu trước.

Ví dụ

Mùa đông

Hợi
Tý
Sửu

↓

ưu tiên Hỏa

Mùa hè

Tỵ
Ngọ
Mùi

↓

ưu tiên Thủy

---

# Công thức Thân Vượng

Điểm Thân =

Điểm Nguyệt lệnh

+

Điểm Tàng Can

+

Điểm Thiên Can

+

Điểm Địa Chi

+

Điểm Sinh Trợ

-

Điểm Khắc

Ví dụ

>= 70

Thân Vượng

40–69

Trung Hòa

<40

Thân Nhược

---

# Công thức Dụng Thần

Nếu

Tòng Cách

↓

Theo Tòng Cách

Ngược lại

↓

Nếu

Điều Hậu

được kích hoạt

↓

Điều Hậu ưu tiên

Nếu không

↓

Theo Thân Vượng / Thân Nhược

Nếu có

Cách Cục

↓

Điều chỉnh kết quả

---

# Công thức Hỷ Thần

Hỷ Thần

=

Hành sinh Dụng Thần

hoặc

Hành hỗ trợ Dụng Thần

---

# Công thức Kỵ Thần

Kỵ Thần

=

Hành phá Dụng Thần

hoặc

Hành làm mất cân bằng ngũ hành.

---

# Thứ tự ưu tiên Rule

1. Tòng Cách
2. Điều Hậu
3. Cách Cục
4. Thân Vượng / Thân Nhược
5. Dụng Thần
6. Hỷ Thần
7. Kỵ Thần

---

# Explainable Engine

Mỗi kết quả phải trả về:

Rule đã kích hoạt

Rule bị loại

Lý do

Giải thích

Khuyến nghị

Không chỉ trả về kết quả cuối cùng.

