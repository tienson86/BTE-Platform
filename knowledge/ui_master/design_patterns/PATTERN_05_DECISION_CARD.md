# BTE Platform

# PATTERN_05 — DECISION CARD

---

Version

1.0.0

Status

FROZEN

Module

UI Design System

Pattern

05

Name

Decision Card

Type

Foundation Pattern

---

# 1. Mục đích

Decision Card là Pattern tiêu chuẩn dùng để trình bày **một kết luận quan trọng nhất** sau khi hệ thống hoàn tất quá trình phân tích.

Đây là Pattern cao nhất trong Information Hierarchy của BTE Platform.

Decision Card không trình bày dữ liệu.

Decision Card không trình bày thuật toán.

Decision Card chỉ trả lời:

**"Kết luận cuối cùng là gì?"**

---

# 2. Triết lý

Decision first.

Evidence second.

Details later.

Người dùng phải nhận được câu trả lời trước.

Sau đó mới xem điểm số.

Sau đó mới xem nguyên nhân.

Sau đó mới xem phân tích chi tiết.

---

# 3. Khi nào sử dụng

Pattern này dùng cho:

• Sức mạnh Mệnh cục

• Dụng thần

• Hỷ thần

• Kỵ thần

• Đánh giá Đại vận

• Đánh giá Lưu niên

• Kết luận Phong thủy

• Kết luận AI

• Khuyến nghị cuối cùng

---

# 4. Không sử dụng

Không dùng cho:

✗ Dashboard

✗ Danh sách

✗ Timeline

✗ Báo cáo

✗ Bảng dữ liệu

✗ Form

✗ So sánh nhiều giá trị

---

# 5. Reading Flow

```
Header

↓

Decision

↓

Score

↓

Insight

↓

Evidence

↓

Primary Action
```

Đây là thứ tự bắt buộc.

Không được đảo.

---

# 6. Canonical Layout

```
┌──────────────────────────────────────────────┐

SỨC MẠNH MỆNH CỤC

──────────────────────────────────────────────

MẠNH

82 / 100

──────────────────────────────────────────────

Mệnh cục cân bằng tốt.

Nhật chủ được sinh trợ.

──────────────────────────────────────────────

██████████████████░░░░

──────────────────────────────────────────────

✓ Nhật chủ đắc lệnh

✓ Được Mộc sinh trợ

✓ Hỏa vượng

✓ Kim suy

──────────────────────────────────────────────

[Xem phân tích chi tiết →]

└──────────────────────────────────────────────┘
```

---

# 7. Component Tree

```
DecisionCard

├── Header
│
├── Decision
│
├── Score
│
├── Insight
│
├── Progress
│
├── EvidenceList
│
└── PrimaryAction
```

---

# 8. Decision

Đây là thành phần quan trọng nhất.

Ví dụ

```
RẤT MẠNH

MẠNH

TRUNG BÌNH

YẾU

RẤT YẾU
```

Không dùng câu dài.

Không thêm mô tả.

---

# 9. Score

Hiển thị ngay dưới Decision.

Ví dụ

```
82 / 100
```

Score chỉ là định lượng.

Không phải kết luận.

---

# 10. Insight

Insight giải thích Decision.

Giới hạn:

Tối đa

2 dòng.

Ví dụ

```
Mệnh cục cân bằng tốt.

Nhật chủ được sinh trợ.
```

Không quá 2 dòng.

---

# 11. Progress

Horizontal Progress Bar.

Flat.

Rounded.

Không:

Gradient

Gauge

Donut

Animation

---

# 12. Evidence

Hiển thị đúng

4 dòng.

Ví dụ

```
✓ Nhật chủ đắc lệnh

✓ Được Mộc sinh trợ

✓ Hỏa vượng

✓ Kim suy
```

Không mô tả dài.

Không giải thích.

---

# 13. Primary Action

Chỉ một CTA.

Ví dụ

```
Xem phân tích chi tiết →
```

CTA luôn nằm cuối Card.

---

# 14. Information Hierarchy

★★★★★

Decision

★★★★☆

Insight

★★★★☆

Score

★★★★☆

Progress

★★★☆☆

Evidence

★★☆☆☆

CTA

---

# 15. Typography

Decision

28 px

700

---

Score

24 px

700

---

Insight

14 px

400

---

Evidence

14 px

500

---

CTA

14 px

600

---

# 16. Semantic Colors

Decision

Rất mạnh

Xanh lá đậm

---

Mạnh

Xanh lá

---

Trung bình

Vàng

---

Yếu

Cam

---

Rất yếu

Đỏ

---

Score

Neutral Gray

---

Progress

Semantic

---

CTA

BTE Red

---

# 17. White Space

Padding

20 px

Header Bottom

16 px

Decision Bottom

12 px

Score Bottom

16 px

Insight Bottom

16 px

Progress Bottom

20 px

Evidence Bottom

20 px

Ưu tiên khoảng trắng hơn Divider.

---

# 18. Card Style

Background

White

Border

1 px

Radius

12 px

Shadow

Soft

Theo Enterprise Design System.

---

# 19. Accessibility

Contrast đạt WCAG AA.

Progress có aria-label.

CTA keyboard focus.

Decision không phụ thuộc màu sắc.

---

# 20. Responsive

Desktop

One Card

Tablet

One Card

Mobile

One Card

Reading Flow không thay đổi.

---

# 21. Những điều KHÔNG được phép

Không sử dụng:

✗ Gauge

✗ Pie Chart

✗ Donut

✗ Radar

✗ Spider

✗ Glass

✗ Gradient

✗ Heavy Shadow

✗ Animation

✗ Nhiều CTA

✗ Insight quá 2 dòng

---

# 22. Các màn hình sử dụng

Đã áp dụng:

✓ S05 — Sức mạnh Mệnh cục

Có thể tái sử dụng:

✓ S06 — Dụng thần

✓ S07 — Hỷ thần

✓ S08 — Đại vận

✓ S09 — Hôn nhân

✓ S10 — Sự nghiệp

✓ AI Summary

✓ Final Recommendation

---

# 23. Design Principles

Decision

>

Score

Conclusion

>

Statistics

Reading Speed

>

Analysis

Information

>

Decoration

Consistency

>

Creativity

---

# 24. Reusability

Decision Card phải tái sử dụng được cho:

Customer Portal

Analysis Console

Admin Portal

Desktop

Tablet

Mobile

Không tạo nhiều biến thể.

Chỉ thay đổi dữ liệu.

Không thay đổi cấu trúc.

---

# 25. Acceptance Criteria

PASS khi:

✓ Decision là điểm nhìn đầu tiên.

✓ Người dùng hiểu kết luận trong dưới 5 giây.

✓ Insight không quá 2 dòng.

✓ Có đúng 4 Evidence.

✓ Chỉ có 1 CTA.

✓ Không giống KPI Dashboard.

✓ Không giống báo cáo tài chính.

---

# 26. Design Decision Record

Decision Card là Pattern quan trọng nhất của tầng Analysis.

Đây là nơi chuyển đổi kết quả tính toán của Analysis Engine thành ngôn ngữ mà người dùng có thể hiểu ngay.

BTE không yêu cầu người dùng tự phân tích điểm số.

BTE luôn đưa ra:

**Kết luận → Định lượng → Bằng chứng → Hành động.**

Đây là triết lý UX cốt lõi của toàn bộ hệ thống.

---

# 27. Mapping

Pattern này là nền tảng cho:

| Module | Mức độ |
|---------|---------|
| S05 — Sức mạnh Mệnh cục | ⭐⭐⭐⭐⭐ |
| S06 — Dụng thần | ⭐⭐⭐⭐ |
| S07 — Hỷ thần | ⭐⭐⭐⭐ |
| S08 — Đại vận | ⭐⭐⭐ |
| AI Executive Summary | ⭐⭐⭐⭐⭐ |
| Final Recommendation | ⭐⭐⭐⭐⭐ |

---

# 28. Evolution Policy

Decision Card là một trong năm Foundation Pattern.

Mọi phiên bản mới (Desktop, Tablet, Mobile) chỉ được phép điều chỉnh:

- Kích thước
- Khoảng cách
- Typography responsive

Không được thay đổi:

- Reading Flow
- Information Hierarchy
- Component Tree
- Decision-first Principle

---

# 29. Freeze Statement

PATTERN_05_DECISION_CARD.md là tài liệu chuẩn duy nhất mô tả Decision Card của BTE Platform.

Mọi màn hình sử dụng Decision Card phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

**PATTERN_05_DECISION_CARD.md là Single Source of Truth.**