# BTE Platform

# BTE UI Bible

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Applies To:

- Portal
- Report
- Dashboard
- Mobile
- Future Products

This document is the highest-level UI design authority of the BTE Platform.

All UI decisions must comply with this document.

If any implementation conflicts with this document, this document takes precedence.

---

# 1. Vision

BTE không được xây dựng để hiển thị dữ liệu.

BTE được xây dựng để hỗ trợ con người hiểu bản thân và đưa ra quyết định.

UI của BTE không phải là Data Viewer.

Không phải Dashboard.

Không phải CRM.

Không phải ERP.

Không phải Reporting Tool.

BTE là

Professional Decision Support Platform.

Mọi quyết định thiết kế phải phục vụ mục tiêu này.

---

# 2. Core Mission

UI phải giúp người dùng:

Hiểu

↓

Tin tưởng

↓

Ra quyết định

↓

Hành động

Không phải:

Xem thật nhiều dữ liệu.

---

# 3. Design Philosophy

BTE sử dụng triết lý

Decision Before Data.

Nghĩa là:

Người dùng phải biết

điều quan trọng nhất

trước.

Sau đó

mới biết

vì sao.

Cuối cùng

mới xem

dữ liệu kỹ thuật.

---

# 4. Product Position

BTE không cạnh tranh bằng:

- hiệu ứng
- animation
- màu sắc
- card đẹp

BTE cạnh tranh bằng:

- tốc độ hiểu
- độ tin cậy
- khả năng giải thích
- trải nghiệm phân tích chuyên nghiệp

---

# 5. User Promise

Trong 10 giây đầu,

người dùng phải trả lời được:

1. Tôi đang xem đúng hồ sơ?
2. Tôi là ai trong lá số?
3. Lá số mạnh hay yếu?
4. Điều gì quan trọng nhất?
5. Tôi nên làm gì tiếp?

Nếu UI không giúp trả lời 5 câu hỏi này,

UI thất bại.

---

# 6. First Principles

## Principle 01

Decision Before Data

---

## Principle 02

Reading Before Interaction

---

## Principle 03

Identity Before Analysis

---

## Principle 04

Evidence Before Conclusion Detail

---

## Principle 05

Progressive Disclosure

---

## Principle 06

Commercial First

---

## Principle 07

Clarity Over Decoration

---

## Principle 08

One Canonical UI

---

## Principle 09

AI Implementable

---

## Principle 10

Consistency Over Creativity

---

# 7. Reading Model

Portal luôn phải tuân thủ:

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

Không được đảo thứ tự.

---

# 8. Decision Model

Portal phải hỗ trợ

What

↓

Why

↓

Next

Không được

chỉ hiển thị

What.

---

# 9. Information Hierarchy

Mọi màn hình đều phải ưu tiên:

Priority 1

Identity

Priority 2

Condition

Priority 3

Decision

Priority 4

Evidence

Priority 5

Interpretation

Priority 6

Knowledge

---

# 10. Visual Philosophy

Màu sắc

không phải

Hierarchy.

Typography

không phải

Hierarchy.

Hierarchy được tạo bởi:

- Information Priority
- Reading Order
- Layout
- Spacing
- Density

---

# 11. Information Density

BTE hướng tới:

High Information Density

Low Cognitive Load

Không phải:

Ít dữ liệu

↓

Nhiều khoảng trắng.

Không phải:

Nhồi dữ liệu

↓

Khó đọc.

---

# 12. Progressive Disclosure

Không phải mọi thông tin đều hiển thị ngay.

Thông tin được mở dần theo nhu cầu.

Ví dụ:

Summary

↓

Analysis

↓

Interpretation

↓

Learning

---

# 13. Component Philosophy

Component không phải mục tiêu.

Component phục vụ Reading Experience.

Không bao giờ tạo UI từ:

Card

↓

Grid

↓

Button

↓

Done

Luôn bắt đầu từ:

Business Goal

↓

Reading Goal

↓

Layout

↓

Component

---

# 14. Responsive Philosophy

Responsive

không phải

Scale.

Responsive

là

Re-layout.

Desktop

Tablet

Mobile

có thể khác bố cục

nhưng

không được thay đổi Reading Flow.

---

# 15. Accessibility

Mọi người dùng đều phải:

- đọc được
- hiểu được
- phân biệt được
- thao tác được

Accessibility là yêu cầu bắt buộc.

---

# 16. Anti-Patterns

Không được xây dựng Portal theo tư duy:

Dashboard

CRM

ERP

Admin Panel

Spreadsheet

Report PDF

Portal phân tích phải có trải nghiệm riêng.

---

# 17. AI Rules

AI không được:

- tự ý thay đổi IA
- tự ý thêm section
- tự ý đổi Reading Flow
- tự ý đổi Decision Flow
- tự ý sáng tạo ngoài Blueprint

AI chỉ được hiện thực hóa Blueprint.

---

# 18. Review Rules

Mọi UI đều phải vượt qua:

Business Review

↓

UX Review

↓

Visual Review

↓

Technical Review

↓

Product Owner Approval

---

# 19. Success Metrics

Một UI thành công khi:

- Người dùng hiểu kết quả trong < 10 giây.
- Không cần giải thích cách sử dụng.
- Có thể demo ngay cho khách hàng.
- Có thể triển khai nhất quán bởi nhiều lập trình viên hoặc AI.
- Không cần thay đổi khi bước sang Sprint Integration.

---

# 20. Foundation Rule

BTE_UI_BIBLE.md

là tài liệu gốc.

Các tài liệu sau phải tuân thủ:

- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_USER_JOURNEY.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_GRID_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_SCREEN_SPECIFICATIONS.md
- Mọi Screen Blueprint

Nếu có mâu thuẫn,

BTE_UI_BIBLE.md

được ưu tiên.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial UI Constitution for BTE Platform |