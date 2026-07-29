# BTE Platform V1.0 — Production Validation Cases

**Growing validation library for Architecture V1.0 (frozen)**  
**Harness:** `validation/production_smoke_runner.py`  
**Raw output:** `validation/production_smoke_raw.json`  
**Last run:** 2026-07-27 — **105 / 105 PASS**

---

## Coverage matrix

| Category | Cases | Purpose |
|----------|-------|---------|
| `critical_reference` | 3 | Production audit blocker 1987-01-21 |
| `before_li_chun` | 5 | Year pillar before Lập Xuân (1987, 2000, 2024, 1988, 1996) |
| `after_li_chun` | 5 | Day after Lập Xuân |
| `on_li_chun` | 5 | Li Chun at 00:00 |
| `leap_year` | 5 | Solar Feb 29 (2000, 2004, 2020, 2024, 2028) |
| `leap_month` | 2 | Lunar leap month boundaries |
| `solar_term` | 4 | Solar-term / month pillar boundaries |
| `zi_hour` | 4 | Hours 0, 1, 2, 23 on reference date |
| `midnight` | 2 | 00:00 and 23:59 |
| `hour_boundary` | 2 | 03:00 and 05:00 on Zi-hour edge |
| `missing_gender` | 1 | `gender=null` (feng_shui omitted) |
| `gender_female` | 1 | Female chart |
| `rc1_real_case` | 20 | RC1 `validation/real_cases` inventory |
| `bazi_regression` | 5 | `test_bazi_calendar_regression` CASES |
| `hour_sweep` | 12 | Every 2 hours on 1990-05-15 |
| `decade_grid` | 13 | Years 1960–2020 step 5 |
| `extra_boundary` | 12 | Y2K, century, leap, critical date variants |
| `invalid_input` | 4 | API 422 validation |
| **Total** | **105** | |

---

## Edge-case requirements (mapped)

| Requirement | Cases |
|-------------|-------|
| Before Li Chun | `lichun_before_*`, `ref_1987_0121` |
| After Li Chun | `lichun_after_*`, `bazi_reg_*` |
| Leap year | `leap_feb29_*`, `ext_19760229`, `ext_20240229` |
| Leap month | `leap_lunar_*` |
| Solar-term boundary | `solar_term_*`, `lichun_on_*` |
| Hour boundary | `hour_boundary_*`, `hour_sweep_*` |
| Zi hour | `zi_hour_*`, `ext_19870121_2300` |
| Midnight | `midnight_*`, `ext_20000101`, `ext_19870121_0000` |
| Missing input | `invalid_no_year` → 422 |
| Invalid input | `invalid_month_13`, `invalid_day_32`, `invalid_hour_25` → 422 |
| Missing gender | `gender_none` → 200, `feng_shui` may be null |

---

## Critical reference case (must always PASS)

### `ref_1987_0121`

| Field | Value |
|-------|-------|
| Input | 1987-01-21 03:30, male, Asia/Ho_Chi_Minh |
| Lunar | 1986-12-22 (via calendar) |
| Solar term | Đại Hàn |
| Year pillar | Bính Dần |
| Month pillar | Tân Sửu |
| Day pillar | Canh Ngọ |
| Hour pillar | Mậu Dần |
| Day master | Canh |

**Smoke status:** PASS (pillar assertions in runner)

---

## Per-case verification checklist

Each smoke case validates:

| Stage | Checks |
|-------|--------|
| HTTP | Expected status (200 or 422) |
| Pipeline | `["calendar","bazi","pattern","score","interpretation","report","narrative"]` |
| Calendar | `solar_date`, `lunar` present |
| Bazi | Four pillars + `day_master` |
| Pattern | `pattern`, `cach_cuc`, `success` |
| Score | `total_score`, `success`; no `details`/`modules` leak |
| Interpretation | `sections[]` non-empty; no `summary`/`matched_rule_count` leak |
| Report | `title`, `markdown`, `html`, `section_count`; no `templates_used` |
| Narrative | Same shape as report; markdown non-empty |
| Internal leaks | No forbidden keys on wire |

---

## RC1 real cases (linked)

| ID | Birth (solar) | Gender |
|----|---------------|--------|
| rc1_01 | 1990-05-15 10:30 | male |
| rc1_02 | 1988-01-08 06:00 | female |
| rc1_03 | 1975-12-31 23:45 | male |
| rc1_04 | 2000-02-29 12:00 | female |
| rc1_05 | 1960-07-04 04:20 | male |
| rc1_06 | 1995-09-09 09:09 | female |
| rc1_07 | 1982-03-21 15:15 | male |
| rc1_08 | 1999-11-11 11:11 | female |
| rc1_09 | 1970-06-01 00:00 | male |
| rc1_10 | 2010-08-20 18:30 | female |
| rc1_11 | 1985-04-12 07:45 | male |
| rc1_12 | 1992-10-03 21:10 | female |
| rc1_13 | 1968-02-14 08:00 | male |
| rc1_14 | 2005-05-05 05:05 | female |
| rc1_15 | 1978-08-18 14:00 | male |
| rc1_16 | 1993-01-01 01:01 | female |
| rc1_17 | 1980-12-25 19:30 | male |
| rc1_18 | 1997-07-07 17:00 | female |
| rc1_19 | 1965-09-30 03:15 | male |
| rc1_20 | 2001-03-08 13:45 | female |

Folder snapshots: `validation/real_cases/case_01` … `case_20`.

---

## Bazi regression cases (engine reference)

| ID | Solar | Expected year/month/day/hour pillars |
|----|-------|--------------------------------------|
| bazi_reg_19861230 | 1986-12-30 12:00 | Bính Dần / Canh Tý / Mậu Thân / Mậu Ngọ |
| bazi_reg_19870205 | 1987-02-05 12:00 | Đinh Mão / Nhâm Dần / Ất Dậu / Nhâm Ngọ |
| bazi_reg_19880217 | 1988-02-17 12:00 | Mậu Thìn / Giáp Dần / Nhâm Dần / Bính Ngọ |
| bazi_reg_20000204 | 2000-02-04 12:00 | Canh Thìn / Mậu Dần / Nhâm Thìn / Bính Ngọ |
| bazi_reg_20240210 | 2024-02-10 12:00 | Giáp Thìn / Bính Dần / Giáp Thìn / Canh Ngọ |

Source: `tests/bazi/test_bazi_calendar_regression.py`.

---

## Adding new cases

1. Add entry in `_build_case_library()` in `validation/production_smoke_runner.py`.
2. Choose `category` from existing taxonomy or add new category with documentation update.
3. Run: `py -3.13 validation/production_smoke_runner.py`
4. Update this file and `production_smoke_report.md`.

**Rules (Architecture Freeze):**

- Do not change expected engine output without domain approval.
- Invalid-input cases must expect HTTP 422.
- Reference cases must include pillar assertions in runner if business-critical.

---

## Related artifacts

| File | Purpose |
|------|---------|
| `validation/production_smoke_runner.py` | Executable smoke suite |
| `validation/production_smoke_raw.json` | Machine-readable results |
| `validation/real_cases/` | RC1 case folders |
| `tests/bazi/test_bazi_calendar_regression.py` | Unit regression |
| `applications/api/tests/test_production_readiness.py` | Portal-facing assertions |
