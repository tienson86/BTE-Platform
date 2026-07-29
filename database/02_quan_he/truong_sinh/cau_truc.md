# Cấu trúc dữ liệu Trường Sinh

## Mục đích

Lưu trữ quan hệ giữa Thiên Can và 12 trạng thái Trường Sinh (Thập Nhị Trường Sinh).

Đây là một trong những bảng dữ liệu nền của BTE Core Ontology, phục vụ cho việc:

- Phân tích Bát Tự (Tứ Trụ).
- Xác định vượng, suy của Nhật Chủ.
- Phân tích khí vận.
- Xác định sức mạnh Ngũ Hành.
- Hỗ trợ luận Đại Vận, Lưu Niên và các thuật toán suy luận.

---

## Mô hình dữ liệu

Dữ liệu được chuẩn hóa thành hai bảng:

- `trang_thai.csv`: Danh mục 12 trạng thái Trường Sinh.
- `du_lieu.csv`: Quan hệ giữa Thiên Can, Địa Chi và trạng thái.

Mô hình này giúp tránh lặp dữ liệu và dễ dàng mở rộng.

---

## Cấu trúc file `trang_thai.csv`

| Trường | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|------|
| id | string | Có | Mã trạng thái (TS01–TS12) |
| thu_tu | integer | Có | Thứ tự trong chu kỳ |
| ten | string | Có | Tên trạng thái |
| ten_han | string | Có | Hán tự |
| ten_tieng_anh | string | Có | Tên tiếng Anh |
| alias | string | Có | Tên kỹ thuật |
| nhom | string | Có | Nhóm trạng thái |
| giai_doan | string | Có | Giai đoạn phát triển |
| mo_ta | string | Không | Giải thích ý nghĩa |

---

## Cấu trúc file `du_lieu.csv`

| Trường | Kiểu | Bắt buộc | Mô tả |
|---------|------|----------|------|
| id | string | Có | Mã bản ghi (TS0001–TS0120) |
| thien_can | string | Có | Thiên Can |
| dia_chi | string | Có | Địa Chi |
| trang_thai_id | string | Có | Khóa ngoại đến `trang_thai.csv` |

---

## Khóa chính

- `trang_thai.csv` → id
- `du_lieu.csv` → id

---

## Khóa ngoại

| Bảng | Trường | Tham chiếu |
|------|---------|------------|
| du_lieu.csv | trang_thai_id | trang_thai.csv.id |

---

## Quy mô dữ liệu

| File | Số bản ghi |
|------|-----------:|
| trang_thai.csv | 12 |
| du_lieu.csv | 120 |

---

## Quan hệ

Bảng này sẽ được sử dụng bởi:

- Bát Tự
- Đại Vận
- Lưu Niên
- Dụng Thần
- Hỷ Thần
- Kỵ Thần
- BTE Engine

---

## Header

### trang_thai.csv

```csv
id,thu_tu,ten,ten_han,ten_tieng_anh,alias,nhom,giai_doan,mo_ta
```

### du_lieu.csv

```csv
id,thien_can,dia_chi,trang_thai_id
```
