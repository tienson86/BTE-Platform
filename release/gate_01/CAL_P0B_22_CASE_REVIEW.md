# CAL-P0B — 22 Golden cases requiring Product Owner month review

| Field | Value |
|-------|-------|
| **Standard** | `BTE-MONTH-PILLAR-LUNAR-V1.0` |
| **Date** | 2026-08-20 |
| **Source list** | CAL-P0 `MONTH_PILLAR_REVIEW_REQUIRED` (jieqi ≠ folk lunar-month) |
| **Golden expected files** | **not bulk-updated** |

Old month = 12 Tiết + Ngũ Hổ Độn (`SolarTermEngine.get_bazi_month`).  
New month = lunar month number (1=Dần … 12=Sửu) + same Ngũ Hổ Độn.  
Solar/lunar datetimes are from `tests/golden_dataset/inputs/<id>.json`. Gender from the input file when present.

Product Owner should check each **new** month against *Can Chi Thông Luận*.

| Case ID | Solar datetime | Lunar date | Old 12-Tiết month | New lunar-month month | New full Four Pillars |
|---------|----------------|------------|-------------------|------------------------|------------------------|
| case_0003 | 1960-03-03T10:00:00+07:00 | 06/02/1960 | Mậu Dần | Kỷ Mão | Canh Tý / Kỷ Mão / Canh Dần / Tân Tỵ |
| case_0010 | 1960-12-09T19:00:00+07:00 | 21/10/1960 | Mậu Tý | Đinh Hợi | Canh Tý / Đinh Hợi / Tân Mùi / Mậu Tuất |
| case_0013 | 1961-03-08T20:00:00+07:00 | 22/01/1961 | Tân Mão | Canh Dần | Tân Sửu / Canh Dần / Canh Tý / Bính Tuất |
| case_0026 | 1962-07-02T10:00:00+07:00 | 01/06/1962 | Bính Ngọ | Đinh Mùi | Nhâm Dần / Đinh Mùi / Tân Sửu / Quý Tỵ |
| case_0028 | 1962-10-06T14:00:00+07:00 | 08/09/1962 | Kỷ Dậu | Canh Tuất | Nhâm Dần / Canh Tuất / Đinh Sửu / Đinh Mùi |
| case_0031 | 1963-01-03T15:00:00+07:00 | 08/12/1962 | Nhâm Tý | Quý Sửu | Nhâm Dần / Quý Sửu / Bính Ngọ / Bính Thân |
| case_0036 | 1963-07-18T21:00:00+07:00 | 28/05/1963 | Kỷ Mùi | Mậu Ngọ | Quý Mão / Mậu Ngọ / Nhâm Tuất / Tân Hợi |
| case_0038 | 1963-09-08T21:00:00+07:00 | 21/07/1963 | Tân Dậu | Canh Thân | Quý Mão / Canh Thân / Giáp Dần / Ất Hợi |
| case_0040 | 1963-12-14T01:00:00+07:00 | 29/10/1963 | Giáp Tý | Quý Hợi | Quý Mão / Quý Hợi / Tân Mão / Kỷ Sửu |
| case_0042 | 1964-02-04T01:00:00+07:00 | 21/12/1963 | Bính Dần | Đinh Sửu | Giáp Thìn / Đinh Sửu / Quý Mùi / Quý Sửu |
| case_0044 | 1964-05-10T05:00:00+07:00 | 29/03/1964 | Kỷ Tỵ | Mậu Thìn | Giáp Thìn / Mậu Thìn / Kỷ Mùi / Đinh Mão |
| case_0059 | 1965-11-04T20:00:00+07:00 | 12/10/1965 | Bính Tuất | Đinh Hợi | Ất Tỵ / Đinh Hợi / Nhâm Tuất / Canh Tuất |
| case_0063 | 1966-04-02T00:00:00+07:00 | 12/03/1966 | Tân Mão | Nhâm Thìn | Bính Ngọ / Nhâm Thìn / Tân Mão / Mậu Tý |
| case_0065 | 1966-07-07T04:00:00+07:00 | 19/05/1966 | Ất Mùi | Giáp Ngọ | Bính Ngọ / Giáp Ngọ / Đinh Mão / Nhâm Dần |
| case_0066 | 1966-07-11T02:00:00+07:00 | 23/05/1966 | Ất Mùi | Giáp Ngọ | Bính Ngọ / Giáp Ngọ / Tân Mùi / Kỷ Sửu |
| case_0076 | 1967-08-06T15:00:00+07:00 | 01/07/1967 | Đinh Mùi | Mậu Thân | Đinh Mùi / Mậu Thân / Nhâm Dần / Mậu Thân |
| case_0080 | 1968-01-01T19:00:00+07:00 | 02/12/1967 | Nhâm Tý | Quý Sửu | Đinh Mùi / Quý Sửu / Canh Ngọ / Bính Tuất |
| case_0082 | 1968-03-04T20:00:00+07:00 | 06/02/1968 | Giáp Dần | Ất Mão | Mậu Thân / Ất Mão / Quý Dậu / Nhâm Tuất |
| case_0088 | 1968-11-15T05:00:00+07:00 | 25/09/1968 | Quý Hợi | Nhâm Tuất | Mậu Thân / Nhâm Tuất / Kỷ Sửu / Đinh Mão |
| case_0089 | 1968-11-08T02:00:00+07:00 | 18/09/1968 | Quý Hợi | Nhâm Tuất | Mậu Thân / Nhâm Tuất / Nhâm Ngọ / Tân Sửu |
| case_0091 | 1969-02-12T06:00:00+07:00 | 26/12/1968 | Bính Dần | Đinh Sửu | Kỷ Dậu / Đinh Sửu / Mậu Ngọ / Ất Mão |
| case_0094 | 1969-05-11T08:00:00+07:00 | 25/03/1969 | Kỷ Tỵ | Mậu Thìn | Kỷ Dậu / Mậu Thìn / Bính Tuất / Nhâm Thìn |

Also related (not in the 22 Golden files):

| Case | Solar | Lunar | Old | New | Full |
|------|-------|-------|-----|-----|------|
| Đoàn Quang Hưng | 1981-08-29 04:30 | 01/08/1981 | Bính Thân | Đinh Dậu | Tân Dậu / Đinh Dậu / Kỷ Mão / Bính Dần |
| Pilot CASE-0006 | 1988-06-07 20:45 | 23/04/1988 | Mậu Ngọ | Đinh Tỵ | (live lunar-month; was expert Đinh Tỵ) |

Golden `actual/` and `expected/` JSON were **not** rewritten.
