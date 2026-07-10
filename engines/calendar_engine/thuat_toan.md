# THUẬT TOÁN CALENDAR ENGINE

Version:
0.1

Status:
DESIGN


# 1. INPUT

Engine nhận:

- Ngày
- Tháng
- Năm
- Giờ
- Phút
- Múi giờ


Ví dụ:

21/01/1987

04:00

GMT+7


# 2. VALIDATE INPUT

Kiểm tra:

- Ngày hợp lệ
- Tháng hợp lệ
- Năm hợp lệ
- Giờ hợp lệ
- Phút hợp lệ
- Timezone hợp lệ

Nếu sai:

Trả về Error.


# 3. LOAD CONFIG

Đọc:

engine_config.csv

↓

timezone.csv

↓

version.csv


# 4. LOAD RULE

Đọc:

02_mapping.csv

↓

03_cong_thuc.csv

↓

04_thu_tu_tinh.csv


# 5. THỰC THI WORKFLOW

Bước 01

Chuẩn hóa thời gian.

↓

Bước 02

Tính Julian Day Number.

↓

Bước 03

Đổi lịch Âm.

↓

Bước 04

Tính Can Chi năm.

↓

Bước 05

Tính Tiết Khí.

↓

Bước 06

Xác định Nguyệt Lệnh.

↓

Bước 07

Tính Can Chi tháng.

↓

Bước 08

Tính Can Chi ngày.

↓

Bước 09

Tính Can Chi giờ.

↓

Bước 10

Tra Nạp Âm.

↓

Bước 11

Tra Trực ngày.

↓

Bước 12

Tra Hoàng đạo.

↓

Bước 13

Tổng hợp dữ liệu.

↓

Bước 14

Kiểm tra kết quả.

↓

Bước 15

Xuất dữ liệu.


# 6. OUTPUT

Engine sinh:

calendar_result.csv

Hoặc:

01_du_lieu.csv


Bao gồm:

- Ngày Dương
- Ngày Âm
- Can Chi năm
- Can Chi tháng
- Can Chi ngày
- Can Chi giờ
- Tiết Khí
- Nguyệt Lệnh
- Nạp Âm
- Trực
- Hoàng Đạo


# 7. XỬ LÝ LỖI

Nếu phát hiện:

- ngày sai
- tháng sai
- năm sai
- giờ sai
- dữ liệu thiếu
- Rule không tồn tại

Engine phải:

- Ghi log
- Trả mã lỗi
- Không sinh dữ liệu sai.


# 8. NGUYÊN TẮC

Engine không được:

- Chứa bảng Can Chi.
- Chứa bảng Nạp Âm.
- Chứa bảng Tiết Khí.
- Chứa Rule nghiệp vụ.

Tất cả đều phải được nạp từ các module dữ liệu.


# 9. MỞ RỘNG

Trong các phiên bản tiếp theo có thể bổ sung:

- Solar Longitude chính xác theo thiên văn.
- Hỗ trợ nhiều múi giờ.
- Hỗ trợ lịch Gregory và Julian.
- API phục vụ Web và Mobile.
