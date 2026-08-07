# 09_VALIDATION_RULES.md

Version: 1.0

Status: CANONICAL

Pack: 03

Engine: Score Engine

---

# 1. Purpose

This document defines the canonical validation rules for the Score Engine.

Validation ensures that every AnalysisResult produced by the Score Engine is:

- Structurally complete
- Academically consistent
- Explainable
- Traceable
- Suitable for downstream interpretation

Validation is the final quality gate before AnalysisResult leaves the Score Engine.

---

# 2. Validation Philosophy

The Score Engine validates analytical integrity.

It does not validate calendar calculations.

It does not validate BaZi construction.

Those responsibilities belong to upstream Engines.

The Score Engine validates only analytical correctness.

---

# 3. Validation Pipeline

AnalysisContext

↓

Rule Validation

↓

Evidence Validation

↓

Priority Validation

↓

Score Validation

↓

Confidence Validation

↓

Analysis Validation

↓

Reasoning Validation

↓

Aggregate Validation

↓

Result<AnalysisResult>

Every validation stage is mandatory.

---

# 4. Validation Categories

The Score Engine performs the following validation groups.

| Category | Responsibility |
|----------|----------------|
| Rule | Rule execution correctness |
| Evidence | Evidence integrity |
| Priority | Conflict resolution correctness |
| Score | Score correctness |
| Confidence | Confidence correctness |
| Analysis | Analysis node correctness |
| Reasoning | Explainability |
| Aggregate | Aggregate completeness |

---

# 5. Rule Validation

Validate

✓ Rule exists

✓ Rule version

✓ Rule category

✓ Rule metadata

✓ Rule execution state

✓ Rule trace

Invalid rules terminate execution.

---

# 6. Evidence Validation

Validate every Evidence.

Checks

✓ Evidence ID

✓ Rule reference

✓ Fact Snapshot

✓ Evidence Weight

✓ Metadata

✓ Reasoning Node

✓ Graph consistency

No orphan evidence is allowed.

---

# 7. Priority Validation

Validate

✓ Resolution strategy

✓ Winning rule

✓ Suppressed rules

✓ Deferred rules

✓ Merge strategy

Every priority decision must be traceable.

---

# 8. Score Validation

Validate every Analysis Node.

Checks

✓ Score exists

✓ Score range valid

✓ Score source exists

✓ Evidence attached

✓ Rule references valid

No score may exist without evidence.

---

# 9. Confidence Validation

Validate

✓ Confidence exists

✓ Range between 0.0 and 1.0

✓ Evidence count

✓ Rule agreement

✓ Confidence metadata

Confidence must always be reproducible.

---

# 10. Analysis Validation

Validate

StrengthAnalysis

PatternAnalysis

UsefulGodAnalysis

TenGodAnalysis

FiveElementAnalysis

ShenShaAnalysis

LuckAnalysis

OverallAnalysis

Every Analysis Node must

- exist
- be immutable
- reference evidence
- reference rules

---

# 11. Reasoning Validation

Validate

Reasoning Chain

Checks

✓ Every conclusion has evidence

✓ Every evidence has source rules

✓ Every rule has fact snapshot

✓ Every chain is complete

✓ No broken links

Every analytical conclusion must be explainable.

---

# 12. Aggregate Validation

Validate AnalysisResult.

Checks

✓ Metadata

✓ Analysis Nodes

✓ Evidence Collection

✓ Rule Trace

✓ Confidence Summary

✓ Overall Analysis

No missing Aggregate Members.

---

# 13. Cross-Analysis Consistency

Verify consistency between analyses.

Examples

Strength

↓

Useful God

↓

Pattern

↓

Overall Analysis

Conflicting analytical values must be resolved before release.

---

# 14. Graph Validation

Validate

Evidence Graph

Rule Graph

Reasoning Graph

Checks

✓ No cycles

✓ Valid references

✓ Reachable nodes

✓ Connected reasoning

All graphs must be valid DAGs.

---

# 15. Metadata Validation

Validate

✓ Engine Version

✓ Rule Version

✓ Knowledge Version

✓ Runtime Version

✓ Builder Trace

✓ Execution Duration

Metadata is mandatory.

---

# 16. Warning Rules

Warnings allow execution to continue.

Examples

Low confidence

Multiple candidate patterns

Incomplete optional metadata

Deprecated rule

Warnings are attached to Result<AnalysisResult>.

---

# 17. Error Model

Possible errors

RuleValidationError

EvidenceValidationError

PriorityValidationError

ScoreValidationError

ConfidenceValidationError

ReasoningValidationError

AggregateValidationError

InternalError

Every error contains

- code
- stage
- component
- message
- timestamp
- trace_id

---

# 18. Validation Result

Validation returns

Result<AnalysisResult>

Possible states

SUCCESS

WARNING

ERROR

ERROR terminates execution.

WARNING allows release.

---

# 19. Logging

Validation logs

Stage

Component

Duration

Warnings

Errors

Trace ID

No sensitive personal data may appear in logs.

---

# 20. Acceptance Checklist

Validation is complete when

✓ Rules validated

✓ Evidence validated

✓ Priority validated

✓ Scores validated

✓ Confidence validated

✓ Analysis validated

✓ Reasoning validated

✓ Aggregate validated

✓ Cross-analysis consistency verified

✓ Metadata validated

✓ Structured Result returned

---

END OF DOCUMENT