# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03 — SCREEN SPECIFICATION
# 01_EXECUTIVE_SUMMARY.md
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

Executive Summary is the first screen
users encounter after a BaZi chart is generated.

Its objective is NOT to display data.

Its objective is to answer
the three most important questions
before the user starts reading
the complete report.

The Executive Summary determines
the user's first impression
of the entire platform.

==============================================================================

2. USER GOAL
==============================================================================

Within the first few seconds
users should understand

• Who am I?

• Is this chart generally favorable or challenging?

• What should I pay attention to first?

Users should feel

Confident

↓

Guided

↓

Interested to continue reading.

==============================================================================

3. READING GOAL
==============================================================================

After reading this section
users should know

✓ Day Master

✓ Overall Verdict

✓ Primary Recommendation

✓ Overall Strength

✓ Most important opportunity

✓ Most important risk

without needing
to scroll further.

==============================================================================

4. SUCCESS CRITERIA
==============================================================================

Executive Summary succeeds only when

Users answer correctly

Who am I?

↓

Overall Quality?

↓

First Recommendation?

within

5–10 seconds.

==============================================================================

5. USER QUESTIONS ANSWERED
==============================================================================

The screen explicitly answers

Q1

Who am I?

↓

Day Master

Identity

Q2

Is this chart good?

↓

Overall Verdict

Q3

What should I do first?

↓

Primary Recommendation

Q4

What is my strongest advantage?

↓

Strength Highlight

Q5

What is the biggest risk?

↓

Risk Highlight

==============================================================================

6. INFORMATION PRIORITY
==============================================================================

Priority 0

Identity

--------------------------------------------------

Priority 1

Overall Verdict

--------------------------------------------------

Priority 2

Primary Recommendation

--------------------------------------------------

Priority 3

Strength / Weakness Summary

--------------------------------------------------

Priority 4

Metrics

--------------------------------------------------

Priority 5

Metadata

==============================================================================

7. EXPECTED READING TIME
==============================================================================

5–10 seconds

This screen must support

glance reading.

==============================================================================

8. ASCII LAYOUT
==============================================================================

+--------------------------------------------------------------+

Executive Summary

--------------------------------------------------------------

Day Master

Overall Verdict

--------------------------------------------------------------

Primary Recommendation

--------------------------------------------------------------

Strength Summary

Weakness Summary

--------------------------------------------------------------

Executive Metrics

--------------------------------------------------------------

Continue Reading

+--------------------------------------------------------------+

==============================================================================

9. COMPONENT TREE
==============================================================================

ExecutiveSummary

├── DayMasterIdentity

├── OverallVerdict

├── RecommendationPanel

├── StrengthSummary

├── WeaknessSummary

├── ExecutiveMetricRow

└── ContinueReadingHint

==============================================================================

10. GRID MAPPING
==============================================================================

Desktop

Reading Width

Tablet

Reading Width

Mobile

Single Column

==============================================================================

11. SPACING MAPPING
==============================================================================

Uses

space.chapter

↓

space.section

↓

space.block

↓

space.inline

No custom spacing.

==============================================================================

12. TYPOGRAPHY ROLES
==============================================================================

Identity

↓

Decision

↓

Recommendation

↓

Explanation

↓

Metadata

==============================================================================

13. COLOR INTENT
==============================================================================

Identity

Decision

Recommendation

Explanation

Metadata

Only semantic colors
may be used.

==============================================================================

14. SURFACE ROLE
==============================================================================

Reading Surface

Recommendation Surface

No Card Grid.

No Dashboard Panels.

==============================================================================

15. MOTION INTENT
==============================================================================

Guide

Reveal

Focus

Only subtle transitions.

==============================================================================

16. INTERACTION RULES
==============================================================================

Hover

Optional

Keyboard

Supported

Touch

Supported

No hidden interactions.

==============================================================================

17. BINDING CONTRACT
==============================================================================

Consumes only

report.summary

report.identity

report.metrics

report.recommendation

Missing fields

↓

Unavailable

Never infer values.

==============================================================================

18. DATA DEPENDENCIES
==============================================================================

Required

Day Master

Overall Verdict

Recommendation

Metrics

Optional

Confidence

Knowledge Reference

==============================================================================

19. LOADING STATE
==============================================================================

Display

Hero Skeleton

Metric Skeleton

Recommendation Skeleton

Layout
must remain stable.

==============================================================================

20. EMPTY STATE
==============================================================================

Display

"No Executive Summary available."

Provide

Retry

or

Return to Analysis.

==============================================================================

21. UNAVAILABLE STATE
==============================================================================

Unavailable values
display

Unavailable

Never

null

undefined

0

or

placeholder text.

==============================================================================

22. ERROR STATE
==============================================================================

Display

Friendly explanation.

Retry button.

Diagnostic ID.

==============================================================================

23. RESPONSIVE BEHAVIOUR
==============================================================================

Desktop

Horizontal emphasis.

Tablet

Compressed spacing.

Mobile

Single-column reading.

Business meaning

never changes.

==============================================================================

24. ACCESSIBILITY
==============================================================================

Keyboard navigation.

Screen reader labels.

Semantic headings.

Visible focus.

WCAG AA.

==============================================================================

25. PERFORMANCE BUDGET
==============================================================================

First Paint

< 1 second

No layout shift.

Minimal DOM.

==============================================================================

26. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ User identifies Day Master.

✓ User understands Overall Verdict.

✓ Recommendation is immediately visible.

✓ Reading time under 10 seconds.

✓ Reading hierarchy is obvious.

✓ Layout feels like
a consultation report.

FAIL

✗ User scrolls before understanding.

✗ Metrics dominate content.

✗ Dashboard appearance.

✗ Recommendation hidden.

✗ Identity unclear.

==============================================================================

27. FUTURE EXTENSIONS
==============================================================================

May support

AI Executive Summary

Voice Summary

Video Summary

Personalized Greeting

without changing
the layout contract.

==============================================================================

28. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Reading Experience

Layout

Binding

States

Acceptance

It does NOT define

HTML

CSS

React

Vue

Implementation technology.

==============================================================================

29. FREEZE
==============================================================================

After approval

Executive Summary
becomes the canonical first screen
of Commercial UI V3.

Every implementation

must follow
this specification.

No implementation
may alter

Business Goal

Reading Goal

Information Priority

or

Binding Contract.

# ============================================================================
# END OF DOCUMENT
# ============================================================================