# Analysis Runtime Pipeline

**Component:** Analysis Runtime  
**Version:** V1.0.0  
**Status:** Frozen Runtime Baseline

---

# 1. Purpose

This document defines the canonical runtime pipeline for analysis execution.

---

# 2. Pipeline Overview

```text
Receive Analysis Request
        │
        ▼
Validate Input Context
        │
        ▼
Bind Knowledge Session (SDK)
        │
        ▼
Initialize Runtime Context
        │
        ▼
01 Strength Module
        │
        ▼
02 Temperature Module
        │
        ▼
03 Pattern Module
        │
        ▼
04 Useful God Module
        │
        ▼
05 Ten Gods Module
        │
        ▼
06 Combination Module
        │
        ▼
07 ShenSha Module
        │
        ▼
08 Luck Module
        │
        ▼
09 Summary Module
        │
        ▼
Final Validation
        │
        ▼
Assemble AnalysisResult
        │
        ▼
Publish to Downstream (Interpretation Engine)
```

Each Analysis Module executes exactly once per request in this order.

---

# 3. Pipeline Phases

## Phase A — Admission

- accept upstream Calendar/BaZi-derived AnalysisContext
- validate required input fields
- reject invalid requests fail-closed

## Phase B — Knowledge Bind

- ResolveVersion / ResolveDependency via Knowledge SDK as required
- Validate knowledge compatibility
- freeze KnowledgeSession for the request

## Phase C — Stage Execution

- execute modules 01–09 sequentially
- after each stage: validate StageResult and append to context
- on failure: enter Error Recovery policy

## Phase D — Finalization

- final cross-stage validation
- assemble AnalysisResult + ExecutionMetadata
- emit explainability references
- release or retain runtime caches per policy

---

# 4. Execution Order Rules

- Order is canonical and mandatory for V1.0
- Skipping stages is forbidden unless a governed profile explicitly marks a stage optional (default: all required)
- Reordering is a breaking runtime change

---

# 5. Module Dependencies (Runtime Data)

| Module | Reads from Context |
|--------|--------------------|
| Strength | Base chart facts + knowledge |
| Temperature | Base chart + StrengthResult (as required by module contract) |
| Pattern | Base chart + Strength/Temperature results as required |
| Useful God | Strength/Temperature/Pattern results as required |
| Ten Gods | Upstream analytical results as required |
| Combination | Chart structure + upstream results as required |
| ShenSha | Chart anchors + upstream results as required |
| Luck | Natal analytical results as required |
| Summary | All prior StageResults |

Knowledge dependencies are resolved through SDK; data dependencies use shared context.

---

# 6. Downstream Handoff

Interpretation Engine consumes immutable AnalysisResult only.

It does not resume Analysis Runtime internals.

---

# 7. Acceptance Criteria

Runtime Pipeline is accepted when phases, order, module data dependencies, and handoff rules are complete.
