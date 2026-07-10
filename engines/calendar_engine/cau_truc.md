# CALENDAR ENGINE

Version: 0.1

Status:
DESIGN

Ngày tạo:
2026-07-10

Phụ thuộc:
- lich_am_duong v1.0


# 1. MỤC TIÊU

Calendar Engine là bộ xử lý trung tâm chịu trách nhiệm:

- Nhận ngày giờ Dương lịch.
- Chuẩn hóa dữ liệu đầu vào.
- Chuyển đổi Dương lịch → Âm lịch.
- Tính Can Chi năm, tháng, ngày, giờ.
- Tính Tiết Khí.
- Xác định Nguyệt Lệnh.
- Tính các thông tin lịch nền.
- Sinh dữ liệu chuẩn cho các Engine phía sau.

Calendar Engine không thực hiện luận giải Bát Tự.


# 2. KIẾN TRÚC

calendar_engine/

├── core/
│   ├── engine.py
│   ├── loader.py
│   ├── executor.py
│   └── exporter.py
│
├── config/
│   ├── engine_config.csv
│   ├── timezone.csv
│   └── version.csv
│
├── input/
│
├── output/
│
├── processor/
│   ├── lunar_converter.py
│   ├── ganzhi_year.py
│   ├── ganzhi_month.py
│   ├── ganzhi_day.py
│   ├── ganzhi_hour.py
│   ├── jieqi.py
│   ├── zhiri.py
│   └── huangdao.py
│
├── validator/
│
├── tests/
│
├── logs/
│
├── cau_truc.md
├── thuat_toan.md
└── version.txt


# 3. LUỒNG DỮ LIỆU

Input

↓

Validator

↓

Loader

↓

Executor

↓

Processor

↓

Exporter

↓

Output


# 4. THÀNH PHẦN CHÍNH

## Validator

Kiểm tra:

- ngày hợp lệ
- tháng hợp lệ
- năm hợp lệ
- giờ hợp lệ
- múi giờ

Nếu lỗi:

Dừng xử lý.


--------------------------------

## Loader

Đọc:

- 02_mapping.csv
- 03_cong_thuc.csv
- 04_thu_tu_tinh.csv

Không đọc dữ liệu cứng trong source code.


--------------------------------

## Executor

Điều phối toàn bộ workflow.

Không chứa công thức nghiệp vụ.

Executor chỉ thực hiện đúng thứ tự đã định nghĩa trong:

04_thu_tu_tinh.csv


--------------------------------

## Processor

Các Processor xử lý độc lập:

- Lunar Converter
- Ganzhi Year
- Ganzhi Month
- Ganzhi Day
- Ganzhi Hour
- JieQi
- ZhiRi
- HuangDao

Mỗi Processor chỉ có một trách nhiệm.


--------------------------------

## Exporter

Sinh:

calendar_result.csv

Hoặc:

01_du_lieu.csv

tùy chế độ chạy.


# 5. NGUYÊN TẮC THIẾT KẾ

1.

Không viết cứng dữ liệu.

2.

Không viết cứng Rule.

3.

Mọi quy tắc nằm trong CSV.

4.

Engine chỉ đọc và thực thi.

5.

Processor phải độc lập.

6.

Có thể thay thế Processor mà không ảnh hưởng Engine.


# 6. PHỤ THUỘC

calendar_engine

↓

lich_am_duong

↓

03_can_chi

↓

04_nap_am


# 7. PHIÊN BẢN

v0.1

Hoàn thành thiết kế.

Chưa triển khai mã nguồn.
