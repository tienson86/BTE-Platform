# Strength Engine Algorithm

**Module:** `engines/analysis_engine/01_strength_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Algorithm Specification)

---

# 1. Purpose

This document specifies the analytical algorithm executed by the Strength Engine.

The algorithm is deterministic and rule-driven.

---

# 2. Algorithm Objectives

The algorithm shall:

- evaluate each analytical dimension independently;
- aggregate all dimensions into a normalized strength score;
- calculate confidence;
- produce a reproducible StrengthResult.

---

# 3. Processing Algorithm

```text
Receive AnalysisContext

↓

Validate Input

↓

Normalize Context

↓

Load Rules

↓

Evaluate Season

↓

Evaluate Root

↓

Evaluate Heavenly Stems

↓

Evaluate Earthly Branches

↓

Evaluate Support

↓

Evaluate Control

↓

Evaluate Drain

↓

Aggregate Scores

↓

Normalize Result

↓

Evaluate Confidence

↓

Build StrengthResult
```

---

# 4. Analytical Dimensions

Each dimension is evaluated independently.

Dimensions include:

- Seasonal Influence
- Root Strength
- Heavenly Stem Influence
- Earthly Branch Influence
- Support
- Control
- Drain

No dimension may directly modify another.

---

# 5. Score Aggregation

The algorithm shall:

1. Collect all dimension scores.
2. Apply configured weights.
3. Normalize the total score.
4. Determine the strength level.

Aggregation order shall remain stable.

---

# 6. Confidence Algorithm

Confidence is determined using:

- Rule coverage
- Data completeness
- Rule consistency
- Analytical agreement

Confidence shall be independent of the strength score.

---

# 7. Tie Resolution

When multiple rule outcomes have equal priority:

1. Apply the official Priority Rules.
2. Preserve deterministic ordering.
3. Record the resolution path.

---

# 8. Explainability

Every output score shall reference:

- contributing analyzers;
- matched rules;
- score contributions;
- supporting evidence.

---

# 9. Complexity Targets

Target characteristics:

- Linear processing with respect to the number of applicable rules.
- Stateless execution.
- Minimal memory allocation.
- Cache-friendly rule access.

---

# 10. Algorithm Constraints

The algorithm shall never:

- infer undocumented rules;
- modify Rule Database contents;
- invoke downstream engines;
- produce non-deterministic results.

---

# 11. Acceptance Criteria

The algorithm is accepted when:

- identical inputs produce identical outputs;
- all analytical dimensions execute successfully;
- confidence is calculated;
- all matched rules are traceable;
- StrengthResult is reproducible.