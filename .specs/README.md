# BTE Platform Specifications

Version: 1.0

## Mục đích

Thư mục `.specs/` chứa toàn bộ đặc tả kỹ thuật chính thức của BTE Platform.

Đây là nguồn tài liệu duy nhất mô tả cách các Engine hoạt động, cách chúng giao tiếp và các hợp đồng (contracts) giữa các thành phần.

Mọi thay đổi về kiến trúc hoặc API phải được cập nhật tại đây trước khi triển khai vào mã nguồn.

---

# Danh sách Specifications

## Core Engines

- calendar_engine.md
- bazi_engine.md
- score_engine.md
- pattern_engine.md
- interpretation_engine.md
- report_engine.md

## Shared Specifications

- database.md
- data_models.md
- api_contracts.md
- pipeline.md
- testing.md

---

# Nguyên tắc

- Specification là tài liệu thiết kế, không phải mã nguồn.
- Mỗi Engine chỉ có một Specification chính thức.
- Nếu mã nguồn và Specification khác nhau, Specification phải được xem xét và cập nhật trước khi sửa mã nguồn.
- AI Agent phải đọc Specification liên quan trước khi sửa Engine.

---

# Chu kỳ phát triển

Requirement
↓

Specification
↓

Implementation
↓

Testing
↓

Review
↓

Release

Không triển khai tính năng mới khi chưa có Specification.

---

END
