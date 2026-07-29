# Luck Engine Knowledge Base

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/
>
> Author: BTE Platform
>
> Language: Vietnamese
>
> Last Updated: YYYY-MM-DD

---

# 1. Giới thiệu

Luck Engine là module chịu trách nhiệm tính toán và phân tích toàn bộ hệ thống vận trình của lá số Bát Tự trong BTE Platform.

Module này **không tạo Mệnh cục**, **không tính Bát Tự**, **không xác định Cách Cục**, **không tính Thân Vượng/Nhược**, mà chỉ sử dụng kết quả từ các Engine trước đó để phân tích diễn biến của vận theo thời gian.

Luck Engine là tầng nghiệp vụ (Business Runtime Layer) nằm giữa Score Engine và Interpretation Engine.

---

# 2. Mục tiêu

Luck Engine có nhiệm vụ:

- Tính Đại vận
- Tính Lưu niên
- Tính Lưu nguyệt
- Tính Lưu nhật
- Tính Lưu thời
- Phân tích sự tương tác giữa vận và Mệnh cục
- Đánh giá ảnh hưởng của vận đối với Cách cục
- Đánh giá ảnh hưởng tới Dụng thần
- Đánh giá ảnh hưởng tới Ngũ hành
- Cung cấp dữ liệu cho Interpretation Engine

Luck Engine **không trực tiếp sinh câu luận giải**.

---

# 3. Vai trò trong toàn bộ kiến trúc

Pipeline tổng thể của BTE Platform:

Calendar Engine

↓

BaZi Engine

↓

Pattern Engine

↓

RuleContext Builder

↓

Score Engine

↓

Luck Engine

↓

Knowledge Engine

↓

Rule Matcher

↓

Priority Engine

↓

Interpretation Engine

↓

Report Engine

Luck Engine chỉ nhận dữ liệu từ các Engine trước đó.

Không được thay đổi dữ liệu của bất kỳ Engine nào.

---

# 4. Phạm vi của Luck Engine

Luck Engine chịu trách nhiệm các hệ thống sau:

## 4.1 Đại vận

Chu kỳ vận 10 năm.

Bao gồm:

- Tuổi khởi vận
- Thuận hành
- Nghịch hành
- Thiên Can
- Địa Chi
- Tàng Can
- Thập Thần
- Ngũ Hành

---

## 4.2 Lưu niên

Chu kỳ từng năm.

Bao gồm:

- Can năm
- Chi năm
- Thập thần
- Quan hệ với Mệnh cục

---

## 4.3 Lưu nguyệt

Chu kỳ từng tháng.

Bao gồm:

- Tháng tiết khí
- Can tháng
- Chi tháng
- Quan hệ với Đại vận

---

## 4.4 Lưu nhật

Chu kỳ từng ngày.

---

## 4.5 Lưu thời

Chu kỳ từng giờ.

---

# 5. Những gì Luck Engine KHÔNG làm

Luck Engine tuyệt đối không:

- Tính Bát Tự
- Tính Tứ Trụ
- Tính Tiết Khí
- Tính Nhật Chủ
- Tính Thân Vượng/Nhược
- Tính Dụng Thần
- Tính Hỷ Thần
- Tính Kỵ Thần
- Xác định Cách Cục
- Xác định Tòng Cách
- Chấm điểm Mệnh cục

Các kết quả trên đều phải được lấy từ các Engine khác.

---

# 6. Kiến trúc tài liệu

Module Luck Engine được chia thành nhiều nhóm tài liệu.

## Foundation

- README.md
- ARCHITECTURE.md

## Đại vận

01_dayun/

- README.md
- DAYUN_SPEC.md
- DAYUN_ALGORITHM.md
- DAYUN_EDGE_CASES.md
- DAYUN_TEST_CASES.md
- CHANGELOG.md

## Lưu niên

02_liunian/

- README.md
- LIUNIAN_SPEC.md
- LIUNIAN_ALGORITHM.md
- LIUNIAN_TEST_CASES.md

## Lưu nguyệt

03_liuyue/

- README.md
- LIUYUE_SPEC.md
- LIUYUE_ALGORITHM.md

## Lưu nhật

04_liuri/

## Lưu thời

05_liushi/

## Rule Layer

06_rules/

Bao gồm:

- TEN_GOD_LUCK_RULES.md
- COMBINATION_IN_LUCK.md
- TEMPERATURE_IN_LUCK.md
- USEFUL_GOD_IN_LUCK.md
- PATTERN_IN_LUCK.md

## Interpretation Layer

07_interpretation/

Bao gồm:

- INTERPRETATION_RULES.md

---

# 7. Quan hệ với các Engine khác

## Calendar Engine

Cung cấp:

- Âm lịch
- Dương lịch
- Tiết khí
- Can Chi

Luck Engine không tự tính lịch.

---

## BaZi Engine

Cung cấp:

- Tứ Trụ
- Nhật Chủ
- Tàng Can
- Thập Thần

Luck Engine không được sửa dữ liệu Bát Tự.

---

## Pattern Engine

Cung cấp:

- Cách cục
- Theo cách
- Thân vượng nhược
- Pattern Metadata

Luck Engine chỉ đọc.

---

## RuleContext

Là đầu vào chính của Luck Engine.

RuleContext là immutable.

Luck Engine không được phép sửa RuleContext.

---

## Score Engine

Cung cấp điểm tổng hợp của Mệnh cục.

Luck Engine chỉ sử dụng khi cần đánh giá tổng quan.

---

## Interpretation Engine

Luck Engine chỉ cung cấp LuckContext.

Interpretation Engine chịu trách nhiệm sinh câu luận giải.

---

# 8. Nguyên tắc thiết kế

Luck Engine phải tuân thủ các nguyên tắc sau:

1. Immutable Runtime
2. Single Responsibility
3. Không tính trùng
4. Không sửa dữ liệu upstream
5. Có thể mở rộng
6. Có thể kiểm thử độc lập
7. Có thể thay thế thuật toán
8. Tách biệt dữ liệu và luận giải

---

# 9. Quy ước phát triển

Mọi thuật toán mới phải:

- Có Specification
- Có Algorithm Document
- Có Test Cases
- Có Edge Cases
- Có Changelog

Không được lập trình trực tiếp khi chưa có tài liệu.

---

# 10. Roadmap

Giai đoạn 1

- Foundation

Giai đoạn 2

- Đại vận

Giai đoạn 3

- Lưu niên

Giai đoạn 4

- Lưu nguyệt

Giai đoạn 5

- Lưu nhật

Giai đoạn 6

- Lưu thời

Giai đoạn 7

- Rule Layer

Giai đoạn 8

- Interpretation Layer

---

# 11. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Khởi tạo Luck Engine Knowledge Base |