# MODULE: lich_am_duong

## VERSION

Version: 1.0

Status:
DESIGN_LOCKED

Ngày khóa:
2026-07-10


# 1. MỤC ĐÍCH MODULE

Module lich_am_duong là tầng nền Calendar Engine.

Nhiệm vụ:

- Chuyển đổi lịch Dương sang lịch Âm.
- Xác định Can Chi năm, tháng, ngày, giờ.
- Xác định tiết khí.
- Xác định nguyệt lệnh.
- Sinh dữ liệu nền phục vụ:
    - Bát Tự Engine
    - Tử Bình Engine
    - Hoàng lịch Engine
    - Thần Sát Engine
    - Dụng Thần Engine


# 2. CẤU TRÚC THƯ MỤC


lich_am_duong/

│
├── 01_du_lieu.csv
│
├── 02_mapping.csv
│
├── 03_cong_thuc.csv
│
├── 04_thu_tu_tinh.csv
│
├── cau_truc.md
│
├── ghi_chu.md
│
└── version.txt



# 3. CHỨC NĂNG FILE


## 01_du_lieu.csv

Vai trò:

Kho dữ liệu lịch đã sinh.

Trạng thái:

Chưa tạo dữ liệu.

Được sinh bởi Calendar Engine.


Bao gồm:

- ngày dương
- ngày âm
- Can Chi năm
- Can Chi tháng
- Can Chi ngày
- Can Chi giờ
- tiết khí
- trực ngày
- hoàng đạo
- nạp âm


--------------------------------


## 02_mapping.csv

Vai trò:

Bản đồ ánh xạ dữ liệu.

Nhiệm vụ:

Xác định:

Input
    ↓
Processing
    ↓
Output


Ví dụ:

Ngày dương
    ↓
Ngày âm
    ↓
Can Chi ngày
    ↓
Nhật Chủ


--------------------------------


## 03_cong_thuc.csv

Vai trò:

Kho công thức tính.

Bao gồm:

- Công thức Can Chi
- Công thức tiết khí
- Công thức trực ngày
- Công thức hoàng đạo
- Công thức quan hệ địa chi


Engine không chứa công thức cứng.

Engine đọc công thức từ file này.


--------------------------------


## 04_thu_tu_tinh.csv

Vai trò:

Điều khiển workflow.

Quy định thứ tự xử lý:

Input
 ↓
Âm lịch
 ↓
Can Chi
 ↓
Tiết khí
 ↓
Thập thần
 ↓
Kết quả cuối


# 4. LUỒNG DỮ LIỆU


Người dùng nhập:

Ngày / tháng / năm / giờ Dương lịch

↓

Calendar Engine

↓

02_mapping.csv

↓

03_cong_thuc.csv

↓

04_thu_tu_tinh.csv

↓

Sinh:

01_du_lieu.csv


# 5. QUAN HỆ VỚI MODULE KHÁC


lich_am_duong
        |
        |
        ↓

02_quan_he
        |
        ↓

03_can_chi
        |
        ↓

04_nap_am
        |
        ↓

05_bat_tu_core
        |
        ↓

08_than_sat
        |
        ↓

09_hon_nhan
        |
        ↓

10_tu_tuc



# 6. NGUYÊN TẮC THIẾT KẾ


1. Không viết cứng dữ liệu trong Code.

2. Mọi quy tắc phải nằm trong CSV.

3. Engine chỉ đọc và xử lý.

4. Có thể nâng cấp dữ liệu mà không sửa Code.

5. Mỗi thay đổi phải tăng Version.


# 7. TRẠNG THÁI


Version 1.0:

Đã khóa thiết kế.

Chưa triển khai Engine.

Chưa sinh dữ liệu lịch.
