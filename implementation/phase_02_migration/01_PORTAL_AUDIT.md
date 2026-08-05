# BTE Platform

# Phase 02 — Portal Audit

Version: 1.0.0

Status: Active

Owner: BTE Platform Architecture

---

# 1. Purpose

Portal Audit là bước đầu tiên của Migration.

Mục tiêu của Portal Audit là:

- Hiểu đầy đủ trạng thái hiện tại của Customer Portal.
- Xác định mọi thành phần sẽ được Migration.
- Phân loại thành phần theo chiến lược Migration.
- Làm cơ sở cho Screen Mapping và UI Migration.

Portal Audit không sửa mã nguồn.

Portal Audit chỉ khảo sát, đánh giá và lập danh mục.

---

# 2. Objectives

Sau khi hoàn thành Portal Audit phải biết chính xác:

- Có bao nhiêu màn hình.
- Có bao nhiêu Layout.
- Có bao nhiêu Shared Component.
- Có bao nhiêu Business Component.
- Có bao nhiêu CSS.
- Có bao nhiêu Route.
- Có bao nhiêu Binding.
- Có bao nhiêu Legacy Module.

Không được tồn tại "Unknown Area".

---

# 3. Scope

Bao gồm:

- Customer Portal
- Commercial UI V3
- Legacy UI
- Routing
- Navigation
- Layout
- Theme
- CSS
- Assets
- Bindings
- ViewModels

Không bao gồm:

- Analysis Engine
- Rule Engine
- Knowledge Base
- Runtime Pipeline
- Backend
- API

---

# 4. Audit Principles

## Read Only

Audit không sửa bất kỳ file nào.

---

## Complete

Không bỏ sót bất kỳ module nào.

---

## Traceable

Mọi phát hiện đều phải truy vết được:

- Path
- Module
- Owner
- Purpose

---

## Evidence Based

Mọi kết luận phải dựa trên:

- Source Code
- Folder Structure
- Runtime Structure

Không suy đoán.

---

# 5. Audit Categories

Portal được chia thành các nhóm sau.

## 5.1 Applications

Ví dụ:

```
applications/customer_portal
```

---

## 5.2 Routes

Toàn bộ Routing.

---

## 5.3 Screens

Danh sách màn hình.

---

## 5.4 Layouts

Header

Footer

Sidebar

Reading Layout

Report Layout

...

---

## 5.5 Components

Base

Shared

Business

Legacy

---

## 5.6 Styles

CSS

Theme

Tokens

Legacy Styles

---

## 5.7 Assets

Images

Icons

Fonts

Static Resources

---

## 5.8 Bindings

Presentation Binding

ViewModel

State

---

## 5.9 Legacy

Toàn bộ UI cũ.

---

# 6. Classification Rules

Mọi module phải được phân loại thành đúng một nhóm.

## KEEP

Giữ nguyên.

Ví dụ:

- Engine
- Rule
- Knowledge

---

## REPLACE

Thay bằng Commercial UI V3.

Ví dụ:

Legacy Screen

↓

Commercial Screen

---

## MERGE

Ghép vào hệ thống mới.

Ví dụ:

CSS

↓

Design Tokens

---

## REMOVE

Loại bỏ hoàn toàn.

Ví dụ:

Deprecated UI

Unused CSS

Unused Assets

---

# 7. Audit Deliverables

Mỗi module phải có:

| Field | Description |
|--------|-------------|
| Path | Đường dẫn |
| Type | Screen / Component / Layout / CSS... |
| Purpose | Vai trò |
| Current Status | Active / Legacy |
| Migration Action | KEEP / REPLACE / MERGE / REMOVE |
| Notes | Ghi chú |

---

# 8. Expected Outputs

Portal Audit phải tạo được:

## Module Inventory

Danh mục toàn bộ module.

---

## Screen Inventory

Danh mục toàn bộ màn hình.

---

## Component Inventory

Danh mục toàn bộ Component.

---

## Layout Inventory

Danh mục toàn bộ Layout.

---

## CSS Inventory

Danh mục toàn bộ CSS.

---

## Legacy Inventory

Danh mục toàn bộ Legacy.

---

## Migration Inventory

Danh mục những phần sẽ Migration.

---

# 9. Dependencies

Phụ thuộc:

- Phase 01 Architecture
- Migration Master Plan

Là đầu vào cho:

- 02_SCREEN_MAPPING.md
- 03_FOLDER_RESTRUCTURE.md
- 04_UI_MIGRATION_PHASES.md

---

# 10. Risks

## Missing Module

Bỏ sót module.

---

## Wrong Classification

KEEP thành REMOVE.

REPLACE thành KEEP.

---

## Hidden Dependencies

Module phụ thuộc nhưng không được phát hiện.

---

## Legacy Leakage

Legacy vẫn tồn tại sau Migration.

---

# 11. Validation Checklist

Portal Audit phải xác nhận:

✓ Đã quét toàn bộ Customer Portal.

✓ Đã lập Inventory.

✓ Đã phân loại KEEP.

✓ Đã phân loại REPLACE.

✓ Đã phân loại MERGE.

✓ Đã phân loại REMOVE.

✓ Không còn Unknown Module.

---

# 12. Exit Criteria

Chỉ được chuyển sang

02_SCREEN_MAPPING.md

khi:

- Tất cả Screen đã được kiểm kê.
- Tất cả Component đã được kiểm kê.
- Tất cả Layout đã được kiểm kê.
- Tất cả CSS đã được kiểm kê.
- Mọi module đều có Migration Action.
- Không còn Unknown Area.

---

# 13. Acceptance Criteria

Portal Audit được coi là PASS khi:

- Inventory đầy đủ.
- Phân loại chính xác.
- Có thể truy vết từng module.
- Đủ dữ liệu để thực hiện Screen Mapping.

---

# 14. Version History

## Version 1.0.0

- Khởi tạo Portal Audit Blueprint.
- Chuẩn hóa quy trình kiểm kê hệ thống.
- Thiết lập tiêu chuẩn phân loại Migration.