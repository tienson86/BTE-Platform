# Cấu trúc Module am_duong

## Mục đích

Module am_duong là dữ liệu nền của toàn bộ hệ thống BTE.

Module này chịu trách nhiệm chuyển đổi giữa:

- Dương lịch
- Âm lịch
- Can Chi
- Tiết khí
- Tháng Bát Tự
- Giờ Can Chi

Đây là nguồn dữ liệu chuẩn được sử dụng bởi tất cả các module nghiệp vụ.

## Cấu trúc

am_duong/
├── 01_du_lieu.csv
├── 02_quy_tac.csv
├── cau_truc.md
├── ghi_chu.md
└── README.md

## Vai trò từng file

### 01_du_lieu.csv

Master Calendar.

Mỗi dòng tương ứng với một ngày dương lịch.

### 02_quy_tac.csv

Quy tắc xác định:

- Năm Can Chi
- Tháng Bát Tự
- Giờ Can Chi
- Điều kiện chuyển năm
- Điều kiện chuyển tháng

### cau_truc.md

Mô tả cấu trúc module.

### ghi_chu.md

Giải thích nghiệp vụ.

### README.md

Tài liệu hướng dẫn sử dụng.
