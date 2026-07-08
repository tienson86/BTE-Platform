# Cấu trúc dữ liệu Nạp Âm

## Mục đích

Lưu trữ quan hệ giữa cặp Thiên Can - Địa Chi trong Lục Thập Hoa Giáp với Nạp Âm tương ứng.

Mỗi bản ghi đại diện cho một Nạp Âm gồm hai Can Chi.

---

## Khóa chính

id

---

## Các trường

| Tên trường | Kiểu | Bắt buộc | Mô tả |
|------------|------|----------|-------|
| id | string | Có | Mã định danh duy nhất (NA001–NA030) |
| thu_tu | integer | Có | Thứ tự từ 1 đến 30 |
| ten | string | Có | Tên Nạp Âm |
| ngu_hanh | string | Có | Ngũ hành của Nạp Âm |
| can_chi_1 | string | Có | Can Chi thứ nhất |
| can_chi_2 | string | Có | Can Chi thứ hai |
| mo_ta | string | Không | Giải nghĩa ngắn gọn của tên Nạp Âm |

---

## Quan hệ

- ngu_hanh → 01_ngu_hanh/ngu_hanh.csv
- can_chi_1 → 03_thien_can_dia_chi/luc_thap_hoa_giap.csv
- can_chi_2 → 03_thien_can_dia_chi/luc_thap_hoa_giap.csv
