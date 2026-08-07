# PACK_04_INTERPRETATION_ENGINE_ARCHITECTURE.md

Version: 1.0

Status: CANONICAL

Pack: 04

Engine: Interpretation Engine

---

# 1. Purpose

The Interpretation Engine transforms a canonical AnalysisResult into a structured InterpretationResult.

Its responsibility is to express analytical conclusions using natural language.

The Interpretation Engine never performs analysis.

The Interpretation Engine never evaluates rules.

The Interpretation Engine never recalculates scores.

---

# 2. Position in Architecture

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

The Interpretation Engine consumes AnalysisResult only.

---

# 3. Responsibilities

The Interpretation Engine is responsible for

✓ Sentence Selection

✓ Template Selection

✓ Placeholder Binding

✓ Paragraph Construction

✓ Section Construction

✓ Explanation Construction

✓ InterpretationResult generation

The Interpretation Engine is NOT responsible for

✗ Calendar calculation

✗ BaZi construction

✗ Rule execution

✗ Score calculation

✗ Priority resolution

✗ Report rendering

---

# 4. Interpretation Philosophy

The Interpretation Engine expresses analytical facts.

It never changes them.

Every sentence must be derived from AnalysisResult.

No sentence may introduce new analytical conclusions.

---

# 5. Runtime Pipeline

AnalysisResult

↓

Sentence Engine

↓

Template Engine

↓

Placeholder Engine

↓

Explanation Engine

↓

Interpretation Builder

↓

Validation

↓

InterpretationResult

Every stage has one responsibility.

---

# 6. Canonical Aggregate

The Interpretation Engine produces one Aggregate Root.

InterpretationResult

The Aggregate contains

InterpretationMetadata

OverviewSection

StrengthSection

PatternSection

UsefulGodSection

TenGodSection

FiveElementSection

ShenShaSection

LuckSection

SummarySection

ParagraphCollection

SentenceCollection

ReferenceCollection

TraceCollection

---

# 7. Engine Components

The Interpretation Engine consists of

Sentence Engine

Template Engine

Placeholder Engine

Explanation Engine

Interpretation Builder

Validation Engine

Each component is independent.

---

# 8. Runtime Characteristics

The Engine must be

- Deterministic

- Stateless

- Immutable

- Thread-safe

- Explainable

Given the same AnalysisResult,

the same InterpretationResult must always be produced.

---

# 9. Public Contract

Input

AnalysisResult

Output

Result<InterpretationResult>

InterpretationResult is immutable.

---

# 10. Knowledge Dependency

The Interpretation Engine depends on

Sentence Library

Template Library

Placeholder Library

Localization Resources

It never loads analytical rules.

It never reads the Rule Database.

---

# 11. Sentence Generation Model

Every interpretation follows

Analysis

↓

Sentence Selection

↓

Template Selection

↓

Placeholder Binding

↓

Explanation

↓

Paragraph

↓

Section

↓

InterpretationResult

---

# 12. Explainability

Every paragraph keeps references to

Analysis Node

Evidence

Rule Trace

Confidence

This supports complete traceability.

---

# 13. Localization

The Interpretation Engine supports

Vietnamese

English

Future languages

Localization affects only presentation.

AnalysisResult remains unchanged.

---

# 14. Error Handling

Every execution returns

Result<InterpretationResult>

Possible outcomes

Success

↓

InterpretationResult

Failure

↓

Structured Error

Partial interpretation is never returned.

---

# 15. Performance Targets

Single Interpretation

<100 ms

100 Interpretations

<1 second

1000 Interpretations

<10 seconds

No external network dependency.

---

# 16. Documentation Structure

The Interpretation Engine documentation consists of

PACK_04_INTERPRETATION_ENGINE_ARCHITECTURE.md

01_DATA_MODEL.md

02_RUNTIME_PIPELINE.md

03_PUBLIC_API.md

04_SENTENCE_ENGINE.md

05_TEMPLATE_ENGINE.md

06_PLACEHOLDER_ENGINE.md

07_EXPLANATION_ENGINE.md

08_VALIDATION_RULES.md

09_TEST_STRATEGY.md

10_ACCEPTANCE_CHECKLIST.md

---

# 17. Long-Term Vision

The Interpretation Engine is the canonical Natural Language Generation layer of the BTE Platform.

Future capabilities such as

- AI Rewrite
- Style Profiles
- Multiple Writing Levels
- School-specific Narratives
- Personalized Reports

must integrate without changing the public contract.

---

# 18. Source of Truth

InterpretationResult is the only narrative representation within the BTE Platform.

Every downstream Engine consumes InterpretationResult.

No downstream Engine regenerates interpretation text.

The Interpretation Engine is the single source of truth for narrative output.

---

# 19. Acceptance Criteria

The Interpretation Engine architecture is complete when

✓ Runtime pipeline defined

✓ Aggregate Root defined

✓ Engine responsibilities defined

✓ Component boundaries defined

✓ Public API defined

✓ Knowledge dependency defined

✓ Documentation approved

---

END OF DOCUMENT