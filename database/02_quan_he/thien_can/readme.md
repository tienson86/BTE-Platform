# BTE Platform - Quan hệ Thiên Can

## 1. Giới thiệu

Thư mục `thien_can` lưu trữ toàn bộ dữ liệu chuẩn hóa về các quan hệ giữa Thiên Can trong hệ thống BTE (BaTu Engine).

Đây là lớp dữ liệu nền (Knowledge Layer) để Rule Engine, AI Engine và các ứng dụng thương mại khai thác.

Thư mục này không chứa thuật toán suy luận mà chỉ mô tả các quan hệ đã được chuẩn hóa.

---

## 2. Phạm vi dữ liệu

Bao gồm các nhóm quan hệ sau:

- Thiên Can Hợp
- Thiên Can Xung
- Thiên Can Hóa

Trong tương lai có thể mở rộng thêm nếu cần nhưng vẫn đảm bảo tương thích ngược.

---

## 3. Mục tiêu

Chuẩn hóa dữ liệu Thiên Can để phục vụ:

- Website Bát Tự
- REST API
- AI Agent
- Rule Engine
- Knowledge Graph
- Ontology
- Phân tích học thuật

---

## 4. Nguyên tắc thiết kế

Mỗi bản ghi chỉ mô tả một quan hệ.

Không chứa:

- if/else
- thuật toán
- công thức suy luận

Mọi logic xử lý sẽ nằm trong Rule Engine.

---

## 5. Chuẩn dữ liệu

Dữ liệu được chuẩn hóa theo:

- UTF-8
- Unicode NFC
- Không viết tắt
- Không trùng lặp
- Có ID duy nhất

---

## 6. Cấu trúc thư mục

thien_can/

├── README.md
├── cau_truc.md
├── du_lieu.csv
└── ghi_chu.md

---

## 7. Quan hệ được hỗ trợ

### Thiên Can Hợp

Lưu quan hệ hợp giữa các Thiên Can.

Ví dụ:

Giáp ↔ Kỷ

---

### Thiên Can Xung

Lưu quan hệ xung.

Ví dụ:

(BTE sẽ định nghĩa theo học phái được lựa chọn.)

---

### Thiên Can Hóa

Lưu kết quả hóa khí khi đủ điều kiện.

Ví dụ:

Giáp + Kỷ → Thổ

---

## 8. Quy tắc mở rộng

Không sửa dữ liệu cũ.

Chỉ bổ sung bản ghi mới khi:

- Có thêm học phái
- Có thêm quy tắc
- Có phiên bản dữ liệu mới

---

## 9. Phiên bản

Version: 1.0

Thuộc dự án:

BTE Platform (BaTu Engine)
