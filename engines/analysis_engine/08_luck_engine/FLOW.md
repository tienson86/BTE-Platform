# Luck Engine Execution Flow

**Module:** `engines/analysis_engine/08_luck_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Execution Flow Specification)

---

# 1. Purpose

This document defines the end-to-end execution flow of the Luck Engine.

---

# 2. Execution Principles

- Deterministic
- Stateless
- Knowledge-driven
- Immutable
- Explainable
- Fail-fast / fail-closed

---

# 3. High-Level Flow

```text
Receive AnalysisContext
        │
        ▼
Validate Context
        │
        ▼
Read Upstream Stage Results
        │
        ▼
Access Luck Knowledge (Knowledge SDK)
        │
        ▼
Evaluate Da Yun
        │
        ▼
Evaluate Liu Nian
        │
        ▼
Evaluate Liu Yue
        │
        ▼
Evaluate Liu Ri
        │
        ▼
Evaluate Liu Shi
        │
        ▼
Evaluate Luck Interaction
        │
        ▼
Apply Timing Principles
        │
        ▼
Apply Activation Rules
        │
        ▼
Evaluate Favorability
        │
        ▼
Resolve Priority / Conflicts
        │
        ▼
Calculate Confidence
        │
        ▼
Build Immutable LuckResult
        │
        ▼
Publish LuckResult
```

---

# 4. Stage Definitions

## Stage 1 — Receive AnalysisContext

Accept shared immutable AnalysisContext from Analysis Runtime.

## Stage 2 — Validate Context

Validate integrity and required upstream fields.

## Stage 3 — Read Upstream Results

Read:

- `AnalysisContext.strength_result`
- `AnalysisContext.temperature_result`
- `AnalysisContext.pattern_result`
- `AnalysisContext.useful_god_result`
- `AnalysisContext.ten_gods_result`
- `AnalysisContext.combination_result`
- `AnalysisContext.shensha_result`

Missing required upstream results fail closed.

## Stage 4 — Access Knowledge

Obtain declarative Luck Knowledge views through Knowledge SDK under the request-frozen KnowledgeSession.

## Stage 5 — Da Yun Evaluation

Evaluate decade-layer sequence and outcomes per knowledge.

## Stage 6 — Liu Nian Evaluation

Evaluate annual-layer outcomes within Da Yun context.

## Stage 7 — Liu Yue Evaluation

Evaluate monthly-layer outcomes within Liu Nian context.

## Stage 8 — Liu Ri Evaluation

Evaluate daily-layer outcomes within Liu Yue context.

## Stage 9 — Liu Shi Evaluation

Evaluate hourly-layer outcomes within Liu Ri context.

## Stage 10 — Luck Interaction Evaluation

Apply luck–natal interaction knowledge using published upstream evidence.

## Stage 11 — Timing / Activation Evaluation

Apply timing principles and activation rules.

## Stage 12 — Favorability Evaluation

Assign favorability classes under declared conditions.

## Stage 13 — Priority / Conflict Resolution

Resolve competing outcomes deterministically.

## Stage 14 — Confidence Calculation

Compute confidence from evidence contributions.

## Stage 15 — Build and Publish Result

Construct immutable `LuckResult` and return to orchestrator.

---

# 5. Layer Hierarchy

```text
Da Yun
  └── Liu Nian
        └── Liu Yue
              └── Liu Ri
                    └── Liu Shi
```

Nested evaluation respects declared hierarchy in knowledge.

---

# 6. Data Movement

```text
AnalysisContext
   + upstream StageResults
   + SDK Knowledge views
        │
        ▼
Internal analytical intermediates (request-scoped)
        │
        ▼
LuckResult (immutable)
```

---

# 7. Failure Points

Any stage may fail closed with classified errors.

Partial success must not be published as complete LuckResult.

---

# 8. Acceptance Criteria

Execution flow is accepted when order, layer hierarchy, upstream reads, SDK access, and publish semantics are complete.
