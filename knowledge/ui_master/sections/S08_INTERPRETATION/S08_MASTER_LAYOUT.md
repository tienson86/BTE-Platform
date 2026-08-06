# BTE Platform

# S08 — LUẬN GIẢI TỔNG HỢP

# S08_MASTER_LAYOUT.md

---

Version

1.0.0

Status

CANONICAL

Module

Desktop Canonical UI

Section

S08

Name

Luận giải tổng hợp

Pattern

PATTERN_05_DECISION_CARD

PATTERN_06_INFORMATION_LIST

PATTERN_10_REPORT_BLOCK

Related Engine

Interpretation Engine

---

# 1. Mục tiêu

S08 là Section quan trọng nhất của toàn bộ Desktop Canonical.

Đây là nơi toàn bộ dữ liệu từ Analysis Engine và Interpretation Engine được chuyển đổi thành tri thức có thể hiểu ngay.

Mục tiêu không phải hiển thị dữ liệu.

Mục tiêu là:

**Giúp người dùng hiểu lá số trong dưới 30 giây.**

---

# 2. Reading Flow

```
Header

↓

Executive Summary

↓

Tổng luận

↓

Điểm mạnh

↓

Điểm cần lưu ý

↓

Gợi ý hành động

↓

Đọc luận giải đầy đủ
```

Reading Flow này là bắt buộc.

Không được thay đổi.

---

# 3. Canonical Layout

```
┌──────────────────────────────────────────────────────┐

S08 – LUẬN GIẢI TỔNG HỢP

──────────────────────────────────────────────────────

┌──────────────────────────────────────────────────┐
│            TỔNG QUAN LUẬN GIẢI                    │
│                                                  │
│ Bạn là người có tố chất lãnh đạo, quyết đoán,    │
│ tư duy nhanh và khả năng truyền cảm hứng.        │
│ Mệnh cục thiên về Hỏa nên hành động mạnh mẽ,     │
│ tuy nhiên cần cân bằng cảm xúc và sự kiên nhẫn. │
└──────────────────────────────────────────────────┘

──────────────────────────────────────────────────────

🟢 ĐIỂM MẠNH

✓ Khả năng lãnh đạo

✓ Quyết đoán

✓ Ý chí mạnh

✓ Có tinh thần trách nhiệm

──────────────────────────────────────────────────────

🟠 CẦN LƯU Ý

• Hỏa quá vượng

• Thiếu Thủy

• Dễ nóng vội

• Cần lắng nghe nhiều hơn

──────────────────────────────────────────────────────

🔵 GỢI Ý HÀNH ĐỘNG

→ Phát triển vai trò quản lý

→ Bổ sung yếu tố Thủy

→ Làm việc theo nhóm

→ Kiểm soát cảm xúc

──────────────────────────────────────────────────────

Đọc luận giải đầy đủ →

└──────────────────────────────────────────────────────┘
```

---

# 4. Component Tree

```
S08

├── Header
│
├── ExecutiveSummaryCard
│
├── StrengthSection
│   ├── Title
│   └── List
│
├── Divider
│
├── WarningSection
│   ├── Title
│   └── List
│
├── Divider
│
├── ActionSection
│   ├── Title
│   └── List
│
├── Divider
│
└── ReadMoreLink
```

---

# 5. Header

Hiển thị:

```
S08 – LUẬN GIẢI TỔNG HỢP
```

Typography

16 px

700

BTE Red

Margin Bottom

16 px

---

# 6. Executive Summary Card

Đây là vùng quan trọng nhất.

Không phải Text Block.

Đây là Executive Card.

```
┌──────────────────────────────┐

TỔNG QUAN LUẬN GIẢI

Bạn là người có tố chất lãnh đạo...

...

└──────────────────────────────┘
```

Background

#FFF8EF

Radius

10 px

Padding

16 px

Border

1 px

Neutral 100

Shadow

Enterprise Shadow

---

# 7. Nội dung Executive Summary

Độ dài:

80–120 từ

Không dài hơn.

Không xuống quá:

5 dòng.

---

# 8. Strength Section

Title

```
🟢 ĐIỂM MẠNH
```

Danh sách

✓ Khả năng lãnh đạo

✓ Quyết đoán

✓ Ý chí mạnh

✓ Tư duy chiến lược

Mỗi dòng:

Icon

+

Text

---

# 9. Warning Section

Title

```
🟠 CẦN LƯU Ý
```

Danh sách

• Hỏa quá mạnh

• Thiếu Thủy

• Dễ nóng vội

• Thiếu kiên nhẫn

Không dùng màu đỏ đậm.

Đây là Warning.

Không phải Error.

---

# 10. Action Section

Title

```
🔵 GỢI Ý HÀNH ĐỘNG
```

Danh sách

→ Làm quản lý

→ Phát triển kỹ năng lắng nghe

→ Tăng yếu tố Thủy

→ Cân bằng nghỉ ngơi

Đây là Actionable Advice.

Không phải luận giải.

---

# 11. Divider

Giữa các khối

1 px

Inset

Neutral 200

Margin

16 px

---

# 12. Link

```
Đọc luận giải đầy đủ →
```

Center

14 px

600

BTE Red

Text only.

Không Button.

---

# 13. Information Hierarchy

★★★★★

Executive Summary

★★★★☆

Điểm mạnh

★★★★☆

Điểm cần lưu ý

★★★★☆

Gợi ý hành động

★★☆☆☆

Link

---

# 14. White Space

Padding

20 px

Khoảng cách giữa các Block

16 px

Khoảng cách Item

8 px

Không giảm.

---

# 15. Maximum Content

Executive Summary

120 từ

Strength

6 mục

Warning

6 mục

Action

6 mục

Nếu vượt

↓

Rút gọn.

Không kéo dài Card.

---

# 16. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có dữ liệu luận giải.
```

Không để khoảng trắng.

---

# 17. Responsive

Desktop

Một Card.

Tablet

Một Card.

Mobile

Một Card.

Reading Flow giữ nguyên.

---

# 18. Accessibility

Contrast đạt WCAG AA.

Không dùng màu làm tín hiệu duy nhất.

Icon có Label.

Keyboard Focus.

---

# 19. Những điều KHÔNG được phép

Không dùng

✗ KPI

✗ Pie Chart

✗ Gauge

✗ Radar

✗ Dashboard

✗ JSON

✗ Rule ID

✗ Engine Debug

✗ AI Prompt

✗ Markdown dài

✗ Accordion

---

# 20. Mapping

Input

```
InterpretationResult
```

↓

ExecutiveSummary

↓

Strengths[]

↓

Warnings[]

↓

Actions[]

↓

UI

S08 không tự tính toán.

---

# 21. Performance

Render

<30 ms

Không Animation.

Không Lazy.

Không Infinite Scroll.

---

# 22. Design Principles

Interpretation

>

Description

Decision

>

Observation

Action

>

Knowledge

Executive Summary

>

Long Report

---

# 23. Relationship

```
S03

↓

S04

↓

S05

↓

S06

↓

S07

↓

S08

↓

Report Engine
```

S08 là cầu nối giữa Dashboard và Report.

---

# 24. UX Principles

Người dùng phải:

✓ Hiểu mình là người như thế nào.

✓ Biết điểm mạnh.

✓ Biết điểm cần cải thiện.

✓ Có định hướng hành động.

✓ Muốn đọc tiếp báo cáo.

---

# 25. Acceptance Criteria

PASS khi

✓ Executive Summary đọc trong dưới 20 giây.

✓ Không có đoạn văn dài.

✓ Danh sách rõ ràng.

✓ Không hiển thị dữ liệu kỹ thuật.

✓ Không cần cuộn trên Desktop.

✓ Đồng bộ Desktop Canonical.

---

# 26. Design Decision Record

Khác với các phần mềm Bát Tự truyền thống hiển thị một đoạn luận giải dài ngay trên Dashboard, S08 của BTE được thiết kế theo mô hình:

```
Executive Summary

↓

Strengths

↓

Warnings

↓

Actions

↓

Full Report
```

Thiết kế này giúp người dùng:

- Hiểu nhanh.
- Ghi nhớ tốt hơn.
- Chuyển đổi sang hành động dễ hơn.
- Không bị quá tải thông tin.

Đây là triết lý cốt lõi của BTE:

**"Hiểu trước – Hành động sau – Đào sâu khi cần."**

---

# 27. Freeze Statement

S08_MASTER_LAYOUT.md là tài liệu chuẩn mô tả bố cục chính thức của Section S08.

Frontend phải triển khai đúng:

- Component Tree
- Reading Flow
- Information Hierarchy
- White Space
- Typography
- Executive Summary

Không được tự ý thay đổi nếu chưa cập nhật tài liệu này.

Nếu có khác biệt giữa mã nguồn và tài liệu thì:

**S08_MASTER_LAYOUT.md là Single Source of Truth cho Layout của S08.**