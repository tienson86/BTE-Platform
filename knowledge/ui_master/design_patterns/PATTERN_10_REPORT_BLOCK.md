# BTE Platform

# PATTERN_10 — REPORT BLOCK

---

Version

1.0.0

Status

FROZEN

Module

UI Design System

Pattern

10

Name

Report Block

Type

Foundation Pattern

---

# 1. Mục đích

Report Block là Pattern tiêu chuẩn dùng để trình bày một phần (Section) của báo cáo luận giải.

Đây là Pattern cuối cùng trong chuỗi Information Hierarchy của BTE Platform.

Khác với các Pattern trước:

- Decision Card → Đưa ra kết luận.
- Status Panel → Hiển thị trạng thái.
- Knowledge Card → Giải thích kiến thức.
- Report Block → Trình bày nội dung luận giải đầy đủ.

Report Block là nơi người dùng đọc sâu sau khi đã hiểu kết quả tổng quan.

---

# 2. Triết lý

Summary First.

Explanation Second.

Evidence Third.

Người dùng luôn phải nhận được:

Kết luận

↓

Giải thích

↓

Luận giải

↓

Khuyến nghị

Không viết luận giải ngay từ đầu.

---

# 3. Khi nào sử dụng

Áp dụng cho:

• Luận giải Mệnh cục

• Luận giải Dụng thần

• Luận giải Hỷ thần

• Luận giải Đại vận

• Luận giải Lưu niên

• Luận giải Hôn nhân

• Luận giải Sự nghiệp

• Luận giải Tài vận

• Báo cáo AI

• Báo cáo PDF

---

# 4. Không sử dụng

Không dùng cho:

✗ Dashboard

✗ KPI

✗ Timeline

✗ Summary

✗ Decision

✗ Form

---

# 5. Reading Flow

```
Title

↓

Executive Summary

↓

Interpretation

↓

Evidence

↓

Recommendation

↓

Related Knowledge
```

Đây là Reading Flow chuẩn.

---

# 6. Canonical Layout

```
┌──────────────────────────────────────────────┐

LUẬN GIẢI MỆNH CỤC

──────────────────────────────────────────────

TÓM TẮT

Mệnh cục thuộc nhóm Mạnh,
có khả năng tự cân bằng tốt.

──────────────────────────────────────────────

LUẬN GIẢI

Nhật chủ được sinh trợ,
Ngũ hành phân bố khá hài hòa,
khả năng thích nghi cao...

──────────────────────────────────────────────

CƠ SỞ PHÂN TÍCH

• Nhật chủ đắc lệnh

• Mộc sinh Hỏa

• Kim suy

──────────────────────────────────────────────

KHUYẾN NGHỊ

Ưu tiên phát triển lĩnh vực giáo dục,
đào tạo hoặc nghiên cứu.

──────────────────────────────────────────────

KIẾN THỨC LIÊN QUAN →

└──────────────────────────────────────────────┘
```

---

# 7. Component Tree

```
ReportBlock

├── Header
│
├── ExecutiveSummary
│
├── Interpretation
│
├── Evidence
│
├── Recommendation
│
└── RelatedKnowledge
```

---

# 8. Executive Summary

Đây là phần đầu tiên.

Giới hạn:

2–3 dòng.

Trả lời:

"Kết luận là gì?"

Không giải thích dài.

---

# 9. Interpretation

Đây là phần chính.

Giới hạn:

3–6 đoạn.

Mỗi đoạn:

≤ 4 dòng.

Không tạo khối văn bản lớn.

---

# 10. Evidence

Danh sách:

3–6 ý.

Ví dụ

```
• Nhật chủ đắc lệnh

• Hỏa được sinh trợ

• Kim suy

• Không phạm phá cách
```

Không viết thành đoạn.

---

# 11. Recommendation

Một nhóm khuyến nghị.

Gồm:

Điều nên làm

↓

Điều cần tránh

↓

Điểm cần lưu ý

Mỗi mục:

≤ 2 dòng.

---

# 12. Related Knowledge

Một Link.

Ví dụ

```
Xem kiến thức liên quan →
```

Không nhiều CTA.

---

# 13. Information Hierarchy

★★★★★

Executive Summary

★★★★☆

Interpretation

★★★☆☆

Evidence

★★★☆☆

Recommendation

★★☆☆☆

Related Knowledge

---

# 14. Typography

Header

20 px

700

---

Executive Summary

16 px

600

---

Interpretation

15 px

400

---

Evidence

14 px

500

---

Recommendation

14 px

500

---

Link

14 px

600

---

# 15. White Space

Padding

24 px

Header Bottom

20 px

Section Gap

24 px

Paragraph Gap

16 px

List Gap

10 px

Khoảng trắng là thành phần bắt buộc.

---

# 16. Card Style

Background

White

Radius

12 px

Border

1 px

Soft Shadow

Theo Enterprise Design System.

---

# 17. Text Rules

Không đoạn văn nào dài quá:

4 dòng.

Không quá:

700 ký tự

cho một Report Block.

Nếu dài hơn:

Chia thành nhiều Block.

---

# 18. Accessibility

Contrast đạt WCAG AA.

Heading hierarchy đúng chuẩn.

Link keyboard focus.

Không phụ thuộc màu sắc.

---

# 19. Responsive

Desktop

One Column

Tablet

One Column

Mobile

One Column

Không đổi Reading Flow.

---

# 20. Những điều KHÔNG được phép

Không sử dụng:

✗ Đoạn văn dài

✗ Wall of Text

✗ Nhiều CTA

✗ Gradient

✗ Glass

✗ Animation

✗ Accordion mặc định

✗ Tooltip

---

# 21. Các màn hình sử dụng

Áp dụng cho:

✓ Báo cáo luận giải

✓ AI Report

✓ PDF Report

✓ In báo cáo

✓ Customer Report

✓ Expert Report

✓ Report Viewer

---

# 22. Design Principles

Summary

>

Explanation

Explanation

>

Evidence

Evidence

>

Recommendation

Reading

>

Scrolling

Knowledge

>

Decoration

---

# 23. Reusability

Report Block phải tái sử dụng được cho:

Customer Portal

Analysis Console

Admin Portal

PDF Engine

Print Engine

Mobile

Desktop

Chỉ thay đổi nội dung.

Không thay đổi cấu trúc.

---

# 24. Acceptance Criteria

PASS khi:

✓ Người dùng hiểu Executive Summary trong dưới 10 giây.

✓ Interpretation chia thành nhiều đoạn ngắn.

✓ Không có Wall of Text.

✓ Recommendation rõ ràng.

✓ Chỉ có 1 Related Knowledge Link.

✓ Dễ chuyển thành PDF.

---

# 25. Design Decision Record

Report Block là Pattern cuối cùng trong chuỗi trải nghiệm của BTE.

Information Journey:

Identity

↓

Summary

↓

Data

↓

Comparison

↓

Decision

↓

Status

↓

Knowledge

↓

Timeline

↓

Report

Điều này phản ánh triết lý của BTE:

Không bắt người dùng đọc báo cáo ngay từ đầu.

Hệ thống luôn dẫn dắt người dùng:

Hiểu

↓

Tin

↓

Đọc sâu

↓

Hành động

---

# 26. Mapping

Pattern này là nền tảng cho:

| Module | Mức độ |
|----------|---------|
| Report Engine | ⭐⭐⭐⭐⭐ |
| PDF Report | ⭐⭐⭐⭐⭐ |
| Customer Report | ⭐⭐⭐⭐⭐ |
| AI Interpretation | ⭐⭐⭐⭐⭐ |
| Print Report | ⭐⭐⭐⭐⭐ |
| Expert Report | ⭐⭐⭐⭐ |

---

# 27. Relationship với các Pattern khác

Report Block là tầng cuối của Design System.

Thông thường sẽ nhận dữ liệu từ:

PATTERN_05 — Decision Card

↓

PATTERN_06 — Information List

↓

PATTERN_08 — Knowledge Card

↓

PATTERN_09 — Timeline

Report Block không thay thế các Pattern trên.

Nó tổng hợp và trình bày chúng thành một báo cáo hoàn chỉnh.

---

# 28. Future Extensions

Có thể mở rộng:

• Trích dẫn Rule Engine

• Hiển thị nguồn dữ liệu

• AI Confidence

• Tài liệu tham khảo

• Xuất PDF

• Chia sẻ báo cáo

Các mở rộng này phải nằm sau nội dung chính.

Không được làm thay đổi Reading Flow.

---

# 29. Design Language Position

Report Block là Pattern kết thúc hành trình người dùng.

Một hành trình chuẩn của BTE luôn là:

```
Identity
      ↓
Summary
      ↓
Data
      ↓
Comparison
      ↓
Decision
      ↓
Status
      ↓
Knowledge
      ↓
Timeline
      ↓
Report
```

Không được đảo thứ tự này trong các màn hình chính của Customer Portal.

---

# 30. Freeze Statement

PATTERN_10_REPORT_BLOCK.md là tài liệu chuẩn duy nhất mô tả Report Block của BTE Platform.

Mọi màn hình sử dụng Report Block phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

**PATTERN_10_REPORT_BLOCK.md là Single Source of Truth.**