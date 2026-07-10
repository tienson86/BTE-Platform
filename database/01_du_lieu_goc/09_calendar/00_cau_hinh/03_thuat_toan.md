# THUẬT TOÁN MODULE lich_am_duong


Version:

1.0


Status:

DESIGN_LOCKED



# 1. INPUT


Dữ liệu đầu vào:


NgayDuong

ThangDuong

NamDuong

GioDuong

Phut

MuiGio



Ví dụ:

21/01/1987
04:00
GMT+7



# 2. CHUẨN HÓA THỜI GIAN


Bước 1:

Kiểm tra ngày hợp lệ.


Bước 2:

Chuẩn hóa múi giờ.


Bước 3:

Chuyển sang Julian Day Number.



# 3. TÍNH LỊCH ÂM


Input:

Julian Day


Process:

Tính:

- Ngày âm
- Tháng âm
- Năm âm


Output:

AmLich



# 4. TÍNH CAN CHI NĂM


Input:

NamAm


Process:

Tra vòng 60 Hoa Giáp.


Output:

CanNam

ChiNam



# 5. TÍNH TIẾT KHÍ


Input:

Ngày dương


Process:

Tính vị trí mặt trời.


Output:

TietKhi



# 6. XÁC ĐỊNH THÁNG TỬ BÌNH


Nguyên tắc:


Không dùng:

Tháng âm lịch


Dùng:

Tiết khí



Output:

CanThang

ChiThang

NguyetLenh



# 7. TÍNH NHẬT TRỤ


Input:

Julian Day


Process:

Tra Can Chi ngày.


Output:


CanNgay

ChiNgay



# 8. TÍNH THỜI TRỤ


Input:

CanNgay

GioDiaChi


Công thức:


CanGio =
(CanNgay × 2 + ChiGio)
mod 10



Output:


CanGio

ChiGio



# 9. TÍNH NẠP ÂM


Input:

4 trụ


Process:

Tra bảng 60 Hoa Giáp.


Output:

NapAm



# 10. SINH KẾT QUẢ


Output:


01_du_lieu.csv


Bao gồm:


- Ngày dương
- Ngày âm
- Năm Can Chi
- Tháng Can Chi
- Ngày Can Chi
- Giờ Can Chi
- Tiết khí
- Nguyệt lệnh
- Nạp âm



# 11. KIỂM TRA LỖI


Engine phải kiểm tra:


- Ngày không tồn tại
- Sai múi giờ
- Sai tháng nhuận
- Sai giao tiết khí


Nếu lỗi:

Không sinh dữ liệu.



# 12. NGUYÊN TẮC ENGINE


Engine chỉ xử lý.


Không chứa:

- Công thức cố định
- Rule nghiệp vụ
- Dữ liệu bảng


Tất cả lấy từ:


02_mapping.csv

03_cong_thuc.csv

04_thu_tu_tinh.csv
