# CASE-0006 — Calendar / BaZi Root Cause Analysis

**Sprint:** PILOT-1A  
**Status:** Investigation complete — no production code change applied  
**Architecture Freeze:** AF-1 unchanged  
**Confidence:** High (~0.95)

---

## 0. Sprint-brief correction

The PILOT-1A brief listed CASE-0006 as:

- Gregorian `2015-08-14 07:20` Hà Nội  
- Expected month `Giáp Thân` vs live `Mậu Ngọ`

That birth/pillars belong to **CASE-0003** (Pilot Replay fixtures), which **matched** live pillars in the first replay.

The **actual** CASE-0006 divergence from live Pilot Replay is:

| Field | Value |
|---|---|
| Subject | Nguyễn Thị Hương Mai |
| Gregorian | **1988-06-07 20:45** |
| Timezone label | `Asia/Ho_Chi_Minh` |
| Location | Hải Phòng, Việt Nam |
| Gender | female |

This RCA investigates the **real** CASE-0006.

---

## 1. Input

```text
year=1988, month=6, day=7, hour=20, minute=45
timezone="Asia/Ho_Chi_Minh"   # label discarded on live path
gender="female"
```

Entrypoint:

```text
OrchestratorService.analyze → CalendarEngine.build → BaziEngine.build
```

---

## 2. Canonical expected pillars (Pilot fixture / expert)

| Pillar | Expert expected |
|---|---|
| Year | Mậu Thìn |
| Month | **Đinh Tỵ** |
| Day | Quý Tỵ |
| Hour | Nhâm Tuất |

---

## 3. Live runtime pillars

| Pillar | Live actual |
|---|---|
| Year | Mậu Thìn |
| Month | **Mậu Ngọ** |
| Day | Quý Tỵ |
| Hour | Nhâm Tuất |

Calendar enrichment also reported:

- `solar_term`: Mang Chủng (index 8)
- `lunar`: 1988-04-23 (tháng 4 âm, not leap)
- `month_can_chi`: Mậu Ngọ (copied from BaZi in orchestrator shaping)

Year / Day / Hour agree. **Only month diverges.**

---

## 4. Algorithm path

```text
Gregorian Input (y/m/d/h/min)
        ↓
OrchestratorService.run_stage
  del timezone   ← timezone string ignored
        ↓
CalendarEngine.build(y, m, d, h, min)
  • stores solar civil datetime
  • SolarTermEngine.get_current_term(y, m, d)   ← DATE ONLY (no hour)
  • solar_to_lunar(..., time_zone=7.0)          ← lunar only
        ↓
BaziEngine.build(calendar | y,m,d,h,min)
  • Year: Lập Xuân rule → GanzhiAlgorithm.year
  • Month BRANCH: SolarTermEngine.get_bazi_month(y, m, d)
  • Month STEM: Wu Hu Dun (_month_stem)
  • Day: JulianDay + GanzhiAlgorithm.day
  • Hour: earthly branch from clock hour + Ngũ Thử Độn stem
        ↓
BaZi Output / Calendar month_can_chi shaped from BaZi
```

Key files:

- `applications/api/services/orchestrator.py` (`del timezone`)
- `engines/calendar_engine/engine.py`
- `engines/calendar_engine/solar_terms/engine.py`
- `engines/calendar_engine/solar_terms/data/solar_term_base_dates.csv`
- `engines/calendar_engine/solar_terms/data/month_branch.csv`
- `engines/bazi_engine/engine.py` (`get_bazi_month` + `_month_stem`)

---

## 5. Timezone path

| Question | Answer |
|---|---|
| Which timezone is applied? | **None for solar terms / month pillar.** Label discarded. |
| Location conversion correct? | Location not used on this path. |
| DST involved? | **No.** VN modern civil time is fixed UTC+7; 1988 has no DST effect here. |
| Local civil time? | Yes — y/m/d/h/min treated as local civil wall clock, but **month branch uses calendar date only**. |

Evidence:

```222:222:applications/api/services/orchestrator.py
        del timezone  # reserved for future calendar localization
```

Timezone non-application is a **latent** gap for near-boundary births. It is **not causal** for CASE-0006 (birth is ≥1 calendar day after the engine’s Mang Chủng flip).

---

## 6. Solar-term result

Engine V1 base table (`solar_term_base_dates.csv`):

```text
Mang Chủng (index 8) → month=6, day=6  (every year, date-only)
```

Live flip for June 1988:

| Date | Current term | Month branch |
|---|---|---|
| 1988-06-05 | Tiểu Mãn | **Tỵ** |
| 1988-06-06 | Mang Chủng | **Ngọ** |
| 1988-06-07 | Mang Chủng | **Ngọ** |

`month_branch.csv` rule:

- Tỵ: Lập Hạ → Mang Chủng  
- Ngọ: Mang Chủng → Tiểu Thử  

So for 1988-06-07, **Ngọ is the engine-correct month branch**.

Wu Hu Dun (year stem Mậu):

- Tỵ → **Đinh Tỵ** (matches expert stem if branch were Tỵ)
- Ngọ → **Mậu Ngọ** (matches live)

Stem divergence is **consequent** to branch choice. First divergence is month **branch**.

---

## 7. First divergence

```text
Input PASS
Time normalization PASS (civil y/m/d/h/min accepted)
Solar term resolution → Mang Chủng on 1988-06-07 PASS (under V1 table)
Year pillar PASS (Mậu Thìn)
Month BRANCH  ← FIRST DIVERGENCE (expert Tỵ vs engine Ngọ)
Month STEM consequent (Đinh vs Mậu)
Day / Hour PASS
```

Not caused by:

- wrong Wu Hu Dun math (both stems consistent with their branches)
- hour pillar logic
- lunar-month engine path (engine does **not** use lunar month for BaZi month)
- DST

---

## 8. Root cause classification

**Primary: `FIXTURE_INCORRECT` (expert / Pilot expected month)**

Relative to BTE classical solar-term month rules (nguyệt lệnh theo tiết khí), live **Mậu Ngọ** is correct for 1988-06-07.

Expert **Đinh Tỵ** matches the Wu Hu Dun stem for a **Tỵ** month — i.e. the chart that would apply **before** Mang Chủng. Likely confusion with:

- folk lunar month 4 (`lunar_month=4` on this chart), or  
- a charting table that still placed the day in Tỵ month

BTE calendar data states Ngọ begins at Mang Chủng (`02_jieqi.csv`: “Bắt đầu tháng Ngọ”).

### Secondary (not causal for this birth)

| Finding | Class | Notes |
|---|---|---|
| Solar terms date-only (no hour; fixed June 6) | V1 approximation | Can misclassify some **June 5 evening** births vs astronomy; not June 7 |
| Timezone ignored | Latent publication/localization gap | Irrelevant here |
| Missing generated `solar_term_dates.csv` | Alternate calculator path incomplete | Live path uses `SolarTermEngine` + base dates |

Not classified as `ENGINE_BUG` or `AMBIGUOUS_BOUNDARY` for CASE-0006 specifically.

---

## 9. Evidence

1. Live replay result: `knowledge/pilot/replay/results/CASE-0006.json`  
2. Month flip dump: 1988-06-05 → Tỵ; 1988-06-06/07 → Ngọ  
3. `month_branch.csv` rows for Tỵ/Ngọ  
4. `solar_term_base_dates.csv` Mang Chủng = 6/6  
5. Orchestrator `del timezone`  
6. `BaziEngine.build` month from `get_bazi_month` + `_month_stem`

---

## 10. Recommended fix

| Action | Required now? |
|---|---|
| Production engine code change for CASE-0006 | **No** |
| Fixture / Pilot expected month correction to **Mậu Ngọ** | **Yes** (when Expected edits are explicitly allowed) |
| Document expert source as lunar-folk vs tiết khí | Recommended |
| Future V2 astronomical jieqi + real timezone | Separate backlog; not required to close this case |

### If Expected remains frozen

Keep CASE-0006 as **DISCREPANCY with root cause FIXTURE_INCORRECT** — do not “fix” the engine to emit Đinh Tỵ.

---

## 11. Whether code change is required

**No** for CASE-0006 month divergence.

Stop condition for code change is **not met**: current month behavior is objectively aligned with published solar-term month rules; expert expected month is the incorrect side under that SSOT.

---

## 12. Whether fixture correction is required

**Yes** (process / Pilot data), not engine:

- Update expert month to **Mậu Ngọ**, **or**  
- Relabel the expected pillars as “non-SSOT / lunar-month charting” so they are not treated as classical BaZi ground truth.

Do **not** change Golden Dataset expected values in this sprint (scope forbid). Record the finding only.

---

## 13. Decision gate (PILOT-1A)

```text
Code change proposed?  NO
Fixture change applied? NO (frozen expecteds)
Investigation artifact? YES — this file
```
