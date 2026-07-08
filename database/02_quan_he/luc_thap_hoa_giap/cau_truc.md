# Cấu trúc dữ liệu: luc_thap_hoa_giap

## Mục đích

Lưu trữ quan hệ Lục Thập Hoa Giáp (60 tổ hợp Can Chi).

Đây là bảng ontology trung gian kết nối:

- Thiên Can
- Địa Chi
- Nạp Âm
- Ngũ Hành
- Chu kỳ Hoa Giáp


## Schema CSV

| Field | Type | Mô tả |
|---|---|---|
| id | string | ID duy nhất |
| ma_quan_he | string | Mã quan hệ Hoa Giáp |
| ten | string | Tên tổ hợp Can Chi |
| thien_can | string | Thiên Can |
| dia_chi | string | Địa Chi |
| am_duong | string | Âm Dương |
| ngu_hanh_nap_am | string | Ngũ hành Nạp Âm |
| mo_ta | text | Mô tả tổng quát |


## Quy tắc ID

Ví dụ:

HG001

Trong đó:

HG = Hoa Giáp

001 = số thứ tự trong chu kỳ 60


## Quy tắc dữ liệu

- Bắt đầu từ Giáp Tý.
- Kết thúc tại Quý Hợi.
- Tổng cộng 60 tổ hợp.
- Thiên Can tuần hoàn 10.
- Địa Chi tuần hoàn 12.
- Không lặp trong một chu kỳ 60 năm.


## Quan hệ hệ thống

luc_thap_hoa_giap
        |
        ├── thien_can
        |
        ├── dia_chi
        |
        └── nap_am
