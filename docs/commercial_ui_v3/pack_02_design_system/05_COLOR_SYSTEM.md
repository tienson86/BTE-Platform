# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 02 — DESIGN SYSTEM
# 05_COLOR_SYSTEM.md
# ============================================================================
#
# Version : 1.0.0
# Status  : Foundation (Freeze Candidate)
# Owner   : Product Architecture
#
# This document defines the ONLY accepted Color System
# for Commercial UI V3.
#
# ============================================================================

# 1. PURPOSE

Color exists to communicate meaning.

Color does NOT exist
to decorate the interface.

Commercial UI V3 uses
Semantic Colors.

Meaning first.

Appearance second.

------------------------------------------------------------------------------

# 2. DESIGN PHILOSOPHY

Users read text.

Not colors.

Therefore

Typography

↓

Whitespace

↓

Hierarchy

↓

Color

Color supports understanding.

Color never creates understanding.

------------------------------------------------------------------------------

# 3. COLOR PRINCIPLES

Commercial UI V3 follows
five principles.

Meaning

↓

Consistency

↓

Accessibility

↓

Subtlety

↓

Trust

Color must reduce ambiguity.

Never create visual noise.

------------------------------------------------------------------------------

# 4. COLOR HIERARCHY

The interface defines
exactly six semantic groups.

Text

↓

Surface

↓

Border

↓

Semantic Feedback

↓

Interaction

↓

Accent

Nothing exists outside
these six groups.

------------------------------------------------------------------------------

# 5. TEXT COLORS

Semantic Tokens

text.primary

Primary reading.

--------------------------------------------------

text.secondary

Supporting reading.

--------------------------------------------------

text.muted

Metadata.

--------------------------------------------------

text.inverse

Dark surfaces only.

Text hierarchy
must remain stable
across themes.

------------------------------------------------------------------------------

# 6. SURFACE COLORS

Semantic Tokens

surface.report.paper

Primary reading surface.

--------------------------------------------------

surface.section

Secondary surface.

--------------------------------------------------

surface.callout

Important explanation.

--------------------------------------------------

surface.overlay

Modal.

--------------------------------------------------

surface.disabled

Unavailable content.

Surface colors
create structure.

Never attraction.

------------------------------------------------------------------------------

# 7. BORDER COLORS

Semantic Tokens

border.divider

Hairline separators.

--------------------------------------------------

border.callout

Highlighted notes.

--------------------------------------------------

border.focus

Keyboard accessibility.

Borders
must never dominate
the page.

------------------------------------------------------------------------------

# 8. SEMANTIC FEEDBACK

Commercial UI V3
defines semantic states.

Success

Confirmed.

--------------------------------------------------

Warning

Needs attention.

--------------------------------------------------

Danger

Critical issue.

--------------------------------------------------

Info

Supporting information.

Feedback colors

never replace
written explanations.

------------------------------------------------------------------------------

# 9. INTERACTION COLORS

Interaction colors
communicate state.

Hover

↓

Focus

↓

Selected

↓

Active

↓

Disabled

Interaction
must never rely
only on color.

------------------------------------------------------------------------------

# 10. ACCENT COLORS

Accent color

is reserved for

Primary actions.

Important links.

Critical navigation.

Never use accent colors
to decorate layouts.

------------------------------------------------------------------------------

# 11. CHART COLORS

Charts
support analysis.

Charts
never become
visual anchors.

Chart colors
must remain

Calm.

Muted.

Consistent.

Never rainbow palettes.

Never saturated dashboards.

------------------------------------------------------------------------------

# 12. READING ATMOSPHERE

Commercial UI V3
should resemble

Ink

on

Paper.

The page
must feel

Open.

Calm.

Professional.

Avoid
high saturation.

------------------------------------------------------------------------------

# 13. DARK MODE

Dark mode
preserves

Meaning.

Hierarchy.

Reading rhythm.

Dark mode

does NOT invert
semantic intent.

Text remains primary.

------------------------------------------------------------------------------

# 14. COLOR TOKENS

Every color
references
Semantic Tokens.

Examples

text.primary

text.secondary

surface.report.paper

surface.callout

border.divider

feedback.success

feedback.warning

interaction.hover

accent.primary

Raw HEX values
must never appear
inside components.

------------------------------------------------------------------------------

# 15. COLOR ACCESSIBILITY

All color combinations
must satisfy

WCAG AA

minimum.

Long-form reading
should target

WCAG AAA

where practical.

Color alone
must never communicate
critical meaning.

------------------------------------------------------------------------------

# 16. IMPLEMENTATION RULES

Frontend SHALL NOT

Hardcode colors.

Invent palettes.

Invent semantic roles.

Invent new accents.

Everything
must consume
Color Tokens.

------------------------------------------------------------------------------

# 17. ANTI-PATTERNS

Commercial UI V3
must never contain

Rainbow dashboards.

Colorful cards.

Heavy gradients.

Neon highlights.

Colored borders everywhere.

Decorative backgrounds.

Marketing-style sections.

If users notice colors
before content,

the design fails.

------------------------------------------------------------------------------

# 18. ACCEPTANCE CRITERIA

Color System passes only when

✓ Reading remains effortless.

✓ Color reinforces meaning.

✓ Colors never compete
with typography.

✓ Charts remain secondary.

✓ The interface feels
professional.

✓ Users describe the UI as

Calm.

Trustworthy.

Elegant.

------------------------------------------------------------------------------

# 19. FREEZE

After approval,

Color System
becomes immutable.

Every future

Theme

Screen

Component

Animation

must consume

Semantic Color Tokens.

No implementation
may bypass
this specification.

# ============================================================================
# END OF DOCUMENT
# ============================================================================