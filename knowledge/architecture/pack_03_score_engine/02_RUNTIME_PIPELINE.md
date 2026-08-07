# 02_RUNTIME_PIPELINE.md

Version: 1.0

Status: CANONICAL

Pack: 03

Engine: Score Engine

---

# 1. Purpose

This document defines the canonical runtime pipeline of the Score Engine.

The Score Engine transforms a canonical BaziChart into a complete AnalysisResult through a deterministic inference pipeline.

The pipeline performs analytical reasoning only.

It never modifies the BaziChart.

---

# 2. Runtime Philosophy

The Score Engine is an inference engine.

It does not calculate calendar data.

It does not build BaZi structures.

It does not generate interpretation text.

Its responsibility is to evaluate structural facts using canonical analytical rules.

Every execution must be deterministic, explainable and reproducible.

---

# 3. Canonical Runtime Pipeline

BaziChart

↓

Analysis Context Builder

↓

Rule Loader

↓

Rule Matcher

↓

Evidence Collector

↓

Conflict Resolver

↓

Priority Engine

↓

Score Calculator

↓

Confidence Calculator

↓

Analysis Builder

↓

Analysis Validation

↓

Result<AnalysisResult>

---

# 4. Runtime Overview

| Stage | Input | Output | Responsibility |
|--------|-------|--------|----------------|
| 01 | BaziChart | AnalysisContext | Prepare runtime context |
| 02 | AnalysisContext | RuleSet | Load canonical rules |
| 03 | RuleSet | MatchedRules | Match analytical rules |
| 04 | MatchedRules | EvidenceCollection | Collect reasoning evidence |
| 05 | EvidenceCollection | ResolvedEvidence | Resolve conflicts |
| 06 | ResolvedEvidence | PrioritizedEvidence | Priority resolution |
| 07 | PrioritizedEvidence | Scores | Calculate analytical scores |
| 08 | Scores | ConfidenceSummary | Calculate confidence |
| 09 | All Analysis | AnalysisResult | Build Aggregate |
| 10 | AnalysisResult | Result<AnalysisResult> | Final validation |

---

# 5. Stage 01 — Analysis Context Builder

Input

BaziChart

Responsibilities

Prepare runtime context.

Collect

- Four Pillars
- Hidden Stems
- Relationships
- Five Elements
- Na Yin
- Growth Phases

No rules loaded.

No scoring.

Output

AnalysisContext

---

# 6. Stage 02 — Rule Loader

Consumes

AnalysisContext

Responsibilities

Load

- Strength Rules
- Pattern Rules
- Useful God Rules
- Ten God Rules
- Five Element Rules
- Shen Sha Rules
- Luck Rules

Rules are loaded from the canonical Rule Database.

No rule evaluation occurs here.

Output

RuleSet

---

# 7. Stage 03 — Rule Matcher

Consumes

RuleSet

Responsibilities

Evaluate every rule against the AnalysisContext.

Each rule returns

Matched

Not Matched

Skipped

No conclusions are generated.

Output

MatchedRules

---

# 8. Stage 04 — Evidence Collector

Consumes

MatchedRules

Responsibilities

Collect every successful match.

Each evidence contains

- Rule ID
- Evidence Type
- Weight
- Supporting Facts
- Source Objects

Evidence is immutable.

Output

EvidenceCollection

---

# 9. Stage 05 — Conflict Resolver

Consumes

EvidenceCollection

Responsibilities

Detect conflicting evidence.

Examples

- Strong vs Weak
- Pattern A vs Pattern B
- Multiple Useful Gods

Resolve structural conflicts.

No scoring.

Output

ResolvedEvidence

---

# 10. Stage 06 — Priority Engine

Consumes

ResolvedEvidence

Responsibilities

Apply canonical priority rules.

Determine

- Winning Rule
- Secondary Rules
- Ignored Rules

Every decision is recorded.

Output

PrioritizedEvidence

---

# 11. Stage 07 — Score Calculator

Consumes

PrioritizedEvidence

Responsibilities

Calculate

- Strength Score
- Pattern Score
- Useful God Score
- Ten God Scores
- Five Element Scores
- Shen Sha Scores
- Overall Score

Every score references supporting evidence.

Output

Scores

---

# 12. Stage 08 — Confidence Calculator

Consumes

Scores

Responsibilities

Calculate confidence.

Factors include

- Evidence quantity
- Evidence quality
- Rule consistency
- Rule agreement

Output

ConfidenceSummary

---

# 13. Stage 09 — Analysis Builder

Consumes

All analytical outputs.

Produces

AnalysisResult

AnalysisResult includes

- Metadata
- StrengthAnalysis
- PatternAnalysis
- UsefulGodAnalysis
- TenGodAnalysis
- FiveElementAnalysis
- ShenShaAnalysis
- LuckAnalysis
- OverallAnalysis
- EvidenceCollection
- RuleTrace
- ConfidenceSummary

The Aggregate becomes immutable.

---

# 14. Stage 10 — Analysis Validation

Validate

AnalysisResult

Checks

- Aggregate completeness
- Required analyses
- Evidence integrity
- Rule trace integrity
- Confidence availability
- Metadata completeness

Output

Result<AnalysisResult>

---

# 15. Error Flow

BaziChart

↓

Analysis Context

↓

Rule Matching

↓

❌ Error

↓

Result.Error

↓

Pipeline Stops

No partial analysis is returned.

---

# 16. Success Flow

BaziChart

↓

Analysis Context

↓

Rules

↓

Evidence

↓

Priority

↓

Scores

↓

Confidence

↓

AnalysisResult

↓

Validation

↓

Result.Success

---

# 17. Runtime Characteristics

The Score Engine must be

- Deterministic
- Stateless
- Immutable
- Explainable
- Thread-safe
- Traceable

Identical BaziChart inputs must always produce identical AnalysisResult outputs.

---

# 18. Logging

Each runtime stage records

- Stage Name
- Start Time
- End Time
- Duration
- Rule Count
- Matched Rule Count
- Warning Count
- Error Count

No personal data may be logged.

---

# 19. Performance Targets

Single Analysis

<150 ms

100 Analyses

<2 seconds

1000 Analyses

<15 seconds

No network dependency.

---

# 20. Downstream Contract

Only AnalysisResult may leave the Score Engine.

Interpretation Engine consumes

AnalysisResult

Report Engine consumes

AnalysisResult

No downstream Engine executes rules again.

---

# 21. Runtime Diagram

BaziChart

↓

Analysis Context

↓

Rule Loader

↓

Rule Matcher

↓

Evidence Collector

↓

Conflict Resolver

↓

Priority Engine

↓

Score Calculator

↓

Confidence Calculator

↓

Analysis Builder

↓

Analysis Validation

↓

AnalysisResult

↓

Interpretation Engine

---

# 22. Acceptance Criteria

The runtime pipeline is complete when

✓ Every inference stage has one responsibility

✓ Rule loading completed

✓ Evidence collected

✓ Conflicts resolved

✓ Priorities applied

✓ Scores calculated

✓ Confidence calculated

✓ AnalysisResult validated

✓ Runtime deterministic

✓ Thread-safe

✓ Unit Tests pass

✓ Integration Tests pass

✓ Golden Dataset verified

---

END OF DOCUMENT