# BTE Platform V1.0 — AnalysisResult Contract (Phase 1)

**Priority:** HIGHEST  
**Date:** 2026-07-27  
**Status:** **Contract definition only** — not yet implemented in code  
**Consumers (future):** `OrchestratorService`, `APIResponse.data`, `ResultStore`, Portal presenters

---

## 1. Purpose

`AnalysisResult` is the **only** object that crosses the API → Portal boundary for a full analyze run.

| Layer | Allowed action |
|-------|----------------|
| Engines | Produce native results + participate in single `RuleContext` build |
| Orchestrator | Assemble **one** `AnalysisResult` per run |
| API | `AnalysisResult.to_dict()` → JSON |
| Portal | Read JSON slices — **render only** |

**Forbidden:**

- Intermediate DTOs per stage (`_shape_bazi`, `_shape_score`, …) as separate public contracts  
- Portal re-aggregation (`summary_builder` as second pipeline)  
- API-layer pillar/score/report calculation  
- Per-engine `RuleContextBuilder.build()` without shared context  

---

## 2. Type definition (target)

**Recommended location (Phase 2+ implementation):**

`applications/api/models/analysis_result.py` (or `engines/integration/models/analysis_result.py` if engines must import slices — prefer applications layer as HTTP owner)

```python
@dataclass(slots=True)
class AnalysisResult:
    calendar: CalendarView
    bazi: BaziView
    feng_shui: FengShuiView | None
    pattern: PatternView
    score: ScoreView
    interpretation: InterpretationView
    report: ReportView
    narrative: NarrativeView
    meta: AnalysisMeta
```

Serialization: `to_dict()` → JSON-compatible `dict` matching schema below.  
No separate “public” vs “internal” dict — one schema.

---

## 3. Top-level schema

```json
{
  "calendar": { ... },
  "bazi": { ... },
  "feng_shui": { ... } | null,
  "pattern": { ... },
  "score": { ... },
  "interpretation": { ... },
  "report": { ... },
  "narrative": { ... },
  "meta": { ... }
}
```

**Not top-level (customer presentation only):**

`customer` block remains in `APIResponse` assembly (`attach_presentation_metadata`) — **not** part of `AnalysisResult` engine graph. Optional mirror in `meta.request` for Portal convenience.

---

## 4. `calendar` — CalendarView

**SSOT producer:** `CalendarEngine.build`  
**May include derived display fields** only if computed in orchestrator from **same** `BaziView` slice (single pass, documented).

| Field | Type | Required | Source |
|-------|------|----------|--------|
| `solar_date` | string | yes | `CalendarResult.solar_date` |
| `lunar_date` | string | yes | `CalendarResult.lunar_date` |
| `solar_year` | int | yes | `CalendarResult.solar_year` |
| `solar_month` | int | yes | `CalendarResult.solar_month` |
| `solar_day` | int | yes | `CalendarResult.solar_day` |
| `solar_hour` | int | yes | `CalendarResult.solar_hour` |
| `solar_minute` | int | yes | `CalendarResult.solar_minute` |
| `julian_day` | float | yes | `CalendarResult.julian_day` |
| `solar_term` | `{name, index}` | yes | `CalendarResult.solar_term` |
| `lunar` | `{year, month, day, leap, year_can_chi}` | yes | `CalendarResult.lunar` |
| `year_can_chi` | string | yes | From **same** bazi year pillar (not recomputed elsewhere) |
| `month_can_chi` | string | yes | From bazi month pillar |
| `day_can_chi` | string | yes | From bazi day pillar |
| `hour_can_chi` | string | yes | From bazi hour pillar |
| `timezone` | string | yes | From `BirthRequest.timezone` (echo for Portal) |
| `cung_phi` | string | optional | From `feng_shui` slice (display convenience) |
| `menh_quai` | string | optional | From `feng_shui` |
| `nhom_trach` | string | optional | From `feng_shui` |
| `gua_name` | string | optional | From `feng_shui` |

**Portal binding:** `presenters/calendar.js` — must not guess dates; read these fields.

---

## 5. `bazi` — BaziView

**SSOT producer:** `BaziEngine.build` + orchestrator enrichment **once** (nap_am, truong_sinh, ten_god per pillar — until engine owns them in Phase 2).

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `year_pillar` | PillarView | yes | |
| `month_pillar` | PillarView | yes | |
| `day_pillar` | PillarView | yes | |
| `hour_pillar` | PillarView | yes | |
| `day_master` | string | yes | Can day stem |
| `day_master_element` | string | yes | Vietnamese: Mộc/Hỏa/Thổ/Kim/Thủy |
| `day_master_yin_yang` | string | yes | Dương/Âm |
| `gender` | string | optional | |
| `hidden_stems` | string[] | optional | Flat list (legacy compat) |
| `ten_gods` | string[] | optional | **Must match** per-pillar `ten_god` after Phase 2 |
| `shensha` | string[] | optional | From engine when available |

### PillarView

| Field | Type | Required |
|-------|------|----------|
| `stem` | string | yes |
| `branch` | string | yes |
| `hidden_stems` | string[] | yes |
| `ten_god` | string | yes |
| `nap_am` | string | yes |
| `truong_sinh` | string | yes |

**Portal binding:** `presenters/bazi.js` — use `day_master_element` / `day_master_yin_yang` from contract; **no** `STEM_META` inference (Phase 7).

**Downstream engines** must consume the **same** `BaziView` / `BaziChart` built from this data — not a stub parallel chart (Phase 2).

---

## 6. `feng_shui` — FengShuiView

**SSOT producer:** `FengShuiEngine.calculate`

| Field | Type | Required |
|-------|------|----------|
| `cung_phi` | string | yes |
| `menh_quai` | string | yes |
| `nhom_trach` | string | optional |
| `gua_name` | string | optional |
| `gua_number` | int | optional |
| `group` | string | optional |

`null` when gender invalid/missing (current behavior).

---

## 7. `pattern` — PatternView

**SSOT producer:** `PatternEngine` + `RuleContext` signals (Phase 3)

| Field | Type | Required | Portal (`pattern.js`) |
|-------|------|----------|----------------------|
| `success` | bool | yes | status bar |
| `pattern` | string | yes | code |
| `cach_cuc` | string | yes | Cách cục card |
| `score` | float | yes | status bar |
| `priority` | int | yes | status bar |
| `than` | string | optional | Thân |
| `than_vuong_nhuoc` | string | optional | Thân vượng/nhược |
| `tong_cach` | string | optional | Tòng cách |
| `dung_than` | string | optional | Dụng thần |
| `hy_than` | string | optional | Hỷ thần |
| `ky_than` | string | optional | Kỵ thần |
| `dieu_hau` | string | optional | Điều hậu |

**Excluded from contract (internal only):** `matched_rules`, `error` debug strings.

**Rule:** Fields must come from Pattern/Rule engines — **not** regex scrape from interpretation (replaces LEGACY `_shape_pattern` enrichment).

---

## 8. `score` — ScoreView

**SSOT producer:** `ScoreEngine` with shared `RuleContext`

| Field | Type | Required | Portal (`score.js`) |
|-------|------|----------|----------------------|
| `success` | bool | yes | |
| `total_score` | float | yes | overall card |
| `strength_score` | float | yes | than card |
| `pattern_score` | float | yes | pattern card |
| `ten_god_score` | float | yes | |
| `wuxing_score` | float | yes | |
| `useful_god_score` | float | optional | |
| `shensha_score` | float | optional | |
| `luck_score` | float | optional | |
| `grade` | string | yes | badge |
| `confidence` | string | yes | badge |
| `recommendation` | string | yes | badge |
| `wuxing_series` | ScoreSeriesItem[] | optional | bar chart |
| `ten_god_series` | ScoreSeriesItem[] | optional | bar chart |
| `interpretation_score` | float | optional | if product needs card |

### ScoreSeriesItem

| Field | Type | Notes |
|-------|------|-------|
| `label` | string | Vietnamese label |
| `value` | float | score |

**Excluded from contract:** `details`, `matched_rules`, `history`, `metadata`, `execution_time`, raw rule IDs.

---

## 9. `interpretation` — InterpretationView

**SSOT producer:** `InterpretationEngine.run`

| Field | Type | Required |
|-------|------|----------|
| `sections` | InterpretationSection[] | yes |
| `section_count` | int | yes |
| `sentence_count` | int | yes |
| `confidence` | float | yes |

### InterpretationSection

| Field | Type | Required |
|-------|------|----------|
| `id` | string | yes | e.g. `summary`, `career` |
| `title` | string | yes | Vietnamese |
| `body` | string | yes | Commercial prose — no rule IDs |

**Excluded:** `summary` top-level string, `rules_used`, `rule_id`, `matched_rule_count`, raw `sections` dict from engine.

**Portal:** `interpretation.js` reads `sections[]` only.

---

## 10. `report` — ReportView

**SSOT owner (choose one in Phase 5):**

- **Option A:** `ReportEngine.render` output mapped to `ReportView`  
- **Option B:** `InterpretationView` rendered to markdown/html in orchestrator  

Until decided, contract shape is fixed:

| Field | Type | Required |
|-------|------|----------|
| `title` | string | yes |
| `markdown` | string | yes |
| `html` | string | yes |
| `section_count` | int | yes |

**Excluded:** `templates_used`, `appendix`, `pdf_path`, internal metadata.

---

## 11. `narrative` — NarrativeView

Same shape as `ReportView` today, but **Phase 5** must decide if content differs from `report` (tone, transitions, metrics).

| Field | Type | Required |
|-------|------|----------|
| `title` | string | yes |
| `markdown` | string | yes |
| `html` | string | yes |
| `section_count` | int | yes |
| `tone` | string | optional | from NarrativeEngine when SSOT = narrative |
| `metrics` | object | optional | sanitized public metrics only |

---

## 12. `meta` — AnalysisMeta

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `pipeline` | string[] | yes | Completed stages |
| `stage` | string | optional | `"analyze"` on full run |
| `request_id` | string | optional | From middleware |
| `bazi_source` | object | yes | Engine fingerprint |
| `rule_context_id` | string | optional | Hash/version of shared RuleContext build |
| `contract_version` | string | yes | e.g. `"1.0"` |
| `built_at` | string | optional | ISO timestamp |

### `bazi_source` (provenance)

| Field | Type | Example |
|-------|------|---------|
| `engine` | string | `engines.bazi_engine.engine.BaziEngine` |
| `method` | string | `build` |
| `contract` | string | `li_chun_jdn_v1` |

---

## 13. RuleContext (not a Portal tab — pipeline internal)

Stored on pipeline context or `meta` — **not** duplicated in HTTP unless debug flag.

```json
{
  "built_once": true,
  "coverage_percent": 85.0,
  "present_signals": ["..."],
  "missing_signals": ["..."]
}
```

**Rule:** `RuleContextBuilder.build(calendar=…, bazi=…, pattern=…, score=…)` called **once** in orchestrator; Score and Interpretation receive **reference** to same dict — not rebuild.

---

## 14. API envelope (unchanged)

```json
{
  "success": true,
  "message": "OK",
  "data": { /* AnalysisResult.to_dict() */ },
  "request_id": "..."
}
```

`attach_presentation_metadata` may add sibling keys **outside** `AnalysisResult`:

```json
{
  "customer": {
    "full_name": "...",
    "birth_place": "...",
    "gender": "...",
    "timezone": "...",
    "customer_id": null
  }
}
```

---

## 15. Portal consumption map

| Tab | Slice | Presenter |
|-----|-------|-----------|
| Lịch Việt | `data.calendar` | `calendar.js` |
| Bát Tự | `data.bazi` | `bazi.js` |
| Cách Cục | `data.pattern` | `pattern.js` |
| Đánh Giá | `data.score` | `score.js` |
| Luận Giải | `data.interpretation` | `interpretation.js` |
| Bản luận | `data.narrative` + optional executive read-only summary | `narrative.js`, `executive.js` |

**ResultStore:** persists `{ input, data }` where `data` conforms to `AnalysisResult` JSON.

**Forbidden Portal actions:** `POST /analyze` on `/result`, merge/guess pillars, `summary_builder.build` as second pipeline (Phase 7 collapse).

---

## 16. Migration from current loose dict

| Current key / method | AnalysisResult field | Action |
|---------------------|----------------------|--------|
| `_shape_calendar` output | `calendar` | Replace with CalendarView assembly |
| `_shape_bazi` output | `bazi` | Replace with BaziView assembly |
| `feng_shui` + calendar copy | `feng_shui` + calendar display fields | Single feng_shui slice |
| `_shape_pattern` | `pattern` | Engine-driven PatternView |
| `_shape_score` | `score` | ScoreView + optional series |
| `_shape_interpretation` | `interpretation` | InterpretationView |
| `_shape_report_like` | `report`, `narrative` | Report/Narrative SSOT decision |
| `payload["stage"]` | `meta.stage` | |
| `payload["pipeline"]` | `meta.pipeline` | |
| `bazi_source` | `meta.bazi_source` | |

---

## 17. Contract tests (Phase 2+)

Golden file: `tests/applications/api/fixtures/analysis_result_1987_01_21.json`

Assertions:

- Schema version `meta.contract_version == "1.0"`
- Bazi pillars: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần
- `calendar.*_can_chi` matches `bazi` pillars
- No keys: `details`, `matched_rules`, `rule_id`, `templates_used`
- `score.total_score` not forced zero when RuleContext valid (Phase 2+)

---

## 18. Phase 1 completion status

| Deliverable | Status |
|-------------|--------|
| Schema documented | ✅ this file |
| Python dataclass implemented | ⏸ awaiting approval |
| Orchestrator emits AnalysisResult | ⏸ Phase 2+ |
| Portal bound to contract only | ⏸ Phase 7 |
| Behavior change | ❌ none in Phase 1 |

**STOP** — await approval before implementing Phase 2 (Unified Bazi Truth).
