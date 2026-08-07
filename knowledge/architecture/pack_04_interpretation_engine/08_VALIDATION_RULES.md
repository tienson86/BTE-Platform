# 08_VALIDATION_RULES.md

Version: 1.0

Status: CANONICAL

Pack: 04

Engine: Interpretation Engine

---

# 1. Purpose

This document defines the canonical validation rules of the Interpretation Engine.

Validation ensures every InterpretationResult is

- Structurally complete
- Grammatically valid
- Narratively coherent
- Fully traceable
- Ready for Report Engine

Interpretation validation is the final quality gate before narrative leaves the Engine.

---

# 2. Validation Philosophy

The Interpretation Engine validates

narrative quality.

It never validates

- calendar calculations
- BaZi structures
- analytical conclusions

Those responsibilities belong to upstream Engines.

---

# 3. Validation Pipeline

NarrativeContext

↓

Sentence Validation

↓

Template Validation

↓

Placeholder Validation

↓

Narrative Validation

↓

Localization Validation

↓

Reference Validation

↓

Aggregate Validation

↓

Result<InterpretationResult>

Every stage is mandatory.

---

# 4. Validation Categories

The Interpretation Engine performs

Sentence Validation

Template Validation

Placeholder Validation

Narrative Validation

Localization Validation

Reference Validation

Trace Validation

Aggregate Validation

Metadata Validation

---

# 5. Sentence Validation

Validate every sentence.

Checks

✓ Sentence exists

✓ Sentence enabled

✓ Language valid

✓ Style valid

✓ Audience valid

✓ Metadata complete

No missing sentence is allowed.

---

# 6. Template Validation

Validate

✓ Template exists

✓ Template version

✓ Paragraph layout

✓ Section layout

✓ Ordering rules

✓ Metadata

Every section must have a valid template.

---

# 7. Placeholder Validation

Validate

✓ Placeholder exists

✓ Placeholder resolved

✓ Value type valid

✓ Formatter valid

✓ Localization available

✓ No unresolved placeholders

Every placeholder must resolve successfully.

---

# 8. Narrative Validation

Validate

✓ Logical flow

✓ Paragraph continuity

✓ Section continuity

✓ Summary consistency

✓ No duplicated meaning

✓ No contradictory wording

Narrative must be readable.

---

# 9. Localization Validation

Validate

✓ Language

✓ Locale

✓ Terminology

✓ Writing style

✓ Formatting

Localization never changes meaning.

---

# 10. Reference Validation

Every sentence must reference

Analysis Node

Evidence

Confidence

Rule Trace

Broken references are not allowed.

---

# 11. Trace Validation

Validate

Sentence Trace

Template Trace

Placeholder Trace

Builder Trace

Runtime Trace

Every narrative element must be traceable.

---

# 12. Aggregate Validation

Validate

InterpretationResult

Checks

✓ Metadata

✓ Narrative Tree

✓ Sections

✓ Paragraphs

✓ Sentences

✓ References

✓ Trace Collection

No missing Aggregate members.

---

# 13. Metadata Validation

Validate

Engine Version

Language

Knowledge Version

Template Version

Sentence Version

Execution Duration

Metadata is mandatory.

---

# 14. Consistency Validation

Verify

Section titles

Paragraph ordering

Sentence ordering

Summary

Narrative Tree

Consistency must be deterministic.

---

# 15. Explainability Validation

Every sentence must explain

which

Analysis Node

generated it.

Every paragraph must remain traceable.

No anonymous narrative is allowed.

---

# 16. Error Handling

Possible errors

SentenceValidationError

TemplateValidationError

PlaceholderValidationError

NarrativeValidationError

LocalizationValidationError

ReferenceValidationError

AggregateValidationError

InternalError

Every error contains

- code

- stage

- component

- message

- trace_id

- timestamp

---

# 17. Warning Rules

Warnings allow execution.

Examples

Fallback sentence

Fallback template

Optional placeholder missing

Deprecated terminology

Warnings never change meaning.

---

# 18. Validation Result

Validation returns

Result<InterpretationResult>

Possible states

SUCCESS

WARNING

ERROR

Only SUCCESS and WARNING produce InterpretationResult.

---

# 19. Logging

Validation records

Stage

Duration

Warnings

Errors

Trace ID

No personal data may appear in logs.

---

# 20. Acceptance Checklist

Interpretation validation is complete when

✓ Sentence Validation passed

✓ Template Validation passed

✓ Placeholder Validation passed

✓ Narrative Validation passed

✓ Localization Validation passed

✓ Reference Validation passed

✓ Trace Validation passed

✓ Aggregate Validation passed

✓ Metadata Validation passed

✓ Structured Result returned

---

END OF DOCUMENT