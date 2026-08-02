# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 05 — EXECUTION PLAN
# 03_COMPONENT_MIGRATION.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Related Documents

Pack 02 Design System

Pack 03 Screen Specification

Pack 04 Component Architecture

01_IMPLEMENTATION_PHASES.md

==============================================================================
1. PURPOSE
==============================================================================

This document defines

the official

Component Migration Strategy

for Commercial UI V3.

Migration

must replace

legacy presentation

without

changing

Business Behaviour,

Binding Contracts,

or

Reading Experience.

==============================================================================

2. COMPONENT MIGRATION PHILOSOPHY
==============================================================================

Commercial UI V3

does not

rewrite components.

Commercial UI V3

migrates

components

progressively.

Every migration

must preserve

Business Meaning.

==============================================================================

3. MIGRATION PRINCIPLES
==============================================================================

Each component

must be

Migrated

↓

Reviewed

↓

Verified

↓

Frozen

No component

may bypass

this lifecycle.

==============================================================================

4. MIGRATION ORDER
==============================================================================

Base Components

↓

Shared Components

↓

Business Components

↓

Screen Composition

↓

Legacy Removal

The order

must never

be reversed.

==============================================================================

5. BASE COMPONENT MIGRATION
==============================================================================

Objectives

Replace

primitive UI

with

Commercial UI V3

Base Components.

Examples

Button

↓

BaseButton

Divider

↓

BaseDivider

Badge

↓

BaseBadge

Spinner

↓

BaseSpinner

Acceptance

Visual behaviour

must remain

consistent.

==============================================================================

6. SHARED COMPONENT MIGRATION
==============================================================================

Objectives

Replace

generic reusable

presentation.

Examples

Section Header

↓

SharedSectionHeader

Metric Row

↓

SharedMetricRow

Tooltip

↓

SharedTooltip

Callout

↓

SharedCallout

Acceptance

Shared Components

must remain

framework-independent.

==============================================================================

7. BUSINESS COMPONENT MIGRATION
==============================================================================

Objectives

Replace

legacy BaZi UI

with

Commercial Components.

Examples

Executive Hero

↓

BusinessExecutiveHero

Pillar Column

↓

BusinessPillarColumn

Analysis Block

↓

BusinessAnalysisBlock

Knowledge Block

↓

BusinessKnowledgeBlock

Acceptance

Business Components

consume

View Models only.

==============================================================================

8. SCREEN COMPOSITION
==============================================================================

After

Business Components

are complete,

compose

Commercial Screens.

Screen Assembly

must not

introduce

new business logic.

==============================================================================

9. COMPONENT COMPATIBILITY
==============================================================================

Every migrated component

must remain

compatible

with

existing

Binding Contracts.

Adapters

must isolate

payload changes.

==============================================================================

10. LEGACY COMPONENTS
==============================================================================

Legacy Components

remain

temporarily

during migration.

Legacy removal

is allowed

only after

Acceptance Review.

==============================================================================

11. COMPONENT MAPPING
==============================================================================

Every migrated component

must maintain

a mapping.

Legacy Component

↓

Commercial Component

↓

Specification

↓

Migration Phase

==============================================================================

12. COMPONENT DEPENDENCIES
==============================================================================

Dependencies

must remain

top-down.

Business

↓

Shared

↓

Base

Reverse dependencies

are forbidden.

==============================================================================

13. COMPONENT VERIFICATION
==============================================================================

Every migrated component

must verify

Binding

↓

Rendering

↓

Accessibility

↓

Responsive

↓

Performance

↓

Visual Consistency

==============================================================================

14. COMPONENT TESTING
==============================================================================

Every migrated component

must provide

Unit Tests

↓

Rendering Tests

↓

Accessibility Tests

↓

Visual Regression

↓

Responsive Tests

==============================================================================

15. COMPONENT REVIEW
==============================================================================

Review

must verify

Architecture

↓

Naming

↓

Bindings

↓

Tokens

↓

States

↓

Reading Behaviour

==============================================================================

16. COMPONENT FREEZE
==============================================================================

Approved Components

become

Frozen.

Frozen Components

accept only

Bug Fixes

Accessibility Fixes

Performance Improvements

No redesign.

==============================================================================

17. LEGACY REMOVAL
==============================================================================

Legacy Components

may be removed

only when

Commercial Components

have passed

Acceptance

and

Regression Testing.

==============================================================================

18. ROLLBACK
==============================================================================

Every migration

must support

rollback

to

Legacy Components.

Rollback

must not

affect

other migrated components.

==============================================================================

19. MIGRATION TRACEABILITY
==============================================================================

Every migrated component

must reference

Legacy Component

↓

Specification

↓

Acceptance Report

↓

Replacement Commit

Traceability

must remain

bidirectional.

==============================================================================

20. FORBIDDEN PRACTICES
==============================================================================

Commercial UI V3

must never

✗ Rewrite multiple component layers together.

✗ Merge unrelated Business Components.

✗ Break Binding Contracts.

✗ Remove Legacy Components

before approval.

✗ Change Design Tokens

during migration.

✗ Introduce temporary UI.

==============================================================================

21. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Legacy mapping complete.

✓ New Component implemented.

✓ Binding preserved.

✓ Accessibility verified.

✓ Responsive verified.

✓ Tests passed.

✓ Visual comparison approved.

✓ Legacy safely removable.

FAIL

✗ Missing mapping.

✗ Broken bindings.

✗ Changed reading behaviour.

✗ Untested migration.

✗ Mixed legacy and commercial styles.

==============================================================================

22. IMPLEMENTATION NOTES
==============================================================================

This document defines

Component Migration

Execution Rules

Verification

Rollback

Acceptance

It does NOT define

React implementation,

CSS implementation,

or

Business Logic.

==============================================================================

23. FINAL DECLARATION
==============================================================================

Commercial UI V3

evolves

through

controlled component migration.

Every migrated component

must improve

implementation quality

while

preserving

approved specifications.

==============================================================================

24. FREEZE
==============================================================================

After approval,

this document

becomes

the canonical

Component Migration Strategy

for Commercial UI V3.

Every migration

must comply

with

the rules

defined herein.

# ============================================================================
# END OF DOCUMENT
# ============================================================================