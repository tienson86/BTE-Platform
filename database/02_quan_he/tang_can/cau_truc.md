# 03_tang_can/cau_truc.md

# Cấu trúc dữ liệu Tàng Can (03_tang_can)

## Phiên bản

- Module: 03_tang_can
- File dữ liệu: du_lieu.csv
- Phiên bản: 1.0.0
- Trạng thái: Stable

---

# 1. Mục đích

Module này lưu trữ dữ liệu chuẩn về quan hệ giữa **Địa Chi** và **Thiên Can Tàng** (Tàng Can).

Đây là dữ liệu nền tảng phục vụ:

- Thập Thần
- Thông Căn
- Thân Vượng / Thân Nhược
- Dụng Thần
- Hỷ Thần
- Kỵ Thần
- Đại Vận
- Lưu Niên
- Rule Engine
- AI Analysis

Module chỉ lưu **Fact (dữ liệu gốc)**, không lưu các quy tắc suy luận.

---

# 2. Cấu trúc file

Tên file:

```
du_lieu.csv
```

Encoding:

```
UTF-8
```

Delimiter:

```
,
```

Mỗi dòng biểu diễn **một quan hệ giữa một Địa Chi và một Thiên Can**.

---

# 3. Schema

| STT | Tên cột | Kiểu dữ liệu | Bắt buộc | Mô tả |
|-----|----------|--------------|----------|-------|
| 1 | id | String | ✔ | Mã định danh duy nhất |
| 2 | dia_chi | Enum | ✔ | Địa Chi chứa Tàng Can |
| 3 | thien_can | Enum | ✔ | Thiên Can được tàng |
| 4 | loai_tang | Enum | ✔ | Loại Tàng Can |
| 5 | thu_tu | Integer | ✔ | Thứ tự xuất hiện |
| 6 | mo_ta | String | ✘ | Ghi chú |

---

# 4. Mô tả từng cột

## id

Khóa chính của bản ghi.

Ví dụ:

```
TGC001
```

Không được thay đổi sau khi phát hành.

---

## dia_chi

Địa Chi chứa Thiên Can.

Giá trị hợp lệ:

```
Tý
Sửu
Dần
Mão
Thìn
Tỵ
Ngọ
Mùi
Thân
Dậu
Tuất
Hợi
```

Khóa ngoại:

```
01_core_data/dia_chi
```

---

## thien_can

Thiên Can được tàng trong Địa Chi.

Giá trị hợp lệ:

```
Giáp
Ất
Bính
Đinh
Mậu
Kỷ
Canh
Tân
Nhâm
Quý
```

Khóa ngoại:

```
01_core_data/thien_can
```

---

## loai_tang

Phân loại vị trí của Tàng Can trong Địa Chi.

Giá trị hợp lệ:

```
Chính khí
Trung khí
Dư khí
```

Ý nghĩa:

- Chính khí: Can chủ đạo của Địa Chi.
- Trung khí: Can phụ.
- Dư khí: Can còn lại.

---

## thu_tu

Thứ tự xuất hiện của Tàng Can trong Địa Chi.

Giá trị:

```
1
2
3
```

Ý nghĩa:

- 1 = Chính khí
- 2 = Trung khí hoặc Dư khí
- 3 = Dư khí

Không dùng để tính trọng số.

---

## mo_ta

Thông tin bổ sung.

Không được Rule Engine sử dụng.

---

# 5. Quy tắc dữ liệu

- Một bản ghi chỉ chứa một Thiên Can.
- Không gộp nhiều Thiên Can trong một ô.
- Không lưu trọng số.
- Không lưu tỷ lệ phần trăm.
- Không lưu điều kiện suy luận.

---

# 6. Quan hệ với các module khác

Đầu vào:

```
01_core_data/thien_can
01_core_data/dia_chi
```

Đầu ra:

```
04_thap_than
05_nap_am
07_truong_sinh
Rule Engine
AI Engine
```

---

# 7. Quy tắc kiểm tra

- ID phải duy nhất.
- Địa Chi phải tồn tại trong module Địa Chi.
- Thiên Can phải tồn tại trong module Thiên Can.
- loai_tang chỉ được nhận một trong ba giá trị chuẩn.
- thu_tu phải là số nguyên dương.
- Không được trùng cặp (dia_chi + thien_can).

---

# 8. Nguyên tắc thiết kế

Module tuân thủ:

- Single Source of Truth
- Atomic Data
- Ontology First
- Rule Separation
- Knowledge Graph Ready

---

# 9. Lịch sử phiên bản

## Version 1.0.0

- Khởi tạo module Tàng Can.
- Chuẩn hóa dữ liệu thành 28 bản ghi.
- Mỗi bản ghi biểu diễn một quan hệ Địa Chi → Thiên Can.
