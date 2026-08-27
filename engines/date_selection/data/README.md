# Date Selection Cung Phi datasets

These tables are **not** Cân Xương weight data.

## Person Cung Phi

Runtime person Cung uses canonical Feng Shui Engine:

`birth year + gender → Cung Phi → element → Đông/Tây Tứ Trạch`

`hoa_giap_cung_phi.csv` remains a person-reference helper (Cung Nam / Cung Nữ). It is **not** the date/hour rule.

## Date / hour Hạ Nguyên Cung

Canonical file:

`engines/date_selection/data/ha_nguyen_cung.csv`

| Field | Meaning |
|---|---|
| `ganzhi` | 60 Hoa Giáp label |
| `ha_nguyen_cung` | Intrinsic Hạ Nguyên Cung for that Ganzhi |
| `cung_element` | Ngũ hành of the Cung |
| `trach_group` | `dong` / `tay` |

This mapping is the Product Owner–approved **Cung → Nam** column from workbook `can_xuong_PRO.xlsx`, sheet `Nam_60_Hoa_Giap`, normalized as intrinsic date/hour Cung.

It is **not** viewer gender. The same Ganzhi always yields the same date/hour Cung.

The Excel workbook is reference only. Runtime reads this CSV. No Excel dependency.

Hạ Nguyên cycle used to normalize the 60 rows: Giáp Tý 1984 through Quý Hợi 2043. Mandatory checks:

- Quý Dậu → Đoài → Kim → Tây
- Tân Dậu → Tốn → Mộc → Đông
