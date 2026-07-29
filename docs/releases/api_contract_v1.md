# BTE Platform API Contract V1.0

| Field | Value |
|-------|-------|
| **Contract version** | 1.0 |
| **API prefix** | `/api/v1` |
| **Freeze date** | 2026-07-27 |
| **Status** | Frozen |

---

## Purpose

This document freezes the HTTP JSON contract between BTE API and consumers (Customer Portal, integrations). V1.0 requires backward-compatible changes only: new optional fields allowed; required fields and semantics must not break.

---

## Envelope

### `APIResponse`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `success` | boolean | yes | `true` on successful handler completion |
| `message` | string | yes | Human-readable status (e.g. `"Analyze OK"`) |
| `data` | object | yes | Payload; shape depends on endpoint |
| `request_id` | string \| null | no | From `X-Request-ID` header or generated |

### Request headers

| Header | Required | Description |
|--------|----------|-------------|
| `X-Request-ID` | no | Client trace id; echoed in response |
| `Content-Type` | yes (POST) | `application/json` |

### Response headers

| Header | Description |
|--------|-------------|
| `X-Request-ID` | Request trace id |
| `X-Elapsed-Ms` | Server processing time |

---

## Request: `BirthRequest`

Used by all birth-datetime POST endpoints.

| Field | Type | Required | Constraints | Engine input? |
|-------|------|----------|-------------|---------------|
| `year` | int | yes | 1–9999 | yes |
| `month` | int | yes | 1–12 | yes |
| `day` | int | yes | 1–31 | yes |
| `hour` | int | no (default 0) | 0–23 | yes |
| `minute` | int | no (default 0) | 0–59 | yes |
| `gender` | string \| null | no | e.g. `"male"`, `"female"` | yes (bazi, feng shui) |
| `timezone` | string | no (default `Asia/Ho_Chi_Minh`) | IANA name | **echo only in V1.0** (not applied) |
| `full_name` | string \| null | no | — | no (presentation) |
| `birth_place` | string \| null | no | — | no (presentation) |
| `customer_id` | string \| null | no | — | no (presentation) |
| `metadata` | object \| null | no | Opaque client metadata | no (optional echo) |

**Portal requirement:** `full_name` and `birth_place` required client-side on analyze form; API does not enforce.

---

## Endpoints

| Method | Path | Pipeline stop | `data.pipeline` |
|--------|------|---------------|-----------------|
| GET | `/health` | — | — |
| POST | `/calendar` | calendar | `["calendar"]` |
| POST | `/bazi` | bazi | `["calendar","bazi"]` |
| POST | `/pattern` | pattern | through `pattern` |
| POST | `/score` | score | through `score` |
| POST | `/interpretation` | interpretation | through `interpretation` |
| POST | `/report` | report | through `report` (no `narrative`) |
| POST | `/narrative` | narrative | full 7 stages |
| POST | `/analyze` | narrative (= full) | full 7 stages + `stage: "analyze"` |

**Primary Portal endpoint:** `POST /api/v1/analyze`

---

## Response: `data` object (full analyze)

### Top-level keys (full run)

| Key | Type | Required (analyze) | Source |
|-----|------|-------------------|--------|
| `pipeline` | string[] | yes | Completed stage names |
| `stage` | string | yes on analyze | `"analyze"` |
| `calendar` | object | yes | Calendar + shaping |
| `bazi` | object | yes | `AnalysisResult.bazi_dict()` |
| `bazi_source` | object | yes | Provenance fingerprint |
| `feng_shui` | object \| null | yes | FengShuiEngine or null |
| `pattern` | object | yes | `pattern_dict()` |
| `pattern_source` | object | yes | Provenance |
| `score` | object | yes | `score_dict()` |
| `score_source` | object | yes | Provenance |
| `interpretation` | object | yes | `interpretation_dict()` |
| `interpretation_source` | object | yes | Provenance |
| `report` | object | yes | `report_dict()` |
| `report_source` | object | yes | Provenance |
| `narrative` | object | yes | `narrative_dict()` |
| `customer` | object | yes | `attach_presentation_metadata` |

**Not on wire (forbidden):** `rule_context` (unless future debug flag), engine raw objects, `templates_used`, score `details`/`modules`.

---

## JSON sections

### `data.calendar`

| Field | Type | Required | Nullable |
|-------|------|----------|----------|
| `solar_date` | string | yes | no |
| `lunar_date` | string | yes | no |
| `solar_year`, `solar_month`, `solar_day` | int | yes | no |
| `solar_hour`, `solar_minute` | int | yes | no |
| `julian_day` | float | yes | no |
| `solar_term` | object | yes | no |
| `lunar` | object | yes | no |
| `year_can_chi`, `month_can_chi`, `day_can_chi`, `hour_can_chi` | string | when bazi run | no |
| `cung_phi`, `menh_quai`, `nhom_trach`, `gua_name` | string | no | when feng_shui ok |

**Portal:** `presenters/calendar.js`

### `data.bazi`

| Field | Type | Required | Nullable |
|-------|------|----------|----------|
| `year_pillar`, `month_pillar`, `day_pillar`, `hour_pillar` | PillarView | yes | no |
| `day_master` | string | yes | no |
| `day_master_element` | string | yes | no |
| `day_master_yin_yang` | string | yes | no |
| `gender` | string \| null | no | yes |
| `hidden_stems` | string[] | no | no |
| `ten_gods` | string[] | no | no |
| `shensha` | string[] | no | no |

**PillarView:** `stem`, `branch`, `hidden_stems`, `ten_god`, `nap_am`, `truong_sinh`

**Portal:** `presenters/bazi.js`

### `data.feng_shui`

| Field | Type | Required | Nullable |
|-------|------|----------|----------|
| (engine dict) | object | no | **yes** (null if gender invalid/missing) |

### `data.pattern`

| Field | Type | Required | Nullable |
|-------|------|----------|----------|
| `success` | boolean | yes | no |
| `pattern` | string | yes | no |
| `cach_cuc` | string | yes | no |
| `score` | float | yes | no |
| `priority` | int | yes | no |
| `than`, `than_vuong_nhuoc`, `tong_cach` | string | no | omitted if empty |
| `dung_than`, `hy_than`, `ky_than`, `dieu_hau` | string | no | omitted if empty |

**Portal:** `presenters/pattern.js`

### `data.score`

| Field | Type | Required | Nullable |
|-------|------|----------|----------|
| `success` | boolean | yes | no |
| `total_score` | float | yes | no |
| `strength_score`, `pattern_score`, `ten_god_score`, `wuxing_score` | float | yes | no |
| `grade`, `confidence`, `recommendation` | string | yes | empty string allowed |
| `useful_god_score`, `shensha_score`, `luck_score` | float | no | omitted if zero |
| `interpretation_score` | float | no | omitted if null |
| `wuxing_series`, `ten_god_series` | array | no | omitted if empty |

**Excluded:** `details`, `modules`, `execution_time`, `weighted_score`

**Portal:** `presenters/score.js`

### `data.interpretation`

| Field | Type | Required | Nullable |
|-------|------|----------|----------|
| `sections` | array | yes | no (may be empty) |
| `section_count` | int | yes | no |
| `sentence_count` | int | yes | no |
| `confidence` | float | yes | no |

**Section:** `id`, `title`, `body` (strings)

**Excluded:** `summary`, `rules_used`, `matched_rule_count`, `resolved_rule_count`

**Portal:** `presenters/interpretation.js`

### `data.report` / `data.narrative`

| Field | Type | Required | Nullable |
|-------|------|----------|----------|
| `title` | string | yes | no |
| `markdown` | string | yes | no |
| `html` | string | yes | no |
| `section_count` | int | yes | no |
| `tone` | string | narrative only | yes (omitted in V1.0) |
| `metrics` | object | narrative only | yes (omitted in V1.0) |

**Excluded:** `templates_used`, `pdf_path`, `appendix`

**Portal:** `presenters/narrative.js`, `reports.js`

### `data.customer` (presentation only)

| Field | Type | Required |
|-------|------|----------|
| `full_name` | string \| null | no |
| `birth_place` | string \| null | no |
| `gender` | string \| null | no |
| `timezone` | string | no |
| `customer_id` | string \| null | no |

**Not passed to engines.**

### `*_source` provenance blocks

| Field | Type | Example |
|-------|------|---------|
| `engine` | string | Module path |
| `method` | string | `build`, `run`, `render_from_analysis` |
| `contract` | string | e.g. `li_chun_jdn_v1` |
| `view` | string | Truth module path |

---

## Null handling

| Scenario | Behavior |
|----------|----------|
| `gender` null | 200; `feng_shui` may be `null` |
| Missing optional score fields | Omitted from JSON (not `null`) |
| Empty pattern labels | Field omitted |
| Stage endpoint partial run | Absent keys for stages not run |
| `customer` fields null | Included as `null` when not in request |

---

## Error handling

| Condition | HTTP | Body |
|-----------|------|------|
| Invalid `BirthRequest` (Pydantic) | 422 | FastAPI validation detail |
| Pipeline failure | 500 / wrapped | `success: false`, message with stage |
| Unknown stage | error | PipelineAPIError |

**Invalid examples (422):** missing `year`, `month` > 12, `day` > 31, `hour` > 23

---

## Versioning rules

| Rule | V1.0 policy |
|------|-------------|
| Contract version | `meta.contract_version` = `"1.0"` when exposed |
| API path | `/api/v1/*` frozen |
| New optional fields | Allowed in 1.0.x |
| Remove required field | **Forbidden** in 1.0.x |
| Rename field | **Forbidden** — use wrapper or 2.0 |
| Change field type | **Forbidden** without version bump |
| New endpoint | Allowed if does not break existing |

---

## Backward compatibility policy

1. **Additive only** in 1.0.x: new optional JSON fields, new endpoints.
2. **Wrappers** for renamed internal APIs; public field names unchanged.
3. **Portal** must tolerate omitted optional fields (already does via fallbacks).
4. **Clients** must not depend on excluded internal fields.
5. Breaking changes require **API v2** proposal and architecture approval.

---

## Portal binding summary

| API `data.*` | Portal consumer |
|--------------|-------------------|
| Full `data` | `ResultStore` → `result.js` |
| `calendar` | `calendar.js` |
| `bazi` | `bazi.js`, `summary_builder.js` |
| `pattern` | `pattern.js` |
| `score` | `score.js` |
| `interpretation` | `interpretation.js` |
| `narrative` | `narrative.js` |
| `report` | `reports.js` (history) |
| `customer` | `summary_builder.js`, `executive.js` |

**Portal does not recalculate engine outputs.**

---

## Related documents

- `docs/releases/analysis_result_contract_v1.md` — in-memory SSOT
- `docs/releases/architecture_v1_frozen.md` — pipeline freeze
- `applications/api/schemas/common.py` — Pydantic models

---

**API Contract V1.0 — Frozen 2026-07-27**
