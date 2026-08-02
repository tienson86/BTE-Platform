# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03 — SCREEN SPECIFICATION
# 03_EXECUTIVE_INSIGHT.md
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

Executive Insight is the bridge

between

Raw Analysis

and

Professional Consultation.

Its objective is to transform
hundreds of analytical results

into

a small number
of high-value conclusions
that users can understand immediately.

The screen should answer

"What matters most?"

==============================================================================
2. USER GOAL
==============================================================================

Users want to know

• What are my greatest strengths?

• What are my biggest weaknesses?

• Where are my opportunities?

• What risks require attention?

• What should I remember first?

Users do not want
to read detailed rules yet.

==============================================================================
3. READING GOAL
==============================================================================

After reading this screen
users should understand

✓ Core Strengths

✓ Core Weaknesses

✓ Opportunities

✓ Risks

✓ Strategic Recommendation

The user should finish this section
with a mental model
of the chart.

==============================================================================
4. SUCCESS CRITERIA
==============================================================================

Executive Insight succeeds only when

users can summarize
their chart

in one minute

without opening
the detailed analysis.

==============================================================================
5. USER QUESTIONS ANSWERED
==============================================================================

Q1

What am I naturally good at?

↓

Strength Summary

--------------------------------------------------

Q2

What is my biggest challenge?

↓

Weakness Summary

--------------------------------------------------

Q3

Where should I focus?

↓

Opportunity

--------------------------------------------------

Q4

What should I avoid?

↓

Risk

--------------------------------------------------

Q5

What is my overall strategy?

↓

Executive Recommendation

==============================================================================
6. INFORMATION PRIORITY
==============================================================================

Priority 0

Executive Recommendation

--------------------------------------------------

Priority 1

Strength Summary

--------------------------------------------------

Priority 2

Weakness Summary

--------------------------------------------------

Priority 3

Opportunity

--------------------------------------------------

Priority 4

Risk

--------------------------------------------------

Priority 5

Supporting Insight

==============================================================================
7. EXPECTED READING TIME
==============================================================================

30–60 seconds

This section supports

executive reading.

Not detailed study.

==============================================================================
8. ASCII LAYOUT
==============================================================================

+------------------------------------------------------------------+

EXECUTIVE INSIGHT

--------------------------------------------------------------------

Primary Recommendation

--------------------------------------------------------------------

Strength Summary

--------------------------------------------------------------------

Weakness Summary

--------------------------------------------------------------------

Opportunity

--------------------------------------------------------------------

Risk

--------------------------------------------------------------------

Supporting Insight

+------------------------------------------------------------------+

==============================================================================
9. COMPONENT TREE
==============================================================================

ExecutiveInsight

├── ExecutiveRecommendation

├── StrengthSummary

├── WeaknessSummary

├── OpportunitySummary

├── RiskSummary

└── SupportingInsight

==============================================================================
10. GRID MAPPING
==============================================================================

Desktop

Single Reading Column

Tablet

Single Reading Column

Mobile

Single Reading Column

Multi-column layouts

are forbidden.

==============================================================================
11. SPACING MAPPING
==============================================================================

Uses only

Spacing Tokens

space.chapter

↓

space.section

↓

space.block

==============================================================================

12. TYPOGRAPHY ROLES
==============================================================================

Executive Recommendation

↓

Insight Heading

↓

Summary

↓

Supporting Text

↓

Metadata

==============================================================================

13. COLOR INTENT
==============================================================================

Recommendation

↓

Strength

↓

Risk

↓

Neutral Explanation

Only semantic color tokens
may be used.

==============================================================================

14. SURFACE ROLE
==============================================================================

One continuous Reading Surface.

Insight sections

must feel like

chapters

not cards.

==============================================================================

15. MOTION INTENT
==============================================================================

Guide

↓

Reveal

↓

Focus

No decorative animation.

==============================================================================

16. INTERACTION RULES
==============================================================================

Hover

Optional.

Keyboard

Supported.

Touch

Supported.

Expand

only for
supporting explanation.

==============================================================================

17. BINDING CONTRACT
==============================================================================

Consumes only

report.executive_insight

report.recommendation

report.strength_summary

report.weakness_summary

report.opportunity

report.risk

Presentation only.

Never calculate.

Never summarize
inside UI.

==============================================================================

18. DATA DEPENDENCIES
==============================================================================

Required

Recommendation

Strength

Weakness

Optional

Opportunity

Risk

Supporting Insight

==============================================================================

19. LOADING STATE
==============================================================================

Display

Executive Summary Skeleton

Maintain

identical layout.

==============================================================================

20. EMPTY STATE
==============================================================================

Display

"No executive insight available."

Provide

Retry

or

Return to Analysis.

==============================================================================

21. UNAVAILABLE STATE
==============================================================================

Unavailable fields

display

Unavailable

Never display

null

undefined

raw i18n keys

or fabricated content.

==============================================================================

22. ERROR STATE
==============================================================================

Display

Friendly explanation.

Retry.

Diagnostic identifier.

==============================================================================

23. RESPONSIVE BEHAVIOUR
==============================================================================

Desktop

Reading Width

Tablet

Reading Width

Mobile

Full Width

Reading sequence

never changes.

==============================================================================

24. ACCESSIBILITY
==============================================================================

Semantic headings.

Keyboard navigation.

Visible focus.

Screen reader labels.

WCAG AA compliance.

==============================================================================

25. PERFORMANCE BUDGET
==============================================================================

Render

<100 ms

No layout shift.

Minimal DOM depth.

==============================================================================

26. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Recommendation appears first.

✓ User understands strengths.

✓ User understands weaknesses.

✓ Opportunities are clear.

✓ Risks are clear.

✓ Reading completes
within one minute.

✓ Feels like
an executive briefing.

FAIL

✗ Dashboard appearance.

✗ Competing cards.

✗ Charts dominate.

✗ Recommendation buried.

✗ User cannot summarize
their chart.

==============================================================================

27. FUTURE EXTENSIONS
==============================================================================

May support

AI Executive Insight

Trend Comparison

Historical Snapshot

Personalized Action Plan

without changing

Business Goal

Reading Order

or Binding Contract.

==============================================================================

28. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Reading Experience

Component Hierarchy

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

Executive Insight
becomes the canonical
high-level interpretation layer
of Commercial UI V3.

Every implementation

must preserve

Business Goal

Reading Goal

Information Priority

Reading Hierarchy

and Binding Contract.

# ============================================================================
# END OF DOCUMENT
# ============================================================================