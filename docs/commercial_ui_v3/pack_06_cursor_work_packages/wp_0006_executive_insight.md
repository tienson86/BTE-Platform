# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0006 — EXECUTIVE INSIGHT
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Work Package ID

WP-0006

Estimated Scope

Executive Insight Screen

Owner

Product Architecture

Executor

Cursor

==============================================================================
1. OBJECTIVE
==============================================================================

Implement

the Executive Insight Screen

according to

Commercial UI V3.

This screen

transforms

analytical results

into

high-level consulting insights.

It is

the bridge

between

raw BaZi analysis

and

professional interpretation.

==============================================================================

2. BUSINESS GOAL
==============================================================================

Provide

clear,

actionable,

executive-level

insights

that summarize

the user's chart

without requiring

deep technical knowledge.

Users

must understand

the major strengths,

risks,

and opportunities

within

2–3 minutes.

==============================================================================

3. REQUIRED SPECIFICATIONS
==============================================================================

Cursor MUST read

Pack 01

01_PRODUCT_VISION.md

02_INFORMATION_ARCHITECTURE.md

03_READING_JOURNEY.md

04_PAGE_LAYOUT.md

05_VISUAL_HIERARCHY.md

Pack 02

All Design System

Pack 03

03_EXECUTIVE_INSIGHT.md

09_RESPONSIVE_LAYOUTS.md

Pack 03.5

01_DESKTOP_WIREFRAMES.md

02_TABLET_WIREFRAMES.md

03_MOBILE_WIREFRAMES.md

05_READING_FLOW_VALIDATION.md

Pack 04

All Implementation Specifications

WP-0001

WP-0002

WP-0003

WP-0004

WP-0005

==============================================================================

4. SCOPE
==============================================================================

IN SCOPE

Executive Insight Header

↓

Overall Insight

↓

Personality Insight

↓

Career Insight

↓

Wealth Insight

↓

Relationship Insight

↓

Health Insight

↓

Opportunity Summary

↓

Risk Summary

↓

Recommended Focus

↓

Section Transition

OUT OF SCOPE

Metrics

Explainable Analysis

Consultation Report

Appendix

Navigation

==============================================================================

5. COMPONENTS TO IMPLEMENT
==============================================================================

Business Components

ExecutiveInsightHero

InsightSection

OpportunityPanel

RiskPanel

RecommendationPanel

InsightSummary

ExecutiveConclusion

Shared Components

SectionHeader

HighlightBox

Callout

InformationBox

EvidenceRow

ConfidenceBadge

StatusBadge

PropertyGrid

PropertyItem

ReadingProgress

Base Components

Consume only

WP-0002 components.

==============================================================================

6. LAYOUT REQUIREMENTS
==============================================================================

The screen

must follow

Commercial Report Layout V3.

Reading order

Section Title

↓

Executive Conclusion

↓

Key Insights

↓

Opportunity

↓

Risk

↓

Recommendations

↓

Transition

The layout

must feel

like

a consulting report,

not

a dashboard.

==============================================================================

7. READING EXPERIENCE
==============================================================================

Executive Insight

must support

continuous reading.

Each section

must begin

with

the conclusion,

followed by

supporting explanation.

Avoid

fragmented cards,

isolated widgets,

or

parallel reading paths.

==============================================================================

8. DATA BINDING
==============================================================================

Components

must consume

Executive Insight

View Models only.

Forbidden

Raw Payload

Business Calculation

Rule Evaluation

Knowledge Lookup

==============================================================================

9. STATE SUPPORT
==============================================================================

Every Business Component

must support

Loading

↓

Ready

↓

Empty

↓

Unavailable

↓

Error

according to

Presentation State Contract.

==============================================================================

10. ACCESSIBILITY
==============================================================================

Verify

Semantic Headings

↓

Logical Reading Order

↓

Keyboard Navigation

↓

Screen Reader Labels

↓

Focus Order

↓

Contrast

↓

Reduced Motion

==============================================================================

11. RESPONSIVE
==============================================================================

Desktop

Multi-section report

↓

Tablet

Stacked sections

↓

Mobile

Single-column reading

Reading order

must remain identical

across

all devices.

==============================================================================

12. PERFORMANCE
==============================================================================

Render

Executive Conclusion

before

secondary insights.

Do not

block rendering

with

non-critical content.

No layout shift.

==============================================================================

13. STYLING
==============================================================================

Consume only

Design Tokens.

Forbidden

Hardcoded spacing

Hardcoded colors

Hardcoded typography

Hardcoded elevation

==============================================================================

14. VISUAL VALIDATION
==============================================================================

Verify

Reading hierarchy

↓

Whitespace rhythm

↓

Typography hierarchy

↓

Section transitions

↓

Light Theme

↓

Dark Theme

==============================================================================

15. TESTING
==============================================================================

Execute

Build

↓

Lint

↓

Component Tests

↓

Binding Tests

↓

Accessibility Tests

↓

Responsive Tests

↓

Performance Tests

↓

Visual Regression

==============================================================================

16. DELIVERABLES
==============================================================================

Executive Insight Screen

↓

Business Components

↓

Styles

↓

Tests

↓

Documentation

↓

Visual Comparison

==============================================================================

17. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Reading Journey matches Pack 03.

✓ Executive Conclusion appears first.

✓ Insight hierarchy preserved.

✓ Recommendation section clearly separated.

✓ Design Tokens only.

✓ Binding unchanged.

✓ Accessibility PASS.

✓ Responsive PASS.

✓ Performance PASS.

✓ Tests PASS.

FAIL

✗ Dashboard appearance.

✗ Parallel reading layout.

✗ Excessive cards.

✗ Payload parsing.

✗ Hardcoded styling.

✗ Business logic inside Components.

==============================================================================

18. ROLLBACK
==============================================================================

Rollback

must restore

the previous

Executive Insight Screen

without

affecting

Executive Summary

or

Four Pillars.

==============================================================================

19. REQUIRED OUTPUT
==============================================================================

Cursor must provide

Implementation Summary

↓

Files Changed

↓

Business Components Created

↓

Visual Comparison

↓

Binding Validation

↓

Accessibility Report

↓

Performance Report

↓

Acceptance Checklist

==============================================================================

20. REVIEW CHECKLIST
==============================================================================

Architecture

□ PASS

Reading Journey

□ PASS

Executive Hierarchy

□ PASS

Design Tokens

□ PASS

Binding

□ PASS

Accessibility

□ PASS

Responsive

□ PASS

Performance

□ PASS

Testing

□ PASS

==============================================================================

21. EXECUTION PROMPT
==============================================================================

Implement

WP-0006 only.

Implement

Executive Insight Screen only.

Consume

Shared Components

from WP-0003.

Do not implement

Metrics

Explainable Analysis

Consultation Report

Appendix

Navigation

Do not modify

Backend

Bindings

Business Logic

Database

Analysis Engine

Return

1.

Files Changed

2.

Business Components Created

3.

Visual Comparison

4.

Binding Validation

5.

Accessibility Validation

6.

Performance Validation

7.

Acceptance Checklist

==============================================================================

22. REFERENCE SCREENSHOT CONTRACT (RSC)
==============================================================================

The implementation

must be validated

against

Approved Desktop Wireframe

↓

Approved Tablet Wireframe

↓

Approved Mobile Wireframe

↓

Pack 03 Screen Specification

↓

Commercial UI V3 Visual Hierarchy

No layout deviation

is permitted

without

Product Architecture approval.

==============================================================================

23. EXECUTIVE INSIGHT CONTRACT (EIC)
==============================================================================

Every Insight

must follow

the same structure

Conclusion

↓

Explanation

↓

Evidence Reference

↓

Confidence

↓

Recommendation

Business Components

must never

change

this sequence.

==============================================================================

24. FREEZE
==============================================================================

After approval,

WP-0006

becomes

Frozen.

Executive Insight

becomes

the canonical

consulting insight screen

for Commercial UI V3.

No redesign

is permitted

after Freeze.

# ============================================================================
# END OF DOCUMENT
# ============================================================================