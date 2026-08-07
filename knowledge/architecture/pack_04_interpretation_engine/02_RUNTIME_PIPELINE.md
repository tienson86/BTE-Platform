# 02_RUNTIME_PIPELINE.md

Version: 1.0

Status: CANONICAL

Pack: 04

Engine: Interpretation Engine

---

# 1. Purpose

This document defines the canonical runtime pipeline of the Interpretation Engine.

The Interpretation Engine transforms a canonical AnalysisResult into a structured InterpretationResult through a deterministic narrative pipeline.

The pipeline never performs analytical reasoning.

It only converts analytical conclusions into natural language.

---

# 2. Runtime Philosophy

The Interpretation Engine is a narrative engine.

It does not

- execute rules
- calculate scores
- evaluate priorities
- modify AnalysisResult

Its responsibility is

Express AnalysisResult
↓

Narrative Structure
↓

InterpretationResult

Every execution must be deterministic, explainable and reproducible.

---

# 3. Canonical Runtime Pipeline

AnalysisResult

↓

Narrative Context Builder

↓

Sentence Engine

↓

Template Engine

↓

Placeholder Engine

↓

Explanation Engine

↓

Section Builder

↓

Interpretation Builder

↓

Interpretation Validation

↓

Result<InterpretationResult>

---

# 4. Runtime Overview

| Stage | Input | Output | Responsibility |
|--------|-------|--------|----------------|
| 01 | AnalysisResult | NarrativeContext | Prepare runtime context |
| 02 | NarrativeContext | SentenceCollection | Select canonical sentences |
| 03 | SentenceCollection | TemplateCollection | Select templates |
| 04 | Templates | Rendered Sentences | Bind placeholders |
| 05 | Rendered Sentences | ParagraphCollection | Build explanations |
| 06 | ParagraphCollection | SectionCollection | Organize sections |
| 07 | SectionCollection | InterpretationResult | Build Aggregate |
| 08 | InterpretationResult | Result<InterpretationResult> | Final validation |

---

# 5. Stage 01 — Narrative Context Builder

Input

AnalysisResult

Responsibilities

Prepare runtime context.

Collect

- Analysis Nodes
- Evidence
- Confidence
- References
- Metadata
- Localization
- Writing Style

Output

NarrativeContext

NarrativeContext is immutable.

---

# 6. Stage 02 — Sentence Engine

Consumes

NarrativeContext

Responsibilities

Select canonical sentences.

Sentence selection is based on

- Analysis Type
- Confidence
- Severity
- Writing Style
- Language

Output

SentenceCollection

No placeholders replaced.

---

# 7. Stage 03 — Template Engine

Consumes

SentenceCollection

Responsibilities

Select

- Paragraph Templates
- Section Templates
- Summary Templates

Templates define structure only.

Output

TemplateCollection

---

# 8. Stage 04 — Placeholder Engine

Consumes

TemplateCollection

Responsibilities

Resolve every placeholder.

Examples

{{day_master}}

{{pattern}}

{{strength}}

{{useful_god}}

{{season}}

Output

Rendered Sentences

No analytical values are recalculated.

---

# 9. Stage 05 — Explanation Engine

Consumes

Rendered Sentences

Responsibilities

Construct

Paragraphs

Merge related sentences

Remove redundancy

Improve readability

Maintain traceability

Output

ParagraphCollection

---

# 10. Stage 06 — Section Builder

Consumes

ParagraphCollection

Responsibilities

Build

Overview

Strength

Pattern

Useful God

Ten Gods

Five Elements

Shen Sha

Luck

Summary

Output

SectionCollection

Sections remain independent.

---

# 11. Stage 07 — Interpretation Builder

Consumes

SectionCollection

Produces

InterpretationResult

InterpretationResult contains

- Metadata
- Narrative Tree
- References
- Trace
- Localization
- Sections

Aggregate becomes immutable.

---

# 12. Stage 08 — Interpretation Validation

Validate

InterpretationResult

Checks

✓ Required Sections

✓ Required Paragraphs

✓ Placeholder Resolution

✓ Reference Integrity

✓ Narrative Integrity

✓ Metadata

Output

Result<InterpretationResult>

---

# 13. Error Flow

AnalysisResult

↓

Narrative Context

↓

Sentence Engine

↓

❌ Error

↓

Result.Error

↓

Pipeline Stops

No partial interpretation is returned.

---

# 14. Success Flow

AnalysisResult

↓

Narrative Context

↓

Sentence Engine

↓

Template Engine

↓

Placeholder Engine

↓

Explanation Engine

↓

Section Builder

↓

Interpretation Builder

↓

Validation

↓

InterpretationResult

↓

Result.Success

---

# 15. Runtime Characteristics

The Interpretation Engine is

✓ Deterministic

✓ Stateless

✓ Immutable

✓ Thread-safe

✓ Localizable

✓ Explainable

---

# 16. Logging

Every runtime stage records

- Stage Name
- Start Time
- End Time
- Duration
- Selected Sentences
- Selected Templates
- Warning Count
- Error Count
- Trace ID

No personal information may be logged.

---

# 17. Performance Targets

Single Interpretation

<100 ms

100 Interpretations

<1 second

1000 Interpretations

<10 seconds

No network dependency.

---

# 18. Downstream Contract

Only InterpretationResult leaves the Engine.

Consumed by

- Report Engine
- Desktop UI
- Tablet UI
- Mobile UI
- Voice Engine

No downstream component regenerates narrative.

---

# 19. Runtime Diagram

AnalysisResult

↓

Narrative Context

↓

Sentence Engine

↓

Template Engine

↓

Placeholder Engine

↓

Explanation Engine

↓

Section Builder

↓

Interpretation Builder

↓

Validation

↓

InterpretationResult

↓

Report Engine

---

# 20. Acceptance Criteria

The runtime pipeline is complete when

✓ Narrative Context created

✓ Sentences selected

✓ Templates selected

✓ Placeholders resolved

✓ Explanations built

✓ Sections built

✓ InterpretationResult built

✓ Validation completed

✓ Runtime deterministic

✓ Thread-safe

✓ Unit Tests pass

✓ Integration Tests pass

✓ Golden Dataset verified

---

END OF DOCUMENT