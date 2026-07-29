# Special Case Rules

## Mục đích

Module **Special Case Rules** định nghĩa các tình huống đặc biệt (Special Cases) xảy ra trong quá trình phân tích Bát Tự mà hệ thống không thể xử lý theo luồng thông thường.

Các quy tắc trong module này giúp:

- Phát hiện dữ liệu bất thường.
- Xử lý các trường hợp ngoại lệ.
- Ưu tiên các quy tắc đặc biệt.
- Kích hoạt cơ chế Fallback.
- Chuyển sang Manual Review khi cần.
- Đảm bảo tính ổn định của toàn bộ BTE Platform.

---

# Vai trò trong hệ thống

```text
Input
   │
   ▼
Validation
   │
   ▼
Pattern Engine
   │
   ▼
Score Engine
   │
   ▼
Special Case Rules
   │
   ├── Normal
   │      │
   │      ▼
   │  Interpretation Engine
   │
   └── Special Case
          │
          ├── Override
          ├── Fallback
          ├── Manual Review
          └── Stop Processing
```

Module này được gọi sau khi các Engine chính hoàn thành việc tính toán và trước khi sinh kết quả luận giải.

---

# Cấu trúc thư mục

```text
05_special_case_rules/
│
├── special_case_rules.json
├── special_case_score_rules.json
├── special_case_priority.json
├── special_case_labels.json
├── special_case_examples.json
└── README.md
```

---

# Các file

## 1. special_case_rules.json

Định nghĩa toàn bộ Special Case được hệ thống hỗ trợ.

Ví dụ:

- thieu_du_lieu_bat_buoc
- xung_dot_dieu_kien
- khong_xac_dinh_duoc_cach_cuc
- do_tin_cay_thap
- can_kiem_tra_thu_cong

Đây là file trung tâm của module.

---

## 2. special_case_score_rules.json

Định nghĩa cách cộng hoặc trừ điểm khi xuất hiện Special Case.

Ví dụ:

- cộng điểm cảnh báo
- giảm độ tin cậy
- vô hiệu hóa điểm số
- kích hoạt Override

---

## 3. special_case_priority.json

Quy định mức ưu tiên giữa các Special Case.

Ví dụ:

```text
Manual Review
      ↑
Data Missing
      ↑
Conflict
      ↑
Fallback
```

Giúp Priority Engine xác định Special Case nào được xử lý trước.

---

## 4. special_case_labels.json

Chuẩn hóa tên hiển thị.

Ví dụ:

```text
thieu_du_lieu_bat_buoc
↓

Thiếu dữ liệu bắt buộc
```

Giúp giao diện và báo cáo sử dụng ngôn ngữ thống nhất.

---

## 5. special_case_examples.json

Golden Dataset của module.

Bao gồm 50 ví dụ kiểm thử:

- Part 1A
  - Thiếu dữ liệu

- Part 1B
  - Dữ liệu không hợp lệ

- Part 1C
  - Xung đột nghiệp vụ

- Part 1D
  - Không xác định được Cách cục

- Part 1E
  - Fallback / Manual Review / Exception

File này phục vụ:

- Unit Test
- Integration Test
- Regression Test
- Golden Dataset
- AI Evaluation

---

# Luồng xử lý

```text
Input

↓

Validation

↓

Rule Engine

↓

Pattern Engine

↓

Score Engine

↓

Special Case Detection

↓

Priority Resolution

↓

Decision

↓

Interpretation Engine
```

---

# Quy tắc thiết kế

- Mỗi Special Case có ID duy nhất.
- Mỗi Rule chỉ mô tả một tình huống.
- Priority được quản lý riêng.
- Score được quản lý riêng.
- Label được quản lý riêng.
- Example được quản lý riêng.
- Không trùng lặp Rule.
- Không chứa logic xử lý trong dữ liệu.
- Dữ liệu chỉ mô tả quy tắc.

---

# Quan hệ với các Module khác

Special Case Rules có thể được kích hoạt bởi:

- Validation Engine
- Calendar Engine
- Bazi Engine
- Pattern Engine
- Score Engine
- Interpretation Engine

Module này không thay thế các Engine trên mà đóng vai trò xử lý ngoại lệ và điều phối các tình huống đặc biệt.

---

# Phiên bản

**Version:** V1.0

## Trạng thái

- ✅ Rule Database hoàn chỉnh
- ✅ Priority Database hoàn chỉnh
- ✅ Score Rule Database hoàn chỉnh
- ✅ Label Database hoàn chỉnh
- ✅ Example Database hoàn chỉnh

Module **Special Case Rules V1.0** đã sẵn sàng tích hợp vào Rule Engine của BTE Platform.