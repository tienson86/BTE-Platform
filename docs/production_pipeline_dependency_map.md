# BTE Platform — Production Pipeline Dependency Map (Pre-Fix)

**Priority:** BLOCKER  
**Date:** 2026-07-27  
**Status:** Diagnostic only — **no code modified**  
**Prerequisite:** [`production_pipeline_contract_audit.md`](production_pipeline_contract_audit.md) accepted as diagnostic baseline

**Goal of fixes (not implemented here):** Every Portal tab renders from **one** shared `AnalysisResult` object — no parallel recalculation, no divergent ViewModels, no legacy cache as contract source.

---

## 1. Naming reality (types in repo)

| Audit name | Actual production type | File |
|------------|------------------------|------|
| `CalendarResult` | `CalendarResult` (dataclass) | `engines/calendar_engine/engine.py` |
| `BaziResult` | **`BaziChart`** (compact facade; no `BaziResult` class) | `engines/bazi_engine/engine.py` |
| `PatternResult` | `PatternResult` (dataclass) | `engines/pattern_engine/engine.py` |
| `ScoreResult` | `ScoreResult` (dataclass) | `engines/score_engine/result.py` |
| `InterpretationResult` | `InterpretationResult` (dataclass) | `engines/interpretation_engine/legacy_builder.py` |
| `ReportResult` | **`Report`** (`ReportModel` path) + **`NarrativeReport`** | `engines/report_engine/report.py`, `engines/narrative_engine/models.py` |
| `AnalysisResult` | **Does not exist** | — |

Legacy / duplicate types (not production SSOT):

| Type | Location | Role |
|------|----------|------|
| `CalendarResult` (alternate) | `engines/calendar_engine/models.py` | Older model module |
| `BaziChart` (full package) | `engines/bazi_engine/models/bazi_chart.py`, `pillars/*` | Not wired to `applications/api` orchestrator |
| `PatternResultModel` | `engines/pattern_engine/models/pattern_result.py` | Internal model layer |
| `PatternResult` | `engines/bazi_engine/models.py` | Different domain — not Pattern Engine |
| Loose `dict` payload | `OrchestratorService._run` | **De facto** HTTP contract today |

---

## 2. End-to-end dependency graph (production path)

```
BirthRequest
    │
    ▼
OrchestratorService._run()                    applications/api/services/orchestrator.py
    │
    ├─► CalendarEngine.build ──► CalendarResult (raw)
    │         │
    │         ├─► _shape_calendar ──► data.calendar (HTTP VM) ──► Portal calendar.js
    │         │
    ├─► BaziEngine.build(cal) ──► BaziChart (raw)
    │         │
    │         ├─► _shape_bazi ──► data.bazi (HTTP VM) ──► Portal bazi.js
    │         │
    │         ├─► PatternContext(stubs) ──► PatternEngine ──► PatternResult (raw)
    │         │                                    │
    │         │                                    └─► _shape_pattern ──► data.pattern ──► pattern.js
    │         │
    │         ├─► ScoreEngine.calculate({cal,bazi,pattern}) ──► ScoreResult (raw) ⚠ C1
    │         │                                    │
    │         │                                    └─► _shape_score ──► data.score ──► score.js
    │         │
    │         └─► InterpretationEngine.run({...}) ──► InterpretationResult (raw)
    │                      │
    │                      ├─► _shape_interpretation ──► data.interpretation ──► interpretation.js
    │                      └─► re-_shape_pattern (regex enrich)
    │
    ├─► ReportEngine.render(interp) ──► Report (raw) ──► DISCARDED for HTTP
    ├─► NarrativeEngine.compose(interp, report) ──► NarrativeReport ──► DISCARDED
    │
    └─► _shape_report_like(interp VM) ──► data.report + data.narrative ──► narrative.js + reports.js
              │
              └─► executive/summary_builder (full data) ──► Narrative tab overlay

Parallel (not in engine chain for Bazi pillars):
    FengShuiEngine.calculate ──► GuaResult.to_dict ──► data.feng_shui + copied to calendar VM

Portal persistence:
    analyze.js ──► ResultStore.save({input, data}) ──► result.js ──► data[stage] presenters
```

**Critical fork:** HTTP consumers read **shaped VMs**; Pattern / Score / Interpretation engines read **raw engine objects** (often stubs). That is the architectural split blocking “one AnalysisResult.”

---

## 3. Per-object dependency sheets

### 3.1 CalendarResult

| Dimension | Detail |
|-----------|--------|
| **Single Source of Truth (intended)** | `CalendarEngine.build()` → `CalendarResult` |
| **SSOT today (actual)** | Split: calendar fields from `CalendarResult`; **Can Chi** from `BaziChart` via `_shape_calendar(bazi_data)`; **feng shui** from `FengShuiEngine` |
| **Producer** | `CalendarEngine.build` (`engines/calendar_engine/engine.py`); enrichment in `OrchestratorService._shape_calendar` |
| **Consumers (downstream)** | Raw: Score/Interp via `RuleContextBuilder._build_calendar`; HTTP: `data.calendar`; Portal `calendar.js`; Summary Builder |
| **API contract** | `to_jsonable(calendar)` + `year/month/day/hour_can_chi`, `cung_phi`, `menh_quai`, `nhom_trach`, `gua_name` |
| **Portal binding** | `presenters/calendar.js`: `solar_date`, `lunar_*`, `*_can_chi`, `solar_term`, feng fields; timezone from cal or **form input** |
| **Recalculated elsewhere?** | Can Chi **re-derived from Bazi pillars** in orchestrator (not Calendar Engine) |
| **Legacy** | `engines/calendar_engine/models.py` `CalendarResult`; legacy `api/` stack uses same `CalendarEngine` |
| **Duplicated ViewModels?** | Yes: raw `CalendarResult` vs shaped `data.calendar` vs Summary Builder date strings |

---

### 3.2 BaziChart (BaziResult)

| Dimension | Detail |
|-----------|--------|
| **SSOT (intended)** | One chart object feeding all downstream engines and Portal |
| **SSOT today** | **Dual:** Portal sees `_shape_bazi` VM; engines see compact `BaziChart` with stub `ten_gods`, empty `shensha` |
| **Producer** | `BaziEngine.build` (`engines/bazi_engine/engine.py`) — production facade, not `pillars/pillar_builder.py` |
| **Consumers** | `PatternContext`, `ScoreEngine`, `InterpretationEngine`, `RuleContextBuilder`; HTTP `data.bazi`; Portal `bazi.js`, Summary Builder, executive |
| **API contract** | Per-pillar `stem/branch/hidden_stems/ten_god/nap_am/truong_sinh`; `day_master`, `day_master_element`, `day_master_yin_yang`; flat `ten_gods[]`, `shensha[]` |
| **Portal binding** | `bazi.js`: pillar keys; **element/âm dương from client `STEM_META`** (ignores API element fields) |
| **Recalculated elsewhere?** | `_shape_bazi` recomputes `ten_god`, `nap_am`, `truong_sinh` from DB lookups; Portal re-slices `hidden_stems` |
| **Legacy** | Full `PillarService` / `PillarBuilder` package (`engines/bazi_engine/pillars/*`) — **not** on production API path |
| **Duplicated ViewModels?** | **Yes — core blocker:** HTTP Bazi VM ≠ raw `BaziChart` passed to Pattern/Score/Interp |

---

### 3.3 PatternResult

| Dimension | Detail |
|-----------|--------|
| **SSOT (intended)** | `PatternEngine.calculate(PatternContext)` → `PatternResult` |
| **SSOT today** | Engine `PatternResult` + orchestrator `_shape_pattern` + optional regex scrape from Interpretation |
| **Producer** | `PatternEngine` → `PatternService` → `PatternCalculator` (`engines/pattern_engine/`) |
| **Consumers** | Score (as input dict), Interpretation, HTTP `data.pattern`; Portal `pattern.js`; Summary Builder |
| **API contract** | `success`, `score`, `priority`, `pattern`, `cach_cuc`, optional `than_vuong_nhuoc`, `dung_than`; **no** `matched_rules` |
| **Portal binding** | `pattern.js` `FIELDS`: `than`, `than_vuong_nhuoc`, `cach_cuc`, `tong_cach`, `dung_than`, `hy_than`, `ky_than`, `dieu_hau` |
| **Recalculated elsewhere?** | `_humanize_token` / `PATTERN_LABELS` in Portal; regex enrichment from interpretation sentences |
| **Legacy** | `PatternResultModel`; pattern rules in `database/14_pattern/` |
| **Duplicated ViewModels?** | Yes: raw result vs shaped API vs Portal label maps vs Summary Builder `formatLabel` |

---

### 3.4 ScoreResult

| Dimension | Detail |
|-----------|--------|
| **SSOT (intended)** | `ScoreEngine.calculate(RuleContext)` → `ScoreResult` |
| **SSOT today** | `ScoreResult` internally correct structure but fed **empty RuleContext** (C1); API strips `details` |
| **Producer** | `ScoreEngine.calculate` (`engines/score_engine/engine.py`) |
| **Consumers** | InterpretationEngine, HTTP `data.score`, Portal `score.js`, Summary Builder, report conclusion text |
| **API contract** | Whitelist: `total_score`, module scores, `grade`, `confidence`, `recommendation`, `success` |
| **Portal binding** | `score.js`: totals + **expects** `details.*` series, `interpretation_score`, `priority` — absent in API |
| **Recalculated elsewhere?** | Portal bar widths / gauge angles (display only); **no** rescoring |
| **Legacy** | `api/services/pipeline_service.py` registers same `ScoreEngine` |
| **Duplicated ViewModels?** | Yes: full `ScoreResult.to_dict()` (with `details`) vs `_shape_score` whitelist |

---

### 3.5 InterpretationResult

| Dimension | Detail |
|-----------|--------|
| **SSOT (intended)** | `InterpretationEngine.run` → `InterpretationResult` |
| **SSOT today** | Raw result discarded for HTTP; `_shape_interpretation` builds new `sections[]`; Report/Narrative rebuilt from that |
| **Producer** | `InterpretationEngine.run` (`engines/interpretation_engine/engine.py`) |
| **Consumers** | ReportEngine.render, NarrativeEngine.compose (engine objects); HTTP `data.interpretation`; `_shape_report_like`; Portal `interpretation.js` |
| **API contract** | `sections[{id,title,body}]`, `section_count`, `sentence_count`, `confidence`; **no** `summary`, `rules_used`, `rule_id` |
| **Portal binding** | `interpretation.js`: `sections[]` primary; legacy top-level keys optional |
| **Recalculated elsewhere?** | `_sanitize_sentence`, section grouping in orchestrator; Portal `humanizeKey` / join only |
| **Legacy** | `legacy_builder.py` name; raw `sections` dict not exposed |
| **Duplicated ViewModels?** | Yes: `InterpretationResult` vs shaped sections vs Report/Narrative clone |

---

### 3.6 Report / Narrative (ReportResult)

| Dimension | Detail |
|-----------|--------|
| **SSOT (intended)** | Report Engine and/or Narrative Engine output |
| **SSOT today** | **`_shape_report_like(interpretation_view)`** — engine `Report` and `NarrativeReport` **not** HTTP SSOT |
| **Producer** | `ReportEngine.render`, `NarrativeEngine.compose` (run then discarded); markdown/html from orchestrator |
| **Consumers** | HTTP `data.report`, `data.narrative`; Portal `narrative.js`, `reports.js`; executive overlay |
| **API contract** | `{title, markdown, html, section_count}` — identical for report and narrative |
| **Portal binding** | `narrative.js`: markdown/html; `executive.js` + Summary Builder on full `data` |
| **Recalculated elsewhere?** | Portal markdown→HTML, TOC; executive re-aggregates from full payload |
| **Legacy** | Rich `Report.to_dict()` with templates/metadata; `api/schemas/report.py` schemas for legacy stack |
| **Duplicated ViewModels?** | **Yes:** engine Report ≠ API report; report ≡ narrative in API |

---

### 3.7 AnalysisResult (target — not implemented)

| Dimension | Detail |
|-----------|--------|
| **SSOT (target)** | One typed object (or immutable dict schema) produced once at end of orchestrator, serialized to HTTP and Portal |
| **SSOT today** | `dict[str, Any]` assembled incrementally; stage VMs shaped at different times; engines use different subgraph |
| **Producer** | Should be: `OrchestratorService` after all engines, **before** HTTP shaping |
| **Consumers** | API `APIResponse.data`, `ResultStore`, all Portal tabs, Summary Builder (read-only slices) |
| **Required children** | `calendar`, `bazi`, `pattern`, `score`, `interpretation`, `report`, `narrative`, `feng_shui`, `meta` |
| **Rule** | Downstream engines must consume **same** intermediate graph (or RuleContext derived once), not HTTP VMs |

---

## 4. Cross-cutting dependency layers

### 4.1 RuleContext (hidden hub)

| Item | Detail |
|------|--------|
| **SSOT** | `RuleContextBuilder.build()` (`engines/rule_contract/context_builder.py`) |
| **Producers** | Should be built once from Calendar + Bazi + Pattern + Score + optional luck/shensha |
| **Consumers** | Score module calculators, Interpretation rule matching, Pattern enrichment (future) |
| **Break** | ScoreEngine `_to_rule_context` returns empty context (C1); InterpretationEngine `_to_rule_context` unpacks orchestrator dict correctly (C12 contrast) |
| **Fix dependency** | Must be unified **before** Score, Pattern strength fields, and Interpretation quality can align |

### 4.2 HTTP envelope

| Item | Detail |
|------|--------|
| **Type** | `APIResponse` (`applications/api/schemas/common.py`) |
| **Shape** | `{ success, message, data: AnalysisPayload, request_id }` |
| **Extra** | `customer` via `attach_presentation_metadata` (`applications/api/routes/_helpers.py`) |
| **Portal unwrap** | `analyze.js`: `res.data`; store `{input, data}` |

### 4.3 Portal binding stacks (dual)

| Stack | Files | Input | Duplicates orchestrator? |
|-------|-------|-------|--------------------------|
| Stage presenters | `presenters/*.js` | `data[stage]` | Wider key lists than API |
| Summary Builder | `summary_builder.js` | full `data` | Re-aggregates; different label rules |
| Executive | `executive.js` | Summary Builder model | Narrative tab only |
| Chart header | `chart_info.js` | `data` + `input` | Feng shui / customer |

---

## 5. C1–C15 classification matrix

| ID | Root cause | Category | Severity | Downstream impact | Must fix before |
|----|------------|----------|----------|-------------------|-----------------|
| **C0** | No `AnalysisResult` type; loose dict payload | Contract + Missing implementation | **BLOCKER** | All tabs; no schema validation; engines diverge | — (foundation) |
| **C1** | `ScoreEngine._to_rule_context` ignores `{calendar,bazi,pattern}` dict | Contract | **BLOCKER** | Score 0/E; interpretation conclusion; report conclusion | C0, C4/C5 (partial), C12 pattern |
| **C2** | `PatternContext` omits strength/wuxing/useful_god/luck | Contract | **HIGH** | Pattern thin; C3 fields empty; Score/Interp weak context | C4/C5, unified RuleContext |
| **C3** | `PatternResult` schema ≪ Portal Pattern VM | Contract + Binding | **HIGH** | 5+ Pattern cards `--` | C2, C11 (data) |
| **C4** | Bazi facade stubs `ten_gods`, empty `shensha` | Missing implementation | **BLOCKER** | Pattern, Score ten-god/shensha, Interpretation | C0 (Bazi slice in AnalysisResult) |
| **C5** | HTTP `_shape_bazi` ≠ raw chart for downstream | Contract | **BLOCKER** | Dual truth; Portal OK, engines wrong | C0, C4 |
| **C6** | Pattern fields scraped from Interpretation regex | Presentation + Contract | **MEDIUM** | Fragile `than_vuong_nhuoc`/`dung_than`; wrong layer | C2, C3, C7 |
| **C7** | Interpretation sentences = rule activation / template prose | Translation + Missing implementation | **HIGH** | Luận giải tab; report/narrative body | C1, C2, C4 (correct inputs) |
| **C8** | Report/Narrative engine output discarded | Contract | **MEDIUM** | Report stack not SSOT; duplicate markdown builder | C7 (content owner decision) |
| **C9** | Calendar Can Chi from Bazi, not Calendar Engine | Contract | **MEDIUM** | Calendar tab coupled to Bazi stage; ordering constraint | C5 (single bazi truth) |
| **C10** | Portal binds fields API omits | Binding | **MEDIUM** | `--` on Score/Pattern tabs | C1, C3, API contract freeze |
| **C11** | Pattern DB rules `conditions=[]` → always match | Contract (data) | **HIGH** | Always `chinh_quan`; Pattern meaningless | Independent but before C3 validation |
| **C12** | Score vs Interpretation `_to_rule_context` asymmetry | Contract | **BLOCKER** | Score broken while Interpretation partially works | C1 fix (same adapter pattern) |
| **C13** | Dual Portal stacks (presenters vs Summary Builder) | Binding + Presentation | **MEDIUM** | Narrative/executive ≠ stage tabs; label drift | C0, API contract freeze |
| **C14** | `ResultStore.defaultSummary` expects `interpretation.summary` | Binding + Legacy | **LOW** | History labels generic | C7 / API shape |
| **C15** | `timezone` on `customer`, not `calendar` | Contract + Binding | **LOW** | Calendar tz card; works via form fallback | C0 calendar slice |

**Categories used:**

- **Contract** — producer/consumer schema mismatch  
- **Binding** — Portal reads keys API does not emit  
- **Legacy** — old types/stacks still readable  
- **Cache** — (client store stale pillars — **operational**, not in C1–C15 table; fix via workflow, not engine)  
- **Presentation** — shaping/label/humanize layers  
- **Translation** — Vietnamese commercial copy vs rule text  
- **Missing implementation** — stub or unimplemented engine fields  

---

## 6. Legacy and parallel stacks (do not use for Portal SSOT)

| Stack | Path | Risk |
|-------|------|------|
| Legacy API | `api/app.py`, `api/services/pipeline_service.py` | Same engines but loose `dict` responses; deploy confusion |
| Full Bazi package | `engines/bazi_engine/pillars/*`, `PillarService` | Richer chart; **not** wired to `applications/api` |
| Alternate calendar models | `engines/calendar_engine/models.py` | Duplicate `CalendarResult` concept |
| Integration orchestrator | `engines/integration/orchestrator.py` | Separate wiring |
| Client storage | `bte_last_result`, `bte_portal_last_result` | Stale pillars if API/process mismatch |

---

## 7. Implementation order (dependency-based, not C-number order)

Phases are **sequential**. Within a phase, items can be parallelized.

### Phase 0 — Foundation (blocks everything)

| Step | Work | Resolves | Guarantees |
|------|------|----------|------------|
| 0.1 | Define `AnalysisResult` schema (dataclass or strict TypedDict + OpenAPI) | C0 | One payload type for API + Portal + tests |
| 0.2 | Single pipeline context holder in orchestrator: raw engine outputs + one `RuleContext` build | C0, C12 | One graph per analyze run |
| 0.3 | Contract tests: golden JSON per stage **inside** `AnalysisResult` | C0 | CI blocks drift |

**Exit criterion:** `POST /api/v1/analyze` returns `data` matching `AnalysisResult` schema; no ad-hoc keys outside schema.

---

### Phase 1 — Unified Bazi truth (blocks Pattern, Score, Interpretation)

| Step | Work | Resolves | Depends on |
|------|------|----------|------------|
| 1.1 | One `BaziChart` (or `BaziView`) used for **both** engine handoff and HTTP serialization | C4, C5 | Phase 0 |
| 1.2 | Replace stub `ten_gods` / populate `shensha` **at facade** OR merge shaped pillar `ten_god` back into chart before downstream | C4 | 1.1 |
| 1.3 | Stop passing HTTP-only `_shape_bazi` dict to engines; engines consume same object Portal will see | C5 | 1.1 |
| 1.4 | Align `bazi.js` to read `day_master_element` / `day_master_yin_yang` from API (binding only) | C10 (partial) | 1.1 API fields stable |

**Exit criterion:** `PatternContext.ten_gods` and `RuleContextBuilder._build_bazi` reflect real per-pillar ten gods; Portal and engines show same pillars.

---

### Phase 2 — RuleContext adapter parity (blocks Score)

| Step | Work | Resolves | Depends on |
|------|------|----------|------------|
| 2.1 | Fix `ScoreEngine._to_rule_context` to mirror `InterpretationEngine` (unpack `{calendar,bazi,pattern,score}`) | C1, C12 | Phase 1 |
| 2.2 | Build `RuleContext` **once** in orchestrator; pass to Score and Interpretation | C1, C12 | 2.1, Phase 0.2 |
| 2.3 | Verify non-zero module scores for reference case 1987-01-21 | C1 | 2.2 |

**Exit criterion:** `AnalysisResult.score.total_score` not forced to 0 by empty context.

---

### Phase 3 — Pattern pipeline (blocks Pattern tab + enriches Score/Interp)

| Step | Work | Resolves | Depends on |
|------|------|----------|------------|
| 3.1 | Audit/fix `database/14_pattern/01_main_pattern.csv` rule conditions | C11 | Can parallel Phase 2 |
| 3.2 | Feed full `PatternContext` from `RuleContext` (strength, wuxing, useful_god) | C2 | Phase 1, 2.2 |
| 3.3 | Extend `PatternResult` / `AnalysisResult.pattern` with structural fields Portal needs (only if engines compute them) | C3 | 3.2 |
| 3.4 | Remove regex scrape `_shape_pattern(..., interpretation)` for structural fields | C6 | 3.3 |

**Exit criterion:** `AnalysisResult.pattern` contains real `than_vuong_nhuoc`, `dung_than`, etc. from engines — not Interpretation regex.

---

### Phase 4 — Score API contract (blocks Score tab series)

| Step | Work | Resolves | Depends on |
|------|------|----------|------------|
| 4.1 | Define `ScoreView` in `AnalysisResult`: totals + optional **sanitized** series (no `matched_rules` leak) | C10 (score) | Phase 2 |
| 4.2 | Either emit series in API or narrow Portal `score.js` to match whitelist (prefer emit from AnalysisResult) | C10 | 4.1 |

**Exit criterion:** Score tab shows non-zero totals and intended breakdown without reading stripped `details`.

---

### Phase 5 — Interpretation & narrative content (blocks Luận giải / Bản luận quality)

| Step | Work | Resolves | Depends on |
|------|------|----------|------------|
| 5.1 | Interpretation engine outputs commercial Vietnamese sentences (not activation-only) | C7 | Phases 1–4 |
| 5.2 | Single content owner: Interpretation sections **or** Report Engine — not both discarded | C8 | 5.1 |
| 5.3 | `AnalysisResult.interpretation` + `report`/`narrative` slices from same SSOT | C8, C7 | 5.2 |
| 5.4 | Restore or replace `interpretation.summary` for history if needed | C14 | 5.3 |

**Exit criterion:** Luận giải and Bản luận read from `AnalysisResult` without rule-activation boilerplate.

---

### Phase 6 — Calendar & metadata contract cleanup

| Step | Work | Resolves | Depends on |
|------|------|----------|------------|
| 6.1 | Decide Can Chi owner: Calendar slice includes pillars **or** explicit `calendar.can_chi` from shared Bazi slice | C9 | Phase 1 |
| 6.2 | Add `timezone` to `AnalysisResult.calendar` (from request) | C15 | Phase 0 |
| 6.3 | Feng shui: single slice `feng_shui` referenced by calendar VM (no duplicate copy rules) | C9 partial | Phase 0 |

---

### Phase 7 — Portal binding consolidation (last)

| Step | Work | Resolves | Depends on |
|------|------|----------|------------|
| 7.1 | All tabs: `data = AnalysisResult` from store — `data[stage]` is a **view** of same object | C13 | Phases 0–5 |
| 7.2 | Collapse Summary Builder / executive to read `AnalysisResult` fields only — no re-aggregation, no `formatLabel` dropping valid codes | C13 | 7.1 |
| 7.3 | Remove binding to keys not in schema; `--` only when data truly absent | C10 | 7.1 |
| 7.4 | `result_store.defaultSummary` uses `AnalysisResult` meta | C14 | 7.1 |

**Exit criterion:** Every tab + Narrative executive render from **one** stored `AnalysisResult` JSON; no secondary calculations beyond display formatting.

---

## 8. Dependency DAG (fix order summary)

```
Phase 0: AnalysisResult schema + single RuleContext build
    │
    ▼
Phase 1: Unified BaziChart (engine + API same object)
    │
    ├──────────────────┐
    ▼                  ▼
Phase 2: Score RuleContext fix    Phase 3: Pattern DB + PatternContext
    │                                  │
    └──────────────┬───────────────────┘
                   ▼
            Phase 4: ScoreView series contract
                   ▼
            Phase 5: Interpretation / Report SSOT
                   ▼
            Phase 6: Calendar/metadata alignment
                   ▼
            Phase 7: Portal binding consolidation
```

**Never start with:** Portal tab patches (Phase 7), regex Pattern enrichment (C6), or Report HTML polish before Phases 1–2.

---

## 9. One AnalysisResult guarantee checklist

After all phases, these must hold:

| # | Guarantee |
|---|-----------|
| G1 | Exactly one object graph per `POST /api/v1/analyze` |
| G2 | `ResultStore` persists serialized `AnalysisResult` only |
| G3 | `result.js` passes slices of same object to presenters — no re-fetch analyze on `/result` |
| G4 | Calendar Can Chi matches `AnalysisResult.bazi` pillars |
| G5 | Pattern/Score/Interpretation engines consumed inputs from same graph used to build `AnalysisResult` |
| G6 | No engine output discarded and replaced by a second markdown builder unless that builder **is** the declared SSOT |
| G7 | Summary Builder / executive are **read-only views** of `AnalysisResult`, not a second pipeline |
| G8 | Legacy `api/*` and `pillars/*` package not on production path without explicit adapter |

---

## 10. References

| Document / code | Role |
|-----------------|------|
| [`production_pipeline_contract_audit.md`](production_pipeline_contract_audit.md) | C1–C15 findings, live JSON snapshots |
| `applications/api/services/orchestrator.py` | Production orchestrator |
| `engines/rule_contract/context_builder.py` | RuleContext hub |
| `engines/score_engine/engine.py` | Score adapter bug (C1) |
| `engines/interpretation_engine/engine.py` | Working adapter pattern (C12) |
| `applications/customer_portal/static/js/presenters/*` | Portal bindings |
| `applications/customer_portal/static/js/summary_builder.js` | Second ViewModel stack |

---

**End of dependency map — no code changes in this deliverable.**
