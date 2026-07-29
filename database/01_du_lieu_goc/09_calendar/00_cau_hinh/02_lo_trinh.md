# LỘ TRÌNH PHÁT TRIỂN MODULE lich_am_duong


Version:
1.0


Status:
DESIGN_LOCKED


Ngày:
2026-07-10



# 1. MỤC TIÊU MODULE


Xây dựng Calendar Engine chuẩn hóa:

- Lịch Dương
- Lịch Âm
- Can Chi thời gian
- Tiết khí
- Dữ liệu nền Bát Tự



# 2. GIAI ĐOẠN PHÁT TRIỂN



## Giai đoạn 1: Thiết kế dữ liệu

Trạng thái:

HOÀN THÀNH


Bao gồm:

- Xây dựng cấu trúc thư mục
- Xây dựng mapping
- Xây dựng công thức
- Xây dựng thứ tự tính


Kết quả:

DESIGN_LOCKED v1.0



--------------------------------


## Giai đoạn 2: Xây dựng Calendar Engine


Trạng thái:

CHƯA THỰC HIỆN


Công việc:

- Đọc file CSV
- Nhận input ngày giờ
- Xử lý lịch
- Sinh dữ liệu đầu ra


Kết quả:

Engine Alpha



--------------------------------


## Giai đoạn 3: Kiểm thử


Trạng thái:

CHƯA THỰC HIỆN


Kiểm tra:

- Ngày sinh mẫu
- Năm nhuận
- Tháng nhuận
- Giao tiết khí
- Giờ Tý sớm / muộn



Kết quả:

Calendar Engine Beta



--------------------------------


## Giai đoạn 4: Sinh dữ liệu


Trạng thái:

CHƯA THỰC HIỆN


Sinh:

01_du_lieu.csv


Phạm vi:

1900 - 2100


Bao gồm:

- Ngày âm
- Can Chi
- Tiết khí
- Trực
- Hoàng đạo



--------------------------------


## Giai đoạn 5: Tích hợp BTE Core


Trạng thái:

SAU NÀY


Kết nối:

lich_am_duong

↓

03_can_chi

↓

04_nap_am

↓

05_bat_tu_core



# 3. QUY TẮC PHÁT TRIỂN


Không bỏ qua thứ tự.

Không viết Engine trước khi:

- Mapping hoàn thiện
- Công thức hoàn thiện
- Thuật toán khóa


# 4. VERSION


v1.0

Thiết kế.


v1.1

Hoàn thiện Engine.


v1.2

Sinh dữ liệu.


v2.0

Mở rộng thiên văn chính xác.
