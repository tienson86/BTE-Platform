# 03_tang_can/ghi_chu.md

# Ghi chú học thuật - Module Tàng Can

Phiên bản: 1.0.0

---

# 1. Mục đích

Module `03_tang_can` chuẩn hóa dữ liệu Tàng Can của 12 Địa Chi theo hướng Ontology.

Đây là dữ liệu nền tảng để phục vụ:

- Thập Thần
- Thông Căn
- Thân Vượng / Thân Nhược
- Dụng Thần
- Hỷ Thần
- Kỵ Thần
- Đại Vận
- Lưu Niên
- AI Analysis
- Rule Engine

Module này không thực hiện suy luận mà chỉ lưu trữ dữ liệu gốc (Fact).

---

# 2. Nguyên tắc xây dựng

Module tuân thủ các nguyên tắc của BTE Data Standard:

- Single Source of Truth
- Atomic Data
- Ontology First
- Rule Separation
- Knowledge Graph Ready

Mỗi bản ghi chỉ biểu diễn duy nhất một quan hệ giữa một Địa Chi và một Thiên Can.

Không gộp nhiều Thiên Can trong cùng một ô dữ liệu.

---

# 3. Phạm vi dữ liệu

Phiên bản hiện tại lưu:

- 12 Địa Chi
- 28 quan hệ Tàng Can

Không lưu:

- Trọng số Tàng Can
- Tỷ lệ phần trăm
- Mức vượng suy
- Điều kiện phát lực
- Quy tắc Thông Căn
- Quy tắc Thấu Can

Các nội dung trên sẽ được xây dựng ở các module Rule trong tương lai.

---

# 4. Loại Tàng Can

BTE sử dụng ba loại chuẩn:

- Chính khí
- Trung khí
- Dư khí

Đây là cách phân loại phổ biến trong Tử Bình truyền thống.

Không sử dụng các thuật ngữ khác để tránh phát sinh nhiều hệ quy chiếu.

---

# 5. Thứ tự Tàng Can

Trường `thu_tu` chỉ phản ánh vị trí truyền thống của Tàng Can trong từng Địa Chi.

Không mang ý nghĩa:

- Trọng số
- Mức mạnh yếu
- Xác suất
- Điểm số

Mọi phép tính sẽ do Rule Engine xử lý.

---

# 6. Không lưu trọng số

BTE không quy định mặc định các tỷ lệ như:

- 60 - 30 - 10
- 70 - 20 - 10
- 80 - 10 - 10

Lý do:

Các trường phái có cách xác định khác nhau.

Để đảm bảo tính trung lập học thuật, module chỉ lưu dữ liệu gốc.

Nếu cần áp dụng từng học phái sẽ xây dựng Rule riêng.

---

# 7. Quan hệ với các module khác

Module này là đầu vào của:

- 04_thap_than
- 05_nap_am (tham chiếu khi cần)
- 07_truong_sinh
- Rule Engine
- AI Engine

Đây là một trong những module nền tảng quan trọng nhất của BTE.

---

# 8. Khả năng mở rộng

Trong các phiên bản tiếp theo có thể bổ sung:

- tang_can_weight.csv
- thong_can_rule.csv
- tang_can_strength.csv
- hidden_stem_alias.csv

Các dữ liệu mở rộng này phải tách khỏi `du_lieu.csv`.

---

# 9. Quy tắc bảo trì

Không thay đổi:

- ID
- Địa Chi
- Thiên Can
- Loại Tàng Can

Nếu cần cập nhật học thuật:

- Tăng Version
- Ghi vào CHANGELOG
- Không sửa trực tiếp dữ liệu đã phát hành.

---

# 10. Tài liệu tham khảo

Module được xây dựng dựa trên hệ thống Tử Bình truyền thống và được chuẩn hóa theo mô hình Ontology của BTE.

Trong trường hợp có sự khác biệt giữa các học phái, BTE ưu tiên:

1. Dữ liệu phổ biến và được đa số tài liệu truyền thống công nhận.
2. Dữ liệu có thể chuẩn hóa và biểu diễn dưới dạng Ontology.
3. Các khác biệt giữa học phái sẽ được triển khai ở tầng Rule Engine thay vì thay đổi dữ liệu gốc.

---

# Lịch sử phiên bản

## Version 1.0.0

- Khởi tạo module `03_tang_can`.
- Chuẩn hóa dữ liệu thành 28 bản ghi.
- Áp dụng mô hình "mỗi bản ghi = một quan hệ Địa Chi → Thiên Can".
- Tách biệt hoàn toàn dữ liệu và quy tắc suy luận.
