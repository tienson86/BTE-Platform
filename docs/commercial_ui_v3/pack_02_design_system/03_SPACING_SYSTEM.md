# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 02 — DESIGN SYSTEM
# 03_SPACING_SYSTEM.md
# ============================================================================
#
# Version : 1.0.0
# Status  : Foundation (Freeze Candidate)
# Owner   : Product Architecture
#
# This document defines the ONLY accepted Spacing System
# for Commercial UI V3.
#
# ============================================================================

# 1. PURPOSE

Spacing is not empty space.

Spacing is the primary tool
for controlling reading rhythm.

Commercial UI V3 uses whitespace
to reduce cognitive load,
guide attention,
and separate ideas.

Spacing creates hierarchy
before borders,
colors,
or shadows.

------------------------------------------------------------------------------

# 2. DESIGN PHILOSOPHY

Commercial UI V3 follows

Reading Rhythm First.

Spacing is designed around

human reading,

not component density.

Readers should feel

calm,

comfortable,

guided,

never crowded.

------------------------------------------------------------------------------

# 3. SPACING PRINCIPLES

Spacing communicates

Hierarchy

↓

Relationship

↓

Importance

↓

Reading Pace

Every gap
must have meaning.

Random spacing
is forbidden.

------------------------------------------------------------------------------

# 4. SPACING SCALE

Commercial UI V3 uses
an 8-point based scale.

Token

Value

space-0

0

space-1

4

space-2

8

space-3

12

space-4

16

space-5

24

space-6

32

space-7

48

space-8

64

space-9

96

space-10

120

No intermediate values
are allowed.

------------------------------------------------------------------------------

# 5. SEMANTIC SPACING TOKENS

Spacing is consumed
through semantic tokens.

Examples

space.inline

space.list

space.paragraph

space.block

space.section

space.chapter

space.page

Never consume
raw spacing tokens
inside components.

------------------------------------------------------------------------------

# 6. PAGE RHYTHM

Page

↓

Chapter

120

↓

Section

96

↓

Block

48

↓

Paragraph

24

↓

Inline

8–16

Every page
follows this rhythm.

------------------------------------------------------------------------------

# 7. HERO SPACING

Hero Top

96

Identity → Verdict

32

Verdict → Recommendation

24

Recommendation → Metrics

32

Bottom

96

Hero must breathe.

------------------------------------------------------------------------------

# 8. FOUR PILLARS SPACING

Section Title

↓

32

↓

Pillars

↓

32

↓

Metadata

↓

24

↓

Divider

↓

48

Avoid compressed tables.

------------------------------------------------------------------------------

# 9. EXECUTIVE INSIGHT

Headline

↓

24

↓

Summary

↓

32

↓

Insight Blocks

↓

32

↓

Recommendation

↓

48

Reading must feel effortless.

------------------------------------------------------------------------------

# 10. ANALYSIS BLOCKS

Title

↓

24

↓

Conclusion

↓

24

↓

Explanation

↓

32

↓

Evidence

↓

24

↓

Rule

↓

24

↓

Confidence

↓

48

Every block
shares identical rhythm.

------------------------------------------------------------------------------

# 11. CONSULTATION REPORT

Heading

↓

32

↓

Paragraph

↓

24

↓

Paragraph

↓

24

↓

Callout

↓

32

↓

Paragraph

Long-form reading
must resemble books.

------------------------------------------------------------------------------

# 12. APPENDIX

Evidence

↓

24

↓

Reference

↓

16

↓

Citation

↓

32

Appendix has
the lowest density.

------------------------------------------------------------------------------

# 13. LIST SPACING

List Item

↓

12

Group

↓

24

Section

↓

48

No crowded lists.

------------------------------------------------------------------------------

# 14. TABLE SPACING

Header

↓

16

↓

Rows

↓

16

↓

Section

↓

32

Tables remain readable.

------------------------------------------------------------------------------

# 15. FORM SPACING

Although reports dominate,
future forms
must follow the same rhythm.

Field Label

↓

8

↓

Input

↓

24

↓

Next Field

Consistency is mandatory.

------------------------------------------------------------------------------

# 16. RESPONSIVE SPACING

Desktop

100%

Laptop

90%

Tablet

80%

Mobile

70%

Spacing scales proportionally.

Reading rhythm
must remain recognizable.

------------------------------------------------------------------------------

# 17. SPACING TOKENS

All spacing
references Design Tokens.

Examples

space.page

space.chapter

space.section

space.block

space.paragraph

space.inline

Raw pixel values
must never appear
inside components.

------------------------------------------------------------------------------

# 18. IMPLEMENTATION RULES

Frontend SHALL NOT

Invent spacing.

Compress sections.

Stretch layouts
without semantic reason.

Every spacing decision
must reference
Spacing Tokens.

------------------------------------------------------------------------------

# 19. ANTI-PATTERNS

Commercial UI V3
must never contain

Random spacing.

Uneven spacing.

Nested padding.

Large empty gaps.

Crowded layouts.

Visual noise.

Spacing
must create rhythm,
not confusion.

------------------------------------------------------------------------------

# 20. ACCEPTANCE CRITERIA

Spacing System passes only when

✓ Reading feels natural.

✓ Sections breathe.

✓ No component feels cramped.

✓ White space guides attention.

✓ Visual rhythm
is immediately recognizable.

✓ Users never perceive
spacing as inconsistent.

------------------------------------------------------------------------------

# 21. FREEZE

After approval,

Spacing System
becomes immutable.

Future components
must consume
Spacing Tokens only.

No arbitrary spacing
may be introduced.

# ============================================================================
# END OF DOCUMENT
# ============================================================================