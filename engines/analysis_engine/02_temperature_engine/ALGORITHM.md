# Temperature Engine Algorithm

**Module:** `engines/analysis_engine/02_temperature_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Algorithm Specification)

---

# 1. Purpose

This document specifies the analytical algorithm executed by the Temperature Engine.

The algorithm is deterministic and rule-driven.

---

# 2. Algorithm Objectives

The algorithm shall:

- evaluate each climatic analytical dimension independently;
- aggregate all dimensions into a normalized climate score;
- determine climate adjustment requirements;
- calculate confidence;
- produce a reproducible TemperatureResult.

---

# 3. Processing Algorithm

```text
Receive AnalysisContext and StrengthResult

↓

Validate Input

↓

Normalize Context

↓

Load Rules

↓

Evaluate Season Temperature

↓

Evaluate Warm / Cold Balance

↓

Evaluate Dryness

↓

Evaluate Humidity

↓

Evaluate Equilibrium

↓

Evaluate Environmental Support

↓

Evaluate Adjustment Requirements

↓

Aggregate Scores

↓

Normalize Result

↓

Evaluate Confidence

↓

Build TemperatureResult
```

---

# 4. Analytical Dimensions

Each dimension is evaluated independently.

Dimensions include:

- Seasonal Temperature
- Warm / Cold Balance
- Dryness
- Humidity
- Climate Equilibrium
- Environmental Support
- Climate Adjustment Requirements

No dimension may directly modify another.

---

# 5. Score Aggregation

The algorithm shall:

1. Collect all dimension scores.
2. Apply configured weights.
3. Normalize the total score.
4. Determine the temperature level.
5. Derive adjustment indicators from matched Adjustment Rules.

Aggregation order shall remain stable.

---

# 6. Confidence Algorithm

Confidence is determined using:

- Rule coverage
- Data completeness
- Rule consistency
- Analytical agreement
- StrengthResult completeness where required by Temperature Rules

Confidence shall be independent of the climate score.

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
- supporting evidence;
- StrengthResult evidence when consumed.

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
- recompute Day Master strength;
- invoke downstream engines;
- produce non-deterministic results.

---

# 11. Acceptance Criteria

The algorithm is accepted when:

- identical inputs produce identical outputs;
- all analytical dimensions execute successfully;
- confidence is calculated;
- all matched rules are traceable;
- TemperatureResult is reproducible.
