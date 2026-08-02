# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03
# SCREEN SPECIFICATION
# README.md
# ============================================================================

Version : 1.0.0

Status : Foundation

Owner : Product Architecture

------------------------------------------------------------------------------

# 1. PURPOSE

Pack 03 defines the complete Screen Specification
for Commercial UI V3.

If

Pack 01 answers

"What product should be built?"

and

Pack 02 answers

"How the design system works?"

then

Pack 03 answers

"What exactly does every screen look like?"

This pack is the UI Contract
between Product,
Design,
Frontend,
QA,
and AI-assisted implementation.

------------------------------------------------------------------------------

# 2. POSITION IN THE ARCHITECTURE

Commercial UI V3

↓

Pack 01

Foundation

↓

Pack 02

Design System

↓

Pack 03

Screen Specification

↓

Pack 04

Implementation Rules

Pack 03 translates

Business Goals

↓

Reading Goals

↓

Design System

↓

Concrete Screens

------------------------------------------------------------------------------

# 3. PHILOSOPHY

Commercial UI V3 does not design pages.

Commercial UI V3 designs

Reading Experiences.

Every screen exists
to answer one user question.

Screens are organized
according to

Reading Journey,

not

Application Navigation.

------------------------------------------------------------------------------

# 4. OBJECTIVES

Pack 03 has five objectives.

1.

Define every screen completely.

2.

Prevent implementation guessing.

3.

Guarantee UI consistency.

4.

Guarantee Reading Journey.

5.

Provide implementation contracts.

------------------------------------------------------------------------------

# 5. WHAT THIS PACK DEFINES

Pack 03 defines

✓ Business Goal

✓ User Goal

✓ Reading Goal

✓ Information Priority

✓ Layout

✓ Component Composition

✓ Grid

✓ Spacing

✓ Typography Roles

✓ Color Intent

✓ Surface Roles

✓ Motion Intent

✓ Binding Index

✓ Loading State

✓ Empty State

✓ Unavailable State

✓ Error State

✓ Responsive Behavior

✓ Accessibility

✓ Performance

✓ Acceptance Criteria

------------------------------------------------------------------------------

# 6. WHAT THIS PACK DOES NOT DEFINE

Pack 03 does NOT define

Business Logic

Rule Engine

API

Database

Calculation

Interpretation Logic

Knowledge Engine

Those belong
to other architecture packs.

------------------------------------------------------------------------------

# 7. DOCUMENT STRUCTURE

Every Screen Specification
uses exactly the same structure.

Business Goal

↓

User Goal

↓

Reading Goal

↓

Information Priority

↓

ASCII Layout

↓

Grid

↓

Spacing

↓

Typography Roles

↓

Color Intent

↓

Surface Roles

↓

Motion Intent

↓

Binding

↓

States

↓

Responsive

↓

Accessibility

↓

Acceptance

Every screen
must follow
this contract.

------------------------------------------------------------------------------

# 8. SCREEN LIST

00_SCREEN_SPEC_STANDARD.md

Defines
the mandatory specification template.

--------------------------------------------------

01_EXECUTIVE_HERO.md

Executive summary
of the BaZi chart.

--------------------------------------------------

02_FOUR_PILLARS.md

Interactive BaZi chart.

--------------------------------------------------

03_EXECUTIVE_INSIGHT.md

Strengths,
weaknesses,
opportunities,
risks.

--------------------------------------------------

04_VISUAL_ANALYTICS.md

Metrics
and supporting visualizations.

--------------------------------------------------

05_EXPLAINABLE_ANALYSIS.md

Evidence-driven analysis.

--------------------------------------------------

06_CONSULTATION_REPORT.md

Professional consultation report.

--------------------------------------------------

07_KNOWLEDGE_WORKSPACE.md

Knowledge,
citations,
classical references.

--------------------------------------------------

08_NAVIGATION.md

Navigation,
Rail,
TOC,
Reading Progress.

--------------------------------------------------

09_RESPONSIVE_LAYOUTS.md

Desktop,
Laptop,
Tablet,
Mobile.

--------------------------------------------------

10_PRINT_REPORT.md

Printable consultation document.

------------------------------------------------------------------------------

# 9. IMPLEMENTATION ORDER

The implementation order
must always follow
the Reading Journey.

Executive Hero

↓

Four Pillars

↓

Executive Insight

↓

Visual Analytics

↓

Explainable Analysis

↓

Consultation Report

↓

Knowledge Workspace

↓

Navigation

↓

Responsive

↓

Print

Never implement
out of sequence.

------------------------------------------------------------------------------

# 10. DEPENDENCIES

Each Screen Specification
depends on

Visual Language

↓

Design Tokens

↓

Grid System

↓

Spacing System

↓

Typography System

↓

Color System

↓

Surface System

↓

Motion System

↓

Component Principles

No screen
may redefine
the Design System.

------------------------------------------------------------------------------

# 11. IMPLEMENTATION RULES

Frontend SHALL NOT

Invent layouts.

Invent spacing.

Invent typography.

Invent components.

Invent loading states.

Invent empty states.

Invent interactions.

Everything
must follow
the Screen Specification.

------------------------------------------------------------------------------

# 12. REVIEW PROCESS

Every Screen Specification
must be reviewed by

Product

↓

UX

↓

Frontend

↓

QA

↓

Architecture

Only then

may implementation begin.

------------------------------------------------------------------------------

# 13. ACCEPTANCE

Pack 03 passes only when

Every screen
can be implemented
without guessing.

Every screen
preserves
the Reading Journey.

Every screen
consumes
Design Tokens.

Every screen
binds only
to defined payloads.

Every screen
has complete
acceptance criteria.

------------------------------------------------------------------------------

# 14. FREEZE

After approval,

Pack 03 becomes
the official UI Contract
of Commercial UI V3.

No implementation
may bypass
or reinterpret
this specification.

All future UI work
must conform
to this pack.

# ============================================================================
# END
# ============================================================================