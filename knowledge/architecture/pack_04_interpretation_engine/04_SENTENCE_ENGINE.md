# 04_SENTENCE_ENGINE.md

Version: 1.0

Status: CANONICAL

Pack: 04

Engine: Interpretation Engine

Component: Sentence Engine

---

# 1. Purpose

The Sentence Engine is responsible for selecting the most appropriate canonical sentences for a given AnalysisResult.

It converts structured analytical conclusions into reusable narrative units.

The Sentence Engine never performs analysis.

The Sentence Engine never modifies analytical conclusions.

---

# 2. Position in Runtime

AnalysisResult

↓

Narrative Context

↓

Sentence Engine

↓

Sentence Collection

↓

Template Engine

↓

InterpretationResult

---

# 3. Sentence Philosophy

Sentences express knowledge.

They never create knowledge.

Every sentence is selected from the canonical Sentence Library.

No sentence is generated from business logic.

---

# 4. Responsibilities

The Sentence Engine is responsible for

✓ Sentence Selection

✓ Sentence Ranking

✓ Sentence Filtering

✓ Sentence Variant Selection

✓ Localization

✓ Style Selection

The Sentence Engine is NOT responsible for

✗ Rule execution

✗ Score calculation

✗ Template rendering

✗ Placeholder binding

---

# 5. Runtime Flow

NarrativeContext

↓

Sentence Candidate Search

↓

Sentence Filtering

↓

Sentence Ranking

↓

Sentence Selection

↓

Sentence Collection

---

# 6. Input

Consumes

NarrativeContext

Containing

AnalysisResult

Localization

Writing Style

Audience Profile

Confidence

Metadata

---

# 7. Output

Produces

SentenceCollection

Each Sentence remains unresolved.

Placeholders are preserved.

---

# 8. Sentence Library

Sentences are stored inside

Sentence Library

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

The library is immutable.

---

# 9. Sentence Structure

Each sentence contains

Sentence ID

Category

Priority

Language

Writing Style

Audience

Template Reference

Placeholder List

Metadata

Example

"Nhật chủ {{day_master}} có xu hướng {{strength}}."

---

# 10. Sentence Variants

One analytical conclusion

may have multiple sentence variants.

Example

Variant A

"Nhật chủ khá vượng."

Variant B

"Khí lực bản mệnh tương đối mạnh."

Variant C

"Mệnh cục có nền khí vững."

Selection depends on style profile.

---

# 11. Sentence Ranking

Candidate sentences are ranked by

Priority

Language

Audience

Writing Style

Confidence

Knowledge Version

The highest ranked sentence is selected.

---

# 12. Sentence Filtering

Filter removes

Deprecated Sentences

Wrong Language

Wrong Audience

Disabled Sentences

Low Priority Variants

Filtering never changes meaning.

---

# 13. Localization

Supported

Vietnamese

English

Future languages

Localization affects wording only.

Meaning remains unchanged.

---

# 14. Writing Style

Supported styles

Professional

Academic

Traditional

Simple

Beginner

Expert

Style changes wording only.

Analysis remains identical.

---

# 15. Audience Profile

Supported audiences

General User

Student

Consultant

Master

API

Sentence selection adapts to audience.

---

# 16. Confidence Adaptation

Confidence influences wording.

High Confidence

↓

Definitive wording

Medium Confidence

↓

Balanced wording

Low Confidence

↓

Cautious wording

Analytical result never changes.

---

# 17. Metadata

Every sentence stores

Version

Knowledge Version

Language

Priority

Author

Created Date

Updated Date

Metadata supports auditing.

---

# 18. Error Handling

Possible errors

SentenceNotFound

LanguageNotFound

VariantConflict

MetadataError

RuntimeError

Errors return

Result.Error

---

# 19. Performance

Target

10,000 Sentences

↓

Selection

<20 ms

Supports caching.

---

# 20. Thread Safety

The Sentence Engine is

✓ Stateless

✓ Immutable

✓ Deterministic

✓ Thread-safe

---

# 21. Downstream Contract

Produces

SentenceCollection

Consumed by

Template Engine

No downstream component

re-selects sentences.

---

# 22. Acceptance Criteria

The Sentence Engine is complete when

✓ Sentence Library loaded

✓ Candidate search completed

✓ Filtering completed

✓ Ranking completed

✓ Localization supported

✓ Style adaptation supported

✓ Metadata preserved

✓ Thread-safe

✓ Deterministic

✓ Performance targets achieved

✓ Documentation approved

---

END OF DOCUMENT