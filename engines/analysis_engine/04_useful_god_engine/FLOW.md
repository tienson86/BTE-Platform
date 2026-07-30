# Useful God Engine Execution Flow

**Module:** `engines/analysis_engine/04_useful_god_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Execution Flow Specification)

---

# 1. Purpose

This document defines the end-to-end execution flow of the Useful God Engine.

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
Load Useful God Rules
        │
        ▼
Generate Candidates
        │
        ▼
Evaluate Candidates
        │
        ▼
Resolve Priority
        │
        ▼
Determine Yong Shen
        │
        ▼
Determine Xi Shen
        │
        ▼
Determine Ji Shen
        │
        ▼
Calculate Confidence
        │
        ▼
Build Immutable UsefulGodResult
        │
        ▼
Publish UsefulGodResult
```

---

# 4. Stage Definitions

## Stage 1 — Receive AnalysisContext

Objective:

Accept the shared immutable AnalysisContext from the Analysis Engine orchestrator.

---

## Stage 2 — Validate Context

Objective:

Validate AnalysisContext integrity, including required upstream fields.

Output:

Validated AnalysisContext.

Failure:

Terminate immediately.

---

## Stage 3 — Read StrengthResult

Objective:

Read published StrengthResult from AnalysisContext.strength_result.

Failure:

Terminate immediately if missing or invalid.

---

## Stage 4 — Read TemperatureResult

Objective:

Read published TemperatureResult from AnalysisContext.temperature_result.

Failure:

Terminate immediately if missing or invalid.

---

## Stage 5 — Read PatternResult

Objective:

Read published PatternResult from AnalysisContext.pattern_result.

Failure:

Terminate immediately if missing or invalid.

---

## Stage 6 — Load Useful God Rules

Objective:

Discover and load applicable Useful God Rules from the Rule Registry.

Output:

Executable Useful God Rule set.

---

## Stage 7 — Generate Candidates

Objective:

Generate Useful God candidates, including primary, secondary, and alternative candidates, across supported categories:

- Yong Shen
- Xi Shen
- Ji Shen
- Xian Shen

Output:

UsefulGodCandidateSet.

---

## Stage 8 — Evaluate Candidates

Objective:

Evaluate each candidate against Useful God Rules and upstream evidence.

Output:

CandidateEvaluation set.

---

## Stage 9 — Resolve Priority

Objective:

Resolve conflicts and priority contests among competing candidates.

Output:

Selected candidate rankings and rejected candidates.

---

## Stage 10 — Determine Yong Shen

Objective:

Determine Useful God (Dụng Thần).

---

## Stage 11 — Determine Xi Shen

Objective:

Determine Favorable Gods (Hỷ Thần).

---

## Stage 12 — Determine Ji Shen

Objective:

Determine Unfavorable Gods (Kỵ Thần).

Xian Shen determination is completed as part of final result assembly using resolved candidates and Useful God Rules.

---

## Stage 13 — Calculate Confidence

Objective:

Evaluate analytical confidence.

---

## Stage 14 — Build Immutable UsefulGodResult

Objective:

Construct immutable UsefulGodResult containing useful_god, favorable_gods, unfavorable_gods, neutral_gods, candidate rankings, confidence, matched rules, rejected candidates, reasoning, diagnostics, and metadata.

---

## Stage 15 — Publish UsefulGodResult

Objective:

Return UsefulGodResult to the Analysis Engine orchestrator for inclusion in AnalysisResult.

---

# 5. State Transitions

```text
Received
↓

Validated
↓

Upstream Evidence Loaded
↓

Rules Loaded
↓

Candidates Generated
↓

Candidates Evaluated
↓

Priority Resolved
↓

Yong Shen Determined
↓

Xi Shen Determined
↓

Ji Shen Determined
↓

Confidence Evaluated
↓

Completed
↓

Published
```

Failure transitions immediately enter the Error state.

---

# 6. Failure Flow

Validation Failure

↓

Stop Execution

Missing Upstream Result

↓

Stop Execution

Rule Failure

↓

Stop Execution

Unresolvable Candidate Conflict

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
- UsefulGodResult is immutable.
- useful_god, favorable_gods, unfavorable_gods, and neutral_gods are present.
- Candidate rankings are recorded.
- All matched rules are recorded.
- Rejected candidates are recorded.
- Confidence has been calculated.
- Reasoning, diagnostics, and metadata have been attached.
- UsefulGodResult has been published to the orchestrator.
