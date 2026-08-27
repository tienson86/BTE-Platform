# Date Selection Cung Phi dataset

This table is **not** Cân Xương weight data.

## Person columns

- 60 Hoa Giáp labels and Nạp Âm ngũ hành: `engines/calendar_engine/data/01_nap_am.csv`
- `cung_nam` / `cung_nu`: person birth Cung for the 1924–1983 Giáp Tý cycle (Feng Shui year-digit method). Used only as a Ganzhi+gender person lookup helper.
- Runtime **person** Cung Phi uses canonical Feng Shui Engine (`year` + `gender`), not these columns as a date rule.

## Date / hour column

- `cung_ngay`: intrinsic Date Selection Cung for a day or hour Ganzhi (Hạ Nguyên / 60 Hoa Giáp).
- This column is **empty**. The repository has no canonical date/hour Hạ Nguyên mapping (no Tam Nguyên Cửu Vận date table; `can_xuong_PRO.xlsx` / `Nam_60_Hoa_Giap` is not checked in).
- Do **not** fill `cung_ngay` from Cung Nam/Nữ, stem polarity, viewer gender, or Feng Shui Engine gender output.
