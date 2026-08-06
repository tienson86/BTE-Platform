# BTE Platform

# S01 — README

---

Version

1.0.0

Status

FROZEN

Module

UI Master

Section

S01 — Thông Tin & Định Hướng

---

# 1. Purpose

S01 là section quan trọng nhất của toàn bộ BTE Portal.

Nếu S00 trả lời:

> **"Đây là ai?"**

thì S01 trả lời:

> **"Người này là người như thế nào?"**

S01 không đi sâu vào phân tích kỹ thuật.

S01 cung cấp một **Executive Summary** giúp người dùng hiểu bản thân chỉ trong khoảng **30–60 giây đầu tiên**.

Đây là khu vực có giá trị nhận thức cao nhất sau S00.

---

# 2. Business Objective

S01 giúp người dùng trả lời ngay các câu hỏi:

- Nhật Chủ của tôi là gì?
- Tôi thuộc nhóm người nào?
- Điểm nổi bật của mệnh cục là gì?
- Tôi có xu hướng phát triển theo hướng nào?
- Tôi nên đọc tiếp phần nào?

Sau khi xem S01, người dùng phải có cảm giác:

> "Tôi đã hiểu được bức tranh tổng quát của mình."

---

# 3. UX Goal

S01 phải tạo được ba cảm giác:

### 1. Rõ ràng

Thông tin được phân nhóm hợp lý.

Không gây quá tải.

---

### 2. Dễ đọc

Không yêu cầu người dùng có kiến thức Bát Tự.

Ngôn ngữ phải gần gũi.

Có thể đọc trong dưới một phút.

---

### 3. Muốn khám phá tiếp

S01 chỉ tóm tắt.

Không trình bày toàn bộ luận giải.

CTA sẽ dẫn người dùng sang phần luận giải chi tiết.

---

# 4. Reading Flow

Thứ tự đọc bắt buộc:

```
Thông tin bản mệnh

↓

Điều kiện mệnh cục

↓

Định hướng cuộc đời

↓

CTA
```

Không được thay đổi.

---

# 5. Information Hierarchy

## Level 1

Nhật Chủ

Ví dụ:

```
Bính Hỏa
```

Đây là thông tin nổi bật nhất.

---

## Level 2

Điều kiện mệnh cục

- Mùa sinh
- Cục mệnh
- Thân cư

---

## Level 3

Định hướng cuộc đời

Ba câu hỏi:

- Bạn là ai?
- Thế mạnh của bạn?
- Bạn nên làm gì?

---

## Level 4

CTA

```
Xem luận giải chi tiết →
```

CTA luôn xuất hiện sau khi người dùng đã đọc xong ba nhóm thông tin.

---

# 6. User Journey

```
S00

↓

S01

↓

S08

↓

Báo cáo
```

S01 là cầu nối giữa thông tin hồ sơ và phần luận giải.

---

# 7. Layout Philosophy

S01 sử dụng bố cục hai cột.

```
┌───────────────────────────────────────────────┐

LEFT                     RIGHT

Thông tin bản mệnh        Định hướng

↓

Điều kiện mệnh cục

                          ↓

                          CTA

└───────────────────────────────────────────────┘
```

Lý do:

- Cột trái chứa dữ liệu nhận diện.
- Cột phải chứa dữ liệu định hướng hành động.

Điều này giúp người dùng tách biệt giữa:

> **"Tôi là ai"**

và

> **"Tôi nên làm gì".**

---

# 8. Cognitive Roles

## Identity

Thông tin bản mệnh.

---

## Evidence

Điều kiện mệnh cục.

---

## Recommendation

Định hướng cuộc đời.

---

## Action

CTA.

Đây là mô hình chuẩn của toàn bộ BTE UI.

---

# 9. Visual Weight

Mức độ ưu tiên thị giác.

| Thành phần | Trọng số |
|------------|----------|
| Nhật Chủ | ★★★★★ |
| Điều kiện mệnh cục | ★★★★☆ |
| Định hướng cuộc đời | ★★★★☆ |
| CTA | ★★★☆☆ |
| Metadata | ★★☆☆☆ |

---

# 10. Design Principles

S01 phải:

- Gọn gàng.
- Dễ quét mắt.
- Dễ hiểu.
- Không tạo cảm giác "bảng dữ liệu".
- Không giống báo cáo kỹ thuật.

Ưu tiên:

**Business First**

không phải

**Technical First**.

---

# 11. Decision Principles

Sau khi đọc S01, người dùng phải có thể trả lời:

✓ Tôi là ai?

✓ Tôi thuộc nhóm mệnh nào?

✓ Điểm mạnh của tôi là gì?

✓ Tôi nên phát triển theo hướng nào?

Nếu chưa trả lời được bốn câu hỏi này thì S01 chưa đạt yêu cầu.

---

# 12. Composition Rules

S01 luôn gồm đúng bốn thành phần:

```
Thông tin bản mệnh

↓

Điều kiện mệnh cục

↓

Định hướng cuộc đời

↓

CTA
```

Không thêm.

Không bớt.

Không thay đổi thứ tự.

---

# 13. Freeze Policy

Đã Freeze:

- Reading Flow
- Information Hierarchy
- Two-column Composition
- CTA Position
- Business Structure

Không được thay đổi trong Desktop V1.0.

---

# 14. Dependencies

S01 phụ thuộc:

- S00 (Thông tin bối cảnh)
- S08 (Luận giải tổng hợp)

S01 không phụ thuộc vào:

- S03
- S04
- S05
- S06
- S07

Điều này cho phép người dùng hiểu nhanh trước khi đi vào phân tích chuyên sâu.

---

# 15. Success Criteria

Một người chưa từng biết Bát Tự có thể:

- Đọc S01 trong dưới 60 giây.
- Hiểu mình thuộc nhóm mệnh nào.
- Biết điểm mạnh tổng quát.
- Biết nên đọc tiếp phần luận giải.

Nếu đạt được bốn tiêu chí trên thì S01 hoàn thành đúng mục tiêu thiết kế.

---

# 16. Canonical References

S01 được triển khai theo các tài liệu sau:

Priority 1

```
knowledge/ui_master/assets/
CANONICAL_PORTAL_UI_DESKTOP_V1.png
```

Priority 2

```
S01_MASTER_LAYOUT.md
```

Priority 3

```
S01_MASTER_GRID.png
```

Priority 4

```
S01_MASTER_ANNOTATION.png
```

Priority 5

```
S01_REVIEW_CHECKLIST.md
```

---

# 17. Guiding Principle

S01 không nhằm trình bày toàn bộ kiến thức Bát Tự.

S01 chỉ thực hiện một nhiệm vụ duy nhất:

> **Giúp người dùng hiểu bản thân một cách nhanh chóng, rõ ràng và tạo động lực để tiếp tục khám phá toàn bộ lá số.**