# MODULE 11 - TÀI VẬN (11_tai_van)

# ghi_chu.md

## 1. Mục đích của Module

Module **11_tai_van** chịu trách nhiệm đánh giá năng lực tài chính của lá số Bát Tự thông qua việc tổng hợp dữ liệu từ các module nền tảng và áp dụng hệ thống Rule Engine.

Module này **không tự tính Thập Thần, Thân Vượng, Dụng Thần hay Đại Vận**, mà chỉ sử dụng kết quả đã được chuẩn hóa từ các module trước để suy luận.

Đây là một module đánh giá (Evaluation Module), không phải module tính toán cơ sở (Calculation Module).

---

# 2. Phạm vi đánh giá

Module có khả năng đánh giá các khía cạnh sau:

* Khả năng kiếm tiền.
* Khả năng giữ tiền.
* Khả năng tích lũy tài sản.
* Khả năng đầu tư.
* Khả năng kinh doanh.
* Mức độ ổn định tài chính.
* Nguy cơ hao tài.
* Nguy cơ phá sản.
* Rủi ro đầu tư.
* Thời kỳ phát tài.
* Thời kỳ suy giảm tài vận.
* Mức độ phù hợp với từng hình thức tạo thu nhập.

---

# 3. Nguồn dữ liệu sử dụng

Module kế thừa dữ liệu từ:

| Module        | Nội dung                                                           |
| ------------- | ------------------------------------------------------------------ |
| 03_thap_than  | Chính Tài, Thiên Tài, Thực Thần, Thương Quan, Tỷ Kiên, Kiếp Tài... |
| 04_than_vuong | Thân vượng, thân nhược                                             |
| 05_dung_than  | Dụng thần, Hỷ thần, Kỵ thần                                        |
| 06_dai_van    | Chu kỳ 10 năm                                                      |
| 07_luu_nien   | Từng năm                                                           |
| 08_than_sat   | Các thần sát liên quan tài vận                                     |
| 09_hon_nhan   | (tham chiếu khi đánh giá tài vận sau kết hôn)                      |
| 10_tu_tuc     | (tham chiếu khi đánh giá gánh nặng tài chính gia đình)             |

---

# 4. Nguyên tắc đánh giá

Mọi kết luận đều phải được tạo từ Rule Engine.

Không tồn tại kết luận được ghi cứng trong dữ liệu.

Ví dụ:

Không viết:

> Có Chính Tài thì giàu.

Mà phải viết:

Điều kiện:

* Chính Tài vượng
* Thân đủ lực
* Dụng thần hỗ trợ
* Không bị Kiếp Tài phá
* Đại vận trợ Tài

↓

Điểm tài vận tăng.

---

# 5. Hệ thống điểm

Module sử dụng điểm chuẩn hóa.

Ví dụ:

-100 → +100

Sau đó quy đổi về:

0 → 100

Ví dụ:

-40 → 30 điểm

0 → 50 điểm

+80 → 90 điểm

Điểm này sẽ được dùng thống nhất trong toàn bộ BTE.

---

# 6. Các nhóm Rule

Module được chia thành các nhóm:

## Nhóm A

Nguồn thu nhập

File:

02_rule_nguon_tai.csv

---

## Nhóm B

Tích lũy tài sản

File:

03_rule_tich_luy.csv

---

## Nhóm C

Phá tài

File:

04_rule_pha_tai.csv

---

## Nhóm D

Đầu tư

File:

05_rule_dau_tu.csv

---

## Nhóm E

Kinh doanh

File:

06_rule_kinh_doanh.csv

---

## Nhóm F

Liên kết nghề nghiệp

File:

07_rule_nghe_nghiep.csv

---

## Nhóm G

Điểm số

File:

08_diem_so.csv

---

## Nhóm H

Dữ liệu tổng hợp

File:

09_du_lieu.csv

---

# 7. Thứ tự xử lý

Engine thực hiện theo trình tự:

1. Đọc kết quả Thập Thần.
2. Đọc trạng thái Thân Vượng.
3. Đọc Dụng Thần.
4. Đọc Đại Vận.
5. Đọc Lưu Niên.
6. Đọc Thần Sát.
7. Áp dụng toàn bộ Rule.
8. Tính điểm.
9. Chuẩn hóa điểm.
10. Sinh kết luận.
11. Sinh cảnh báo.
12. Sinh giải thích (Explain AI).

---

# 8. Giải thích kết quả (Explain)

Mỗi kết luận phải truy vết được Rule đã kích hoạt.

Ví dụ:

Kết luận:

"Tài vận mạnh."

Giải thích:

* Chính Tài đắc lực (+20)
* Thực Thần sinh Tài (+15)
* Đại Vận trợ Dụng thần (+18)
* Không có Kiếp Tài phá (+10)

Tổng:

63 điểm.

Người dùng có thể xem đầy đủ lịch sử tính điểm.

---

# 9. Khả năng mở rộng

Module được thiết kế để:

* Bổ sung Rule mới mà không thay đổi cấu trúc.
* Hỗ trợ nhiều trường phái Bát Tự.
* Hỗ trợ AI tự động sinh luận giải.
* Hỗ trợ API cho Web, Mobile và Desktop.
* Hỗ trợ điều chỉnh trọng số theo từng phiên bản BTE.

---

# 10. Phiên bản

* Phiên bản dữ liệu: 1.0
* Chuẩn mã hóa: UTF-8
* Định dạng dữ liệu: CSV
* Khóa chính của mọi Rule: `rule_id`
* Chuẩn tương thích: BTE Core Ontology v1.x

