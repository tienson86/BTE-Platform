# BTE Knowledge Canon Specification
## Document ID

BTE-KC-001

---

# Version

V1.0.0

---

# Status

Official

---

# Author

BTE Platform

---

# Last Updated

2026-07-30

---

# 1. Mục đích

Tài liệu này là đặc tả chính thức (Canonical Specification) của toàn bộ hệ thống tri thức BTE Platform.

Đây là tài liệu có mức ưu tiên cao nhất trong hệ thống Knowledge.

Mọi tài liệu học thuật, Rule Database, Sentence Library, Report Template và Runtime Engine đều phải tuân thủ đặc tả này.

Nếu có mâu thuẫn giữa tài liệu này và bất kỳ tài liệu nào khác thì tài liệu này được ưu tiên.

---

# 2. Triết lý thiết kế

BTE Platform được xây dựng theo nguyên tắc:

> Một nguồn tri thức duy nhất (Single Source of Truth).

Knowledge chỉ tồn tại ở một nơi.

Không được sao chép.

Không được trùng lặp.

Không được viết nhiều phiên bản cùng một nội dung.

Tri thức gốc được viết dưới dạng Markdown.

Rule Engine không được tự định nghĩa tri thức.

Sentence Library không được tự tạo quy tắc.

Runtime Engine không được sửa đổi Knowledge.

---

# 3. Kiến trúc tổng thể

```

BTE-Platform/

├── engines/
├── frontend/
├── tests/
│
├── knowledge/
│
│   ├── bazi/
│   ├── numerology/
│   ├── meihua/
│   │
│   ├── rule_database/
│   ├── sentence_library/
│   ├── phrase_library/
│   ├── terminology/
│   ├── report_templates/
│   │
│   ├── governance/
│   └── infrastructure/

```

---

# 4. Phạm vi

Phiên bản đầu tiên của BTE Knowledge Canon bao gồm:

• Bát Tự (Core Domain)

Các miền bổ trợ:

• Sim số
• Mai Hoa Dịch Số

Các lĩnh vực sau KHÔNG nằm trong phạm vi của Canon V1:

- Dương Trạch
- Âm Trạch
- Kỳ Môn Độn Giáp
- Tử Vi
- Lục Hào
- Kinh Dịch tổng quát

Nếu sau này phát triển sẽ được xem như một Domain độc lập.

---

# 5. Kiến trúc Knowledge

Knowledge được chia thành ba tầng.

## Tầng 1

Canonical Knowledge

Đây là tri thức học thuật.

Được viết bằng Markdown.

Đây là nguồn tri thức duy nhất.

---

## Tầng 2

Rule Database

Đây là tri thức đã được chuẩn hóa thành Rule JSON.

Không được bổ sung Rule nếu chưa có nguồn trong Canon.

---

## Tầng 3

Runtime

Engine chỉ đọc Rule.

Không đọc trực tiếp Markdown.

---

# 6. Pipeline

Markdown

↓

Knowledge Canon

↓

Rule Database

↓

Analysis Engine

↓

Sentence Library

↓

Report Engine

↓

Report

---

# 7. Single Source of Truth

Mọi kết luận đều phải truy ngược được về Canon.

Ví dụ:

Rule

↓

Knowledge

↓

Chapter

↓

Section

↓

Paragraph

---

# 8. Quy tắc không trùng lặp

Một khái niệm chỉ được định nghĩa một lần.

Ví dụ:

"Dụng Thần"

được định nghĩa tại

05_useful_god_knowledge

Không được định nghĩa lại ở

09_luck_knowledge

Nếu cần chỉ được tham chiếu.

---

# 9. Dependency

Knowledge có thể phụ thuộc.

Ví dụ

Strength

↓

Temperature

↓

Pattern

↓

Useful God

Nhưng không được phụ thuộc vòng.

---

# 10. Versioning

Mỗi Module có Version riêng.

Ví dụ

01_fundamental_knowledge

V1.0.0

02_strength_knowledge

V1.0.0

---

# 11. Freeze Policy

Khi Module đã Freeze

không được sửa trực tiếp.

Mọi thay đổi phải tăng Version.

---

# 12. Quy tắc tham chiếu

Không Copy nội dung.

Chỉ Reference.

Ví dụ

See:

01_fundamental_knowledge

Chapter 03

Section 2

---

# 13. Quy tắc đặt tên

Toàn bộ thư mục

snake_case

Toàn bộ file

snake_case

Knowledge ID

UPPER_CASE

Rule ID

UPPER_CASE

Sentence ID

UPPER_CASE

---

# 14. Quy tắc Metadata

Mọi tài liệu phải có

Document ID

Version

Status

Author

Created

Updated

Dependencies

Knowledge IDs

---

# 15. Quality Standards

Một chương chỉ được xem là hoàn thành khi:

✓ Nội dung đầy đủ

✓ Có ví dụ

✓ Có Case Study

✓ Có Reference

✓ Có Mapping Rule

✓ Có Glossary

✓ Đã Review

✓ Đã Freeze

---

# 16. Mục tiêu cuối cùng

BTE Knowledge Canon hướng tới việc xây dựng một kho tri thức chuẩn hóa, nhất quán và có khả năng truy vết hoàn toàn, làm nền tảng cho mọi Engine và mọi kết quả luận giải của BTE Platform.

Không có Runtime nào được phép vượt quyền Canon.

Không có Rule nào được phép tồn tại nếu không có nguồn tri thức.

Không có kết luận nào được phép không truy vết được về Canon.