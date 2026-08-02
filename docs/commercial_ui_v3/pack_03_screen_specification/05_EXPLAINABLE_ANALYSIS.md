# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03 — SCREEN SPECIFICATION
# 05_EXPLAINABLE_ANALYSIS.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

Related Documents

- Pack 01 Product Vision
- Pack 02 Design System
- 00_SCREEN_SPEC_STANDARD.md

==============================================================================
1. BUSINESS GOAL
==============================================================================

Explainable Analysis is the core analytical workspace
of Commercial UI V3.

Its objective is

not

to present conclusions.

Its objective is

to explain

why every conclusion exists.

Every analytical conclusion
must be traceable.

Users should always understand

Reason

↓

Evidence

↓

Rule

↓

Confidence

==============================================================================

2. USER GOAL
==============================================================================

Users want to know

• Why did the system reach this conclusion?

• Which rules support it?

• What evidence was used?

• How reliable is this conclusion?

• Where can I verify it?

==============================================================================

3. READING GOAL
==============================================================================

After reading this screen

users should understand

✓ The analytical conclusion

✓ The reasoning

✓ The supporting evidence

✓ The governing rules

✓ Confidence level

✓ Related knowledge

without reading engine documentation.

==============================================================================

4. SUCCESS CRITERIA
==============================================================================

The screen succeeds only when

users can explain

why

the system reached

its conclusion.

Acceptance without understanding

is considered failure.

==============================================================================

5. USER QUESTIONS ANSWERED
==============================================================================

Q1

What is the conclusion?

↓

Conclusion

--------------------------------------------------

Q2

Why?

↓

Explanation

--------------------------------------------------

Q3

What supports it?

↓

Evidence

--------------------------------------------------

Q4

Which rule?

↓

Rule Reference

--------------------------------------------------

Q5

How reliable?

↓

Confidence

--------------------------------------------------

Q6

Where can I learn more?

↓

Knowledge Reference

==============================================================================

6. INFORMATION PRIORITY
==============================================================================

Priority 0

Conclusion

--------------------------------------------------

Priority 1

Explanation

--------------------------------------------------

Priority 2

Evidence

--------------------------------------------------

Priority 3

Rule

--------------------------------------------------

Priority 4

Confidence

--------------------------------------------------

Priority 5

Knowledge

No section
may bypass
this hierarchy.

==============================================================================

7. EXPECTED READING TIME
==============================================================================

2–5 minutes

This section supports

deep understanding,

not glance reading.

==============================================================================

8. ASCII LAYOUT
==============================================================================

+------------------------------------------------------------------+

EXPLAINABLE ANALYSIS

--------------------------------------------------------------------

Conclusion

--------------------------------------------------------------------

Explanation

--------------------------------------------------------------------

Evidence

--------------------------------------------------------------------

Rule Reference

--------------------------------------------------------------------

Confidence

--------------------------------------------------------------------

Knowledge Reference

+------------------------------------------------------------------+

Every Analysis Block
follows exactly
this structure.

==============================================================================

9. COMPONENT TREE
==============================================================================

ExplainableAnalysis

├── AnalysisBlock

│   ├── ConclusionPanel

│   ├── ExplanationPanel

│   ├── EvidencePanel

│   ├── RulePanel

│   ├── ConfidenceIndicator

│   └── KnowledgeReference

Repeat

for every analytical topic.

==============================================================================

10. ANALYSIS BLOCK CONTRACT
==============================================================================

Every Analysis Block
must contain

Conclusion

↓

Explanation

↓

Evidence

↓

Rule

↓

Confidence

↓

Knowledge

No field
may be omitted.

If unavailable

display

Unavailable.

==============================================================================

11. SUPPORTED ANALYSIS TOPICS
==============================================================================

The screen supports

Five Elements

Ten Gods

Pattern

Strength

Useful God

Favorable God

Unfavorable God

Combinations

Clashes

Punishments

Harms

Breaks

Shen Sha

Priority Resolution

Knowledge Summary

Topics may grow.

Structure never changes.

==============================================================================

12. GRID MAPPING
==============================================================================

Desktop

Single Reading Column

Tablet

Single Reading Column

Mobile

Single Reading Column

Analysis
must never become
a card dashboard.

==============================================================================

13. SPACING MAPPING
==============================================================================

Uses only

Spacing Tokens

space.chapter

↓

space.section

↓

space.block

Evidence
must remain visually attached
to its explanation.

==============================================================================

14. TYPOGRAPHY ROLES
==============================================================================

Conclusion

↓

Explanation

↓

Evidence

↓

Rule

↓

Knowledge

↓

Metadata

Typography
defines hierarchy.

==============================================================================

15. COLOR INTENT
==============================================================================

Semantic colors only.

Status

Evidence

Confidence

Warning

Neutral

No decorative colors.

==============================================================================

16. SURFACE ROLE
==============================================================================

One Reading Surface.

Analysis Blocks

are chapters,

not widgets.

Nested cards
are forbidden.

==============================================================================

17. MOTION INTENT
==============================================================================

Guide

↓

Reveal

↓

Focus

Expand / Collapse

applies only
to secondary content.

The Conclusion
must always remain visible.

==============================================================================

18. INTERACTION RULES
==============================================================================

Hover

Highlight references.

Click / Tap

Expand

Evidence

Rule

Knowledge.

Keyboard

Supported.

Touch

Supported.

==============================================================================

19. BINDING CONTRACT
==============================================================================

Consumes only

analysis.*

rule.*

knowledge.*

confidence.*

report.*

Presentation only.

No calculation.

No inference.

No AI rewrite.

==============================================================================

20. DATA DEPENDENCIES
==============================================================================

Required

Conclusion

Explanation

Optional

Evidence

Rule

Confidence

Knowledge

Unavailable fields

must preserve layout.

==============================================================================

21. LOADING STATE
==============================================================================

Display

Analysis Skeleton

Maintain

identical layout

until content arrives.

==============================================================================

22. EMPTY STATE
==============================================================================

Display

"No analytical explanation available."

Provide

Retry

or

Return to Summary.

==============================================================================

23. UNAVAILABLE STATE
==============================================================================

Missing content

display

Unavailable

Never fabricate.

Never hallucinate.

Never derive
inside UI.

==============================================================================

24. ERROR STATE
==============================================================================

Display

Friendly explanation.

Retry action.

Diagnostic identifier.

==============================================================================

25. RESPONSIVE BEHAVIOUR
==============================================================================

Desktop

Continuous reading.

Tablet

Same hierarchy.

Mobile

Vertical stacking.

Reading order

never changes.

==============================================================================

26. ACCESSIBILITY
==============================================================================

Semantic headings.

Keyboard navigation.

Screen readers.

Visible focus.

ARIA labels.

Reduced Motion.

WCAG AA.

==============================================================================

27. PERFORMANCE BUDGET
==============================================================================

Initial render

<150 ms

Large analysis blocks

may lazy render.

Expand/Collapse

must remain responsive.

==============================================================================

28. COGNITIVE OUTCOME
==============================================================================

After reading

users should understand

why

the conclusion exists.

Users should be able

to explain

the reasoning

to another person.

==============================================================================

29. ANTI-PATTERNS
==============================================================================

Commercial UI V3 must never

✗ Display conclusion
without explanation.

✗ Display evidence
before explanation.

✗ Display rule
before evidence.

✗ Hide conclusion
inside expandable panels.

✗ Mix unrelated analyses
inside one block.

✗ Dump raw rules.

✗ Display engine names
to end users.

✗ Replace reasoning
with AI-generated prose.

==============================================================================

30. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Every conclusion
has explanation.

✓ Every explanation
has evidence.

✓ Every evidence
has rule reference.

✓ Confidence
is visible
when available.

✓ Knowledge
extends the explanation.

✓ Reading flow
remains consistent.

FAIL

✗ Conclusion
without explanation.

✗ Missing evidence.

✗ Missing rule reference.

✗ Dashboard appearance.

✗ Essay without structure.

✗ User cannot trace
the reasoning.

==============================================================================

31. FUTURE EXTENSIONS
==============================================================================

May support

Interactive rule tracing

Evidence comparison

Classical source explorer

AI discussion

without changing

Analysis Block Contract

or Reading Hierarchy.

==============================================================================

32. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Explainable Reading Experience

Component Hierarchy

Binding Contract

State Behaviour

Acceptance Rules

It does NOT define

HTML

CSS

React

Vue

Implementation technology.

==============================================================================

33. FREEZE
==============================================================================

After approval

Explainable Analysis
becomes the canonical
reasoning layer
of Commercial UI V3.

Every implementation

must preserve

Business Goal

Reading Goal

Analysis Block Contract

Information Priority

Binding Contract

and Explainable Reading Flow.

# ============================================================================
# END OF DOCUMENT
# ============================================================================