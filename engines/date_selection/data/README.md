# Date Selection Cung Phi dataset

This table is **not** Cân Xương weight data.

Source of truth:

- 60 Hoa Giáp labels and Nạp Âm ngũ hành: `engines/calendar_engine/data/01_nap_am.csv`
- Cung Nam / Cung Nữ: canonical Feng Shui Engine (`calculate_gua_number`) applied to the 1924–1983 Giáp Tý cycle (one complete 60-year set, all pre-2000 so the year-digit method is internally consistent)

Runtime Date Selection looks up Cung Phi by Ganzhi + gender from this CSV. It does not import Excel.
