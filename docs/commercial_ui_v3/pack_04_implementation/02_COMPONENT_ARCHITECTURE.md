# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 04 — IMPLEMENTATION SPECIFICATION
# 02_COMPONENT_ARCHITECTURE.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Related Documents

- 00_IMPLEMENTATION_PRINCIPLES.md
- 01_FOLDER_STRUCTURE.md
- Pack 03 Screen Specifications

==============================================================================
1. PURPOSE
==============================================================================

This document defines

the canonical component architecture

for Commercial UI V3.

Every UI element

must belong

to exactly one

architectural layer.

No component

may assume

multiple responsibilities.

==============================================================================

2. DESIGN GOALS
==============================================================================

The component architecture

must provide

• Single Responsibility

• Predictable Composition

• High Reusability

• Easy Testing

• Stable Binding

• Long-term Maintainability

==============================================================================

3. COMPONENT PHILOSOPHY
==============================================================================

Commercial UI V3

is built

from

small components

↓

composed

into

business components

↓

assembled

into

screens.

No component

implements

business logic.

==============================================================================

4. COMPONENT HIERARCHY
==============================================================================

Application

↓

Screen

↓

Layout

↓

Business Component

↓

Shared Component

↓

Base Component

This hierarchy

must never change.

==============================================================================

5. COMPONENT RESPONSIBILITY
==============================================================================

Application

Bootstraps

the application.

--------------------------------------------------

Screen

Owns

one screen only.

--------------------------------------------------

Layout

Defines

reading structure.

--------------------------------------------------

Business Component

Represents

a BaZi business concept.

--------------------------------------------------

Shared Component

Reusable

presentation logic.

--------------------------------------------------

Base Component

Primitive UI.

==============================================================================

6. SCREEN LAYER
==============================================================================

Each Screen

represents

one specification

from Pack 03.

Examples

ExecutiveSummaryScreen

FourPillarsScreen

ExecutiveInsightScreen

MetricsScreen

ExplainableAnalysisScreen

ConsultationReportScreen

AppendixScreen

NavigationScreen

ResponsiveLayoutScreen

A Screen

must never

contain

business calculations.

==============================================================================

7. LAYOUT LAYER
==============================================================================

Layouts

organize

content.

Examples

ReportLayout

ReadingLayout

SectionLayout

TwoColumnLayout

ResponsiveLayout

Layouts

must never

know

BaZi concepts.

==============================================================================

8. BUSINESS COMPONENT LAYER
==============================================================================

Business Components

represent

BaZi concepts.

Examples

ExecutiveHero

PillarColumn

AnalysisBlock

KnowledgeBlock

RecommendationPanel

ConfidenceIndicator

EvidencePanel

Business Components

consume

View Models only.

==============================================================================

9. SHARED COMPONENT LAYER
==============================================================================

Shared Components

are reusable.

Examples

Heading

SectionHeader

MetricRow

ProgressBar

Tooltip

Skeleton

Callout

ReferenceList

EmptyState

UnavailableState

==============================================================================

10. BASE COMPONENT LAYER
==============================================================================

Base Components

contain

primitive UI.

Examples

Button

Text

Badge

Divider

Icon

Spinner

Input

Link

CardSurface

No business meaning.

==============================================================================

11. COMPONENT TREE
==============================================================================

Application

└── ReportScreen

    └── ReportLayout

        ├── ExecutiveHero

        │   ├── RecommendationPanel

        │   ├── VerdictLabel

        │   ├── MetricRow

        │   └── SummaryText

        │

        ├── FourPillarsWorkspace

        │   ├── PillarColumn

        │   ├── StemBadge

        │   ├── BranchBadge

        │   └── HiddenStemGroup

        │

        ├── ExecutiveInsight

        │

        ├── MetricsWorkspace

        │

        ├── ExplainableAnalysis

        │

        ├── ConsultationReport

        │

        └── Appendix

==============================================================================

12. COMPONENT COMPOSITION
==============================================================================

Components

compose

downwards only.

Example

ExecutiveHero

↓

RecommendationPanel

↓

Heading

↓

Text

↓

Badge

Reverse composition

is forbidden.

==============================================================================

13. DATA OWNERSHIP
==============================================================================

Every Component

has

exactly one

owner.

Screens

own

Business Components.

Business Components

own

Shared Components.

Shared Components

own

Base Components.

==============================================================================

14. VIEW MODEL CONSUMPTION
==============================================================================

Business Components

consume

View Models.

Shared Components

consume

simple props.

Base Components

consume

primitive values.

==============================================================================

15. COMPONENT COMMUNICATION
==============================================================================

Allowed

Parent

↓

Child

Properties

Callbacks

Context

Forbidden

Sibling mutation

Global mutation

Hidden dependencies

==============================================================================

16. COMPONENT STATES
==============================================================================

Every Business Component

supports

Loading

↓

Ready

↓

Unavailable

↓

Empty

↓

Error

The state contract

is identical

across all screens.

==============================================================================

17. COMPONENT ISOLATION
==============================================================================

Every Component

must be

independently

renderable.

Every Component

must be

independently

testable.

==============================================================================

18. DEPENDENCY RULES
==============================================================================

Allowed

Screen

↓

Layout

↓

Business

↓

Shared

↓

Base

Forbidden

Base

↓

Business

Shared

↓

Screen

Circular imports

are prohibited.

==============================================================================

19. STYLING OWNERSHIP
==============================================================================

Every Component

owns

its own

presentation.

Components

must not

modify

styles

of sibling components.

==============================================================================

20. BINDING OWNERSHIP
==============================================================================

Components

never bind

payload directly.

Flow

Payload

↓

Adapter

↓

View Model

↓

Component

==============================================================================

21. EXTENSIBILITY
==============================================================================

New Components

must

fit

an existing layer.

New architectural layers

require

architecture review.

==============================================================================

22. COMPONENT NAMING
==============================================================================

Screens

ExecutiveSummaryScreen

Business Components

ExecutiveHero

Shared Components

SectionHeader

Base Components

Button

Hooks

useExecutiveSummary

Files

PascalCase

==============================================================================

23. FORBIDDEN PATTERNS
==============================================================================

Commercial UI V3

must never

✗ Components reading APIs.

✗ Components reading Rule Database.

✗ Components calculating metrics.

✗ Components mutating payload.

✗ Giant components.

✗ God components.

✗ Circular rendering.

✗ Deep inheritance.

==============================================================================

24. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ One responsibility.

✓ One owner.

✓ Downward dependencies.

✓ Stable View Models.

✓ Small reusable components.

✓ Easy testing.

FAIL

✗ Mixed responsibilities.

✗ Circular dependencies.

✗ Payload parsing inside UI.

✗ Business logic inside rendering.

✗ Oversized components.

==============================================================================

25. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Component Architecture

Composition

Ownership

Responsibilities

Dependency Rules

It does NOT define

React syntax

TypeScript syntax

CSS

Framework implementation.

==============================================================================

26. FREEZE
==============================================================================

After approval,

this component architecture

becomes

the canonical

frontend architecture

of Commercial UI V3.

Every implementation

must preserve

Layering

Responsibilities

Ownership

Dependency Rules

and

Composition Hierarchy.

# ============================================================================
# END OF DOCUMENT
# ============================================================================