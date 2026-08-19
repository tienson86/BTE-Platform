# G1-03 — Pattern / Cách cục Truth & Evidence Audit

| Field | Value |
|-------|-------|
| **Gate** | GATE 1 / G1-03 |
| **Document** | `release/gate_01/G1_03_PATTERN_AUDIT.md` |
| **Phase** | 1 — Audit only |
| **Date** | 2026-08-19 |
| **Status** | READY FOR PRODUCT OWNER REVIEW |
| **Scope** | Calculation Truth → Evidence → Presentation binding |
| **Out of scope** | Ý nghĩa Chính Ấn; nghề nghiệp; tài vận; cát/hung; lời khuyên; engine repair; Portal/Report repair |

This report does not modify Engine, Rule Database, Priority, Portal, Report, Strength, Temperature, Ten Gods, Useful God, or Narrative.

No new Pattern Engine is proposed. Canonical implementation already exists.

Live CASE-0001 was executed read-only through `CalendarEngine` → `BaziEngine` → `build_pattern_context` → `PatternEngine.calculate` → `OrchestratorService.analyze` → Report V1 adapter.

---

# Verdict

| Question | Result |
|----------|--------|
| Canonical Pattern Engine exists? | **Yes** — `engines/pattern_engine` |
| New engine required? | **No** |
| CASE-0001 `Chính Ấn` from canonical engine? | **Yes** — rule `pat_ca_01`, `pattern=chinh_an`, `cach_cuc=Chính Ấn` |
| Nguyệt lệnh = month branch main qi (Lệnh Tháng)? | **Yes** — Sửu → Kỷ → `ten_god_name(Canh, Kỷ)` = **Chính Ấn** |
| Thấu can used in selection? | **No** — computed nowhere as a match condition |
| Middle / residual qi of month branch used? | **Stored, not scored** |
| Portal/Report bind `pattern.cach_cuc`? | **Yes** — same `Chính Ấn` |
| PatternView publishes candidates / winning rule / month-command evidence? | **No** |
| Taxonomy of main patterns is 10 lệnh-tháng ways? | **Yes** (plus `pat_fallback` → `chinh_quan`) |
| G1-03 freeze-ready today? | **No** |

---

# BLOCKERS

These match the G1-03 blocker rules. CASE-0001 **calculation** itself is **not** a blocker.

| ID | Rule | Finding | Layer |
|----|------|---------|-------|
| — | CASE-0001 `Chính Ấn` không đến từ canonical Pattern Engine | **False.** Winner is `pat_ca_01` via `month_branch_ten_god == "Chính Ấn"`. | calculation |
| — | Portal/Report tự suy ra Pattern | **False** on live TypeScript adapters and Report V1. They read `data.pattern.cach_cuc`. | presentation |
| — | Pattern Engine và Report dùng hai kết quả khác nhau | **False.** Report `primary_pattern` = `Chính Ấn`. | presentation |
| — | Candidate selection phụ thuộc iteration order không deterministic | **False.** Rank keys are `(priority, score, rule_id)` then Priority Engine re-sorts the same tuple. | priority |
| — | Priority rule không được production load | **Partial / not a selection blocker.** `05_priority_rules.csv` is **metadata-only** (not merged). Executable priority is the `priority` column on 01–04 plus `PriorityService` (`max_rules_per_section=1`). | rule / priority |
| — | Special/follow bị main override sai | **False on CASE-0001** (no special; follow candidate rejected). In general special (95) and validated follow (90) outrank main (60–80). | priority |
| — | Pattern tự tính Ten Gods bằng mapping khác G1-01 | **False as mapping.** Uses `engines.bazi_engine.ten_god.ten_god_name` (same function G1-01 uses). Does **not** call `TenGodsEngine` (that runs later). | cross-engine |
| — | Hai final patterns không có winner | **False.** `select_final` takes `resolved[0]` only. | priority |
| — | Duplicate canonical IDs | **False.** 27 loaded `rule_id` values are unique. | rule |
| — | CASE-0001 không tái tạo được | **False.** Live orchestrator: `chinh_an` / `Chính Ấn` / score `72` / priority `72`. | calculation |

Not blockers, but they **block freeze** until Product Owner decides / Phase 2 publishes evidence:

| ID | Finding | Layer |
|----|---------|-------|
| **G1** | Main pattern is `month branch → main stem → Ten God → pattern` with **no 透干 gate**. CASE-0001 Kỷ (Chính Ấn) does **not** appear as a visible stem. | calculation (methodology review) |
| **G2** | `PatternView` / `to_portal_dict()` drop `candidate_patterns`, `matched_rules`, `final_pattern`, `confidence`, `reason`. Presentation cannot show compact evidence without reading internals. | contract / presentation |
| **G3** | Tests and golden snapshot still treat CASE-0001 as **Chính Quan** when `build_pattern_context` is skipped (`pat_fallback`). Production path is Chính Ấn. | test |

---

# 1. Canonical production implementation

## 1.1 Production owner (frozen)

`beta/BETA0_ANALYTICAL_TRUTH_LOCK.md` assigns Pattern to:

```text
Pattern
    engines/pattern_engine
```

It must not be invented in Narrative.

Public entry:

```text
from engines.pattern_engine import PatternEngine
from engines.pattern_engine.utils.context_builder import build_pattern_context

ctx = build_pattern_context(bazi_chart, calendar=calendar)
result = PatternEngine().calculate(ctx)
```

| Item | Value |
|------|-------|
| Canonical module | `engines/pattern_engine` |
| Public class | `PatternEngine` |
| Public method | `PatternEngine.calculate(context: PatternContext) -> PatternResult` |
| Input model | `engines.pattern_engine.context.PatternContext` |
| Output model | `engines.pattern_engine.engine.PatternResult` (also unused `models/pattern_result.py` `PatternResultModel`) |
| Context builder | `engines.pattern_engine.utils.context_builder.build_pattern_context` |
| Rule loader | `engines.pattern_engine.loader.PatternLoader` |
| Matcher | `engines.pattern_engine.matcher.PatternMatcher` |
| Evaluator / pipeline | `engines.pattern_engine.calculator.PatternCalculator` |
| Follow detector | `engines.pattern_engine.calculators.follow_pattern.FollowPatternCalculator` |
| Conflict | `engines.pattern_engine.conflict.resolve_exclusive_conflicts` |
| Priority mechanism | `engines.priority_engine.PriorityService.for_matched_rules(max_rules_per_section=1)` |
| Engine version | `__version__ = "1.0.0"` (`engines/pattern_engine/__init__.py`) |
| Rule DB version | `database/14_pattern/README.md` **2.0** (2026-07-29) |
| Default DB path | `database/14_pattern` |

Production callers:

| Caller | What it does |
|--------|----------------|
| `applications/api/services/orchestrator.py` | Stage 4: `build_pattern_context` → Strength/Temperature overlay → `PatternEngine.calculate` → `build_pattern_view` |
| `applications/production/engine_runner.py` | Same engine + `build_pattern_context` |
| `applications/api/services/pattern_truth.py` | `PatternResult.to_portal_dict()` → `PatternView` |

## 1.2 Other Pattern implementations

| Module | Classification | Production leak? |
|--------|----------------|------------------|
| `engines/pattern_engine` | **canonical** | Yes — Orchestrator / production runner |
| `engines/pattern/` | adapter wrapper (`from engines.pattern_engine ...`) | Same engine if imported |
| `engines/bazi_engine/pattern/` | **legacy** (imports `bazi_engine.ten_gods.service`) | **No** — Orchestrator does not call it |
| `engines/analysis_engine/integration/pattern_stage.py` | package bind; “does not recompute identification” | **No** — applications do not run this pipeline |
| `engines/interpretation_engine/.../pattern/rule_engine.py` | re-matches `database/14_pattern` for interpretation facts | Does not write `AnalysisResult.pattern` on the analyze path |
| `knowledge/packages/pattern/` | interpretation knowledge package | unused by PatternLoader |
| `knowledge/rule_database/04_pattern_rules/` | legacy JSON rules | unused by PatternLoader |
| `database/15_score_engine/05_pattern/` | Score Engine success/failure weights | **not** Pattern selection |
| `database/20_knowledge/07_patterns.csv` | knowledge catalog | unused by PatternLoader |
| `SpecialPatternCalculator` / `CombinationCalculator` / `StructureCalculator` | **unused** in `PatternCalculator.calculate` | No — special/combination are **CSV-matched**, not these classes |
| `engines/pattern_engine/rules/priority.py` `PriorityResolver` | unused by production calculator | Interpretation matcher may use it |

---

# 2. Pattern dependency graph

Production analyze order (Orchestrator):

```text
CalendarEngine
    ↓
BaziEngine          (pillars, hidden_stems, visible ten_gods list)
    ↓
build_pattern_context   (Lệnh Tháng + families; ten_god_name)
    ↓
StrengthEngine          → pattern_context.strength_level / strength_score
TemperatureEngine       → pattern_context.temperature_type  (overwrites branch map)
    ↓
PatternEngine.calculate
    ↓
UsefulGodEngine         reads pattern_result.pattern + follow_type
    ↓
RuleContext publish / Score / TenGodsEngine / Luck / Interpretation
```

```text
Strength ──feeds──► PatternContext.strength_level     (no CSV rule reads it)
Temperature ──feeds──► PatternContext.temperature_type (no CSV rule reads it)
BaZi ten_god_name ──used by──► month_branch_ten_god / month_stem_ten_god / Follow
TenGodsEngine ──after Pattern──► display payload only (not used to select cách)
Pattern.pattern ──read by──► Useful God (main_pattern / special_pattern / follow_type)
Score ──does not remap──► pattern code; may overlay dung_than / than_vuong_nhuoc labels
```

No engine replaces `pattern` / `cach_cuc` after Pattern Engine. Score stage calls `enrich_result_from_rule_context`, which **refreshes labels** (`than_vuong_nhuoc` from Strength, `dung_than` from Useful God) and keeps `cach_cuc` from `pattern_display_label(pattern)`.

---

# 3. Rule inventory

Production load: `PatternLoader.load_rules()` concatenates:

1. `01_main_pattern.csv` (required; alias `rules.csv` unused)
2. `02_special_pattern.csv`
3. `03_follow_pattern.csv`
4. `04_combination_pattern.csv`

**Not merged:** `05_priority_rules.csv`, `06_pattern_conditions.csv`, `07_pattern_examples.csv`.

| File | On disk | Loaded as match rules | Category |
|------|--------:|----------------------:|----------|
| `01_main_pattern.csv` | 11 | 11 | 10 main + `pat_fallback` |
| `02_special_pattern.csv` | 5 | 5 | Khúc Trực, Viêm Thượng, Nhuận Hạ, Giá Sắc, Giá Vượng |
| `03_follow_pattern.csv` | 6 | 6 | Tòng Vượng/Tài/Sát/Quan/Nhi/Ấn |
| `04_combination_pattern.csv` | 5 | 5 | Quan Ấn, Sát Ấn, Thực sinh Tài, Thương phối Ấn, Tài Quan Song Mỹ |
| `05_priority_rules.csv` | 3 | **0** | documentation markers |
| `06_pattern_conditions.csv` | 24 | **0** | condition library |
| `07_pattern_examples.csv` | 16 | **0** | examples |

README claimed 4 special rules; disk has **5** (`spe_jw_01` Giá Vượng).

Main 10 (Ziping lệnh-tháng families):

| Code | Vietnamese (labels.py) | Rule | Lệnh tháng Ten God |
|------|------------------------|------|--------------------|
| `chinh_quan` | Chính Quan | `pat_cq_01` | Chính Quan |
| `that_sat` | Thất Sát | `pat_ts_01` | Thất Sát |
| `chinh_tai` | Chính Tài | `pat_ct_01` | Chính Tài |
| `thien_tai` | Thiên Tài | `pat_tt_01` | Thiên Tài |
| `thuc_than` | Thực Thần | `pat_tht_01` | Thực Thần |
| `thuong_quan` | Thương Quan | `pat_thuq_01` | Thương Quan |
| `chinh_an` | Chính Ấn | `pat_ca_01` | Chính Ấn |
| `thien_an` | Thiên Ấn | `pat_ta_01` | Thiên Ấn |
| `ty_kien` | Kiến Lộc (label) / Tỷ Kiên | `pat_tyk_01` | Tỷ Kiên |
| `kiep_tai` | Dương Nhẫn (label) / Kiếp Tài | `pat_ktai_01` | Kiếp Tài |

`pat_fallback`: empty conditions, `pattern=chinh_quan`, priority 1. Always matches; rejected when any substantive rule also matches.

---

# 4. Rule load status

Live `PatternLoader` on CASE-0001:

| Check | Result |
|-------|--------|
| Rows loaded | **27** |
| All `enabled=true` | **Yes** |
| Duplicate `rule_id` | **No** |
| Malformed JSON conditions | None observed (loader + matcher ran) |
| Disabled rules | **0** |
| Orphan on disk vs matcher | `05` / `06` / `07` not matched (intentional for 06/07; 05 unused) |
| Score-engine / knowledge pattern files | not reachable by PatternLoader |

---

# 5. Pattern selection pipeline

Actual code path (`PatternCalculator.calculate`), not the conceptual ideal:

```text
load CSV 01+02+03+04
    ↓
1. detect_candidates     every enabled rule whose ALL conditions match
    ↓
2. FollowPatternCalculator.detect(context)   → follow_type or None
    ↓
3. validate_candidates
      follow CSV rows require follow_type and matching tong_* code
      pat_fallback rejected if any non-follow substantive candidate exists
    ↓
4. resolve_exclusive_conflicts
      at most one of standard_main / follow / special group
      combination is a separate section (not exclusive vs main)
    ↓
5. PriorityService.resolve_matched_interpretation_rules
      max 1 rule per section; sort (priority, score, rule_id)
    ↓
6. select_final
      winner = resolved[0]
      pattern code + description → cach_cuc label
```

| Stage | What it does |
|-------|----------------|
| Candidate creation | CSV condition match on `PatternContext` fields |
| Candidate elimination | Validation (follow gate, fallback) then exclusive groups then priority cap |
| Special | CSV `02_*` only (calculator class unused) |
| Follow | CSV `03_*` **and** `FollowPatternCalculator.detect` (support ratio ≤ 0.25 or ≥ 0.70) |
| Combination | CSV `04_*`; **can become the final pattern** if it wins priority — not evidence-only |
| Final winner | `resolved[0]` in `select_final` |

Empty-condition match: `PatternMatcher.match` returns `True` when `conditions == []` (`pat_fallback`, and would also fire `05_*` if those rows were loaded).

---

# 6. Nguyệt lệnh logic

## 6.1 Which “month” Pattern uses

| Factor | Used for **calendar month identity** | Used for **Pattern selection** |
|--------|--------------------------------------|--------------------------------|
| Solar terms (12 tiết) | **Yes** — `BaziEngine` month branch via `SolarTermEngine.get_bazi_month` | Indirect: chooses the branch only |
| Month Branch | Yes | **Yes** — `month_branch` |
| Month Stem | Yes | Computed as `month_stem_ten_god`; **no main/special rule reads it** |
| Hidden stems (all three) | Stored `month_hidden_stems` | **Not scored** |
| Main qi | Hardcoded `_BRANCH_MAIN_STEM` | **Yes — this is Lệnh Tháng** |
| Middle / residual qi | In hidden list (Sửu: Quý, Tân) | **No** |
| Season | From month branch map | Available; main rules unused; special uses `month_branch_element` |
| Solar term **name** | Calendar payload | **Not read** by Pattern |
| TemperatureEngine | Overwrites `temperature_type` | **No CSV uses it** |

Main-stem table (`context_builder._BRANCH_MAIN_STEM`), Sửu = **Kỷ**. Same hidden table as `BaziEngine.HIDDEN`.

Ten God of lệnh: `ten_god_name(day_master, main_stem)` → `PatternContext.month_branch_ten_god`.

Every main rule is:

```json
{"field": "month_branch_ten_god", "operator": "==", "value": "<Ten God>"}
```

## 6.2 Review flag (Task 4)

This **is** `month branch → fixed Ten God → pattern`.

Classical Ziping often also requires **透** (command god appearing among heavenly stems) and may weigh middle/residual qi. Production does **not**. Marked for Product Owner review. Not a CASE-0001 reproducibility failure: the live winner is exactly this mapping.

---

# 7. Thấu can logic

Production **does not define** a `thau_can` / `transmitted` field. No rule condition checks stem appearance.

Audit matrix (behavior today; **not implemented as tests in Phase 1**):

| Case | Production |
|------|------------|
| Hidden stem of nguyệt chi appears as year/month/hour stem | Overlap can be derived from pillars; **unused** |
| Year / month / hour stems considered | Visible `ten_gods_list` is year+month+hour only (day = Nhật Chủ dropped) |
| Nhật can counted as 透 | **No** — labeled `Nhật Chủ`, stripped from `ten_gods_list` |
| Same element, different stem (Kỷ vs Mậu) | **Not treated as 透 of Chính Ấn**. Mậu = Thiên Ấn |
| Must exact stem vs element | N/A — no 透 operator |
| Multiple stems 透 | N/A |

CASE-0001 overlap: month hidden `{Kỷ, Quý, Tân}`; visible stems `{Bính, Tân, Mậu}`. Exact-stem 透 of residual qi **Tân** (Kiếp Tài) only. Command god **Kỷ is not 透**.

Follow detector re-calls `ten_god_name` on pillars + hidden stems **and** already listed `ten_gods` — possible double-count on other charts. CASE-0001 `follow_type` still `None`.

---

# 8. Priority logic

Executable order (CSV `priority` column, higher wins):

| Layer | Priority | Source |
|-------|----------|--------|
| Special | 93–95 | `02_special_pattern.csv` |
| Follow (if calculator detects) | 90 | `03_follow_pattern.csv` |
| Combination | 82–86 | `04_combination_pattern.csv` |
| Main | 60–80 | `01_main_pattern.csv` |
| Fallback | 1 | `pat_fallback` |

`05_priority_rules.csv` (200/190/185 markers, empty conditions) is **not loaded**. README hierarchy is approximated by these numbers, not by executing 05.

Tie-break within exclusive group and Priority Engine:

```text
(priority, score|confidence, rule_id)  descending
```

`rule_id` string is the last key — deterministic, not dict-hash order.

`max_rules_per_section=1` keeps one winner in `standard_main`, `follow`, `special`, `combination`, `other`. `select_final` then picks the globally highest among those section winners.

**Implication:** a matching combination (e.g. Sát Ấn, priority 85) **beats** a matching main (Chính Ấn, 72) on other charts. Combination is not “evidence only”. CASE-0001 combination did **not** match (see §10).

---

# 9. CASE-0001 full trace

Golden chart: Nguyễn Tiến Sơn, 1987-01-21 04:30, male.

| Pillar | Stem Branch | Visible Ten God vs Canh |
|--------|-------------|-------------------------|
| Year | Bính Dần | Thất Sát |
| Month | Tân Sửu | Kiếp Tài |
| Day | Canh Ngọ | Nhật Chủ |
| Hour | Mậu Dần | Thiên Ấn |

`BaziChart.ten_gods` = `['Thất Sát', 'Kiếp Tài', 'Nhật Chủ', 'Thiên Ấn']`.

## 9.1 Facts the engine actually reads

Used for the **winning** rule:

| Fact | Value | Source |
|------|-------|--------|
| Day Master | Canh | BaZi |
| Month Branch | Sửu | Calendar solar-term month |
| Main stem of Sửu | Kỷ | `_BRANCH_MAIN_STEM` |
| `month_branch_ten_god` | **Chính Ấn** | `ten_god_name("Canh", "Kỷ")` |

Also computed (not used by `pat_ca_01`):

| Fact | Value |
|------|-------|
| Month Stem | Tân → Kiếp Tài |
| `month_hidden_stems` | Kỷ, Quý, Tân |
| `ten_gods_list` | Thất Sát, Kiếp Tài, Thiên Ấn |
| `officer_elements` | [Thất Sát] |
| `resource_elements` | [Thiên Ấn] |
| `companion_elements` | [Kiếp Tài] |
| `season` | winter / late_winter / cold (then TemperatureEngine may overwrite type) |
| `strength_level` | set by orchestrator to `strong` **after** builder; unused by CSV |

Not used: solar term name, Useful God, TenGodsEngine payload, Score.

## 9.2 Month branch Sửu tàng

| Hidden stem | vs Canh | Role in production |
|-------------|---------|-------------------|
| Kỷ | **Chính Ấn** | **Main qi / Lệnh Tháng — winner** |
| Quý | Thương Quan | stored only |
| Tân | Kiếp Tài | stored only; also month stem |

No weighting of the three qi. Command is 100% Kỷ.

## 9.3 Visible stems vs 透

| Stem | Ten God | 透 of nguyệt chi? | Used as pattern evidence? |
|------|---------|-------------------|---------------------------|
| Bính | Thất Sát | No | `ten_gods_list` only (follow/combination) |
| Tân | Kiếp Tài | Yes (residual of Sửu) | unused for main |
| Canh | Nhật Chủ | excluded | no |
| Mậu | Thiên Ấn | same element as Kỷ, **different stem** | unused for main |

---

# 10. CASE-0001 candidate list

Live `PatternCalculator.calculate` (full `build_pattern_context`, Strength not required for this winner):

| Candidate | Rule | Evidence | Matched? | Validated? | Priority | Score | Final |
|-----------|------|----------|----------|------------|----------|-------|-------|
| `chinh_quan` | `pat_fallback` | empty conditions | Yes | **No** (`fallback_superseded`) | 1 | 10 | discarded |
| `chinh_an` | `pat_ca_01` | `month_branch_ten_god == Chính Ấn` | Yes | **Yes** | 72 | 72 | **winner** |
| `tong_sat` | `fol_tsat_01` | `ten_gods_list contains Thất Sát` | Yes | **No** (`follow_not_detected`) | 90 | 86 | discarded |

Not matched (selected): other nine main rules, all special (Kim day / Thổ month ≠ Giá Sắc), other follow rows, all combination rows (`com_san_01` needs **Chính Ấn in `ten_gods_list`**, which only has Thiên Ấn / Thất Sát / Kiếp Tài).

`follow_type` from calculator: **None** (support ratio not in tòng bands).

`secondary_patterns`: `[]`.

---

# 11. Why final = Chính Ấn

```text
Calendar month branch = Sửu
    → main stem Kỷ
    → ten_god_name(Canh, Kỷ) = Chính Ấn
    → pat_ca_01 matches
    → fallback and tong_sat rejected
    → exclusive group standard_main keeps pat_ca_01
    → resolved[0] = chinh_an
    → pattern_display_label("chinh_an") = "Chính Ấn"
```

Orchestrator `analyze` payload:

```text
pattern = chinh_an
cach_cuc = Chính Ấn
score = 72.0
priority = 72
```

`confidence` on `PatternResult` is `72/100 = 0.72` (rule score scale), **not** published on `PatternView`.

This is **not** a frontend fallback and **not** a simple month-branch string map in the UI. It **is** a simple lệnh-tháng map **inside** the canonical engine.

---

# 12. PatternResult contract

`PatternResult` (engine) vs `PatternView` (API / Portal):

| Requested field | Engine | PatternView / portal JSON |
|-----------------|--------|---------------------------|
| pattern id | `pattern`, `final_pattern` | `pattern` (`chinh_an`) |
| Vietnamese name | `cach_cuc` | `cach_cuc` |
| category | internal `section` only | **absent** |
| candidate patterns | `candidate_patterns` | **stripped** |
| winning rule | in calculator `matched_rules` / discarded | **stripped** (`matched_rules` not in view) |
| evidence | `reason` / `success_reason` / description | **stripped** |
| confidence | `confidence` 0–1 | **absent** (Report uses `score` 72 as “Độ tin cậy”) |
| priority | `priority` | `priority` |
| reason codes | `reason` | **absent** |
| follow | `follow_type` | **absent** on view |
| Extra view fields | filled from RuleContext | `than`, `than_vuong_nhuoc`, `tong_cach`, `dung_than`, `hy_than`, `ky_than`, `dieu_hau` |

`to_portal_dict()` is the contraction. Presentation cannot show §11 evidence from the public contract alone.

After full `analyze`, `dung_than` on the pattern slice is copied from Useful God (`Thực Thần`). That is **not** Pattern selection; it is label overlay.

---

# 13. Cross-engine dependencies

| Relation | Production fact |
|----------|-----------------|
| Strength → Pattern | Orchestrator writes `strength_level` / `strength_score` onto context **before** calculate. **No loaded pattern rule reads them.** Follow uses its own stem-count ratios. |
| Temperature → Pattern | Orchestrator overwrites `temperature_type`. **No loaded rule reads it.** |
| Ten Gods → Pattern | Pattern **recomputes** lệnh and families via `ten_god_name`, not `TenGodsEngine`. Mapping matches G1-01. Visible list is BaZi four-pillar stems only. |
| Pattern → Useful God | `build_useful_god_context(..., pattern_result)` reads `pattern` (code) and `follow_type`. CASE-0001 Useful God = **Thực Thần** with `strength_level=strong`. |
| Override after Pattern | Score/Interpretation **do not change** `pattern` / `cach_cuc`. They overlay Useful God / Strength labels onto the pattern slice. |

---

# 14. Portal / Report / PDF / DOCX binding

Exact field path for CASE-0001 **Cách cục: Chính Ấn**:

```text
PatternEngine.cach_cuc
  → PatternView.cach_cuc
  → data.pattern.cach_cuc
```

| Surface | Path | CASE-0001 |
|---------|------|-----------|
| API analyze | `payload["pattern"]["cach_cuc"]` | Chính Ấn |
| Canonical Desktop | `pickStr(pattern, ["cach_cuc", "pattern"])` | Chính Ấn |
| Result V2 Technical | `pattern.cach_cuc ?? pattern.pattern` | Chính Ấn |
| Full Report VM | `pattern.cach_cuc \|\| pattern.pattern` | Chính Ấn |
| BaZi knowledge card | `pattern.cach_cuc` | Chính Ấn |
| Legacy HTML | `pattern.cach_cuc` then aliases `pattern_name` / `ge_ju` / `main_pattern` of the **same object** | Chính Ấn if API filled |
| Report V1 | `analysis.pattern.cach_cuc` → `primary_pattern` | Chính Ấn |
| PDF / DOCX | `build_presented_report` section `06. Mệnh cục / Cách cục` **Cách chính** | same source |

Portal uses the **final** `cach_cuc`, not `candidate_patterns[0]`.

Legacy `formatLabel` can map code `chinh_an` → `Chính Ấn` if only the code is present. That is display of the canonical id, not a Ten Gods recompute.

Report extras (semantic mix, not a second pattern):

- `secondary_patterns` = `[tong_cach]` → also “Chính Ấn”
- `follow_pattern` bound to `dieu_hau` = **Đắc lệnh** (month status), not a Tòng cách
- `confidence` shown as `72.0` (rule score)

No live renderer derives Cách cục from Ten Gods independently of `data.pattern`.

---

# 15. Regression test coverage

| Area | Coverage today |
|------|----------------|
| 10 main patterns | CSV examples in `07_pattern_examples.csv` **not executed** as pytest. No matrix test of all 10 lệnh-tháng gods. |
| Special | no dedicated engine tests |
| Follow | no dedicated calculator tests in `tests/pattern/` |
| Combination | none |
| Multiple candidates / priority collision / tie-break | none targeting PatternCalculator |
| No-pattern / fallback | `pat_fallback` implicitly: incomplete `PatternContext` → `chinh_quan` |
| Malformed context | `tests/pattern/test_pattern_engine.py` empty context → success + some pattern (fallback) |
| CASE-0001 production path | `knowledge/pilot/cases/CASE-0001/actual.json` has `chinh_an`. Report golden `primary_pattern=Chính Ấn`. |
| CASE-0001 **false lock** | `applications/api/tests/test_phase3_unified_pattern.py` builds context **without** `build_pattern_context` and expects **Chính Quan**. `tests/golden_dataset/snapshots/pattern_engine/case_0001.json` still says `chinh_quan`. |
| `tests/pattern/test_pattern_matcher.py` | wraps stub `engines.pattern.matcher.PatternMatcher.match(context)` returning `[]` — **not** the production matcher |

Gaps: 10-main matrix, special, follow, combination, collision, tie-break, incomplete-context documented as fallback, production CASE-0001 pytest on `build_pattern_context`.

---

# 16. Gaps discovered

1. Lệnh Tháng = main qi only; 透 and middle/residual qi unused.
2. `month_stem_ten_god` unused by selection.
3. Combination can **replace** main when it matches (higher priority).
4. Follow CSV is loose (`contains Thất Sát`); real gate is `FollowPatternCalculator` (hard-coded ratios 0.25 / 0.70, possible double-count).
5. `05_priority_rules.csv` unused; empty conditions would match globally if loaded.
6. Public contract drops candidates / winning rule / evidence.
7. Pattern slice carries Useful God / Strength labels (`dung_than`, `than_vuong_nhuoc`).
8. Report maps `dieu_hau` → “Theo cách”.
9. Tests/golden can still encode CASE-0001 as Chính Quan (fallback).
10. Unused calculator classes vs CSV-driven special/combination.
11. Interpretation has a second matcher over the same CSV (does not overwrite analyze `PatternView`).

---

# 17. Gap classification

| Gap | Class |
|-----|--------|
| Main qi only / no 透 | calculation (PO methodology) |
| Combination can win over main | priority / rule |
| Follow ratios hard-coded | calculation |
| `05_priority_rules.csv` not loaded | rule / priority |
| Candidates & evidence stripped | contract |
| Portal/Report name binding | presentation — **OK** |
| Report follow/confidence semantics | adapter / presentation |
| CASE-0001 Chính Quan tests/snapshot | test |
| Unused special/combination Python calculators | unused code (not freeze-blocking) |

---

# 18. Minimum changes for G1-03 PASS

Do **not** change the lệnh-tháng formula unless Product Owner rejects main-qi-only.

1. **Keep** `pat_ca_01` / `chinh_an` / `Chính Ấn` for CASE-0001.
2. **Publish compact evidence** already in the calculation (no new astrology), e.g. on Strength-style additive fields or diagnostics:
   `Căn cứ: Nguyệt lệnh Sửu · khí chính Kỷ → Chính Ấn · rule pat_ca_01`
   Do not add personality/career narrative.
3. **Bind** Portal/Report Cách cục evidence from that field; do not invent from Ten Gods.
4. **Lock tests** to `build_pattern_context` + Orchestrator: CASE-0001 `chinh_an`, not `pat_fallback` Chính Quan. Do not “fix” by changing golden expected pattern to Quan.
5. **PO decisions required before any formula edit:**
   - Accept V1.0 lệnh = main qi without 透? If no → Phase 2 calculation change (out of “minimal binding” repair).
   - May combination remain a final pattern, or evidence-only?
6. Optionally clarify Report “Theo cách” vs `dieu_hau` (not Pattern winner).
7. Do not load `05_priority_rules.csv` as match rules without redesign (empty conditions).
8. Do not expand taxonomy. Do not start G1-04 in this gate.

---

# Minimum evidence proposal (not implemented)

Existing facts only:

**Cách cục:** Chính Ấn

**Căn cứ:** Nguyệt lệnh Sửu · khí chính Kỷ (Chính Ấn) · `pat_ca_01`

Do not show: tính cách Chính Ấn, nghề, tài vận, cát/hung, khuyến nghị (V1.1).

---

# PHASE 1 STATUS

CASE-0001 `Chính Ấn` is canonical Pattern Engine output. Portal/Report/PDF/DOCX already display that name from `pattern.cach_cuc`. Freeze is blocked by missing public evidence, methodology review (透 / combination-as-winner), and tests that still lock the fallback Chính Quan.

`G1-03 PHASE 1: AUDIT PASS / G1-03 NOT READY — REPAIR REQUIRED`
