# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 02 — DESIGN SYSTEM
# 04_TYPOGRAPHY_SYSTEM.md
# ============================================================================
#
# Version : 1.0.0
# Status  : Foundation (Freeze Candidate)
# Owner   : Product Architecture
#
# This document defines the ONLY accepted Typography System
# for Commercial UI V3.
#
# ============================================================================

# 1. PURPOSE

Typography is the primary communication system
of Commercial UI V3.

Users read before they interact.

Typography therefore has higher priority than

Colors

Borders

Cards

Icons

Animations

Good typography makes the interface disappear.

Users focus on meaning,
not on UI.

------------------------------------------------------------------------------

# 2. TYPOGRAPHY PHILOSOPHY

Commercial UI V3 is designed for

Professional Reading.

Typography should feel like

a premium consulting report,

not

a web application.

Reading comfort

always wins over visual novelty.

------------------------------------------------------------------------------

# 3. TYPOGRAPHY PRINCIPLES

Commercial UI V3 follows
five principles.

Hierarchy

↓

Readability

↓

Consistency

↓

Scanning

↓

Accessibility

Every text element
must support
at least one principle.

------------------------------------------------------------------------------

# 4. TYPOGRAPHY HIERARCHY

The system defines nine semantic levels.

Display

↓

Page Title

↓

Chapter

↓

Section

↓

Subsection

↓

Body Large

↓

Body

↓

Caption

↓

Metadata

Never invent
additional levels.

------------------------------------------------------------------------------

# 5. TYPOGRAPHY TOKENS

Every typography element
must consume semantic tokens.

Examples

font.display

font.pageTitle

font.chapter

font.section

font.subsection

font.body.large

font.body

font.caption

font.metadata

Raw font sizes
must never appear
inside components.

------------------------------------------------------------------------------

# 6. DISPLAY

Purpose

First impression.

Usage

Executive Hero only.

Maximum

One Display
per page.

Never use
Display
inside reports.

------------------------------------------------------------------------------

# 7. PAGE TITLE

Purpose

Identify
major documents.

One title
per report.

Never compete
with Display.

------------------------------------------------------------------------------

# 8. CHAPTER TITLE

Purpose

Separate
major chapters.

Examples

Executive Summary

BaZi Chart

Executive Insight

Explainable Analysis

Consultation Report

Appendix

Every chapter
uses identical style.

------------------------------------------------------------------------------

# 9. SECTION TITLE

Purpose

Organize
reading.

Section titles
must never dominate
chapter titles.

------------------------------------------------------------------------------

# 10. SUBSECTION TITLE

Purpose

Guide scanning.

Subsections
must be visually lighter
than sections.

------------------------------------------------------------------------------

# 11. BODY LARGE

Purpose

Executive Summary

Highlights

Callouts

Recommendations

Body Large
bridges headings
and paragraphs.

------------------------------------------------------------------------------

# 12. BODY

Body text
is the most important
typography level.

Body must maximize

Reading Comfort.

Never optimize
for information density.

------------------------------------------------------------------------------

# 13. CAPTION

Captions explain.

Captions never conclude.

Captions support charts,
tables,
figures,
references.

------------------------------------------------------------------------------

# 14. METADATA

Metadata has the
lowest typography priority.

Examples

Timestamp

Rule ID

Evidence ID

Confidence

Reference Code

Metadata
must never compete
with conclusions.

------------------------------------------------------------------------------

# 15. LINE LENGTH

Reading width
must remain comfortable.

Target

70–80 characters
per line.

Long paragraphs
must never span
the full monitor width.

------------------------------------------------------------------------------

# 16. LINE HEIGHT

Line height
prioritizes readability.

Display

Compact

Headings

Comfortable

Body

Relaxed

Captions

Compact

Avoid dense text blocks.

------------------------------------------------------------------------------

# 17. PARAGRAPH RHYTHM

Paragraph

↓

Whitespace

↓

Paragraph

↓

Whitespace

Paragraphs
must breathe.

Never stack
long paragraphs
without rhythm.

------------------------------------------------------------------------------

# 18. EMPHASIS

Emphasis uses

Weight

↓

Hierarchy

↓

Whitespace

↓

Contrast

Never use

Many colors

ALL CAPS

Multiple bold words

Large icons

Heavy borders

to replace typography.

------------------------------------------------------------------------------

# 19. TEXT ALIGNMENT

Long-form reading

Left aligned.

Titles

Left aligned.

Metrics

Centered
only when necessary.

Never justify paragraphs.

------------------------------------------------------------------------------

# 20. TYPOGRAPHY & COLOR

Typography defines hierarchy.

Color adds semantics.

Color must never replace
typography hierarchy.

------------------------------------------------------------------------------

# 21. TYPOGRAPHY & GRID

Typography
must align
to the Reading Grid.

Headings

Paragraphs

Lists

Callouts

share the same
alignment axis.

------------------------------------------------------------------------------

# 22. TYPOGRAPHY & SPACING

Typography
works together
with Reading Rhythm.

Heading

↓

Whitespace

↓

Paragraph

↓

Whitespace

↓

Next Heading

Spacing
must reinforce
typography.

------------------------------------------------------------------------------

# 23. RESPONSIVE TYPOGRAPHY

Desktop

Reading optimized.

Laptop

Slightly reduced scale.

Tablet

Maintain hierarchy.

Mobile

Reduce size,

never reduce
hierarchy.

Reading comfort
must remain identical.

------------------------------------------------------------------------------

# 24. ACCESSIBILITY

Typography
must remain readable

without zoom.

Avoid

tiny captions,

low contrast,

dense paragraphs.

Typography
must support
long reading sessions.

------------------------------------------------------------------------------

# 25. TYPOGRAPHY TOKENS

Every typography decision
references Design Tokens.

Examples

font.display

font.chapter

font.section

font.body

font.caption

lineHeight.body

letterSpacing.body

paragraphSpacing.section

Raw values
must never appear
inside components.

------------------------------------------------------------------------------

# 26. ANTI-PATTERNS

Commercial UI V3
must never contain

Too many heading levels.

Random font sizes.

Centered paragraphs.

Long lines.

Dense walls of text.

Multiple highlight styles.

Typography
must create calm.

------------------------------------------------------------------------------

# 27. IMPLEMENTATION RULES

Frontend SHALL NOT

Invent font sizes.

Invent font weights.

Invent line heights.

Invent paragraph spacing.

Everything
must consume
Typography Tokens.

------------------------------------------------------------------------------

# 28. ACCEPTANCE CRITERIA

Typography System
passes only when

✓ Users read effortlessly.

✓ Reading sessions
remain comfortable.

✓ Headings
guide navigation.

✓ Paragraphs
feel book-like.

✓ Typography
creates hierarchy.

✓ Decorative elements
never replace typography.

------------------------------------------------------------------------------

# 29. FREEZE

After approval,

Typography System
becomes immutable.

Future screens
must consume
Typography Tokens only.

No implementation
may bypass
this specification.

# ============================================================================
# END OF DOCUMENT
# ============================================================================