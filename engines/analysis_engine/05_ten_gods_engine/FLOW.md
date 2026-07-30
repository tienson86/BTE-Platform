# Ten Gods Engine Execution Flow

**Module:** `engines/analysis_engine/05_ten_gods_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Execution Flow Specification)

---

# 1. Purpose

This document defines the end-to-end execution flow of the Ten Gods Engine.

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
Read StrengthResult
        │
        ▼
Read TemperatureResult
        │
        ▼
Read PatternResult
        │
        ▼
Read UsefulGodResult
        │
        ▼
Access Ten Gods Knowledge (Knowledge SDK)
        │
        ▼
Analyse Ten Gods Presence / Identities
        │
        ▼
Evaluate Relationship Models
        │
        ▼
Evaluate Strength Interaction
        │
        ▼
Evaluate Temperature Interaction
        │
        ▼
Evaluate Pattern Interaction
        │
        ▼
Evaluate Useful God Interaction
        │
        ▼
Evaluate Favorability
        │
        ▼
Evaluate Life-Area Concepts
        │
        ▼
Resolve Priority / Conflicts
        │
        ▼
Calculate Confidence
        │
        ▼
Build Immutable TenGodsResult
        │
        ▼
Publish TenGodsResult
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

Missing required upstream results fail closed.

## Stage 4 — Access Knowledge

Obtain declarative Ten Gods Knowledge views through Knowledge SDK under the request-frozen KnowledgeSession.

## Stage 5 — Presence / Identity Analysis

Determine Ten Gods identities and presence structure from chart facts and knowledge.

## Stage 6 — Relationship Evaluation

Apply relationship models among co-present Ten Gods.

## Stage 7 — Interaction Evaluation

Apply strength, temperature, pattern, and useful-god interaction knowledge to Ten Gods quality/favorability frames.

## Stage 8 — Favorability Evaluation

Assign favorability classes under declared conditions.

## Stage 9 — Life-Area Concept Evaluation

Attach personality, career, wealth, marriage, and health analytical concept tags where knowledge applies.

## Stage 10 — Priority / Conflict Resolution

Resolve competing outcomes deterministically.

## Stage 11 — Confidence Calculation

Compute confidence from evidence contributions.

## Stage 12 — Build and Publish Result

Construct immutable `TenGodsResult` and return to orchestrator for context publication.

---

# 5. Data Movement

```text
AnalysisContext
   + upstream StageResults
   + SDK Knowledge views
        │
        ▼
Internal analytical intermediates (request-scoped)
        │
        ▼
TenGodsResult (immutable)
```

Internal intermediates are not public API.

---

# 6. Failure Points

Any stage may fail closed with classified errors (validation, knowledge, prerequisite, execution).

Partial success must not be published as complete TenGodsResult.

---

# 7. Acceptance Criteria

Execution flow is accepted when order, stage responsibilities, upstream reads, SDK access, and publish semantics are complete.
