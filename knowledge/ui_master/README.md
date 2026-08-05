# knowledge/ui_master/README.md

# BTE Platform

# UI Master Design System

---

Version

1.0.0

Status

ACTIVE

Owner

Product Owner

Purpose

Canonical Master UI for the entire BTE Platform.

---

# 1. Mission

`ui_master/` là bộ thiết kế gốc (Master Design) của toàn bộ BTE Platform.

Đây là nơi định nghĩa giao diện chuẩn cuối cùng trước khi triển khai React.

Không phải Blueprint.

Không phải Wireframe.

Không phải Prototype.

Đây là **Master UI**.

Mọi giao diện được lập trình đều phải được tạo ra từ thư mục này.

---

# 2. Position in Architecture

```
Business Requirements
        │
        ▼
UI Blueprints
        │
        ▼
UI Master
        │
        ▼
React Implementation
        │
        ▼
Review
        │
        ▼
Freeze
```

Blueprint mô tả.

Master UI thể hiện.

React hiện thực.

---

# 3. Single Source of Truth

Đối với giao diện Portal.

Nguồn sự thật duy nhất là:

```
knowledge/ui_master/
```

Không phải:

- CURRENT_PORTAL_UI
- Legacy UI
- Existing Components

---

# 4. Folder Structure

```
ui_master/

README.md

MASTER_DESKTOP_V1.md

MASTER_GRID.md

MASTER_LAYOUT.md

MASTER_COMPONENT_TREE.md

MASTER_UI_REVIEW.md
```

---

# 5. Design Scope

Master UI bao gồm:

- Desktop Layout
- Navigation
- Sidebar
- Header
- Context Header
- Identity Panel
- Overview
- Four Pillars
- Element Balance
- Strength
- Ten Gods
- ShenSha
- Interpretation
- Learning Panel

Không bao gồm:

- React
- CSS
- Tailwind
- API
- Mock Data

---

# 6. Design Principles

Master UI luôn tuân thủ:

- Reading Flow
- Decision Flow
- Information Hierarchy
- Visual Hierarchy
- Progressive Disclosure
- Commercial UX

---

# 7. Implementation Rule

Cursor không được thiết kế UI.

Cursor chỉ được:

Implement the Master UI.

---

# 8. Review Rule

Review dựa trên:

Master UI

không dựa trên:

Current UI

---

# 9. Freeze Policy

Sau khi Master UI được Freeze.

Không thay đổi Layout nếu không có Change Request.

---

# 10. Definition of Done

Master UI hoàn thành khi:

✓ Desktop Layout hoàn chỉnh

✓ Components hoàn chỉnh

✓ Hierarchy hoàn chỉnh

✓ Review PASS

✓ Freeze

---

Version History

| Version | Status | Description |
|----------|---------|-------------|
|1.0.0|ACTIVE|Initial Master UI|