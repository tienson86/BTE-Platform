# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 04 — IMPLEMENTATION SPECIFICATION
# 06_STYLING_STRATEGY.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Related Documents

- Pack 02 Design System
- 00_IMPLEMENTATION_PRINCIPLES.md
- 01_FOLDER_STRUCTURE.md
- 02_COMPONENT_ARCHITECTURE.md

==============================================================================
1. PURPOSE
==============================================================================

This document defines

the canonical styling strategy

for Commercial UI V3.

All visual appearance

must originate

from

Design Tokens.

Styling

is an implementation

of the Design System,

not

an independent layer.

==============================================================================

2. DESIGN GOALS
==============================================================================

The Styling Strategy provides

• Visual consistency

• Predictable styling

• Token-driven implementation

• Theme support

• Easy maintenance

• Scalable architecture

==============================================================================

3. STYLING PHILOSOPHY
==============================================================================

Commercial UI V3

is

Token Driven.

Components

never define

their own

visual language.

Components

consume

Design Tokens.

==============================================================================

4. CANONICAL STYLING FLOW
==============================================================================

Design Language

↓

Design Tokens

↓

CSS Variables

↓

Component Styles

↓

Layout Styles

↓

Rendered UI

No shortcut

is allowed.

==============================================================================

5. STYLE OWNERSHIP
==============================================================================

Visual decisions

belong to

Design Tokens.

Component Styles

apply

those decisions.

Business Components

never

invent

visual rules.

==============================================================================

6. DESIGN TOKENS
==============================================================================

Every visual value

must come from

Design Tokens.

Examples

Spacing

Typography

Color

Radius

Elevation

Motion

Border

Opacity

Z-index

==============================================================================

7. CSS VARIABLES
==============================================================================

Every Design Token

must become

one CSS Variable.

Example

spacing-lg

↓

--space-lg

Primary Color

↓

--color-primary

Body Font

↓

--font-body

==============================================================================

8. COMPONENT STYLES
==============================================================================

Components

consume

CSS Variables only.

Hardcoded values

are forbidden.

Example

padding

↓

var(--space-md)

Never

padding: 13px

==============================================================================

9. LAYOUT STYLES
==============================================================================

Layouts define

Grid

Spacing

Alignment

Reading Width

Surface Position

Layouts

must not

change

Component styling.

==============================================================================

10. SCREEN STYLES
==============================================================================

Screens

compose

Layouts

and

Components.

Screens

must contain

minimal

styling rules.

==============================================================================

11. RESPONSIVE STYLING
==============================================================================

Responsive behavior

uses

Design Tokens.

Never

duplicate CSS

for devices.

Breakpoint logic

must remain

predictable.

==============================================================================

12. THEMING
==============================================================================

Light Theme

↓

Dark Theme

↓

Future Themes

Themes

override

Token values,

not

Component rules.

==============================================================================

13. TYPOGRAPHY
==============================================================================

Typography

must consume

Typography Tokens.

Never

hardcode

font-family

font-size

line-height

font-weight.

==============================================================================

14. COLORS
==============================================================================

All colors

must use

Semantic Tokens.

Examples

Text

Surface

Border

Success

Warning

Danger

Muted

Never

direct HEX values

inside Components.

==============================================================================

15. SPACING
==============================================================================

All spacing

must use

Spacing Tokens.

Examples

Margin

Padding

Gap

Inset

Section spacing

Hardcoded spacing

is forbidden.

==============================================================================

16. ELEVATION
==============================================================================

All shadows

must use

Elevation Tokens.

Never

define

custom shadows

inside Components.

==============================================================================

17. ICONS
==============================================================================

Icons

must inherit

semantic color

and

size tokens.

Icons

must never

define

fixed colors.

==============================================================================

18. ANIMATIONS
==============================================================================

Motion

must consume

Motion Tokens.

Animation duration

↓

Token

Animation easing

↓

Token

Animation distance

↓

Token

==============================================================================

19. STATE STYLING
==============================================================================

Loading

Ready

Unavailable

Empty

Error

Hover

Focus

Disabled

All states

must consume

State Tokens.

==============================================================================

20. CSS ORGANIZATION
==============================================================================

styles/

├── tokens.css

├── reset.css

├── typography.css

├── layout.css

├── utilities.css

├── themes/

│   ├── light.css

│   └── dark.css

└── components/

No business logic

inside CSS.

==============================================================================

21. FORBIDDEN STYLING
==============================================================================

Commercial UI V3

must never

✗ Hardcode colors.

✗ Hardcode spacing.

✗ Hardcode typography.

✗ Hardcode shadows.

✗ Use inline styles.

✗ Override sibling styles.

✗ Duplicate token values.

==============================================================================

22. ACCESSIBILITY
==============================================================================

Styling

must preserve

Contrast

Focus

Reduced Motion

Readable Typography

Minimum Touch Target

WCAG AA

==============================================================================

23. PERFORMANCE
==============================================================================

Styling

must minimize

CSS size

Unused rules

Deep selectors

Specificity conflicts

Prefer

token reuse

over duplication.

==============================================================================

24. TRACEABILITY
==============================================================================

Every style

must be traceable

to

Design Token

↓

Component

↓

Screen Specification

No orphan styles.

==============================================================================

25. TESTING REQUIREMENTS
==============================================================================

Every visual component

must support

Light Theme

Dark Theme

Responsive

Focus

Hover

Disabled

Reduced Motion

==============================================================================

26. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Every style uses Design Tokens.

✓ No hardcoded values.

✓ Theme switching works.

✓ Responsive styling preserved.

✓ Components remain visually consistent.

✓ Styling remains traceable.

FAIL

✗ Hardcoded CSS.

✗ Mixed spacing scales.

✗ Direct HEX colors.

✗ Duplicate visual rules.

✗ Theme-specific components.

==============================================================================

27. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Styling Architecture

Token Consumption

Theme Strategy

CSS Organization

Traceability

It does NOT define

specific CSS frameworks,

Tailwind configuration,

CSS preprocessors,

or runtime styling libraries.

==============================================================================

28. FUTURE EXTENSIONS
==============================================================================

The Styling Strategy

may support

Brand Themes

Seasonal Themes

High Contrast Theme

Print Theme

Custom Client Themes

provided

all styling

continues to consume

Design Tokens.

==============================================================================

29. FREEZE
==============================================================================

After approval,

Styling Strategy

becomes

the canonical

visual implementation architecture

for Commercial UI V3.

Every implementation

must preserve

Token-driven styling,

Theme isolation,

Visual consistency,

Traceability,

and

Maintainability.

# ============================================================================
# END OF DOCUMENT
# ============================================================================