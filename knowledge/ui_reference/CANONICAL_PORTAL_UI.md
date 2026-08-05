# BTE Platform V1.0

# Canonical Portal UI Specification

---

## Document Information

| Item | Value |
|------|-------|
| Document | Canonical Portal UI Specification |
| Version | 1.0 |
| Status | ACTIVE |
| Scope | Portal UI V1.0 |
| Owner | Product Owner |

---

# Purpose

Tài liệu này định nghĩa giao diện chuẩn (Canonical UI) của BTE Platform V1.0.

Đây là nguồn tham chiếu chính thức cho mọi công việc liên quan đến:

- UI
- UX
- Layout
- Information Hierarchy
- Visual Hierarchy

Tất cả màn hình của Portal phải tuân theo tài liệu này.

---

# Design Reference

Reference Image:

```
knowledge/ui_reference/CANONICAL_PORTAL_UI.png
```

Ảnh trên là hình tham khảo về:

- Bố cục
- Cấu trúc thông tin
- Khoảng trắng
- Trải nghiệm người dùng

Không được sao chép từng pixel.

Không clone giao diện.

Phải sử dụng Design System và Component Library của BTE.

---

# Design Philosophy

Portal phải được thiết kế theo nguyên tắc:

**Information First**

Người dùng phải hiểu lá số trong vài giây đầu tiên.

Không phải đọc hết toàn bộ báo cáo mới hiểu kết quả.

Portal là sản phẩm thương mại.

Không phải công cụ kỹ thuật.

---

# Information Hierarchy

Thông tin hiển thị theo đúng thứ tự sau:

## Level 1 — Executive Summary

Đây là phần đầu tiên người dùng nhìn thấy.

Bao gồm:

- Nhật Chủ
- Ngũ Hành Nhật Chủ
- Âm Dương
- Cân Xương Đoán Mệnh
- Đánh giá tổng quan

Mục tiêu:

Trong 5 giây đầu người dùng hiểu:

"Tôi là ai?"

---

## Level 2 — Four Pillars

Hiển thị:

- Năm
- Tháng
- Ngày
- Giờ

Mỗi trụ:

- Thiên Can
- Địa Chi
- Tàng Can
- Nạp Âm
- Trường Sinh

---

## Level 3 — Core Analysis

Bao gồm:

- Thân Vượng / Nhược
- Ngũ Hành
- Dụng Thần
- Hỷ Thần
- Kỵ Thần

Đây là trung tâm của màn hình.

---

## Level 4 — Secondary Analysis

Bao gồm:

- Thập Thần
- Thần Sát
- Quan hệ đặc biệt

---

## Level 5 — Interpretation

Luận giải.

Khuyến nghị.

Giải thích.

---

## Level 6 — Knowledge

Kiến thức.

Thuật ngữ.

Giải thích chuyên sâu.

---

# Reading Flow

Người dùng phải đọc theo thứ tự:

Top

↓

Left

↓

Right

↓

Down

Không được buộc người dùng phải nhảy liên tục giữa các khu vực.

---

# Visual Hierarchy

Thông tin quan trọng hơn phải nổi bật hơn.

Ví dụ:

- Nhật Chủ
- Dụng Thần
- Đánh giá

phải nổi bật hơn

Thần Sát.

---

# Layout Principles

Sử dụng Grid.

Khoảng trắng rộng.

Không nhồi dữ liệu.

Card có chiều cao hợp lý.

Không để card quá dài.

---

# Component Principles

Chỉ sử dụng:

- Design System
- Component Library

Không tạo component mới nếu có thể tái sử dụng.

---

# Responsive

Portal phải hoạt động tốt trên:

- Desktop
- Laptop
- Tablet
- Mobile

Không có horizontal scroll.

---

# UX Principles

Portal không hiển thị toàn bộ dữ liệu cùng lúc.

Áp dụng Progressive Disclosure.

Thông tin đi từ:

Tóm tắt

↓

Chi tiết

↓

Luận giải

↓

Kiến thức

---

# Accessibility

Đảm bảo:

- Keyboard Navigation
- Focus State
- ARIA Label
- Contrast
- Touch Target

---

# Design Consistency

Toàn bộ Portal phải thống nhất về:

- Typography
- Colors
- Iconography
- Border Radius
- Shadows
- White Space

Không tồn tại hai phong cách thiết kế khác nhau.

---

# Out of Scope

Không quy định:

- Business Logic
- Engine
- API
- Database
- Report Engine

---

# Change Management

Không thay đổi Canonical UI nếu chưa có quyết định của Product Owner.

Mọi thay đổi lớn phải:

1. Cập nhật tài liệu này.
2. Cập nhật ảnh tham chiếu.
3. Cập nhật ADR (nếu ảnh hưởng kiến trúc).

---

# Definition of Canonical UI

Một giao diện được coi là đạt chuẩn Canonical khi:

- Tuân thủ Information Hierarchy.
- Tuân thủ Design System.
- Tuân thủ Component Library.
- Đạt chất lượng thương mại.
- Được Product Owner phê duyệt.

Chỉ giao diện đạt chuẩn Canonical mới được phép tích hợp với Backend trong Sprint 01.5.