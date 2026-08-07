# PACK_03_SCORE_ENGINE_ARCHITECTURE

Version: 1.0

Status: CANONICAL

Pack: 03

Engine: Score Engine (Analysis Engine Core)

---

# 1. Purpose

The Score Engine is the analytical core of the BTE Platform.

Its responsibility is to transform a canonical BaziChart into a complete, explainable AnalysisResult.

Unlike the Calendar Engine and BaZi Engine, the Score Engine does not create structural facts.

Instead, it evaluates those facts using the canonical Rule Database.

The Score Engine produces analytical conclusions that are transparent, traceable and reproducible.

---

# 2. Position in the Architecture

Runtime Pipeline

BirthRequest

↓

Calendar Engine

↓

BirthContext

↓

BaZi Engine

↓

BaziChart

↓

Score Engine

↓

AnalysisResult

↓

Interpretation Engine

↓

InterpretationResult

↓

Report Engine

↓

ReportResult

The Score Engine always consumes BaziChart.

The Score Engine always produces AnalysisResult.

---

# 3. Responsibilities

The Score Engine is responsible for

✓ Rule Loading

✓ Rule Matching

✓ Evidence Collection

✓ Conflict Resolution

✓ Priority Resolution

✓ Score Calculation

✓ Confidence Evaluation

✓ Analysis Construction

✓ Canonical AnalysisResult generation

The Score Engine is NOT responsible for

✗ Calendar calculation

✗ Four Pillar construction

✗ Relationship construction

✗ Natural language generation

✗ Report rendering

---

# 4. Domain Philosophy

The Score Engine produces explainable analytical conclusions.

Every conclusion must be supported by:

- Matched Rules
- Evidence
- Confidence
- Priority Resolution

No conclusion may exist without traceable evidence.

---

# 5. Canonical Runtime

BaziChart

↓

Rule Loader

↓

Rule Matcher

↓

Evidence Engine

↓

Conflict Resolver

↓

Priority Engine

↓

Score Calculator

↓

Analysis Builder

↓

AnalysisResult

Every stage has exactly one responsibility.

---

# 6. Canonical Aggregate

The Score Engine produces one Aggregate Root.

AnalysisResult

The Aggregate contains

AnalysisMetadata

StrengthAnalysis

PatternAnalysis

UsefulGodAnalysis

TenGodAnalysis

FiveElementAnalysis

ShenShaAnalysis

LuckAnalysis

OverallScore

EvidenceCollection

RuleTrace

ConfidenceSummary

---

# 7. Engine Components

The Score Engine consists of independent components.

RuleLoader

RuleMatcher

EvidenceEngine

ConflictResolver

PriorityEngine

ScoreCalculator

AnalysisBuilder

ValidationEngine

Each component has a single responsibility.

---

# 8. Runtime Characteristics

The Engine must be

- Deterministic
- Stateless
- Immutable
- Thread-safe
- Explainable

The same BaziChart always produces the same AnalysisResult.

---

# 9. Public Contract

Input

BaziChart

Output

Result<AnalysisResult>

No additional public outputs are allowed.

AnalysisResult is immutable.

---

# 10. Knowledge Dependency

The Score Engine depends on

Canonical Rule Database

The Score Engine never accesses raw knowledge files directly.

Knowledge must be loaded through the RuleLoader.

---

# 11. Rule Processing Model

Every rule follows the same lifecycle.

Load

↓

Match

↓

Evidence

↓

Priority

↓

Score

↓

Analysis

Rules never generate text.

Rules never render UI.

---

# 12. Evidence Philosophy

Every analytical conclusion must include evidence.

Example

Strength

↓

Weak

↓

Evidence

- Month Branch controls Day Master
- Root support insufficient
- Seasonal support absent

Evidence becomes part of the AnalysisResult.

---

# 13. Conflict Resolution

When multiple rules produce conflicting conclusions,

the Conflict Resolver normalizes them before scoring.

No downstream Engine resolves rule conflicts.

---

# 14. Confidence Model

Every analytical conclusion has

- Score
- Confidence
- Evidence Count
- Matched Rule Count

Confidence is calculated structurally.

Interpretation does not modify confidence.

---

# 15. Error Handling

Every execution returns

Result<AnalysisResult>

Possible outcomes

Success

↓

AnalysisResult

Failure

↓

Structured Error

Partial analysis is never returned.

---

# 16. Performance Targets

Single Chart

<150 ms

100 Charts

<2 seconds

1000 Charts

<15 seconds

No external network dependency.

---

# 17. Documentation Structure

The Score Engine documentation consists of

PACK_03_SCORE_ENGINE_ARCHITECTURE.md

01_DATA_MODEL.md

02_RUNTIME_PIPELINE.md

03_PUBLIC_API.md

04_RULE_ENGINE.md

05_RULE_MATCHER.md

06_EVIDENCE_ENGINE.md

07_PRIORITY_ENGINE.md

08_SCORING_ENGINE.md

09_VALIDATION_RULES.md

10_TEST_STRATEGY.md

11_ACCEPTANCE_CHECKLIST.md

---

# 18. Long-Term Vision

The Score Engine is designed as the canonical analytical engine of the BTE Platform.

Future analytical modules such as

- Advanced Strength Engine
- Dynamic Pattern Engine
- AI Rule Engine
- Multi-school Analysis
- School-specific Rule Packs

must integrate through the same architecture without changing the public contract.

The Score Engine is the single source of truth for analytical results.

---

# 19. Acceptance Criteria

The Score Engine architecture is complete when

✓ Runtime pipeline defined

✓ Rule lifecycle defined

✓ Evidence model defined

✓ Conflict resolution defined

✓ Aggregate Root defined

✓ Public API defined

✓ Knowledge dependency defined

✓ Documentation approved

---

# 20. Source of Truth

The AnalysisResult Aggregate is the only analytical representation within the BTE Platform.

Every downstream Engine consumes AnalysisResult.

No downstream Engine recalculates rules, priorities or scores.

The Score Engine is the single source of truth for all analytical conclusions.

---

END OF DOCUMENT