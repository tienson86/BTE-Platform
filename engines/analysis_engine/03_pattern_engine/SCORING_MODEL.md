# Pattern Engine Scoring Model

**Module:** `engines/analysis_engine/03_pattern_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Mathematical Model Specification)

---

# 1. Purpose

This document defines the mathematical scoring model used by the Pattern Engine.

It specifies the scoring dimensions, weighting principles, normalization rules, confidence calculation inputs, and traceability requirements.

The scoring model is independent of the execution algorithm.

---

# 2. Design Principles

The scoring model shall be:

- Rule-driven
- Deterministic
- Explainable
- Extensible
- Versioned
- Reproducible

All numerical values originate from the Rule Database.

---

# 3. Scoring Architecture

```text
Individual Rule Scores
        │
        ▼
Dimension Scores
        │
        ▼
Weighted Scores
        │
        ▼
Candidate Ranking
        │
        ▼
Normalization
        │
        ▼
Pattern Identity
```

---

# 4. Scoring Dimensions

The model evaluates the following analytical dimensions:

- Chart Structure Influence
- Standard Pattern Match Strength
- Special Pattern Match Strength
- Candidate Resolution Strength

Each dimension is evaluated independently.

---

# 5. Weight Model

Each dimension defines:

- Raw Score
- Weight
- Weighted Score
- Evidence
- Matched Rules

Weights are loaded from the Rule Database.

The engine shall not hard-code weights.

---

# 6. Normalization

The aggregated score shall be normalized using the configured scoring model.

Normalization shall:

- preserve ordering;
- maintain determinism;
- avoid score overflow;
- remain version-compatible.

---

# 7. Pattern Classification

Normalized candidate scores are mapped to a Pattern identity.

Classification thresholds and selection criteria are defined in the Rule Database.

The engine shall never embed threshold values in source code.

---

# 8. Candidate Resolution Model

Competing candidates are resolved using:

- Candidate Resolution Rules
- Priority Rules
- Score separation
- Special-pattern override criteria where defined by rules

Resolution shall remain deterministic and explainable.

---

# 9. Confidence Inputs

Confidence evaluation considers:

- Rule coverage
- Data completeness
- Rule consistency
- Evidence quality
- Analytical agreement
- Candidate separation quality
- AnalysisContext.strength_result completeness where required
- AnalysisContext.temperature_result completeness where required

Confidence is evaluated independently from the pattern score where applicable.

---

# 10. Explainability

Every score shall include:

- contributing rules;
- contributing analyzers;
- calculation evidence;
- weighting details;
- normalization path;
- candidate resolution path;
- StrengthResult and TemperatureResult references from AnalysisContext when used as evidence.

No score may exist without traceability.

---

# 11. Versioning

The scoring model is version-controlled.

Any modification to:

- dimensions;
- weighting strategy;
- normalization method;
- classification thresholds;
- candidate resolution strategy;

requires a new scoring model version.

---

# 12. Constraints

The scoring model shall never:

- modify Rule Database contents;
- infer undocumented weights;
- skip mandatory dimensions;
- generate random scores;
- recompute Day Master strength scores;
- recompute climate scores.

---

# 13. Acceptance Criteria

The scoring model is accepted when:

- identical inputs always produce identical normalized scores;
- all score contributions are traceable;
- confidence is reproducible;
- pattern classification is deterministic;
- candidate resolution is deterministic.
