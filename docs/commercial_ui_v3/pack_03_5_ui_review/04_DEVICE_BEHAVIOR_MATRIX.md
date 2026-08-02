# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03.5 — UI REVIEW & WIREFRAMES
# 04_DEVICE_BEHAVIOR_MATRIX.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

------------------------------------------------------------------------------
# 1. PURPOSE

This document defines the canonical behavior matrix
for every supported device.

It specifies

what must remain identical,

what may adapt,

and

what must never change.

This document guarantees
a consistent Commercial UI experience
across Desktop,
Tablet,
and Mobile.

------------------------------------------------------------------------------

# 2. DESIGN PHILOSOPHY

Commercial UI V3 is

One Product

One Reading Journey

Many Presentations.

Presentation adapts.

Meaning does not.

------------------------------------------------------------------------------

# 3. DEVICE ROLES

Desktop

Professional Workstation

Deep analysis.

--------------------------------------------------

Tablet

Professional Reading Device

Long-form consultation.

--------------------------------------------------

Mobile

Consultation Companion

Quick understanding.

------------------------------------------------------------------------------

# 4. INVARIANT RULES

The following elements
MUST remain identical
on every device.

✓ Business Goal

✓ Reading Goal

✓ Reading Order

✓ Information Priority

✓ Section Sequence

✓ Business Components

✓ Binding Contract

✓ Data Meaning

✓ Interpretation

✓ Knowledge References

These items
may never change.

------------------------------------------------------------------------------

# 5. ADAPTIVE RULES

The following elements
may change
according to device.

Grid

Spacing

Margins

Reading Width

Column Count

Navigation Style

Chart Scaling

Typography Scale

Component Density

Surface Width

Only presentation changes.

------------------------------------------------------------------------------

# 6. PAGE STRUCTURE

| Area | Desktop | Tablet | Mobile |
|------|----------|---------|---------|
| Navigation | Top + Reading Rail | Top + Drawer | Top + Drawer |
| Reading Progress | Rail | Top | Top |
| Report Sheet | Centered | Full Width | Full Width |
| Footer | Visible | Visible | Compact |

------------------------------------------------------------------------------

# 7. EXECUTIVE HERO

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Display | Wide | Single Column | Single Column |
| Recommendation | Above Metrics | Above Metrics | Above Metrics |
| Metrics | Horizontal | Wrap | Vertical |
| Hero Height | ~1 Viewport | ~1 Viewport | ~1 Viewport |

Business Goal

unchanged.

------------------------------------------------------------------------------

# 8. FOUR PILLARS

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Layout | 4 Columns | 4 Columns or 2×2 | Vertical Stack |
| Day Pillar | Highlighted | Highlighted | Highlighted |
| Hidden Stems | Chips | Chips | Chips |
| Metadata | Expanded | Compact | Collapsible |

------------------------------------------------------------------------------

# 9. EXECUTIVE INSIGHT

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Layout | Reading Width | Reading Width | Full Width |
| Recommendation | Highlight | Highlight | Highlight |
| Multi-column | No | No | No |

Insight remains textual.

------------------------------------------------------------------------------

# 10. VISUAL ANALYTICS

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Charts | Medium | Smaller | Small |
| Explanation | Beside / Below | Below | Below |
| Horizontal Scroll | Never | Never | Never |

Charts support text.

------------------------------------------------------------------------------

# 11. EXPLAINABLE ANALYSIS

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Blocks | Expanded | Expanded | Expandable |
| Evidence | Visible | Visible | Collapsible |
| Rule | Visible | Visible | Expandable |
| Confidence | Visible | Visible | Visible |

Reading sequence
never changes.

------------------------------------------------------------------------------

# 12. CONSULTATION REPORT

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| TOC | Sticky | Collapsible | Drawer |
| Chapters | Continuous | Continuous | Continuous |
| Reading Progress | Rail | Top | Top |

The report remains
one document.

------------------------------------------------------------------------------

# 13. KNOWLEDGE WORKSPACE

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Evidence | Expanded | Expanded | Collapsed |
| Classical Sources | Expanded | Expandable | Collapsible |
| Related Topics | Visible | Visible | Expandable |

Knowledge remains
after the report.

------------------------------------------------------------------------------

# 14. NAVIGATION

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Reading Rail | Sticky | Drawer | Drawer |
| Scroll Spy | Always | Active | Active |
| Progress | Rail | Top | Top |
| Jump Navigation | Rail | Drawer | Drawer |

------------------------------------------------------------------------------

# 15. SCROLLING

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Vertical Scroll | Yes | Yes | Yes |
| Nested Scroll | No | No | No |
| Horizontal Scroll | No | No | No |

------------------------------------------------------------------------------

# 16. TYPOGRAPHY

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Hierarchy | Fixed | Fixed | Fixed |
| Scale | 100% | 95% | 90% |
| Reading Width | 70–80 chars | Comfortable | Comfortable |

Hierarchy
must never change.

------------------------------------------------------------------------------

# 17. SPACING

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Chapter | Large | Medium | Medium |
| Section | Large | Medium | Medium |
| Paragraph | Standard | Standard | Standard |

Reading rhythm
remains identical.

------------------------------------------------------------------------------

# 18. MOTION

| Behaviour | Desktop | Tablet | Mobile |
|-----------|----------|---------|---------|
| Motion Intent | Same | Same | Same |
| Hover | Yes | No | No |
| Tap | Optional | Primary | Primary |
| Keyboard | Full | Partial | External Only |

------------------------------------------------------------------------------

# 19. ACCESSIBILITY

Every device
must support

Keyboard (where applicable)

↓

Screen Readers

↓

High Contrast

↓

Reduced Motion

↓

Semantic Structure

Accessibility
must never degrade
on smaller devices.

------------------------------------------------------------------------------

# 20. IMPLEMENTATION MATRIX

Frontend SHALL

adapt presentation.

Frontend SHALL NOT

change

Business Goal

Reading Goal

Reading Order

Information Priority

Binding

Meaning

Interpretation

------------------------------------------------------------------------------

# 21. REVIEW CHECKLIST

The cross-device experience passes only when

✓ Reading Journey is identical.

✓ Meaning is identical.

✓ Business Components are identical.

✓ Binding Contract is identical.

✓ Presentation adapts naturally.

✓ No device feels like a different product.

------------------------------------------------------------------------------

# 22. FREEZE

After approval,

this Device Behavior Matrix
becomes the canonical reference
for all responsive implementations.

Every future device
must inherit these rules.

No implementation
may redefine cross-device behavior.

# ============================================================================
# END OF DOCUMENT
# ============================================================================