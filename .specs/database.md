# BTE Database Specification

Version: 1.0

---

# 1. Purpose

Định nghĩa cấu trúc dữ liệu của BTE Platform.

Database là nguồn tri thức của hệ thống.

Business Logic không được hard-code nếu có thể biểu diễn bằng dữ liệu.

---

# 2. Storage Format

Ưu tiên

CSV

Sau đó

JSON

Các định dạng khác chỉ sử dụng khi có yêu cầu rõ ràng.

---

# 3. Top-Level Structure

database/

01_calendar/

02_bazi/

03_score/

04_pattern/

05_interpretation/

06_report/

shared/

---

# 4. Naming Convention

- Tiếng Việt không dấu
- snake_case
- Không khoảng trắng
- Không ký tự đặc biệt

Ví dụ

ngu_hanh.csv

thap_than.csv

dung_than.csv

---

# 5. Rule Database

Rule được tổ chức theo nhóm:

- Calendar Rules
- Bazi Rules
- Score Rules
- Pattern Rules
- Interpretation Rules
- Report Templates

Mỗi nhóm có Loader riêng.

---

# 6. Shared Data

shared/

Bao gồm

- heavenly_stems.csv
- earthly_branches.csv
- five_elements.csv
- yin_yang.csv
- relationships.csv
- constants.csv

---

# 7. Rule Priority

Mọi Rule phải có:

- id
- priority
- condition
- action
- enabled

Không phụ thuộc thứ tự đọc file.

---

# 8. Validation

Trước khi sử dụng phải kiểm tra:

- Duplicate ID
- Thiếu dữ liệu bắt buộc
- Giá trị enum không hợp lệ
- Tham chiếu không tồn tại
- Chu kỳ tham chiếu (nếu có)

---

# 9. Access Layer

Engine không đọc CSV trực tiếp.

Luôn thông qua:

Loader

↓

Repository

↓

Service

---

# 10. Versioning

Database phải có:

database_version

Mọi thay đổi schema phải tăng phiên bản.

---

# 11. Backward Compatibility

Không xóa file dữ liệu đang sử dụng.

Nếu thay đổi cấu trúc:

- Giữ Loader cũ nếu cần.
- Có kế hoạch chuyển đổi dữ liệu.

---

# 12. Future Extensions

Cho phép mở rộng sang:

- SQLite
- PostgreSQL
- Cloud Storage

mà không thay đổi Business Logic.

---

END
