# 08_SCORING_ENGINE.md

Version: 1.0

Status: CANONICAL

Pack: 03

Engine: Score Engine

Component: Scoring Engine

---

# 1. Purpose

The Scoring Engine transforms prioritized analytical evidence into the canonical AnalysisResult.

It is responsible for calculating normalized analytical scores and constructing every analytical node.

The Scoring Engine never executes rules.

The Scoring Engine never performs interpretation.

The Scoring Engine never modifies BaziChart.

---

# 2. Position in Runtime

AnalysisContext

↓

Rule Engine

↓

Rule Matcher

↓

Evidence Engine

↓

Priority Engine

↓

Scoring Engine

↓

AnalysisResult

↓

Interpretation Engine

---

# 3. Scoring Philosophy

Scoring is not decision making.

All analytical decisions have already been completed by

Rule Engine

Evidence Engine

Priority Engine

The Scoring Engine transforms approved evidence into structured analytical results.

---

# 4. Responsibilities

The Scoring Engine is responsible for

✓ Score normalization

✓ Confidence normalization

✓ Analysis node construction

✓ Overall score calculation

✓ Aggregate construction

✓ Score metadata generation

The Scoring Engine is NOT responsible for

✗ Rule execution

✗ Rule matching

✗ Priority resolution

✗ Interpretation

---

# 5. Runtime Flow

Prioritized Evidence

↓

Score Builder

↓

Analysis Node Builder

↓

Overall Score Builder

↓

Confidence Builder

↓

AnalysisResult Builder

↓

AnalysisResult

---

# 6. Input

Consumes

PrioritizedEvidenceCollection

Each Evidence contains

Rule

Evidence Weight

Decision

Reasoning Chain

Fact Snapshot

Confidence Hint

Metadata

---

# 7. Output

Produces

AnalysisResult

AnalysisResult is immutable.

Every analytical conclusion is traceable.

---

# 8. Analysis Nodes

The Scoring Engine constructs

StrengthAnalysis

PatternAnalysis

UsefulGodAnalysis

TenGodAnalysis

FiveElementAnalysis

ShenShaAnalysis

LuckAnalysis

OverallAnalysis

Every node follows the same canonical structure.

---

# 9. Canonical Analysis Node

Every Analysis Node contains

Value

Score

Confidence

Evidence

Matched Rules

Warnings

Metadata

Every node is immutable.

---

# 10. Score Calculation

Scores are calculated only from

Prioritized Evidence.

Suppressed Evidence

does not contribute.

Deferred Evidence

does not contribute.

Merged Evidence

contributes according to merge policy.

---

# 11. Score Normalization

Scores are normalized

to canonical ranges.

Example

0

↓

100

Normalization rules are versioned.

---

# 12. Confidence Calculation

Confidence combines

Evidence Quality

Evidence Quantity

Rule Agreement

Priority Stability

Conflict Resolution

Confidence range

0.0

↓

1.0

---

# 13. Overall Score

Overall Score is derived from

Strength

Pattern

Useful God

Ten Gods

Five Elements

Shen Sha

Luck

Overall Score is a summary metric.

It never replaces individual analyses.

---

# 14. Analysis Builder

Analysis Builder assembles

AnalysisMetadata

Analysis Nodes

EvidenceCollection

RuleTrace

ConfidenceSummary

OverallAnalysis

The Aggregate becomes immutable.

---

# 15. Metadata

Analysis Metadata contains

Analysis Version

Knowledge Version

Rule Version

Runtime Version

Execution Duration

Builder Trace

Metadata supports auditing.

---

# 16. Validation

Before release

AnalysisResult validates

✓ Required Nodes

✓ Score Ranges

✓ Confidence Ranges

✓ Metadata

✓ Evidence References

✓ Rule References

Invalid AnalysisResult

returns

Result.Error

---

# 17. Error Handling

Possible errors

ScoreCalculationError

NormalizationError

AggregateError

MetadataError

ValidationError

InternalError

Errors terminate execution.

No partial AnalysisResult is returned.

---

# 18. Performance

Target

10,000 Evidence

↓

AnalysisResult

<50 ms

Supports parallel aggregation.

---

# 19. Thread Safety

The Scoring Engine is

✓ Stateless

✓ Immutable

✓ Deterministic

✓ Thread-safe

Parallel execution supported.

---

# 20. Downstream Contract

Produces

AnalysisResult

Consumed by

Interpretation Engine

Report Engine

AI Advisory Engine

No downstream component

recalculates scores.

---

# 21. Acceptance Criteria

The Scoring Engine is complete when

✓ Analysis Nodes created

✓ Scores normalized

✓ Confidence calculated

✓ Overall Score calculated

✓ Aggregate validated

✓ Metadata preserved

✓ Thread-safe

✓ Deterministic

✓ Performance targets achieved

✓ Documentation approved

---

END OF DOCUMENT