# G1-10B — Actual Year/Month Can Chi from Tam Nguyên dataset

## 1. STATUS

**DONE.**

Year and Month heavenly stem / earthly branch are now **looked up** from `engines/calendar_engine/data/tam_nguyen_60_hoa_giap.csv`. They are no longer produced by `GanzhiAlgorithm.year`.

Live `/api/v1/analyze` for 24/09/1966 04:15 male matches the Trung Nguyên dataset row. Header identity stems equal BaZi stems. `calendar_rule_version = G1-10B`. Pre-G1-10B ResultStore payloads with `ganzhi_routing` and no version are dropped.

## 2. Root cause

G1-10A only routed **Cung** and `source_nguyen`. Actual stems still came from:

- Year: `GanzhiAlgorithm.year` (formula `(year+6)%10`, `(year+8)%12`)
- Month: `month_pillar` → that same year stem + 12 Tiết Ngũ Hổ Độn

Attaching `source_nguyen=Trung Nguyên` onto Bính Ngọ / Đinh Dậu did not change the Can Chi producer.

## 3. Exact file/function that produced old Bính Ngọ

`engines/bazi_engine/engine.py` → `BaziEngine.build`

```
year_gz = GanzhiAlgorithm.year(bazi_year)
year_pillar = Pillar(stem=year_gz["can"], branch=year_gz["chi"])
```

`bazi_year` from `_bazi_year` (Lập Xuân). For 24/09/1966 that year is 1966 → formula Bính Ngọ.

Calendar lunar label used the same algorithm on the lunar year in `CalendarEngine.build`.

## 4. Exact file/function that produced old Đinh Dậu

`engines/calendar_engine/month_ganzhi.py` → `month_pillar`

```
year_stem = GanzhiAlgorithm.year(bazi_year_number(...))["can"]
stem = month_stem_for(year_stem, info.month_index)
```

Sept 1966 nguyệt lệnh = Dậu; year stem Bính → Ngũ Hổ Độn **Đinh Dậu**.

`BaziEngine.build` called `canonical_month_pillar` (same function).

## 5. Canonical Tam Nguyên dataset used

New file (180 rows, three 60 Hoa Giáp blocks):

`engines/calendar_engine/data/tam_nguyen_60_hoa_giap.csv`

| Column | Meaning |
| --- | --- |
| `tam_nguyen` | Thượng / Trung / Hạ Nguyên |
| `thu_tu` | 0–59 inside the block (Giáp Tý = 0) |
| `thien_can` / `dia_chi` / `hoa_giap` | actual Can Chi |
| `nap_am` | from `database/02_quan_he/luc_thap_hoa_giap/du_lieu.csv` |
| `nam_mau` | sample civil year (1864 / 1924 / 1984 bases) |

Trung Nguyên 1966 row:

`Trung Nguyên,42,Bính,Ngọ,Bính Ngọ,Thiên Hà Thủy,1966`

Loader: `engines/calendar_engine/tam_nguyen_dataset.py`

## 6. Previous Year actual value

Bính Ngọ — from `GanzhiAlgorithm.year`.

## 7. New Year actual value

**Bính Ngọ** — from Trung Nguyên dataset row `nam_mau=1966`.

The glyph did not change because the canonical table lists 1966 as Bính Ngọ. The **producer** changed. Regression `test_year_pillar_does_not_use_legacy_ganzhi_algorithm` monkeypatches `GanzhiAlgorithm.year` → Giáp Tý; Year pillar stays Bính Ngọ.

## 8. Previous Month actual value

Đinh Dậu — from `month_pillar` + `GanzhiAlgorithm.year` stem.

## 9. New Month actual value

**Đinh Dậu** — Ngũ Hổ Độn using **dataset Year stem Bính** + 12-Tiết branch Dậu. Nạp âm **Sơn Hạ Hỏa** from the same 60 Hoa Giáp nap_am table.

## 10. Day value and source

Bính Tuất — noon JDN + `GanzhiAlgorithm.day`. `source_nguyen` = Hạ Nguyên.

## 11. Hour value and source

Canh Dần — Ngũ Thử Độn from day stem. `source_nguyen` = Hạ Nguyên.

## 12. Derived Nạp Âm rebuild

`build_bazi_view` looks up nap_am by `(stem, branch)` after the new pillars exist.

- Year: Thiên Hà Thủy (dataset Bính Ngọ)
- Month: Sơn Hạ Hỏa (Đinh Dậu)

No old nap_am is copied onto a new Can Chi.

## 13. Derived Tàng Can rebuild

`BaziEngine.build` rebuilds `hidden_stems` from the new branches (`HIDDEN[branch]`), Ten Gods from the new stems vs day master, and ShenSha from the new stem/branch lists. Trường Sinh in `PillarView` uses the new day-master + branch lookup.

## 14. Homepage Kết quả ngày verification

`DateSelectionService.inspect_day` uses `calendar.year_can_chi` / `month_can_chi` from CalendarEngine (dataset), not `GanzhiAlgorithm.year`.

Live 1966: homepage year = Bính Ngọ, month = Đinh Dậu (same as API).

## 15. /result API verification

`POST /api/v1/analyze` 24/09/1966 04:15 male (TestClient, 200):

```
calendar.calendar_rule_version = G1-10B
calendar.tam_nguyen = Trung Nguyên
bazi.year  = Bính Ngọ  source_nguyen=Trung Nguyên
bazi.month = Đinh Dậu  source_nguyen=Trung Nguyên
bazi.day   = Bính Tuất source_nguyen=Hạ Nguyên
bazi.hour  = Canh Dần  source_nguyen=Hạ Nguyên
year_match_dataset = True
month_match_dataset = True
```

## 16. /result Header verification

`identity.four_pillars.year.can_chi` = Bính Ngọ = `bazi.year_pillar` stem+branch. Adapter still binds BaZi first (G1-10A). No UI hardcoded 1966 override.

Live browser screenshot of `/result` was not taken in this session (no portal browser session). API + identity equality is the evidence that Header Tứ Trụ would render Bính Ngọ / Đinh Dậu from the same object as Bát Tự.

## 17. /result Bát Tự verification

Same `data.bazi` pillars. Header `stem` == `bazi.year_pillar.stem` (`header_eq_bazi=True`).

## 18. Report/PDF/DOCX verification

`ReportInputV1Adapter._build_pillars` copies `analysis.bazi`. Customer export copies stored `data.bazi`. After G1-10B those stems are dataset Year/Month.

## 19. Cache/ResultStore invalidation

- Payload field `calendar.calendar_rule_version = G1-10B`
- `ResultStore.loadCurrent()` returns null when:
  - version is present and not `G1-10B`, or
  - version is missing **and** `ganzhi_routing` is present (G1-10A stale)
- `resolveCurrentStoredResult` applies the same check so `/result` will not render a pre-G1-10B analysis as current

User must submit a **new Analyze** after this change.

## 20. Boundary tests

`test_boundary_switches_actual_dataset_row` + `test_1923_1924_actual_can_chi_change`:

| Year | Dataset Year Can Chi | Nguyên |
| --- | --- | --- |
| 1923 | Quý Hợi | Thượng |
| 1924 | Giáp Tý | Trung |
| 1983 | Quý Hợi | Trung |
| 1984 | Giáp Tý | Hạ |
| 2043 | Quý Hợi | Hạ |
| 2044 | Giáp Tý | Thượng (next cycle) |

1923 → 1924 **changes actual Can Chi**, not only the enum.

## 21. Three-Nguyên value tests

`test_three_nguyen_year_month_match_dataset` for 1864 / 1924 / 1966 / 1984 / 2026 asserts stem, branch, and nap_am against the CSV row.

`test_same_cycle_index_uses_selected_nguyen_row`: index 42 in each table is a different `nam_mau`; lookup returns that Nguyên’s row.

## 22. Tests

```
pytest tests/calendar tests/identity tests/date_selection
       tests/bazi/test_pillars.py tests/bazi/test_bazi_calendar_regression.py
       applications/api/tests/test_production_readiness.py
       applications/api/tests/test_phase2_unified_bazi.py -q
```

**298 passed.** Remaining failures in that set: none.

New: `tests/calendar/test_g1_10b_actual_ganzhi.py`

## 23. Files changed

| File | Role |
| --- | --- |
| `engines/calendar_engine/data/tam_nguyen_60_hoa_giap.csv` | 180-row Thượng/Trung/Hạ 60 Hoa Giáp |
| `engines/calendar_engine/tam_nguyen_dataset.py` | Loader + `resolve_year_pillar` / `resolve_month_pillar` |
| `engines/calendar_engine/ganzhi_routing.py` | Year/Month routes use dataset Can Chi |
| `engines/calendar_engine/engine.py` | Tứ Trụ year/month from dataset; `calendar_rule_version` |
| `engines/bazi_engine/engine.py` | Year/Month pillars from dataset; Day/Hour unchanged |
| `engines/date_selection/calendar_adapter.py` | Homepage year from `calendar.year_can_chi` |
| `applications/customer_portal/static/js/result_store.js` | Drop incompatible current result |
| `applications/customer_portal/src/resultState/currentResult.ts` | Same gate for `/result` |
| `tests/calendar/test_g1_10b_actual_ganzhi.py` | Dataset / monkeypatch / boundary / page equality |

## 24. Live screenshot / DOM evidence

API TestClient capture (textual, not a PNG):

```
POST /api/v1/analyze  24/09/1966 04:15 male  → 200
calendar_rule_version G1-10B
tam_nguyen            Trung Nguyên
Header/Bát Tự year    Bính Ngọ   (= Trung Nguyên CSV 1966)
Header/Bát Tự month   Đinh Dậu   (= dataset year stem + 12 Tiết)
Day                   Bính Tuất  (Hạ Nguyên)
Hour                  Canh Dần   (Hạ Nguyên)
identity.year         == bazi.year
homepage year/month   == bazi year/month
```

No UI restyle. Re-run Analyze in the browser so ResultStore writes a G1-10B payload.

G1-10B stops here.
