# ShenSha Engine Execution Flow

**Module:** `engines/analysis_engine/07_shensha_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Execution Flow Specification)

---

# 1. Purpose

This document defines the end-to-end execution flow of the ShenSha Engine.

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
Access ShenSha Knowledge (Knowledge SDK)
        │
        ▼
Resolve Calculation References
        │
        ▼
Evaluate Lookup / Mapping Tables
        │
        ▼
Detect Auspicious ShenSha
        │
        ▼
Detect Inauspicious ShenSha
        │
        ▼
Evaluate Interaction Rules
        │
        ▼
Evaluate Compatibility
        │
        ▼
Apply Exceptions
        │
        ▼
Resolve Priority / Conflicts
        │
        ▼
Calculate Confidence
        │
        ▼
Build Immutable ShenShaResult
        │
        ▼
Publish ShenShaResult
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

Missing required upstream results fail closed.

## Stage 4 — Access Knowledge

Obtain declarative ShenSha Knowledge views through Knowledge SDK under the request-frozen KnowledgeSession.

## Stage 5 — Calculation Reference Resolution

Derive lookup keys from chart anchors per calculation reference knowledge.

## Stage 6 — Lookup / Mapping Evaluation

Apply lookup and mapping tables to determine ShenSha presence and polarity.

## Stage 7 — Auspicious / Inauspicious Classification

Assign ShenSha identities to auspicious or inauspicious polarity classes.

## Stage 8 — Interaction Evaluation

Apply interaction rules for co-present ShenSha identities.

## Stage 9 — Compatibility Evaluation

Apply compatibility classes among ShenSha and declared chart-structure classes.

## Stage 10 — Exception Application

Apply exception overrides, suppressions, or qualifications.

## Stage 11 — Priority / Conflict Resolution

Resolve competing outcomes deterministically.

## Stage 12 — Confidence Calculation

Compute confidence from evidence contributions.

## Stage 13 — Build and Publish Result

Construct immutable `ShenShaResult` and return to orchestrator.

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
ShenShaResult (immutable)
```

---

# 6. Failure Points

Any stage may fail closed with classified errors.

Partial success must not be published as complete ShenShaResult.

---

# 7. Acceptance Criteria

Execution flow is accepted when order, stage responsibilities, upstream reads, SDK access, and publish semantics are complete.
