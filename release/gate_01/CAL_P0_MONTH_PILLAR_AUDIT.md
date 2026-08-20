# CAL-P0 — Month Pillar Canonical Audit

| Field | Value |
|-------|-------|
| **Gate** | CAL-P0 Phase 1 forensic |
| **Date** | 2026-08-20 |
| **Case (Product Owner)** | Đoàn Quang Hưng · nam · 29/08/1981 04:30 · Quảng Ninh |
| **Do not confuse with** | Pilot `CASE-0004` = Nguyễn Tiến Minh 2013-08-20 (month Canh Thân, jieqi-aligned) |
| **Phase 2** | **STOPPED.** No engine repair. |

---

## Decision (read this first)

Product Owner now requires month pillar **Đinh Dậu** from *Can Chi Thông Luận* (lunar `01/08/1981`).

Frozen BTE Calendar/BaZi SSOT requires month pillar from **12 Tiết / nguyệt lệnh**, and the locked algorithm document says **do not use lunar month** for Tử Bình month.

Live production for this birth is **Bính Thân**. That result is **correct under the project SSOT** and **incorrect under the Product Owner lunar-month reading**.

This is **not** a Strength bug, not a wrong Ngũ Hổ Độn table, and not a wrong lunar converter. Lunar conversion already returns `01/08/1981`. Month stem **Bính** is the Ngũ Hổ Độn stem of **Thân** in a Tân year. Stem **Đinh** is what Ngũ Hổ Độn would produce **if the branch were Dậu**.

Repairing to Đinh Dậu would mean **replacing the locked 12-tiết month rule with lunar-month mapping**. That is a new canonical formula. Item 9 of this gate forbids inventing it.

**No code was changed. Strength weights/thresholds were not touched. Golden Dataset was not updated.**

---

## 1. Captured production input

Normalized request (not altered to force a pillar):

```json
{
  "year": 1981,
  "month": 8,
  "day": 29,
  "hour": 4,
  "minute": 30,
  "gender": "male",
  "timezone": "Asia/Ho_Chi_Minh",
  "full_name": "Doan Quang Hung",
  "birth_place": "Quang Ninh"
}
```

Civil wall clock is treated as local time. Location name is presentation metadata and is **not** passed into Calendar/BaZi. Timezone label is stored; solar-term month still uses **date only** (no hour, no longitude).

---

## 2. Lunar conversion (PASS — do not change)

| Field | Production |
|-------|------------|
| Solar date | `29/08/1981` |
| Lunar day | `1` |
| Lunar month | `8` |
| Lunar year | `1981` |
| Leap | `false` |
| `lunar_date` | `01/08/1981` |

Matches Product Owner / project expected lunar date. Converter: `engines/calendar_engine/lunar/converter.py` via `CalendarEngine.build()`.

Lunar year can chi on calendar payload: **Tân Dậu** (same as BaZi year for this date; Lập Xuân 1981 = 4 Feb).

---

## 3. Month branch — why production is **Thân**

Production month branch does **not** come from lunar month 8.

Path:

```text
Birth y/m/d
  → CalendarEngine.build()                 # lunar + current solar term name only
  → OrchestratorService._run
  → BaziEngine.build(calendar)
       SolarTermEngine.get_bazi_month(y, m, d)   ← FIRST (and only) month-branch source
```

`get_bazi_month` (`engines/calendar_engine/solar_terms/engine.py`):

- Uses the **12 Tiết** start terms, not Gregorian month, not lunar month.
- Table: `engines/calendar_engine/solar_terms/data/month_branch.csv`
- Term dates: `solar_term_base_dates.csv` (V1 date-only approximation)

For 1981-08-29:

| Item | Value |
|------|-------|
| Current term | **Xử Thử** (index 13) |
| Last month-start 节 | **Lập Thu** = 1981-08-07 (`solar_term_base_dates.csv` month=8 day=7) |
| Next month-start 节 | **Bạch Lộ** = 1981-09-07 |
| `month_index` | **7** |
| Branch | **Thân** |

So:

```text
input 1981-08-29  →  after Lập Thu, before Bạch Lộ  →  branch = Thân
```

Lunar month 8 would map (folk 寅正) to **Dậu**. That mapping is **not** on the production path.

V1 boundaries for 1981 (date-only table):

| Date | Term | Month branch |
|------|------|----------------|
| 1981-08-06 | Đại Thử | Mùi |
| 1981-08-07 | Lập Thu | **Thân** |
| 1981-08-29 | Xử Thử | **Thân** |
| 1981-09-06 | Xử Thử | Thân |
| 1981-09-07 | Bạch Lộ | **Dậu** |

29 August cannot become Dậu under 12 Tiết unless Bạch Lộ is redefined to before 29 Aug, which astronomy and this table both reject (Bạch Lộ ≈ solar longitude 165° ≈ 7–8 Sep).

---

## 4. Month stem — why production is **Bính** not **Đinh**

Formula: Ngũ Hổ Độn in `BaziEngine._month_stem` / `_MONTH_YIN_START_STEM` / `month_stem_rules.csv`.

Year stem **Tân** → “Bính Tân chi niên **Canh** tác thủ” → month **Dần** starts at **Canh**.

| `month_index` | Branch | Stem (Tân year) |
|--------------:|--------|-----------------|
| 1 | Dần | Canh |
| 2 | Mão | Tân |
| 3 | Thìn | Nhâm |
| 4 | Tỵ | Quý |
| 5 | Ngọ | Giáp |
| 6 | Mùi | Ất |
| 7 | **Thân** | **Bính** |
| 8 | **Dậu** | **Đinh** |

Production: `month_index=7` → **Bính Thân**.  
Product Owner: lunar month 8 treated as Dậu → **Đinh Dậu**.

The stem table is the same in both readings. The disagreement is **which month index / branch** is fed into it.

---

## 5. Project canonical rule (already locked)

Intended SSOT for Tử Bình month is **tiết khí / 12 Tiết**, not lunar month.

| Source | Status | Rule |
|--------|--------|------|
| `database/01_du_lieu_goc/09_calendar/00_cau_hinh/03_thuat_toan.md` §6 | **DESIGN_LOCKED** | “Xác định tháng Tử Bình: **Không dùng tháng âm lịch. Dùng tiết khí.**” |
| `engines/bazi_engine/engine.py` module docstring | production code | “Month follows **12 Tiết (nguyệt lệnh)**” |
| `engines/calendar_engine/solar_terms/engine.py` | production code | “Tháng Bát Tự đổi theo 12 Tiết … không theo tháng dương lịch.” |
| `engines/calendar_engine/thuat_toan.md` | DESIGN | Bước 05 Tiết Khí → Bước 06 Nguyệt Lệnh → Bước 07 Can Chi tháng |
| `.specs/calendar_engine.md` | Official | Solar Terms in flow before Ganzhi |
| `knowledge/pilot/replay/root_cause/CASE_0006_CALENDAR_RCA.md` | closed RCA | Expert lunar-like month vs engine 12 Tiết: classified **FIXTURE_INCORRECT**, **no engine change** |

Hạ Nguyên / Tam Nguyên Cửu Vận is **not** used for month GanZhi.

*Can Chi Thông Luận* is **not** checked into the Calendar pack as the month-pillar SSOT.

---

## 6. CASE_004 contradiction (Đoàn Quang Hưng)

| Field | Product Owner canonical | BTE live `/analyze` | Status |
|-------|-------------------------|---------------------|--------|
| Year | Tân Dậu | Tân Dậu | PASS |
| Month | **Đinh Dậu** | **Bính Thân** | **CONFLICT** (two canons) |
| Day | Kỷ Mão | Kỷ Mão | PASS |
| Hour | Bính Dần | Bính Dần | PASS |
| Lunar | 01/08/1981 | 01/08/1981 | PASS |

Isolated to Month Pillar **relative to the Product Owner book**. Isolated to **month-system choice** relative to project SSOT.

---

## 7. Inventory — who can compute Month GanZhi

| Implementation | Used by live `/analyze`? | System |
|----------------|--------------------------|--------|
| `BaziEngine.build` → `SolarTermEngine.get_bazi_month` + `_month_stem` | **YES — production SSOT** | 12 Tiết + Ngũ Hổ Độn |
| `OrchestratorService._shape_calendar` `bazi_can_chi.month` | copies BaZi | no second calc |
| Portal / Report adapters | bind `data.bazi.month_pillar` | **no independent calc** |
| `LuckEngine` Dayun | starts from **BaZi month pillar**; jie for start-age | depends on BaZi month |
| `engines/bazi_engine/pillars/month_pillar.py` | legacy / not wired to API | also solar-term |
| `engines/calendar_engine/solar_terms/calculator.py` | alternate calculator | solar-term + CSV |
| `GanzhiMonthProcessor` | old processor registry; **not** `CalendarEngine.build` | mapping + month_commander |
| `CalendarEngine.build` | lunar + term **name** only; **does not emit month pillar** | — |

There are **legacy duplicates**, but live pipeline has **one** month calculation: `BaziEngine.build`. Portal does not recompute.

Competing **semantic** systems:

1. **Project / live:** 12 Tiết nguyệt lệnh.  
2. **Product Owner this case / folk lunar month 1=Dần:** lunar month 8 → Dậu.  
3. Lunar month is computed and displayed, then **ignored** for BaZi month.

---

## 8–9. Why Phase 2 is stopped

Item 9: if the Product Owner-approved canonical rule is not actually implemented/documented, **STOP** before inventing a new formula.

Product Owner rule for this case = lunar-month (book) **Đinh Dậu**.  
That rule is **explicitly forbidden** in the locked Calendar algorithm doc and is **not** implemented.

Switching production to lunar month would:

- violate DESIGN_LOCKED §6;
- invert the CASE-0006 RCA (engine was judged correct vs expert Tỵ);
- silently change every birth that sits between a lunar-month boundary and a 12-tiết boundary (22 of 101 Golden datetime inputs disagree — see §21);
- require a Product Owner **SSOT change**, not a bugfix.

Hard-coding Đinh Dậu for 1981-08-29 is also forbidden.

**Repair location:** none. Canonical source remains `BaziEngine.build` + `SolarTermEngine.get_bazi_month`.

---

## 10–17. Downstream on the **current** (Bính Thân) chart

These are live `/analyze` values. They are **valid under 12 Tiết**. They are **stale if** Product Owner later switches SSOT to lunar month. They were **not** snapshotted as freeze targets for a lunar-month world.

| Layer | Live (Bính Thân) | If SSOT became Đinh Dậu |
|-------|------------------|-------------------------|
| Strength | **0.71 / strong** (`raw=21`, Thân vượng). Season Hưu +10 (Kỷ Thổ sinh Thân Kim). Evidence: `sea_003 +10 · root_002 +22 · sup_002 +10 · sup_006 +5 · ctl_002 −8 · flw_001 −8 · flw_005 −10` | Must be recomputed. **Do not force Thân nhược.** |
| Pattern | `thuong_quan_phoi_an` / **Thương Quan phối Ấn** (`com_thuq_an_01`). Nguyệt lệnh Thân · khí chính Canh = Thương Quan vs Kỷ | Would follow Dậu 本气 Tân = Thực Thần vs Kỷ — pattern almost certainly changes |
| Temperature | `cool` / customer label **Lương** / **Cần ôn ấm** (`cli_004`). Month branch Thân, season autumn | Must recompute. Customer copy **Khí mát** (instead of Lương) is a **presentation** request, not a month-algorithm repair; **not applied in this STOP** |
| Useful God | **Hỏa · Đinh · Thiên Ấn** (`sea_004` “Thu kim vượng cần hỏa tôi luyện”) | Winner likely changes with month/season |
| Ten Gods (month stem vs Kỷ) | Month **Bính** vs Kỷ = **Chính Ấn** (G1-01 `ten_god_name`) | Month **Đinh** vs Kỷ = **Thiên Ấn** (same mapping; different stem) |
| Five Elements | Mộc4 · Hỏa3 · Thổ3 · Kim5 · Thủy1 | Must regenerate (Dậu/Tân ≠ Thân/Canh hidden set) |
| Luck / Đại vận | Reverse from **Bính Thân** → first cycle **Ất Mùi** (age 7). `from_month_ganzhi=Bính Thân`. Start-age jie = Lập Thu 1981-08-07 | Entire sequence would change if month pillar changes |

Strength was **not** retuned. 0.71 is not an expected freeze for a future Đinh Dậu chart.

---

## 18 + 23. Four-case month regression (no algorithm change)

Folk lunar-month mapping below is **diagnostic only** (tháng âm 1 = Dần). It is not production.

| Case | Birth date | Lunar date | Old month (live) | Folk lunar-month pillar | New canonical month | Status |
|------|------------|------------|------------------|-------------------------|---------------------|--------|
| Đoàn Quang Hưng | 29/08/1981 | 01/08/1981 | **Bính Thân** | Đinh Dậu | **unchanged Bính Thân** (project SSOT) | CONFLICT vs PO book |
| Nguyễn Tiến Sơn | 21/01/1987 | 22/12/1986 | Tân Sửu | Tân Sửu | Tân Sửu | PASS both systems |
| Lương Ngọc Huỳnh | 24/09/1966 | 10/08/1966 | Đinh Dậu | Đinh Dậu | Đinh Dậu | PASS both systems |
| Đặng Thị Dung | 22/05/1982 | 29/04/1982 | Ất Tỵ | Ất Tỵ | Ất Tỵ | PASS both systems |

A lunar-month switch would **not** move Sơn / Huỳnh / Dung on this sample, and **would** move Hưng. That is why a four-case smoke test is insufficient: see Golden disagreements in §21.

Live HTTP `POST /api/v1/analyze` (127.0.0.1:8000) confirmed the live column (UTF-8 pillars: Hung Bính Thân 0.71 strong; Sơn Tân Sửu 0.87; Huỳnh Đinh Dậu 0.64; Dung Ất Tỵ 0.24).

---

## 19. Month-pillar Golden matrix (project 12-tiết SSOT)

Expected month GanZhi below is derived from **data tables**, not from calling `get_bazi_month`:

- branch from `month_branch.csv` + `solar_term_base_dates.csv` (date strictly after start 节, before next);
- stem from `month_stem_rules.csv` Ngũ Hổ Độn;
- year stem from Lập Xuân (4 Feb).

Year **1981** = Tân after Lập Xuân. Tân → Dần starts **Canh**.

| # | Gregorian (mid-month) | Lunar (engine) | Year GZ | Expected month GZ | Provenance |
|---|-----------------------|----------------|---------|-------------------|------------|
| 1 | 1981-02-20 | 16/01/1981 | Tân Dậu | Canh Dần | after Lập Xuân 2/4, before Kinh Trập 3/6 |
| 2 | 1981-03-20 | 15/02/1981 | Tân Dậu | Tân Mão | after Kinh Trập 3/6, before Thanh Minh 4/5 |
| 3 | 1981-04-20 | 16/03/1981 | Tân Dậu | Nhâm Thìn | after Thanh Minh 4/5, before Lập Hạ 5/5 |
| 4 | 1981-05-20 | 17/04/1981 | Tân Dậu | Quý Tỵ | after Lập Hạ 5/5, before Mang Chủng 6/6 |
| 5 | 1981-06-20 | 19/05/1981 | Tân Dậu | Giáp Ngọ | after Mang Chủng 6/6, before Tiểu Thử 7/7 |
| 6 | 1981-07-20 | 19/06/1981 | Tân Dậu | Ất Mùi | after Tiểu Thử 7/7, before Lập Thu 8/7 |
| 7 | 1981-08-20 | 21/07/1981 | Tân Dậu | **Bính Thân** | after Lập Thu 8/7, before Bạch Lộ 9/7 |
| 8 | 1981-09-20 | 23/08/1981 | Tân Dậu | **Đinh Dậu** | after Bạch Lộ 9/7, before Hàn Lộ 10/8 |
| 9 | 1981-10-20 | 23/09/1981 | Tân Dậu | Mậu Tuất | after Hàn Lộ 10/8, before Lập Đông 11/7 |
| 10 | 1981-11-20 | 24/10/1981 | Tân Dậu | Kỷ Hợi | after Lập Đông 11/7, before Đại Tuyết 12/7 |
| 11 | 1981-12-20 | 25/11/1981 | Tân Dậu | Canh Tý | after Đại Tuyết 12/7, before Tiểu Hàn 1/6 |
| PO conflict | **1981-08-29** | **01/08/1981** | Tân Dậu | **Bính Thân** under 12 Tiết; **Đinh Dậu** under lunar month 8 | Product Owner vs SSOT |

Row 7 shows Đinh Dậu is the **correct 12-tiết month in late September**, not on 29 August.

Tests for this matrix were **not** added: writing them would freeze 12 Tiết; writing the inverse would freeze lunar month. Product Owner must pick SSOT first.

---

## 20. Boundary cases (project rule = 12 Tiết)

Representative 1981 transitions from the same CSV dates:

| Window | Date | Expected branch (12 Tiết) |
|--------|------|---------------------------|
| before Lập Thu | 1981-08-06 | Mùi |
| Lập Thu | 1981-08-07 | Thân |
| after | 1981-08-08 | Thân |
| before Bạch Lộ | 1981-09-06 | Thân |
| Bạch Lộ | 1981-09-07 | Dậu |
| after | 1981-09-08 | Dậu |

V1 limitation (already in CASE-0006 RCA): term tables are **date-only**, no hour / true solar time. Not causal for 29 Aug (22 days after Lập Thu, 9 days before Bạch Lộ).

---

## 21. `MONTH_PILLAR_REVIEW_REQUIRED`

Do **not** bulk-update Golden. Product Owner should review cases where **12 Tiết ≠ folk lunar-month 1=Dần**.

### Pilot Replay (expert expected vs live jieqi)

| Case | Birth | Expert month | Live jieqi | Folk lunar-month | Note |
|------|-------|--------------|------------|------------------|------|
| CASE-0006 | 1988-06-07 | **Đinh Tỵ** | **Mậu Ngọ** | Đinh Tỵ | Same class as Hưng: expert = lunar month; RCA already kept jieqi |
| CASE-0001 … 0005, 0007 | — | matches live | matches live | matches live | no review for month system |

Pilot CASE-0004 (2013-08-20 Canh Thân) is **not** Đoàn Quang Hưng.

### Golden datetime inputs (`tests/golden_dataset/inputs`)

101 inputs with `solar_datetime`. **22** disagree jieqi vs folk lunar-month:

| File | Gregorian | Lunar | Jieqi (live) | Folk lunar-month | Term |
|------|-----------|-------|--------------|------------------|------|
| case_0003.json | 1960-03-03 | 06/02/1960 | Mậu Dần | Kỷ Mão | Vũ Thủy |
| case_0010.json | 1960-12-09 | 21/10/1960 | Mậu Tý | Đinh Hợi | Đại Tuyết |
| case_0013.json | 1961-03-08 | 22/01/1961 | Tân Mão | Canh Dần | Kinh Trập |
| case_0026.json | 1962-07-02 | 01/06/1962 | Bính Ngọ | Đinh Mùi | Hạ Chí |
| case_0028.json | 1962-10-06 | 08/09/1962 | Kỷ Dậu | Canh Tuất | Thu Phân |
| case_0031.json | 1963-01-03 | 08/12/1962 | Nhâm Tý | Quý Sửu | Đông Chí |
| case_0036.json | 1963-07-18 | 28/05/1963 | Kỷ Mùi | Mậu Ngọ | Tiểu Thử |
| case_0038.json | 1963-09-08 | 21/07/1963 | Tân Dậu | Canh Thân | Bạch Lộ |
| case_0040.json | 1963-12-14 | 29/10/1963 | Giáp Tý | Quý Hợi | Đại Tuyết |
| case_0042.json | 1964-02-04 | 21/12/1963 | Bính Dần | Đinh Sửu | Lập Xuân |
| case_0044.json | 1964-05-10 | 29/03/1964 | Kỷ Tỵ | Mậu Thìn | Lập Hạ |
| case_0059.json | 1965-11-04 | 12/10/1965 | Bính Tuất | Đinh Hợi | Sương Giáng |
| case_0063.json | 1966-04-02 | 12/03/1966 | Tân Mão | Nhâm Thìn | Xuân Phân |
| case_0065.json | 1966-07-07 | 19/05/1966 | Ất Mùi | Giáp Ngọ | Tiểu Thử |
| case_0066.json | 1966-07-11 | 23/05/1966 | Ất Mùi | Giáp Ngọ | Tiểu Thử |
| case_0076.json | 1967-08-06 | 01/07/1967 | Đinh Mùi | Mậu Thân | Đại Thử |
| case_0080.json | 1968-01-01 | 02/12/1967 | Nhâm Tý | Quý Sửu | Đông Chí |
| case_0082.json | 1968-03-04 | 06/02/1968 | Giáp Dần | Ất Mão | Vũ Thủy |
| case_0088.json | 1968-11-15 | 25/09/1968 | Quý Hợi | Nhâm Tuất | Lập Đông |
| case_0089.json | 1968-11-08 | 18/09/1968 | Quý Hợi | Nhâm Tuất | Lập Đông |
| case_0091.json | 1969-02-12 | 26/12/1968 | Bính Dần | Đinh Sửu | Lập Xuân |
| case_0094.json | 1969-05-11 | 25/03/1969 | Kỷ Tỵ | Mậu Thìn | Lập Hạ |

Plus Product Owner Hưng 1981-08-29 (not in this Golden folder).

Golden `case_0004.json` is 1960-04-20 (WP4.5 coverage), **not** Hưng.

---

## 22. Live runtime

No repair → API was not restarted for this gate. Existing `127.0.0.1:8000` `POST /api/v1/analyze` already returns Bính Thân for Hưng. Portal rebuild not required (no binding change). Do not reuse `bte_last_result` when Product Owner inspects: run a **new** Analyze.

Out of scope observation (not repaired): `calendar.lunar_can_chi.day` for this birth shows `Mậu Dần` while BaZi day pillar is `Kỷ Mão`. Month path does not use that field.

---

## 24. Required report checklist

1. **Root cause:** production month = 12 Tiết nguyệt lệnh; 1981-08-29 is inside Lập Thu→Bạch Lộ → Thân; Ngũ Hổ Độn(Tân, 7) = Bính. Product Owner Đinh Dậu = lunar month 8 as Dậu.  
2. **Old / current algorithm:** `SolarTermEngine.get_bazi_month` + `BaziEngine._month_stem`.  
3. **Canonical project algorithm:** tiết khí, not lunar month (`03_thuat_toan.md` §6 DESIGN_LOCKED).  
4. **Why Hưng is Bính Thân:** Xử Thử / month_index 7 / Thân / Canh+6 = Bính.  
5. **Repair location:** none.  
6. **SSOT:** `BaziEngine.build` month pillar; Portal copies it.  
7. **CASE_004 before/after:** before = after = Bính Thân (no repair).  
8. **Downstream:** current Bính Thân values recorded; not preserved as lunar-month expected.  
9. **Four-case:** only Hưng disagrees jieqi vs folk lunar.  
10. **Month Golden matrix:** 12-tiết table in §19 (from CSV).  
11. **Historical review list:** §21.  
12. **Tests:** none added (would freeze one side of the conflict).  
13. **Live:** `/analyze` Hưng = Tân Dậu / Bính Thân / Kỷ Mão / Bính Dần · lunar 01/08/1981 · strength 0.71 strong.

Repair report / regression file: **not written**.

---

## What Product Owner must decide

Choose **one** V1.0 month SSOT:

**A. Keep 12 Tiết (current locked rule).**  
Hưng month stays **Bính Thân**. Book Đinh Dậu is a source-convention difference (*Can Chi Thông Luận* / lunar month), same class as Pilot CASE-0006. Strength 0.71 / Pattern Thương Quan phối Ấn remain the chart of Bính Thân.

**B. Change SSOT to lunar-month Tử Bình.**  
Requires unfreezing `03_thuat_toan.md` §6, a general month implementation (not a date hard-code), invalidation of CASE-0006 RCA, and Product Owner review of the 22 Golden disagreements plus Hưng. Downstream of Hưng must be recomputed from scratch after that change.

Until that decision, CAL-P0 does not mark repaired.

---

## Completion

**CAL-P0 MONTH PILLAR: CONFLICT — PRODUCT OWNER LUNAR-MONTH CANON vs PROJECT 12-TIẾT SSOT — NO REPAIR**
