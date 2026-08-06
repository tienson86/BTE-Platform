# BTE Platform

# PATTERN_08 — KNOWLEDGE CARD

---

Version

1.0.0

Status

FROZEN

Module

UI Design System

Pattern

08

Name

Knowledge Card

Type

Foundation Pattern

---

# 1. Mục đích

Knowledge Card là Pattern tiêu chuẩn dùng để trình bày một đơn vị tri thức (Knowledge Unit) dưới dạng ngắn gọn, có cấu trúc và dễ tiếp thu.

Khác với Information List:

Information List

↓

Liệt kê thông tin.

Knowledge Card

↓

Giải thích một khái niệm.

Knowledge Card giúp người dùng:

• Hiểu một thuật ngữ.

• Hiểu một quy luật.

• Hiểu một khái niệm.

• Hiểu ý nghĩa của kết quả phân tích.

Đây là Pattern quan trọng nhất của tầng **Interpretation**.

---

# 2. Triết lý

Explain.

Don't Teach.

Knowledge Card không phải giáo trình.

Knowledge Card không phải bài viết.

Knowledge Card chỉ giúp người dùng:

Hiểu nhanh.

Nhớ lâu.

Áp dụng được.

---

# 3. Khi nào sử dụng

Áp dụng cho:

• Giải thích Dụng thần.

• Giải thích Hỷ thần.

• Giải thích Kỵ thần.

• Giải thích Thập thần.

• Giải thích Thần sát.

• Giải thích Cách cục.

• Giải thích Đại vận.

• Giải thích Thuật ngữ.

• AI Knowledge.

---

# 4. Không sử dụng

Không dùng cho:

✗ Dashboard

✗ KPI

✗ Timeline

✗ Data Table

✗ Decision Card

✗ Status Panel

✗ Paragraph dài

---

# 5. Reading Flow

```
Tiêu đề

↓

Định nghĩa

↓

Ý nghĩa

↓

Điểm cần nhớ

↓

Xem thêm
```

Người dùng phải hiểu được nội dung chỉ trong khoảng 30 giây.

---

# 6. Canonical Layout

```
┌──────────────────────────────────────────────┐

DỤNG THẦN

──────────────────────────────────────────────

ĐỊNH NGHĨA

Dụng thần là Ngũ hành được lựa chọn
để cân bằng Mệnh cục.

──────────────────────────────────────────────

Ý NGHĨA

Giúp điều hòa Ngũ hành,
tăng sự ổn định và hỗ trợ vận trình.

──────────────────────────────────────────────

ĐIỂM CẦN NHỚ

• Không phải lúc nào cũng là hành mạnh.

• Phụ thuộc toàn bộ Mệnh cục.

──────────────────────────────────────────────

Xem kiến thức đầy đủ →

└──────────────────────────────────────────────┘
```

---

# 7. Component Tree

```
KnowledgeCard

├── Header
│
├── Definition
│
├── Explanation
│
├── KeyPoints
│
└── LearnMore
```

---

# 8. Header

Hiển thị tên khái niệm.

Ví dụ

```
DỤNG THẦN

THẬP THẦN

THẦN SÁT
```

Không quá dài.

---

# 9. Definition

Định nghĩa ngắn.

Giới hạn:

2 dòng.

Ví dụ

```
Dụng thần là Ngũ hành
được dùng để cân bằng Mệnh cục.
```

Không viết Paragraph.

---

# 10. Explanation

Giải thích ngắn.

Giới hạn:

3 dòng.

Ví dụ

```
Giúp điều hòa các hành,
hạn chế mất cân bằng
và cải thiện tổng thể.
```

Không vượt quá.

---

# 11. Key Points

Danh sách:

3–5 ý.

Ví dụ

```
• Không cố định.

• Thay đổi theo Mệnh cục.

• Là nền tảng của luận giải.
```

Không quá 5 ý.

---

# 12. Learn More

Một liên kết duy nhất.

Ví dụ

```
Xem kiến thức đầy đủ →
```

Không dùng Button lớn.

Không CTA Marketing.

---

# 13. Information Hierarchy

★★★★★

Header

★★★★☆

Definition

★★★★☆

Explanation

★★★☆☆

Key Points

★★☆☆☆

Learn More

---

# 14. Typography

Header

18 px

700

---

Definition

15 px

600

---

Explanation

14 px

400

---

Key Point

14 px

500

---

Learn More

14 px

600

---

# 15. White Space

Padding

20 px

Header Bottom

16 px

Definition Bottom

16 px

Explanation Bottom

20 px

Key Points Bottom

20 px

Ưu tiên khoảng trắng.

---

# 16. Card Style

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

# 17. Accessibility

Contrast đạt WCAG AA.

Learn More keyboard focus.

Không phụ thuộc màu sắc.

---

# 18. Responsive

Desktop

One Card

Tablet

One Card

Mobile

One Card

Reading Flow giữ nguyên.

---

# 19. Những điều KHÔNG được phép

Không sử dụng:

✗ Đoạn văn dài

✗ Hơn 5 Key Points

✗ Animation

✗ Gradient

✗ Glass

✗ Accordion mặc định

✗ Tooltip

✗ Quảng cáo

---

# 20. Các màn hình sử dụng

Có thể áp dụng cho:

✓ S06 — Dụng thần

✓ S07 — Hỷ thần

✓ S08 — Kỵ thần

✓ Giải thích Thập thần

✓ Giải thích Thần sát

✓ Knowledge Base

✓ AI Explain

✓ Glossary

---

# 21. Design Principles

Understanding

>

Reading

Knowledge

>

Decoration

Clarity

>

Density

Progressive Disclosure

>

Information Dump

---

# 22. Reusability

Knowledge Card phải tái sử dụng được cho:

Customer Portal

Knowledge Center

Analysis Console

Admin Portal

Desktop

Tablet

Mobile

Chỉ thay đổi nội dung.

Không thay đổi cấu trúc.

---

# 23. Acceptance Criteria

PASS khi:

✓ Người dùng hiểu khái niệm trong dưới 30 giây.

✓ Definition ≤ 2 dòng.

✓ Explanation ≤ 3 dòng.

✓ Có 3–5 Key Points.

✓ Chỉ có 1 Learn More Link.

✓ Không biến thành bài viết.

---

# 24. Design Decision Record

Knowledge Card được thiết kế để chuyển đổi tri thức chuyên môn thành nội dung dễ tiếp cận.

Đây không phải là nơi trình bày toàn bộ học thuật.

Đây là "điểm dừng" giúp người dùng:

Hiểu khái niệm

↓

Hiểu ý nghĩa

↓

Muốn tìm hiểu sâu hơn

Knowledge Card là cầu nối giữa Analysis và Knowledge Base.

---

# 25. Mapping

Pattern này là nền tảng cho:

| Module | Mức độ |
|----------|---------|
| S06 — Dụng thần | ⭐⭐⭐⭐⭐ |
| S07 — Hỷ thần | ⭐⭐⭐⭐⭐ |
| S08 — Kỵ thần | ⭐⭐⭐⭐ |
| Knowledge Center | ⭐⭐⭐⭐⭐ |
| AI Explain | ⭐⭐⭐⭐⭐ |
| Thuật ngữ Bát Tự | ⭐⭐⭐⭐⭐ |

---

# 26. Evolution Policy

Knowledge Card là Foundation Pattern.

Được phép thay đổi:

- Typography responsive

- Khoảng cách

- Responsive Layout

Không được thay đổi:

- Reading Flow

- Component Tree

- Information Hierarchy

- Progressive Disclosure Principle

---

# 27. Relationship với các Pattern khác

Knowledge Card thường đi sau:

PATTERN_05 — Decision Card

↓

Đưa ra kết luận.

PATTERN_06 — Information List

↓

Liệt kê các nguyên nhân.

Knowledge Card

↓

Giải thích vì sao.

Đây là tầng "giải thích tri thức" của BTE.

---

# 28. Future Extensions

Knowledge Card có thể mở rộng:

• Video giải thích

• Minh họa trực quan

• Ví dụ thực tế

• FAQ

• Liên kết tới Knowledge Base

Nhưng các nội dung mở rộng phải nằm sau phần cốt lõi.

Không được làm ảnh hưởng đến khả năng đọc nhanh.

---

# 29. Freeze Statement

PATTERN_08_KNOWLEDGE_CARD.md là tài liệu chuẩn duy nhất mô tả Knowledge Card của BTE Platform.

Mọi màn hình sử dụng Knowledge Card phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

**PATTERN_08_KNOWLEDGE_CARD.md là Single Source of Truth.**