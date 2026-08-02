# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03 — SCREEN SPECIFICATION
# 06_CONSULTATION_REPORT.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

Related Documents

- Pack 01 Product Vision
- Pack 02 Design System
- 00_SCREEN_SPEC_STANDARD.md
- 05_EXPLAINABLE_ANALYSIS.md

==============================================================================
1. BUSINESS GOAL
==============================================================================

Consultation Report is the primary deliverable
of Commercial UI V3.

It transforms analytical results
into a coherent professional consultation.

The report is designed to be

read,

shared,

saved,

printed,

and revisited.

It is not a dashboard.

It is not a collection of cards.

It is a consulting document.

==============================================================================

2. USER GOAL
==============================================================================

Users want

a complete interpretation

that explains

their BaZi chart

from beginning

to end.

The report should feel

authoritative,

clear,

professional,

and trustworthy.

==============================================================================

3. READING GOAL
==============================================================================

After completing the report

users should understand

✓ Overall life pattern

✓ Personality

✓ Career

✓ Wealth

✓ Relationship

✓ Health

✓ Development direction

✓ Practical recommendations

without needing
additional explanation.

==============================================================================

4. SUCCESS CRITERIA
==============================================================================

The report succeeds only when

users finish reading

with

clarity,

confidence,

and

actionable understanding.

==============================================================================

5. USER QUESTIONS ANSWERED
==============================================================================

Q1

Who am I?

↓

Overview

--------------------------------------------------

Q2

How does this chart influence me?

↓

Personality

--------------------------------------------------

Q3

How should I develop?

↓

Career

↓

Wealth

↓

Relationship

↓

Health

--------------------------------------------------

Q4

What should I do?

↓

Recommendations

--------------------------------------------------

Q5

Why should I trust this report?

↓

References

==============================================================================

6. INFORMATION PRIORITY
==============================================================================

Priority 0

Executive Summary

--------------------------------------------------

Priority 1

Core Chapters

--------------------------------------------------

Priority 2

Recommendations

--------------------------------------------------

Priority 3

References

--------------------------------------------------

Priority 4

Appendix

==============================================================================

7. EXPECTED READING TIME
==============================================================================

10–30 minutes

The report supports

deep reading.

==============================================================================

8. DOCUMENT STRUCTURE
==============================================================================

Cover

↓

Executive Summary

↓

Table of Contents

↓

Chapter 1

Overview

↓

Chapter 2

Personality

↓

Chapter 3

Career

↓

Chapter 4

Wealth

↓

Chapter 5

Relationship

↓

Chapter 6

Health

↓

Chapter 7

Recommendations

↓

References

↓

Appendix

==============================================================================

9. ASCII LAYOUT
==============================================================================

+----------------------------------------------------------------+

Report Header

------------------------------------------------------------------

Executive Summary

------------------------------------------------------------------

Table of Contents

------------------------------------------------------------------

Chapter 1

------------------------------------------------------------------

Chapter 2

------------------------------------------------------------------

Chapter 3

------------------------------------------------------------------

Chapter 4

------------------------------------------------------------------

Chapter 5

------------------------------------------------------------------

Chapter 6

------------------------------------------------------------------

Chapter 7

------------------------------------------------------------------

References

------------------------------------------------------------------

Appendix

+----------------------------------------------------------------+

==============================================================================

10. COMPONENT TREE
==============================================================================

ConsultationReport

├── ReportHeader

├── ExecutiveSummary

├── TableOfContents

├── ReportChapter × N

│   ├── Heading

│   ├── Summary

│   ├── Body

│   ├── Callout

│   ├── Citation

│   └── References

├── RecommendationSection

├── ReferenceList

└── Appendix

==============================================================================

11. CHAPTER CONTRACT
==============================================================================

Every chapter

must contain

Heading

↓

Summary

↓

Body

↓

Callout (optional)

↓

Citation (optional)

↓

References (optional)

No chapter

may begin

with long paragraphs.

==============================================================================

12. GRID MAPPING
==============================================================================

Desktop

Single Reading Column

Tablet

Single Reading Column

Mobile

Single Reading Column

The report

never becomes

multi-column.

==============================================================================

13. SPACING MAPPING
==============================================================================

Uses only

Spacing Tokens.

Large spacing

between chapters.

Moderate spacing

inside chapters.

==============================================================================

14. TYPOGRAPHY ROLES
==============================================================================

Document Title

↓

Chapter Title

↓

Section Heading

↓

Body

↓

Callout

↓

Citation

↓

Metadata

==============================================================================

15. COLOR INTENT
==============================================================================

Neutral reading palette.

Semantic highlights

for

Recommendation

Warning

Important Notes

No decorative gradients.

==============================================================================

16. SURFACE ROLE
==============================================================================

One continuous document surface.

No nested cards.

No floating panels.

The document should resemble

a printed report.

==============================================================================

17. MOTION INTENT
==============================================================================

Guide

↓

Reveal

↓

Orient

Reading Progress

may update smoothly.

No decorative transitions.

==============================================================================

18. INTERACTION RULES
==============================================================================

Table of Contents

↓

Scroll to Chapter

Reading Progress

↓

Sticky Navigation

Copy Citation

↓

Supported

Expand

↓

Only for optional content.

==============================================================================

19. BINDING CONTRACT
==============================================================================

Consumes only

report.*

interpretation.*

references.*

appendix.*

No calculations.

No inference.

No rewriting.

==============================================================================

20. DATA DEPENDENCIES
==============================================================================

Required

Executive Summary

Chapters

Recommendations

Optional

References

Appendix

Knowledge Links

==============================================================================

21. LOADING STATE
==============================================================================

Display

Document Skeleton.

Maintain

final layout.

==============================================================================

22. EMPTY STATE
==============================================================================

Display

"No consultation report available."

Offer

Retry

or

Return to Analysis.

==============================================================================

23. UNAVAILABLE STATE
==============================================================================

Unavailable chapters

display

Unavailable.

Never hide

chapter titles.

==============================================================================

24. ERROR STATE
==============================================================================

Display

Friendly explanation.

Retry.

Diagnostic identifier.

==============================================================================

25. RESPONSIVE BEHAVIOUR
==============================================================================

Desktop

Reading Width.

Tablet

Comfortable Reading Width.

Mobile

Single-column report.

Reading sequence

never changes.

==============================================================================

26. ACCESSIBILITY
==============================================================================

Semantic headings.

Document outline.

Keyboard navigation.

Screen readers.

Reading Progress.

Reduced Motion.

WCAG AA.

==============================================================================

27. PERFORMANCE BUDGET
==============================================================================

Initial render

under 200 ms.

Long reports

may lazy render

chapter bodies.

Table of Contents

must remain responsive.

==============================================================================

28. COGNITIVE OUTCOME
==============================================================================

After reading

users should understand

their chart

as one coherent story,

not

as unrelated analyses.

==============================================================================

29. ANTI-PATTERNS
==============================================================================

Commercial UI V3 must never

✗ Display dashboard widgets.

✗ Repeat identical conclusions.

✗ Break reading flow.

✗ Mix explanation and evidence.

✗ Create card grids.

✗ Interrupt reading

with decorative elements.

==============================================================================

30. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Reads like a professional report.

✓ Chapters flow naturally.

✓ Recommendations are actionable.

✓ References support claims.

✓ Reading remains uninterrupted.

✓ Users complete the report

with confidence.

FAIL

✗ Dashboard appearance.

✗ Fragmented chapters.

✗ Repeated content.

✗ Weak hierarchy.

✗ Users lose context.

==============================================================================

31. FUTURE EXTENSIONS
==============================================================================

May support

PDF Export

Print Layout

Bilingual Report

Voice Narration

AI Follow-up Discussion

without changing

the document structure.

==============================================================================

32. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Document Experience

Reading Behaviour

Binding

State Management

Acceptance Rules

It does NOT define

HTML

CSS

React

Vue

PDF rendering.

==============================================================================

33. FREEZE
==============================================================================

After approval

Consultation Report
becomes the canonical
professional reading experience
of Commercial UI V3.

Every implementation

must preserve

Business Goal

Reading Goal

Document Structure

Chapter Contract

Reading Hierarchy

and Binding Contract.

# ============================================================================
# END OF DOCUMENT
# ============================================================================