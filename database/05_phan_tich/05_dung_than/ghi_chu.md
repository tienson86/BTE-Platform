# Ghi chú Module 05 - DỤNG THẦN

## Mục tiêu thiết kế

Module được xây dựng theo kiến trúc Rule Engine.

Không sử dụng if-else cứng trong mã nguồn.

Mọi quy tắc đều được cấu hình bằng dữ liệu CSV.

---

## Nguyên tắc

Một Rule chỉ thực hiện một nhiệm vụ.

Không gộp nhiều điều kiện vào một Rule.

Rule phải độc lập.

Có thể bật/tắt mà không ảnh hưởng Rule khác.

---

## Explainable Engine

Mỗi kết quả phải trả về:

- Rule đã kích hoạt.
- Rule bị loại.
- Lý do.
- Độ ưu tiên.
- Giải thích.
- Khuyến nghị.

Người dùng phải biết vì sao Engine đưa ra kết luận.

---

## Priority Engine

Thứ tự ưu tiên mặc định:

1. Tòng Cách
2. Điều Hậu
3. Cách Cục
4. Thân Vượng/Nhược
5. Dụng Thần
6. Hỷ Thần
7. Kỵ Thần

Các ngoại lệ được quản lý trong:

09_xung_dot_rule.csv

---

## Conflict Engine

Nếu hai Rule đưa ra kết quả khác nhau:

Engine sẽ tra:

09_xung_dot_rule.csv

để xác định:

- Rule thắng
- Rule bị ghi đè
- Rule được hợp nhất
- Rule chỉ dùng để giải thích

---

## Mở rộng

Có thể bổ sung Rule mới mà không cần sửa Engine.

Chỉ cần:

1. thêm Rule CSV

2. thêm giải thích

3. thêm xung đột (nếu có)

---

## Quy ước đặt mã Rule

DHxxx

Điều Hậu

TVxxx

Thân Vượng

CCxxx

Cách Cục

TCxxx

Tòng Cách

DTxxx

Dụng Thần

HTxxx

Hỷ Thần

KTxxx

Kỵ Thần

---

## Quy ước phiên bản

Version 1.x

Bổ sung dữ liệu.

Không thay đổi cấu trúc.

Version 2.x

Có thể bổ sung cột dữ liệu mới.

Version 3.x

Có thể thay đổi mô hình Rule Engine.

---

## Kiểm thử

Mỗi Rule cần có:

- ít nhất 01 trường hợp đúng (Positive Test)
- ít nhất 01 trường hợp sai (Negative Test)
- ít nhất 01 trường hợp biên (Boundary Test)

---

## Định hướng phát triển

Trong các phiên bản tiếp theo, module sẽ được mở rộng để:

- chấm điểm xác suất (Confidence Score)
- hỗ trợ nhiều trường phái Tử Bình
- giải thích đa tầng (Rule → Nhóm Rule → Kết luận)
- tích hợp với module Đại Vận và Lưu Niên
- hỗ trợ nhiều ngôn ngữ (Việt, Anh, Trung)
