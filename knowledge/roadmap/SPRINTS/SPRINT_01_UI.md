# BTE Platform V1.0

# Sprint 01 — Portal UI Foundation

Version: 1.0

Status:
READY

Priority:
P0 (Highest)

Estimated:
5–7 Days

Owner:
Frontend

Reviewer:
ChatGPT

---

# 1. Sprint Goal

Hoàn thiện toàn bộ giao diện Portal đạt chất lượng thương mại.

Sprint này KHÔNG phát triển logic Bát Tự.

KHÔNG viết Rule.

KHÔNG sửa Engine.

Chỉ tập trung vào UI.

---

# 2. Scope

Bao gồm

✔ Design System

✔ Layout

✔ Components

✔ Portal

✔ Responsive

✔ UX

Không bao gồm

✘ Engine

✘ API

✘ Database

✘ Interpretation

✘ Report PDF

---

# 3. Architecture

applications/

    portal/

        src/

            components/

            layouts/

            pages/

            hooks/

            services/

            styles/

            theme/

            icons/

            assets/

Không đổi cấu trúc.

---

# 4. Design Principles

Portal phải giống SaaS hiện đại.

Ưu tiên

- Đơn giản

- Rõ ràng

- Ít màu

- Nhiều khoảng trắng

- Font lớn

- Card đẹp

- Responsive

---

# 5. Design Tokens

Primary Color

Emerald

Secondary

Slate

Danger

Red

Warning

Amber

Success

Green

Radius

12px

Shadow

Soft

Spacing

8px Grid

Animation

200ms

---

# 6. Component Library

Cursor chỉ được sử dụng component chuẩn.

Danh sách bắt buộc

□ Button

□ Card

□ Input

□ Select

□ Checkbox

□ Radio

□ Switch

□ Tabs

□ Badge

□ Chip

□ Alert

□ Progress

□ Tooltip

□ Dialog

□ Drawer

□ Table

□ Skeleton

□ Empty State

□ Error State

□ Loading Spinner

Nếu thiếu phải bổ sung.

Không được tạo component trùng chức năng.

---

# 7. Portal Screens

Sprint này hoàn thiện

□ Dashboard

□ Calendar

□ Bazi Result

□ Analysis

□ Interpretation

□ Discussion

□ Profile

□ Login

□ Register

□ Settings

---

# 8. Bazi Result Screen

Đây là màn hình quan trọng nhất.

Phải đạt chất lượng production.

Bao gồm

Header

Summary Cards

Four Pillars

Strength

Five Elements

Ten Gods

Useful God

Lucky God

Unlucky God

ShenSha

Luck

Interpretation Preview

Không thay đổi logic.

Chỉ tối ưu hiển thị.

---

# 9. UX Rules

Toàn Portal phải thống nhất

Card Height

Typography

Spacing

Padding

Margin

Hover

Animation

Loading

Error

Responsive

Không được màn hình nào khác style.

---

# 10. Responsive

Desktop

Laptop

Tablet

Mobile

Không được overflow.

Không xuất hiện scrollbar ngang.

---

# 11. Accessibility

Button có hover

Button có focus

Keyboard navigation

Contrast đạt chuẩn

Icon có label khi cần

---

# 12. Performance

Không render dư.

Lazy loading.

Code splitting.

Memo khi cần.

Không optimize quá sớm.

---

# 13. Coding Rules

TypeScript Strict.

Không any.

Không duplicated component.

Không duplicated CSS.

Không hardcode màu.

Không inline style nếu không cần.

---

# 14. Deliverables

Cursor phải hoàn thành

□ Portal UI

□ Responsive

□ Component Library

□ Design Tokens

□ Animation

□ Loading

□ Error State

□ Empty State

---

# 15. Review Checklist

ChatGPT sẽ review

□ Code Structure

□ Naming

□ UI

□ Responsive

□ UX

□ Performance

□ Accessibility

□ Maintainability

Nếu chưa đạt sẽ trả lại.

---

# 16. Definition of Done

Sprint chỉ DONE khi

100% màn hình hiển thị đúng.

Không có lỗi TypeScript.

Không có Warning.

Không có Component trùng.

Responsive đạt.

Review PASS.

Merge vào develop.

---

# 17. Out of Scope

Không sửa Engine.

Không sửa Database.

Không sửa Rule.

Không viết API.

Không Report PDF.

Không AI.

Không thêm tính năng ngoài Sprint.