# BTE Platform V1.0

# UI Changelog

---

# Document Information

| Item | Value |
|------|-------|
| Document | UI Changelog |
| Version | 1.0 |
| Status | ACTIVE |
| Scope | Portal UI |
| Owner | Product Owner |

---

# Purpose

Tài liệu này ghi lại toàn bộ các thay đổi quan trọng của giao diện Portal trong suốt vòng đời của BTE Platform.

Mục tiêu:

- Theo dõi quá trình tiến hóa của giao diện.
- Giải thích lý do thay đổi.
- Hỗ trợ Review và Audit.
- Tránh lặp lại các quyết định cũ.

---

# Version History

| Version | Date | Status | Description |
|----------|------|--------|-------------|
| 0.1 | Initial | Archived | Portal UI đầu tiên |
| 0.2 | Sprint 01 | Archived | Dashboard + BaZi Result |
| 0.3 | UI Review 01 | Archived | Sau Wave 3 |
| 1.0 | Canonical UI | Active | Giao diện chính thức của BTE V1 |

---

# UI-001

## Date

2026-08-05

## Status

APPROVED

## Type

Architecture

## Title

Canonical Portal UI

## Description

Quyết định sử dụng giao diện Canonical làm giao diện chính thức của BTE Platform V1.

## Why

Giao diện cũ:

- Quá nhiều card.
- Thiếu phân cấp thông tin.
- Trải nghiệm chưa phù hợp sản phẩm thương mại.

Canonical UI:

- Có Information Hierarchy rõ ràng.
- White Space tốt hơn.
- Visual Hierarchy rõ ràng.
- Dễ mở rộng.

## Impact

- Sprint 01.5 Integration tạm dừng.
- Chuyển sang Canonical UI Migration.
- UI cũ chuyển trạng thái Legacy.

## Related Documents

- CANONICAL_PORTAL_UI.md
- RELEASE_DECISIONS_LOG.md

---

# UI-002

## Type

Information Hierarchy

## Title

Executive Summary lên đầu trang

## Description

Toàn bộ phần đánh giá tổng quan được đưa lên đầu Portal.

## Why

Người dùng cần hiểu ngay:

- Nhật Chủ
- Thân Vượng
- Dụng Thần
- Đánh giá

không phải cuộn xuống nhiều.

## Impact

Cải thiện UX.

---

# UI-003

## Type

Layout

## Title

Thiết kế theo Progressive Disclosure

## Description

Thông tin hiển thị theo tầng:

Executive Summary

↓

Core Analysis

↓

Interpretation

↓

Knowledge

## Why

Giảm tải nhận thức (Cognitive Load).

---

# UI-004

## Type

Component

## Title

Không tạo Component mới ngoài Component Library

## Description

Toàn bộ Portal chỉ sử dụng Component Library.

## Why

Giữ tính thống nhất.

Giảm bảo trì.

---

# UI-005

## Type

Design

## Title

Commercial First

## Description

Portal ưu tiên trải nghiệm sản phẩm thương mại.

Không ưu tiên hiển thị toàn bộ dữ liệu kỹ thuật.

## Why

Khách hàng không cần xem mọi dữ liệu ngay lập tức.

---

# UI-006

## Type

Navigation

## Title

Single Navigation

## Description

Một Sidebar.

Một Header.

Một Flow.

Không nhiều kiểu điều hướng.

---

# UI-007

## Type

Spacing

## Title

Whitespace First

## Description

Ưu tiên khoảng trắng.

Không nhồi dữ liệu.

---

# UI-008

## Type

Responsive

## Title

Responsive Standard

## Description

Desktop là chuẩn.

Tablet và Mobile kế thừa.

Không tạo giao diện riêng.

---

# Pending Changes

| ID | Description | Planned Version |
|----|-------------|-----------------|
| UI-009 | Report UI Canonical | V1.1 |
| UI-010 | Dark Mode | V1.1 |
| UI-011 | Multi-language UI | V2 |
| UI-012 | Mobile App UI | V2 |

---

# Deprecated

## Legacy Portal UI

Status:

Deprecated

Reason:

Được thay thế bằng Canonical Portal UI.

Không tiếp tục phát triển.

Chỉ giữ để tham chiếu.

---

# Governance

Mọi thay đổi lớn về:

- Layout
- Navigation
- Information Hierarchy
- Component Structure
- Visual Hierarchy

đều phải:

1. Cập nhật tài liệu này.
2. Cập nhật `CANONICAL_PORTAL_UI.md`.
3. Cập nhật ảnh tham chiếu nếu cần.
4. Được Product Owner phê duyệt.

---

# Current UI Status

| Area | Status |
|------|--------|
| Design System | ✅ Canonical |
| Component Library | ✅ Canonical |
| Information Architecture | ⏳ v1.1 — Awaiting Freeze Approval |
| Dashboard | ⏸ Paused — pending IA Freeze |
| BaZi Result | ⏸ No section UI until IA v1.1 APPROVED |
| Report | ⏳ Planned |
| Interpretation | ⏳ Planned |
| Settings | ⏳ Planned |

---

# UI-013

## Date

2026-08-05

## Status

ACTIVE

## Type

Process / Architecture

## Title

Round 2 REJECT — Architecture First Reset

## Description

Round 2 (Executive Summary visual polish) bị Product Owner REJECT — sai bài toán (card design thay vì Information Architecture).

## Related Documents

- CANONICAL_PORTAL_INFORMATION_ARCHITECTURE.md

---

# UI-014

## Date

2026-08-05

## Status

ACTIVE

## Type

Information Architecture

## Title

IA v1.1 — PASS WITH CHANGES applied

## Description

Product Owner review v1.0 = PASS WITH CHANGES.

Applied:

1. S01 rename → Identity & Decision Panel
2. Zone A without Cân Xương
3. Zone C → Decision Support (What / Why / Next)
4. Five Elements → Element Balance
5. Knowledge → Learning Panel (expandable, on demand)
6. NEW S00 Context Header before S01

## Impact

- Architecture Freeze chờ APPROVED trên v1.1
- Chưa được thiết kế S00/S01 UI
- Không Integration

## Related Documents

- CANONICAL_PORTAL_INFORMATION_ARCHITECTURE.md (v1.1)

---

# UI-015

## Date

2026-08-05

## Status

**REJECT** — Product Owner Design Review

## Type

Section UI — S00 only

## Title

S00 Context Header (Context Strip)

## Description

Triển khai S00 Context Header theo Screen Specification.

Strip ngữ cảnh ở đầu Result: hồ sơ, mã lá số, giới tính, ngày giờ sinh, phiên bản phân tích, thời điểm phân tích, trạng thái.

## Review Result

REJECT — không vì React/CSS/Component.

Nguyên nhân: hiểu sai triết lý Canonical Portal — tối ưu Component/CRM metadata thay vì Reading Experience / Decision Support.

## Why REJECT

- First fold = admin/CRM record header, không phải decision brief
- Metadata trước, kết luận sau
- Shell Canonical-ish nhưng soul vẫn Dashboard

## Follow-up

- Phân tích: `CANONICAL_UI_COMPARISON_REVIEW.md`
- **STOP implementation** toàn bộ section
- Chỉ thiết kế lại S00 sau khi PO xác nhận Agent đã hiểu đúng Canonical

## Related Documents

- PORTAL_SCREEN_SPECIFICATIONS.md (S00)
- CANONICAL_UI_COMPARISON_REVIEW.md
- migration_report/S00_CONTEXT_HEADER_REVIEW.md
- screenshots/s00_context/

---

# Next Milestone

**PO xác nhận Agent hiểu đúng Canonical Portal**

↓

**Chỉ khi đó: thiết kế lại S00 (intent trước code)**

↓

**Section-by-section UI**

↓

**UI Freeze**

↓

**Sprint 01.5 Integration**
