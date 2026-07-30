# Analysis Runtime Result Model

**Component:** Analysis Runtime  
**Version:** V1.0.0  
**Status:** Frozen Runtime Baseline

---

# 1. Purpose

This document defines Shared Result contracts produced by Analysis Runtime.

---

# 2. Result Hierarchy

```text
AnalysisResult
 ├── StageResults[]
 │    ├── StrengthResult
 │    ├── TemperatureResult
 │    ├── PatternResult
 │    ├── UsefulGodResult
 │    ├── TenGodsResult
 │    ├── CombinationResult
 │    ├── ShenShaResult
 │    ├── LuckResult
 │    └── SummaryResult
 ├── ExecutionMetadata
 ├── ConfidenceEvaluation (where declared)
 ├── RuleEvidence / KnowledgeReferences
 └── DiagnosticInfo
```

Exact field schemas remain aligned with Analysis Engine Shared Models; this document defines runtime assembly semantics.

---

# 3. StageResult

Each StageResult is:

- immutable after publish into Shared Context
- attributable to one stage module/version
- explainable via evidence references
- self-contained for downstream stage reads

---

# 4. AnalysisResult

AnalysisResult is the only successful runtime publication for downstream consumers.

It aggregates all required StageResults and ExecutionMetadata.

Interpretation Engine consumes AnalysisResult only.

---

# 5. Shared Result Progression

```text
empty stage set
  → append StrengthResult
  → append TemperatureResult
  → …
  → append SummaryResult
  → freeze AnalysisResult
```

No stage may present a provisional value as final without validation.

---

# 6. Explainability Requirements

Successful results shall support:

- KnowledgeReferences for matched knowledge
- RuleEvidence / rationale slots per stage contracts
- stage identity and knowledge version identity used

---

# 7. Failure Results

Failed executions do not publish a successful AnalysisResult.

They publish classified error information and optional partial diagnostics under Error Model rules.

---

# 8. Acceptance Criteria

Result Model is accepted when hierarchy, immutability, explainability, and success/failure publication rules are complete.
