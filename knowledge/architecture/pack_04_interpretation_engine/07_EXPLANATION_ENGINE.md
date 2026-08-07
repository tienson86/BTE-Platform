# 07_EXPLANATION_ENGINE.md

Version: 1.0

Status: CANONICAL

Pack: 04

Engine: Interpretation Engine

Component: Explanation Engine

---

# 1. Purpose

The Explanation Engine is responsible for transforming rendered sentences into coherent, structured and readable explanations.

It builds the final narrative while preserving analytical accuracy.

The Explanation Engine never performs analytical reasoning.

The Explanation Engine never changes analytical conclusions.

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

Interpretation Builder

↓

InterpretationResult

---

# 3. Explanation Philosophy

Explanation is narrative composition.

It never creates new analytical facts.

Every explanation must originate from AnalysisResult.

Every sentence remains traceable.

---

# 4. Responsibilities

The Explanation Engine is responsible for

✓ Sentence Composition

✓ Paragraph Composition

✓ Narrative Flow

✓ Transition Construction

✓ Summary Construction

✓ Readability Optimization

The Explanation Engine is NOT responsible for

✗ Rule execution

✗ Score calculation

✗ Placeholder resolution

✗ Report rendering

---

# 5. Runtime Flow

Rendered Sentence Collection

↓

Sentence Ordering

↓

Transition Builder

↓

Paragraph Builder

↓

Section Builder

↓

Summary Builder

↓

Narrative Validation

↓

Explanation Collection

---

# 6. Input

Consumes

RenderedSentenceCollection

NarrativeContext

TemplateCollection

Metadata

Localization

Writing Style

---

# 7. Output

Produces

ExplanationCollection

Containing

Paragraphs

Sections

Summary

Narrative Tree

ExplanationCollection is immutable.

---

# 8. Sentence Ordering

The Explanation Engine determines

Sentence Order

Logical Sequence

Narrative Continuity

Ordering follows Template definitions.

---

# 9. Transition Builder

Transitions improve readability.

Examples

Ngoài ra

Đồng thời

Bên cạnh đó

Tuy nhiên

Mặt khác

Do đó

Consequently

Furthermore

Transitions never alter meaning.

---

# 10. Paragraph Builder

Paragraphs contain

Introduction

Evidence

Analysis Summary

Recommendation

Conclusion

Every paragraph has one topic.

---

# 11. Section Builder

Sections include

Overview

Strength

Pattern

Useful God

Ten Gods

Five Elements

Shen Sha

Luck

Summary

Sections remain independent.

---

# 12. Summary Builder

Produces

Overall Summary

Executive Summary

Key Findings

Recommendations

The Summary never introduces new analytical conclusions.

---

# 13. Narrative Optimization

Optimization includes

Removing repetition

Combining similar sentences

Improving readability

Maintaining logical flow

Reducing redundancy

Optimization never changes meaning.

---

# 14. Writing Style

Supported styles

Professional

Academic

Traditional

Simple

Beginner

Expert

Consultant

Style affects expression only.

Meaning remains identical.

---

# 15. Localization

Supported languages

Vietnamese

English

Future languages

Localization changes wording only.

AnalysisResult remains unchanged.

---

# 16. Narrative Tree

The Explanation Engine builds

Section

↓

Paragraph

↓

Sentence

↓

Fragment

The Narrative Tree becomes part of InterpretationResult.

---

# 17. Explainability

Every Paragraph references

Analysis Nodes

Evidence

Confidence

Rule Trace

Every explanation remains fully traceable.

---

# 18. Metadata

Every explanation stores

Version

Language

Writing Style

Execution Duration

Builder Trace

Timestamp

Metadata supports auditing.

---

# 19. Error Handling

Possible errors

NarrativeError

ParagraphError

SectionError

SummaryError

LocalizationError

MetadataError

RuntimeError

Errors return

Result.Error

---

# 20. Performance

Target

1,000 Sentences

↓

Explanation Collection

<30 ms

Supports parallel paragraph construction.

---

# 21. Thread Safety

The Explanation Engine is

✓ Stateless

✓ Immutable

✓ Deterministic

✓ Thread-safe

---

# 22. Downstream Contract

Produces

ExplanationCollection

Consumed by

Interpretation Builder

No downstream component

rewrites explanations.

---

# 23. Acceptance Criteria

The Explanation Engine is complete when

✓ Narrative flow completed

✓ Paragraphs created

✓ Sections created

✓ Summary created

✓ Narrative Tree completed

✓ References preserved

✓ Metadata preserved

✓ Thread-safe

✓ Deterministic

✓ Performance targets achieved

✓ Documentation approved

---

END OF DOCUMENT