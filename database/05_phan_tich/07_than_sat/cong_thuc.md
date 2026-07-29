# Công thức đánh giá Thần Sát

Bước 1:
Kích hoạt các thần sát theo 02_rule_kich_hoat.csv.

Bước 2:
Tra điểm Cát tinh trong 03_rule_cat_tinh.csv.

Bước 3:
Tra điểm Hung tinh trong 04_rule_hung_tinh.csv.

Bước 4:
Tổng điểm = Tổng điểm Cát - Tổng điểm Hung.

Bước 5:
Đối chiếu với 05_danh_gia.csv để xác định mức đánh giá.

Bước 6:
Nếu có xung đột, xử lý theo 07_xung_dot_rule.csv.

Bước 7:
Lấy nội dung giải thích từ 06_giai_thich_rule.csv để hiển thị cho người dùng.
