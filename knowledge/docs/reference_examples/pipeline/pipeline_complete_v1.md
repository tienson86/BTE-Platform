# Pipeline Complete Reference Example

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Pipeline Reference Example
>
> Origin: reference_example
>
> BTE Platform

---

# Summary

Canonical complete documentation of the BTE analysis pipeline as defined in `PIPELINE_MODEL_SPEC.md`. Describes every stage, data exchange, and responsibility boundary from raw birth input through frozen Result output.

---

# Description

This reference example maps the standard BTE Platform processing flow for Bazi analysis. Each stage is stateless, deterministic, and produces structured data consumed exclusively by the next stage. The pipeline terminates with a single `Result` object; Report, API, and UI layers consume Result downstream.

Subject anchor: male born `1987-01-21T04:10:00` in Ha Tay, Vietnam (`Asia/Ho_Chi_Minh`), corresponding to `context_complete_v1.json` and `result_complete_v1.json`.

---

# Pipeline Stages

## 1. Input

**Purpose:** Accept raw birth data.

**Input:**

- Birth datetime: `1987-01-21T04:10:00`
- Gender: `male`
- Timezone: `Asia/Ho_Chi_Minh`
- Location: `Ha Tay, Vietnam`

**Output:** Raw Input object passed to Context Builder.

**Responsibility:** No normalization, no calculation.

---

## 2. Context Builder

**Purpose:** Transform Raw Input into frozen Context per `CONTEXT_MODEL_SPEC.md`.

**Input:** Raw Input.

**Output:** Context with `metadata`, `subject`, `calendar`, `natal_chart`, `analysis`, `luck`, `runtime`, `extensions`.

**Reference:** `context/context_complete_v1.json`

**Responsibility:** Sole stage permitted to convert raw data into Context.

---

## 3. Validation

**Purpose:** Verify Context integrity before Rule processing.

**Checks:**

- Required sections present (metadata, subject, calendar, natal_chart).
- ISO-8601 timestamps.
- Valid enum values.
- No Rule or Interpretation embedded in Context.

**On failure:** Pipeline stops; standardized error returned.

**Reference:** `VALIDATION_STANDARD.md` Levels 1–5.

---

## 4. Rule Loader

**Purpose:** Load Rule Database into memory.

**Input:** Rule CSV/JSON from `database/`.

**Output:** Rule registry indexed by `id` and `code`.

**Responsibility:** Read only. No matching, no modification.

**Reference:** `rule/rule_complete_v1.json`

---

## 5. Rule Matcher

**Purpose:** Evaluate each Rule against Context conditions.

**Input:** Context + Rule registry.

**Output:** Rule match list with `rule_id`, `matched`, `priority`, `weight_applied`.

**Example match:** `SUP-000001` (Wood Generates Fire) matches when season is spring and strength is balanced or weak.

---

## 6. Priority Resolver

**Purpose:** Resolve conflicts among matched Rules.

**Resolves:**

- Duplicate matches.
- Exclusive Rules.
- Stack limits (`max_stack`).
- Order by `priority.level` and `priority.order`.

**Output:** Final ordered Rule match set.

---

## 7. Score Engine

**Purpose:** Compute numeric scores from resolved Rule matches and analysis data.

**Input:** Resolved Rule matches + Context analysis.

**Output:** Scores object (`strength`, `pattern`, `temperature`, `support`, `overall`).

**Reference scores:** `result/result_complete_v1.json` → `scores`.

---

## 8. Interpretation Builder

**Purpose:** Generate natural-language interpretations from structured analysis.

**Input:** Scores + analysis + resolved Rules.

**Output:** Interpretations array with `topic` and `text`.

**Constraint:** No Rule Database content in output text.

---

## 9. Result Builder

**Purpose:** Assemble final Result per `RESULT_MODEL_SPEC.md`.

**Input:** All prior stage outputs.

**Output:** Frozen Result object.

**Reference:** `result/result_complete_v1.json`

**Invariant:** Result contains metadata, summary, and rule_matches at minimum.

---

# Data Flow Diagram

```
Raw Input
    │
    ▼
Context Builder ──► context_complete_v1.json
    │
    ▼
Validation
    │
    ▼
Rule Loader ──► rule_complete_v1.json
    │
    ▼
Rule Matcher
    │
    ▼
Priority Resolver
    │
    ▼
Score Engine
    │
    ▼
Interpretation Builder
    │
    ▼
Result Builder ──► result_complete_v1.json
```

---

# Pipeline Properties

| Property | Value |
|----------|-------|
| Deterministic | Yes |
| Stateless | Yes |
| Idempotent | Yes |
| Traceable | Yes via diagnostics |
| Testable | Yes via reference examples |

---

# References

- `PIPELINE_MODEL_SPEC.md`
- `CONTEXT_MODEL_SPEC.md`
- `RESULT_MODEL_SPEC.md`
- `RULE_MODEL_SPEC.md`
- `VALIDATION_STANDARD.md`
- `METADATA_STANDARD.md`
- `REFERENCE_EXAMPLE_REQUIREMENTS.md`

---

# Metadata

| Field | Value |
|-------|-------|
| schema_version | 1.0.0 |
| version | 1.0.0 |
| status | active |
| origin | reference_example |
| author | BTE |
| created_at | 2026-07-29T08:00:00Z |
| updated_at | 2026-07-29T08:30:00Z |
