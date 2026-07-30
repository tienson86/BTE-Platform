# Pattern Engine Algorithm

**Module:** `engines/analysis_engine/03_pattern_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Algorithm Specification)

---

# 1. Purpose

This document specifies the analytical algorithm executed by the Pattern Engine.

The algorithm is deterministic and rule-driven.

---

# 2. Algorithm Objectives

The algorithm shall:

- evaluate each pattern analytical dimension independently;
- identify standard and special pattern candidates;
- resolve competing candidates into one Pattern identity;
- calculate confidence;
- produce a reproducible PatternResult.

---

# 3. Processing Algorithm

```text
Receive AnalysisContext

↓

Validate Input

↓

Read StrengthResult from AnalysisContext

↓

Read TemperatureResult from AnalysisContext

↓

Normalize Context

↓

Load Rules

↓

Evaluate Structure

↓

Evaluate Standard Patterns

↓

Evaluate Special Patterns

↓

Resolve Competing Candidates

↓

Aggregate Scores

↓

Normalize Result

↓

Evaluate Confidence

↓

Build PatternResult
```

---

# 4. Analytical Dimensions

Each dimension is evaluated independently.

Dimensions include:

- Chart Structure
- Standard Patterns
- Special Patterns
- Candidate Resolution

No dimension may directly modify another.

---

# 5. Score Aggregation

The algorithm shall:

1. Collect all dimension scores.
2. Apply configured weights.
3. Normalize the total score.
4. Determine the Pattern identity.
5. Record rejected candidates and resolution evidence.

Aggregation order shall remain stable.

---

# 6. Confidence Algorithm

Confidence is determined using:

- Rule coverage
- Data completeness
- Rule consistency
- Analytical agreement
- Candidate separation quality
- Upstream StrengthResult and TemperatureResult completeness where required by Pattern Rules

Confidence shall be independent of the pattern score where applicable.

---

# 7. Tie Resolution

When multiple rule outcomes or candidates have equal priority:

1. Apply the official Priority Rules.
2. Preserve deterministic ordering.
3. Record the resolution path.

---

# 8. Explainability

Every output decision shall reference:

- contributing analyzers;
- matched rules;
- score contributions;
- supporting evidence;
- upstream StrengthResult and TemperatureResult evidence when consumed.

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
- recompute climate balance;
- invoke downstream engines;
- produce non-deterministic results.

---

# 11. Acceptance Criteria

The algorithm is accepted when:

- identical inputs produce identical outputs;
- all analytical dimensions execute successfully;
- confidence is calculated;
- all matched rules are traceable;
- PatternResult is reproducible.
