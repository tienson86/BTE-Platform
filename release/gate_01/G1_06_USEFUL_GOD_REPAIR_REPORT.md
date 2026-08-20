# G1-06 — Useful God Repair Report

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-06 Phase 2 |
| **Date** | 2026-08-20 |
| **Product decisions** | A = Option B (explicit Ten God + stem + element). B = read G1-04 `climate_state` |
| **Canonical production** | `UsefulGodEngine` V2 (`database/13_useful_god`) |
| **Status** | FINAL FREEZE READY |

No Temperature Engine calculation change. No Strength / Pattern / Ten Gods / Five Elements formula change. Group priorities unchanged (season 90 / strength 80 / temperature 70 / flow 60). Golden Dataset not edited.

---

## 1. Old vs new Temperature input

Exact layer that classified score as heat: `TemperatureResult.useful_god_temperature_overlay()` in `engines/temperature_engine/models.py`.

Orchestrator / production runner already called this method into `PatternContext.temperature_type`. The bug was inside the overlay, not the call site.

| Input | Before (frozen G1-04) | After (G1-06) |
|-------|------------------------|---------------|
| Method | `score ≥ 0.65 → hot`; `≤ 0.35 → cold` | `to_pattern_temperature_type()` = `climate_state` |
| CASE-0001 score | `0.72` (imbalance intensity) | unchanged `0.72` |
| CASE-0001 published climate | `cold` / warming | `cold` / warming |
| Useful God `temperature_type` | **`hot`** | **`cold`** |
| TemperatureEngine.calculate | not edited | not edited |

Regression: same chart, score `0.72`, climate `cold`, Useful God context receives `cold`. Overlay is no longer a hot/cold axis on the score.

---

## 2. Old vs new candidate set (CASE-0001)

Live re-evaluation after overlay + flow predicate repair. Winner was not pre-seeded.

Internal `element_distribution` (stems + hidden, not customer 19-count): `{Hỏa: 4, Kim: 3, Thổ: 5, Mộc: 2, Thủy: 1}` sum **15**. Unique maximum = **Thổ 5**.

### Before (Phase 1 audit)

| Rule | Group | Group priority | Token | Ten God / stem / element (G1-01) | Match | Why |
|------|-------|----------------|-------|----------------------------------|-------|-----|
| `str_004` | strength | 80 | Thực Thần | Thực Thần / Nhâm / Thủy | matched | `strength_level == strong` |
| `tmp_002` | temperature | 70 | Quý | Thương Quan / Quý / Thủy | matched | overlay **hot** |
| `flo_001` | flow | 60 | Canh | Tỷ Kiên / Canh / Kim | matched | key `Mộc` exists |
| `flo_002` | flow | 60 | Nhâm | Thực Thần / Nhâm / Thủy | matched | key `Hỏa` exists |
| `flo_003` | flow | 60 | Đinh | Chính Quan / Đinh / Hỏa | matched | key `Kim` exists |
| `flo_004` | flow | 60 | Mậu | Thiên Tài / Mậu / Thổ | matched | key `Thủy` exists (count **1**) |
| `sea_001` | season | 90 | Bính | Thất Sát / Bính / Hỏa | **no** | overlay was hot, not cold |
| `tmp_001` | temperature | 70 | Đinh | Chính Quan / Đinh / Hỏa | **no** | overlay was hot |

Winner: **`str_004` → Thực Thần** (group 80 beats 70 and 60).

### After

| Rule | Group | Group priority | Token | Ten God | Stem | Element | Rule priority | Score | Evidence | Status |
|------|-------|----------------|-------|---------|------|---------|---------------|-------|----------|--------|
| `sea_001` | season | **90** | Bính | Thất Sát | Bính | Hỏa | 90 | 0.90 | winter + cold | **matched / winner** |
| `str_004` | strength | 80 | Thực Thần | Thực Thần | Nhâm | Thủy | 76 | 0.77 | `strength_level == strong` | matched / lost |
| `tmp_001` | temperature | 70 | Đinh | Chính Quan | Đinh | Hỏa | 86 | 0.87 | `temperature_type == cold` | matched / lost |
| `tmp_002` | temperature | 70 | Quý | Thương Quan | Quý | Thủy | 86 | 0.87 | requires hot | **not matched** |
| `flo_001`–`flo_004` | flow | 60 | — | — | — | — | 74 | 0.76 | unique-max is Thổ; no `flo_*` for Thổ; Thủy 1 is not unique-max | **not matched** |
| Pattern / `spc_*` | special | 100 | — | — | — | — | — | — | CASE-0001 `chinh_an` is not tòng/chuyên in UG special list | **not matched** |

Matched set is deterministic: `str_004`, `sea_001`, `tmp_001`. Resolver: group 90 > 80 > 70.

---

## 3. Flow predicate bug

CSV `04_flow_rules.csv` uses `element_distribution contains <Hành>` with reason `… quá thịnh`. Matcher treated `contains` on a dict as **key presence**.

`Thủy: 1` matched `flo_004` (“Thủy quá thịnh”) only because key `Thủy` existed.

CSV defines **no numeric cutoff**. Threshold was not invented (`>= 3` was not added). Predicate now evaluates **relative unique maximum**: the named element’s numeric count must be strictly greater than every other stored count. Ties are not unique-max. List `contains` (Ấn/Quan membership) is unchanged.

| Rule | Old behavior | Corrected behavior | CASE-0001 |
|------|--------------|--------------------|-----------|
| `flo_001` Mộc | key exists | unique-max Mộc | no (Mộc 2, max Thổ 5) |
| `flo_002` Hỏa | key exists | unique-max Hỏa | no (Hỏa 4 < Thổ 5) |
| `flo_003` Kim | key exists | unique-max Kim | no |
| `flo_004` Thủy | key exists even at 1 | unique-max Thủy | no |
| Thổ | no rule | n/a | unique-max unused |

Rule content / priorities / scores were not edited.

---

## 4. CASE-0001 winner before / after

| | Before | After |
|--|--------|-------|
| Winner rule | `str_004` | **`sea_001`** |
| Legacy token | Thực Thần | **Bính** |
| Display | (bare string) | **Hỏa · Bính · Thất Sát** |
| Compatibility hold | n/a | **not kept** — Product Owner accepted new canonical winner |

---

## 5. Winner rationale (`sea_001 → Bính`)

- **Why:** `season == winter` and `temperature_type == cold` after overlay reads G1-04 climate. Rule reason: “Mùa đông hàn cần hỏa”.
- **Priority:** group **season 90** (CSV `pri_002`). Beats strength 80 and temperature 70. Group ladder not changed.
- **Upstream evidence:** month branch **Sửu** → winter; climate_state **cold**; balancing need **warming** (Điều hậu, separate field). Strength still **strong / 0.87**. Pattern still **Chính Ấn**.
- **Ten God vs Canh / vs old Thực Thần:** G1-01 Canh (Kim Dương) × Bính (Hỏa Dương) = **Thất Sát**, element **Hỏa**. Old winner Thực Thần was Canh × Nhâm = Thủy. Output is not forced to keep Thực Thần.
- **Hỏa as Dụng** is true because `sea_001` selected Bính, **not** because Điều hậu `Cần ôn ấm` was mapped to Dụng thần Hỏa.

---

## 6. Ten God / Stem / Element mapping

No Useful God mapping table. Reverse/forward lookup reuses G1-01 `engines/bazi_engine/ten_god.py` (`ten_god_name`, new `stem_for_ten_god`, `stem_element`).

Day Master **Canh**:

| Ten God | Stem | Element |
|---------|------|---------|
| Thực Thần | Nhâm | Thủy |
| Thương Quan | Quý | Thủy |
| Tỷ Kiên | Canh | Kim |
| Kiếp Tài | Tân | Kim |
| Thất Sát | Bính | Hỏa |
| Chính Quan | Đinh | Hỏa |
| Thiên Tài | Giáp | Mộc |

CSV tokens may be a stem (`Bính`) or a Ten God (`Thực Thần`). Resolver handles both polarities. Presentation copies engine-built `useful_display` / role lists. Portal/Report do not derive Can/Hành.

---

## 7. Hỷ / Kỵ result

Still copied from the **winning CSV row** (canonical V1.0). Not recomputed by a new Hỷ/Kỵ engine.

Winner is now `sea_001`, so Hỷ/Kỵ follow that row (not `str_004`).

| Role | CSV tokens | Enriched display |
|------------------|------------------|
| Hỷ | Bính, Đinh, Giáp | `Hỏa · Bính · Thất Sát / Hỏa · Đinh · Chính Quan / Mộc · Giáp · Thiên Tài` |
| Kỵ | Nhâm, Quý | `Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan` |

Legacy arrays `favorable_gods` / `unfavorable_gods` remain. Rich fields are the display source.

---

## 8. Cross-surface result

| Surface | Dụng | Hỷ | Kỵ | Điều hậu |
|---------|------|----|----|----------|
| API `data.useful_god` | `Hỏa · Bính · Thất Sát` (`useful_display`); token `Bính` | enriched display | enriched display | TemperatureView `cold` / `warming` |
| Report V1 / HTML / PDF / DOCX | same `useful_display` | same | same | section 07 climate rows, separate from Dụng |
| Portal Desktop S02 / Full Report / BaZi adapter | copy `useful_display` | copy `favorable_display` | copy `unfavorable_display` | S01 climate rows |

Renderers do not reverse-map Ten God → stem. Điều hậu is not shown as Dụng unless UG rules actually select that god (here they do, via `sea_001`).

---

## 9. Tests

Module tests only (not full pytest).

| Suite | Result |
|-------|--------|
| `pytest tests/useful_god -q` | **18 passed** |
| `pytest tests/temperature/test_g1_04_temperature_binding.py` | **PASS** (overlay now `cold`) |
| `pytest tests/five_elements/test_g1_05_five_elements_binding.py` | **PASS** (19-count unchanged; UG assertion updated to new winner) |
| `pytest tests/report_engine/test_g1_04_temperature_binding.py tests/report_engine/test_g1_06_useful_god_binding.py` | **PASS** |
| `pytest tests/report_engine/test_html_report_v1.py` | **PASS** |
| Portal `g1_04` / `g1_05` / `g1_06` vitest | **9 passed** |
| Portal `canonical_desktop_adapter.test.tsx` | **PASS** |

Regression matrix covered: CASE-0001 frozen upstream; strong; weak; cold; hot; flow below unique-max; flow above unique-max; seasonal vs strength; seasonal vs temperature; equal-priority tie; G1-01 mapping; API/Report/HTML/DOCX consistency.

### Remaining failure (not edited)

None for Useful God canonical CASE-0001. Golden `expected_report_input.json` is synchronized to live `sea_001` / `Hỏa · Bính · Thất Sát`.

Historical Phase 1 audit docs and unrelated Ten God occurrences (WP4.5 coverage, G1-01 mapping tables) were left unchanged.

---

## 10. Remaining V1.1 backlog

- Flow CSV still has no numeric cutoff; unique-max is the documented V1.0 meaning of `quá thịnh`.
- CSV still mixes stem tokens and Ten God tokens; engine now normalizes both via G1-01.
- Hỷ/Kỵ remain winner-row copies (not independent selection).
- Internal UG tally remains 15; customer widget remains G1-05 19-count. Do not merge.
- Interpretation composer copies `useful_display` into strategy text; no Deep Useful God narrative.
- Do not start G1-07 in this gate.

---

## Files changed (source + G1-06 tests)

Engine / API / Report: `engines/temperature_engine/models.py`, `engines/bazi_engine/ten_god.py`, `engines/useful_god_engine/{matcher,models,engine,roles}.py`, `applications/api/models/analysis_result.py`, `applications/api/services/{orchestrator,useful_god_truth}.py`, `applications/production/interpretation/useful_god_composer.py`, `engines/report_engine/{contracts/report_input_v1.py,adapters/report_input_v1_adapter.py,rendering/report_sections_v1.py}`.

Portal: `canonicalUsefulGod.ts`, `canonicalDesktopAdapter.ts`, `baziResultAdapter.ts`, `fullReportViewModel.ts`.

Tests added: `tests/useful_god/test_g1_06_useful_god_binding.py`, `tests/report_engine/test_g1_06_useful_god_binding.py`, `applications/customer_portal/tests/js/g1_06_useful_god_binding.test.ts`. Overlay freeze assertions in G1-04/G1-05 live tests updated to the new canonical winner.

Not changed: Temperature calculate, Strength, Pattern, Ten Gods formula, Five Elements count, Useful God CSV priorities.

---

**G1-06 STATUS: FROZEN FOR BTE V1.0**
