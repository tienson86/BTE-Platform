# Temperature Engine Scoring Model

**Module:** `engines/analysis_engine/02_temperature_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Mathematical Model Specification)

---

# 1. Purpose

This document defines the mathematical scoring model used by the Temperature Engine.

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
Overall Climate Score
        │
        ▼
Temperature Level
        │
        ▼
Adjustment Indicators
```

---

# 4. Scoring Dimensions

The model evaluates the following analytical dimensions:

- Seasonal Temperature Influence
- Warm / Cold Balance
- Dryness Influence
- Humidity Influence
- Climate Equilibrium
- Environmental Support
- Climate Adjustment Requirements

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

# 7. Temperature Classification

The normalized score is mapped to a temperature level.

Classification thresholds are defined in the Rule Database.

The engine shall never embed threshold values in source code.

---

# 8. Adjustment Classification

Climate adjustment requirements are derived from:

- Adjustment Rules
- Equilibrium state
- Warm / cold imbalance
- Dryness and humidity imbalance
- Environmental support deficits

Adjustment indicators shall remain rule-defined and explainable.

---

# 9. Confidence Inputs

Confidence evaluation considers:

- Rule coverage
- Data completeness
- Rule consistency
- Evidence quality
- Analytical agreement
- StrengthResult completeness where required

Confidence is evaluated independently from the climate score.

---

# 10. Explainability

Every score shall include:

- contributing rules;
- contributing analyzers;
- calculation evidence;
- weighting details;
- normalization path;
- StrengthResult references when used as evidence.

No score may exist without traceability.

---

# 11. Versioning

The scoring model is version-controlled.

Any modification to:

- dimensions;
- weighting strategy;
- normalization method;
- classification thresholds;
- adjustment derivation logic;

requires a new scoring model version.

---

# 12. Constraints

The scoring model shall never:

- modify Rule Database contents;
- infer undocumented weights;
- skip mandatory dimensions;
- generate random scores;
- recompute Day Master strength scores.

---

# 13. Acceptance Criteria

The scoring model is accepted when:

- identical inputs always produce identical normalized scores;
- all score contributions are traceable;
- confidence is reproducible;
- classification is deterministic;
- adjustment indicators are deterministic.
