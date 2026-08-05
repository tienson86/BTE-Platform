# BTE Platform V1.0

# UI Blueprints
UI Blueprints là tài liệu triển khai chính thức (Implementation Specification) của Portal UI. Trong trường hợp có khác biệt giữa mã nguồn và Blueprint, Blueprint là nguồn tham chiếu để đánh giá việc triển khai; mọi thay đổi kiến trúc phải được cập nhật từ các tài liệu nền tảng (Design Principles, Information Architecture, Screen Specifications) trước khi sửa Blueprint.

**Version:** 1.0.0  
**Status:** ACTIVE  
**Owner:** Product Owner  
**Scope:** Canonical Portal UI Blueprint  
**Applies To:** `applications/customer_portal`

---

# 1. Purpose

Thư mục `ui_blueprints/` là **Blueprint Layer** của BTE Platform.

Đây là tầng nằm giữa:

- Information Architecture
- Screen Specifications
- UI Implementation

Mục tiêu của Blueprint là chuyển đổi các yêu cầu nghiệp vụ và trải nghiệm người dùng thành các đặc tả kỹ thuật có thể triển khai trực tiếp.

Blueprint **không chứa code**.

Blueprint **không chứa React**.

Blueprint **không chứa CSS**.

Blueprint mô tả:

- bố cục
- luồng đọc
- phân cấp thông tin
- hệ thống layout
- nguyên tắc thiết kế
- blueprint từng màn hình

---

# 2. UI Development Architecture

```
Business Requirements
        │
        ▼
Design Principles
        │
        ▼
Canonical UI
        │
        ▼
Information Architecture
        │
        ▼
Portal Screen Specifications
        │
        ▼
UI Blueprints
        │
        ▼
Cursor Implementation
        │
        ▼
Product Owner Review
        │
        ▼
UI Freeze
```

---

# 3. Objectives

Blueprint phải đảm bảo:

- Không còn suy diễn khi triển khai UI.
- Một màn hình chỉ có một cách triển khai chính thức.
- Mọi AI đều tạo ra cùng một kết quả.
- UI nhất quán trên toàn bộ Portal.
- Đảm bảo trải nghiệm thương mại cho BTE Platform.

---

# 4. Directory Structure

```
ui_blueprints/

README.md

00_FOUNDATION/
    BTE_UI_BIBLE.md
    PORTAL_DESIGN_PHILOSOPHY.md
    PORTAL_READING_FLOW.md
    PORTAL_DECISION_FLOW.md
    PORTAL_USER_JOURNEY.md

01_LAYOUT_SYSTEM/
    PORTAL_LAYOUT_SYSTEM.md
    PORTAL_GRID_SYSTEM.md
    PORTAL_SPACING_SYSTEM.md
    PORTAL_VISUAL_HIERARCHY.md
    PORTAL_TYPOGRAPHY_SYSTEM.md
    PORTAL_COMPONENT_USAGE.md

02_SCREEN_BLUEPRINTS/
    S00_CONTEXT_HEADER.md
    S01_IDENTITY_DECISION_PANEL.md
    S02_CHART_OVERVIEW.md
    S03_FOUR_PILLARS.md
    S04_ELEMENT_BALANCE.md
    S05_STRENGTH.md
    S06_TEN_GODS.md
    S07_SHENSHA.md
    S08_INTERPRETATION.md
    LEARNING_PANEL.md

03_RESPONSIVE/
    DESKTOP.md
    TABLET.md
    MOBILE.md

04_REVIEW/
    UI_REVIEW_CHECKLIST.md
    SECTION_ACCEPTANCE.md
    UI_FREEZE_CRITERIA.md

99_IMPLEMENTATION/
    CURSOR_IMPLEMENTATION_RULES.md
    IMPLEMENTATION_WORKFLOW.md
    DEFINITION_OF_DONE.md
```

---

# 5. Relationship With Other Documents

Blueprint không thay thế các tài liệu hiện có.

| Document | Vai trò |
|----------|----------|
| UI_DESIGN_PRINCIPLES.md | Triết lý thiết kế |
| CANONICAL_PORTAL_UI.md | Giao diện tham chiếu |
| CANONICAL_PORTAL_INFORMATION_ARCHITECTURE.md | Kiến trúc thông tin |
| PORTAL_SCREEN_SPECIFICATIONS.md | Đặc tả chức năng từng màn hình |
| UI Blueprints | Đặc tả triển khai UI |

---

# 6. Blueprint Philosophy

Blueprint không mô tả giao diện đẹp.

Blueprint mô tả:

- người dùng nhìn gì trước
- hiểu gì trước
- quyết định điều gì
- tương tác như thế nào

Mọi quyết định thiết kế đều phải phục vụ trải nghiệm đọc và ra quyết định.

---

# 7. Development Rules

## Rule 01

Không được code khi chưa có Blueprint.

---

## Rule 02

Không được thay đổi Blueprint trong quá trình implement.

---

## Rule 03

Blueprint là nguồn sự thật duy nhất cho UI.

---

## Rule 04

Mỗi lần chỉ triển khai một Section.

---

## Rule 05

Section tiếp theo chỉ được mở khi Section trước được Product Owner phê duyệt.

---

## Rule 06

Không được tự ý thêm Component ngoài Blueprint nếu chưa được duyệt.

---

# 8. Review Workflow

```
Blueprint

↓

Review

↓

Approved

↓

Implementation

↓

Screenshot Review

↓

Accepted

↓

Freeze
```

---

# 9. Definition of Blueprint

Một Blueprint hoàn chỉnh phải trả lời được:

- Business Goal
- User Goal
- Reading Goal
- Decision Goal
- Layout
- Grid
- Component
- Responsive
- Accessibility
- Data Contract
- Interaction
- Review Checklist

Nếu thiếu một trong các nội dung trên thì chưa được coi là Blueprint hoàn chỉnh.

---

# 10. UI Principles

Portal BTE không phải:

- Dashboard
- CRM
- ERP
- Data Viewer

Portal BTE là:

> **Decision Support Portal**

Người dùng phải:

1. Hiểu mình là ai.
2. Hiểu điều gì quan trọng.
3. Hiểu vì sao.
4. Biết nên làm gì tiếp.

Sau đó mới đọc dữ liệu kỹ thuật.

---

# 11. Reading Priority

Mọi màn hình phải tuân theo:

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

Knowledge
```

Không được đảo ngược thứ tự này nếu không có quyết định mới từ Product Owner.

---

# 12. Canonical UI Rules

Không sao chép pixel từ ảnh tham chiếu.

Phải học:

- Information Hierarchy
- Reading Flow
- Information Density
- Visual Hierarchy
- Progressive Disclosure

Không bắt chước:

- màu sắc
- icon
- font
- style cụ thể

---

# 13. AI Implementation Rules

Mọi AI tham gia dự án phải tuân thủ:

- Không tự thiết kế lại UI.
- Không thay đổi Information Architecture.
- Không thay đổi Reading Flow.
- Không thay đổi Screen Hierarchy.
- Chỉ hiện thực hóa đúng Blueprint.

---

# 14. Success Criteria

UI Blueprint được coi là thành công khi:

- Cursor có thể triển khai mà không cần suy đoán.
- Product Owner review dựa trên Blueprint thay vì ý kiến cá nhân.
- Toàn bộ Portal có cùng ngôn ngữ thiết kế.
- UI đạt chất lượng thương mại.
- Sprint 01.5 Integration không phải thay đổi giao diện.

---

# 15. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0 | ACTIVE | Khởi tạo UI Blueprint System cho BTE Platform V1.0 |