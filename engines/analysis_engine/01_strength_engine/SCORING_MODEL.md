# Strength Engine Scoring Model

**Module:** `engines/analysis_engine/01_strength_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Mathematical Model Specification)

---

# 1. Purpose

This document defines the mathematical scoring model used by the Strength Engine.

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
Normalization
        │
        ▼
Overall Strength Score
        │
        ▼
Strength Level
```

---

# 4. Scoring Dimensions

The model evaluates the following analytical dimensions:

- Seasonal Influence
- Root Strength
- Heavenly Stem Influence
- Earthly Branch Influence
- Support Influence
- Control Influence
- Drain Influence

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

# 7. Strength Classification

The normalized score is mapped to a strength level.

Classification thresholds are defined in the Rule Database.

The engine shall never embed threshold values in source code.

---

# 8. Confidence Inputs

Confidence evaluation considers:

- Rule coverage
- Data completeness
- Rule consistency
- Evidence quality
- Analytical agreement

Confidence is evaluated independently from the strength score.

---

# 9. Explainability

Every score shall include:

- contributing rules;
- contributing analyzers;
- calculation evidence;
- weighting details;
- normalization path.

No score may exist without traceability.

---

# 10. Versioning

The scoring model is version-controlled.

Any modification to:

- dimensions;
- weighting strategy;
- normalization method;
- classification thresholds;

requires a new scoring model version.

---

# 11. Constraints

The scoring model shall never:

- modify Rule Database contents;
- infer undocumented weights;
- skip mandatory dimensions;
- generate random scores.

---

# 12. Acceptance Criteria

The scoring model is accepted when:

- identical inputs always produce identical normalized scores;
- all score contributions are traceable;
- confidence is reproducible;
- classification is deterministic.