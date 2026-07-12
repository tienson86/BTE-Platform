# MODULE 11 - TÀI VẬN (11_tai_van)

## 1. Mục đích

Module 11_tai_van có nhiệm vụ đánh giá toàn diện năng lực tài chính của một lá số Bát Tự.

Module này không trực tiếp tính toán từ Thiên Can, Địa Chi mà kế thừa kết quả từ các module:

* 03_thap_than
* 04_than_vuong
* 05_dung_than
* 06_dai_van
* 07_luu_nien
* 08_than_sat

Sau đó áp dụng Rule Engine để suy luận mức độ tài vận.

---

# 2. Đầu vào (Input)

## Thập Thần

* Chính Tài
* Thiên Tài
* Chính Quan
* Thất Sát
* Chính Ấn
* Thiên Ấn
* Thực Thần
* Thương Quan
* Tỷ Kiên
* Kiếp Tài

---

## Thân vượng / thân nhược

* Vượng
* Khá vượng
* Cân bằng
* Khá nhược
* Nhược

---

## Dụng thần

* Dụng thần
* Hỷ thần
* Kỵ thần
* Nhàn thần

---

## Đại vận

* Ngũ hành Đại vận
* Thập thần Đại vận
* Xung hợp Đại vận

---

## Lưu niên

* Can năm
* Chi năm
* Thập thần năm
* Xung hợp năm

---

## Thần sát

Ví dụ:

* Thiên Đức
* Nguyệt Đức
* Quốc Ấn
* Văn Xương
* Thiên Ất
* Kiếp Sát
* Đại Hao
* Tiểu Hao
* Phá Toái
* v.v.

---

# 3. Đầu ra (Output)

Engine trả về:

## Điểm tài vận

Giá trị:

0 → 100

---

## Xếp hạng

* Rất yếu
* Yếu
* Trung bình
* Khá
* Mạnh
* Rất mạnh

---

## Loại nguồn thu

Có thể đồng thời nhiều nguồn:

* Lương
* Kinh doanh
* Đầu tư
* Bất động sản
* Chứng khoán
* Nghề chuyên môn
* Dịch vụ
* Tự do
* Hoa hồng
* Nghề phụ

---

## Khả năng

* Kiếm tiền
* Giữ tiền
* Tích lũy
* Đầu tư
* Quản trị tài chính
* Chịu rủi ro

---

## Cảnh báo

Ví dụ:

* Hao tài
* Phá tài
* Bị lừa
* Kiện tụng tài chính
* Đầu tư thất bại
* Nợ xấu
* Chi tiêu quá mức
* Hùn hạp rủi ro

---

## Thời kỳ

Đánh giá theo:

* Đại vận
* Lưu niên

Xác định:

* Giai đoạn phát tài
* Giai đoạn ổn định
* Giai đoạn suy giảm
* Giai đoạn cần phòng thủ

---

# 4. Các bảng dữ liệu

Module gồm các file:

01_loai_tai.csv

Danh mục các loại tài vận.

---

02_rule_nguon_tai.csv

Quy tắc xác định nguồn thu nhập.

---

03_rule_tich_luy.csv

Quy tắc đánh giá khả năng tích lũy tài sản.

---

04_rule_pha_tai.csv

Quy tắc phát hiện nguy cơ hao tài, phá tài.

---

05_rule_dau_tu.csv

Quy tắc đánh giá đầu tư.

---

06_rule_kinh_doanh.csv

Quy tắc đánh giá năng lực kinh doanh.

---

07_rule_nghe_nghiep.csv

Liên kết tài vận với nhóm nghề phù hợp.

---

08_diem_so.csv

Điểm số chuẩn hóa cho từng Rule.

---

09_du_lieu.csv

Tổng hợp dữ liệu chuẩn phục vụ Rule Engine.

---

# 5. Nguyên tắc thiết kế

* Không ghi kết luận cứng.
* Mọi kết luận phải sinh từ Rule Engine.
* Mỗi Rule có mã định danh duy nhất.
* Hỗ trợ nhiều trường phái Bát Tự trong tương lai.
* Cho phép bổ sung Rule mà không thay đổi cấu trúc dữ liệu.
* Tương thích với hệ thống chấm điểm và AI Explain của BTE.

---

# 6. Quan hệ với các Module khác

Phụ thuộc:

03_thap_than

04_than_vuong

05_dung_than

06_dai_van

07_luu_nien

08_than_sat

Kết quả của Module này sẽ được sử dụng bởi:

12_su_nghiep

13_suc_khoe

14_phu_mau

15_tong_luan

