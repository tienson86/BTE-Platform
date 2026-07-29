# Dayun Module

> Version: 1.0
>
> Status: Draft
>
> Module: Luck Engine
>
> Location:
>
> knowledge/luck_engine/01_dayun/
>
> Author: BTE Platform
>
> Language: Vietnamese

---

# 1. Giới thiệu

Dayun Module là thành phần đầu tiên của Luck Engine.

Module này chịu trách nhiệm đặc tả toàn bộ quy tắc liên quan đến **Đại vận (大运)** trong hệ thống BTE Platform.

Đây là tài liệu nghiệp vụ (Business Knowledge), không phải tài liệu triển khai mã nguồn.

---

# 2. Mục tiêu

Dayun Module xác định:

- Quy tắc tính Đại vận.
- Quy tắc xác định tuổi khởi vận.
- Quy tắc xác định chiều vận.
- Quy tắc sinh các trụ Đại vận.
- Cấu trúc dữ liệu Đại vận.
- Các trường hợp ngoại lệ.
- Bộ dữ liệu kiểm thử.

Module này không thực hiện việc luận giải cát hung.

---

# 3. Phạm vi

Module bao gồm:

- Tuổi khởi vận.
- Thuận hành.
- Nghịch hành.
- Thiên Can Đại vận.
- Địa Chi Đại vận.
- Tàng Can Đại vận.
- Thập Thần của Đại vận.
- Ngũ Hành của Đại vận.
- Metadata của Đại vận.

Không bao gồm:

- Lưu niên.
- Lưu nguyệt.
- Lưu nhật.
- Lưu thời.
- Luận giải.

---

# 4. Cấu trúc tài liệu

Thư mục bao gồm:

README.md

↓

DAYUN_SPEC.md

↓

DAYUN_ALGORITHM.md

↓

DAYUN_EDGE_CASES.md

↓

DAYUN_TEST_CASES.md

↓

CHANGELOG.md

Mỗi tài liệu có vai trò độc lập.

---

# 5. Vai trò của từng tài liệu

## README.md

Giới thiệu tổng quan module.

---

## DAYUN_SPEC.md

Đặc tả nghiệp vụ chính thức.

Định nghĩa:

- Khái niệm.
- Quy tắc.
- Điều kiện.
- Đầu vào.
- Đầu ra.
- Data Contract.

---

## DAYUN_ALGORITHM.md

Mô tả chi tiết thuật toán.

Bao gồm:

- Các bước xử lý.
- Trình tự tính toán.
- Pseudo Code.
- Flow Diagram.

Không chứa mã nguồn.

---

## DAYUN_EDGE_CASES.md

Tập hợp toàn bộ trường hợp đặc biệt.

Ví dụ:

- Sinh gần tiết khí.
- Tuổi khởi vận bằng 0.
- Sai lệch múi giờ.
- Chuyển năm.
- Chuyển tháng.

---

## DAYUN_TEST_CASES.md

Bộ dữ liệu kiểm thử chuẩn.

Mỗi Test Case gồm:

- Input.
- Expected Output.
- Giải thích.
- Kết quả mong đợi.

---

## CHANGELOG.md

Lịch sử thay đổi của Module.

---

# 6. Quan hệ với các Module khác

Dayun Module phụ thuộc:

- Calendar Engine.
- BaZi Engine.

Dayun Module cung cấp dữ liệu cho:

- Luck Engine.
- Interpretation Engine (thông qua LuckContext).

---

# 7. Nguyên tắc phát triển

Mọi thay đổi liên quan đến Đại vận phải:

- Cập nhật Specification.
- Cập nhật Algorithm.
- Cập nhật Test Cases.
- Cập nhật Changelog.

Không được thay đổi thuật toán trực tiếp trong mã nguồn khi chưa cập nhật tài liệu.

---

# 8. Roadmap

Giai đoạn 1

- README

Giai đoạn 2

- DAYUN_SPEC

Giai đoạn 3

- DAYUN_ALGORITHM

Giai đoạn 4

- DAYUN_EDGE_CASES

Giai đoạn 5

- DAYUN_TEST_CASES

Giai đoạn 6

- CHANGELOG

---

# 9. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Khởi tạo Dayun Module |