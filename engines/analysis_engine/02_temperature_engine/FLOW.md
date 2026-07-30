# Temperature Engine Execution Flow

**Module:** `engines/analysis_engine/02_temperature_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Execution Flow Specification)

---

# 1. Purpose

This document defines the end-to-end execution flow of the Temperature Engine.

It specifies the sequence of processing stages, execution boundaries, state transitions, and data movement from input reception to result publication.

---

# 2. Execution Principles

The execution flow shall be:

- Deterministic
- Stateless
- Rule-driven
- Immutable
- Explainable
- Fail-fast

Each stage has exactly one responsibility.

---

# 3. High-Level Flow

```text
Receive AnalysisContext
        │
        ▼
Context Validation
        │
        ▼
Read StrengthResult from AnalysisContext
        │
        ▼
Temperature Context Builder
        │
        ▼
Rule Discovery
        │
        ▼
Rule Loading
        │
        ▼
Season Temperature Analysis
        │
        ▼
Warm / Cold Analysis
        │
        ▼
Dryness Analysis
        │
        ▼
Humidity Analysis
        │
        ▼
Equilibrium Analysis
        │
        ▼
Environmental Support Analysis
        │
        ▼
Adjustment Analysis
        │
        ▼
Score Aggregation
        │
        ▼
Confidence Evaluation
        │
        ▼
Temperature Result Builder
        │
        ▼
TemperatureResult
```

---

# 4. Stage Definitions

## Stage 1 — Context Validation

Objective:

Validate AnalysisContext integrity, including required upstream fields.

Output:

Validated AnalysisContext.

Failure:

Terminate immediately.

---

## Stage 2 — Read StrengthResult

Objective:

Read published StrengthResult from AnalysisContext.strength_result.

Output:

Validated StrengthResult evidence for temperature analysis.

Failure:

Terminate immediately if missing or invalid.

---

## Stage 3 — Temperature Context Builder

Objective:

Normalize reusable analytical data and project strength evidence.

Output:

TemperatureContext.

---

## Stage 4 — Rule Discovery

Objective:

Identify applicable Temperature Rules.

Output:

Rule identifiers.

---

## Stage 5 — Rule Loading

Objective:

Load rule definitions from the Rule Registry.

Output:

Executable rule set.

---

## Stage 6 — Season Temperature Analysis

Objective:

Evaluate seasonal temperature influence on the natal chart.

---

## Stage 7 — Warm / Cold Analysis

Objective:

Evaluate warm / cold balance.

---

## Stage 8 — Dryness Analysis

Objective:

Evaluate dryness contribution.

---

## Stage 9 — Humidity Analysis

Objective:

Evaluate humidity contribution.

---

## Stage 10 — Equilibrium Analysis

Objective:

Evaluate climate equilibrium.

---

## Stage 11 — Environmental Support Analysis

Objective:

Evaluate environmental support for climatic balance.

---

## Stage 12 — Adjustment Analysis

Objective:

Evaluate climate adjustment requirements.

---

## Stage 13 — Score Aggregation

Objective:

Aggregate all analytical dimensions into a normalized climate score.

---

## Stage 14 — Confidence Evaluation

Objective:

Evaluate analytical confidence.

---

## Stage 15 — Result Builder

Objective:

Construct immutable TemperatureResult.

---

# 5. State Transitions

```text
Received
↓

Validated
↓

Strength Evidence Loaded
↓

Prepared
↓

Rules Loaded
↓

Analyzing
↓

Scored
↓

Confidence Evaluated
↓

Completed
```

Failure transitions immediately enter the Error state.

---

# 6. Failure Flow

Validation Failure

↓

Stop Execution

Missing StrengthResult

↓

Stop Execution

Rule Failure

↓

Stop Execution

Internal Analyzer Failure

↓

Stop Execution

No partial result shall be published.

---

# 7. Completion Criteria

Execution is complete only when:

- All stages succeed.
- TemperatureResult is immutable.
- All matched rules are recorded.
- Confidence has been calculated.
- Execution metadata has been attached.
