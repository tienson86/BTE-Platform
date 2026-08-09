# Platform Runtime Flow

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_RUNTIME_FLOW |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## Complete lifecycle

```
User Request
        ↓
Calendar
        ↓
Bazi (Four Pillars)
        ↓
Analysis          (canonical_analysis_pipeline 2.0.0)
        ↓
Decision          (canonical_decision_pipeline 1.0.0)
        ↓
Luck              (canonical_luck_pipeline 1.0.0)
        ↓
Interpretation    (canonical_interpretation_pipeline 1.0.0)
        ↓
Report            (canonical_report_pipeline 1.0.0)
        ↓
Artifact          (Canonical Report Artifact)
        ↓
API / Portal response
```

---

## Stage detail

### 1. User Request

API or application accepts birth data and options. No engine internals are invoked out of order.

### 2. Analysis

Calendar and Four Pillars facts feed Seasonal, Strength, Temperature, Pattern, Pattern Evaluation, and Useful God analysis signal. Result: Canonical Analysis Result + trace + audit + diagnostics.

### 3. Decision

Consumes published analysis outputs only. Foundation → Priority → Override. Result: Canonical Decision Result (`final_*` fields).

### 4. Luck

Timeline foundation (`bz_09`) then luck analysis then luck decision. No fortune-quality invention; opportunity/risk from declared deltas. Result: Canonical Luck Result.

### 5. Interpretation

Builds interpretation context, selects knowledge/sentence candidates, assembles sections. No AI rewrite. Result: Canonical Interpretation Result.

### 6. Report

Report Foundation structures slots. Layout assigns theme/sections/blocks. Rendering selects an enabled renderer (`json` default) and publishes an in-memory artifact. Result: Canonical Report Result whose `canonical_report_artifact` is the rendering snapshot.

### 7. Artifact

Mime envelope (`application/json`, `text/html`, `text/markdown`, PDF/DOCX envelopes). Not written to disk by RX-1. Publisher / email / print remain disabled.

---

## Runtime invariants

| Invariant | Rule |
|-----------|------|
| Execute once | Each pipeline stage publishes once |
| Immutable outputs | No overwrite of published names |
| Fail closed | Contract / dependency / missing-input stop execution |
| No exception leak | Pipeline `run()` returns diagnostics |
| Determinism | Same inputs + clock ⇒ identical JSON |
| Version aware | SemVer constraints checked before stages |

---

## Failure flow

```
Violation
  → diagnostic code (FOUNDATION-MISSING, DEP-VIOLATION, …)
  → PIPE-FAIL
  → audit flags fail / not_run
  → official result with success=false
```

Callers never receive raw exception types from canonical `run()`.
