# Cấu trúc dữ liệu 01_nhat_chu


## Mục đích

Lưu trữ quy tắc xác định Nhật Chủ trong Bát Tự.

Nhật Chủ = Thiên Can của Trụ Ngày.

Đây là thực thể trung tâm để:

- xác định Thập Thần
- xác định Ngũ Hành bản mệnh
- xác định Thân Vượng / Thân Nhược
- xác định Dụng Thần
- luận vận


---

# Schema CSV


| Field | Type | Mô tả |
|---|---|---|
| id | string | mã bản ghi |
| ma_can | string | mã Thiên Can |
| ten_can | string | tên Thiên Can |
| am_duong | string | Âm Dương |
| ngu_hanh | string | Ngũ hành của Can |
| vai_tro | string | vai trò khi làm Nhật Chủ |
| mo_ta | text | mô tả |


---

# Quy tắc chính


Nhật Chủ lấy:

Can ngày sinh


Ví dụ:

Ngày sinh:
Canh Ngọ


Nhật Chủ:

Canh Kim


Không lấy:

- Can năm
- Can tháng
- Can giờ


---

# Quan hệ dữ liệu


01_nhat_chu

        |

        ↓

01_du_lieu_goc/thien_can


        |

        ↓

02_quan_he/thap_than


        |

        ↓

05_phan_tich
