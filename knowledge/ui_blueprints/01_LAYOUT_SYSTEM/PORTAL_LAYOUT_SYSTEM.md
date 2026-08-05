# BTE Platform

# Portal Layout System

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Depends On:

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_USER_JOURNEY.md

Applies To:

- applications/customer_portal
- Desktop
- Tablet
- Mobile

---

# 1. Purpose

Tài liệu này định nghĩa kiến trúc không gian (Spatial Architecture) của Portal BTE.

Layout System không quy định:

- CSS
- Component
- Typography
- Grid chi tiết

Layout System chỉ định nghĩa:

- các vùng chức năng
- quan hệ giữa các vùng
- thứ tự hiển thị
- quy tắc bố cục

Mọi Blueprint S00–S08 phải tuân thủ tài liệu này.

---

# 2. Core Principle

Portal không được xây dựng từ Card.

Portal không được xây dựng từ Grid.

Portal được xây dựng từ:

Business Goal

↓

Information Architecture

↓

Spatial Layout

↓

Grid

↓

Component

↓

CSS

Nếu Layout sai thì mọi tầng phía dưới đều sai.

---

# 3. Canonical Portal Structure

Portal V1.0 gồm các vùng chính sau:

```

┌───────────────────────────────────────────────┐

GLOBAL HEADER

└───────────────────────────────────────────────┘

┌───────────────┬───────────────────────────────┐

TABLE OF CONTENT │ MAIN CONTENT

│

│ S00

│

│ S01

│

│ S02

│

│ S03

│

│ S04

│

│ S05

│

│ S06

│

│ S07

│

│ S08

│

│ Learning Panel

│

└───────────────┴───────────────────────────────┘

```

Không được thay đổi cấu trúc này nếu chưa có Architecture Review.

---

# 4. Layout Zones

Portal được chia thành 6 Zone.

## Zone A — Global Header

Chức năng:

- Navigation
- User Menu
- Search
- Notifications

Không chứa:

- Business Data
- Result Data

---

## Zone B — Table Of Contents

Chức năng:

- Điều hướng giữa các Section
- Hiển thị trạng thái đọc
- Hiển thị Progress

Không chứa:

- Nội dung phân tích

---

## Zone C — Main Content

Đây là vùng quan trọng nhất.

Chứa:

- S00
- S01
- S02
- S03
- S04
- S05
- S06
- S07
- S08

Mọi phân tích đều diễn ra tại đây.

---

## Zone D — Learning Layer

Learning luôn là:

On-demand

Không được là nội dung chính.

Có thể:

- Drawer
- Side Panel
- Accordion

Không được chiếm Main Content.

---

## Zone E — Overlay Layer

Bao gồm:

- Dialog
- Modal
- Drawer
- Toast
- Tooltip

Không được phá Reading Flow.

---

## Zone F — System Layer

Bao gồm:

- Loading
- Error
- Empty State
- Permission
- Offline

Luôn nằm ngoài Business Content.

---

# 5. Layout Hierarchy

Portal luôn theo thứ tự:

Global Navigation

↓

Reading Navigation

↓

Business Content

↓

Learning

↓

System Overlay

Không được đảo.

---

# 6. Main Content Structure

Main Content luôn gồm:

```

S00 Context

↓

S01 Identity & Decision

↓

S02 Overview

↓

S03 Four Pillars

↓

S04 Element Balance

↓

S05 Strength

↓

S06 Ten Gods

↓

S07 ShenSha

↓

S08 Interpretation

↓

Learning

```

Đây là Canonical Structure.

---

# 7. Section Layout Rules

Mỗi Section là một Block độc lập.

Section gồm:

Header

↓

Body

↓

Supporting Information

↓

Action (nếu có)

Không được tạo nhiều kiểu Section khác nhau.

---

# 8. Fold Strategy

First Viewport chỉ được chứa:

S00

+

S01

Mục tiêu:

Người dùng không cần cuộn vẫn hiểu:

- Tôi là ai.
- Tôi mạnh hay yếu.
- Điều gì quan trọng nhất.

Các Section khác phải nằm dưới Fold.

---

# 9. Reading Axis

Portal chỉ có một trục đọc chính:

Vertical

Không tạo nhiều vùng đọc song song.

Desktop có thể có TOC bên trái nhưng nội dung chính vẫn chỉ có một trục.

---

# 10. Navigation Model

Portal có hai lớp điều hướng.

## Navigation Level 1

Global Navigation

Ví dụ:

Dashboard

History

Reports

Settings

---

## Navigation Level 2

Section Navigation

Ví dụ:

S00

↓

S01

↓

S02

...

↓

S08

Không thêm cấp điều hướng thứ ba.

---

# 11. Layout Density

Portal hướng tới:

Medium–High Density

Không phải:

Dashboard KPI

Không phải:

Landing Page

Không phải:

PDF

Mật độ phải đủ thông tin nhưng không gây quá tải.

---

# 12. Layout Consistency

Desktop

Tablet

Mobile

có thể:

- đổi số cột
- đổi vị trí TOC
- đổi cách hiển thị Learning

Không được:

- đổi Reading Flow
- đổi Decision Flow
- đổi thứ tự Section

---

# 13. Layout Anti-Patterns

Không được:

❌ Mỗi màn hình một bố cục.

❌ TOC thay đổi vị trí tùy ý.

❌ Hero biến mất trên Mobile.

❌ Learning chen vào Main Flow.

❌ Modal thay thế Main Content.

❌ Tạo nhiều vùng cuộn độc lập.

---

# 14. Responsive Layout Strategy

Desktop

Header

+

TOC

+

Main

Tablet

Header

+

Collapsible TOC

+

Main

Mobile

Header

+

Drawer TOC

+

Single Column Main

Responsive chỉ thay đổi cách bố trí.

Không thay đổi cấu trúc.

---

# 15. Layout Validation Checklist

□ Header luôn tồn tại.

□ TOC luôn truy cập được.

□ Main chỉ có một trục đọc.

□ S00 luôn đứng đầu.

□ S01 luôn ngay sau S00.

□ Learning không chen giữa các Section.

□ Overlay không che Business Content khi không cần.

□ Không có nhiều vùng cuộn.

---

# 16. Relationship

Layout System là nền tảng cho:

- PORTAL_GRID_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_COMPONENT_USAGE.md
- Tất cả Screen Blueprints

Không Blueprint nào được tự định nghĩa Layout riêng.

---

# 17. Architecture Protection Rule

Mọi thay đổi Layout đều phải:

Architecture Review

↓

Product Owner Approval

↓

Blueprint Update

↓

Implementation

Không được sửa Layout trực tiếp trong React.

---

# 18. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Canonical Portal Layout System |

# 19. Layout Tokens (Conceptual Architecture)

## 19.1 Purpose

Layout Tokens không phải Design Tokens.

Layout Tokens định nghĩa các **vùng chức năng (Functional Regions)** của Portal.

Mục tiêu là tạo ra một ngôn ngữ chung giữa:

- Product Owner
- UX Designer
- UI Designer
- Frontend Developer
- AI Coding Assistant

Thay vì mô tả:

> "Khu vực bên trái chứa mục lục..."

mọi tài liệu chỉ cần sử dụng tên Token chuẩn.

---

## 19.2 Canonical Layout Tokens

| Token | Region | Description |
|--------|--------|-------------|
| `PrimaryNavigation` | Global Header | Điều hướng toàn cục của Portal |
| `ReadingNavigation` | TOC | Điều hướng giữa các Section của Portal |
| `ContextRegion` | S00 | Xác nhận đúng hồ sơ và phiên phân tích |
| `IdentityRegion` | S01-A | Nhật Chủ, Ngũ Hành, Âm Dương |
| `ConditionRegion` | S01-B | Thân Vượng/Nhược, đánh giá tổng quan |
| `DecisionRegion` | S01-C | What / Why / Next |
| `BusinessRegion` | S02–S08 | Toàn bộ nội dung phân tích |
| `LearningRegion` | Learning Panel | Kiến thức mở rộng theo yêu cầu |
| `OverlayRegion` | Modal / Drawer / Dialog | Lớp giao diện tạm thời |
| `SystemRegion` | Loading / Error / Empty | Trạng thái hệ thống |

---

## 19.3 Token Hierarchy

Portal luôn tuân theo cấu trúc:

```
PrimaryNavigation
        │
        ▼
ReadingNavigation
        │
        ▼
ContextRegion
        │
        ▼
IdentityRegion
        │
        ▼
ConditionRegion
        │
        ▼
DecisionRegion
        │
        ▼
BusinessRegion
        │
        ▼
LearningRegion
```

Không được thay đổi thứ tự phân cấp này.

---

## 19.4 Token Usage Rules

### Rule 01

Mỗi vùng chỉ có một Token chính.

---

### Rule 02

Một Component không được tự ý thay đổi Region của mình.

Ví dụ:

`DecisionCard`

luôn thuộc

`DecisionRegion`.

Không được đưa vào

`LearningRegion`.

---

### Rule 03

Blueprint chỉ sử dụng Token chuẩn.

Ví dụ:

```
BusinessRegion

↓

Section

↓

Component
```

Không mô tả lại bố cục bằng văn bản dài.

---

### Rule 04

Mọi Screen Blueprint phải tham chiếu Layout Token thay vì định nghĩa Layout mới.

---

## 19.5 Future Compatibility

Các module tương lai:

- Phong Thủy
- Chọn ngày
- Sim số
- Kỳ Môn
- Báo cáo chuyên sâu

được phép thay đổi nội dung,

nhưng phải tái sử dụng các Layout Token này để giữ trải nghiệm nhất quán.

---

# 20. Layout Evolution Policy

## 20.1 Purpose

Portal Layout là nền tảng kiến trúc.

Không được thay đổi tùy ý trong quá trình phát triển.

Mọi thay đổi phải tuân theo chính sách quản lý phiên bản của Layout.

---

## 20.2 Stability Levels

| Level | Được phép thay đổi |
|--------|--------------------|
| Foundation | ❌ Không |
| Layout System | Rất hạn chế |
| Screen Blueprint | Có |
| React Implementation | Có |
| CSS | Có |

Layout System chỉ thay đổi khi thật sự cần thiết và phải có phê duyệt ở cấp kiến trúc.

---

## 20.3 Version Policy

### V1.x

Được phép:

- Điều chỉnh khoảng cách.
- Điều chỉnh kích thước.
- Thêm Section mới nếu không phá Reading Flow.
- Tối ưu Responsive.

Không được:

- Thay đổi thứ tự S00 → S08.
- Thay đổi Decision Flow.
- Thay đổi Reading Flow.
- Thay đổi Layout Tokens.

---

### V2.x

Được phép:

- Mở rộng BusinessRegion.
- Thêm module mới.
- Thêm vùng chuyên biệt nếu có Architecture Review.

Bắt buộc giữ:

- Identity → Condition → Decision → Evidence → Interpretation.
- Canonical Layout Tokens.
- Reading Flow.
- Decision Flow.

---

## 20.4 Architecture Change Process

Mọi thay đổi Layout phải đi theo quy trình:

```
Business Requirement

↓

Architecture Proposal

↓

Product Owner Review

↓

Foundation Update

↓

Blueprint Update

↓

Implementation

↓

Regression Review
```

Không được sửa React trước khi cập nhật tài liệu kiến trúc.

---

## 20.5 Backward Compatibility

Các Blueprint đã được phê duyệt phải tiếp tục hoạt động khi Layout được mở rộng.

Nếu một thay đổi làm ảnh hưởng tới Blueprint cũ thì phải:

- Cập nhật Blueprint.
- Cập nhật tài liệu Foundation liên quan.
- Thực hiện lại Review.

---

## 20.6 Extension Principles

Module mới chỉ được bổ sung nếu:

- Không phá Reading Flow.
- Không phá Decision Flow.
- Không thay đổi First Viewport Strategy.
- Không làm mất tính nhất quán của Portal.

Ví dụ:

- Phong Thủy.
- Chọn ngày.
- Sim số.
- Kỳ Môn.

đều phải tuân thủ cùng triết lý bố cục.

---

## 20.7 Layout Freeze Policy

Sau khi UI V1.0 được Product Owner phê duyệt:

- Layout System được đánh dấu **FROZEN**.
- Chỉ sửa lỗi triển khai.
- Không thay đổi kiến trúc không gian.
- Không đổi vị trí các Region.

Điều này giúp Sprint Integration chỉ tập trung vào tích hợp hệ thống thay vì sửa giao diện.

---

## 20.8 Success Criteria

Layout Evolution được coi là thành công khi:

- Mọi phiên bản vẫn giữ cùng trải nghiệm đọc.
- Người dùng cũ không cần học lại cách sử dụng.
- Blueprint cũ vẫn còn giá trị tham chiếu.
- AI và lập trình viên luôn có một nguồn kiến trúc thống nhất.
# 21. Layout Governance

## 21.1 Purpose

Layout System là nền tảng kiến trúc của toàn bộ Portal BTE.

Tài liệu này không chỉ định nghĩa cách tổ chức giao diện mà còn quy định cách quản trị (Governance) để đảm bảo Layout luôn nhất quán trong suốt vòng đời của sản phẩm.

Mục tiêu của Layout Governance là:

- Bảo vệ kiến trúc Portal.
- Ngăn việc thay đổi bố cục tùy ý.
- Đảm bảo mọi phiên bản đều duy trì cùng trải nghiệm người dùng.
- Phân biệt rõ thay đổi kiến trúc và thay đổi triển khai.

---

## 21.2 Governance Levels

Mọi thay đổi UI phải được phân loại vào đúng cấp độ.

| Level | Phạm vi | Cần Architecture Review |
|--------|----------|--------------------------|
| Foundation | UI Bible, Philosophy, Reading Flow, Decision Flow | ✅ Bắt buộc |
| Layout System | Spatial Layout, Layout Tokens, Portal Structure | ✅ Bắt buộc |
| Screen Blueprint | S00–S08, Learning Panel | ⚠ Product Owner Review |
| Component Library | Component composition | Không nếu không đổi Blueprint |
| React Implementation | JSX, CSS, Tailwind | Không |
| Bug Fix | UI bug, responsive bug | Không |

Không được xử lý một thay đổi Foundation như một thay đổi CSS.

---

## 21.3 Change Authority

Quyền thay đổi được phân định như sau:

| Hạng mục | Người phê duyệt |
|-----------|-----------------|
| Foundation Documents | Product Owner |
| Layout System | Product Owner |
| Screen Blueprint | Product Owner |
| React Implementation | Development Team |
| CSS / Styling | Development Team |

Nếu thay đổi ảnh hưởng tới Reading Flow hoặc Decision Flow thì bắt buộc phải quay về Product Owner để xem xét.

---

## 21.4 Architecture Change Workflow

Mọi thay đổi Layout phải tuân theo quy trình sau:

```
Business Requirement
        ↓
Architecture Analysis
        ↓
Proposal
        ↓
Product Owner Approval
        ↓
Foundation Update
        ↓
Blueprint Update
        ↓
Implementation
        ↓
Review
        ↓
Freeze
```

Không được triển khai React trước khi Blueprint được cập nhật.

---

## 21.5 Review Gates

Portal chỉ được phép chuyển sang giai đoạn tiếp theo khi vượt qua các cổng kiểm tra sau:

| Gate | Điều kiện |
|------|-----------|
| Foundation Gate | Foundation Documents được phê duyệt |
| Layout Gate | Layout System được khóa |
| Blueprint Gate | Blueprint của Section được phê duyệt |
| Implementation Gate | React triển khai đúng Blueprint |
| Review Gate | Screenshot Review PASS |
| Freeze Gate | UI Freeze |

Không được bỏ qua bất kỳ Gate nào.

---

## 21.6 Documentation First Policy

BTE áp dụng nguyên tắc:

**Documentation First.**

Thứ tự luôn là:

```
Foundation

↓

Layout

↓

Blueprint

↓

Implementation

↓

Review

↓

Freeze
```

Không được phát triển theo trình tự:

```
Code

↓

Review

↓

Viết tài liệu
```

Tài liệu luôn đi trước mã nguồn.

---

## 21.7 Canonical Source of Truth

Trong trường hợp có mâu thuẫn giữa các tài liệu, thứ tự ưu tiên là:

```
BTE_UI_BIBLE.md
        ↓
PORTAL_DESIGN_PHILOSOPHY.md
        ↓
PORTAL_READING_FLOW.md
        ↓
PORTAL_DECISION_FLOW.md
        ↓
PORTAL_LAYOUT_SYSTEM.md
        ↓
Screen Blueprint
        ↓
React Source Code
```

Code không được coi là nguồn sự thật.

Blueprint và Foundation mới là nguồn tham chiếu chính thức.

---

## 21.8 Freeze Policy

Sau khi Sprint UI được hoàn thành:

- Foundation → FROZEN
- Layout System → FROZEN
- Screen Blueprint → FROZEN

Trong Sprint Integration:

Chỉ được phép:

- Bind API.
- Bind Engine.
- Bind Report.
- Sửa lỗi triển khai.

Không được:

- Thay đổi Reading Flow.
- Thay đổi Decision Flow.
- Thay đổi Layout.
- Thay đổi Information Hierarchy.

---

## 21.9 Success Criteria

Layout Governance được coi là thành công khi:

- Mọi màn hình Portal có cùng ngôn ngữ thiết kế.
- Không tồn tại nhiều Layout khác nhau trong cùng một sản phẩm.
- AI và lập trình viên có thể triển khai nhất quán dựa trên Blueprint.
- Product Owner review dựa trên tài liệu thay vì cảm nhận.
- Sprint Integration không phải sửa lại giao diện.

---

## 21.10 Closing Statement

`PORTAL_LAYOUT_SYSTEM.md` là tài liệu kiến trúc chính thức của Portal BTE.

Mọi Blueprint (S00–S08), Component Library và React Implementation phải tuân thủ tài liệu này.

Bất kỳ thay đổi nào làm ảnh hưởng đến Layout System đều phải được xem là thay đổi kiến trúc và thực hiện theo đúng quy trình Governance của BTE Platform.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Canonical Portal Layout System |