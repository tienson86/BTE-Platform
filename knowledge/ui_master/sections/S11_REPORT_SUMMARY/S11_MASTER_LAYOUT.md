# BTE Platform

# S11 — BÁO CÁO TỔNG KẾT

# S11_MASTER_LAYOUT.md

---

## Phiên bản

**1.0.0**

## Trạng thái

**CANONICAL**

## Module

Desktop Canonical UI

## Section

S11

## Tên

**Báo cáo tổng kết**

---

# 1. Mục tiêu

Tài liệu này quy định bố cục (Layout) chuẩn của Section S11.

Đây là tài liệu duy nhất mô tả:

- Information Architecture
- Reading Flow
- Component Hierarchy
- Executive Summary Layout
- Responsive Structure

Không mô tả:

- Typography
- Grid
- CSS
- Design Token

Các nội dung này được định nghĩa trong:

```
S11_MASTER_GRID_VI.md
```

---

# 2. Triết lý bố cục

S11 là **Section kết thúc của toàn bộ Dashboard**.

Mục tiêu:

Người dùng chỉ cần đọc khoảng **30–60 giây** là hiểu:

- Lá số này như thế nào?
- Điều gì quan trọng nhất?
- Nên ưu tiên làm gì?
- Muốn xem sâu thì đi đâu?

S11 phải tạo cảm giác:

> **Đã hoàn thành quá trình phân tích.**

---

# 3. Reading Flow

```
Header

↓

Executive Summary Card

↓

Điểm mạnh

↓

Điểm cần lưu ý

↓

Khuyến nghị hành động

↓

Đọc báo cáo đầy đủ
```

Reading Flow cố định.

Không thay đổi.

---

# 4. Component Tree

```
S11

├── Header
│
├── Executive Summary Card
│
├── Strength Block
│
├── Attention Block
│
├── Recommendation Block
│
└── Footer Link
```

Không thêm Component khác.

---

# 5. Tổng thể Layout

```
┌──────────────────────────────────────────────┐

S11 — BÁO CÁO TỔNG KẾT

┌──────────────────────────────────────────┐
│                                          │
│  KẾT LUẬN TỔNG QUAN                      │
│                                          │
│  Executive Summary                       │
│                                          │
└──────────────────────────────────────────┘

────────────────────────────────────────────

✓ ĐIỂM MẠNH

• ...

• ...

• ...

────────────────────────────────────────────

⚠ ĐIỂM CẦN LƯU Ý

• ...

• ...

• ...

────────────────────────────────────────────

➜ KHUYẾN NGHỊ HÀNH ĐỘNG

→ ...

→ ...

→ ...

────────────────────────────────────────────

Xem báo cáo phân tích đầy đủ →

└──────────────────────────────────────────────┘
```

---

# 6. Header

Bao gồm:

```
S11 — BÁO CÁO TỔNG KẾT
```

Không có Icon.

Không Badge.

Không KPI.

---

# 7. Executive Summary Card

Đây là vùng quan trọng nhất.

Nội dung:

- Tiêu đề
- Executive Summary

Ví dụ:

```
KẾT LUẬN TỔNG QUAN

Bạn có nền tảng mệnh cục tốt,
khả năng phát triển bền vững,
nếu phát huy đúng điểm mạnh
và cân bằng cảm xúc.
```

Không quá 5 dòng.

---

# 8. Strength Block

Tiêu đề

```
ĐIỂM MẠNH
```

Danh sách:

✓

✓

✓

✓

Không quá:

5 mục.

---

# 9. Attention Block

Tiêu đề

```
ĐIỂM CẦN LƯU Ý
```

Danh sách:

•

•

•

•

Không quá:

5 mục.

---

# 10. Recommendation Block

Tiêu đề

```
KHUYẾN NGHỊ HÀNH ĐỘNG
```

Danh sách:

→

→

→

→

Không quá:

5 mục.

Khuyến nghị phải cụ thể.

Không chung chung.

---

# 11. Footer

Luôn hiển thị:

```
Xem báo cáo phân tích đầy đủ →
```

Text Link.

Không Button.

Không Icon riêng.

---

# 12. Information Hierarchy

★★★★★

Executive Summary

★★★★★

Kết luận

★★★★☆

Điểm mạnh

★★★★☆

Điểm cần lưu ý

★★★★☆

Khuyến nghị

★★☆☆☆

Footer

---

# 13. White Space

Giữa các Block luôn có Divider.

Không ghép hai Block.

Không tạo cảm giác dồn.

---

# 14. Layout Rules

Executive Summary luôn nằm trên.

Footer luôn nằm cuối.

Không đổi vị trí.

Không đảo thứ tự.

---

# 15. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có báo cáo tổng kết.

Vui lòng hoàn thành phân tích trước.
```

Không để Block rỗng.

---

# 16. Responsive

Desktop

Một Card.

Tablet

Một Card.

Mobile

Một Card.

Reading Flow giữ nguyên.

---

# 17. Quan hệ với Report Engine

Dashboard

↓

Executive Summary

↓

Report Link

↓

Report Engine

S11 không hiển thị toàn bộ báo cáo.

---

# 18. Những điều KHÔNG được phép

✗ Biểu đồ

✗ KPI

✗ Pie Chart

✗ Gauge

✗ Rule

✗ JSON

✗ Debug

✗ Score chi tiết

✗ Dashboard phụ

✗ Accordion

✗ Tabs

---

# 19. Design Decision

S11 được thiết kế như:

```
Executive Closing Report
```

Không phải:

```
Knowledge Base

hoặc

Technical Report
```

Người dùng phải có cảm giác:

> "Tôi đã hiểu kết quả và biết mình nên làm gì tiếp theo."

---

# 20. Mapping với Design Pattern

S11 sử dụng:

- PATTERN_05_DECISION_CARD
- PATTERN_06_INFORMATION_LIST
- PATTERN_08_KNOWLEDGE_CARD
- PATTERN_10_REPORT_BLOCK

Không tạo Pattern mới.

---

# 21. Freeze Statement

S11_MASTER_LAYOUT.md là tài liệu quy định bố cục chuẩn của Section S11.

Frontend, UI Designer, QA và Cursor AI phải triển khai đúng theo tài liệu này.

Nếu có khác biệt giữa giao diện và tài liệu thì:

**S11_MASTER_LAYOUT.md là Single Source of Truth cho Layout của Section S11.**