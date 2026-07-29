# Cấu trúc dữ liệu Tiết Khí

## Mục đích

Lưu trữ danh mục 24 Tiết Khí trong hệ thống lịch pháp truyền thống.

Dữ liệu này được sử dụng để:

- Xác định tháng Tiết trong Bát Tự (Tứ Trụ).
- Tính toán thời điểm chuyển tháng theo Tiết Khí.
- Làm dữ liệu nền cho BTE Engine.
- Hỗ trợ các thuật toán lịch pháp và thiên văn.

---

## Khóa chính

id

---

## Các trường dữ liệu

| Tên trường | Kiểu | Bắt buộc | Mô tả |
|------------|------|----------|------|
| id | string | Có | Mã định danh duy nhất (TK001–TK024) |
| thu_tu | integer | Có | Thứ tự từ 1 đến 24 |
| ten | string | Có | Tên Tiết Khí tiếng Việt |
| ten_han | string | Có | Tên Hán Việt |
| kinh_do_bat_dau | integer | Có | Kinh độ Mặt Trời bắt đầu Tiết Khí (độ) |
| kinh_do_ket_thuc | integer | Có | Kinh độ Mặt Trời kết thúc Tiết Khí (độ) |
| mua | string | Có | Mùa (Xuân, Hạ, Thu, Đông) |
| thang_am_bat_dau | integer | Có | Tháng âm lịch quy ước bắt đầu |
| ngay_duong_du_kien | string | Có | Ngày dương lịch xấp xỉ (MM-DD) |
| mo_ta | string | Không | Mô tả ngắn về Tiết Khí |

---

## Quy ước dữ liệu

- Có tổng cộng 24 bản ghi.
- Thứ tự luôn bắt đầu từ Lập Xuân.
- Kinh độ được tính theo hệ Hoàng Đạo.
- Mỗi Tiết Khí có phạm vi 15°.
- Tiết Khí cuối cùng (Đại Hàn) kết thúc tại 315° để quay lại Lập Xuân.

---

## Quan hệ

Hiện tại bảng này chưa phụ thuộc bảng dữ liệu nào khác.

Trong tương lai sẽ được sử dụng bởi:

- Bảng Tháng Tiết.
- Bảng Tứ Trụ.
- Bảng Đại Vận.
- Bảng Lưu Niên.
- BTE Engine.

---

## Header của du_lieu.csv

```csv
id,thu_tu,ten,ten_han,kinh_do_bat_dau,kinh_do_ket_thuc,mua,thang_am_bat_dau,ngay_duong_du_kien,mo_ta
```
