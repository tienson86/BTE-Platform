# BTE Platform

# Phase 02 — Folder Restructure

Version: 1.0.0

Status: Active

Owner: BTE Platform Architecture

---

# 1. Purpose

Folder Restructure định nghĩa cấu trúc thư mục mục tiêu của Customer Portal sau khi hoàn thành Migration.

Blueprint này chuẩn hóa:

- Source Tree
- Module Boundaries
- Layer Responsibilities
- Import Direction
- Legacy Isolation

Folder Restructure không thay đổi Business Logic.

Folder Restructure chỉ chuẩn hóa tổ chức mã nguồn.

---

# 2. Objectives

Sau khi hoàn thành Folder Restructure:

- Source Tree thống nhất.
- Layer rõ ràng.
- Không còn cấu trúc chồng chéo.
- Legacy được cô lập.
- Commercial UI V3 trở thành cấu trúc chuẩn.

---

# 3. Scope

Bao gồm:

- applications/customer_portal
- src/
- app/
- screens/
- components/
- navigation/
- bindings/
- view_models/
- services/
- layouts/
- styles/
- assets/
- hooks/
- utils/
- constants/
- types/

Không bao gồm:

- engines/
- knowledge/
- backend/
- tests ngoài Portal

---

# 4. Design Principles

## Single Responsibility

Mỗi thư mục chỉ có một nhiệm vụ.

---

## Layer Isolation

Không được phụ thuộc ngược.

```
Application

↓

Screen

↓

Business Component

↓

Shared Component

↓

Base Component

↓

Foundation
```

---

## Stable Imports

Import chỉ theo chiều từ trên xuống.

Không deep import.

Không circular dependency.

---

## Predictable Structure

Mọi developer đều phải đoán được vị trí file.

Ví dụ:

```
view_models/

↓

ExecutiveSummaryViewModel
```

không được đặt ở:

```
business/

utils/

services/
```

---

# 5. Target Folder Structure

```
applications/
└── customer_portal/
    │
    ├── src/
    │   ├── app/
    │   ├── layouts/
    │   ├── navigation/
    │   ├── screens/
    │   ├── components/
    │   │   ├── base/
    │   │   ├── shared/
    │   │   └── business/
    │   ├── bindings/
    │   ├── view_models/
    │   ├── services/
    │   ├── hooks/
    │   ├── styles/
    │   ├── assets/
    │   ├── icons/
    │   ├── constants/
    │   ├── types/
    │   └── utils/
    │
    └── tests/
```

Đây là cấu trúc chuẩn sau Migration.

---

# 6. Folder Responsibilities

## app/

Application bootstrap.

Providers.

Configuration.

---

## layouts/

Page layout.

Reading layout.

Report layout.

---

## navigation/

Commercial UI Navigation.

---

## screens/

Presentation screens.

Không Business Logic.

---

## components/

Base

↓

Shared

↓

Business

---

## bindings/

Presentation Binding.

Không Runtime Logic.

---

## view_models/

Presentation Data.

Không Engine.

---

## services/

UI Services.

Không Analysis Engine.

---

## hooks/

Presentation hooks.

---

## styles/

Design System.

Theme.

Responsive.

Print.

---

## utils/

Presentation Utility.

---

# 7. Legacy Strategy

Legacy không xóa ngay.

Tất cả Legacy phải được đưa vào:

```
legacy/
```

hoặc

```
deprecated/
```

tùy chiến lược của dự án.

Không được để Legacy xen lẫn cấu trúc mới.

---

# 8. Import Rules

Cho phép:

```
Screen

↓

Business

↓

Shared

↓

Base
```

Không cho phép:

```
Base

↓

Business
```

Không cho phép:

```
Shared

↓

Screen
```

Không cho phép:

```
Business

↓

Engine
```

---

# 9. Migration Rules

Migration phải theo từng nhóm.

Phase 1

Folder

↓

Phase 2

Components

↓

Phase 3

Screens

↓

Phase 4

Bindings

↓

Phase 5

Legacy

Không được thực hiện ngược.

---

# 10. Dependencies

Input:

- 00_MIGRATION_MASTER_PLAN.md
- 01_PORTAL_AUDIT.md
- 02_SCREEN_MAPPING.md

Output:

- 04_UI_MIGRATION_PHASES.md
- 05_BINDING_INTEGRATION.md
- 06_LEGACY_CLEANUP.md

---

# 11. Validation Checklist

✓ Không còn thư mục trùng chức năng.

✓ Không còn circular structure.

✓ Import direction đúng.

✓ Layer đúng.

✓ Legacy được cô lập.

✓ Cấu trúc phù hợp Commercial UI V3.

---

# 12. Risks

## Folder Collision

Tên thư mục mới trùng thư mục cũ.

---

## Broken Imports

Sai đường dẫn sau khi di chuyển.

---

## Circular Dependency

Phụ thuộc ngược giữa các Layer.

---

## Legacy Leakage

Legacy nằm lẫn trong cấu trúc mới.

---

# 13. Exit Criteria

Chỉ chuyển sang

04_UI_MIGRATION_PHASES.md

khi:

- Folder Tree được chuẩn hóa.
- Layer Responsibility rõ ràng.
- Import Rules được xác nhận.
- Legacy Strategy được thống nhất.

---

# 14. Acceptance Criteria

Folder Restructure PASS khi:

- Có Target Folder Structure.
- Không còn cấu trúc chồng chéo.
- Layer rõ ràng.
- Import Direction đúng.
- Architecture Review PASS.

---

# 15. Deliverables

Sau khi hoàn thành phải sinh ra:

```
folder_tree.md

folder_mapping.csv

import_rules.md

layer_matrix.csv

legacy_locations.csv
```

Các tài liệu này sẽ được sử dụng trong toàn bộ quá trình Migration.

---

# 16. Future Compatibility

Cấu trúc này phải hỗ trợ mở rộng cho:

- Customer Portal
- Admin Portal
- Mobile Applications
- Public APIs
- AI Console

Không cần thay đổi kiến trúc thư mục khi bổ sung các sản phẩm trên.

---

# 17. Version History

## Version 1.0.0

- Khởi tạo Folder Restructure Blueprint.
- Chuẩn hóa Source Tree.
- Định nghĩa Layer Responsibility.
- Thiết lập Import Rules.
- Chuẩn hóa Legacy Strategy.