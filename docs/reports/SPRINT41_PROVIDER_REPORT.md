# Sprint 4.1 Provider Report

| Item | Value |
|------|-------|
| Document | `SPRINT41_PROVIDER_REPORT.md` |
| Project | BTE Platform V1.0 |
| Sprint | Sprint 4.1 — Luck Data Providers |
| Prerequisite | `SPRINT4_FOUNDATION_REPORT.md` |
| Case | Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh |
| Date | 2026-07-28 |
| Scope | **Runtime data providers only** — no evaluation / scoring / interpretation |

---

# Objective

Populate `LuckContext` with immutable runtime pillars:

| Layer | Provider | Role |
|-------|----------|------|
| Đại vận | `DefaultDayunProvider` | Decade sequence + current pillar |
| Lưu niên | `DefaultLiunianProvider` | Annual pillar |
| Lưu nguyệt | `DefaultLiuyueProvider` | Monthly pillar + solar term |
| Lưu nhật | `DefaultLiuriProvider` | Daily pillar (calendar conversion) |
| Lưu thì | `DefaultLiushiProvider` | Hourly pillar (calendar conversion) |

**Explicitly out of scope:** favorable/unfavorable luck, Pattern/Useful God comparison, support/attack levels, luck scores, interpretation narrative.

---

# Implemented providers

| Class | File | Output model |
|-------|------|--------------|
| `DefaultDayunProvider` | `engines/luck_engine/providers/dayun.py` | `DayunPeriod` |
| `DefaultLiunianProvider` | `engines/luck_engine/providers/liunian.py` | `LiunianPeriod` |
| `DefaultLiuyueProvider` | `engines/luck_engine/providers/liuyue.py` | `LiuyuePeriod` |
| `DefaultLiuriProvider` | `engines/luck_engine/providers/liuri.py` | `LiuriPeriod` |
| `DefaultLiushiProvider` | `engines/luck_engine/providers/liushi.py` | `LiushiPeriod` |

Shared helpers: `engines/luck_engine/providers/_common.py`

`LuckEngine` now installs default providers when `use_default_providers=True` (default). Orchestrator keeps `LuckEngine()` — no upstream engine changes.

---

# Runtime models

Immutable (`@dataclass(frozen=True, slots=True)`) in `engines/luck_engine/models.py`:

### DayunPeriod

| Field | Description |
|-------|-------------|
| `index` | Decade order 0..n |
| `start_age` / `end_age` | Age window |
| `start_year` / `end_year` | Civil year window |
| `heavenly_stem` / `earthly_branch` | Can Chi |
| `element` / `yin_yang` | From stem meta |
| `ten_god` | Relation to Nhật Chủ (label only) |
| `hidden_stems` | Branch tàng can |
| `metadata` | Sequence, direction, start-age calc |

### LiunianPeriod

`year`, `ganzhi`, stem/branch, element, yin/yang, ten_god, hidden_stems, metadata (`nearby_years`)

### LiuyuePeriod

`year`, `month`, `month_index`, `ganzhi`, `solar_term`, element, yin/yang, ten_god, hidden_stems, metadata (`year_months`)

### LiuriPeriod / LiushiPeriod

Civil date/time + ganzhi enrichment; conversion only (Julian day / Ngũ Thử Độn).

---

# Dayun algorithm (data generation)

| Step | Rule |
|------|------|
| Direction | Male⊕yang year stem / female⊕yin → forward; else reverse |
| Start age | Days to adjacent major Tiết (`SolarTermEngine`) ÷ 3, round, min 1 |
| Sequence | Step ±1 from month pillar on 60-jiazi; 10 decades |
| Current | Decade covering age at reference year (`datetime.now()` by default) |

Case start-age calc: **14 days** to Lập Xuân 1987-02-04 → **start_age = 5**, direction **forward**.

---

# Modified / new files

| File | Change |
|------|--------|
| `engines/luck_engine/models.py` | **NEW** — runtime period models |
| `engines/luck_engine/providers/__init__.py` | **NEW** |
| `engines/luck_engine/providers/_common.py` | **NEW** — shared conversion helpers |
| `engines/luck_engine/providers/dayun.py` | **NEW** |
| `engines/luck_engine/providers/liunian.py` | **NEW** |
| `engines/luck_engine/providers/liuyue.py` | **NEW** |
| `engines/luck_engine/providers/liuri.py` | **NEW** |
| `engines/luck_engine/providers/liushi.py` | **NEW** |
| `engines/luck_engine/engine.py` | Default providers; sprint metadata `4.1_providers` |
| `engines/luck_engine/context.py` | Nested `to_dict` serialization |
| `engines/luck_engine/__init__.py` | Export models + default providers |

**Not modified:** Calendar, BaZi, Score, Pattern, Interpretation, Report, Rule Database, frontend, tests, Golden Dataset.

---

# Pipeline validation

Case: Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh

| Check | Result |
|-------|--------|
| Pipeline completes | **PASS** |
| `payload.luck.available` | **PASS** — `true` |
| `current_dayun` | **PASS** — Ất Tỵ · ages 35–44 · years 2022–2031 · 10-pillar sequence |
| `current_liunian` | **PASS** — Bính Ngọ (BaZi year 2026) |
| `current_liuyue` | **PASS** — Ất Mùi · solar_term Tiểu Thử |
| `current_liuri` | **PASS** — day ganzhi present |
| `current_liushi` | **PASS** — hour ganzhi present |
| Evaluation fields empty | **PASS** — support/attack empty; stage/strength/summary/`confidence` null |
| Score unchanged | **PASS** — `total_score=55.25` |
| No interpretation of luck | **PASS** — no luck_summary / favorable flags |

### Sample current Dayun (case)

```text
Ất Tỵ | Mộc Âm | Chính Tài | hidden [Bính, Mậu, Canh]
start_age=35 end_age=44 | 2022–2031 | index=3
```

### Tests executed

| Suite | Result |
|-------|--------|
| `pytest tests/score -q` | **38 passed** |

---

# Remaining work (Sprint 4.2+)

| Item | Status |
|------|--------|
| Support / Attack evaluators | Not implemented |
| Luck stage / strength / summary | Not implemented |
| Favorable vs unfavorable vs Pattern / Useful God | Not implemented |
| Score `luck_score` from matched luck rules | Not implemented |
| Interpretation / Report luck narrative sections | Not implemented |
| Frontend Đại vận binding | Not implemented |

---

# Sprint 4.2 readiness

**YES**

Providers produce stable immutable runtime objects inside `LuckContext`. Sprint 4.2 can inject `SupportEvaluator` / `AttackEvaluator` / `LuckEvaluator` without changing pipeline order or regenerating pillars.

---

END
