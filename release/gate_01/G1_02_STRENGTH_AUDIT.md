# G1-02 — Strength Truth & Evidence Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-02 |
| **Document** | `release/gate_01/G1_02_STRENGTH_AUDIT.md` |
| **Phase** | 1 — Audit only |
| **Date** | 2026-08-19 |
| **Status** | READY FOR PRODUCT OWNER REVIEW |
| **Scope** | Calculation Truth → Evidence → Presentation tối thiểu |
| **Out of scope** | Narrative tính cách / tài vận / nghề nghiệp / hôn nhân / cát hung / cải vận; engine repair; Portal repair; threshold change; contract mới |

This report does not modify Engine, Rule Database, Portal, Report, Temperature, Pattern, or Useful God.

No new Strength engine is proposed. Canonical implementation already exists.

Live CASE-0001 was executed read-only through `CalendarEngine` → `BaziEngine` → `build_strength_context` → `StrengthEngine.calculate` → `OrchestratorService.analyze`.

---

# Verdict

| Question | Result |
|----------|--------|
| Canonical Strength Engine exists? | **Yes** — `engines/strength_engine` |
| New engine required? | **No** |
| CASE-0001 engine score reproducible? | **Yes** — `strength_level=strong`, `strength_score=0.87` |
| `0.87` is canonical Strength score? | **Yes** — normalized 0–1 public score, not confidence |
| Confidence bound as Điểm thân on surfaces that show `0.87`? | **No** — those surfaces read `StrengthResult.strength_score` |
| Portal/Report all bind the same numeric field? | **No** — several Portal cards prefer `ScoreView.strength_score` (`45.0`) or `total_score` |
| Taxonomy is 7 classes (Cực nhược … Cực vượng)? | **No** — Strength Engine has **3** classes: `strong` / `weak` / `balanced` |
| Threshold overlap/gap? | **No** in Strength Engine level rules |
| Temperature mutates Strength? | **No** |
| Pattern overrides Strength class? | **No** on the live path |
| Useful God reads the same class as Portal label? | **Yes** — `strength_level=strong` → `Thân vượng` |
| G1-02 PASS today? | **No** |

---

# BLOCKERS

These match the G1-02 blocker rules. Calculation of CASE-0001 itself is **not** a blocker.

| ID | Rule | Finding | Layer |
|----|------|---------|-------|
| **B1** | Engine và presentation dùng hai source khác nhau | Canonical Desktop `mapS05` / `mapS01` / `baziResultAdapter.mapStrength` prefer `data.score.strength_score` (`45.0`, Score Engine 0–100) over `data.strength.strength_score` (`0.87`). `mapS05` may further display `total_score / grade` (`51.25 / D+`) as the card score. Class still comes from Pattern/Strength (`Thân vượng`). | adapter / presentation |
| **B2** | Engine và Report (legacy HTML) dùng hai source khác nhau | `applications/customer_portal/static/js/report/report_model.js` `strengthGaugeValue()` reads `score.strength_score` / `body_strength_score` / `than_score`, then metrics.js labels it **Điểm Thân**. Report V1 PDF/DOCX uses `analysis.strength.strength_score` and is canonical. | adapter / presentation |
| **B3** | Cùng một chart cho ra nhiều số “điểm thân” | CASE-0001 live: Strength `0.87`, Score contribution `45.0`, overall `51.25 / D+`, confidence `1.0`. Different surfaces pick different numbers next to `Thân vượng`. | presentation |

Not blockers (checked):

| Rule | Result |
|------|--------|
| `0.87` không phải canonical Strength score | **False.** It is `StrengthResult.strength_score`. |
| Portal bind nhầm `confidence` thành Điểm thân on the 0.87 surfaces | **False** for Technical Info / Full Report / Production appendix / Report V1. `confidence` is `1.0`. |
| CASE-0001 không tái tạo được từ engine | **False.** Live match: `0.87` / `strong` / matched rules identical to `knowledge/pilot/cases/CASE-0001/actual.json`. |
| Threshold overlap/gap | **False** for the 3-class Strength rules. |
| Same Strength score → multiple Strength Engine classes | **False** for CASE-0001. Special rules with `priority >= 105` *can* override class independently of score (see §7). |
| Legacy `engines/bazi_engine/strength` override production | **False.** Orchestrator does not call it. |
| Useful God reads a different **class** than Portal label | **False** on live CASE-0001. Useful God matches `strength_level=strong`; Portal label is `Thân vượng`. Useful God does not read the numeric score. |

---

# 1. Canonical production implementation

## 1.1 Production owner (frozen)

`beta/BETA0_ANALYTICAL_TRUTH_LOCK.md` assigns Strength to:

```text
Strength
    engines/strength_engine
```

It must not be replaced by Score or Pattern. Temperature must not be folded into Strength.

Public entry:

```text
from engines.strength_engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context

ctx = build_strength_context(bazi_chart, calendar=calendar)
result = StrengthEngine().calculate(ctx)
```

| Item | Value |
|------|-------|
| Canonical module | `engines/strength_engine` |
| Public class | `StrengthEngine` |
| Public method | `StrengthEngine.calculate(context: StrengthContext) -> StrengthResult` |
| Input model | `engines.strength_engine.context.StrengthContext` |
| Output model | `engines.strength_engine.models.StrengthResult` |
| Rule database | `database/12_strength/` via `StrengthLoader` |
| Default DB path | `engines/strength_engine/engine.py` → `database/12_strength` |

Production callers:

| Caller | What it does |
|--------|----------------|
| `applications/api/services/orchestrator.py` | `self.strength_engine = StrengthEngine()`; `calculate(strength_context)`; `analysis.strength = build_strength_view(...)` |
| `applications/production/engine_runner.py` | Same engine; copies `strength_level` / `strength_score` onto `PatternContext` |
| `applications/api/services/strength_truth.py` | `StrengthResult.to_portal_dict()` → `StrengthView` |

## 1.2 Calculators / stages

`StrengthAnalyzer` runs, in order:

| Stage | Module | Rule file |
|-------|--------|-----------|
| season | `calculators/season_strength.py` | `01_season_rules.csv` |
| root | `calculators/root_strength.py` | `02_root_rules.csv` |
| support | `calculators/support_strength.py` | `03_support_rules.csv` |
| control | `calculators/control_strength.py` | `04_control_rules.csv` |
| drain | `calculators/drain_strength.py` | `05_flow_rules.csv` |
| combination | `calculators/combination_strength.py` | rows in `07_special_rules.csv` with `score_target=combination` |
| special | `calculators/special_case.py` | remaining `07_special_rules.csv` |

Shared matcher: `engines/strength_engine/matcher.py`.

Scoring / classification: `engines/strength_engine/scorer.py`.

Level priority: `engines/strength_engine/priority.py` + `06_priority_rules.csv`.

Normalization config: `09_conditions.csv`.

Context facts (month status, root, support/control/drain types, season tokens) are built in `engines/strength_engine/utils/context_builder.py` from `BaziChart`. The `calendar=` argument is accepted and **unused**. Season is derived from month earthly branch maps, not from solar term.

## 1.3 Parallel / legacy Strength implementations

| Module | Status | Production leak? |
|--------|--------|------------------|
| `engines/strength_engine` | **canonical** | Yes — Orchestrator / Production runner |
| `engines/analysis_engine/01_strength_engine/` | Architecture docs only (no live `engine.py`) | **No** — not imported by applications |
| `engines/analysis_engine/pipeline/stage_registry.py` | Catalog names a `strength` stage | **No** — applications do not run this pipeline |
| `engines/bazi_engine/strength/` | Legacy BaZi-internal calculator | **No** on API/production path. Only referenced by `engines/bazi_engine/pattern/calculator.py` and `engines/bazi_engine/useful_god/calculator.py`, which applications do not call |
| `engines/score_engine/calculators/strength_score.py` | Score **contribution** 0–100 from `database/15_score_engine/03_strength/` | Does **not** write `AnalysisResult.strength`. **Does** populate `ScoreView.strength_score` and can overwrite top-level `rule_context["strength_score"]` after compose |
| `database/15_score_engine/03_strength/07_strength_level.csv` | **7-class** Score taxonomy | Unused for `StrengthView.strength_level` |

## 1.4 Engine actually used

Orchestrator Stage 3.5:

```text
build_pattern_context(bazi)
build_strength_context(bazi)
StrengthEngine.calculate(strength_context)
pattern_context.strength_level = strength_result.strength_level
pattern_context.strength_score = strength_result.strength_score
analysis.strength = build_strength_view(strength_result)
```

Then Temperature (reads Strength, does not write Strength), Pattern, Useful God.

---

# 2. Dependency graph

```text
CalendarEngine.build
        ↓
BaziEngine.build
        day_master, pillars, ten_gods (visible stems), hidden_stems
        ↓
build_strength_context(bazi, calendar=…)
        month_status, root_level, support/control/drain types,
        season tokens, ten-god family counts
        ↓
StrengthAnalyzer stages (season → root → support → control → drain → combination → special)
        ↓
StrengthScorer
        raw_total, normalized strength_score, strength_level, confidence
        ↓
StrengthResult
        ↓
        ├─ AnalysisResult.strength          (StrengthView)     ← API / Report V1 / Full Report
        ├─ PatternContext.strength_level/score
        │         ↓
        │   PatternEngine  →  pattern.than_vuong_nhuoc  (label only, mapped from level)
        │         ↓
        │   UsefulGodEngine.strength_level  (class only, not the 0–1 score)
        ├─ TemperatureContext.strength_level/score
        │         ↓
        │   TemperatureEngine  (fields present; no temperature CSV rule matches them)
        └─ ScoreEngine StrengthScoreCalculator
                  ↓
            ScoreResult.strength_score (0–100 contribution)
                  ↓
            AnalysisResult.score.strength_score
```

Direction is one-way. No circular dependency Strength ↔ Temperature ↔ Pattern.

---

# 3. Strength formula hiện tại

Name the scores distinctly. Do **not** call all of them `strength_score`.

| Name | Field | Unit | Meaning |
|------|-------|------|---------|
| **Raw total** | `metadata.trace.scoring.raw_total` | points | Sum of matched rule `score` values |
| **Baseline** | config `cfg_baseline` | points | `50.0` |
| **Scale** | config `cfg_scale` | points | `100.0` |
| **Normalized public score** | `StrengthResult.strength_score` | 0–1 | `(raw_total + baseline) / scale`, clamp `[0, 1]` |
| **Component scores** | `season_score`, `root_score`, `support_score`, `drain_score`, `control_score` | 0–1 scale | `bucket_raw / scale` (no baseline) |
| **Classification** | `StrengthResult.strength_level` | enum | `strong` \| `weak` \| `balanced` |
| **Match confidence** | `StrengthResult.confidence` | 0–1 | `min(1, n_matched / 5) + 0.2` if a level rule matched, cap 1.0 |
| **Score Engine contribution** | `ScoreView.strength_score` | 0–100 | Separate module score; **not** Strength truth |
| **Display score (Portal S05)** | adapter-derived | mixed | May be 0–100 Strength, Score contribution, or total grade |

## 3.1 Aggregation

Every **active matching rule** adds `rule["score"]` into its `score_target` bucket.

Rule `priority` does **not** pick a winner inside a scoring bucket. Multiple matches **stack** (CASE-0001: `ctl_001` + `ctl_006`).

```text
raw_total = season + root + support + drain + control + combination + special
normalized = clamp((raw_total + 50) / 100, 0, 1)
StrengthResult.strength_score = normalized
```

Clamp is only after normalization, to `[0.0, 1.0]`. There is no second public rescale.

## 3.2 Component answers (engine, not CASE-specific)

| Question | Answer |
|----------|--------|
| Raw score ban đầu? | Sum of matched CSV `score` cells. No implicit starting raw besides baseline at normalize time. |
| Baseline? | **Yes, +50** at normalize time only. Not added into component fields. |
| Seasonal / month command? | `01_season_rules.csv` via `month_status` (Đắc lệnh / Tướng / Hưu / Tù / Tử). |
| Root / thông căn? | `02_root_rules.csv` via `root_level`. |
| Support / sinh trợ? | `03_support_rules.csv`. Includes companion (“Đồng hành”) and resource. There is **no separate peer calculator**. Peer is the support bucket. |
| Control / khắc chế? | `04_control_rules.csv` (negative scores). |
| Drain / tiết hao? | `05_flow_rules.csv` (negative scores). |
| Combination / transformation? | Yes, if combination rows match. Scores go to the `combination` bucket. **Not published** as a `StrengthResult` field. |
| Temperature / điều hậu cộng trực tiếp vào Strength? | **No.** `temperature_type` is stored on context; no `database/12_strength` rule matches it. |
| Special bonus/penalty? | Yes, `07_special_rules.csv`. Also may **override class** if `priority >= 105` and `strength_level` hint is set. |
| Normalization? | `(raw + 50) / 100`. |
| Clamp min/max? | Yes, `[0, 1]` on the public score. |
| Public final value? | `StrengthResult.strength_score` (0–1). |

## 3.3 Classification after score

1. Write `context.strength_score = normalized`.
2. `StrengthPriorityResolver.resolve_level` picks the matching level rule with max `(priority, score)`.
3. Special matches with `priority >= 105` and a `strength_level` hint **replace** the class (not the numeric score).

`09_conditions.csv` also stores `cfg_strong_threshold=0.65` and `cfg_weak_threshold=0.35`, but the scorer classifies from `06_priority_rules.csv` level rows, not from those config keys. Today the numbers agree. Dual source is a gap.

---

# 4. Component calculators

Context builder facts (before scoring):

| Fact | How it is derived |
|------|-------------------|
| `month_status` | Day-master element vs month-branch **main hidden stem** element: same → Đắc lệnh; month produces DM → Tướng; DM produces month → Hưu; DM controls month → Tù; month controls DM → Tử. |
| `root_level` | Count of earthly branches whose hidden stems contain DM element: 3+ / 2 / 1 / tàng can / vô căn. |
| `support_type` | First of year/month/**hour** visible stems (not day) that is companion or resource ten-god. |
| `control_type` | First of year/month/hour visible stems that is officer / output / wealth. |
| `drain_type` | From visible ten-god lists: output first, else wealth. |
| `ten_gods_list` | `BaziChart.ten_gods` minus `Nhật Chủ` — **visible pillar stems only**. Hidden ten-gods are used for rooting, not for family counts. |
| `season` | Month branch map: Sửu → `winter`. Calendar solar term is not read. |

Each calculator is a thin `run_rule_stage` over CSV.

---

# 5. Rule sources

| File | Role |
|------|------|
| `database/12_strength/01_season_rules.csv` | Month command points |
| `database/12_strength/02_root_rules.csv` | Root points |
| `database/12_strength/03_support_rules.csv` | Support points |
| `database/12_strength/04_control_rules.csv` | Control points |
| `database/12_strength/05_flow_rules.csv` | Drain points |
| `database/12_strength/06_priority_rules.csv` | Group priority labels + **level classification** |
| `database/12_strength/07_special_rules.csv` | Special + combination |
| `database/12_strength/08_examples.csv` | Loader examples (not production runtime) |
| `database/12_strength/09_conditions.csv` | baseline / scale / documented thresholds |

Not Strength SSOT:

| Source | Role |
|--------|------|
| `database/15_score_engine/03_strength/*` | Score Engine module contribution + 7-class table |
| `engines/bazi_engine/strength/` | Legacy unused by Orchestrator |
| `database/05_phan_tich/.../than_vuong*` | Knowledge docs / other domains |

---

# 6. Classification thresholds

Canonical Strength taxonomy is **three classes**, from `06_priority_rules.csv` and `engines/pattern_engine/labels.py` `STRENGTH_LEVEL_LABELS`.

Do not invent a 7-class Strength taxonomy. The 7-class table exists only in Score Engine CSV (`07_strength_level.csv`) and is **not** `StrengthResult.strength_level`.

| Score range (normalized) | Internal class | Vietnamese label | Rule / source | Bounds |
|--------------------------|----------------|------------------|---------------|--------|
| `score >= 0.65` | `strong` | Thân vượng | `pri_level_strong` | inclusive lower |
| `0.35 < score < 0.65` | `balanced` | Trung hòa | `pri_level_balanced` | exclusive both ends |
| `score <= 0.35` | `weak` | Thân nhược | `pri_level_weak` | inclusive upper |

Boundary check:

| Value | Matches | Winner |
|-------|---------|--------|
| `0.65` | strong only (`>=`); balanced requires `< 0.65` | `strong` |
| `0.649…` | balanced | `balanced` |
| `0.35` | weak only (`<=`); balanced requires `> 0.35` | `weak` |
| `0.351…` | balanced | `balanced` |
| `0.00` (clamp min) | weak | `weak` |
| `1.00` (clamp max) | strong | `strong` |

No gap. No overlap among the three level rules.

If several level rules matched, resolver uses max `(priority, score)`. Strong and weak both have priority 100; they cannot both match the same score.

Report localization (`engines/report_engine/localization/labels_vi.py`) also maps unused tokens `very_strong` / `very_weak` / `neutral` onto the same three Vietnamese labels. Strength Engine never emits those tokens.

---

# 7. CASE-0001 full trace

Golden identity:

| Field | Value |
|-------|-------|
| Subject | Nguyễn Tiến Sơn |
| Solar | 1987-01-21 04:30 |
| Pillars | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| Nhật chủ | Canh Kim |

Live engine output: **`strong` / `0.87` / reasoning `Thân vượng`**.

This matches `applications/production/fixtures/case_0001.py` `CASE_0001_EXPECTED_STRENGTH` and `knowledge/pilot/cases/CASE-0001/actual.json` strength block.

Note: `actual.json` **pattern.than_vuong_nhuoc** was historically `"Trung hòa"`. Live Orchestrator now emits `"Thân vượng"`. That historical fixture row is stale relative to current Pattern label mapping; Strength numbers are not.

## 7.1 Input evidence

| Evidence | Live value | Used by Strength? |
|----------|------------|-------------------|
| Nguyệt lệnh / month branch | Sửu; main hidden stem Kỷ (Thổ) | Yes — `month_status` |
| Month status | **Tướng** (Thổ sinh Kim) | Yes — `sea_002` |
| Mùa | `winter` / `late_winter` (from Sửu, not solar term Đại Hàn) | Yes — `spc_004` season list |
| Temperature token | `cold` | Stored only; **not scored** |
| Thông căn | Sửu hidden **Tân** (Kim) → 1 chi | Yes — `root_003` |
| Year/hour Dần hidden | Giáp/Bính/Mậu — no Kim | Counted as non-root |
| Day sitting Ngọ | Đinh/Kỷ — Hỏa/Thổ, no Kim | **Not** a separate scored pressure |
| Can lộ year | Bính → Thất Sát | control + officer list |
| Can lộ month | Tân → Kiếp Tài | support_type companion |
| Can lộ hour | Mậu → Thiên Ấn | resource count; not support_type (companion already chosen) |
| Day stem | Canh = Nhật Chủ | excluded from `ten_gods_list` |
| Nguyệt chi ten-god (branch main stem) | Kỷ vs Canh = **Chính Ấn** | `spc_004` |
| Month **pillar** ten-god (stem) | Tân = Kiếp Tài | Shown on BaZi pillar; Strength support uses this stem, special uses branch main stem |
| Hợp/hóa | no combination match | No |
| Drain / wealth / output | empty visible lists | No drain rule |
| Special | Chính Ấn + winter | `spc_004` +10; priority 102 **does not** override class |

Visible ten gods used for family counts: Thất Sát, Kiếp Tài, Thiên Ấn.

## 7.2 Score decomposition

Formula check:

```text
+25  sea_002   Tướng
+12  root_003  Thông căn 1 chi
 +8  sup_001   Đồng hành trợ thân
-10  ctl_001   Bị Quan Sát khắc
 -8  ctl_006   Có Thất Sát
+10  spc_004   Ấn mùa lạnh
────────────────
raw_total = 37
normalized = (37 + 50) / 100 = 0.87
clamp unchanged
class = pri_level_strong because 0.87 >= 0.65
confidence = min(1, 6/5) + 0.2 = 1.0
```

| Component | Evidence | Rule ID | Raw contribution | Applied (bucket/100) |
|-----------|----------|---------|-----------------:|---------------------:|
| Season | Tháng Sửu, Thổ sinh Kim → Tướng | `sea_002` | +25 | +0.25 |
| Root | Tàng can Tân trong Sửu | `root_003` | +12 | +0.12 |
| Support / peer | Can Tân = Kiếp Tài | `sup_001` | +8 | +0.08 |
| Drain | none | — | 0 | 0.00 |
| Control | Can Bính = Thất Sát | `ctl_001` | −10 | |
| Control | `officer_elements` contains Thất Sát | `ctl_006` | −8 | **−0.18** combined |
| Combination | none | — | 0 | unpublished |
| Special | `month_branch_ten_god=Chính Ấn`, `season=winter` | `spc_004` | +10 | **unpublished** as a result field; included in raw_total |
| Baseline | config | `cfg_baseline` | +50 | applied only at normalize |
| Public score | | | | **0.87** |

Published component fields `0.25 + 0.12 + 0.08 + 0.00 + (−0.18) = 0.27`. Adding unpublished special `0.10` and baseline `0.50` yields `0.87`. A UI that sums only published components **cannot** reconstruct `0.87` without special + baseline.

`0.87` is **not** Score Engine (`45.0`) and **not** confidence (`1.0`).

---

# 8. Exact source of `0.87`

`0.87` is the **normalized public Strength score** (0–1).

Field path (canonical):

```text
StrengthScorer.normalized
  → StrengthResult.strength_score
    → StrengthResult.to_portal_dict()["strength_score"]
      → strength_truth.build_strength_view()
        → AnalysisResult.strength.strength_score
          → API payload data.strength.strength_score
```

Surfaces that show **0.87** for CASE-0001:

| Surface | Path |
|---------|------|
| Production advisor appendix | `strength_result.strength_score` labeled **Điểm thân** |
| Portal Full Report | `fullReportViewModel.ts` `data.strength?.strength_score` labeled **Điểm thân** |
| Portal Technical Info | `liveAnalysisResultAdapter.pickStrengthScore` → `data.strength.strength_score` labeled **Điểm thân** |
| Report V1 PDF/DOCX | `report_input_v1_adapter._build_strength` → `ReportStrengthV1.score` → section “Điểm” |
| API `data.strength` | `StrengthView.strength_score` |

Surfaces that do **not** show 0.87, despite the same chart:

| Surface | What it shows | Source |
|---------|---------------|--------|
| Canonical Desktop S05 score number | `45` or `51.25 / D+` | `score.strength_score` then possibly `total_score/grade` |
| Canonical Desktop S05 bar percent | `45` | `normalizeScore100(score.strength_score)` |
| BaZi result Strength card score | `45 / 100` | same Score preference |
| Legacy JS report “Điểm Thân” gauge | `45` | `score.strength_score` |
| Score category “Thân” | `45` | `presenters/score.js` keys `strength_score` on `data.score` |

`normalizeScore100` treats values `<= 1` as 0–1 (`0.87 → 87`). If S05 bound Strength instead of Score, it would display **87 / 100**, not `0.87`. Full Report currently prints the raw `0.87`.

Confidence path (must not be labeled Điểm thân):

```text
StrengthResult.confidence = 1.0
  → StrengthView.confidence
    → BaZi CoreAnalysisSection “Độ tin cậy: 100%”
```

That badge is separate from 0.87 on the BaZi card. S05 does not show confidence as the main number.

---

# 9. Evidence availability

`StrengthResult` today:

| Evidence need (V1.0) | Present? | Where |
|----------------------|----------|-------|
| Component / category | Partial | `season_score` … `control_score`; combination/special **missing** on the result object |
| Source pillar/stem/branch | Partial | In `StrengthContext`, not copied onto public `to_portal_dict()` |
| Rule id | Yes | `matched_rules: list[str]` |
| Direction support / weaken | Implicit | Sign of CSV score; not a dedicated field |
| Weight / contribution | Lost on public view | Only rule ids, not per-rule score |
| Machine-readable reason | Partial | `reasoning` is the **winning level** reason (`Thân vượng`), not a component list |
| Trace | Internal | `metadata.trace` (analysis groups, raw_total, level_rule, config). Not in `to_portal_dict()` |

`StrengthRuleMatch` exists in `models.py` and is **unused**. Matches are reduced to id strings.

Adapter `build_strength_view` copies portal dict only. Report adapter turns `support_score` / `drain_score` / `control_score` into short strings (`Hỗ trợ: 0.08`) and drops rule ids.

Gap: evidence exists in engine metadata and is stripped before Portal.

---

# 10. Portal / Report / PDF / DOCX binding

## 10.1 Class label `Thân vượng`

| Surface | Field | Same StrengthResult? |
|---------|-------|----------------------|
| API `data.strength.reasoning` | copied from level rule reason | Yes |
| API `data.strength.strength_level` | `strong` | Yes |
| API `data.pattern.than_vuong_nhuoc` | `STRENGTH_LEVEL_LABELS["strong"]` | Same class, different field |
| Full Report strengthLabel | `pattern.than_vuong_nhuoc` then `pattern.than` then `strength.strength_level` | Label from Pattern mapping |
| S05 `level` | `pattern.than_vuong_nhuoc` / `than`, else score bands MẠNH / TRUNG BÌNH / YẾU | Class from Pattern; **fallback invents a second taxonomy** |
| BaZi `mapStrengthLevel` | `strength.strength_level` → `THÂN VƯỢNG` / `Mạnh` | Class from Strength; score from Score Engine |
| Report V1 “Mức” / “Phân loại” | `display_text(level, "strength")` → Thân vượng | Yes |
| Production appendix “Mức thân” | `strength_level` English `strong` | Yes, untranslated |

Live CASE-0001: Pattern label and Strength class agree (`Thân vượng` / `strong`). Historical `actual.json` Pattern `Trung hòa` is **not** current production.

No renderer recomputes Strength. Adapters **re-pick fields** and **re-band** 0–100 scores.

## 10.2 Numeric `0.87` vs other numbers

See §8. Report V1 PDF/DOCX is canonical. Several Portal cards are not.

## 10.3 Evidence on UI

`matched_rules` and component scores are on the API. S05 factors split `reasoning` (`Thân vượng`) into a single factor. Rule ids and decomposition are **not** shown.

## 10.4 Proposed V1.0 presentation (do not implement in Phase 1)

Keep three-class taxonomy. Do not add personality narrative.

```text
Thân: Thân vượng
Điểm thân: 0.87
Căn cứ chính: Nguyệt lệnh · Thông căn · Sinh trợ · Khắc chế · Đặc lệ
```

Compact decomposition if existing fields are reused:

```text
Nguyệt lệnh +0.25 · Thông căn +0.12 · Sinh trợ +0.08 · Khắc chế −0.18
(Đặc lệ +10 raw is in the total; publish it before showing.)
```

Bind **only**:

- class: `STRENGTH_LEVEL_LABELS[strength.strength_level]` (or Pattern `than_vuong_nhuoc` after it is proven equal)
- score: `strength.strength_score`
- never: `strength.confidence`, `score.strength_score`, `score.total_score`

---

# 11. Legacy / duplicate fields

| Field / module | Classification |
|----------------|----------------|
| `StrengthResult.strength_score` | **canonical** (0–1) |
| `StrengthResult.strength_level` | **canonical** |
| `StrengthResult.confidence` | **canonical but different quantity** (match density) |
| `StrengthView.*` | **canonical API** |
| `PatternContext.strength_score` / `strength_level` | **canonical copy** into Pattern |
| `pattern.than_vuong_nhuoc` | **presentation label** of canonical class |
| `pattern.than` | **not Strength** — day-master element (`Kim`) |
| `ScoreResult.strength_score` / `ScoreView.strength_score` | **presentation-adjacent Score contribution** (0–100); not Strength truth |
| `rule_context["strength"]["score"]` | **canonical** after Pattern publish / merge |
| `rule_context["strength_score"]` after Score compose | **legacy/confusable** — Score Engine writes 0–100 onto the top-level key |
| `database/15_score_engine/03_strength/07_strength_level.csv` 7 classes | **unused** for StrengthView |
| `engines/bazi_engine/strength` | **legacy unused** by Orchestrator |
| `engines/analysis_engine/01_strength_engine` | **docs only / unused** |
| `body_strength_score` | **legacy alias** in JS report_model pick list |
| `than_score` | **legacy alias** in JS report_model |
| `strength_ratio` / `day_master_strength` | **not found** as production fields |
| Canonical Desktop mock `s05.score = "82 / 100"` | **presentation-only fixture** |
| `CASE_0001_EXPECTED_STRENGTH = 0.87` | **canonical golden** — matches live engine |

---

# 12. Boundary test coverage

Existing Strength tests live under `tests/strength/` (not `tests/strength_engine/`).

| Need | Coverage now |
|------|----------------|
| Exact lower strong `0.65` | **Missing** (`test_priority` uses `0.70` only) |
| Exact upper weak `0.35` | **Missing** |
| ± epsilon around `0.65` and `0.35` | **Missing** |
| Min `0.0` / max `1.0` | Indirect clamp in scorer; no dedicated test |
| Neutral / middle `0.50` | **Missing** as a level test |
| Extreme raw (below −50 / above 50) | **Missing** |
| CASE-0001 live 0.87 | `tests/production/test_case_0001_regression.py` (expects 0.87). **Not** in `tests/strength/` |
| Stacking control rules | Implicit via CASE-0001 production test, not unit-level |
| Special override `priority >= 105` vs score band | **Missing** |
| Dual threshold files (`09_conditions` vs `06_priority_rules`) stay equal | **Missing** |
| Portal must not bind `score.strength_score` as Điểm thân | **Missing** |

`tests/strength/test_regression.py` runs 100 random charts for distribution / dead rules. It is not a boundary suite.

HUYNH P0 tests (`0.66` / Thân vượng) are a **different birth**, not CASE-0001.

Phase 1 does not add tests. Phase 2 should.

---

# 13. Gaps

1. Portal Canonical Desktop and BaZi adapters prefer Score Engine’s 0–100 `strength_score` (and S05 may show overall grade) while class is Strength/Pattern.
2. Legacy HTML report gauge labeled Điểm Thân binds Score, not Strength.
3. Full Report prints `0.87` (0–1); S05 would print `87` if it used Strength via `normalizeScore100`. Unit inconsistency across Portal.
4. Special and combination contributions are in `raw_total` but omitted from `StrengthResult` component fields, so published components do not sum to the public score.
5. Public API drops per-rule scores, source pillar, and trace. `StrengthRuleMatch` unused.
6. `reasoning` is the class slogan (`Thân vượng`), not evidence.
7. Thresholds exist in both `09_conditions.csv` and `06_priority_rules.csv`.
8. Context builder ignores `calendar`; solar term is not Strength evidence.
9. Visible-only ten-god family counts; hidden gods other than rooting are ignored.
10. Sitting day-branch pressure (CASE-0001 Ngọ Hỏa) is not a scored component.
11. Score Engine keeps a 7-class table that is not Strength SSOT; Report labels map `very_strong` anyway.
12. `pattern.than` fallback can show `Kim` as a strength label if `than_vuong_nhuoc` is empty.
13. Production appendix prints English `strong` for “Mức thân”.
14. No Strength boundary unit tests; no Portal-binding regression for CASE-0001 `0.87`.
15. `append_score_to_rule_context` writes Score’s 0–100 onto top-level `strength_score`, colliding with the Strength 0–1 name.

---

# 14. Gap classification

| Gap | Category |
|-----|----------|
| S05 / mapS01 / baziResultAdapter prefer `score.strength_score` | **adapter**, **presentation** |
| S05 may display `total_score / grade` as the strength card score | **adapter**, **presentation** |
| Legacy JS Điểm Thân gauge | **adapter**, **presentation** |
| 0–1 vs 0–100 display units | **presentation** |
| Special/combination not on StrengthResult | **contract** |
| Per-rule contribution stripped | **contract**, **adapter** |
| Dual threshold files | **rule**, **threshold** |
| Calendar unused / solar term unused | **calculation** (context), not a live CASE-0001 error |
| Visible-only ten-god counts | **calculation** |
| Day-branch sitting not scored | **calculation** / product rule choice |
| 7-class Score CSV vs 3-class Strength | **rule**, **presentation** |
| `pattern.than` fallback | **adapter** |
| Appendix English class | **presentation** |
| Missing boundary tests | **test** |
| Top-level `rule_context["strength_score"]` name collision | **contract** |
| Confidence vs score (not currently mixed on 0.87 surfaces) | watch item, **presentation** |

---

# 15. Minimal changes for G1-02 PASS

Phase 2 only. Do not expand narrative. Do not replace the engine. Do not change CASE-0001 math unless Product Owner requests a rule change.

1. **Adapter (required):** Canonical Desktop `mapS01` / `mapS05` and `baziResultAdapter.mapStrength` must read `data.strength.strength_score` and `data.strength.strength_level`. Stop preferring `data.score.strength_score`. Do not put `total_score / grade` on the Strength card.
2. **Adapter (required):** Legacy `report_model.js` `strengthGaugeValue` must read `data.strength.strength_score` (0–1 → display policy), not `score.strength_score`.
3. **Presentation (required):** One display policy for Điểm thân (keep `0.87` or show `87/100` from that same field). Do not mix Score contribution.
4. **Presentation (required):** Label class only via `STRENGTH_LEVEL_LABELS` / existing `than_vuong_nhuoc`. No S05 fallback MẠNH/TRUNG BÌNH/YẾU from a different number.
5. **Presentation (minimum evidence):** Show compact căn cứ from existing `matched_rules` or published component scores. Do not write personality copy.
6. **Contract (recommended, small):** Publish special/combination raw or scaled scores on `StrengthResult` so components + baseline reconstruct `strength_score`. Reuse `StrengthRuleMatch` or `metadata.trace`; do not design a new engine.
7. **Test (required):** Boundary cases at `0.35`, `0.65`, ± epsilon, min, max, middle; CASE-0001 `0.87` + `Thân vượng` on API `data.strength` **and** Portal adapter inputs; assert adapter output ≠ `score.strength_score` `45.0`.
8. **Do not:** Change `database/12_strength` scores or thresholds; fold Temperature into Strength; adopt Score’s 7 classes; delete legacy modules; make Useful God reread a different Strength field.

Optional later (not required to declare calculation truth frozen): single threshold source; include calendar solar term; score sitting branch; translate appendix `strong`.

---

# Interaction with Temperature / Pattern / Useful God

```text
StrengthResult
    ↓ copy level+score
TemperatureContext          Temperature CSV does not match strength_* fields.
    ↓ temperature_type only
PatternContext              Pattern does not recompute Strength.
    ↓ strength_level
UsefulGodContext            Rules in database/13_useful_god/01_strength_rules.csv
                            match strength_level == weak|strong|balanced.
```

- Strength does not depend on Temperature output.
- Temperature does not rewrite Strength score or class.
- Pattern maps class to `than_vuong_nhuoc`; it does not override it from cách cục / tòng cách on the live path.
- Tòng cách (`follow_type`) affects Useful God / `tong_cach`, not `StrengthResult`.
- Special Strength override (priority ≥ 105) lives **inside** StrengthScorer. That is still canonical Strength, not Pattern.
- Useful God CASE-0001: `str_004` “Than vượng cần tiết khí” because `strength_level=strong`. Same class Portal shows as Thân vượng. Useful God does not consume `0.87`.

No circular dependency.

---

# STOP

Phase 1 complete.

No Strength Engine change.
No Rule Database change.
No threshold change.
No Portal / Report / Temperature / Pattern / Useful God change.

Return this audit to Product Owner before Phase 2.
