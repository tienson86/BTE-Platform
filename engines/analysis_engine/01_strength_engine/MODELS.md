# Strength Engine Domain Models

**Module:** `engines/analysis_engine/01_strength_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the official domain model specification for the Strength Engine.

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

The Strength Engine defines the following primary models:

```text
AnalysisContext (Input)

        │

        ▼

StrengthContext

        │

        ▼

SeasonAnalysis

RootAnalysis

StemAnalysis

SupportAnalysis

ControlAnalysis

DrainAnalysis

        │

        ▼

StrengthScore

        │

        ▼

ConfidenceEvaluation

        │

        ▼

StrengthResult
```

---

# 4. AnalysisContext (External)

Owner:

- Bazi Engine

Purpose:

Provides immutable analytical input.

Mutability:

Immutable

Lifecycle:

Created before Strength Engine execution.

Modified:

Never.

---

# 5. StrengthContext

Owner:

Strength Engine

Purpose:

Internal normalized analytical context.

Contains:

- normalized references
- cached calculations
- runtime configuration
- rule references

Mutability:

Immutable after creation.

---

# 6. SeasonAnalysis

Represents seasonal influence.

Contains:

- season
- weight
- score
- matched_rules
- evidence

---

# 7. RootAnalysis

Represents rooting strength.

Contains:

- hidden stems
- rooting depth
- rooting score
- evidence

---

# 8. StemAnalysis

Represents Heavenly Stem influence.

Contains:

- supporting stems
- controlling stems
- stem weights
- score

---

# 9. SupportAnalysis

Represents productive relationships.

Contains:

- producing elements
- assisting elements
- total support
- evidence

---

# 10. ControlAnalysis

Represents restrictive relationships.

Contains:

- controlling elements
- weakening factors
- total control
- evidence

---

# 11. DrainAnalysis

Represents energy leakage.

Contains:

- output elements
- drain weight
- drain score
- evidence

---

# 12. StrengthScore

Represents aggregated analytical scores.

Contains:

- season score
- root score
- stem score
- support score
- control score
- drain score
- weighted score
- normalized score

---

# 13. ConfidenceEvaluation

Represents confidence assessment.

Contains:

- confidence level
- confidence score
- coverage
- reasoning

---

# 14. StrengthResult

Represents the final analytical result.

Contains:

- StrengthScore
- ConfidenceEvaluation
- matched_rules
- reasoning
- execution metadata

Immutable.

Returned by the Public API.

---

# 15. Ownership Rules

Each model has exactly one owner.

Models shall never be modified by downstream engines.

---

# 16. Serialization

All models shall support deterministic serialization.

Serialization format shall remain version compatible within V1.x.

---

# 17. Validation

Every model shall define:

- required fields
- optional fields
- constraints
- invariant rules

Validation occurs before model publication.

---

# 18. Compatibility

The model hierarchy shall remain backward compatible throughout the V1.x lifecycle.

Breaking changes require V2.