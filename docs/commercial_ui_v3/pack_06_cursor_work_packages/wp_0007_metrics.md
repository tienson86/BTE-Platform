# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0007 — METRICS
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : HIGH

Work Package ID

WP-0007

Estimated Scope

Metrics Screen

Owner

Product Architecture

Executor

Cursor

==============================================================================
1. OBJECTIVE
==============================================================================

Implement

the Metrics Screen

according to

Commercial UI V3.

This screen

transforms

analytical scores

into

supporting evidence

for

professional consultation.

Metrics

exist

to reinforce

interpretation,

not

to dominate

the reading experience.

==============================================================================
2. BUSINESS GOAL
==============================================================================

Present

quantitative indicators

that support

Executive Insight.

Users

must understand

the meaning

of each metric

without

having to interpret

charts.

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

04_METRICS.md

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

WP-0006

==============================================================================
4. SCOPE
==============================================================================

IN SCOPE

Metrics Header

↓

Executive Metrics Summary

↓

Strength Metrics

↓

Five Elements Metrics

↓

Ten Gods Metrics

↓

Balance Indicators

↓

Confidence Indicators

↓

Metric Explanations

↓

Section Transition

OUT OF SCOPE

Explainable Analysis

Consultation Report

Appendix

Navigation

==============================================================================
5. COMPONENTS TO IMPLEMENT
==============================================================================

Business Components

MetricsSummary

MetricSection

MetricCard

MetricIndicator

MetricExplanation

ConfidencePanel

BalancePanel

Shared Components

SectionHeader

MetricRow

MetricGroup

PropertyGrid

LabelValueRow

Callout

InformationBox

StatusBadge

ConfidenceBadge

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

Executive Metrics Summary

↓

Metric Explanation

↓

Supporting Indicators

↓

Confidence

↓

Transition

Charts

must remain

secondary.

Narrative

must remain

primary.

==============================================================================
7. VISUAL REQUIREMENTS
==============================================================================

Metrics

must support

the narrative.

Do not

create

dashboard layouts.

Avoid

large KPI tiles,

multiple columns

of equal importance,

or

dense chart grids.

Whitespace

must separate

ideas,

not

widgets.

==============================================================================
8. DATA BINDING
==============================================================================

Components

must consume

Metrics View Models only.

Forbidden

Raw Payload

Business Calculation

Rule Evaluation

Knowledge Lookup

Chart Calculations

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

Keyboard Navigation

↓

Logical Reading Order

↓

Screen Reader Labels

↓

Chart Alternatives

↓

Contrast

↓

Reduced Motion

Every chart

must have

an equivalent

text explanation.

==============================================================================
11. RESPONSIVE
==============================================================================

Desktop

Narrative-first layout

↓

Tablet

Stacked metric groups

↓

Mobile

Single-column reading

Reading order

must remain

identical

across

all devices.

==============================================================================
12. PERFORMANCE
==============================================================================

Render

Executive Metrics Summary

before

charts.

Lazy-render

non-critical

visualizations.

Avoid

layout shift.

==============================================================================
13. STYLING
==============================================================================

Consume only

Design Tokens.

Forbidden

Hardcoded colors

Hardcoded spacing

Hardcoded typography

Hardcoded chart palettes

==============================================================================

14. VISUAL VALIDATION
==============================================================================

Verify

Narrative hierarchy

↓

Metric hierarchy

↓

Whitespace rhythm

↓

Chart proportion

↓

Typography

↓

Dark Theme

↓

Light Theme

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

Metrics Screen

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

✓ Narrative remains primary.

✓ Metrics support conclusions.

✓ Charts remain secondary.

✓ Design Tokens only.

✓ Binding unchanged.

✓ Accessibility PASS.

✓ Responsive PASS.

✓ Performance PASS.

✓ Tests PASS.

FAIL

✗ Dashboard appearance.

✗ KPI-first layout.

✗ Large widget grids.

✗ Hardcoded styling.

✗ Payload parsing.

✗ Business logic inside Components.

==============================================================================

18. ROLLBACK
==============================================================================

Rollback

must restore

the previous

Metrics Screen

without

affecting

Executive Insight

or

Explainable Analysis.

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

Narrative Hierarchy

□ PASS

Metric Hierarchy

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

WP-0007 only.

Implement

Metrics Screen only.

Consume

Shared Components

from WP-0003.

Do not implement

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

22. METRIC PRESENTATION CONTRACT (MPC)
==============================================================================

Every metric

must follow

the sequence

Metric

↓

Meaning

↓

Supporting Explanation

↓

Confidence

↓

Related Recommendation

Metrics

must never

appear

without

context.

Charts

must never

replace

written explanations.

==============================================================================

23. REFERENCE SCREENSHOT CONTRACT (RSC)
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

24. FREEZE
==============================================================================

After approval,

WP-0007

becomes

Frozen.

The Metrics Screen

becomes

the canonical

metric presentation

for Commercial UI V3.

No redesign

is permitted

after Freeze.

# ============================================================================
# END OF DOCUMENT
# ============================================================================