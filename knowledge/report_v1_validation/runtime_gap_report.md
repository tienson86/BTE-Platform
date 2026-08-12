# Runtime Gap Report — Report V1 / CASE-0001

**Date:** 2026-08-12  
**Scope:** Audit only. No engine or Rule Database changes.

Message shown in customer report when a listed slice is absent:

```text
DATA NOT PROVIDED BY RUNTIME
```

---

## Summary

| Field | Customer report (after WP-RPT-003A) | Runtime actually has data? | Engine responsible |
|-------|-------------------------------------|----------------------------|--------------------|
| Five elements | DATA NOT PROVIDED BY RUNTIME | Partial — Score Engine series exists but adapter keys do not match | Score Engine + Report adapter mapping |
| Executive summary | Mapped from `summary` section after rule-text filter | Interpretation has a `summary` section, not `executive_summary` | Interpretation Engine |
| Wealth | DATA NOT PROVIDED BY RUNTIME | No wealth section in InterpretationView | Interpretation Engine |
| Children | DATA NOT PROVIDED BY RUNTIME | No children/tử tức section | Interpretation Engine |
| Full luck cycles | Current decade only + gap note | Full sequence exists on Luck payload, not mapped into ReportInputV1 | Luck Engine + Report adapter mapping |

`ReportInputV1` / golden snapshot were **not** changed in WP-RPT-003A (backward compatibility). Gaps below are backlog for a later mapping WP.

---

## 1. Five elements (`five_elements`)

| Item | Value |
|------|-------|
| Report field | `ReportInputV1.five_elements.{wood,fire,earth,metal,water}` |
| Desired source | Per-element counts/percentages from Score / RuleContext wuxing |
| Current source | `AnalysisResult.score.wuxing_series` |
| Engine | `engines.score_engine.engine.ScoreEngine` |
| Adapter | `ReportInputV1Adapter._build_five_elements` |

### What runtime provides

`ScoreEngine._build_wuxing_series()` emits:

```text
{"label": "Mộc"|"Hỏa"|"Thổ"|"Kim"|"Thủy", "value": <float>}
```

CASE-0001 diagnostics already list `AnalysisResult.score.wuxing_series` as a source contract, but `raw` stays `{}`.

### Why the report is empty

Adapter looks for:

```text
item["element"] or item["name"]  →  lowercase key in {wood, fire, earth, metal, water}
```

Runtime series uses `label` (Vietnamese) and does not use `element`/`name`. Mapping miss → all five values `None`.

### Must not do

- Recalculate ngũ hành in Report Engine
- Invent percentages

### Backlog

Align adapter keys to `label`/`value` (or ask Score Engine to also emit `element`). Requires an authorized golden-snapshot update.

---

## 2. Executive summary (`interpretation.executive_summary`)

| Item | Value |
|------|-------|
| Report field | `ReportInputV1.interpretation.executive_summary` |
| Desired source | Commercial summary paragraph from Interpretation |
| Current source | Empty string; section `id=summary` title `Tổng quan` exists |
| Engine | `engines.interpretation_engine` via `InterpretationView` |

### CASE-0001

- `executive_summary` = `""`
- Section `summary` contains Rule Engine instructions plus one conclusion line: `Tổng quan: Nhật Chủ Canh, cách cục Chinh An.`

WP-RPT-003A maps the `summary` section at **render time**, filters instructional sentences, and keeps the conclusion line. If nothing remains: `Chưa có dữ liệu tổng hợp.`

### Backlog

Interpretation Engine should emit a real `summary` / `executive_summary` customer paragraph (not rule-activation text). Report must not invent it.

---

## 3. Wealth (`interpretation` domain `wealth` / `tai_van`)

| Item | Value |
|------|-------|
| Report section | 12. Tài vận |
| Desired source | Interpretation section `wealth` / `tai_van` / `tài` |
| Current source | Absent from CASE-0001 InterpretationView sections |
| Engine | Interpretation Engine (sentence library / section builder) |

No wealth sentence is selected for CASE-0001. Report shows `DATA NOT PROVIDED BY RUNTIME`. Do not synthesize tài vận from Thập thần.

---

## 4. Children (`interpretation` domain `children` / `tu_tuc`)

| Item | Value |
|------|-------|
| Report section | 15. Tử tức |
| Desired source | Interpretation section `children` / `tu_tuc` / `con` |
| Current source | Absent |
| Engine | Interpretation Engine |

Same treatment as wealth. Do not infer children from Thần sát or Thập thần.

---

## 5. Full luck cycles (`luck_cycles.cycles`)

| Item | Value |
|------|-------|
| Report field | `ReportInputV1.luck_cycles.cycles` (full decade list) plus `direction`, `start_age`, `start_date` |
| Desired source | Full Đại vận sequence from Luck Engine |
| Current mapped source | `LuckContext.current_dayun` only (one decade: Ất Tỵ 2022–2031, age 35–44) |
| Engine | `engines.luck_engine` (`DefaultDayunProvider`) |

### What runtime already computes

`DefaultDayunProvider.provide()` builds the full sequence and stores it on:

```text
current_dayun.metadata.sequence
```

Direction lives on period metadata (`forward` / `reverse`), not on `LuckContext.metadata.direction`.

### Why the report shows one row

Adapter looks for:

```text
luck.metadata.dayun_periods
luck.metadata.cycles
luck.dayun_periods
```

Those keys are empty. Fallback: single `current_dayun`. `direction` / `start_age` / `start_date` stay empty.

### Must not do

- Recalculate Đại vận in Report Engine
- Change Luck algorithm

### Backlog

Map `current_dayun.metadata.sequence` → `luck_cycles.cycles` and direction/start_age from period metadata. Requires authorized snapshot update.

---

## 6. Related thin slices (not in the five named gaps)

| Slice | Observation | Engine |
|-------|-------------|--------|
| Recommendations | Empty | Interpretation |
| `calendar.calendar_mode` | Empty | Calendar shaping |
| `calendar.solar_term` | Dict object in contract (`{'name': 'Đại Hàn', 'index': 23}`) | Calendar → adapter `str()` |
| Pattern `secondary_patterns` | Duplicates `primary_pattern` (Chính Ấn) | Pattern view mapping |
| Useful god reasoning | `Than vượng cần tiết khí` (typo / internal phrasing) | Useful God Engine |
| Summary text `Chinh An` | Missing diacritics vs `Chính Ấn` | Interpretation sentence |

These stay as diagnostics. WP-RPT-003A only unwraps `solar_term` at **display** time.

---

## 7. ShenSha duplicate candidates (ISSUE-006)

Present together in CASE-0001, **not merged**:

| Pair | Status |
|------|--------|
| Thiên Ất / Thiên Ất Quý Nhân | Duplicate candidate |
| Thiên Đức / Thiên Đức Quý Nhân | Duplicate candidate |
| Nguyệt Đức / Nguyệt Đức Quý Nhân | Duplicate candidate |

May be aliases or distinct entries. Rule Database confirmation required. Report Engine must not merge by guesswork.
