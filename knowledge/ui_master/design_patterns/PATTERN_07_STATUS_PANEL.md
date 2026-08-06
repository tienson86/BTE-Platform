# BTE Platform

# PATTERN_07 — STATUS PANEL

---

Version

1.0.0

Status

FROZEN

Module

UI Design System

Pattern

07

Name

Status Panel

Type

Foundation Pattern

---

# 1. Mục đích

Status Panel là Pattern tiêu chuẩn dùng để hiển thị trạng thái hiện tại của một đối tượng, một quá trình hoặc một kết quả phân tích.

Khác với Decision Card:

Decision Card trả lời:

"Kết luận cuối cùng là gì?"

Status Panel trả lời:

"Hiện tại đang ở trạng thái nào?"

Status Panel giúp người dùng nắm bắt trạng thái của hệ thống chỉ bằng vài giây.

---

# 2. Triết lý

Current State First.

Actions Later.

Người dùng luôn phải biết:

Hiện tại đang ở trạng thái nào?

trước khi xem:

- nguyên nhân
- phân tích
- hành động

---

# 3. Khi nào sử dụng

Áp dụng cho:

• Trạng thái Mệnh cục

• Trạng thái Đại vận

• Trạng thái Lưu niên

• Trạng thái Hôn nhân

• Trạng thái Sức khỏe

• Trạng thái Tài vận

• Trạng thái Phong thủy

• Trạng thái AI Analysis

• System Status

• Data Validation

---

# 4. Không sử dụng

Không dùng cho:

✗ Dashboard

✗ Báo cáo

✗ Danh sách dữ liệu

✗ Timeline

✗ Pie Chart

✗ KPI

---

# 5. Reading Flow

```
Header

↓

Current Status

↓

Status Description

↓

Indicators

↓

Recommended Action
```

Đây là Reading Flow chuẩn.

---

# 6. Canonical Layout

```
┌──────────────────────────────────────────────┐

TRẠNG THÁI MỆNH CỤC

──────────────────────────────────────────────

● ỔN ĐỊNH

──────────────────────────────────────────────

Mệnh cục đang ở trạng thái cân bằng,
có khả năng phát triển ổn định.

──────────────────────────────────────────────

✓ Ngũ hành cân bằng

✓ Nhật chủ được sinh trợ

✓ Không có xung khắc lớn

──────────────────────────────────────────────

Khuyến nghị:

Tiếp tục duy trì.

└──────────────────────────────────────────────┘
```

---

# 7. Component Tree

```
StatusPanel

├── Header
│
├── CurrentStatus
│
├── Description
│
├── IndicatorList
│
└── Recommendation
```

---

# 8. Current Status

Đây là thành phần quan trọng nhất.

Ví dụ:

```
RẤT TỐT

ỔN ĐỊNH

TRUNG BÌNH

CẦN LƯU Ý

NGUY CƠ CAO
```

Không dùng câu dài.

Không dùng đoạn văn.

---

# 9. Status Description

Giải thích ngắn.

Tối đa:

2 dòng.

Ví dụ

```
Mệnh cục đang cân bằng tốt,
không xuất hiện mất cân đối nghiêm trọng.
```

Không dài hơn.

---

# 10. Indicator List

Hiển thị

3–5 dòng.

Ví dụ

```
✓ Nhật chủ đắc lệnh

✓ Hỏa sinh trợ

✓ Không có phá cách
```

Không giải thích dài.

---

# 11. Recommendation

Một khuyến nghị ngắn.

Ví dụ

```
Tiếp tục duy trì trạng thái hiện tại.
```

Hoặc

```
Ưu tiên tăng yếu tố Thủy.
```

Không quá 2 dòng.

---

# 12. Information Hierarchy

★★★★★

Current Status

★★★★☆

Description

★★★☆☆

Indicators

★★☆☆☆

Recommendation

---

# 13. Typography

Header

16 px

700

---

Status

30 px

700

---

Description

14 px

400

---

Indicator

14 px

500

---

Recommendation

14 px

600

---

# 14. Semantic Status

Chỉ sử dụng các trạng thái chuẩn.

```
Rất tốt

Tốt

Ổn định

Trung bình

Cần lưu ý

Nguy cơ cao
```

Không sáng tạo thêm.

---

# 15. Semantic Color

Rất tốt

Dark Green

---

Tốt

Green

---

Ổn định

Blue

---

Trung bình

Gold

---

Cần lưu ý

Orange

---

Nguy cơ cao

Red

---

Không sử dụng màu khác.

---

# 16. White Space

Padding

20 px

Header Bottom

16 px

Status Bottom

16 px

Description Bottom

20 px

Indicators Bottom

20 px

Khoảng trắng ưu tiên hơn Divider.

---

# 17. Card Style

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

# 18. Accessibility

Contrast đạt WCAG AA.

Status luôn có văn bản.

Không phụ thuộc màu sắc.

Recommendation hỗ trợ Screen Reader.

---

# 19. Responsive

Desktop

One Card

Tablet

One Card

Mobile

One Card

Reading Flow giữ nguyên.

---

# 20. Những điều KHÔNG được phép

Không sử dụng:

✗ Gauge

✗ Pie Chart

✗ Donut

✗ Radar

✗ Glass

✗ Gradient

✗ Animation

✗ Quá nhiều màu

✗ Paragraph dài

---

# 21. Các màn hình sử dụng

Có thể áp dụng cho:

✓ S06 — Dụng thần

✓ S07 — Hỷ thần

✓ S08 — Kỵ thần

✓ S09 — Hôn nhân

✓ S10 — Sức khỏe

✓ S11 — Tài vận

✓ AI Status

✓ System Health

---

# 22. Design Principles

Current State

>

Raw Data

Recognition

>

Analysis

Clarity

>

Complexity

Action

>

Explanation

---

# 23. Reusability

Pattern này phải tái sử dụng được cho:

Customer Portal

Analysis Console

Admin Portal

Desktop

Tablet

Mobile

Chỉ thay đổi dữ liệu.

Không thay đổi cấu trúc.

---

# 24. Acceptance Criteria

PASS khi:

✓ Người dùng nhận biết trạng thái trong dưới 3 giây.

✓ Status là điểm nhìn đầu tiên.

✓ Description ≤ 2 dòng.

✓ Có 3–5 Indicator.

✓ Recommendation rõ ràng.

✓ Không tạo cảm giác giống báo cáo.

---

# 25. Design Decision Record

Status Panel được thiết kế để trình bày "trạng thái hiện tại" thay vì "kết quả cuối cùng".

Khác với Decision Card:

Decision Card

↓

Đưa ra kết luận.

Status Panel

↓

Mô tả trạng thái hiện tại.

Điều này giúp hệ thống có thể trình bày các đánh giá động (ví dụ Đại vận, Lưu niên, Sức khỏe...) mà không làm người dùng nhầm lẫn với kết luận cuối cùng.

---

# 26. Mapping

Pattern này là nền tảng cho:

| Module | Mức độ |
|---------|---------|
| S06 — Dụng thần | ⭐⭐⭐⭐ |
| S07 — Hỷ thần | ⭐⭐⭐⭐ |
| S08 — Kỵ thần | ⭐⭐⭐⭐ |
| S09 — Hôn nhân | ⭐⭐⭐⭐⭐ |
| S10 — Sức khỏe | ⭐⭐⭐⭐⭐ |
| S11 — Tài vận | ⭐⭐⭐⭐⭐ |
| AI Status | ⭐⭐⭐⭐⭐ |
| System Status | ⭐⭐⭐⭐ |

---

# 27. Evolution Policy

Status Panel là Foundation Pattern.

Các phiên bản mới chỉ được thay đổi:

- Responsive
- Typography
- Khoảng cách

Không được thay đổi:

- Reading Flow
- Component Tree
- Information Hierarchy
- Semantic Status

---

# 28. Relationship với các Pattern khác

Status Panel thường kết hợp với:

PATTERN_05 — Decision Card
→ Đưa ra kết luận.

PATTERN_06 — Information List
→ Liệt kê các nguyên nhân.

PATTERN_04 — Comparison Bar
→ Trực quan hóa các chỉ số.

Status Panel đóng vai trò là cầu nối giữa "kết luận" và "phân tích chi tiết".

---

# 29. Freeze Statement

PATTERN_07_STATUS_PANEL.md là tài liệu chuẩn duy nhất mô tả Status Panel của BTE Platform.

Mọi màn hình sử dụng Status Panel phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

**PATTERN_07_STATUS_PANEL.md là Single Source of Truth.**