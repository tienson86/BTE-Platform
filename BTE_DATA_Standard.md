# BTE_DATA_STANDARD.md

# BTE Platform
## Data Standard Specification
Version: 1.0

---

# 1. Mục đích

Tài liệu này quy định toàn bộ tiêu chuẩn dữ liệu của dự án BTE (BaTu Engine).

Mọi dữ liệu trong hệ thống phải tuân theo tài liệu này nhằm đảm bảo:

- Đồng nhất
- Dễ bảo trì
- Có thể mở rộng
- Phù hợp Rule Engine
- Phù hợp AI
- Phù hợp Knowledge Graph
- Phù hợp API thương mại

---

# 2. Kiến trúc dữ liệu

BTE chia thành 4 tầng.

01_core_data
↓

02_relationship

↓

03_rules

↓

04_engine

Trong đó

Core Data
=
Fact

Relationship
=
Ontology

Rules
=
Inference

Engine
=
Execution

---

# 3. Nguyên tắc thiết kế

## 3.1 Single Source of Truth

Mỗi dữ liệu chỉ được lưu một lần.

Ví dụ

Ngũ Hành của Giáp

chỉ tồn tại

01_core_data/thien_can

không lưu lại ở bất kỳ module nào khác.

---

## 3.2 Atomic Data

Mỗi cột chỉ biểu diễn một thuộc tính.

Không gộp nhiều thông tin trong một ô.

Đúng

chi_1
chi_2
chi_3

Sai

Thân,Tý,Thìn

---

## 3.3 Không lưu dữ liệu suy diễn

Ví dụ

Sai

Mùa Đông

Đúng

Thủy

Engine tự suy ra.

---

## 3.4 Fact và Rule tách biệt

Ontology

chỉ lưu

Fact

Rule Engine

mới xử lý

if

else

score

weight

priority

---

# 4. Chuẩn thư mục

Mỗi module đều có cấu trúc.

module/

README.md

cau_truc.md

du_lieu.csv

ghi_chu.md

---

# 5. Chuẩn CSV

UTF-8

Unicode NFC

Dấu phân cách

,

Một dòng

=

Một Record

Không Merge Cell

Không xuống dòng trong dữ liệu

---

# 6. Quy tắc đặt tên File

Tên file

snake_case

Ví dụ

tam_hop.csv

thap_than.csv

truong_sinh.csv

Không dùng khoảng trắng.

---

# 7. Quy tắc đặt tên Cột

snake_case

Ví dụ

chi_1

ngu_hanh

am_duong

không dùng

Chi1

Chi-1

Chi 1

---

# 8. Quy tắc ID

ID

không được thay đổi.

Ví dụ

TH001

TH002

TC001

NA001

TT001

TS001

ID là khóa chính.

---

# 9. Kiểu dữ liệu

String

Integer

Boolean

Enum

Date

Không dùng kiểu hỗn hợp.

---

# 10. Enum

Ví dụ

Ngũ Hành

Kim

Mộc

Thủy

Hỏa

Thổ

Không viết

kim

MOC

Fire

---

# 11. Giá trị Null

Không có dữ liệu

=

để trống

Không dùng

NULL

None

N/A

Unknown

---

# 12. Chuẩn mô tả

Mô tả

không dùng để Engine xử lý.

Chỉ dùng cho người đọc.

---

# 13. Chuẩn Version

Version

Major.Minor.Patch

Ví dụ

1.0.0

1.1.0

2.0.0

---

# 14. Quy tắc mở rộng

Không sửa ID.

Không đổi tên cột.

Chỉ thêm Record.

Hoặc thêm Module.

---

# 15. Chuẩn Ontology

Entity

Quan hệ

Thuộc tính

được tách riêng.

Ví dụ

Thiên Can

Entity

Quan hệ Thiên Can

Relationship

Hợp Hóa

Rule

---

# 16. Chuẩn Rule Engine

Rule

không nằm trong CSV.

Rule

được lưu riêng.

Ví dụ

rules/

can_hop.yaml

tam_hop.yaml

than_vuong.yaml

---

# 17. Chuẩn API

Mọi Record

phải có

ID

để API truy xuất.

Không dùng tên làm khóa.

---

# 18. Chuẩn AI

AI chỉ đọc

CSV

không đọc

Markdown

Markdown

chỉ dành cho con người.

---

# 19. Chuẩn tài liệu

README.md

Giới thiệu Module

cau_truc.md

Schema

du_lieu.csv

Data

ghi_chu.md

Academic Note

---

# 20. Lịch sử thay đổi

Version 1.0.0

Khởi tạo tiêu chuẩn dữ liệu BTE.
