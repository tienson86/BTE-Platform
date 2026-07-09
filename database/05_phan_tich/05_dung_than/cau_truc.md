# Module 05 - DỤNG THẦN

## Mục đích

Module `05_dung_than` là trung tâm suy luận của hệ thống BTE.

Nhiệm vụ:

- Đánh giá sức mạnh Nhật Chủ.
- Xác định Điều Hậu.
- Đánh giá Thân Vượng / Thân Nhược.
- Nhận diện Cách Cục.
- Kiểm tra Tòng Cách.
- Xác định Dụng Thần.
- Xác định Hỷ Thần.
- Xác định Kỵ Thần.
- Sinh kết quả có thể giải thích (Explainable Rule Engine).

---

# Cấu trúc thư mục

05_dung_than/

├── 01_rule_dieu_hau.csv
├── 02_rule_than_vuong.csv
├── 03_rule_cach_cuc.csv
├── 04_rule_tong_cach.csv
├── 05_rule_dung_than.csv
├── 06_rule_hy_than.csv
├── 07_rule_ky_than.csv
├── 08_giai_thich_rule.csv
├── 09_xung_dot_rule.csv
│
├── cau_truc.md
├── ghi_chu.md
├── cong_thuc.md
└── tai_lieu_tham_khao.md

---

# Vai trò từng file

## 01_rule_dieu_hau.csv

Quy tắc xác định Điều Hậu theo:

- mùa sinh
- nhiệt độ
- hàn nhiệt táo thấp
- ưu tiên điều hòa khí hậu

---

## 02_rule_than_vuong.csv

Đánh giá:

- thân vượng
- trung hòa
- thân nhược

Dựa trên:

- nguyệt lệnh
- tàng can
- sinh khắc
- trợ lực
- tiết hao

---

## 03_rule_cach_cuc.csv

Các quy tắc xác định:

- Chính Quan Cách
- Thất Sát Cách
- Chính Tài Cách
- Thiên Tài Cách
- Chính Ấn Cách
- Thiên Ấn Cách
- Thực Thần
- Thương Quan

---

## 04_rule_tong_cach.csv

Các quy tắc:

- Tòng Vượng
- Tòng Cường
- Tòng Tài
- Tòng Quan
- Tòng Sát
- Tòng Nhi
- Tòng Thế

---

## 05_rule_dung_than.csv

Xác định Dụng Thần cuối cùng.

Nguồn dữ liệu:

- Điều Hậu
- Thân Vượng/Nhược
- Cách Cục
- Tòng Cách

---

## 06_rule_hy_than.csv

Xác định Hỷ Thần.

Ưu tiên hành:

- sinh Dụng Thần
- trợ Dụng Thần

---

## 07_rule_ky_than.csv

Xác định Kỵ Thần.

Bao gồm:

- hành phá Dụng Thần
- hành làm mất cân bằng ngũ hành

---

## 08_giai_thich_rule.csv

Lưu nội dung giải thích cho từng Rule.

Engine sử dụng file này để:

- giải thích kết quả
- hiển thị lý do
- đưa ra khuyến nghị

---

## 09_xung_dot_rule.csv

Quản lý xung đột giữa các Rule.

Bao gồm:

- override
- merge
- append
- ignore
- replace

---

# Luồng dữ liệu

Bát tự

↓

Điều Hậu

↓

Thân Vượng/Nhược

↓

Cách Cục

↓

Tòng Cách

↓

Giải quyết xung đột

↓

Dụng Thần

↓

Hỷ Thần

↓

Kỵ Thần

↓

Giải thích kết quả

---

# Module phụ thuộc

01_ngu_hanh

↓

02_quan_he

↓

03_thien_can

↓

04_dia_chi

↓

05_dung_than

↓

06_dai_van

---

# Đầu vào

- Tứ Trụ
- Nhật Chủ
- Thiên Can
- Địa Chi
- Tàng Can
- Quan hệ sinh khắc
- Điểm thân vượng

---

# Đầu ra

- Điều Hậu
- Thân Vượng/Nhược
- Cách Cục
- Tòng Cách
- Dụng Thần
- Hỷ Thần
- Kỵ Thần
- Rule kích hoạt
- Rule bị loại
- Giải thích
- Khuyến nghị
