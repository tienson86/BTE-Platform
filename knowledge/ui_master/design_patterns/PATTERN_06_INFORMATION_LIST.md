# BTE Platform

# PATTERN_06 — INFORMATION LIST

---

Version

1.0.0

Status

FROZEN

Module

UI Design System

Pattern

06

Name

Information List

Type

Foundation Pattern

---

# 1. Mục đích

Information List là Pattern tiêu chuẩn dùng để hiển thị danh sách thông tin, đặc điểm, nhận xét hoặc kết quả phân tích ngắn theo từng dòng.

Đây là Pattern được sử dụng nhiều nhất trong tầng Analysis của BTE Platform.

Pattern này giúp người dùng đọc nhanh các thông tin quan trọng mà không phải đọc đoạn văn dài.

Information List ưu tiên:

- Quét nhanh
- Dễ nhớ
- Dễ mở rộng
- Dễ tái sử dụng

---

# 2. Triết lý

One idea.

One row.

Một dòng chỉ truyền tải một ý.

Không gộp nhiều ý vào cùng một dòng.

Không viết thành đoạn văn.

---

# 3. Khi nào sử dụng

Áp dụng cho:

• Yếu tố chính

• Điểm mạnh

• Điểm yếu

• Dụng thần

• Hỷ thần

• Kỵ thần

• Khuyến nghị

• Nhận xét AI

• Điều nên làm

• Điều nên tránh

• Điều kiện thuận lợi

• Điều kiện bất lợi

---

# 4. Không sử dụng

Không dùng cho:

✗ Paragraph

✗ Timeline

✗ Dashboard

✗ KPI

✗ Data Table

✗ Biểu đồ

---

# 5. Reading Flow

```
Header

↓

Item 1

↓

Item 2

↓

Item 3

↓

Item 4
```

Người dùng luôn đọc từ trên xuống dưới.

Không có phân nhánh.

---

# 6. Canonical Layout

```
┌──────────────────────────────────────────┐

YẾU TỐ CHÍNH

──────────────────────────────────────────

● Nhật chủ đắc lệnh

● Được Mộc sinh trợ

● Hỏa vượng

● Kim suy

└──────────────────────────────────────────┘
```

---

# 7. Component Tree

```
InformationList

├── Header
│
└── List
    │
    ├── InformationItem
    ├── InformationItem
    ├── InformationItem
    └── InformationItem
```

---

# 8. Information Item

Mỗi Item gồm:

```
Indicator

↓

Text
```

Không có mô tả phụ.

Không có Paragraph.

---

# 9. Indicator

Indicator là thành phần định hướng thị giác.

Được phép dùng:

✓ Dot

✓ Check

✓ Arrow

✓ Semantic Dot

Không dùng:

✗ Emoji

✗ Sticker

✗ 3D Icon

✗ Decorative Icon

---

# 10. Semantic Indicators

Tích cực

● Xanh lá

---

Trung tính

● Vàng

---

Cần chú ý

● Cam

---

Bất lợi

● Đỏ

---

Thông tin

● Xanh dương

Không sử dụng màu khác.

---

# 11. Typography

Header

16 px

700

---

Item

14 px

500

---

Indicator

12 px

Không lớn hơn chữ.

---

# 12. White Space

Padding

20 px

Khoảng cách Item

12 px

Khoảng cách Header

16 px

Không để Item dính nhau.

---

# 13. Card Style

Background

White

Radius

12 px

Border

1 px

Shadow

Soft

Theo Enterprise Design System.

---

# 14. Maximum Items

Khuyến nghị:

4–6 Item.

Tối đa:

8 Item.

Nếu nhiều hơn:

Chia thành nhiều nhóm.

Không tạo danh sách quá dài.

---

# 15. Text Rules

Mỗi Item

≤ 1 dòng.

Nếu bắt buộc:

≤ 2 dòng.

Không viết Paragraph.

Ví dụ tốt:

```
Nhật chủ đắc lệnh
```

Ví dụ không tốt:

```
Nhật chủ được sinh vào tháng vượng,
được nhiều Can sinh trợ nên...
```

---

# 16. Information Hierarchy

★★★★★

Header

★★★★☆

Item

★★★☆☆

Indicator

Indicator chỉ hỗ trợ.

Không được nổi bật hơn nội dung.

---

# 17. Accessibility

Contrast đạt WCAG AA.

Indicator không phải phương tiện duy nhất truyền tải thông tin.

Luôn có văn bản.

---

# 18. Responsive

Desktop

Vertical List

Tablet

Vertical List

Mobile

Vertical List

Không thay đổi Reading Flow.

---

# 19. Những điều KHÔNG được phép

Không dùng:

✗ Numbering liên tục nếu không cần

✗ Paragraph

✗ Divider giữa từng dòng

✗ Icon quá lớn

✗ Animation

✗ Gradient

✗ Glass Effect

✗ Accordion

---

# 20. Các màn hình sử dụng

Đã áp dụng:

✓ S05 — Yếu tố chính

Có thể tái sử dụng:

✓ S06 — Dụng thần

✓ S07 — Hỷ thần

✓ S08 — Kỵ thần

✓ S09 — Hôn nhân

✓ S10 — Sự nghiệp

✓ AI Summary

✓ Recommendation

---

# 21. Design Principles

Scanning

>

Reading

Recognition

>

Decoration

Clarity

>

Density

Information

>

Visual Effects

---

# 22. Reusability

Pattern này phải sử dụng được cho:

Customer Portal

Analysis Console

Admin Portal

CRM

Desktop

Tablet

Mobile

Không tạo nhiều biến thể.

Chỉ thay đổi dữ liệu.

---

# 23. Acceptance Criteria

PASS khi:

✓ Người dùng đọc hết danh sách trong dưới 10 giây.

✓ Không có Paragraph.

✓ Mỗi dòng chỉ truyền tải một ý.

✓ Indicator nhất quán.

✓ Danh sách dễ mở rộng.

---

# 24. Design Decision Record

Information List là Pattern chuẩn cho toàn bộ các kết quả phân tích ngắn của BTE Platform.

Pattern này được thiết kế để thay thế các đoạn văn dài bằng các ý ngắn, rõ ràng và có khả năng quét nhanh.

Mục tiêu là giúp người dùng:

Hiểu nhanh

↓

Ghi nhớ nhanh

↓

Ra quyết định nhanh

Đây là một trong những Pattern quan trọng nhất của tầng Analysis.

---

# 25. Mapping

Pattern này là nền tảng cho:

| Module | Mức độ |
|----------|---------|
| S05 — Yếu tố chính | ⭐⭐⭐⭐⭐ |
| S06 — Dụng thần | ⭐⭐⭐⭐⭐ |
| S07 — Hỷ thần | ⭐⭐⭐⭐ |
| S08 — Kỵ thần | ⭐⭐⭐⭐ |
| AI Summary | ⭐⭐⭐⭐⭐ |
| Recommendation | ⭐⭐⭐⭐⭐ |

---

# 26. Evolution Policy

Information List là Foundation Pattern.

Các phiên bản mới chỉ được phép thay đổi:

- Responsive Layout
- Typography responsive
- Khoảng cách

Không được thay đổi:

- Reading Flow
- One Idea = One Row
- Component Tree
- Information Hierarchy

---

# 27. Freeze Statement

PATTERN_06_INFORMATION_LIST.md là tài liệu chuẩn duy nhất mô tả Information List của BTE Platform.

Mọi màn hình sử dụng danh sách thông tin phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

PATTERN_06_INFORMATION_LIST.md là Single Source of Truth.