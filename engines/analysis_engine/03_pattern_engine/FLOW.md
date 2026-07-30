# Pattern Engine Execution Flow

**Module:** `engines/analysis_engine/03_pattern_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Execution Flow Specification)

---

# 1. Purpose

This document defines the end-to-end execution flow of the Pattern Engine.

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
Load Pattern Rules
        │
        ▼
Analyse Structure
        │
        ▼
Generate Pattern Candidates
        │
        ▼
Evaluate Candidates
        │
        ▼
Resolve Priority
        │
        ▼
Calculate Confidence
        │
        ▼
Build Immutable PatternResult
        │
        ▼
Publish PatternResult
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

Output:

Validated StrengthResult evidence for pattern analysis.

Failure:

Terminate immediately if missing or invalid.

---

## Stage 4 — Read TemperatureResult

Objective:

Read published TemperatureResult from AnalysisContext.temperature_result.

Output:

Validated TemperatureResult evidence for pattern analysis.

Failure:

Terminate immediately if missing or invalid.

---

## Stage 5 — Load Pattern Rules

Objective:

Discover and load applicable Pattern Rules from the Rule Registry.

Output:

Executable Pattern Rule set.

---

## Stage 6 — Analyse Structure

Objective:

Analyse chart structure and Day Master relationship with chart composition for pattern eligibility.

Output:

Structure and relation analysis evidence.

---

## Stage 7 — Generate Pattern Candidates

Objective:

Generate competing pattern candidates across supported categories:

- Standard Patterns
- Special Patterns
- Follow Patterns
- Transformation Patterns
- Mixed Patterns
- Exceptional Patterns

Output:

PatternCandidateSet.

---

## Stage 8 — Evaluate Candidates

Objective:

Evaluate each candidate against Pattern Rules and upstream evidence.

Output:

CandidateEvaluation set.

---

## Stage 9 — Resolve Priority

Objective:

Resolve conflicts and priority contests among competing candidates.

Output:

Selected pattern identity and rejected candidates.

---

## Stage 10 — Calculate Confidence

Objective:

Evaluate analytical confidence.

---

## Stage 11 — Build Immutable PatternResult

Objective:

Construct immutable PatternResult containing identified pattern, category, confidence, matched rules, rejected candidates, reasoning, diagnostics, and metadata.

---

## Stage 12 — Publish PatternResult

Objective:

Return PatternResult to the Analysis Engine orchestrator for inclusion in AnalysisResult.

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

Structure Analysed
↓

Candidates Generated
↓

Candidates Evaluated
↓

Priority Resolved
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
- PatternResult is immutable.
- Identified pattern and pattern category are present.
- All matched rules are recorded.
- Rejected candidates are recorded.
- Confidence has been calculated.
- Reasoning, diagnostics, and metadata have been attached.
- PatternResult has been published to the orchestrator.
