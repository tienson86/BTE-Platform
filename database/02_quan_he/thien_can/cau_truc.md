# BTE Platform - Cấu trúc dữ liệu Quan hệ Thiên Can

## 1. Mục đích

Tài liệu này định nghĩa cấu trúc chuẩn (Schema) của file `du_lieu.csv`
thuộc thư mục:

database/
└── 02_quan_he/
    └── thien_can/

Schema này được sử dụng thống nhất trong toàn bộ BTE Platform.

---

## 2. Quy tắc chung

- Mỗi dòng biểu diễn một quan hệ Thiên Can.
- Không có dòng trùng lặp.
- Không chứa thuật toán.
- Không chứa dữ liệu suy luận.
- Chỉ lưu dữ liệu chuẩn hóa.

---

## 3. Cấu trúc bảng

| STT | Tên cột | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----|----------|--------------|----------|-------|
| 1 | id | String | Có | Mã định danh duy nhất |
| 2 | loai_quan_he | Enum | Có | Loại quan hệ |
| 3 | can_1 | Enum | Có | Thiên Can thứ nhất |
| 4 | can_2 | Enum | Có | Thiên Can thứ hai |
| 5 | ket_qua | String | Không | Kết quả của quan hệ (nếu có) |
| 6 | dieu_kien | String | Không | Điều kiện phát sinh quan hệ |
| 7 | ghi_chu | String | Không | Ghi chú bổ sung |

---

## 4. Mô tả từng trường

### id

Kiểu:

String

Ví dụ:

CAN_HOP_001

Quy tắc:

- Duy nhất.
- Không được thay đổi sau khi phát hành.

---

### loai_quan_he

Kiểu:

Enum

Các giá trị hợp lệ:

- hop
- xung
- hoa

Ví dụ:

hop

---

### can_1

Kiểu:

Enum

Giá trị:

- Giáp
- Ất
- Bính
- Đinh
- Mậu
- Kỷ
- Canh
- Tân
- Nhâm
- Quý

---

### can_2

Kiểu:

Enum

Giống can_1.

---

### ket_qua

Kiểu:

String

Áp dụng chủ yếu cho quan hệ Hóa.

Ví dụ:

- Thổ
- Kim
- Thủy
- Mộc
- Hỏa

Nếu không có kết quả thì để trống.

---

### dieu_kien

Kiểu:

String

Ví dụ:

- Đủ điều kiện hóa
- Có Hỏa trợ
- Được mùa
- Không

Phiên bản đầu tiên có thể để:

Không

Sau này Rule Engine sẽ sử dụng trường này.

---

### ghi_chu

Kiểu:

String

Ví dụ:

- Chính hợp
- Hợp hóa
- Theo Tử Bình
- Theo Tam Mệnh Thông Hội

---

## 5. Quan hệ đối xứng

Các quan hệ Hợp và Xung là quan hệ đối xứng.

Ví dụ:

Giáp ↔ Kỷ

Engine có thể xử lý theo một trong hai phương án:

- Chỉ lưu một chiều và suy luận chiều ngược.
- Lưu cả hai chiều.

Việc lựa chọn sẽ được quy định trong `du_lieu.csv`.

---

## 6. Chuẩn dữ liệu

- UTF-8
- Unicode NFC
- Không khoảng trắng thừa
- Không viết tắt
- Không dùng ký hiệu đặc biệt ngoài quy định

---

## 7. Ví dụ

| id | loai_quan_he | can_1 | can_2 | ket_qua | dieu_kien | ghi_chu |
|-----|--------------|-------|-------|----------|------------|----------|
| CAN_HOP_001 | hop | Giáp | Kỷ | Thổ | Đủ điều kiện hóa | Chính hợp |

---

## 8. Khả năng mở rộng

Schema này được thiết kế để:

- Bổ sung học phái mới.
- Bổ sung quy tắc mới.
- Xây dựng Rule Engine.
- Xây dựng Knowledge Graph.
- Tích hợp AI.
- Phát triển API thương mại.

Không thay đổi tên cột trong các phiên bản sau để đảm bảo tương thích.
