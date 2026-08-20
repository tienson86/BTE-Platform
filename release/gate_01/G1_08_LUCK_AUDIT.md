# G1-08 — Đại vận / Luck Cycles Truth & Evidence Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-08 |
| **Document** | `release/gate_01/G1_08_LUCK_AUDIT.md` |
| **Phase** | 1 — Audit only |
| **Date** | 2026-08-20 |
| **Status** | AUDIT PASS / G1-08 NOT READY — REPAIR REQUIRED |
| **Scope** | Production natal Đại vận generation, direction, solar-term start age, CASE-0001, Portal/Report/PDF/DOCX binding |
| **Out of scope** | Engine repair; Calendar/BaZi/Strength/Temperature/Pattern/Useful God/ShenSha edits; Golden edits; Deep Luck interpretation (cát/hung, tài vận, Dụng/Hỷ/Kỵ) |

Live CASE-0001 was executed read-only through:

```text
ProductionEngineRunner / OrchestratorService
  → CalendarEngine.build
  → BaziEngine.build(..., gender=)
  → LuckEngine.build(calendar, bazi, pattern, rule_context, score)
       DefaultDayunProvider.provide
  → shape_luck_payload(luck_context)
  → payload["luck"] / EnginePipelineOutput.luck
  → ReportInputV1Adapter._build_luck_cycles
  → Portal copies data.luck (formatLuckCurrent / formatLuckSequence)
```

No Luck Engine, Calendar, BaZi, rules, Portal, Report, or Golden Dataset was modified for this audit.

---

# Verdict

| # | Question | Answer |
|---|----------|--------|
| 1 | Production Luck Engine? | **`engines.luck_engine.engine.LuckEngine`** + **`DefaultDayunProvider`**. Not `CanonicalLuckPipeline`. Not `engines.analysis_engine.luck_engine`. |
| 2 | Thuận / nghịch formula? | **`is_male(gender) == is_yang(year_stem)`** → thuận (`forward`); else nghịch (`reverse`). Proven in code. |
| 3 | Âm/dương source? | **Niên can** (`year_pillar.stem`) via canonical `STEM_META`. **Not** Nhật can. |
| 4 | Gender effect? | Male + Dương niên can → thuận. Male + Âm → nghịch. Female inverted. Missing gender defaults to **`"male"`**. |
| 5 | Solar-term reference? | **12 Tiết** (month-start jie), not 中气. Thuận = nearest **later** jie (`>`). Nghịch = nearest **earlier** jie (`<`). Birth **on** jie is excluded. |
| 6 | Distance? | Whole **calendar days**: `\|anchor − birth\|.days`. Hour/minute discarded. |
| 7 | Conversion? | **`3 days = 1 year`**: `start_age = max(1, int(round(days / 3.0)))`. No months/hours conversion. Integer age only. |
| 8 | Tuổi khởi vận? | That rounded integer. CASE-0001: 14 days → 4.667 → **5**. |
| 9 | Months/days of start? | **No.** `start_date` is empty. No exact giao vận datetime. |
| 10 | First pillar from month? | Step **±1 JiaZi from month pillar**; month itself is **not** stored. CASE-0001 `Tân Sửu` + thuận → **Nhâm Dần**. |
| 11 | Directional Can Chi? | One 60-Hoa-Giáp step (`jiazi_index + step) % 60`). Stem and branch stay in phase. Wrap `Quý Hợi ↔ Giáp Tý` verified live. |
| 12 | Cycle length? | **10 nominal years**: ages `start+i×10` … `+9`; years `birth_year + those ages`. Inclusive year labels `2022–2031`. |
| 13 | Start/end years? | `start_year = birth_year + start_age + i×10`; `end_year = start_year + 9`. Gregorian birth year, not BaZi year. |
| 14 | Current cycle? | **Year-level:** `age = now.year − birth_year`, then first period with `start_age ≤ age ≤ end_age`. Not birthday, not exact datetime. |
| 15 | CASE-0001 `Ất Tỵ`? | **Yes, live.** Index 3, **2022–2031**, ages **35–44**. On 2026-08-20, `age = 39`. |
| 16 | Same LuckResult across surfaces? | **Sequence + start_age + direction** match Engine → API → Golden → Report. **Current marker** is API/Portal only. Report/PDF/DOCX copy the table, do not highlight current. `shape_luck_payload` drops stem element/yin_yang. |

---

# PHASE 1 STATUS

**G1-08 PHASE 1: AUDIT PASS / G1-08 NOT READY — REPAIR REQUIRED**

Natal Đại vận **calculation for CASE-0001 is reconstructable** at the documented **year-level / integer start-age** semantics. The 15 calculation blockers in §30 **do not fire** for live CASE-0001.

G1-08 still **cannot Freeze** until Product Owner locks precision and presentation contract:

- Engine is **year-level only** (date-only jie table, birth time ignored, `round(days/3)`, `now.year − birth_year`).
- **Do not invent an exact datetime algorithm in Phase 2 unless Product Owner chooses Option B.**
- Minimum evidence row (direction + polarity + jie + start age + current) is **not** published on Portal.
- Report §09 still prints a **false gap note** claiming full cycles are missing.
- Natal direction / start-age / wrap have **no dedicated tests**.

Do not start Phase 2 in this document. Do not change the engine to preserve a UI string. Live current **is** `Ất Tỵ 2022–2031`.

---

## Product Owner decision required (do not auto-choose B)

### Option A — lock V1.0 year-level semantics (recommended default unless PO asks otherwise)

Document and freeze:

- jie = calendar-date only from `solar_term_base_dates.csv`;
- birth hour/minute unused for khởi vận;
- `3 ngày ≈ 1 năm` with `round` to integer age;
- current cycle by **calendar year age**.

### Option B — upgrade exact start datetime before Freeze

Requires a later phase: true jie timestamps, same-timezone comparison, fractional or Y/M/D age, exact giao vận datetime, current cycle by datetime. **Not started.**

---

## 1. Canonical production implementation

**Canonical natal calculator:** `engines/luck_engine/providers/dayun.py` `DefaultDayunProvider`

**Public production engine:** `engines/luck_engine/engine.py` `LuckEngine.build`

**Published contract:** `applications/api/services/luck_truth.py` `shape_luck_payload`

There is a type named `LuckResult` on `CanonicalLuckPipeline`. **That is not the production natal output.** Production natal output is:

1. `DayunPeriod` (current decade) with `metadata.sequence` = full list;
2. wrapped in `LuckContext.current_dayun`;
3. shaped to `data.luck` (`direction`, `start_age`, `current_cycle`, `cycles`).

| Piece | Path | Production? |
|-------|------|-------------|
| Entry | `OrchestratorService` stage 7 → `LuckEngine.build` | **yes** |
| Context builder | `LuckEngine.build` assembles `LuckContext` | **yes** |
| Input | Calendar object + `BaziChart` (gender, year/month pillars) | **yes** |
| Output model | `LuckContext` / `DayunPeriod` | **yes** |
| Direction | `dayun_forward(gender, year_stem)` | **yes** |
| Start-age | `compute_dayun_start_age` | **yes** |
| Cycle generator | `DefaultDayunProvider.provide` loop | **yes** |
| Current selector | same provider, `age = ref.year − birth_year` | **yes** |
| Rule/data | `STEM_META`; `SolarTermEngine` + `solar_term_base_dates.csv`; `GanzhiAlgorithm.STEM/BRANCH` | **yes** |
| Version | Dayun metadata `"sprint": "4.1"`; engine metadata `"sprint": "4.7_liushi_rule_evaluation"` | labeled, not a freeze version |

Production call:

```text
calendar + bazi
  → extract_birth_parts (Y-M-D; H:M discarded for age)
  → dayun_forward(gender, year_pillar.stem)
  → compute_dayun_start_age → 12 Tiết dates
  → step_jiazi(month pillar, ±1) × 10 decades
  → pick current by year-age
  → shape_luck_payload → data.luck
```

### Other implementations (classification)

| Kind | Path | Role |
|------|------|------|
| **Canonical production** | `LuckEngine` + `DefaultDayunProvider` | Live natal decades |
| **Presentation helper** | `shape_luck_payload`, Report §09, Portal `formatLuckCurrent` / `formatLuckSequence` | Copy payload; do not regenerate pillars |
| **Presentation helper** | `applications/production/luck_internal.py` | Extract sequence; not customer UI |
| **Unused / experimental** | `CanonicalLuckPipeline` (`engines/luck_engine/pipeline/`) | Timeline → Analysis → Decision. **Not** called from Orchestrator or `applications/` |
| **Unused** | `engines/analysis_engine/luck_engine/` | Analysis-runtime luck stage. **Not** on API path |
| **Stub** | `engines/bazi_engine/luck/interface.py` | Re-exports `engines.luck_engine` |
| **Score data** | `database/15_score_engine/08_luck/` | Scoring rules, not cycle generation |
| **Layered evaluators** | `engines/luck_engine/evaluators/` | Support/attack/strength **after** decades exist. Not the decade generator |

S10 Canonical Desktop is bone-weight UI, not Đại vận. Luck UI is S01 “Đại vận” / “Lộ trình Đại vận”.

---

## 2. Dependency graph

```text
Birth Input (Y-M-D H:M, gender, timezone label)
        │
        ▼
CalendarEngine ── solar Y-M-D H:M
        │         SolarTermEngine (shared CSV)  ← BaZi month also uses this
        ▼
BaziEngine.build(gender) ── year_pillar, month_pillar
        │
        ▼
LuckEngine.build
        │
        ├─ DefaultDayunProvider     ← natal Đại vận (this gate)
        ├─ DefaultLiunianProvider   ← năm vận (out of G1-08 depth)
        ├─ Liuyue / Liuri / Liushi
        └─ layered evaluators       ← not cát/hung customer copy
                │
                ▼
        LuckContext
                │
                ▼
        shape_luck_payload  →  data.luck
                │
        ┌───────┼────────────┐
        ▼       ▼            ▼
      Portal   Report      PDF/DOCX
               (cycles copy; no current_cycle field)
```

Luck **does not** write Calendar or BaZi. It **reads** Calendar solar date and BaZi pillars. It **reuses** Calendar `SolarTermEngine` rather than a second jie table.

---

## 3. Input fields

| Field | In request? | Read by natal Dayun? | Notes |
|-------|-------------|----------------------|--------|
| `gender` | yes | **yes** | From `bazi.gender`. Missing → `"male"`. |
| Birth solar Y-M-D | yes | **yes** | `calendar.solar_year/month/day`. |
| Birth hour/minute | yes | **extracted then discarded** | `_h, _m` unused in start-age. CASE-0001 `04:30` does not change age. |
| Timezone | yes (`Asia/Bangkok`) | **no** for jie math | Stored on Calendar; jie dates have no TZ. |
| Birthplace | yes | **no** | |
| Year stem | derived | **yes** | `year_pillar.stem` (Niên can). |
| Month pillar | derived | **yes** | First cycle origin. |
| Day stem | derived | enrichment only | Ten-god on luck pillars; **not** direction. |
| Solar terms | Calendar | **yes** | 12 Tiết via `SolarTermEngine`. |
| Lunar date | Calendar | **no** | |
| Pattern / Score / RuleContext | pipeline | **ignored** by Dayun provider (`del rule_context`) | |

---

## 4. Direction formula

Canonical function: `engines/luck_engine/providers/_common.py` `dayun_forward`.

```text
thuận  (forward)  ⇔  is_male(gender) == is_yang(year_stem)
nghịch (reverse)  ⇔  otherwise
```

`is_male_gender` treats as male: `male`, `nam`, `m`, `1` (case-insensitive). Everything else is female.

This **is** the classical rule:

- Dương nam → thuận
- Âm nữ → thuận
- Âm nam → nghịch
- Dương nữ → nghịch

Proven from `is_male == is_yang`, not assumed from commentary.

### Truth table (implementation)

| Gender | Niên can polarity | `is_male == is_yang` | Direction |
|--------|-------------------|----------------------|-----------|
| Nam | Dương | True | **thuận** / `forward` |
| Nam | Âm | False | **nghịch** / `reverse` |
| Nữ | Dương | False | **nghịch** / `reverse` |
| Nữ | Âm | True | **thuận** / `forward` |

CASE-0001: Nam + Bính (Dương) → **thuận**. Live metadata: `direction=forward`, `gender=male`, `year_stem=Bính`.

Nhật can is **not** in this formula.

---

## 5. Polarity source

Single map: `engines/bazi_engine/ten_god.py` `STEM_META` (G1-01 canonical stems). Luck calls `stem_yin_yang` → that map. **No second polarity table.**

| Thiên can | Ngũ hành | Âm/Dương |
|-----------|----------|----------|
| Giáp | Mộc | Dương |
| Ất | Mộc | Âm |
| Bính | Hỏa | Dương |
| Đinh | Hỏa | Âm |
| Mậu | Thổ | Dương |
| Kỷ | Thổ | Âm |
| Canh | Kim | Dương |
| Tân | Kim | Âm |
| Nhâm | Thủy | Dương |
| Quý | Thủy | Âm |

Unknown stem → `stem_yin_yang` returns `""` → `is_yang_stem` is False → treated as Âm. Deterministic, but an unknown stem would silently reverse for males. Production stems are the ten above.

---

## 6. Solar-term source

`compute_dayun_start_age` iterates `SolarTermEngine._MONTH_START_TERM_INDEX`:

| Index | Tiết (month start) |
|-------|-------------------|
| 0 | Lập Xuân |
| 2 | Kinh Trập |
| 4 | Thanh Minh |
| 6 | Lập Hạ |
| 8 | Mang Chủng |
| 10 | Tiểu Thử |
| 12 | Lập Thu |
| 14 | Bạch Lộ |
| 16 | Hàn Lộ |
| 18 | Lập Đông |
| 20 | Đại Tuyết |
| 22 | Tiểu Hàn |

**Not used:** 中气 (Vũ Thủy, Xuân Phân, Đại Hàn, …). CASE-0001 Đại Hàn 1987-01-20 is **ignored**.

### Thuận

Nearest jie with `term_date > birth` (`min(after)`). CASE-0001 → **Lập Xuân 1987-02-04**.

### Nghịch

Nearest jie with `term_date < birth` (`max(before)`).

### Equality

`term_date == birth` is neither `<` nor `>`. Birth **on** a jie day skips that jie. No dedicated test. Limitation, not a second algorithm.

Lunar-month boundaries are **not** used.

---

## 7. Solar-term datetime precision

Source: `engines/calendar_engine/solar_terms/data/solar_term_base_dates.csv`.

| Precision | Present? |
|-----------|----------|
| Month | yes (same every year) |
| Day | yes (same every year) |
| Hour / minute / second | **no** |
| Timezone on jie | **no** |
| Year-specific astronomy | **no** — V1.0 approximate table |

`get_term_datetime_parts(year, index)` returns `(year, csv.month, csv.day)`.

Engine distance: **whole days** via `datetime.date` subtraction. CSV timestamps are not truncated; they never had a time-of-day.

---

## 8. Timezone handling

| Clock | What production uses |
|-------|----------------------|
| Birth | Civil `solar_year/month/day` from Calendar. Request TZ `Asia/Bangkok` is a **label**. `CalendarEngine.calculate` comment: conversion **stays UTC+7**. |
| Jie | Naive `date(Y, m, d)` from CSV. No TZ. |
| Comparison | Date vs date. **Not** local birth datetime vs UTC jie instant. |
| Current cycle | `datetime.now()` naive local; **year only**. |

CASE-0001 04:30 cannot cross the civil date vs a date-only jie. Silent UTC-vs-local **hour** compare **does not occur** for start-age.

**Limitation (not a second jie engine):** true Lập Xuân 1987 may not be 04 Feb; Calendar and Luck share the same approximate table, so BaZi month and khởi vận stay consistent with each other.

**Not BLOCKER 5** for CASE-0001 (no UTC/local timestamp mix). Flag as Calendar V1.0 precision for Option A/B.

---

## 9. Start-age formula

```text
days = |jie_date − birth_date|.days     # integer days
start_age = max(1, int(round(days / 3.0)))
```

Constant: `DAYS_PER_START_AGE_YEAR = 3.0`.

| Question | Implementation |
|----------|----------------|
| 3 ngày = 1 năm? | **Yes.** |
| 1 ngày = 4 tháng? | **Not implemented.** Remainder after `/3` is only used by `round`. |
| 1 giờ = ? | **Unused.** |
| Rounding | `int(round(...))` (Python banker's round at `.5`, then `max(1, …)`). |
| Fractional age stored? | **No.** Integer only. |

CASE-0001: `days_to_jie = 14`; `14/3 = 4.666…`; `round` → **5**. Metadata `method=major_jie_days_div_3`, `anchor_jie_date=1987-02-04`.

---

## 10. Start-age representation

`DayunPeriod.start_age` / `end_age`: **integers**.

Published `data.luck.start_age`: first cycle `age_start` (integer).

`start_age_calc` metadata (days, anchor, method) lives on `current_dayun.metadata` and **is not** copied to Report `luck_cycles`.

UI “Tuổi 5” is **engine start age**, not tuổi mụ (`+1`). Current decade ages 35–44 are the same integer year-age scale (`calendar_year − birth_year`).

Calculation vs presentation: engine integer; Portal S01 **mislabels** that start age onto the **current** Đại vận row (see §18).

---

## 11. Start datetime behavior

Engine **does not** compute `birth_datetime + luck offset`.

Report field `luck_cycles.start_date` is always `""` because `shape_luck_payload` does not emit `start_date`. Report §09 shows “Ngày bắt đầu” empty / fallback.

**Limitation of V1.0:** year labels only. Do not add a datetime algorithm unless PO chooses Option B.

---

## 12. First-cycle generation

From **month pillar**, then **one JiaZi step before storing cycle 0**. Month pillar is not a luck decade.

```text
stem, branch = month_stem, month_branch
for i in 0..9:
    stem, branch = step_jiazi(stem, branch, +1 or −1)
    store cycle i
```

CASE-0001 month `Tân Sửu` (jiazi index 37) + forward → **Nhâm Dần**. Live and Golden agree.

---

## 13. 60-JiaZi progression

`step_jiazi` uses one index:

```text
index = (jiazi_index(stem, branch) + step) % 60
return STEMS[index % 10], BRANCHES[index % 12]
```

Tables: `GanzhiAlgorithm.STEM` / `BRANCH` (canonical Calendar 10×12). Luck does not keep a separate 60-JiaZi list; it reconstructs pairs from those two arrays. Invariant: stem and branch cannot drift out of phase.

Live wrap:

- `Quý Hợi + 1` → `Giáp Tý`
- `Giáp Tý − 1` → `Quý Hợi`

CASE-0001 forward sequence is consecutive +1 each decade (Nhâm Dần → … → Tân Hợi).

No dedicated pytest for wrap. Live reconstruction only.

---

## 14. Cycle boundary semantics

Each cycle lasts **10 nominal age years**, labeled as **10 civil years**.

| Field | Formula |
|-------|---------|
| `start_age` | `start_age_0 + i×10` |
| `end_age` | `start_age + 9` (inclusive 10 ages) |
| `start_year` | `birth_year + start_age` |
| `end_year` | `start_year + 9` (display `2022–2031`) |

Display range is inclusive labels, not `[start, end)` datetime.

Adjacent cycles: `…2001` then `2002…`; ages `14` then `15`. **No year overlap, no year gap** at this granularity.

Mid-year giao vận is **not modeled**. A person who “starts” a decade in March is treated as in that decade for the whole civil year once `now.year − birth_year` lands in the age band.

---

## 15. Current-cycle selection

```text
reference = datetime.now()          # unless provider injected reference_dt
age = max(0, reference.year − birth_year)
current = first period with start_age ≤ age ≤ end_age
if age < first.start_age: current stays cycle 0
if age > last.end_age: last matching loop leaves the last period
```

Not: birthday, not: exact datetime, not: tuổi mụ.

Live 2026-08-20: `age_at_reference=39`, `reference_year=2026` → period 35–44 → **Ất Tỵ**.

If giao vận is mid-year, V1.0 still uses year-age. That is Option A semantics, not a silent renderer override.

---

## 16. CASE-0001 full trace

Production input (`applications/production/fixtures/case_0001.py`):

- Nguyễn Tiến Sơn, **male**, **1987-01-21 04:30**, timezone **Asia/Bangkok**, Hà Tây
- Pillars live: **Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần**

### A. Direction

`Bính` = Hỏa **Dương** (`STEM_META`). Nam → `dayun_forward` True → **thuận** / `forward`.

### B. Solar-term reference

Thuận → next 12-jie after 1987-01-21 → **Lập Xuân 1987-02-04** (CSV). Đại Hàn 01-20 is zhongqi, unused.

### C. Delta

`(date(1987,2,4) − date(1987,1,21)).days` = **14**. Birth **04:30 ignored**.

### D. Conversion

`round(14 / 3.0) = 5`. `start_age = 5`.

### E. First cycle

`Tân Sửu` + 1 → **Nhâm Dần**. Years `1987+5=1992`–2001. Ages 5–14.

### F. Full sequence (live = Golden)

| i | GanZhi | Years | Ages |
|---|--------|-------|------|
| 0 | Nhâm Dần | 1992–2001 | 5–14 |
| 1 | Quý Mão | 2002–2011 | 15–24 |
| 2 | Giáp Thìn | 2012–2021 | 25–34 |
| 3 | **Ất Tỵ** | **2022–2031** | **35–44** |
| 4 | Bính Ngọ | 2032–2041 | 45–54 |
| 5 | Đinh Mùi | 2042–2051 | 55–64 |
| 6 | Mậu Thân | 2052–2061 | 65–74 |
| 7 | Kỷ Dậu | 2062–2071 | 75–84 |
| 8 | Canh Tuất | 2072–2081 | 85–94 |
| 9 | Tân Hợi | 2082–2091 | 95–104 |

### G. Why current is Ất Tỵ

`2026 − 1987 = 39`. `35 ≤ 39 ≤ 44`. Index 3. **UI is not the source of truth; live engine is.** Golden `luck_cycles.cycles[3]` matches.

---

## 17. Current `Ất Tỵ` verification

| Surface | Value | Source |
|---------|-------|--------|
| Engine live | Ất Tỵ, 2022–2031, 35–44, index 3 | `DefaultDayunProvider` |
| API `data.luck.current_cycle` | same | `shape_luck_payload` |
| Golden Report | same row in `cycles`; no `current_cycle` field | `expected_report_input.json` |
| Portal S01 | `formatLuckCurrent` copies `current_cycle` | no year-range recompute |
| Report §09 | table includes Ất Tỵ; **no current badge** | copies cycles |

**Verified.** Do not change the engine to chase a different UI string — live already matches `Ất Tỵ 2022–2031`.

---

## 18. Age / year-range semantics

| Label | Meaning in V1.0 |
|-------|-----------------|
| `start_age` / `age_start` | Integer year-age: `civil_year − birth_year` at decade start |
| `age_end` | `age_start + 9` |
| `year_start` / `year_end` | `birth_year + age_*` |
| Tuổi Tây vs tuổi mụ | Engine is **not** tuổi mụ. Portal “Tuổi 5” = khởi vận integer. |
| S01 tag `Tuổi {start_age}` | Printed on the **current** row (`Ất Tỵ 2022–2031`) → **semantic mix**: khởi vận 5 vs current 35–44 |

Full HTML report separates `luckStartAge` and `luckCurrent` correctly. Canonical Desktop S01 tag does not.

Year range and age range are **internally consistent** (`1987+35=2022`). They are year-age, not birthday-age.

---

## 19. Calendar dependency

Luck uses **canonical** `SolarTermEngine` (same CSV as BaZi month). **Not** a second solar-term implementation.

Risk: CSV is approximate and year-invariant. Luck and Calendar stay **aligned**; both can be astronomically off together. That is Calendar V1.0, out of G1-08 repair scope.

`bazi_year_of` exists in `_common.py` but Dayun **does not** use it for `start_year`. Labels use Gregorian `calendar.solar_year`.

---

## 20. Cross-surface binding

| Surface | Sequence | Start age | Direction | Current | Age labels |
|---------|----------|-----------|-----------|---------|------------|
| Engine | 10 cycles | 5 | `forward` | year-age pick | integers |
| API `data.luck` | copy | copy | copy | `current_cycle` | copy |
| Report / PDF / DOCX | copy cycles | copy | `forward` → **Thuận** | **not bound** | table `5 – 14` … `35 – 44` |
| Portal S01 | copy | tag **5** on current row | **not shown** | copy `Ất Tỵ 2022–2031` | mixed |
| Full report HTML | copy | `luckStartAge` | not in head line | `luckCurrent` | `current` flag via `gan_zhi` equality |

Renderers **do not** recompute `currentYear >= startYear && currentYear <= endYear` independently of Engine. Portal copies `current_cycle`.

`resultPresentationAdapter` splits current value on space and takes token `"Ất"` from `"Ất Tỵ 2022–2031"` for timeline highlight. That is a **fragile string helper**, not a second year-range formula. `fullReportViewModel` compares full `gan_zhi`.

`shape_luck_payload` **drops** `element` / `yin_yang` / `ten_god`. Portal cannot show `Ất · Mộc` / `Tỵ · Hỏa` without a new mapping or publishing metadata. **Do not implement in Phase 1.** Reuse `STEM_META` later; do not invent a renderer map.

Report §09 note:

```text
Toàn bộ đại vận (full luck cycles): DATA NOT PROVIDED BY RUNTIME
```

This is **false** when 10 cycles are in the table. Contract/presentation defect.

---

## 21. Golden comparison

`tests/golden_dataset/report_v1/CASE-0001/expected_report_input.json` `luck_cycles`:

- `direction`: `forward`
- `start_age`: `5`
- `start_date`: `""`
- 10 cycles identical to live Engine/API

**Engine = API = Golden = Report table.** Golden is **not stale** for natal decades.

Golden has **no** `current_cycle` (Report contract). Portal current is live-year dependent (`now.year`). In 2026 it matches Ất Tỵ; it will move in 2032 without Golden changing.

---

## 22. Representative direction tests

No pytest calls `dayun_forward` or `DefaultDayunProvider`. Coverage is **code inspection + live CASE-0001** only.

Formula confirmation (four groups):

| Group | Example | Result |
|-------|---------|--------|
| Dương Nam | male + Bính | thuận — **CASE-0001 live** |
| Âm Nam | male + Ất | nghịch — formula only |
| Dương Nữ | female + Bính | nghịch — formula only |
| Âm Nữ | female + Ất | thuận — formula only |

**Gap:** three of four groups untested in CI.

---

## 23. Solar-term boundary coverage

No natal Dayun tests for:

- birth immediately before jie;
- birth **on** jie (equality skipped);
- birth immediately after jie;
- delta `< 1` day (impossible with date-only except same-day, which is skipped);
- many days;
- timezone crossing midnight.

Precision **cannot** support sub-day boundaries. Report as V1.0 limitation (Option A) or upgrade (Option B).

---

## 24. Existing test coverage

| Area | Tests | Natal Dayun? |
|------|-------|----------------|
| `tests/luck_engine/` | CanonicalLuckPipeline / analysis / decision | **No** |
| `tests/analysis_luck_engine/` | Analysis-runtime luck | **No** (unused path) |
| Golden CASE-0001 | Report `luck_cycles` snapshot | **Yes** (output only) |
| `tests/production/test_p1_calendar_data_recovery.py` | `start_age == 5`, cycle count | Partial integration |
| `tests/interpretation_engine/foundation/test_sprint_a_foundation.py` | `luck.start_age == 5` | Partial |

Missing: direction matrix, 12-jie vs zhongqi, wrap, birth-on-jie, hour independence, current-year selection with injected `reference_dt`.

---

## 25. Blockers (§30 checklist)

| # | Condition | CASE-0001 / production | Verdict |
|---|-----------|------------------------|---------|
| 1 | Direction untraceable | `dayun_forward` + live metadata | **not blocker** |
| 2 | Gender/polarity non-deterministic | `STEM_META` + gender default | **not blocker** (default-male is a risk, not non-deterministic) |
| 3 | CASE-0001 current not reconstructable | Live Ất Tỵ 2022–2031 | **not blocker** |
| 4 | Different solar-term engine vs Calendar | Same `SolarTermEngine` | **not blocker** |
| 5 | Birth vs jie TZ mismatch changing age | Date-only; no UTC vs local instants | **not blocker** for this case |
| 6 | Start-age formula untraceable | `round(days/3)` documented in metadata | **not blocker** |
| 7 | First cycle wrong direction from month | Tân Sửu → Nhâm Dần forward | **not blocker** |
| 8 | GanZhi not ±1 JiaZi | `step_jiazi` mod 60 | **not blocker** |
| 9 | Renderer recomputes current ≠ Engine | Portal copies `current_cycle` | **not blocker** |
| 10 | API vs Report different current | Report has no current field; **same sequence** | **not blocker** (presentation gap) |
| 11 | Golden ≠ live | Match | **not blocker** |
| 12 | Cycle overlap/gap | Adjacent years/ages | **not blocker** at year-level |
| 13 | Datetime in two cycles / none | Year-level only; mid-year unmodeled | **limitation**, not dual membership at year grain |
| 14 | Age vs year mismatch without semantics | `year = birth_year + age` | **not blocker** |
| 15 | Legacy luck overrides canonical | Pipeline unused; shaper copies engine | **not blocker** |

**Freeze blockers (product / contract, not formula bugs):**

1. Precision not locked (Option A vs B).
2. Report false gap note.
3. Portal S01 tag conflates khởi vận with current decade.
4. No CI for direction / jie / wrap.
5. Minimum evidence presentation absent (direction, polarity, jie, start age, current).

---

## 26. Gap classification

| Class | Gaps |
|-------|------|
| **calculation** | Year-level only; `round(days/3)`; hour unused. Correct under that spec. |
| **direction** | Formula clear. Four-group CI missing. Unknown stem treated as Âm. Missing gender → male. |
| **calendar** | Shared approximate jie CSV. Astronomical error possible; Luck ≠ second theory. |
| **timezone** | Jie has no TZ. Calendar conversion labeled UTC+7. No silent UTC instant compare for start-age. |
| **boundary** | Birth on jie skipped. Sub-day unsupported. Current by year, not datetime. |
| **contract** | `LuckResult` name ≠ production natal type. `start_date` always empty. Payload drops element/yin_yang. Report has no `current_cycle`. |
| **adapter** | `shape_luck_payload` strips enrichment. Report copies cycles only. |
| **presentation** | S01 `Tuổi 5` on Ất Tỵ. No Portal direction/evidence. False FULL_LUCK_CYCLES_GAP_NOTE. Timeline `split(" ")[0]` token. |
| **test** | Natal Dayun untested except Golden output and two `start_age==5` asserts. |

---

## 27. Minimum changes required for G1-08 PASS

**Do not change Luck/Calendar formulas in Phase 2 unless PO chooses Option B.**

1. **PO lock:** Option A (year-level freeze text) or Option B (datetime upgrade — later phase, new spec).
2. If **Option A**: freeze the semantics in this audit as V1.0; do **not** add exact giao vận datetime.
3. **Presentation / contract (Option A path):**
   - Stop printing `FULL_LUCK_CYCLES_GAP_NOTE` when cycles exist.
   - Portal: show current `Ất Tỵ · 2022–2031`, age band `35–44`, khởi vận `5`, direction Thuận/Nghịch, evidence `Nam + Bính Dương + Lập Xuân 1987-02-04` — **copy engine fields**, do not recompute.
   - Do not put khởi vận age as the only tag on the current decade.
4. **Tests (no Golden rewrite unless live already matches — it does):** direction matrix (4 groups), JiaZi wrap, CASE-0001 `start_age_calc` (14 days, 1987-02-04, age 5), hour independence, injected `reference_dt` for current pick.
5. **Do not** add cát/hung / tài vận / Dụng-Hỷ-Kỵ luck interpretation.
6. **Do not** add a second polarity or JiaZi map in renderers. If elements are shown later, publish `STEM_META` from engine payload.

---

# Minimum evidence (not implemented — V1.0 target)

Compact customer line, **timeline only**:

**Đại vận hiện tại** `Ất Tỵ · 2022–2031`  
**Tuổi** `35–44` (year-age)  
**Khởi vận** `5`  
**Chiều vận** `Thuận`  
**Căn cứ** `Nam + niên can Bính (Dương) → thuận; Tiết neo Lập Xuân 1987-02-04; 14 ngày ÷ 3 ≈ 5`

No luận cát/hung in G1-08.

---

# PHASE 1 STATUS

**G1-08 PHASE 1: AUDIT PASS / G1-08 NOT READY — REPAIR REQUIRED**

STOP. No Luck Engine / Calendar / BaZi / Strength / Temperature / Pattern / Useful God / ShenSha / Portal / Report / Golden edits. No Deep Luck Interpretation. Wait for Product Owner review (Option A vs B) before Phase 2.
