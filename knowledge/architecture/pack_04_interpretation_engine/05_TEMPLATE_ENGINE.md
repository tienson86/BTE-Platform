# 05_TEMPLATE_ENGINE.md

Version: 1.0

Status: CANONICAL

Pack: 04

Engine: Interpretation Engine

Component: Template Engine

---

# 1. Purpose

The Template Engine is responsible for selecting and applying canonical narrative templates.

It transforms a collection of selected sentences into structured narrative layouts.

The Template Engine defines narrative organization only.

It never performs analytical reasoning.

It never changes analytical conclusions.

---

# 2. Position in Runtime

AnalysisResult

↓

Sentence Engine

↓

Sentence Collection

↓

Template Engine

↓

Template Collection

↓

Placeholder Engine

↓

InterpretationResult

---

# 3. Template Philosophy

Templates define structure.

Sentences define content.

Analysis defines meaning.

The Template Engine never creates new meaning.

It only determines how existing content is organized.

---

# 4. Responsibilities

The Template Engine is responsible for

✓ Template Selection

✓ Section Layout

✓ Paragraph Layout

✓ Sentence Ordering

✓ Summary Layout

✓ Narrative Structure

The Template Engine is NOT responsible for

✗ Rule execution

✗ Score calculation

✗ Sentence generation

✗ Placeholder replacement

✗ Interpretation rewriting

---

# 5. Runtime Flow

Sentence Collection

↓

Template Candidate Search

↓

Template Filtering

↓

Template Ranking

↓

Template Selection

↓

Narrative Layout

↓

Template Collection

---

# 6. Input

Consumes

SentenceCollection

NarrativeContext

Localization

Writing Style

Audience

Metadata

---

# 7. Output

Produces

TemplateCollection

Templates remain unresolved.

Placeholders are preserved.

---

# 8. Template Library

Templates are stored in

Template Library

Categories

Overview

Strength

Pattern

Useful God

Ten Gods

Five Elements

Shen Sha

Luck

Summary

Templates are immutable.

---

# 9. Template Structure

Each Template contains

Template ID

Category

Language

Writing Style

Audience

Paragraph Layout

Sentence Slots

Ordering Rules

Metadata

---

# 10. Section Template

Each section defines

Title

Paragraph Sequence

Sentence Groups

Summary Block

Optional Notes

Sections remain independent.

---

# 11. Paragraph Template

Each paragraph defines

Paragraph Type

Sentence Order

Maximum Sentences

Minimum Sentences

Transition Rules

Paragraphs contain no analytical logic.

---

# 12. Sentence Slots

Templates contain ordered sentence slots.

Example

Sentence 1

↓

Sentence 2

↓

Sentence 3

↓

Summary Sentence

Sentence order is deterministic.

---

# 13. Template Variants

One section

may have multiple templates.

Examples

Professional

Academic

Traditional

Beginner

Consultant

Variant selection is deterministic.

---

# 14. Template Ranking

Candidate templates are ranked by

Priority

Writing Style

Audience

Language

Knowledge Version

Highest ranked template is selected.

---

# 15. Template Filtering

Filter removes

Deprecated Templates

Wrong Language

Wrong Audience

Disabled Templates

Unsupported Variants

Filtering never changes meaning.

---

# 16. Localization

Templates support

Vietnamese

English

Future languages

Localization changes presentation only.

---

# 17. Writing Style

Supported styles

Professional

Academic

Traditional

Simple

Beginner

Expert

Writing style affects organization only.

Meaning remains identical.

---

# 18. Metadata

Every template stores

Template Version

Knowledge Version

Language

Priority

Author

Created Date

Updated Date

Metadata supports auditing.

---

# 19. Error Handling

Possible errors

TemplateNotFound

VariantConflict

LanguageError

MetadataError

RuntimeError

Errors return

Result.Error

No partial template collection is returned.

---

# 20. Performance

Target

10,000 Templates

↓

Selection

<20 ms

Supports caching.

---

# 21. Thread Safety

The Template Engine is

✓ Stateless

✓ Immutable

✓ Deterministic

✓ Thread-safe

---

# 22. Downstream Contract

Produces

TemplateCollection

Consumed by

Placeholder Engine

No downstream component

re-selects templates.

---

# 23. Acceptance Criteria

The Template Engine is complete when

✓ Template Library loaded

✓ Candidate search completed

✓ Filtering completed

✓ Ranking completed

✓ Section layout generated

✓ Paragraph layout generated

✓ Metadata preserved

✓ Thread-safe

✓ Deterministic

✓ Performance targets achieved

✓ Documentation approved

---

END OF DOCUMENT