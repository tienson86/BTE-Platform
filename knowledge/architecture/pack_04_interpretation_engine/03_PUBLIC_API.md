# 03_PUBLIC_API.md

Version: 1.0

Status: CANONICAL

Pack: 04

Engine: Interpretation Engine

---

# 1. Purpose

This document defines the canonical Public API of the Interpretation Engine.

The Interpretation Engine exposes one official service responsible for transforming a canonical AnalysisResult into a canonical InterpretationResult.

All narrative generation remains internal.

---

# 2. API Philosophy

The Interpretation Engine exposes one public service.

Consumers never execute

- Sentence Engine
- Template Engine
- Placeholder Engine
- Explanation Engine
- Section Builder
- Validation Engine

directly.

All narrative logic is encapsulated inside the Engine.

---

# 3. Public Service

Canonical Service

InterpretationEngine

Responsibilities

- Validate input
- Execute narrative pipeline
- Produce InterpretationResult
- Return structured execution result

---

# 4. Public Entry Point

InterpretationEngine.run()

Input

AnalysisResult

↓

Output

Result<InterpretationResult>

This is the only supported public API.

---

# 5. Input Contract

Input Model

AnalysisResult

Produced only by

Score Engine

Requirements

✓ Canonical

✓ Immutable

✓ Fully validated

The Interpretation Engine never accepts

- JSON
- Dictionary
- Anonymous Objects
- UI Models

Only canonical AnalysisResult.

---

# 6. Output Contract

Output

Result<InterpretationResult>

Possible states

Success

↓

InterpretationResult

Warning

↓

InterpretationResult + Warnings

Failure

↓

Structured Error

Partial interpretation is never returned.

---

# 7. Result Model

Result<T>

contains

success

value

warnings

error

metadata

trace

Result<T> is immutable.

Null is never returned.

---

# 8. Public Aggregate

InterpretationResult

contains

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

NarrativeTree

ReferenceCollection

TraceCollection

InterpretationResult is immutable.

---

# 9. Internal Components

The following components are private.

NarrativeContextBuilder

SentenceEngine

TemplateEngine

PlaceholderEngine

ExplanationEngine

SectionBuilder

InterpretationBuilder

ValidationEngine

These components are implementation details.

They are never exposed outside the Interpretation Engine.

---

# 10. Dependency Rules

Allowed

AnalysisResult

Sentence Library

Template Library

Placeholder Library

Localization Resources

Forbidden

Calendar Engine

BaZi Engine

Rule Database

Score Engine internals

Desktop UI

Mobile UI

Report Engine

The Interpretation Engine consumes only AnalysisResult and narrative resources.

---

# 11. Runtime Ownership

The Interpretation Engine owns

- Sentence Selection
- Template Selection
- Placeholder Binding
- Explanation Construction
- Section Construction
- Narrative Construction
- InterpretationResult generation

No downstream Engine regenerates narrative.

---

# 12. Error Model

Possible errors

ValidationError

SentenceSelectionError

TemplateError

PlaceholderError

ExplanationError

SectionBuilderError

InterpretationError

InternalError

Every error contains

- code
- stage
- component
- message
- timestamp
- engine_version
- trace_id

---

# 13. Warning Model

Warnings do not terminate execution.

Examples

Missing optional sentence

Fallback template used

Unknown optional placeholder

Localization fallback

Low confidence narrative

Warnings are attached to Result<InterpretationResult>.

---

# 14. Traceability

Every execution produces

Narrative Trace

including

- Selected Sentences

- Selected Templates

- Placeholder Bindings

- Generated Paragraphs

- Generated Sections

- Runtime Trace

Narrative Trace supports debugging and auditing.

---

# 15. Thread Safety

The Interpretation Engine is

✓ Stateless

✓ Deterministic

✓ Thread-safe

✓ Immutable

Parallel execution is fully supported.

---

# 16. Performance

Target

Single Interpretation

<100 ms

100 Interpretations

<1 second

1000 Interpretations

<10 seconds

No external network dependency.

---

# 17. Semantic Versioning

The Public API follows Semantic Versioning.

Major

Breaking API changes

Minor

Backward-compatible additions

Patch

Bug fixes

Breaking changes require Architecture Review.

---

# 18. Integration Example

AnalysisResult

↓

InterpretationEngine.run()

↓

Result<InterpretationResult>

↓

ReportEngine.run()

↓

Result<ReportResult>

The Interpretation Engine never invokes downstream Engines.

---

# 19. Extension Rules

Future internal components may be added.

Examples

AI Rewrite Engine

Style Adapter

Tone Adapter

Localization Adapter

Personalization Adapter

Extensions remain internal.

The Public API remains unchanged.

---

# 20. API Stability

The Public API is considered stable when

Input remains

AnalysisResult

Output remains

Result<InterpretationResult>

Internal implementation may evolve without affecting consumers.

---

# 21. Acceptance Criteria

The Public API is complete when

✓ One public service

✓ One public entry point

✓ One canonical input

✓ One canonical output

✓ InterpretationResult Aggregate returned

✓ Internal components hidden

✓ Strong typing enforced

✓ Thread-safe

✓ Fully documented

---

END OF DOCUMENT