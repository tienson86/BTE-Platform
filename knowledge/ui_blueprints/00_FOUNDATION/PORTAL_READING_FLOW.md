# BTE Platform

# Portal Reading Flow

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Depends On:

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- CANONICAL_PORTAL_INFORMATION_ARCHITECTURE.md

Applies To:

- Portal UI
- Desktop
- Tablet
- Mobile

---

# 1. Purpose

Tài liệu này định nghĩa luồng đọc chuẩn (Canonical Reading Flow) của Portal BTE.

Reading Flow không mô tả giao diện.

Reading Flow mô tả:

- người dùng nhìn gì
- người dùng hiểu gì
- người dùng quyết định gì

ở từng thời điểm.

Mọi màn hình của Portal phải tuân thủ Reading Flow này.

---

# 2. Core Principle

Portal không ép người dùng đọc theo cấu trúc dữ liệu.

Portal dẫn dắt người dùng đọc theo quá trình ra quyết định.

Do đó:

Reading Flow luôn ưu tiên:

Hiểu

↓

Tin tưởng

↓

Ra quyết định

↓

Đọc chi tiết

Không bao giờ làm ngược lại.

---

# 3. Reading Model

Portal tuân theo mô hình:

```

Identity

↓

Condition

↓

Decision

↓

Evidence

↓

Interpretation

↓

Learning

```

Ý nghĩa:

| Stage | Mục tiêu |
|---------|----------|
| Identity | Tôi là ai? |
| Condition | Lá số hiện như thế nào? |
| Decision | Điều gì quan trọng nhất? |
| Evidence | Vì sao kết luận đó đúng? |
| Interpretation | Tôi nên hiểu như thế nào? |
| Learning | Muốn tìm hiểu sâu hơn |

Không được đảo thứ tự.

---

# 4. Reading Timeline

## 0–3 giây

Người dùng phải xác nhận:

- Đây đúng là hồ sơ của mình.
- Đúng phiên phân tích.

UI:

S00 Context Header

Không có phân tích.

---

## 3–8 giây

Người dùng phải hiểu:

- Nhật Chủ
- Ngũ Hành
- Âm Dương

Đây là Identity.

UI:

S01-A

---

## 8–15 giây

Người dùng phải hiểu:

- Thân mạnh hay yếu
- Đánh giá tổng quan

UI:

S01-B

---

## 15–25 giây

Người dùng phải biết:

- Điều quan trọng nhất
- Vì sao
- Hành động tiếp theo

UI:

S01-C Decision Support

What

↓

Why

↓

Next

---

## 25–40 giây

Người dùng bắt đầu xem:

- Chart Overview
- Four Pillars

Đây là lớp "Evidence".

---

## 40–60 giây

Người dùng tiếp tục:

- Element Balance
- Strength
- Ten Gods
- ShenSha

Đây là lớp phân tích.

---

## Sau 60 giây

Người dùng đọc:

Professional Interpretation

Nếu muốn:

Learning Panel.

---

# 5. Reading Objectives

Mỗi giai đoạn phải trả lời một câu hỏi.

| Stage | User Question |
|---------|---------------|
| S00 | Tôi đang xem đúng lá số? |
| S01-A | Tôi là ai? |
| S01-B | Tôi mạnh hay yếu? |
| S01-C | Điều gì quan trọng nhất? |
| S02 | Đây là lá số nào? |
| S03 | Bốn trụ ra sao? |
| S04 | Ngũ hành cân bằng không? |
| S05 | Vì sao mạnh/yếu? |
| S06 | Thập thần nói gì? |
| S07 | Có tín hiệu đặc biệt nào? |
| S08 | Tôi nên làm gì tiếp? |
| Learning | Muốn hiểu sâu hơn? |

Nếu một Section không trả lời được câu hỏi của mình thì Section đó thất bại.

---

# 6. Reading Priority

Thông tin được chia thành sáu mức ưu tiên.

## Priority 1

Identity

## Priority 2

Condition

## Priority 3

Decision

## Priority 4

Evidence

## Priority 5

Interpretation

## Priority 6

Learning

Không được để Priority thấp lấn át Priority cao.

---

# 7. Reading Rules

## Rule 01

Identity luôn xuất hiện trước Analysis.

---

## Rule 02

Decision luôn xuất hiện trước Evidence.

---

## Rule 03

Interpretation luôn sau Evidence.

---

## Rule 04

Learning luôn là On-demand.

---

## Rule 05

Metadata không được làm gián đoạn Reading Flow.

---

## Rule 06

Không hiển thị quá nhiều thông tin trong First Viewport.

---

# 8. First Viewport Strategy

First Viewport chỉ gồm:

S00

↓

S01

Không có:

- Four Pillars
- Ten Gods
- ShenSha
- Learning

Mục tiêu:

Người dùng hiểu Portal trong một màn hình đầu tiên.

---

# 9. Progressive Disclosure

Portal chia thông tin thành nhiều lớp.

Layer 1

Identity

↓

Layer 2

Condition

↓

Layer 3

Decision

↓

Layer 4

Evidence

↓

Layer 5

Interpretation

↓

Layer 6

Learning

Người dùng không cần mở toàn bộ dữ liệu để đạt mục tiêu.

---

# 10. Reading Anti-Patterns

Không được:

❌ Hiển thị toàn bộ dữ liệu ngay đầu.

❌ Đưa Thập Thần lên trước Identity.

❌ Đưa Thần Sát lên trước Decision.

❌ Đưa Learning lên First Viewport.

❌ Biến Portal thành Dashboard nhiều widget.

---

# 11. Responsive Reading

Reading Flow không thay đổi giữa:

- Desktop
- Tablet
- Mobile

Chỉ thay đổi cách sắp xếp (layout).

Không thay đổi thứ tự nhận thức.

---

# 12. Reading Validation Checklist

Portal được coi là đúng Reading Flow khi:

□ Người dùng xác nhận đúng hồ sơ trong 3 giây.

□ Hiểu Identity trong 8 giây.

□ Hiểu Condition trong 15 giây.

□ Biết Decision trong 25 giây.

□ Bắt đầu đọc Evidence sau đó.

□ Chỉ mở Learning khi có nhu cầu.

---

# 13. Relationship

Tài liệu này là nền tảng cho:

- PORTAL_DECISION_FLOW.md
- PORTAL_USER_JOURNEY.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- Tất cả Screen Blueprints

---

# 14. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Canonical Reading Flow |