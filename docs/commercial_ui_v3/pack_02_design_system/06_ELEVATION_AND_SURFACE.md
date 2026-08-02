# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 02 — DESIGN SYSTEM
# 06_ELEVATION_AND_SURFACE.md
# ============================================================================
#
# Version : 1.0.0
# Status  : Foundation (Freeze Candidate)
# Owner   : Product Architecture
#
# This document defines the ONLY accepted Surface Model
# and Elevation System for Commercial UI V3.
#
# ============================================================================

# 1. PURPOSE

Commercial UI V3 uses

Surface Hierarchy,

NOT

Card Hierarchy.

Elevation exists only to explain
spatial relationships.

It never exists
for decoration.

------------------------------------------------------------------------------

# 2. DESIGN PHILOSOPHY

Commercial UI V3 is inspired by

Paper

↓

Ink

↓

Annotation

↓

Overlay

The interface should resemble

a professional consultation report,

not

a dashboard.

Surfaces organize information.

They never compete with content.

------------------------------------------------------------------------------

# 3. SURFACE HIERARCHY

Commercial UI V3 defines exactly
five surface levels.

Surface 0

Application Background

↓

Surface 1

Report Paper

↓

Surface 2

Embedded Section

↓

Surface 3

Callout

↓

Surface 4

Overlay

Nothing else exists.

------------------------------------------------------------------------------

# 4. SURFACE 0

Name

Application Background

Purpose

Application shell.

Contains

Navigation

Rail

Top Bar

Footer

Lowest priority.

Never draws attention.

------------------------------------------------------------------------------

# 5. SURFACE 1

Name

Report Paper

Purpose

Primary reading surface.

Every report
exists on exactly
one Report Paper.

There must never be

multiple paper surfaces
competing.

------------------------------------------------------------------------------

# 6. SURFACE 2

Name

Embedded Section

Purpose

Organize chapters.

Examples

Executive Summary

Four Pillars

Executive Insight

Explainable Analysis

Consultation Report

Appendix

Embedded Sections
are part of the Paper.

Not separate cards.

------------------------------------------------------------------------------

# 7. SURFACE 3

Name

Callout

Purpose

Highlight important information.

Examples

Recommendation

Critical Warning

Important Observation

Key Insight

Callouts are exceptions.

Not layout primitives.

------------------------------------------------------------------------------

# 8. SURFACE 4

Name

Overlay

Purpose

Temporary interaction.

Examples

Dialog

Modal

Command Palette

Context Menu

Tooltip

Overlays disappear
when interaction ends.

------------------------------------------------------------------------------

# 9. ELEVATION MODEL

Commercial UI V3
defines four elevations.

Level 0

Flat

↓

Level 1

Soft separation

↓

Level 2

Temporary overlay

↓

Level 3

Modal focus

No deeper hierarchy exists.

------------------------------------------------------------------------------

# 10. SHADOW PHILOSOPHY

Shadow communicates

Elevation.

Never decoration.

Default

No shadow.

Preferred

Soft shadow.

Forbidden

Heavy shadow.

Long shadow.

Colored shadow.

Multiple stacked shadows.

------------------------------------------------------------------------------

# 11. BORDER PHILOSOPHY

Borders define structure.

Preferred

Hairline Divider.

Occasional

Callout Border.

Forbidden

Card Border Everywhere.

Double Borders.

Nested Borders.

Borders should almost disappear.

------------------------------------------------------------------------------

# 12. CORNER RADIUS

Radius indicates

surface identity.

Not decoration.

Commercial UI V3
uses semantic radius tokens.

Examples

radius.paper

radius.callout

radius.overlay

Components
must never invent
new radius values.

------------------------------------------------------------------------------

# 13. SECTION COMPOSITION

Every chapter follows

Paper

↓

Whitespace

↓

Heading

↓

Body

↓

Callout (optional)

↓

Whitespace

No nested cards.

No nested surfaces.

------------------------------------------------------------------------------

# 14. SURFACE TRANSITIONS

Transitions rely on

Whitespace

↓

Typography

↓

Hairline Divider

↓

Surface

Never

Large borders.

Large shadows.

Bright backgrounds.

------------------------------------------------------------------------------

# 15. INTERACTION SURFACES

Interactive elements
must not appear
heavier than reading surfaces.

Buttons

Links

Inputs

Menus

must remain visually subordinate
to the report itself.

------------------------------------------------------------------------------

# 16. RESPONSIVE SURFACES

Desktop

Paper centered.

Laptop

Paper centered.

Tablet

Paper expanded.

Mobile

Paper occupies
full width.

Surface hierarchy
never changes.

------------------------------------------------------------------------------

# 17. SURFACE TOKENS

Every surface
must reference
semantic tokens.

Examples

surface.background

surface.report.paper

surface.section

surface.callout

surface.overlay

Raw values
must never appear
inside components.

------------------------------------------------------------------------------

# 18. ELEVATION TOKENS

Examples

elevation.none

elevation.soft

elevation.overlay

elevation.modal

Implementation
must consume
Elevation Tokens only.

------------------------------------------------------------------------------

# 19. IMPLEMENTATION RULES

Frontend SHALL NOT

Invent surfaces.

Invent shadows.

Invent radius values.

Invent borders.

Invent elevation.

Everything
must consume
Surface Tokens.

------------------------------------------------------------------------------

# 20. ANTI-PATTERNS

Commercial UI V3
must never contain

Cards inside cards.

Borders inside borders.

Shadow inside shadow.

Floating dashboards.

Widget walls.

Glassmorphism.

Neumorphism.

Decorative gradients.

If users notice
containers
before content,

the design fails.

------------------------------------------------------------------------------

# 21. ACCEPTANCE CRITERIA

Surface System passes only when

✓ The report feels like
one continuous document.

✓ Surfaces clarify structure.

✓ Shadows are barely noticeable.

✓ Borders are minimal.

✓ Callouts stand out
without overwhelming.

✓ Reading remains primary.

------------------------------------------------------------------------------

# 22. FREEZE

After approval,

Surface & Elevation
become immutable.

Future screens
must consume

Surface Tokens

Elevation Tokens

only.

No implementation
may bypass
this specification.

# ============================================================================
# END OF DOCUMENT
# ============================================================================