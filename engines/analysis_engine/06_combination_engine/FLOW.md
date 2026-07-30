# Combination Engine Execution Flow

**Module:** `engines/analysis_engine/06_combination_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Execution Flow Specification)

---

# 1. Purpose

This document defines the end-to-end execution flow of the Combination Engine.

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
Read TenGodsResult
        │
        ▼
Access Combination Knowledge (Knowledge SDK)
        │
        ▼
Evaluate Heavenly Stem Combinations
        │
        ▼
Evaluate Earthly Branch Combinations
        │
        ▼
Evaluate Clash
        │
        ▼
Evaluate Harm
        │
        ▼
Evaluate Punishment
        │
        ▼
Evaluate Destruction
        │
        ▼
Evaluate Hidden Combination
        │
        ▼
Evaluate Transformation
        │
        ▼
Resolve Priority / Conflicts
        │
        ▼
Calculate Confidence
        │
        ▼
Build Immutable CombinationResult
        │
        ▼
Publish CombinationResult
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

Missing required upstream results fail closed.

## Stage 4 — Access Knowledge

Obtain declarative Combination Knowledge views through Knowledge SDK under the request-frozen KnowledgeSession.

## Stage 5 — Stem / Branch Combination Evaluation

Evaluate Heavenly Stem and Earthly Branch combination classes.

## Stage 6 — Disruptive Relation Evaluation

Evaluate Clash, Harm, Punishment, and Destruction.

## Stage 7 — Hidden Combination Evaluation

Evaluate concealed stem combination outcomes.

## Stage 8 — Transformation Evaluation

Evaluate transformation success/failure and resulting elemental class per knowledge.

## Stage 9 — Priority / Conflict Resolution

Resolve competing outcomes deterministically.

## Stage 10 — Confidence Calculation

Compute confidence from evidence contributions.

## Stage 11 — Build and Publish Result

Construct immutable `CombinationResult` and return to orchestrator.

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
CombinationResult (immutable)
```

---

# 6. Failure Points

Any stage may fail closed with classified errors.

Partial success must not be published as complete CombinationResult.

---

# 7. Acceptance Criteria

Execution flow is accepted when order, stage responsibilities, upstream reads, SDK access, and publish semantics are complete.
