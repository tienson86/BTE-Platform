# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0004 — EXECUTIVE SUMMARY
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Work Package ID

WP-0004

Estimated Scope

Executive Summary Screen

Owner

Product Architecture

Executor

Cursor

==============================================================================
1. OBJECTIVE
==============================================================================

Implement

the Executive Summary Screen

according to

Commercial UI V3.

This is

the first

Business Screen

of the entire platform.

It establishes

the reading experience,

visual hierarchy,

and

consultation style

for every screen

that follows.

==============================================================================
2. BUSINESS GOAL
==============================================================================

Present

the most important conclusions

of the BaZi analysis

within

the first screen.

Users

must understand

the overall chart

without reading

the entire report.

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

01_EXECUTIVE_SUMMARY.md

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

==============================================================================

4. SCOPE
==============================================================================

IN SCOPE

Executive Hero

↓

Overall Verdict

↓

Primary Recommendation

↓

Executive Summary

↓

Glance Information

↓

Quick Highlights

↓

Section Transition

OUT OF SCOPE

Four Pillars

Executive Insight

Metrics

Analysis

Consultation Report

Appendix

Navigation

==============================================================================

5. COMPONENTS TO IMPLEMENT
==============================================================================

Business Components

ExecutiveHero

RecommendationPanel

ExecutiveOverview

ExecutiveHighlights

SummaryGlance

HeroBackground

HeroActions

Shared Components

SectionHeader

Callout

HighlightBox

MetricRow

StatusBadge

InformationBox

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

Order

Hero

↓

Primary Recommendation

↓

Executive Verdict

↓

Executive Summary

↓

Highlights

↓

Transition

Cards

must be minimized.

Whitespace

must define

hierarchy.

==============================================================================

7. READING EXPERIENCE
==============================================================================

Users

must complete

the Executive Summary

within

30–60 seconds.

Important information

must appear

above the fold.

Reading

must feel

like

an executive briefing,

not

a dashboard.

==============================================================================

8. DATA BINDING
==============================================================================

Components

must consume

Executive Summary

View Models only.

No component

may parse

raw payloads.

No component

may execute

business rules.

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

Screen Reader Support

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

Primary Layout

↓

Tablet

Single Column

↓

Mobile

Reading-first

The reading order

must remain identical.

==============================================================================

12. PERFORMANCE
==============================================================================

Initial rendering

must prioritize

Executive Summary.

The Hero

must render

before

secondary sections.

No blocking

charts

or

heavy rendering.

==============================================================================

13. STYLING
==============================================================================

Consume only

Design Tokens.

Forbidden

Hardcoded spacing

Hardcoded colors

Hardcoded typography

Hardcoded shadows

==============================================================================

14. VISUAL ACCEPTANCE
==============================================================================

Verify

Visual hierarchy

↓

Typography scale

↓

Spacing rhythm

↓

Whitespace

↓

Surface hierarchy

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

Executive Summary Screen

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

✓ Hero hierarchy preserved.

✓ Recommendation appears first.

✓ Typography matches Design System.

✓ Design Tokens only.

✓ Binding unchanged.

✓ Accessibility PASS.

✓ Responsive PASS.

✓ Performance PASS.

✓ Tests PASS.

FAIL

✗ Dashboard appearance.

✗ Excessive cards.

✗ Incorrect reading order.

✗ Payload parsing.

✗ Hardcoded styling.

✗ Modified business logic.

==============================================================================

18. ROLLBACK
==============================================================================

Rollback

must restore

the previous

Executive Summary

without

affecting

other screens.

==============================================================================

19. REQUIRED OUTPUT
==============================================================================

Cursor must provide

Implementation Summary

↓

Files Changed

↓

Components Created

↓

Visual Comparison

↓

Test Results

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

Visual Hierarchy

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

WP-0004 only.

Implement

Executive Summary Screen only.

Consume

Shared Components

from WP-0003.

Do not implement

Four Pillars

Metrics

Analysis

Navigation

Appendix

Do not modify

Backend

Bindings

Business Logic

Database

Return

1.

Files Changed

2.

Business Components Created

3.

Visual Comparison

4.

Accessibility Validation

5.

Performance Validation

6.

Acceptance Checklist

==============================================================================

22. FREEZE
==============================================================================

After approval,

WP-0004

becomes

Frozen.

Executive Summary

becomes

the canonical

Business Screen

reference

for every subsequent

Commercial UI V3 screen.

No redesign

is permitted

after Freeze.

# ============================================================================
# END OF DOCUMENT
# ============================================================================