# G1-04 — Temperature / Điều hậu Repair Report

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-04 Phase 2 |
| **Date** | 2026-08-19 |
| **Product decision** | Option B — minimal canonical Điều hậu layer |
| **Canonical production** | `engines/temperature_engine` |
| **Score semantic** | Case 2 — imbalance / intensity (not a cold→hot axis) |
| **Status** | FINAL FREEZE READY |

No Deep Điều Hậu. No Useful God Engine / CSV edit. No Strength formula change. No Pattern identification change. No Ten Gods change.

Semantic lock:

```text
Season / Climate → Climate State → Balancing Need / Điều hậu
≠ Overall Useful God
```

---

## 1. Semantic of score 0.72 before repair

`temperature_score` was never a 0=cold / 1=hot axis.

CASE-0001 live value `0.7166…` came from:

```text
normalized = (sum(matched rule points) / divisor + baseline) / scale
          = (raw_total / 3 + 35) / 100
```

Matched CASE-0001 contributions (audit Phase 1) included **cold** season/climate points (`sea_002`, `cli_002`, `cli_006`, `sea_006`) and **dry** points (`dry_001`, `dry_003`, `dry_004`). Those points are **added**. A high total therefore means **more matching climate-imbalance magnitude**, not “hotter”.

Component fields `warm_score` / `cold_score` exist, but the published total mixed every `score` column (including dryness) into one 0–1 number.

**Verdict:** the score measures **imbalance / intensity** (aggregate rule magnitude + baseline). It does not measure heat direction.

---

## 2. Root cause of `cold → hot`

Two facts were both true on CASE-0001:

| Layer | Value |
|-------|--------|
| Canonical climate fact | `month_branch=Sửu` → `season=winter` → `climate_type=cold` |
| Published classification | `temperature_level=hot` via `pri_level_hot` (`score >= 0.65`) |

Classification used **score thresholds** (`database/11_temperature/06_priority_rules.csv` `pri_level_*`). Because cold/dry points raise the total, Sửu crossed `0.65` and was labeled `hot` (“Nhiệt khí nặng”) while the month-branch climate remained `cold`.

Fire count (CASE-0001 Hỏa=4) has **no** CSV rule that sets `temperature_level=hot`. The flip was **not** a proven khí-cục conversion. It was a threshold applied to the wrong semantic.

Full Report then showed `Điều hậu: —` because the adapter read `dieu_hau / label / status / level` while the API published `temperature_level`.

---

## 3. Decision: Case 2 (do not flip rule signs)

Case 1 (make the score a cold→hot axis) was rejected. Flipping cold-rule signs would only exist to keep a `hot` UI. The rule source adds cold/dry **magnitude**; it does not encode a signed thermal axis.

Repair:

| Keep | Change |
|------|--------|
| Score arithmetic (intensity) | Stop classifying `cold/cool/warm/hot` from `pri_level_*` |
| Month-branch season / climate facts | Publish `climate_state` from `climate_type` (special CSV `priority >= 105` may reinforce) |
| Numeric score in Technical Info | Customer presentation uses climate state + balancing need, not `0.72` |

`temperature_level` is now an **alias of `climate_state`**.

Special rules `spc_001`–`spc_004` still reinforce (Fire+summer→hot, Water+winter→cold, …). They do not flip CASE-0001 Canh / Sửu.

---

## 4. Canonical Điều hậu model

Owner: Temperature Engine. Not Useful God. Not Pattern `dieu_hau`.

| Field | Source | CASE-0001 |
|-------|--------|-----------|
| `month_branch` | BaZi month branch | Sửu |
| `season` | `_BRANCH_SEASON` | winter |
| `climate_state` | `_BRANCH_CLIMATE` / `climate_type` | cold |
| `balancing_need` | Climate CSV mapping | warming |
| `evidence_compact` | month + season + state + need + winning climate rule | Nguyệt lệnh Sửu · mùa Đông · … · `cli_002` |
| `confidence` | existing match coverage | unchanged mechanism |
| `temperature_score` | intensity (technical) | ~0.72 |

Need mapping is from climate recommendations, not a CASE-0001 hard-code:

| `climate_state` | `balancing_need` | Climate CSV evidence |
|-----------------|------------------|----------------------|
| cold / cool | warming | `cli_002` “Dùng Hỏa Mộc ôn dưỡng”; `cli_004` “Tăng dương khí” |
| hot | cooling | `cli_001` “Dùng Thủy Kim nhuận hạ” |
| warm | balance | `cli_003` “Cân Hỏa Thủy” |

Presentation V1.0:

```text
Trạng thái khí hậu: Hàn
Nhu cầu điều hòa: Cần ôn ấm
Căn cứ khí hậu: Nguyệt lệnh Sửu · mùa Đông · …
```

No tốt/xấu, tài vận, sức khỏe, nghề nghiệp, or cải vận copy.

---

## 5. CASE-0001 before / after

Input: Canh Nhật chủ, month branch Sửu.

| Item | Before (Phase 1 audit) | After (Phase 2) |
|------|------------------------|-----------------|
| Season source | BaZi month branch Sửu | unchanged |
| Season | winter | winter |
| Base climate | cold | cold |
| Published level | hot (score ≥ 0.65) | cold (`climate_state`) |
| Score | 0.72 intensity, labeled as heat | 0.72 intensity, `score_semantic=imbalance_intensity` |
| Recommendations | mixed nhuận hạ **and** ôn dưỡng | climate/season-aligned ôn dưỡng |
| Điều hậu (Full Report) | `—` | Hàn / Cần ôn ấm / Nguyệt lệnh Sửu |
| Report V1 `temperature_adjustment` | hot → “Nhiệt” | cold → “Hàn” |
| Strength | 0.87 / strong | 0.87 / strong |
| Pattern | Chính Ấn / `pat_ca_01` | Chính Ấn / `pat_ca_01` |
| Ten Gods visible stems | Bính, Tân, Canh, Mậu | unchanged |
| Overall Useful God | Thực Thần (`str_004`) | Thực Thần (overlay frozen; see §8) |

---

## 6. Adapter repair

Canonical API fields: `climate_state`, `balancing_need`, `evidence_compact`, `temperature_level` (alias), `temperature_score` (technical).

| Surface | Repair |
|---------|--------|
| `TemperatureView` / `temperature_truth` | Publish climate + Điều hậu fields |
| Full Report | `canonicalTemperature.ts` — no `dieu_hau/label/status/level` |
| Canonical Desktop S01 | Trạng thái khí hậu / Nhu cầu điều hòa / Căn cứ khí hậu |
| Result V2 Technical Info | climate + need + evidence; numeric score under technical only |
| Report V1 / PDF / DOCX | `temperature_adjustment=climate_state`; add `balancing_need`, `climate_evidence` |

Report V1 golden CASE-0001 `expected_report_input.json` updated as **identity correction** (`hot` → `cold` + Điều hậu fields). Production adapter is the source; the snapshot follows it.

---

## 7. Legacy `pattern.dieu_hau`

`pattern.dieu_hau` remains month 得令 (`Đắc lệnh` on CASE-0001). Contract kept.

Live V1.0 presentation no longer labels that field **Điều hậu**:

| Path | Change |
|------|--------|
| `presenters/pattern.js` | label → **Đắc lệnh** |
| `static/i18n/vi.json` `executive.dieu_hau` | **Đắc lệnh** |
| `report_model.js` | stop appending `overview.dieu_hau` into Dụng thần factors |
| `pattern_composer.py` | narrative token → `đắc lệnh` |
| Report V1 | still `follow_pattern` as **Theo cách**, not Điều hậu |

---

## 8. Useful God separation

Temperature does not write Overall Useful God.

| Layer | Behavior |
|-------|----------|
| Điều hậu `balancing_need` | warming (climate) |
| Useful God Engine / CSV | **not edited** |
| `tmp_002` (hot → Quý) | still owned by UG; G1-06 |
| Overlay | `useful_god_temperature_overlay()` keeps the **pre-G1-04 score-threshold type** (`hot` on CASE-0001) so `sea_001` does not rewrite the winner in this gate |
| Published climate | `to_pattern_temperature_type()` = `climate_state` = cold |
| CASE-0001 winner | **Thực Thần** |

Feeding `climate_state=cold` into `PatternContext.temperature_type` would match UG `sea_001` (season group 90 > strength 80) and could change Overall Useful God to a Fire stem. G1-04 must not do that. Alignment of overlay with climate_state is **G1-06**.

---

## 9. Tests

| Suite | Result |
|-------|--------|
| `pytest tests/temperature -q` | PASS (includes 12-branch matrix + Fire/Water modifiers + CASE-0001) |
| `pytest tests/report_engine/test_g1_04_temperature_binding.py` | PASS |
| `pytest tests/report_engine/test_case_0001_report_input.py` | PASS (golden identity) |
| `pytest tests/report_engine/test_g1_03_pattern_binding.py` | PASS |
| `pytest tests/report_engine/test_localization_v1.py` | PASS |
| `vitest` `g1_04_temperature_binding.test.ts` | PASS |
| `vitest` `g1_03_pattern_binding.test.ts` | PASS |

Seasonal matrix (no inverted direction):

- Dần/Mão/Thìn → warm / balance
- Tỵ/Ngọ/Mùi → hot / cooling
- Thân/Dậu/Tuất → cool / warming
- Hợi/Tý/Sửu → cold / warming

Modifiers: CSV has no `fire_count→hot` or `water_count→cold` flip rule. Tests assert Sửu stays cold with Fire=0 and Fire=8; Ngọ stays hot with Water=0 and Water=8.

---

## 10. Remaining V1.1 / later-gate backlog

- **G1-06:** Useful God overlay vs canonical `climate_state` (whether `sea_001` / `tmp_001` should win when Sửu is correctly cold).
- Deep Điều Hậu narrative (thành/phá khí, health, career, cải vận) — out of V1.0.
- Customer-facing numeric `temperature_score` — keep technical-only until a directional metric exists.
- Signed cold↔hot axis — only if a new rule design is commissioned (not this score).
- Dry / humid as first-class customer climate states (Táo / Thấp) — component scores exist; not a 4-way class in V1.0.
- `pri_level_*` CSV rows are unused for published state; cleanup is optional later.

---

## Files changed (Phase 2)

Engine / API: `engines/temperature_engine/climate.py` (new), `scorer.py`, `models.py`, `engine.py`, `applications/api/models/analysis_result.py`, `applications/api/services/temperature_truth.py`, `applications/api/services/orchestrator.py`, `applications/production/engine_runner.py`, `applications/api/tests/unified_stack.py`.

Report: `engines/report_engine/contracts/report_input_v1.py`, `adapters/report_input_v1_adapter.py`, `localization/labels_vi.py`, `rendering/report_sections_v1.py`.

Portal: `canonicalTemperature.ts` (new), `fullReportViewModel.ts`, `canonicalDesktopAdapter.ts`, `liveAnalysisResultAdapter.ts`, `TechnicalInfo/index.tsx`, `pattern.js`, `vi.json`, `report_model.js`.

Presentation rename: `applications/production/interpretation/pattern_composer.py`, `validation/live_e2e_trace.py`.

Tests: `tests/temperature/test_g1_04_temperature_binding.py`, `tests/report_engine/test_g1_04_temperature_binding.py`, `applications/customer_portal/tests/js/g1_04_temperature_binding.test.ts`.

CASE-0001 identity: `tests/golden_dataset/report_v1/CASE-0001/expected_report_input.json` (`temperature_adjustment` hot→cold + Điều hậu fields).

---

G1-04 STATUS: FINAL FREEZE READY

Do not start G1-05. Do not edit Useful God or Deep Interpretation.
