# BTE Platform

# Portal Grid System

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Depends On:

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_LAYOUT_SYSTEM.md

Applies To:

- applications/customer_portal
- Desktop
- Tablet
- Mobile

---

# 1. Purpose

Portal Grid System định nghĩa hệ thống lưới chuẩn cho toàn bộ Portal BTE.

Grid System không quy định:

- màu sắc
- typography
- spacing
- component

Grid System chỉ định nghĩa:

- vùng chia cột
- vùng đọc
- nhịp bố cục
- quy tắc phân bổ nội dung

Grid phải phục vụ Reading Flow.

Không phải ngược lại.

---

# 2. Core Principle

Grid không tồn tại để chia đều màn hình.

Grid tồn tại để:

- nhấn mạnh thông tin quan trọng
- tạo nhịp đọc
- giảm Cognitive Load
- hỗ trợ Decision Flow

Business Priority

↓

Information Priority

↓

Grid

↓

Component

Không được thiết kế Grid trước Business.

---

# 3. Canonical Grid Model

Portal sử dụng Canonical 12-Column Grid.

```

|1|2|3|4|5|6|7|8|9|10|11|12|

```

Desktop luôn bắt đầu từ Grid này.

Các tỷ lệ phổ biến:

- 12
- 8 + 4
- 6 + 6
- 4 + 8
- 3 + 9

Không sử dụng Grid tùy ý.

---

# 4. Reading Grid

Portal có hai loại Grid.

## Structural Grid

Dùng cho:

- Header
- TOC
- Main Layout

---

## Reading Grid

Dùng cho:

- Hero
- Summary
- Four Pillars
- Five Elements
- Strength
- Interpretation

Reading Grid luôn ưu tiên chiều dọc.

---

# 5. Desktop Grid

Desktop:

12 Columns

Container:

Centered

Nội dung luôn nằm trong Reading Region.

Không kéo full-width nếu không có lý do nghiệp vụ.

---

# 6. Tablet Grid

Tablet:

8 Columns

TOC có thể thu gọn.

Section vẫn giữ đúng Reading Order.

Không đổi Information Hierarchy.

---

# 7. Mobile Grid

Mobile:

4 Columns

Toàn bộ BusinessRegion:

Single Column.

Không chia đôi nội dung quan trọng.

---

# 8. Section Grid Rules

## S00

1 hàng.

Không chia nhiều cột.

---

## S01

Desktop:

8 + 4

Hero

↓

Decision

Tablet:

12

↓

12

Mobile:

Stack

---

## S02

6 + 6

hoặc

12

---

## S03

Desktop:

4 Pillars

=

4 cột

Tablet:

2 × 2

Mobile:

1 × 4

---

## S04

Desktop:

6 + 6

Mobile:

Stack

---

## S05

Desktop:

6 + 6

---

## S06

Desktop:

3 × 3 × 3 × 3

hoặc

Responsive Cards

---

## S07

Adaptive Grid

---

## S08

Single Reading Column

Không chia đôi.

---

# 9. Grid Priority

Grid phải phản ánh Business Priority.

Ví dụ:

Identity

↓

chiếm nhiều chiều ngang hơn

Decision

↓

rộng hơn Metadata

Learning

↓

không cạnh tranh Main Content

---

# 10. Grid Anti-Patterns

Không được:

❌ Chia đều mọi Section.

❌ Hero = Decision.

❌ Learning = Main Content.

❌ Dashboard Widget Layout.

❌ Masonry.

❌ Pinterest Style.

---

# 11. Responsive Transformation

Desktop

↓

Tablet

↓

Mobile

được phép:

- đổi số cột

- stack

- collapse

Không được:

- đổi Reading Flow

- đổi Decision Flow

---

# 12. Nested Grid

Một Section được phép có Grid riêng.

Ví dụ:

S03

↓

4 Pillars

↓

mỗi Pillar

↓

Internal Layout

Nhưng Nested Grid không được phá Grid cha.

---

# 13. Grid Density

Portal hướng tới:

Medium–High Density.

Không tạo:

Dashboard nhiều widget.

Không tạo:

Landing Page quá nhiều khoảng trắng.

---

# 14. Grid Validation Checklist

□ Grid đúng Blueprint.

□ Reading Flow đúng.

□ Không có khoảng trắng vô nghĩa.

□ Không có cuộn ngang.

□ Không có Grid ngẫu nhiên.

□ Hero nổi bật hơn Decision.

□ Decision nổi bật hơn Metadata.

---

# 15. Grid Tokens

Các Blueprint chỉ sử dụng Token chuẩn:

- Grid12
- Grid8
- Grid4
- Split84
- Split66
- Split39
- Stack
- ReadingColumn
- AdaptiveCards

Không tự định nghĩa.

---

# 16. Relationship

Grid System là nền tảng cho:

- PORTAL_SPACING_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_COMPONENT_USAGE.md
- Tất cả Screen Blueprints

Blueprint không được định nghĩa Grid mới.

---

# 17. Grid Governance

Thay đổi Grid phải:

Architecture Review

↓

Blueprint Update

↓

Implementation

Không sửa Grid trực tiếp trong React.

---

# 18. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Canonical Grid System |

# 19. Grid Tokens Reference

## 19.1 Purpose

Grid Tokens là ngôn ngữ chuẩn để mô tả bố cục trong toàn bộ Portal BTE.

Grid Tokens không phải CSS Utility.

Grid Tokens không phải Tailwind Class.

Grid Tokens là các khái niệm kiến trúc được sử dụng thống nhất trong:

- Foundation Documents
- Screen Blueprints
- React Implementation
- Product Review

Mọi Blueprint phải tham chiếu Grid Token thay vì mô tả Grid bằng văn bản tự do.

---

## 19.2 Canonical Grid Tokens

| Token | Desktop | Tablet | Mobile | Mục đích |
|---------|----------|----------|----------|----------|
| `Grid12` | 12 cột | — | — | Lưới chuẩn Desktop |
| `Grid8` | — | 8 cột | — | Lưới chuẩn Tablet |
| `Grid4` | — | — | 4 cột | Lưới chuẩn Mobile |
| `Split84` | 8 + 4 | 12 | Stack | Hero + Decision |
| `Split66` | 6 + 6 | 8 | Stack | Hai vùng ngang cân bằng |
| `Split39` | 3 + 9 | 8 | Stack | Sidebar + Content |
| `ReadingColumn` | 1 cột | 1 cột | 1 cột | Luận giải dài |
| `AdaptiveCards` | Tự co giãn | Tự co giãn | Stack | Card thống kê |

---

## 19.3 Screen Token Mapping

| Screen | Grid Token |
|----------|------------|
| S00 | ReadingColumn |
| S01 | Split84 |
| S02 | Split66 |
| S03 | AdaptiveCards |
| S04 | Split66 |
| S05 | Split66 |
| S06 | AdaptiveCards |
| S07 | AdaptiveCards |
| S08 | ReadingColumn |
| Learning | ReadingColumn |

Blueprint không được tự định nghĩa Grid ngoài danh sách này nếu chưa có Architecture Review.

---

## 19.4 Naming Convention

Grid Token phải tuân theo quy tắc:

```
GridXX

SplitXX

ReadingColumn

AdaptiveCards
```

Không được tạo tên tùy ý như:

```
HeroGrid

BigGrid

MyLayout

CustomGrid
```

---

## 19.5 Token Stability

Grid Tokens là một phần của Foundation.

Không được:

- đổi tên
- đổi ý nghĩa
- tái sử dụng sai mục đích

Nếu cần Token mới:

Architecture Review

↓

Foundation Update

↓

Blueprint Update

# 20. Grid Evolution Policy

## 20.1 Purpose

Grid System phải phát triển theo hướng mở rộng nhưng vẫn giữ tính ổn định.

Mọi thay đổi Grid đều phải đảm bảo:

- Reading Flow không đổi.
- Decision Flow không đổi.
- Information Hierarchy không đổi.

---

## 20.2 Evolution Rules

### V1.x

Được phép:

- Tối ưu Responsive.
- Thêm Grid Token mới nếu thật sự cần.
- Điều chỉnh kích thước cột.

Không được:

- Đổi Canonical Grid.
- Đổi Split84.
- Đổi ReadingColumn.
- Đổi Mapping Screen.

---

### V2.x

Có thể:

- Thêm Business Module.
- Thêm Grid Pattern mới.

Bắt buộc:

- Tương thích ngược với Grid Tokens V1.

---

## 20.3 Extension Rules

Các module:

- Phong Thủy
- Chọn ngày
- Sim số
- Kỳ Môn
- Báo cáo

phải tái sử dụng Grid Token chuẩn.

Không được xây Grid riêng.

---

## 20.4 Compatibility Rules

Grid mới phải:

✓ Không phá Responsive.

✓ Không phá Reading Flow.

✓ Không phá Decision Flow.

✓ Không làm Blueprint cũ mất hiệu lực.

---

## 20.5 Freeze Policy

Sau khi Sprint UI hoàn thành:

Grid System được đánh dấu:

**FROZEN**

Trong Sprint Integration:

Không được:

- đổi Grid.
- đổi tỷ lệ chia cột.
- đổi Token.

Chỉ sửa lỗi triển khai.

---

## 20.6 Success Criteria

Grid Evolution thành công khi:

- Blueprint cũ vẫn dùng được.
- Module mới dùng chung Grid.
- Người dùng không phải học lại bố cục.
- AI không cần suy diễn Grid.

# 21. Grid Governance

## 21.1 Purpose

Grid Governance quy định cách quản lý toàn bộ Grid System của Portal BTE.

Mục tiêu:

- Bảo vệ kiến trúc.
- Đảm bảo tính nhất quán.
- Ngăn việc sửa Grid tùy ý.

---

## 21.2 Governance Levels

| Level | Ví dụ | Cần Architecture Review |
|---------|--------|-------------------------|
| Foundation | Grid Tokens | ✅ |
| Blueprint | Mapping Screen | ⚠ |
| React | CSS Grid | ❌ |
| Styling | Gap / Width | ❌ |

---

## 21.3 Change Workflow

Mọi thay đổi Grid phải tuân theo:

```
Business Requirement

↓

Architecture Proposal

↓

PO Approval

↓

Grid System Update

↓

Blueprint Update

↓

Implementation

↓

Screenshot Review

↓

Freeze
```

Không được sửa React trước.

---

## 21.4 Review Gates

Một thay đổi Grid chỉ được chấp nhận khi:

□ Reading Flow giữ nguyên.

□ Decision Flow giữ nguyên.

□ Responsive đúng.

□ Không tạo cuộn ngang.

□ Không phá Blueprint.

□ Product Owner phê duyệt.

---

## 21.5 Documentation First

Mọi thay đổi Grid phải cập nhật:

1.

Grid System

↓

2.

Blueprint

↓

3.

React

Không được làm ngược.

---

## 21.6 Canonical Source

Thứ tự ưu tiên:

```
BTE_UI_BIBLE

↓

Design Philosophy

↓

Reading Flow

↓

Decision Flow

↓

Layout System

↓

Grid System

↓

Blueprint

↓

React
```

Code không phải nguồn sự thật.

---

## 21.7 Grid Quality Metrics

Một Grid đạt chuẩn khi:

- Reading Flow rõ ràng.
- Không có vùng chết.
- Không có khoảng trắng vô nghĩa.
- Không có thành phần tranh chấp thị giác.
- Responsive nhất quán.
- Business Priority được phản ánh qua bố cục.

---

## 21.8 Closing Statement

`PORTAL_GRID_SYSTEM.md` là tiêu chuẩn kiến trúc chính thức cho toàn bộ hệ thống Grid của Portal BTE.

Mọi Screen Blueprint, Component Layout và React Implementation phải tuân thủ tài liệu này.

Không Blueprint nào được định nghĩa một hệ thống Grid riêng ngoài những gì được mô tả trong tài liệu này.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Canonical Portal Grid System |