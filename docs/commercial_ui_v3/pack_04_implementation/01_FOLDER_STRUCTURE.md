# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 04 — IMPLEMENTATION SPECIFICATION
# 01_FOLDER_STRUCTURE.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Related Documents

- 00_IMPLEMENTATION_PRINCIPLES.md
- Pack 02 Design System
- Pack 03 Screen Specifications

==============================================================================
1. PURPOSE
==============================================================================

This document defines

the canonical frontend
folder structure

for Commercial UI V3.

Every source file

must belong

to exactly one

architectural layer.

Folder structure

is part of

the architecture.

It is not

an implementation preference.

==============================================================================

2. DESIGN GOALS
==============================================================================

The folder structure must provide

• Predictable organization

• Clear ownership

• Separation of concerns

• Easy navigation

• Scalability

• Long-term maintainability

Every developer

must locate

any file

within seconds.

==============================================================================

3. ARCHITECTURE OVERVIEW
==============================================================================

Commercial UI V3

uses

Layered Architecture.

Presentation

↓

Layout

↓

Business Components

↓

Shared Components

↓

Utilities

↓

Infrastructure

Each layer

depends only

on lower layers.

==============================================================================

4. ROOT STRUCTURE
==============================================================================

applications/

└── customer_portal/

    ├── static/

    ├── templates/

    ├── src/

    ├── tests/

    ├── assets/

    ├── locales/

    └── docs/

All implementation

belongs inside

src/.

==============================================================================

5. SOURCE STRUCTURE
==============================================================================

src/

├── app/

├── screens/

├── layouts/

├── components/

├── bindings/

├── view_models/

├── hooks/

├── services/

├── styles/

├── tokens/

├── icons/

├── assets/

├── utils/

├── constants/

├── types/

└── index.*

Each folder

has one responsibility.

==============================================================================

6. APP LAYER
==============================================================================

app/

contains

Application Bootstrap

Global Providers

Application Configuration

Routing

Theme Initialization

No business rendering.

==============================================================================

7. SCREENS
==============================================================================

screens/

contains

top-level report screens.

Examples

ExecutiveSummary

FourPillars

ExecutiveInsight

Metrics

ExplainableAnalysis

ConsultationReport

Appendix

Navigation

ResponsiveLayout

Screens

compose

Business Components.

==============================================================================

8. LAYOUTS
==============================================================================

layouts/

contains

Page Layouts

Report Layout

Reading Layout

Responsive Layout

Section Layout

Layouts

never

render

business meaning.

==============================================================================

9. COMPONENTS
==============================================================================

components/

contains

all reusable UI components.

Structure

components/

├── base/

├── shared/

├── business/

├── navigation/

├── charts/

├── document/

└── feedback/

Business logic

is forbidden.

==============================================================================

10. BASE COMPONENTS
==============================================================================

base/

contains

Button

Text

Heading

Card

Badge

Divider

Spinner

Skeleton

Icon

No business knowledge.

==============================================================================

11. SHARED COMPONENTS
==============================================================================

shared/

contains

generic reusable components.

Examples

SectionHeader

MetricRow

ReadingProgress

Callout

Tooltip

EmptyState

UnavailableState

==============================================================================

12. BUSINESS COMPONENTS
==============================================================================

business/

contains

BaZi-specific components.

Examples

ExecutiveHero

PillarColumn

AnalysisBlock

KnowledgeBlock

RecommendationPanel

Only presentation.

Never calculations.

==============================================================================

13. DOCUMENT COMPONENTS
==============================================================================

document/

contains

TableOfContents

Chapter

Citation

ReferenceList

ReadingProgress

DocumentFooter

==============================================================================

14. CHART COMPONENTS
==============================================================================

charts/

contains

SVG-based visualization.

Examples

Gauge

Radar

Distribution

ElementChart

TenGodChart

Charts

consume

View Models only.

==============================================================================

15. NAVIGATION COMPONENTS
==============================================================================

navigation/

contains

Reading Rail

Scroll Spy

Outline

Anchor

Drawer

Progress

==============================================================================

16. FEEDBACK COMPONENTS
==============================================================================

feedback/

contains

Loading

Empty

Unavailable

Error

Toast

Alert

==============================================================================

17. VIEW MODELS
==============================================================================

view_models/

contains

UI-ready models.

Examples

ExecutiveSummaryViewModel

MetricsViewModel

AnalysisViewModel

No rendering.

No HTML.

==============================================================================

18. BINDINGS
==============================================================================

bindings/

maps

payload

↓

View Models.

Bindings

never render.

==============================================================================

19. SERVICES
==============================================================================

services/

contains

API communication

Caching

Session

Storage

Formatting

No rendering.

==============================================================================

20. HOOKS
==============================================================================

hooks/

contains

React Hooks

only.

Hooks

must remain

presentation-oriented.

==============================================================================

21. STYLES
==============================================================================

styles/

contains

Global Styles

Layout Styles

Component Styles

Animation

Utilities

No inline styling

except

documented exceptions.

==============================================================================

22. TOKENS
==============================================================================

tokens/

contains

Design Tokens.

Spacing

Typography

Color

Elevation

Radius

Shadow

Motion

Tokens

are

the only

visual source of truth.

==============================================================================

23. ICONS
==============================================================================

icons/

contains

SVG assets

only.

No raster icons.

==============================================================================

24. CONSTANTS
==============================================================================

constants/

contains

UI constants

only.

Business constants

belong elsewhere.

==============================================================================

25. TYPES
==============================================================================

types/

contains

TypeScript

interfaces

types

and

shared contracts.

==============================================================================

26. DEPENDENCY RULES
==============================================================================

Allowed

Screen

↓

Layout

↓

Business Component

↓

Shared Component

↓

Base Component

Forbidden

Base

↓

Business

Shared

↓

Screen

Circular dependency

is forbidden.

==============================================================================

27. NAMING CONVENTIONS
==============================================================================

Folders

kebab-case

Components

PascalCase

Hooks

camelCase

Tokens

snake_case

CSS Variables

kebab-case

==============================================================================

28. FORBIDDEN STRUCTURES
==============================================================================

Commercial UI V3

must never contain

misc/

common/

temp/

helpers/

old/

new/

test2/

backup/

duplicate folders.

Architecture

must remain explicit.

==============================================================================

29. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Every file
has one owner.

✓ Dependencies
flow downward.

✓ No circular imports.

✓ Folder names
describe responsibility.

✓ New developers
find files easily.

FAIL

✗ Mixed responsibilities.

✗ Business logic
inside components.

✗ Circular dependency.

✗ Duplicate folders.

✗ Undefined ownership.

==============================================================================

30. IMPLEMENTATION NOTES
==============================================================================

This specification defines

the physical organization

of the frontend codebase.

It does not define

business logic,

rendering,

or

visual design.

==============================================================================

31. FREEZE
==============================================================================

After approval,

this folder structure

becomes

the canonical

frontend architecture

for Commercial UI V3.

Every implementation

must conform

to this structure.

No architectural deviation

is permitted

without updating

this specification.

# ============================================================================
# END OF DOCUMENT
# ============================================================================