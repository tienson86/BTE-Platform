# BTE Platform — Production Pipeline Contract Audit

**Priority:** BLOCKER  
**Date:** 2026-07-27  
**Scope:** Data contracts only (Calendar → Bazi → Pattern → Score → Interpretation → Report → API → Portal)  
**Method:** Live `OrchestratorService._run(stage="analyze")` for **1987-01-21 04:30 male** + static code inspection  
**Code changes in this document:** NONE (identify broken contracts first)

---

## Executive verdict

| Claim | Finding |
|-------|---------|
| Engines share one `AnalysisResult` | **FALSE** — class does not exist (`AnalysisResult` / `analysis_result` = 0 hits) |
| Pipeline is one object graph | **FALSE** — orchestrator builds a loose `dict` and re-shapes per stage |
| Downstream engines consume Portal ViewModels | **FALSE** — Pattern/Score/Interpretation receive raw engine objects / stubs |
| Symptoms are “UI bugs” | **FALSE** — root causes are **inter-engine contract breaks** |

### Symptom → contract mapping (case 1987-01-21)

| UI symptom | Primary broken contract |
|------------|-------------------------|
| Calendar partially works | Calendar→Portal mostly OK; Can Chi injected from Bazi VM (secondary coupling) |
| Bazi “old pillars” on UI | Live API pillars are **correct**; stale Portal store / wrong API process is client-side. **Separate contract bug:** raw `BaziChart.ten_gods` stub still feeds Pattern/Score/Interp |
| Pattern only “Chính Quan” | `PatternResult` only emits `pattern` (+ score/priority); Portal expects 8 fields |
| Score is zero | `ScoreEngine._to_rule_context` **drops** orchestrator `{calendar,bazi,pattern}` → empty RuleContext |
| Interpretation looks like rule text | Sentences are rule activation / template prose (“Kích hoạt khi…”), not commercial narrative |
| Many `--` | API omits fields Portal whitelists (`than`, `hy_than`, series, etc.) |

---

## Architecture fact: there is no AnalysisResult

```
OrchestratorService._run()
  → payload: dict[str, Any]   # NOT a typed AnalysisResult
  → payload["calendar"] = _shape_calendar(...)
  → payload["bazi"]     = _shape_bazi(...)      # Portal VM
  → pattern_engine.calculate(PatternContext from RAW bazi)  # not from bazi VM
  → score_engine.calculate({calendar, bazi, pattern})       # RAW objects
  → interpretation_engine.run({calendar, bazi, pattern, score})
  → payload["*"] shaped again for HTTP
```

**File:** `applications/api/services/orchestrator.py` (`OrchestratorService._run`)

Portal Result reads **one** stored analyze `data` blob (`ResultStore`), then splits by tab (`data.calendar`, `data.bazi`, …). Tabs do not share a typed object — they share a JSON bag. That is fine **only if** every stage VM is complete and consistent. Today they are not.

---

## Live API snapshot (authoritative for this audit)

Source: `OrchestratorService._run(analyze, 1987,1,21,4,30, gender=male)`

### Calendar (`data.calendar`) — example

```json
{
  "solar_date": "21/01/1987",
  "lunar_date": "22/12/Bính Dần",
  "solar_term": { "name": "...", "index": N },
  "year_can_chi": "Bính Dần",
  "month_can_chi": "Tân Sửu",
  "day_can_chi": "Canh Ngọ",
  "hour_can_chi": "Mậu Dần",
  "cung_phi": "Khôn",
  "menh_quai": "Khôn",
  "nhom_trach": "Tây Tứ Trạch"
}
```

### Bazi (`data.bazi`) — example (shaped VM)

```json
{
  "year_pillar":  { "stem": "Bính", "branch": "Dần", "ten_god": "Thất Sát", "nap_am": "Lư Trung Hỏa", "truong_sinh": "Tuyệt", "hidden_stems": ["Giáp","Bính","Mậu"] },
  "month_pillar": { "stem": "Tân", "branch": "Sửu", "ten_god": "Kiếp Tài", ... },
  "day_pillar":   { "stem": "Canh", "branch": "Ngọ", "ten_god": "Nhật Chủ", ... },
  "hour_pillar":  { "stem": "Mậu", "branch": "Dần", "ten_god": "Thiên Ấn", ... },
  "day_master": "Canh",
  "day_master_element": "Kim",
  "day_master_yin_yang": "Dương",
  "ten_gods": ["Tỷ Kiên","Tỷ Kiên","Tỷ Kiên","Tỷ Kiên"],
  "shensha": []
}
```

### Pattern (`data.pattern`) — example

```json
{
  "success": true,
  "pattern": "chinh_quan",
  "cach_cuc": "Chinh Quan",
  "dung_than": "Chính Quan",
  "score": 91.0,
  "priority": 100
}
```

Missing vs Portal: `than`, `than_vuong_nhuoc`, `tong_cach`, `hy_than`, `ky_than`, `dieu_hau`.

### Score (`data.score`) — example

```json
{
  "success": true,
  "total_score": 0.0,
  "strength_score": 0.0,
  "pattern_score": 0.0,
  "ten_god_score": 0.0,
  "wuxing_score": 0.0,
  "grade": "E",
  "confidence": "low",
  "recommendation": "Cần đặc biệt chú ý"
}
```

### Interpretation (`data.interpretation`) — example

```json
{
  "sections": [
    { "id": "summary", "title": "Tổng quan", "body": "…Kích hoạt khi xác định Chính Cách.…Tổng quan: Nhật Chủ Canh, cách cục Chinh Quan." }
  ],
  "section_count": 9,
  "sentence_count": 22,
  "confidence": 1
}
```

### Report / Narrative

Rebuilt from interpretation sections only (`_shape_report_like`). Engine `report_engine.render` / `narrative_engine.compose` run but **public payload ignores their native artifacts**.

---

## Contract matrix

| Engine / Stage | Engine output (raw) | API field (`data.*`) | Portal bind | Status |
|----------------|---------------------|----------------------|-------------|--------|
| Calendar | `CalendarResult` solar/lunar/JD/term | `calendar.*` + injected `*_can_chi`, feng fields | `presenters/calendar.js` | **PARTIAL OK** |
| Feng Shui | `FengShuiResult.to_dict()` | `feng_shui` + copied onto `calendar` | Calendar cards / chart | **PARTIAL OK** |
| Bazi facade | `BaziChart` pillars + stub `ten_gods`/`shensha` | `bazi` shaped pillars + `day_master*` | `presenters/bazi.js` | **API OK / PIPELINE DUAL** |
| Pattern | `PatternResult{pattern,score,priority,matched_rules}` | `pattern` thin VM | `presenters/pattern.js` 8 cards | **BROKEN** |
| Score | `ScoreResult` (all modules 0) | `score` whitelist totals | `presenters/score.js` | **BROKEN (zero)** |
| Interpretation | sentences / sections / rules | `interpretation.sections[{id,title,body}]` | `presenters/interpretation.js` | **BROKEN (content quality)** |
| Report | `Report` rich internals | `report{title,markdown,html,section_count}` from interp VM | Reports / narrative | **CONTRACT BYPASS** |
| Narrative | narrative compose | same as report clean VM | `presenters/narrative.js` | **CONTRACT BYPASS** |
| Unified result | — | loose dict | `ResultStore` one blob | **MISSING TYPE** |

Legend: **BROKEN** = schema or semantics fail end-to-end; **DUAL** = Portal sees one shape, downstream engines another; **BYPASS** = engine output not the API contract.

---

## Per-stage contract sheets

### 1. Calendar

| Item | Detail |
|------|--------|
| **Input schema** | `(year, month, day, hour, minute)` → `CalendarEngine.build` |
| **Output schema (engine)** | `CalendarResult`: `solar`, `lunar`, `julian_day`, `solar_term`, `solar_*`, `lunar_*`, `solar_date`, `lunar_date` |
| **API shape** | `to_jsonable(calendar)` + `_shape_calendar` adds `year/month/day/hour_can_chi` from **Bazi VM**, plus `cung_phi`/`menh_quai`/`nhom_trach` from Feng Shui |
| **Consumers** | Portal Calendar tab; Score/Interp via raw `calendar` object (not API VM) |
| **Schema identical Engine↔API↔Portal?** | No — Can Chi are not Calendar Engine fields; they are Bazi-derived presentation |
| **Portal bind correct?** | Yes for dates/terms/can chi when API filled |

**Mismatch:** Calendar tab Can Chi depends on Bazi stage succeeding and shaping — not a pure Calendar contract.

---

### 2. Bazi

| Item | Detail |
|------|--------|
| **Input schema** | `BaziEngine.build(calendar\|y,m,d,h,mi, gender=)` |
| **Output schema (engine)** | `BaziChart`: four `Pillar{stem,branch}`, `hidden_stems[]`, `ten_gods[]`, `shensha[]`, `day_master` property |
| **API shape** | `_shape_bazi`: per-pillar `hidden_stems`, `ten_god`, `nap_am`, `truong_sinh`, top-level `day_master*` |
| **Consumers** | Portal Bazi tab (API VM); Pattern/Score/Interp (RAW chart) |
| **Identical?** | **NO** |

**Broken contracts:**

1. **Dual ViewModel**
   - Portal: enriched pillar `ten_god` (correct for case).  
   - Raw chart still has `ten_gods = ["Tỷ Kiên","Tỷ Kiên","Tỷ Kiên","Tỷ Kiên"]` (`engines/bazi_engine/engine.py` stub).  
   - Orchestrator PatternContext uses `bazi.ten_gods` stub list (`orchestrator.py` ~L533).

2. **Empty shensha on facade**  
   - `shensha=[]` always on compact chart → Pattern/Score/Interp cannot see thần sát from Bazi.

3. **UI “old pillars”**  
   - Live API for this case emits Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần.  
   - If UI still shows Đinh Mão…, that is **not** current `data.bazi` from this orchestrator — treat as store/process mismatch, not presenter math.  
   - Contract requirement: Portal must render **only** `data.bazi` from the same analyze payload as Calendar (same `AnalysisResult` once introduced).

---

### 3. Pattern

| Item | Detail |
|------|--------|
| **Input schema** | `PatternContext`: pillars, `day_master`, `strength_*`, `wuxing_score`, `ten_gods`, `shensha`, `useful_god`, … |
| **What orchestrator actually passes** | pillars + day_master + stub ten_gods + empty shensha; **strength/useful_god/wuxing unset** |
| **Output schema (engine)** | `PatternResult`: `success`, `pattern`, `score`, `priority`, `matched_rules`, `error` |
| **API shape** | `_shape_pattern`: `pattern`, `cach_cuc`, `score`, `priority`; optionally scrape `than_vuong_nhuoc` / `dung_than` from interpretation text |
| **Portal expects** | `than`, `than_vuong_nhuoc`, `cach_cuc`, `tong_cach`, `dung_than`, `hy_than`, `ky_than`, `dieu_hau` (`presenters/pattern.js` `FIELDS`) |
| **Identical?** | **NO** |

**Broken contracts:**

| Portal field | API today | Engine has? |
|--------------|-----------|-------------|
| `cach_cuc` | `cach_cuc` / `pattern` | `pattern` only (token `chinh_quan`) |
| `dung_than` | sometimes scraped | not on `PatternResult` |
| `than` | missing → `--` | not produced |
| `than_vuong_nhuoc` | usually missing | needs strength upstream |
| `tong_cach` | missing | not on result |
| `hy_than` / `ky_than` | missing | useful-god domain |
| `dieu_hau` | missing | temperature/climate domain |
| `matched_rules` | stripped from API (good) | internal only |

**Why UI shows only “Chính Quan”:** only `pattern`/`cach_cuc` (and maybe `dung_than`) are populated; other cards bind missing keys → `--`.

**Pattern DB contract (engine audit):** `database/14_pattern/01_main_pattern.csv` — rules with **`conditions=[]`** match every chart; highest `priority` wins → production path often resolves to `chinh_quan` (score 91). This is a **data + matcher contract** issue, not a Portal label issue.

---

### 4. Score

| Item | Detail |
|------|--------|
| **Input schema (intended)** | RuleContext via `RuleContextBuilder.build(calendar=…, bazi=…, pattern=…)` |
| **What orchestrator passes** | `{"calendar": CalendarResult, "bazi": BaziChart, "pattern": PatternResult}` |
| **`ScoreEngine._to_rule_context`** | If dict has `bazi` **and** `wuxing` → use as-is; elif object has `day_master` → build(bazi=…); **else `builder.build()` empty** |
| **Actual path** | Dict has `bazi` key but **no** `wuxing` key; dict has no `.day_master` attribute → **`builder.build()` with no args** |
| **Output** | All module scores 0; grade E |
| **API shape** | `_shape_score` whitelist of totals (hides `details`) |
| **Portal** | Binds `total_score`, `strength_score`, `pattern_score`, … — correctly reads zeros |

**Broken contract (exact):**

```
File:    engines/score_engine/engine.py
Function: ScoreEngine._to_rule_context
Bug:     Orchestrator dict context is ignored → empty RuleContext
Effect:  Wuxing matcher fires MISSING×5 (ES016–ES020), scores clamp to 0
Proof:   Live safe_execute on that context → matched MISSING rules; total_score 0.0
```

**Asymmetry (critical):** `InterpretationEngine._to_rule_context` (`interpretation_engine/engine.py` ≈ L234–252) **unpacks** `{calendar, bazi, pattern, score}` into `RuleContextBuilder.build(...)`. `ScoreEngine._to_rule_context` does **not** — same orchestrator dict shape, different adapter behavior → Score broken while Interpretation partially works.

This is **not** a Portal bug. Portal correctly displays a broken Score contract.

Secondary: even after wiring RuleContext, facade stub `ten_gods`/`shensha` will still underfeed ten-god / shensha modules until Bazi contract is unified.

---

### 5. Interpretation

| Item | Detail |
|------|--------|
| **Input** | `interpretation_engine.run({calendar, bazi, pattern, score})` — raw objects + zeroed score |
| **Output (engine)** | sentences with `section` + `sentence` (plus internal rule metadata upstream) |
| **API shape** | `_shape_interpretation` → `sections[{id,title,body}]` sanitized |
| **Portal** | Renders section titles/bodies; avoids unknown English keys after prior hardening |
| **Identical Engine↔commercial copy?** | **NO** |

**Broken contracts:**

1. Content is rule-engine prose (“Kích hoạt khi xác định Chính Cách”, romanized pattern names like “Tai Hon Tap” in report body) — not final Vietnamese luận giải.  
2. Depends on Score=0 and thin Pattern → conclusion text literally “Điểm tổng hợp: 0.0 — hạng E”.  
3. No shared narrative DTO with Report; Report HTML is regenerated from the same thin sections.

User-visible “rule IDs”: may be FPR codes on older cached payloads, or activation/meta sentences. Live shaped payload for this case shows **activation text**, not `FPR***`, but still non-commercial.

**API sanitization (engine audit):** `_shape_interpretation` uses `interpretation.sentences` only; `rule_id` is **not** in JSON. `_sanitize_sentence` strips `FPR|SPR|PAT|…`, `status=`, upstream/debug. CTX enrich lines with `month=`/`root=` may still pass.

---

### 6. Report / Narrative

| Item | Detail |
|------|--------|
| **Engine call** | `report_engine.render(interpretation)` then `narrative_engine.compose(interpretation, report)` |
| **API field** | `_shape_report_like(interpretation_view)` — **discards** engine report/narrative objects |
| **Portal** | `data.report` / `data.narrative` html/markdown |
| **Contract** | Engines run for side effects / future use; **HTTP contract ≠ engine output** |

**Mismatch:** Two producers (Report Engine vs orchestrator markdown builder). Portal binds orchestrator VM only.

---

### 7. API envelope → Portal

| Item | Detail |
|------|--------|
| **Envelope** | `{ success, message, data, request_id }` + `customer` via `attach_presentation_metadata` |
| **Store** | `ResultStore` keys `bte_last_result` / `bte_view_result` / `bte_history` |
| **Result render** | `result.js` → `data[stage]` → presenter |
| **Secondary calc in Portal?** | Presenters mostly display-only; some label maps (`PATTERN_LABELS`) and Can Chi formatting — **must not** recompute pillars/scores |
| **Duplicated ViewModels** | Orchestrator `_shape_*` **and** `summary_builder.js` / executive presenters re-derive layouts from same bag |

**Top-level `data` keys (analyze):**

| Key | Producer | Notes |
|-----|----------|-------|
| `pipeline` | `_run` | completed stage names |
| `stage` | `_run` | `"analyze"` on full run |
| `calendar` | `_shape_calendar` | + can chi from Bazi, feng from `feng_shui` |
| `bazi` | `_shape_bazi` | Portal VM |
| `bazi_source` | fingerprint | engine path proof |
| `feng_shui` | `GuaResult.to_dict()` or `null` | also copied onto `calendar` |
| `pattern` | `_shape_pattern` | enriched after interpretation |
| `score` | `_shape_score` | whitelist totals |
| `interpretation` | `_shape_interpretation` | `sections[]` only |
| `report` | `_shape_report_like` | **not** `ReportEngine` output |
| `narrative` | `_shape_report_like` | **not** `NarrativeEngine` output |
| `customer` | `attach_presentation_metadata` | name, place, gender, timezone |

**Store:** `ResultStore.save({input, data})` → `bte_last_result` (+ `bte_history`). `defaultSummary()` still prefers `interpretation.summary` — key **removed** from shaped API → history rows use generic label.

---

## Master mismatch list (fix data contract first)

Ordered by pipeline dependency (do **not** start with Portal CSS/tabs):

| ID | Break | Exact location | Effect |
|----|-------|----------------|--------|
| C0 | No typed `AnalysisResult` shared by stages | `orchestrator.py` `_run` returns ad-hoc dict | Stages diverge; Portal cannot validate one schema |
| C1 | Score ignores `{calendar,bazi,pattern}` dict | `score_engine/engine.py` `_to_rule_context` → `builder.build()` | **Score always ~0 / grade E** |
| C2 | PatternContext under-specified | `orchestrator.py` PatternContext construction | Pattern cannot emit strength/useful-god fields |
| C3 | `PatternResult` schema ≪ Portal Pattern VM | `pattern_engine/engine.py` `PatternResult` vs `pattern.js` `FIELDS` | Only Cách cục (and maybe Dụng thần) visible |
| C4 | Bazi facade stub `ten_gods` / empty `shensha` | `bazi_engine/engine.py` `BaziChart` return | Downstream Pattern/Score/Interp poisoned while Portal VM looks richer |
| C5 | Orchestrator shapes Bazi for HTTP but passes raw chart downstream | `orchestrator.py` `_shape_bazi` vs later `calculate` calls | **Dual contract** |
| C6 | Pattern enrichment scraped from interpretation regex | `_shape_pattern(..., interpretation)` | Fragile; wrong layer for structural fields |
| C7 | Interpretation sentences = rule activation copy | Interpretation engine + DB templates | “Rule-like” UI text |
| C8 | Report/Narrative engine output discarded | `_shape_report_like` | Report stack not the source of truth |
| C9 | Calendar Can Chi not owned by Calendar Engine | `_shape_calendar(..., bazi_data)` | Cross-stage presentation coupling |
| C10 | Portal `--` for omitted API keys | pattern/score/summary presenters | Correct binding of incomplete contracts |
| C11 | Pattern DB rules all match (`conditions=[]`) | `database/14_pattern/01_main_pattern.csv` | Highest priority always wins → `chinh_quan` |
| C12 | Score `_to_rule_context` ≠ Interpretation `_to_rule_context` | `score_engine/engine.py` vs `interpretation_engine/engine.py` | Score empty ctx; Interpretation gets full RuleContext |
| C13 | Portal dual binding stacks | stage presenters vs `summary_builder.js` / `executive.js` | Same payload, different keys/labels; Narrative tab ≠ stage tabs |
| C14 | History summary expects removed key | `result_store.js` `defaultSummary` → `interpretation.summary` | API omits top-level `summary` |
| C15 | Calendar `timezone` not on calendar object | `_shape_calendar` vs `calendar.js` | Falls back to form input only |

---

## Who consumes what (dependency direction)

```
                    ┌─────────────────────────────┐
                    │  HTTP payload (shaped VMs)  │──► Portal tabs / ResultStore
                    └─────────────────────────────┘
                                   ▲
                                   │ _shape_*
┌──────────┐  build   ┌──────────┐  PatternContext(stubs)  ┌──────────┐
│ Calendar │─────────►│   Bazi   │────────────────────────►│ Pattern  │
└──────────┘          └──────────┘                         └────┬─────┘
                           │   raw chart                        │
                           ▼                                    ▼
                      ┌──────────┐  dict{cal,bazi,pat}    ┌──────────┐
                      │  Score   │◄── BROKEN wiring ──────│ (unused  │
                      └────┬─────┘     RuleContext)       │  rich    │
                           │                              │  ctx)    │
                           ▼                              │          │
                      ┌──────────────┐◄───────────────────┘          │
                      │Interpretation│◄────────────────────────────────┘
                      └──────┬───────┘
                             ▼
                      Report / Narrative (run, then replaced by interp VM)
```

---

## Portal field binding (verify after contracts match)

| Tab | Payload key | Primary fields read | Secondary calc? |
|-----|-------------|---------------------|-----------------|
| Lịch Việt | `data.calendar` | `solar_date`, `lunar_*`, `*_can_chi`, `solar_term`, `cung_phi`, `menh_quai` | No |
| Bát Tự | `data.bazi` | `*_pillar.stem/branch`, `hidden_stems`, `ten_god`, `nap_am`, `truong_sinh`, `day_master*` | Display maps only |
| Cách Cục | `data.pattern` | 8 `FIELDS` key lists | Label map for codes |
| Đánh Giá | `data.score` | `total_score`, module scores, `grade`, series keys | No scoring math |
| Luận Giải | `data.interpretation` | `sections[]` or legacy top-level keys | No |
| Bản luận | `data.narrative` (+ executive from full `data`) | `html`/`markdown` | Compose only |

**Rule for later work:** Once contracts match, every tab must render from the **same** analyze `data` object without re-fetch inventing values and without a second parallel ViewModel layer in JS.

### Portal dual binding stacks ([Audit portal field bindings](6ab9dbc8-ffe3-4c09-a515-2c44e7c4c5b0))

| Stack | Used by | Input | Contract strictness |
|-------|---------|-------|---------------------|
| Stage presenters | Calendar–Interpretation tabs | `data[stage]` | Wide alias lists; Pattern/Score expect fields API omits |
| Summary Builder + executive | Narrative tab, Reports | **full** `data` | Re-aggregates calendar/bazi/pattern/score; `formatLabel` drops snake_case codes → `--` |
| chartHeader / batTrach | Result header | `data` + `input` | `feng_shui` first; legacy `bat_trach` fallback |

**Inconsistencies (not separate engine bugs — binding drift):**

- `bazi.js` uses client `STEM_META` for element/âm dương; `summary_builder.js` reads API `day_master_element` / `day_master_yin_yang`.
- `pattern.js` humanizes codes; `summary_builder.formatLabel` returns `--` for raw keys.
- Score tab expects `details.*` series and `interpretation_score` — stripped by `_shape_score`.
- Narrative API has no `tone` / `metrics`; presenter helpers exist but stay empty.

### Full contract matrix (Engine → API → Portal)

| Engine / tab | API emits (production) | Portal reads | Status |
|--------------|------------------------|--------------|--------|
| Calendar | `solar_date`, `lunar_*`, `*_can_chi`, `solar_term`, feng fields | Same + `lunar.leap`, tz from cal or input | **PARTIAL** (tz, leap alias) |
| Bazi | shaped pillars + `day_master*`; stub `ten_gods[]`, `shensha[]` | pillar keys; element from **client** STEM_META | **DUAL** |
| Pattern | `pattern`, `cach_cuc`, `score`, `priority`, optional `than_vuong_nhuoc`, `dung_than` | 8 god/body fields (`pattern.js` FIELDS) | **BROKEN** (5+ cards `--`) |
| Score | totals, grade, confidence; no `details` | totals + series from `details.*` | **BROKEN** (zeros + no series) |
| Interpretation | `sections[{id,title,body}]`, counts | sections + legacy top-level keys | **PARTIAL** (works via sections) |
| Narrative | title, markdown, html, section_count | markdown/html + executive overlay | **LOW** body; executive gaps |
| Report | same as narrative VM | reports.js local history | **BYPASS** engine |

---

## Required target contract (definition of done — not implemented here)

Introduce a single production object (name illustrative):

```text
AnalysisResult
  calendar: CalendarView
  bazi: BaziView          # same object used by Pattern/Score/Interp — not a HTTP-only clone
  pattern: PatternView    # than, than_vuong_nhuoc, cach_cuc, tong_cach, dung/hy/ky, dieu_hau
  score: ScoreView        # non-zero when rules match real chart; no empty RuleContext
  interpretation: InterpView  # Vietnamese sections only
  report / narrative: render views derived from InterpView OR Report Engine — one owner
  meta: { pipeline, bazi_source, request_id }
```

Acceptance for case 1987-01-21 04:30 Nam:

1. `AnalysisResult.bazi` pillars = Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần  
2. Same pillars appear in Calendar Can Chi and Bazi tab from **one** payload  
3. Pattern VM fills structural fields that engines actually computed (no fake UI)  
4. Score total ≠ forced 0 from empty RuleContext  
5. Interpretation/Report contain commercial Vietnamese text, not activation/meta rule noise  
6. Portal binds only these fields — no legacy cache as source of truth for contracts  

---

## Explicit non-actions (this audit)

- No Portal tab patches.  
- No Calendar/Bazi formula changes.  
- No “make `--` prettier” CSS.  
- No claiming completion from pytest alone.

---

## Evidence index

| Evidence | Location |
|----------|----------|
| Orchestrator pipeline | `applications/api/services/orchestrator.py` `_run`, `_shape_*` |
| Score context drop | `engines/score_engine/engine.py` `_to_rule_context` L151–172 |
| RuleContext builder | `engines/rule_contract/context_builder.py` `build` |
| Bazi stub ten gods | `engines/bazi_engine/engine.py` `BaziChart` / `build` return |
| Pattern thin result | `engines/pattern_engine/engine.py` `PatternResult` |
| Pattern rich input unused | `engines/pattern_engine/context.py` `PatternContext` |
| Portal Pattern fields | `applications/customer_portal/static/js/presenters/pattern.js` `FIELDS` |
| Portal Score fields | `applications/customer_portal/static/js/presenters/score.js` `SUMMARY` |
| Live zeros / thin pattern / correct pillars | runtime `_run(analyze)` 1987-01-21 (this audit) |
| Score vs Interpretation adapters | `engines/score_engine/engine.py`, `engines/interpretation_engine/engine.py` `_to_rule_context` |
| Pattern DB empty conditions | `database/14_pattern/01_main_pattern.csv` |
| Portal binding audit | `applications/customer_portal/static/js/presenters/*.js`, `summary_builder.js`, `executive.js` |
| Subagent reports | [Audit engine API contracts](ef3b05b4-6d5d-4e02-8afd-6b68dd8ffdd5), [Audit portal field bindings](6ab9dbc8-ffe3-4c09-a515-2c44e7c4c5b0) |

---

## Next step (after this report is accepted)

1. Fix **C1** (Score RuleContext wiring) and **C4/C5** (single Bazi truth) at orchestrator/engine boundary.  
2. Expand **PatternResult / Pattern VM** (C2/C3) from real upstream signals — not Portal guesses.  
3. Define **AnalysisResult** schema + OpenAPI / golden contract tests.  
4. Only then re-verify each Portal tab against the same payload.

**End of audit — contracts identified; no production code changed in this deliverable.**
