# Pattern Engine Domain Models

**Module:** `engines/analysis_engine/03_pattern_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the official domain model specification for the Pattern Engine.

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

The Pattern Engine defines the following primary models:

```text
AnalysisContext (Input)
        │
        │  reads AnalysisContext.strength_result
        │  reads AnalysisContext.temperature_result
        ▼
PatternContext
        │
        ▼
StructureAnalysis
DayMasterRelationAnalysis
StandardPatternAnalysis
TransformationPatternAnalysis
SpecialPatternAnalysis
FollowPatternAnalysis
MixedExceptionalAnalysis
        │
        ▼
PatternCandidateSet
CandidateEvaluation
ConflictResolution
PriorityResolution
        │
        ▼
PatternScore
        │
        ▼
ConfidenceEvaluation
        │
        ▼
PatternResult
```

The engine does not define a dedicated PatternInput wrapper. Shared AnalysisContext is used directly.

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

Mutability:

Immutable

Lifecycle:

Created and enriched before Pattern Engine execution.

Modified:

Never by Pattern Engine.

---

# 5. StrengthResult (Upstream via AnalysisContext)

Owner:

- Strength Engine

Access Path:

```text
AnalysisContext.strength_result
```

Purpose:

Provides published Day Master strength evidence required by Pattern Rules.

Mutability:

Immutable

Lifecycle:

Created by Strength Engine and attached to AnalysisContext before Pattern Engine execution.

Modified:

Never by Pattern Engine.

---

# 6. TemperatureResult (Upstream via AnalysisContext)

Owner:

- Temperature Engine

Access Path:

```text
AnalysisContext.temperature_result
```

Purpose:

Provides published climate evidence required by Pattern Rules.

Mutability:

Immutable

Lifecycle:

Created by Temperature Engine and attached to AnalysisContext before Pattern Engine execution.

Modified:

Never by Pattern Engine.

---

# 7. PatternContext

Owner:

Pattern Engine

Purpose:

Internal normalized analytical context.

Contains:

- normalized chart references
- projected strength evidence
- projected temperature evidence
- Day Master relationship projections
- cached calculations
- runtime configuration
- rule references

Mutability:

Immutable after creation.

---

# 8. StructureAnalysis

Represents chart structure evaluation for pattern eligibility.

Contains:

- structural indicators
- eligibility flags
- structure score
- matched_rules
- evidence

---

# 9. DayMasterRelationAnalysis

Represents Day Master relationship with chart composition.

Contains:

- relational indicators
- composition alignment
- relation score
- matched_rules
- evidence

---

# 10. StandardPatternAnalysis

Represents standard pattern candidate evaluation.

Contains:

- candidate patterns
- match scores
- matched_rules
- evidence

---

# 11. TransformationPatternAnalysis

Represents transformed pattern candidate evaluation.

Contains:

- candidate patterns
- transformation indicators
- match scores
- matched_rules
- evidence

---

# 12. SpecialPatternAnalysis

Represents special pattern candidate evaluation.

Contains:

- candidate patterns
- match scores
- matched_rules
- evidence

---

# 13. FollowPatternAnalysis

Represents follow pattern candidate evaluation.

Contains:

- candidate patterns
- follow direction
- match scores
- matched_rules
- evidence

---

# 14. MixedExceptionalAnalysis

Represents mixed and exceptional pattern candidate evaluation.

Contains:

- candidate patterns
- exceptional indicators
- match scores
- matched_rules
- evidence

---

# 15. PatternCandidateSet

Represents the generated set of competing pattern candidates.

Contains:

- candidate identifiers
- candidate categories
- generation evidence

---

# 16. CandidateEvaluation

Represents evaluation results for each candidate.

Contains:

- candidate identifier
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
- selected candidate
- rejected candidates
- evidence

---

# 19. PatternScore

Represents aggregated analytical scores.

Contains:

- structure score
- relation score
- category scores
- resolution score
- weighted score
- normalized score

---

# 20. ConfidenceEvaluation

Represents confidence assessment.

Contains:

- confidence level
- confidence score
- coverage
- reasoning

---

# 21. PatternResult

Represents the final analytical result.

Contains at least:

- identified pattern
- pattern category
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

# 22. Ownership Rules

Each model has exactly one owner.

Models shall never be modified by downstream engines.

Pattern Engine shall never modify AnalysisContext.strength_result or AnalysisContext.temperature_result.

---

# 23. Serialization

All models shall support deterministic serialization.

Serialization format shall remain version compatible within V1.x.

---

# 24. Validation

Every model shall define:

- required fields
- optional fields
- constraints
- invariant rules

Validation occurs before model publication.

---

# 25. Compatibility

The model hierarchy shall remain backward compatible throughout the V1.x lifecycle.

Breaking changes require V2.
