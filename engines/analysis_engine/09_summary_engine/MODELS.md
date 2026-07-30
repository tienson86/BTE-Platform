# Summary Engine Domain Models

**Module:** `engines/analysis_engine/09_summary_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the official domain model specification for the Summary Engine.

---

# 2. Design Principles

- Immutable by default
- Explicit ownership
- Strong typing
- Deterministic serialization
- Version compatibility
- Non-destructive aggregation
- No presentation concerns

---

# 3. Domain Model Overview

```text
AnalysisContext (Input)
        │
        │  reads all upstream StageResults
        ▼
SummaryEvaluationContext
        │
        ▼
StrengthSummaryView
TemperatureSummaryView
PatternSummaryView
UsefulGodSummaryView
TenGodsSummaryView
CombinationSummaryView
ShenShaSummaryView
LuckSummaryView
        │
        ▼
CrossStageConsistencyReport
ConsolidatedConfidenceSummary
EvidenceIndex
        │
        ▼
SummaryResult
```

No dedicated SummaryInput wrapper is defined. Shared AnalysisContext is used directly.

---

# 4. AnalysisContext (External)

Owner: Analysis Engine orchestrator / Analysis Runtime

Provides chart facts and all published upstream stage results.

Mutability: immutable input for the stage.

---

# 5. Upstream Result Models (External)

| Model | Owner |
|-------|-------|
| StrengthResult | Strength Engine |
| TemperatureResult | Temperature Engine |
| PatternResult | Pattern Engine |
| UsefulGodResult | Useful God Engine |
| TenGodsResult | Ten Gods Engine |
| CombinationResult | Combination Engine |
| ShenShaResult | ShenSha Engine |
| LuckResult | Luck Engine |

Summary Engine must not redefine or mutate these models.

---

# 6. SummaryEvaluationContext

Request-scoped internal working context. Not part of public API.

---

# 7. Domain Summary Views

Non-destructive summary projections of each upstream result:

- StrengthSummaryView
- TemperatureSummaryView
- PatternSummaryView
- UsefulGodSummaryView
- TenGodsSummaryView
- CombinationSummaryView
- ShenShaSummaryView
- LuckSummaryView

Summary views reference upstream results; they do not replace them.

---

# 8. CrossStageConsistencyReport

Represents outcome of cross-stage consistency validation.

---

# 9. ConsolidatedConfidenceSummary

Represents aggregated confidence profile across all stages.

---

# 10. EvidenceIndex

Unified index of KnowledgeReferences / RuleEvidence from all upstream stages.

---

# 11. SummaryResult

Public immutable output model.

Shall include at minimum:

- consolidated domain summary views or equivalent references
- cross-stage consistency status
- consolidated confidence summary
- evidence index
- diagnostics / execution metadata slots aligned with shared Analysis Engine models

Exact field-level schema remains backward compatible within V1.x once published.

---

# 12. AnalysisResult Relationship

`SummaryResult` is a component of `AnalysisResult`.

Analysis Runtime assembles final `AnalysisResult` including all stage results plus `SummaryResult`.

---

# 13. Ownership

All Summary-specific models above are owned by Summary Engine unless marked external.

---

# 14. Acceptance Criteria

Domain models are accepted when overview, summary views, and SummaryResult contract are complete.
