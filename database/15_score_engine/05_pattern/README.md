05_PATTERN

Mục đích
--------
Đánh giá mức độ thành công của Cách cục sau khi Pattern Engine đã xác định loại Cách.

Các file

01_pattern_success.csv
Điểm cộng cho các Cách cục thành.

02_pattern_failure.csv
Điểm trừ khi Cách cục bị phá hoặc không đủ điều kiện.

03_pattern_priority.csv
Hệ số ưu tiên khi nhiều quy tắc Cách cục cùng thỏa mãn.

04_special_pattern.csv
Điểm cho các Cách cục đặc biệt (Hóa Khí, Nhất Khí, Thiên Nguyên Nhất Khí, Củng Cách...).

05_follow_pattern.csv
Đánh giá các Tòng Cách và các trường hợp Tòng giả.

Nguyên tắc
----------
- Pattern Engine chịu trách nhiệm xác định Cách cục.
- Score Engine chỉ đánh giá chất lượng của Cách cục.
- Điểm Cách cục phải kết hợp với kết quả của Strength Engine và Useful God Engine.
- Không xác định lại Cách cục trong Score Engine để tránh trùng lặp logic.
