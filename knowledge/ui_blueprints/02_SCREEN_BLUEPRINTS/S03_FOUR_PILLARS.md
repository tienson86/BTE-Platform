# BTE Platform

# S03 Blueprint — Four Pillars

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Screen

BaZi Result

Depends On

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_GRID_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_TYPOGRAPHY_SYSTEM.md
- PORTAL_SCREEN_SPECIFICATIONS.md

---

# 1. Purpose

S03 trình bày cấu trúc đầy đủ của lá số Bát Tự.

Đây là tầng Evidence đầu tiên sau khi người dùng đã hiểu:

- Tôi là ai.
- Tôi mạnh hay yếu.
- Điều gì quan trọng nhất.

S03 không đưa ra kết luận mới.

S03 chỉ cung cấp bằng chứng cấu trúc.

---

# 2. Business Goal

Người dùng phải hiểu:

- Lá số gồm bốn trụ gì.
- Nhật Chủ nằm ở đâu.
- Quan hệ giữa bốn trụ.
- Các dữ liệu nền của từng trụ.

S03 giúp xác nhận tính chính xác của kết quả trước khi đọc phân tích sâu.

---

# 3. User Questions

S03 trả lời:

✓ Bốn trụ của tôi gồm những gì?

✓ Nhật Chủ nằm ở đâu?

✓ Thiên Can và Địa Chi từng trụ là gì?

✓ Mỗi trụ có những thông tin nào?

Không trả lời:

- mạnh hay yếu
- dụng thần
- thập thần
- thần sát

---

# 4. Decision Goal

Sau khi xem S03,

người dùng quyết định:

"Tôi đã hiểu cấu trúc của lá số."

Tiếp tục:

↓

S04

---

# 5. Reading Goal

≤30 giây.

Reading Flow

Năm

↓

Tháng

↓

Ngày (Nhật Chủ)

↓

Giờ

Không đảo.

---

# 6. Information Architecture

Mỗi Pillar gồm:

## Primary

- Thiên Can
- Địa Chi

---

## Secondary

- Tàng Can
- Nạp Âm

---

## Supporting

- Trường Sinh
- Ghi chú (nếu có)

---

Không hiển thị dữ liệu ngoài Pillar.

---

# 7. Visual Hierarchy

Visual Priority

Ngày (Nhật Chủ)

★★★★★

↓

Tháng

★★★★☆

↓

Năm

★★★☆☆

↓

Giờ

★★★☆☆

Ngày luôn nổi bật hơn ba trụ còn lại.

---

# 8. Layout Blueprint

Desktop

```
+-----------------------------------------------------------+

YEAR

MONTH

DAY

HOUR

+-----------------------------------------------------------+
```

4 Pillars nằm trên cùng một hàng.

Không xếp 2×2 trên Desktop.

---

Tablet

```
YEAR

MONTH

DAY

HOUR
```

2 × 2.

---

Mobile

```
YEAR

↓

MONTH

↓

DAY

↓

HOUR
```

Stack.

---

# 9. Component Composition

Cho phép:

- Pillar Card
- Stem Cell
- Branch Cell
- Hidden Stem List
- Na Yin Badge
- Twelve Stage Badge
- Divider

Không:

- Hero
- Progress
- Chart
- Long Text
- Alert

---

# 10. Data Mapping

| UI | Engine/API |
|-----|------------|
| Year Stem | Chart.Year.Stem |
| Year Branch | Chart.Year.Branch |
| Month Stem | Chart.Month.Stem |
| Month Branch | Chart.Month.Branch |
| Day Stem | Chart.Day.Stem |
| Day Branch | Chart.Day.Branch |
| Hour Stem | Chart.Hour.Stem |
| Hour Branch | Chart.Hour.Branch |
| Hidden Stem | Pillar.HiddenStems |
| Na Yin | Pillar.NaYin |
| Twelve Stage | Pillar.TwelveStage |

---

# 11. Typography Rules

Section Title

→ HeadingPrimary

Pillar Name

→ HeadingSecondary

Stem / Branch

→ BodyPrimary

Supporting

→ BodySecondary

Metadata

→ Caption

Ngày (Day Pillar) được phép sử dụng Typography mạnh hơn các Pillar khác.

---

# 12. Interaction Rules

Cho phép:

- Tooltip từng thành phần.
- Highlight Nhật Chủ.
- Copy dữ liệu trụ.
- Mở Knowledge Panel.

Không:

- Chỉnh sửa.
- Kéo thả.
- Collapse từng Pillar.

---

# 13. Responsive Behaviour

Desktop

4 cột.

Tablet

2 × 2.

Mobile

1 cột.

Reading Flow giữ nguyên.

---

# 14. Accessibility

- Semantic Table/Card.
- Keyboard Focus.
- Tooltip truy cập được.
- Không dùng màu làm tín hiệu duy nhất.
- Nhật Chủ có mô tả cho Screen Reader.

---

# 15. Anti-Patterns

Không được:

❌ Hero hóa Four Pillars.

❌ Làm cả bốn trụ nổi bật như nhau.

❌ Đưa Dụng Thần vào S03.

❌ Đưa Thập Thần vào S03.

❌ Đưa Luận giải vào S03.

❌ Hiển thị quá nhiều Tooltip cùng lúc.

---

# 16. Screenshot Acceptance

Cursor phải cung cấp:

1.

Desktop Full

2.

Desktop Zoom (S03)

3.

Tablet

4.

Mobile

5.

Pillar Hover State

6.

Design Rationale

---

# 17. Cursor Implementation Rules

Cursor không được:

- đổi Reading Order
- đổi thứ tự Pillar
- thêm Card
- thêm Chart
- thêm Summary

Nếu dữ liệu chưa có,

sử dụng Placeholder đúng Blueprint.

---

# 18. Product Owner Review Checklist

Business

□ Hiểu đúng cấu trúc.

Decision

□ Sẵn sàng sang S04.

Reading

□ Nhật Chủ nổi bật.

Layout

□ 4 Pillars rõ.

Responsive

□ Desktop

□ Tablet

□ Mobile

---

# 19. Quality Scorecard

| Category | Score |
|----------|------:|
| Structure Clarity | 20 |
| Reading Flow | 20 |
| Day Master Emphasis | 20 |
| Responsive | 20 |
| Blueprint Compliance | 20 |

95–100

PASS

80–94

PASS WITH CHANGES

<80

REJECT

---

# 20. Relationship

S03 cung cấp dữ liệu nền cho:

S04

↓

Element Balance

S05

↓

Strength

S06

↓

Ten Gods

S07

↓

ShenSha

Không tạo kết luận.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
|1.0.0|ACTIVE|Initial Four Pillars Blueprint|

bổ sung 5 phụ lục cho S03

Appendix A – Four Pillars Priority Matrix
Thành phần	Priority
Day Pillar	10
Month Pillar	8
Year Pillar	6
Hour Pillar	6
Hidden Stem	5
Na Yin	4
Twelve Stage	4


Appendix B – Canonical Four Pillars Wireframe
┌────────┬────────┬────────┬────────┐
│  NĂM   │ THÁNG  │ NGÀY ★ │  GIỜ   │
├────────┼────────┼────────┼────────┤
│Thiên Can│Thiên Can│Thiên Can│Thiên Can│
│Địa Chi │Địa Chi │Địa Chi │Địa Chi │
│Tàng Can│Tàng Can│Tàng Can│Tàng Can│
│Nạp Âm  │Nạp Âm  │Nạp Âm  │Nạp Âm  │
│Tr.Sinh │Tr.Sinh │Tr.Sinh │Tr.Sinh │
└────────┴────────┴────────┴────────┘
Ngày (Day Pillar) luôn có dấu hiệu nhận biết trực quan (viền, nhãn hoặc nền nhẹ) nhưng không phá vỡ tính cân bằng của toàn bộ hàng.

Appendix C – Reading Path
YEAR
   ↓
MONTH
   ↓
DAY ★
   ↓
HOUR
Sau khi hoàn thành bốn trụ:
↓
Element Balance (S04)

Appendix D – Evidence Boundary
S03 chỉ hiển thị Evidence cấu trúc.
Không hiển thị:
Điểm số.
Đánh giá.
Khuyến nghị.
Luận giải.
Dụng Thần.
Hỷ Thần.
Kỵ Thần.
Thập Thần.
Thần Sát.
Điều này giúp ranh giới giữa các section luôn rõ ràng.

Appendix E – Common Mistakes
Các lỗi cần tránh khi triển khai:
Làm Day Pillar không nổi bật nên người dùng khó xác định Nhật Chủ.
Biến mỗi Pillar thành một Card quá lớn, làm mất cảm giác "một cấu trúc thống nhất".
Đưa quá nhiều màu sắc cho từng Thiên Can/Địa Chi gây nhiễu.
Chèn diễn giải hoặc nhận xét ngay trong S03.
Dùng layout khác nhau giữa Desktop và Tablet làm thay đổi Reading Flow.