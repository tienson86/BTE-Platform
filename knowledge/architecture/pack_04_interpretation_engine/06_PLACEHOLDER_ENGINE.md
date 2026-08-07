# 06_PLACEHOLDER_ENGINE.md

Version: 1.0

Status: CANONICAL

Pack: 04

Engine: Interpretation Engine

Component: Placeholder Engine

---

# 1. Purpose

The Placeholder Engine is responsible for resolving canonical placeholders into human-readable values.

It transforms sentence templates into fully rendered sentences.

The Placeholder Engine never performs analytical reasoning.

The Placeholder Engine never changes analytical conclusions.

---

# 2. Position in Runtime

AnalysisResult

↓

Sentence Engine

↓

Template Engine

↓

Placeholder Engine

↓

Rendered Sentences

↓

Explanation Engine

↓

InterpretationResult

---

# 3. Placeholder Philosophy

Placeholders represent structured data.

They never represent analytical logic.

The Placeholder Engine replaces placeholders with canonical values only.

Every replacement must be deterministic.

---

# 4. Responsibilities

The Placeholder Engine is responsible for

✓ Placeholder Resolution

✓ Value Formatting

✓ Localization

✓ Number Formatting

✓ Date Formatting

✓ Runtime Validation

The Placeholder Engine is NOT responsible for

✗ Rule execution

✗ Score calculation

✗ Sentence selection

✗ Template selection

✗ Interpretation rewriting

---

# 5. Runtime Flow

Template Collection

↓

Placeholder Discovery

↓

Value Resolution

↓

Value Formatting

↓

Placeholder Replacement

↓

Rendered Sentences

---

# 6. Input

Consumes

NarrativeContext

TemplateCollection

PlaceholderCollection

Localization Settings

Metadata

---

# 7. Output

Produces

RenderedSentenceCollection

All placeholders are resolved.

No unresolved placeholders remain.

---

# 8. Placeholder Library

Every placeholder is registered in the Placeholder Library.

Examples

{{day_master}}

{{month_branch}}

{{pattern}}

{{strength}}

{{useful_god}}

{{confidence}}

{{overall_score}}

Unknown placeholders are rejected.

---

# 9. Placeholder Structure

Every Placeholder contains

Placeholder ID

Key

Value Type

Source

Formatter

Localization

Metadata

---

# 10. Placeholder Sources

Supported sources

AnalysisResult

Interpretation Metadata

Localization Resources

Runtime Context

Static Dictionary

The Placeholder Engine never reads the Rule Database.

---

# 11. Supported Value Types

Supported value types

String

Integer

Decimal

Boolean

Enumeration

Date

Time

Localized Text

Collections

Every value has a canonical formatter.

---

# 12. Formatting Rules

Formatting supports

Number Formatting

Percentage Formatting

Date Formatting

Language Formatting

Pluralization

Capitalization

Formatting never changes meaning.

---

# 13. Localization

Supported languages

Vietnamese

English

Future languages

Localization affects presentation only.

---

# 14. Placeholder Resolution

Every placeholder follows

Locate

↓

Validate

↓

Resolve

↓

Format

↓

Replace

↓

Verify

Replacement is deterministic.

---

# 15. Missing Placeholder Policy

Required Placeholder

↓

Error

Optional Placeholder

↓

Fallback

↓

Default Value

↓

Warning

No unresolved placeholder is allowed in the final output.

---

# 16. Runtime Validation

Validation checks

✓ Placeholder exists

✓ Value exists

✓ Formatter exists

✓ Type matches

✓ Localization available

✓ Output valid

---

# 17. Metadata

Every placeholder stores

Version

Source

Formatter

Language

Created Date

Updated Date

Metadata supports auditing.

---

# 18. Error Handling

Possible errors

PlaceholderNotFound

FormatterError

LocalizationError

TypeMismatch

ValidationError

RuntimeError

Errors return

Result.Error

---

# 19. Performance

Target

50,000 Placeholder Replacements

↓

<20 ms

Supports caching.

---

# 20. Thread Safety

The Placeholder Engine is

✓ Stateless

✓ Immutable

✓ Deterministic

✓ Thread-safe

---

# 21. Downstream Contract

Produces

RenderedSentenceCollection

Consumed by

Explanation Engine

No downstream component

replaces placeholders again.

---

# 22. Placeholder Trace

Every replacement records

Placeholder ID

Source Field

Resolved Value

Formatter

Localization

Replacement Time

Trace ID

Supports debugging and auditing.

---

# 23. Acceptance Criteria

The Placeholder Engine is complete when

✓ Placeholder Library loaded

✓ Every placeholder resolved

✓ Required placeholders validated

✓ Formatting applied

✓ Localization applied

✓ Metadata preserved

✓ Trace generated

✓ Thread-safe

✓ Deterministic

✓ Performance targets achieved

✓ Documentation approved

---

END OF DOCUMENT