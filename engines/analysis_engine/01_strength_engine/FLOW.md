# Strength Engine Execution Flow

**Module:** `engines/analysis_engine/01_strength_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Execution Flow Specification)

---

# 1. Purpose

This document defines the end-to-end execution flow of the Strength Engine.

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
AnalysisContext
        │
        ▼
Context Validation
        │
        ▼
Strength Context Builder
        │
        ▼
Rule Discovery
        │
        ▼
Rule Loading
        │
        ▼
Season Analysis
        │
        ▼
Root Analysis
        │
        ▼
Heavenly Stem Analysis
        │
        ▼
Earthly Branch Analysis
        │
        ▼
Support Analysis
        │
        ▼
Control Analysis
        │
        ▼
Drain Analysis
        │
        ▼
Score Aggregation
        │
        ▼
Confidence Evaluation
        │
        ▼
Strength Result Builder
        │
        ▼
StrengthResult
```

---

# 4. Stage Definitions

## Stage 1 — Context Validation

Objective:

Validate AnalysisContext integrity.

Output:

Validated AnalysisContext.

Failure:

Terminate immediately.

---

## Stage 2 — Strength Context Builder

Objective:

Normalize reusable analytical data.

Output:

StrengthContext.

---

## Stage 3 — Rule Discovery

Objective:

Identify applicable Strength Rules.

Output:

Rule identifiers.

---

## Stage 4 — Rule Loading

Objective:

Load rule definitions from the Rule Registry.

Output:

Executable rule set.

---

## Stage 5 — Season Analysis

Objective:

Evaluate seasonal influence on the Day Master.

---

## Stage 6 — Root Analysis

Objective:

Evaluate rooting through hidden stems.

---

## Stage 7 — Heavenly Stem Analysis

Objective:

Evaluate Heavenly Stem contributions.

---

## Stage 8 — Earthly Branch Analysis

Objective:

Evaluate Earthly Branch contributions.

---

## Stage 9 — Support Analysis

Objective:

Evaluate producing and assisting elements.

---

## Stage 10 — Control Analysis

Objective:

Evaluate restricting influences.

---

## Stage 11 — Drain Analysis

Objective:

Evaluate energy leakage.

---

## Stage 12 — Score Aggregation

Objective:

Aggregate all analytical dimensions into a normalized strength score.

---

## Stage 13 — Confidence Evaluation

Objective:

Evaluate analytical confidence.

---

## Stage 14 — Result Builder

Objective:

Construct immutable StrengthResult.

---

# 5. State Transitions

```text
Received
↓

Validated
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
- StrengthResult is immutable.
- All matched rules are recorded.
- Confidence has been calculated.
- Execution metadata has been attached.