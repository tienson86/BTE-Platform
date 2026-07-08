# Ghi chú

## Giới thiệu

Tiết Khí (節氣) là hệ thống 24 mốc thời gian trong năm được xác định theo vị trí biểu kiến của Mặt Trời trên Hoàng Đạo. Mỗi Tiết Khí cách nhau 15° kinh độ và phản ánh sự thay đổi của khí hậu, thời tiết và mùa vụ.

Trong học thuật Bát Tự (Tứ Trụ), Tiết Khí có vai trò đặc biệt quan trọng vì tháng được xác định theo **Tiết** chứ không theo tháng âm lịch.

---

## Mục đích sử dụng

Bảng dữ liệu này được sử dụng để:

- Xác định tháng Tiết trong Bát Tự.
- Xác định thời điểm chuyển tháng Can Chi.
- Tính Đại Vận.
- Tính Lưu Niên.
- Xây dựng lịch pháp truyền thống.
- Phân tích các mô hình huyền học có liên quan đến thời khí.

---

## Nguyên tắc xây dựng dữ liệu

- Có tổng cộng **24 Tiết Khí**.
- Mỗi Tiết Khí kéo dài khoảng **15° kinh độ Hoàng Đạo**.
- Thứ tự bắt đầu từ **Lập Xuân** và kết thúc tại **Đại Hàn**.
- Kinh độ được tính theo vị trí biểu kiến của Mặt Trời trên Hoàng Đạo.
- Mỗi năm thời điểm chuyển Tiết có thể chênh lệch vài giờ do chuyển động thiên văn và năm nhuận.

---

## Ý nghĩa các trường dữ liệu

### id

Mã định danh duy nhất của Tiết Khí.

Ví dụ:

- TK001
- TK002
- ...
- TK024

---

### thu_tu

Thứ tự của Tiết Khí trong năm.

Giá trị từ:

1 → 24

---

### ten

Tên Tiết Khí bằng tiếng Việt.

Ví dụ:

- Lập Xuân
- Thanh Minh
- Đông Chí

---

### ten_han

Tên Hán của Tiết Khí.

Ví dụ:

- 立春
- 清明
- 冬至

---

### kinh_do_bat_dau

Kinh độ Hoàng Đạo (độ) tại thời điểm bắt đầu Tiết Khí.

Ví dụ:

Lập Xuân bắt đầu tại:

315°

---

### kinh_do_ket_thuc

Kinh độ kết thúc của Tiết Khí.

Ví dụ:

Lập Xuân:

315° → 330°

---

### mua

Mùa tương ứng.

Giá trị:

- Xuân
- Hạ
- Thu
- Đông

---

### thang_am_bat_dau

Tháng âm lịch quy ước mà Tiết Khí thường bắt đầu.

Lưu ý:

Đây chỉ là giá trị tham khảo.

Việc xác định tháng Bát Tự luôn căn cứ theo thời điểm chuyển Tiết thực tế.

---

### ngay_duong_du_kien

Ngày dương lịch xấp xỉ theo lịch Gregory.

Ví dụ:

- 02-04
- 03-21
- 12-22

Ngày thực tế có thể thay đổi theo từng năm và múi giờ.

---

### mo_ta

Mô tả ngắn gọn ý nghĩa của Tiết Khí.

Ví dụ:

"Bắt đầu mùa xuân"

---

## Lưu ý khi sử dụng

- Không sử dụng trường `ngay_duong_du_kien` để tính toán chính xác.
- Khi lập lá số Bát Tự phải sử dụng thời điểm chuyển Tiết được tính theo thiên văn.
- Các thuật toán của BTE Engine sẽ sử dụng kinh độ Mặt Trời hoặc dữ liệu thiên văn để xác định thời điểm chuyển Tiết.

---

## Quan hệ với các bảng khác

Bảng này là dữ liệu nền cho các module:

- Tứ Trụ (Bát Tự)
- Đại Vận
- Lưu Niên
- Lưu Nguyệt
- Lưu Nhật
- Lịch Can Chi
- Lịch Vạn Niên
- BTE Engine

---

## Phiên bản

- Phiên bản: 1.0
- Chuẩn dữ liệu: BTE Core Ontology
- Mã bảng: TIET_KHI
- Tổng số bản ghi: 24
- Định dạng dữ liệu: UTF-8 CSV
