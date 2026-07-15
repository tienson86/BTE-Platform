02_WUXING

Mục đích:
Chuẩn hóa toàn bộ quy tắc chấm điểm Ngũ hành trong Score Engine.

Các file:

01_element_score.csv
Điểm cơ sở của từng hành.

02_season_score.csv
Điểm theo mùa sinh và tiết khí.

03_root_score.csv
Điểm theo thông căn, tàng can và căn khí.

04_combination_score.csv
Điểm do hợp, hội, bán hợp, hợp hóa.

05_clash_score.csv
Điểm do xung, hình, hại, phá.

06_balance_score.csv
Điểm cân bằng tổng thể Ngũ hành.

07_special_score.csv
Các trường hợp đặc biệt như Tòng cách, Nhất khí, Hóa khí...

Nguyên tắc:
- Mỗi file chỉ quản lý một loại quy tắc.
- Không trùng lặp dữ liệu giữa các file.
- Có thể mở rộng nhiều trường phái bằng cột school.
- Không sửa mã nguồn khi thay đổi trọng số.
