# Luck Analysis Engine

| Field | Value |
|-------|-------|
| **Document** | LUCK_ANALYSIS_ENGINE |
| **Sprint** | LE-2 |
| **Analysis version** | 1.0.0 |
| **Foundation** | 1.0.0 (frozen) |
| **Status** | Canonical |

---

## Analysis philosophy

LE-2 measures **structural overlap** between a Luck Timeline (LE-1) and published AX-2 / AX-3 identities.

It does **not**:

- decide whether a period is good or bad
- compute auspiciousness, risk, or fortune quality
- override Useful God
- mutate Canonical Analysis Result or Canonical Decision Result

Impact scores are overlap intensity (`unit = overlap_intensity`), not fortune scores.

---

## Impact model

| Model | Meaning |
|-------|---------|
| `ImpactDirection` | `amplifying` / `dampening` / `neutral` / `unresolved` — identity match vs divergence |
| `ImpactScore` | 0–100 share of periods matching reference tokens |
| `ImpactDelta` | `(amplifying − dampening) / n` in `[-1, 1]` |
| `ImpactConfidence` | Completeness of upstream tokens (`high`…`none`) |
| `ImpactEvidence` | Period ids + consumed published field names |
| `ImpactSummary` | Structural counts only |

---

## Impact hierarchy

```
Seasonal Impact
  ↓
Strength Impact
  ↓
Temperature Impact
  ↓
Pattern Impact
  ↓
Pattern Evaluation Impact
  ↓
Useful God Impact
  ↓
overall_analysis_impact
```

Each stage consumes the frozen timeline plus the matching AX-2 (and AX-3 for Useful God) snapshot. Upstream objects are copied; never written back.

---

## Analysis trace

`analysis_trace` records:

- timeline consumed (`timeline_id`, `timeline_version`, `chart_id`)
- analysis consumed (`pipeline_id`, `pipeline_version`, `stage_order`)
- decision consumed (`pipeline_id`, `decision_pipeline_version`)
- impact stages executed
- outputs published
- `started_at` / `completed_at`

This is **not** a Decision Trace.

---

## Registry

`ImpactRegistry` lists `stage_id`, `dependencies`, `consumed_inputs`, `published_outputs`, `version`, `enabled`.

Canonical order is frozen for analysis version 1.0.0.

---

## Diagnostics

| Code | Meaning |
|------|---------|
| `TIMELINE-MISSING` | No LuckTimeline input |
| `ANALYSIS-MISSING` | No Canonical Analysis Result |
| `DECISION-MISSING` | No Canonical Decision Result |
| `DEP-VIOLATION` | Impact dependency order broken |
| `CONTRACT-VIOLATION` | Published contract / version failure |
| `OUT-DUPLICATE` | Duplicate impact publication |
| `PIPE-OK` | Successful run |
| `PIPE-FAIL` | Failed run |

`run()` never raises to API callers.

---

## Future LE-3 integration

LE-3 Luck Decision consumes these published outputs only:

`seasonal_impact` … `useful_god_impact`, `overall_analysis_impact`, `analysis_trace`, `analysis_diagnostics`, `analysis_version`.

LE-3 must not recompute AX-2 scores or rewrite Useful God Foundation packages.

---

## Future AX-4 integration

If a later Foundation version activates AX-2 `luck_cycle`, Luck Analysis remains a **separate engine**. AX-4 may bind this engine’s result; it must not fold fortune logic into Analysis Engine.
