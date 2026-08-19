# G1-02 — Strength Repair Report

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-02 Phase 2 |
| **Date** | 2026-08-19 |
| **Canonical production** | `engines/strength_engine` |
| **Not used as Điểm thân** | `score.strength_score` (Score Engine contribution) |
| **Status** | FINAL FREEZE READY |

No Strength formula change. No Score Engine calculation change. No Temperature / Pattern / Useful God / Ten Gods / ShenSha / Luck / Narrative rewrite. No Deep Interpretation. Taxonomy remains `weak` / `balanced` / `strong`.

---

## 1. Adapters repaired

Semantic binding only. Score Engine still emits `score.strength_score`; adapters no longer use it for any field labeled Điểm thân / Strength / Nhật chủ strength.

| Surface | File | Before | After |
|---------|------|--------|-------|
| Canonical helper | `applications/customer_portal/src/adapters/canonicalStrength.ts` | *(new)* | Reads `data.strength.strength_score` only |
| Canonical Desktop S01 / S02 / S05 | `canonicalDesktopAdapter.ts` | Preferred `data.score.strength_score` (`45.0`); S05 could show `51.25 / D+` | `readCanonicalStrengthScore` → display `0.87`; meter percent is presentation-only |
| BaZi Strength card | `baziResultAdapter.ts` `mapStrength` | Fallback to Score 0–100 | Canonical 0–1; `maxScore: 1` |
| Portal Technical Info | `liveAnalysisResultAdapter.ts` `pickStrengthScore` | Could bind Score | Canonical formatted `0.87`; label still **Điểm thân** |
| Full Report HTML | `fullReportViewModel.ts` | Mixed | `strengthScore` = canonical `0.87`; `strengthEvidence` from `evidence_compact` |
| Legacy HTML gauge | `static/js/report/report_model.js` `strengthGaugeValue` | `score.strength_score` / `body_strength_score` / `than_score` | `payload.strength.strength_score` only |
| Legacy metrics | `static/js/report/metrics.js` | Displayed Score 0–100 as **Điểm Thân** | Display `0.87`; source `chart_source_strength` |
| Legacy gauge SVG | `static/js/report/charts.js` `gauge()` | Text = 0–100 integer | If value ∈ `[0,1]`, arc = `n*100`, **text = 0.87** |
| Production appendix | `applications/production/orchestrator.py` | Score-style class string | `strength_level_label()`; Điểm thân = `strength.strength_score` |
| Report V1 | `engines/report_engine/adapters/report_input_v1_adapter.py` | Already `analysis.strength` | Unchanged (already canonical) |

Presentation conversion (meter/gauge only): `0.87 → 87%` bar width. Canonical payload remains `0.87`. Nothing writes `87` back into analysis.

---

## 2. Field before / after

| Semantic | Before (CASE-0001 live) | After |
|----------|-------------------------|-------|
| Điểm thân | `45.0` (Score) and/or `51.25 / D+` (overall) on Desktop S05 | `data.strength.strength_score` = **0.87** |
| Phân loại | Mix of Pattern `than_vuong_nhuoc` and Strength | `data.strength.strength_level` = **strong** → **Thân vượng** |
| Confidence | `1.0` (not shown as Điểm thân) | Unchanged `1.0` |
| Score Engine than module | `score.strength_score` = `45.0` labeled like Điểm thân | Same number, relabeled **Điểm module thân (Score)** / **Module thân (Score)** |
| Score overall | `51.25` / `D+` | Unchanged; remains **Điểm tổng / Hạng điểm**, not Điểm thân |

Canonical V1.0 class labels (engine + Portal):

| `strength_level` | Label |
|------------------|-------|
| `weak` | Thân nhược |
| `balanced` | Thân cân bằng |
| `strong` | Thân vượng |

`strength_class` is not a separate contract field. Equivalent canonical field is `strength.strength_level`.

---

## 3. CASE-0001 output before / after

Live chart: Nguyễn Tiến Sơn, 1987-01-21 04:30, Nhật chủ Canh.

| Item | Engine (unchanged) | Presentation before | Presentation after |
|------|--------------------|---------------------|--------------------|
| Raw | `37` | not shown | `raw_total=37` on StrengthView; evidence reconstructs 37 |
| Normalized | `0.87` = `(37 + 50) / 100` | Desktop often `45.0` or `51.25 / D+` | **0.87** on Desktop, Portal, Report, PDF source, DOCX source, legacy gauge text |
| Class | `strong` | Thân vượng (class was already Strength/Pattern) | **Thân vượng** |
| Confidence | `1.0` | 1.0 | **1.0** |

Matched rules (unchanged): `sea_002 +25`, `root_003 +12`, `sup_001 +8`, `ctl_001 −10`, `ctl_006 −8`, `spc_004 +10`.

---

## 4. Score Engine field semantics

Score Engine calculation was **not** modified.

`score.strength_score` remains the Score module contribution (CASE-0001: `45.0`). It is still used by Score presenters under:

- `score.cat_than` → **Module thân (Score)**
- `score.than` → **Điểm module thân (Score)**

It must not appear under:

- Điểm thân
- Điểm Thân
- Strength (Nhật chủ)
- Thân vượng/nhược score

Overall `total_score` / `grade` (`51.25` / `D+`) stay on Score surfaces (`score_total`, `score_grade`, Điểm tổng hợp). They are not Điểm thân.

---

## 5. Evidence path

No new Report V1 contract field (avoids Golden Dataset churn). Compact evidence is additive on `StrengthResult` / `StrengthView`:

```text
data.strength.evidence_compact
```

Built from already-matched rules (`engines/strength_engine/evidence.py` `compact_evidence`). Does not rescore.

CASE-0001 live:

```text
Tướng địa theo tháng +25 · Có căn khí +12 · Đồng hành trợ thân +8 · Bị Quan Sát khắc -10 · Có Thất Sát -8 · Ấn mùa lạnh +10
```

| Product example | Live rule reason | Points |
|-----------------|------------------|--------|
| Tướng | Tướng địa theo tháng | +25 |
| Thông căn | Có căn khí | +12 |
| Đồng hành | Đồng hành trợ thân | +8 |
| Khắc chế | Bị Quan Sát khắc + Có Thất Sát | −10 −8 = −18 |
| Ấn mùa lạnh | Ấn mùa lạnh | +10 |

Raw reconstruction: `25 + 12 + 8 − 10 − 8 + 10 = 37`. Also published as `data.strength.raw_total`.

Trace path (unchanged diagnostics): `StrengthResult.metadata["trace"]["scoring"]["raw_total"]` and `matched_rules`.

Portal S05 / Full Report show this compact line. Report V1 PDF/DOCX keep existing `summary` / score / level; they do not add Deep Interpretation.

---

## 6. Threshold test result

Source: `tests/strength/test_thresholds.py` against `database/12_strength` level rules. Thresholds **not** changed.

| Sample | Class |
|--------|-------|
| `0.35` (weak upper, inclusive) | `weak` |
| `0.349` (just below) | `weak` |
| `0.351` (just above) | `balanced` |
| `0.649` (just below strong) | `balanced` |
| `0.65` (strong lower, inclusive) | `strong` |
| `0.651` (just above) | `strong` |
| `0.0` / `0.50` / `1.0` | `weak` / `balanced` / `strong` |

Taxonomy set is exactly `{weak, balanced, strong}`. No gap or overlap on sampled boundaries. **PASS.** Did not design new thresholds.

---

## 7. Portal result

Binding regression fixture (mandatory): `strength.strength_score = 0.87` and `score.strength_score = 45.0` plus `total_score = 51.25` / `grade = D+`.

| Surface | Điểm thân |
|---------|-----------|
| Canonical Desktop S05 | **Thân vượng** / **0.87** (bar 87% presentation-only) |
| Technical Info `strength_score` | **0.87** |
| Full Report | **0.87** |
| BaZi Strength card | **0.87** / max `1` |
| Legacy HTML **Điểm Thân** | canonical `strength.strength_score`; gauge text **0.87** |

Not shown under Điểm thân: `45.0`, `51.25`, `D+`.

---

## 8. Report / PDF / DOCX result

Report V1 was already bound to `analysis.strength`. Not rewritten.

| Format | Binding | CASE-0001 |
|--------|---------|-----------|
| Report input | `ReportInputV1.strength.score` | `0.87`; `level=strong`; `classification=strong` |
| HTML (PDF source) | section `04. Thân vượng nhược`, field **Điểm** | `0.87` + **Thân vượng** |
| PDF | same presented report as HTML | same `0.87` |
| DOCX | same `meta_rows` in tables | `0.87` + **Thân vượng** in table cells |

Score overall `51.25 — hạng D+` may still appear in a later Score section. That section is not labeled Điểm thân.

---

## 9. Test result

Module tests only (not full project).

| Suite | Result |
|-------|--------|
| `pytest tests/strength tests/report_engine/test_g1_02_strength_binding.py -q` | **24 passed** |
| Portal vitest `g1_02_strength_binding` + `canonical_desktop_adapter` + `canonical_result_routing` + `full_report_composition` | **32 passed** (4 files) |

New tests:

- `tests/strength/test_case_0001.py` — raw 37, score 0.87, class strong, label Thân vượng, confidence 1.0
- `tests/strength/test_thresholds.py` — 3-class taxonomy + boundaries
- `tests/report_engine/test_g1_02_strength_binding.py` — Report / HTML / DOCX / legacy gauge source
- `applications/customer_portal/tests/js/g1_02_strength_binding.test.ts` — adapter prefers 0.87 over 45.0 / 51.25 / D+

---

## 10. Remaining issues

Non-blocking. Do not reopen G1-02 for these.

| Item | Notes |
|------|-------|
| Narrative evidence unit | `engines/narrative_engine/runtime/input_adapter.py` still lists `source_path="strength\|score.strength_score"` as an existence probe. Not a Điểm thân UI field. Narrative was out of G1-02 repair scope. |
| Score module still shows 45.0 | Correct, under **Module thân (Score)**. |
| Report V1 label is **Điểm** inside **04. Thân vượng nhược** | Same semantic as Điểm thân; value is canonical 0.87. |
| Compact evidence wording | Uses rule `reason` text, not the shorthand “Tướng / Thông căn / Khắc chế −18”. Points and total match. Grouping −18 is presentation-optional, not a new contract. |
| Desktop fixture `strength_score: 78` | Existing non-CASE fixture on the Strength field (0–100). Meter treats `>1` as already-percent. Live CASE-0001 is 0.87. |
| Static `docs/reports/ui_sprint03_metrics/preview/*.html` | Frozen preview HTML, not live analysis. |
| Additive StrengthView fields | `evidence_compact`, `raw_total`, `combination_score`, `special_score` are extras. Normalization formula unchanged. |

---

## Formula lock (unchanged)

```text
raw_total = sum(matched rule scores)
strength_score = (raw_total + 50) / 100   # clamped 0–1
CASE-0001: (37 + 50) / 100 = 0.87
```

Classification remains `database/12_strength` 3-class rules (`weak` ≤ 0.35 inclusive, `balanced` between, `strong` ≥ 0.65 inclusive).

Stop: do not start G1-03. Do not edit Temperature, Pattern, Useful God, Ten Gods, ShenSha, Luck, or Narrative.

G1-02 STATUS: FINAL FREEZE READY
