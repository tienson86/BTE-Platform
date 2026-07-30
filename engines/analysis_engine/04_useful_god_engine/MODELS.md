# Useful God Engine Domain Models

**Module:** `engines/analysis_engine/04_useful_god_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the official domain model specification for the Useful God Engine.

All data exchanged within the module shall conform to these model definitions.

No implementation may introduce incompatible domain objects without a major version change.

---

# 2. Design Principles

The domain model follows these principles:

- Immutable by default
- Explicit ownership
- Strong typing
- Deterministic serialization
- Version compatibility
- Explainable analytical data
- No presentation concerns
- No persistence concerns

---

# 3. Domain Model Overview

The Useful God Engine defines the following primary models:

```text
AnalysisContext (Input)
        │
        │  reads AnalysisContext.strength_result
        │  reads AnalysisContext.temperature_result
        │  reads AnalysisContext.pattern_result
        ▼
UsefulGodContext
        │
        ▼
StrengthBalanceAnalysis
ClimateBalanceAnalysis
PatternRequirementAnalysis
EquilibriumAnalysis
RelationAnalysis
AdjustmentPriorityAnalysis
        │
        ▼
UsefulGodCandidateSet
CandidateEvaluation
ConflictResolution
PriorityResolution
        │
        ▼
YongShenDetermination
XiShenDetermination
JiShenDetermination
XianShenDetermination
        │
        ▼
UsefulGodScore
        │
        ▼
ConfidenceEvaluation
        │
        ▼
UsefulGodResult
```

The engine does not define a dedicated UsefulGodInput wrapper. Shared AnalysisContext is used directly.

---

# 4. AnalysisContext (External)

Owner:

- Analysis Engine orchestrator

Purpose:

Provides immutable analytical input, including published upstream stage results.

Contains:

- Calendar and BaZi chart facts
- Runtime metadata
- `strength_result` published by Strength Engine
- `temperature_result` published by Temperature Engine
- `pattern_result` published by Pattern Engine

Mutability:

Immutable

Lifecycle:

Created and enriched before Useful God Engine execution.

Modified:

Never by Useful God Engine.

---

# 5. StrengthResult (Upstream via AnalysisContext)

Owner:

- Strength Engine

Access Path:

```text
AnalysisContext.strength_result
```

Purpose:

Provides published Day Master strength evidence required by Useful God Rules.

Mutability:

Immutable

---

# 6. TemperatureResult (Upstream via AnalysisContext)

Owner:

- Temperature Engine

Access Path:

```text
AnalysisContext.temperature_result
```

Purpose:

Provides published climate evidence required by Useful God Rules.

Mutability:

Immutable

---

# 7. PatternResult (Upstream via AnalysisContext)

Owner:

- Pattern Engine

Access Path:

```text
AnalysisContext.pattern_result
```

Purpose:

Provides published Pattern evidence required by Useful God Rules.

Mutability:

Immutable

---

# 8. UsefulGodContext

Owner:

Useful God Engine

Purpose:

Internal normalized analytical context.

Contains:

- normalized chart references
- projected strength, temperature, and pattern evidence
- cached calculations
- runtime configuration
- rule references

Mutability:

Immutable after creation.

---

# 9. StrengthBalanceAnalysis

Represents strength-balance requirements for Useful God determination.

Contains:

- balance indicators
- score
- matched_rules
- evidence

---

# 10. ClimateBalanceAnalysis

Represents climate-balance requirements for Useful God determination.

Contains:

- climate adjustment indicators
- score
- matched_rules
- evidence

---

# 11. PatternRequirementAnalysis

Represents Pattern requirements for Useful God determination.

Contains:

- pattern-derived requirements
- score
- matched_rules
- evidence

---

# 12. EquilibriumAnalysis

Represents five-element equilibrium evaluation.

Contains:

- equilibrium state
- imbalance indicators
- score
- evidence

---

# 13. RelationAnalysis

Represents supporting and controlling relationships.

Contains:

- supporting factors
- controlling factors
- relation score
- evidence

---

# 14. AdjustmentPriorityAnalysis

Represents adjustment priority evaluation.

Contains:

- priority ordering
- adjustment indicators
- score
- evidence

---

# 15. UsefulGodCandidateSet

Represents the generated set of Useful God candidates.

Contains:

- primary candidates
- secondary candidates
- alternative candidates
- generation evidence

---

# 16. CandidateEvaluation

Represents evaluation results for each candidate.

Contains:

- candidate identifier
- candidate rank class
- evaluation score
- eligibility state
- evidence

---

# 17. ConflictResolution

Represents conflict resolution among competing candidates.

Contains:

- conflicting candidates
- resolution outcome
- resolution path
- evidence

---

# 18. PriorityResolution

Represents priority resolution among matched rules and candidates.

Contains:

- priority ordering
- selected candidates
- rejected candidates
- evidence

---

# 19. YongShenDetermination

Represents Useful God determination.

Contains:

- useful_god
- supporting evidence
- matched_rules

---

# 20. XiShenDetermination

Represents Favorable God determination.

Contains:

- favorable_gods
- supporting evidence
- matched_rules

---

# 21. JiShenDetermination

Represents Unfavorable God determination.

Contains:

- unfavorable_gods
- supporting evidence
- matched_rules

---

# 22. XianShenDetermination

Represents Neutral God determination.

Contains:

- neutral_gods
- supporting evidence
- matched_rules

---

# 23. UsefulGodScore

Represents aggregated analytical scores.

Contains:

- balance scores
- candidate scores
- resolution score
- weighted score
- normalized score

---

# 24. ConfidenceEvaluation

Represents confidence assessment.

Contains:

- confidence level
- confidence score
- coverage
- reasoning

---

# 25. UsefulGodResult

Represents the final analytical result.

Contains at least:

- useful_god
- favorable_gods
- unfavorable_gods
- neutral_gods
- candidate rankings
- confidence
- matched rules
- rejected candidates
- reasoning
- diagnostics
- metadata

Immutable.

Returned by the Public API.

Published into AnalysisResult.

---

# 26. Ownership Rules

Each model has exactly one owner.

Models shall never be modified by downstream engines.

Useful God Engine shall never modify AnalysisContext.strength_result, AnalysisContext.temperature_result, or AnalysisContext.pattern_result.

---

# 27. Serialization

All models shall support deterministic serialization.

Serialization format shall remain version compatible within V1.x.

---

# 28. Validation

Every model shall define:

- required fields
- optional fields
- constraints
- invariant rules

Validation occurs before model publication.

---

# 29. Compatibility

The model hierarchy shall remain backward compatible throughout the V1.x lifecycle.

Breaking changes require V2.
