# BTE Platform

# S01_REVIEW_CHECKLIST

---

Version

1.0.0

Status

ACTIVE

Module

UI Master

Section

S01 — Thông Tin & Định Hướng

Type

Review Checklist

---

# 1. Purpose

Tài liệu này định nghĩa quy trình Review chính thức cho Section S01.

Mục tiêu:

- Đảm bảo Frontend triển khai đúng Canonical UI.
- Loại bỏ đánh giá theo cảm tính.
- Chuẩn hóa quy trình nghiệm thu (Acceptance Test).
- Tạo tiêu chuẩn Freeze cho toàn bộ dự án.

Review luôn thực hiện trên Screenshot.

Không review bằng Code.

---

# 2. Review Priority

Thứ tự ưu tiên:

Priority 1

CANONICAL PNG

↓

Priority 2

MASTER_LAYOUT.md

↓

Priority 3

MASTER_GRID.png

↓

Priority 4

MASTER_ANNOTATION.png

↓

Priority 5

Implementation Screenshot

↓

Priority 6

Source Code

Source Code chỉ được xem khi Screenshot không giải thích được lỗi.

---

# 3. Review Environment

Desktop

1920 × 1080

100% Zoom

Light Mode

Không review trên:

- Mobile
- Tablet
- Browser Zoom
- Responsive Mode

---

# 4. Review Process

Bước 1

Mở Canonical Screenshot.

↓

Bước 2

Mở Screenshot của Cursor.

↓

Bước 3

Đặt cạnh nhau.

↓

Bước 4

So sánh từng nhóm.

↓

Bước 5

Đánh giá PASS / FAIL.

---

# 5. Review Categories

S01 được review theo 10 nhóm.

1.

Layout

2.

Composition

3.

Spacing

4.

Typography

5.

Alignment

6.

Visual Hierarchy

7.

Color

8.

CTA

9.

Business Structure

10.

Overall Quality

---

# 6. Layout Review

## Column Ratio

□ Đúng 58% / 42%.

---

## Column Position

□ LEFT đúng.

□ RIGHT đúng.

---

## Section Height

□ Không cao hơn Canonical.

□ Không thấp hơn Canonical.

---

## Card Width

□ Đúng.

---

PASS khi:

Không có sai lệch rõ ràng.

---

# 7. Composition Review

LEFT chỉ có:

□ Identity

□ Condition

RIGHT chỉ có:

□ Guidance

□ CTA

Không được:

□ CTA dưới toàn Section.

□ Guidance sang trái.

□ Condition sang phải.

---

# 8. Identity Review

Kiểm tra:

□ Icon.

□ Nhật Chủ.

□ Ngũ hành.

□ Âm dương.

□ Badge.

□ Tính cách.

---

Nhật Chủ phải là điểm nổi bật nhất.

PASS

□

FAIL

□

---

# 9. Condition Review

Có đúng:

□ 3 dòng.

Không:

□ 2 dòng.

□ 4 dòng.

---

Badge

□ cùng kích thước.

□ cùng chiều cao.

□ cùng Radius.

---

Label

□ căn trái.

Value

□ căn trái.

Badge

□ căn phải.

---

# 10. Guidance Review

Có đúng:

□ 3 Card.

---

Card Height

□ giống nhau.

---

Icon

□ cùng kích thước.

---

Question

□ cùng Style.

---

Description

□ cùng Style.

---

Không có Card nào dài hơn rõ rệt.

---

# 11. CTA Review

Có đúng:

□ 1 CTA.

---

Position

□ cuối cột phải.

---

Width

□ bằng cột phải.

---

Radius

□ đúng.

---

Color

□ Primary Red.

---

Không được:

□ Full Width toàn Section.

□ nhiều CTA.

---

# 12. Typography Review

Section Title

□ đúng.

---

Card Title

□ đúng.

---

Nhật Chủ

□ lớn nhất.

---

Metadata

□ nhỏ nhất.

---

Badge

□ dễ đọc.

---

Line Height

□ đều.

---

# 13. Spacing Review

Outer Padding

□ đúng.

---

Column Gap

□ đúng.

---

Card Padding

□ đúng.

---

Badge Padding

□ đúng.

---

CTA Margin

□ đúng.

---

Không có:

□ khoảng trắng chết.

□ thành phần dính nhau.

---

# 14. Alignment Review

LEFT

□ Left Align.

---

RIGHT

□ Left Align.

---

Badge

□ Center.

---

CTA

□ Center.

---

Không có phần tử lệch.

---

# 15. Color Review

Primary

□ đúng.

---

Secondary

□ đúng.

---

Badge

□ Semantic.

---

Không dùng màu ngoài Design System.

---

# 16. Visual Hierarchy Review

Thứ tự mắt nhìn phải là:

□ Nhật Chủ.

↓

□ Điều kiện.

↓

□ Bạn là ai?

↓

□ Thế mạnh.

↓

□ Bạn nên làm gì?

↓

□ CTA.

Nếu mắt bị nhảy sai.

FAIL.

---

# 17. Business Review

Sau khi đọc S01.

Người dùng phải hiểu:

□ Tôi là ai.

□ Tôi thuộc nhóm nào.

□ Điểm mạnh.

□ Nên phát triển hướng nào.

Nếu thiếu.

FAIL.

---

# 18. Pixel Review

So sánh với Canonical.

Cho phép sai số:

Padding

±2 px

---

Gap

±2 px

---

Typography

±1 px

---

Border Radius

±2 px

---

Shadow

Tương đương.

Không yêu cầu tuyệt đối.

---

# 19. Scoring

| Category | Max |
|----------|----:|
| Layout | 10 |
| Composition | 15 |
| Spacing | 10 |
| Typography | 15 |
| Alignment | 10 |
| Hierarchy | 15 |
| CTA | 10 |
| Business | 10 |
| Visual Quality | 5 |
| Canonical Match | 10 |

Total

100 điểm.

---

# 20. Acceptance Rules

## PASS

≥95 điểm.

Có thể Freeze.

---

## PASS WITH CHANGES

90–94 điểm.

Cho phép chỉnh nhỏ.

Không sửa Layout.

---

## FAIL

<90 điểm.

Bắt buộc Rebuild.

---

# 21. Freeze Checklist

Trước khi Freeze.

Phải có:

□ Build PASS.

□ TypeScript PASS.

□ Tests PASS.

□ Screenshot.

□ Review PASS.

□ Product Owner Approval.

Thiếu một mục.

Không Freeze.

---

# 22. Deliverables

Sau Review.

Lưu:

```
Screenshot

↓

Review Report

↓

Score

↓

Decision

↓

Freeze Status
```

---

# 23. Review Decision

Reviewer chỉ được chọn một trong bốn trạng thái:

🟢 PASS

Section đạt chuẩn.

Freeze.

---

🟡 PASS WITH CHANGES

Chỉ sửa nhỏ.

Review lại.

---

🟠 REBUILD REQUIRED

Sai bố cục.

Rebuild.

---

🔴 FAIL

Không đúng Canonical.

Làm lại từ đầu.

---

# 24. Golden Rule

Reviewer không đánh giá theo cảm nhận.

Reviewer không đánh giá theo sở thích.

Reviewer chỉ đánh giá theo:

- CANONICAL_PORTAL_UI_DESKTOP_V1.png
- S01_MASTER_LAYOUT.md
- S01_MASTER_GRID.png
- S01_MASTER_ANNOTATION.png

Nếu có mâu thuẫn giữa Screenshot và Canonical.

Canonical luôn đúng.

---

# 25. Freeze Statement

Một Section chỉ được Freeze khi:

- Đạt tối thiểu 95/100.
- Khớp Canonical.
- Được Product Owner phê duyệt.

Sau khi Freeze.

Section trở thành tài sản chính thức của BTE Platform.

Mọi thay đổi tiếp theo phải thông qua Change Request hoặc Release mới.