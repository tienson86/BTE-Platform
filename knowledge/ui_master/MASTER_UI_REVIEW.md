# BTE Platform

# MASTER_UI_REVIEW

---

Version

1.0.0

Status

MASTER

Module

UI_MASTER

Document

MASTER_UI_REVIEW

Owner

Product Owner

Purpose

Canonical review standard for validating every Desktop UI implementation against the Master UI.

---

# 1. Purpose

MASTER_UI_REVIEW định nghĩa quy trình kiểm tra cuối cùng của toàn bộ giao diện BTE Platform.

Đây là tài liệu được Product Owner sử dụng để xác nhận:

- React Implementation
- Cursor Output
- Screenshot Review
- UI Freeze

Mọi giao diện phải vượt qua tài liệu này trước khi được phép Freeze.

---

# 2. Review Philosophy

UI được review bằng:

Master UI

Không review bằng:

- cảm nhận
- sở thích
- ý kiến cá nhân
- "đẹp hơn"
- "hiện đại hơn"

Chỉ có một câu hỏi duy nhất:

> React implementation có giống MASTER_DESKTOP_V1 hay không?

---

# 3. Single Source of Truth

Thứ tự ưu tiên khi review:

Priority 1

MASTER_DESKTOP_V1

↓

Priority 2

CANONICAL_PORTAL_UI.png

↓

Priority 3

MASTER_LAYOUT

↓

Priority 4

MASTER_COMPONENT_TREE

↓

Priority 5

Blueprint Documents

Không review theo Legacy UI.

Không review theo Current UI.

---

# 4. Required Deliverables

Cursor bắt buộc nộp:

✓ Build PASS

✓ TypeScript PASS

✓ Test PASS

✓ Desktop Screenshot

✓ Tablet Screenshot (khi yêu cầu)

✓ Mobile Screenshot (khi yêu cầu)

✓ Completion Report

Nếu thiếu một mục:

Không Review.

---

# 5. Desktop Screenshot Review

Desktop Screenshot phải được chụp:

- Full Screen
- 100% Scale
- Không Crop
- Không Zoom
- Không DevTools
- Không Browser Sidebar

Ảnh phải phản ánh đúng giao diện thực tế.

---

# 6. Layout Review

Kiểm tra:

□ Header đúng.

□ Sidebar đúng.

□ Content Width đúng.

□ Safe Area đúng.

□ Section Gap đúng.

□ Card Alignment đúng.

□ Grid đúng.

Nếu Layout sai:

REJECT.

---

# 7. Reading Flow Review

Desktop phải đọc theo:

```
Header

↓

S00

↓

S01

↓

S02

↓

S03

↓

S04

↓

S05

↓

S06

↓

S07

↓

S08

↓

Learning
```

Không được đảo.

---

# 8. Information Hierarchy Review

Kiểm tra:

□ S01 nổi bật nhất.

□ S00 đứng trước S01.

□ S08 luôn sau S07.

□ Learning luôn cuối.

□ Không có Hero thứ hai.

Nếu Hierarchy sai:

REJECT.

---

# 9. Component Review

Kiểm tra từng Component:

□ PortalHeader

□ PortalSidebar

□ S00ContextHeader

□ S01IdentityDecisionPanel

□ S02OverviewActions

□ S03FourPillars

□ S04ElementBalance

□ S05Strength

□ S06TenGods

□ S07ShenSha

□ S08Interpretation

□ LearningPanel

Không được thiếu.

Không được thêm.

---

# 10. Component Tree Review

Kiểm tra:

□ Component Hierarchy đúng.

□ Shared Component đúng.

□ Không Circular Dependency.

□ Không Component thừa.

□ Không Component sai vai trò.

---

# 11. Visual Hierarchy Review

Kiểm tra:

□ Hero nổi bật.

□ Decision nổi bật.

□ Context rõ.

□ Interpretation dễ đọc.

□ Learning không cạnh tranh sự chú ý.

---

# 12. Typography Review

Kiểm tra:

□ Heading đúng cấp.

□ Body đúng.

□ Caption đúng.

□ Metadata không nổi bật hơn Decision.

□ Không dùng Typography ngoài Design System.

---

# 13. Spacing Review

Kiểm tra:

□ Padding.

□ Margin.

□ Section Gap.

□ Card Gap.

□ Alignment.

□ Baseline.

Nếu khoảng cách không đồng nhất:

PASS WITH CHANGES hoặc REJECT.

---

# 14. Responsive Review

Desktop là chuẩn.

Sau khi Desktop PASS mới review:

Tablet

↓

Mobile

Desktop không PASS:

Không review Responsive.

---

# 15. Accessibility Review

Kiểm tra:

□ Focus.

□ Keyboard.

□ Contrast.

□ Semantic.

□ Touch Target (khi Responsive).

Nếu Accessibility sai nghiêm trọng:

REJECT.

---

# 16. Visual Consistency Review

Kiểm tra:

□ Card giống nhau.

□ Badge giống nhau.

□ Chip giống nhau.

□ Button giống nhau.

□ Shadow giống nhau.

□ Border Radius giống nhau.

□ Color Token đúng.

---

# 17. Anti-Pattern Review

Không được có:

✗ Legacy Component.

✗ Legacy Layout.

✗ Duplicate Card.

✗ Duplicate Hero.

✗ Random Spacing.

✗ Random Font.

✗ Random Color.

✗ Mixed Pattern.

Nếu có:

REJECT.

---

# 18. Acceptance Criteria

Một màn hình chỉ được PASS khi:

✓ Layout đúng.

✓ Grid đúng.

✓ Hierarchy đúng.

✓ Reading Flow đúng.

✓ Component Tree đúng.

✓ Typography đúng.

✓ Spacing đúng.

✓ Không còn Legacy UI.

---

# 19. Review Result

Chỉ có ba trạng thái.

PASS

Mọi tiêu chí đạt.

↓

PASS WITH CHANGES

Có lỗi nhỏ.

Không ảnh hưởng Business.

↓

REJECT

Sai Layout.

Sai Hierarchy.

Sai Reading Flow.

Sai Master UI.

---

# 20. Freeze Policy

Sau khi PASS.

Screen được:

Desktop Freeze

↓

Tablet Freeze

↓

Mobile Freeze

↓

Screen Freeze

↓

Portal Freeze

Sau khi Freeze.

Không sửa nếu không có Change Request.

---

# 21. Product Owner Approval

Product Owner xác nhận:

□ Đúng MASTER_DESKTOP_V1.

□ Đúng MASTER_LAYOUT.

□ Đúng MASTER_COMPONENT_TREE.

□ Không còn Legacy UI.

□ Đủ điều kiện Freeze.

Sau khi ký duyệt.

Screen trở thành:

Canonical UI.

---

# Appendix A — Review Workflow

```
Cursor

↓

Build

↓

Screenshot

↓

MASTER_UI_REVIEW

↓

Issue List

↓

Fix

↓

Review

↓

PASS

↓

Freeze
```

---

# Appendix B — Review Matrix

| Category | Required |
|-----------|:--------:|
| Build PASS | ✓ |
| Tests PASS | ✓ |
| Layout | ✓ |
| Grid | ✓ |
| Reading Flow | ✓ |
| Hierarchy | ✓ |
| Components | ✓ |
| Typography | ✓ |
| Spacing | ✓ |
| Accessibility | ✓ |
| No Legacy UI | ✓ |

Tất cả đều bắt buộc.

---

# Appendix C — Review Checklist

## Architecture

□ Layout

□ Grid

□ Hierarchy

□ Reading Flow

---

## Components

□ Header

□ Sidebar

□ Sections

□ Shared Components

---

## Visual

□ Typography

□ Spacing

□ Alignment

□ Cards

□ Colors

---

## Quality

□ Accessibility

□ Responsive

□ Build

□ Tests

---

## Final

□ PASS

□ PASS WITH CHANGES

□ REJECT

□ FREEZE

---

# Appendix D — Cursor Delivery Standard

Mỗi lần hoàn thành một Screen, Cursor chỉ được nộp:

1. Screenshot.

2. Completion Report.

3. Files Modified.

4. Test Result.

Không giải thích dài.

Không mô tả "đẹp hơn".

Không tự đánh giá chất lượng.

Không tự tuyên bố "improved".

Product Owner là người đánh giá duy nhất.

---

# Appendix E — Golden Rules

1. Master UI luôn đúng.
2. React phải giống Master UI.
3. Không sửa Master để khớp React.
4. Sửa React để khớp Master.
5. Không Review theo cảm tính.
6. Không Review theo Legacy UI.
7. Một Screen chỉ Freeze sau khi PASS.
8. Desktop luôn là chuẩn.
9. Responsive chỉ bắt đầu sau Desktop Freeze.
10. Master UI là tài sản thiết kế cao nhất của BTE Platform.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | MASTER | Initial Master UI Review Standard |