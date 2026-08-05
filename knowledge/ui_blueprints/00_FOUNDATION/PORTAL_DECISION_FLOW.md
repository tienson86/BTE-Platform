# BTE Platform

# Portal Decision Flow

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Depends On:

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- CANONICAL_PORTAL_INFORMATION_ARCHITECTURE.md

Applies To:

- Portal UI
- Desktop
- Tablet
- Mobile

---

# 1. Purpose

Tài liệu này định nghĩa **Decision Flow** của Portal BTE.

Decision Flow không mô tả:

- Layout
- Grid
- Component
- Typography

Decision Flow mô tả:

- Người dùng biết điều gì.
- Người dùng hiểu điều gì.
- Người dùng quyết định điều gì.
- Hệ thống hỗ trợ quyết định như thế nào.

Portal BTE là một **Decision Support Portal**, vì vậy mọi Section đều phải phục vụ một quyết định cụ thể.

---

# 2. Core Principle

Portal không hiển thị dữ liệu để người dùng tự suy luận.

Portal hướng dẫn người dùng:

Hiểu

↓

Đánh giá

↓

Ra quyết định

↓

Hành động

Mỗi Section phải giảm bớt sự mơ hồ và tăng thêm sự chắc chắn.

---

# 3. Decision Model

Portal tuân theo mô hình:

```

Question

↓

Understanding

↓

Decision

↓

Action

```

Nếu một Section chỉ cung cấp dữ liệu mà không hỗ trợ quyết định thì Section đó chưa hoàn thành nhiệm vụ.

---

# 4. Canonical Decision Flow

```

S00
↓

"Tôi đang xem đúng hồ sơ?"

↓

S01
↓

"Tôi là ai?"

↓

"Tôi mạnh hay yếu?"

↓

"Điều gì quan trọng nhất?"

↓

S02
↓

"Lá số này có đúng không?"

↓

S03
↓

"Cấu trúc Tứ Trụ như thế nào?"

↓

S04
↓

"Ngũ Hành cân bằng hay mất cân bằng?"

↓

S05
↓

"Điều gì làm Thân mạnh hoặc yếu?"

↓

S06
↓

"Thập Thần nào đáng chú ý?"

↓

S07
↓

"Có tín hiệu đặc biệt nào cần lưu ý?"

↓

S08
↓

"Tôi nên làm gì tiếp?"

↓

Learning Panel
↓

"Tôi muốn hiểu sâu hơn."

```

Không được thay đổi trình tự này.

---

# 5. Section Decision Matrix

| Section | User Question | Decision | Next Action |
|-----------|---------------|----------|-------------|
| S00 | Tôi đang xem đúng lá số? | Xác nhận hồ sơ | Đọc S01 |
| S01 | Tôi là ai? Mạnh hay yếu? Điều gì quan trọng nhất? | Có cần đọc sâu? | Sang S02 |
| S02 | Lá số đã đúng thông tin chưa? | Tiếp tục hay phân tích lại | Sang S03 |
| S03 | Tứ Trụ của tôi như thế nào? | Hiểu cấu trúc | Sang S04 |
| S04 | Ngũ Hành cân bằng không? | Nhận diện điểm mất cân bằng | Sang S05 |
| S05 | Vì sao Thân mạnh/yếu? | Hiểu nguyên nhân | Sang S06 |
| S06 | Thập Thần nào nổi bật? | Xác định ảnh hưởng chính | Sang S07 |
| S07 | Có tín hiệu đặc biệt? | Đánh giá yếu tố bổ sung | Sang S08 |
| S08 | Tôi nên làm gì? | Chọn hướng hành động | Kết thúc hoặc mở Learning |
| Learning | Muốn tìm hiểu thêm? | Học sâu | Quay lại Portal |

---

# 6. Decision Layers

Portal chia quyết định thành bốn lớp.

## Layer 1 – Identity

Quyết định:

Đây có đúng là kết quả của tôi không?

---

## Layer 2 – Situation

Quyết định:

Tình trạng hiện tại của lá số là gì?

---

## Layer 3 – Cause

Quyết định:

Vì sao lại có kết quả này?

---

## Layer 4 – Action

Quyết định:

Tôi nên làm gì tiếp theo?

Mỗi Layer phải hoàn chỉnh trước khi chuyển sang Layer kế tiếp.

---

# 7. Decision Confidence

Portal không chỉ đưa ra kết luận.

Portal phải giúp người dùng hiểu mức độ tin cậy.

Ví dụ:

- Confidence Score
- Mức độ chắc chắn
- Các yếu tố ảnh hưởng

Điều này giúp tăng niềm tin vào kết quả.

---

# 8. Decision Support Rules

## Rule 01

Không đưa ra hành động khi chưa có đủ ngữ cảnh.

---

## Rule 02

Không trình bày dữ liệu mà thiếu diễn giải.

---

## Rule 03

Không hiển thị quá nhiều lựa chọn cùng lúc.

---

## Rule 04

Mỗi Section chỉ tập trung vào một quyết định chính.

---

## Rule 05

Không để dữ liệu kỹ thuật lấn át quyết định.

---

# 9. Decision Anti-Patterns

Không được:

❌ Hiển thị toàn bộ dữ liệu rồi để người dùng tự kết luận.

❌ Đưa quá nhiều lời khuyên không có ưu tiên.

❌ Trình bày kết luận mà không có cơ sở.

❌ Đặt các yếu tố phụ (Thần Sát...) lên trước các yếu tố cốt lõi.

❌ Để người dùng phải tìm thông tin quan trọng.

---

# 10. Commercial Decision Experience

Portal thương mại phải tạo cảm giác:

- Chuyên nghiệp.
- Đáng tin cậy.
- Có định hướng.

Người dùng không chỉ nhận được kết quả.

Người dùng phải cảm thấy:

"Tôi đã hiểu vấn đề và biết bước tiếp theo."

---

# 11. Decision Validation Checklist

Một Decision Flow đạt yêu cầu khi:

□ Người dùng biết mình đang xem đúng hồ sơ.

□ Hiểu Nhật Chủ và trạng thái.

□ Biết điều quan trọng nhất.

□ Hiểu vì sao.

□ Biết bước tiếp theo.

□ Có thể dừng tại S08 mà vẫn hoàn thành mục tiêu.

□ Learning chỉ là giá trị gia tăng, không bắt buộc.

---

# 12. Relationship

Decision Flow là nền tảng cho:

- PORTAL_USER_JOURNEY.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- S00–S08 Blueprints
- Learning Panel Blueprint

Mọi Screen Blueprint phải chứng minh rằng Section của mình hỗ trợ đúng quyết định đã được định nghĩa trong tài liệu này.

---

# 13. Future Compatibility

Decision Flow phải giữ ổn định khi mở rộng BTE.

Các module tương lai như:

- Phong Thủy
- Chọn ngày
- Sim số
- Kỳ môn
- Báo cáo chuyên sâu

đều phải áp dụng cùng nguyên tắc:

Question

↓

Understanding

↓

Decision

↓

Action

Điều này giúp toàn bộ hệ sinh thái BTE có cùng trải nghiệm người dùng.

---

# 14. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Canonical Decision Flow |

# 15. Decision Failure & Recovery

Portal BTE được xây dựng như một Decision Support System.

Do đó, mọi thiết kế phải được đánh giá không chỉ bằng việc hiển thị đúng dữ liệu, mà còn bằng khả năng giúp người dùng đưa ra quyết định.

Nếu người dùng không thể hoàn thành Decision Flow thì UI được coi là thất bại, ngay cả khi giao diện đẹp và dữ liệu chính xác.

---

## 15.1 Decision Failure Cases

### Failure 01

Người dùng không biết mình đang xem ai.

Ví dụ:

- Không nhận ra hồ sơ.
- Không biết đây có đúng lá số của mình.

Nguyên nhân:

- Thiếu Context Header.
- Metadata bị ẩn.
- Context quá nhỏ hoặc khó đọc.

Khắc phục:

- S00 luôn xuất hiện.
- Hồ sơ phải được xác nhận trong ≤3 giây.

---

### Failure 02

Người dùng không biết mình mạnh hay yếu.

Ví dụ:

- Phải đọc hết Four Pillars mới biết.
- Phải kéo xuống giữa trang.

Nguyên nhân:

- Identity và Condition không nằm trong First Viewport.

Khắc phục:

- S01 phải hiển thị ngay kết luận.
- Strength không được ẩn sau các Section khác.

---

### Failure 03

Người dùng thấy quá nhiều dữ liệu nhưng không biết điều gì quan trọng.

Ví dụ:

- Thập Thần.
- Thần Sát.
- Ngũ Hành.
- Tứ Trụ.

đều có trọng số thị giác như nhau.

Nguyên nhân:

- Thiếu Visual Hierarchy.
- Thiếu Information Priority.

Khắc phục:

- Decision luôn nổi bật hơn Evidence.
- Identity luôn nổi bật hơn Metadata.

---

### Failure 04

Người dùng đọc hết trang nhưng vẫn không biết nên làm gì.

Ví dụ:

- Có nhiều dữ liệu.
- Có nhiều phân tích.
- Không có Action.

Nguyên nhân:

- Thiếu Decision Support.

Khắc phục:

S01 và S08 phải luôn trả lời:

- What
- Why
- Next

---

### Failure 05

Learning trở thành nội dung bắt buộc.

Ví dụ:

Muốn hiểu kết quả

↓

phải mở Learning Panel.

Nguyên nhân:

- Kiến thức nền bị đưa vào luồng chính.

Khắc phục:

Learning chỉ là giá trị gia tăng.

Portal phải hoàn thành Decision Flow mà không cần Learning.

---

### Failure 06

Portal giống Dashboard quản trị.

Dấu hiệu:

- Quá nhiều Card.
- Quá nhiều Widget.
- Quá nhiều KPI.
- Người dùng phải tự tổng hợp thông tin.

Nguyên nhân:

Thiết kế theo Data-first.

Khắc phục:

Quay về Decision-first.

---

### Failure 07

Portal giống PDF được đưa lên Web.

Dấu hiệu:

- Khối văn bản dài.
- Không có phân lớp.
- Không có Progressive Disclosure.

Khắc phục:

Chia nhỏ thành:

Identity

↓

Condition

↓

Decision

↓

Evidence

↓

Interpretation

---

## 15.2 Decision Recovery Principles

Nếu phát hiện một Decision Failure:

Không sửa Component trước.

Không sửa CSS trước.

Không sửa màu trước.

Phải kiểm tra theo thứ tự:

Business Goal

↓

Decision Goal

↓

Reading Flow

↓

Information Hierarchy

↓

Layout

↓

Visual Hierarchy

↓

Component

↓

CSS

Không được làm ngược lại.

---

## 15.3 Decision Quality Checklist

Một Portal đạt chuẩn khi:

□ Người dùng xác nhận đúng hồ sơ trong ≤3 giây.

□ Người dùng biết Nhật Chủ trong ≤8 giây.

□ Người dùng biết Thân mạnh/yếu trong ≤10 giây.

□ Người dùng biết điều quan trọng nhất trong ≤15 giây.

□ Người dùng biết hành động tiếp theo trong ≤20 giây.

□ Người dùng hoàn thành Decision Flow trong ≤60 giây.

□ Learning Panel không bắt buộc.

---

## 15.4 Decision Quality KPIs

| KPI | Mục tiêu |
|------|----------|
| Context Recognition | ≤3 giây |
| Identity Recognition | ≤8 giây |
| Condition Recognition | ≤10 giây |
| Priority Recognition | ≤15 giây |
| Action Recognition | ≤20 giây |
| Full Decision Flow | ≤60 giây |
| Learning Dependency | 0% (không bắt buộc) |

---

## 15.5 Definition of Success

Portal chỉ được coi là thành công khi:

- Người dùng không cần hướng dẫn vẫn hiểu kết quả.
- Người dùng không phải tự tổng hợp dữ liệu.
- Người dùng không bị quá tải thông tin.
- Người dùng biết điều quan trọng nhất trước khi đọc chi tiết.
- Người dùng biết bước tiếp theo sau khi hoàn thành Portal.

Nếu bất kỳ tiêu chí nào không đạt thì Decision Flow phải được xem xét lại trước khi sửa giao diện.

# 16. Decision Review Protocol

Portal BTE không được đánh giá dựa trên cảm nhận "đẹp" hay "xấu".

Mọi Product Review phải tuân theo một quy trình thống nhất.

Mục tiêu của quy trình này là đảm bảo mọi quyết định đánh giá đều dựa trên trải nghiệm người dùng và khả năng hỗ trợ ra quyết định, thay vì sở thích cá nhân.

---

## 16.1 Review Order

Product Owner phải review theo đúng thứ tự sau.

```
Business Goal

↓

Decision Goal

↓

Reading Flow

↓

Information Hierarchy

↓

Visual Hierarchy

↓

Layout

↓

Responsive

↓

Interaction

↓

Component

↓

Visual Style

↓

Animation
```

Không được đảo ngược thứ tự.

Không được bắt đầu từ màu sắc, icon hay hiệu ứng.

---

## 16.2 Stage 1 — Business Review

Câu hỏi:

Section này tồn tại để giải quyết vấn đề gì?

Checklist

□ Có đúng Business Goal?

□ Có đúng User Goal?

□ Có đúng Decision Goal?

□ Có giúp người dùng tiến thêm một bước trong Decision Flow?

Nếu bất kỳ câu trả lời nào là "Không"

↓

DỪNG REVIEW

↓

Không tiếp tục đánh giá UI.

---

## 16.3 Stage 2 — Decision Review

Đánh giá:

Section có giúp người dùng trả lời đúng câu hỏi của mình không?

Ví dụ

S00

↓

"Tôi đang xem đúng hồ sơ?"

S01

↓

"Tôi là ai?"

↓

"Mạnh hay yếu?"

↓

"Quan trọng nhất là gì?"

S08

↓

"Tôi nên làm gì tiếp?"

Checklist

□ Người dùng có quyết định được không?

□ Có cần đọc sang Section khác mới hiểu không?

Nếu có

↓

REJECT.

---

## 16.4 Stage 3 — Reading Review

Kiểm tra:

Mắt người dùng có đi đúng Reading Flow không?

Review:

- Focus đầu tiên
- Focus thứ hai
- Focus thứ ba
- Scroll Point

Checklist

□ Identity trước

□ Condition sau

□ Decision tiếp theo

□ Evidence sau đó

□ Learning cuối cùng

---

## 16.5 Stage 4 — Information Hierarchy Review

Đánh giá:

Thông tin quan trọng có thực sự nổi bật hơn thông tin phụ không?

Checklist

□ Identity > Metadata

□ Decision > Evidence

□ Interpretation > Learning

□ Không có thành phần phụ lấn át thành phần chính

---

## 16.6 Stage 5 — Layout Review

Kiểm tra:

- Grid
- Alignment
- Section spacing
- White space
- Content density

Checklist

□ Không có khoảng trắng vô nghĩa

□ Không tạo cảm giác Dashboard

□ Không tạo cảm giác PDF

---

## 16.7 Stage 6 — Responsive Review

Bắt buộc review:

Desktop

Tablet

Mobile

Checklist

□ Reading Flow không thay đổi

□ Decision Flow không thay đổi

□ Không có cuộn ngang

□ Không mất thông tin

---

## 16.8 Stage 7 — Component Review

Chỉ review sau khi:

Business

↓

Decision

↓

Reading

↓

Layout

đã PASS.

Kiểm tra:

□ Component đúng Blueprint

□ Component đúng Design System

□ Không tự ý sáng tạo

---

## 16.9 Stage 8 — Visual Review

Đây là bước cuối cùng.

Đánh giá:

- Typography
- Color
- Icon
- Shadow
- Radius
- Animation

Lưu ý:

Visual không được cứu một Decision Flow sai.

Nếu Reading Flow sai,

Visual đẹp cũng REJECT.

---

## 16.10 Screenshot Review Protocol

Mỗi Section bắt buộc cung cấp:

1.

Desktop Full

2.

Desktop Zoom

3.

Tablet

4.

Mobile

5.

Design Rationale

6.

Completion Report

Thiếu bất kỳ mục nào

↓

Không review.

---

## 16.11 Product Owner Decision

Product Owner chỉ được chọn:

🟢 PASS

Đúng Blueprint.

Không cần sửa.

---

🟡 PASS WITH CHANGES

Đúng hướng.

Có một số điểm cần điều chỉnh.

Không thay đổi Foundation.

---

🔴 REJECT

Sai Reading Flow

hoặc

Sai Decision Flow

hoặc

Sai Business Goal.

Không sửa CSS.

Quay lại Blueprint.

---

## 16.12 Review Anti-Patterns

Không review theo:

❌ "Tôi thích màu này."

❌ "Card này đẹp hơn."

❌ "Icon này xấu."

❌ "Font này hợp hơn."

Review phải dựa trên:

- Business Goal
- Decision Goal
- Reading Flow
- Information Hierarchy

---

## 16.13 Escalation Rules

Nếu một Section bị REJECT hai lần liên tiếp:

Không tiếp tục sửa UI.

Phải quay lại:

Blueprint

↓

Information Architecture

↓

Design Philosophy

để tìm nguyên nhân.

Không sửa Component trước.

---

## 16.14 Review Completion Criteria

Một Section chỉ được coi là hoàn thành khi:

□ Business PASS

□ Decision PASS

□ Reading PASS

□ Information Hierarchy PASS

□ Layout PASS

□ Responsive PASS

□ Component PASS

□ Visual PASS

□ Product Owner PASS

Thiếu bất kỳ mục nào

↓

Section chưa hoàn thành.

---

## 16.15 Foundation Protection Rule

Trong quá trình review,

không được thay đổi:

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md

Nếu phát hiện cần thay đổi Foundation,

phải mở một Architecture Review riêng.

Không sửa Foundation trong quá trình review UI.

Điều này đảm bảo:

- Foundation ổn định.
- Blueprint ổn định.
- UI Review chỉ tập trung vào chất lượng triển khai.