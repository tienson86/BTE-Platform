# 08_CHART_SYSTEM.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- PACK_04_UI_PRESENTATION_STANDARD.md §15.6
- PACK_05_ACCESSIBILITY.md §13
- 01_COLOR_SYSTEM.md
- 05_CARD_SYSTEM.md

---

# 1. Philosophy

Charts explain analysis.

They are not decoration.

They live inside Analysis or Summary cards (height XL for dedicated Chart cards).

Unified axes, type, and color meaning.

---

# 2. Structure

Title (Card Title or Caption)

↓

Chart

↓

Legend / labels (required for color)

↓

Optional caption

Never a chart without a title.

Never color-only categories.

---

# 3. Color

- Neutral structure: axes, grid, unselected series.
- Primary accent for the focus series.
- Success / Warning / Critical only when the data encodes that meaning.
- Maximum one accent hue plus status colors.

---

# 4. Type

Allowed: bar, horizontal bar, simple line, proportional part-to-whole.

Avoid: 3D, exploded pie as the primary chart, ornamental gauges, rainbow palettes.

Five-element and score charts use the same spacing, radius, and type rules as the rest of the product.

---

# 5. Responsive

PACK_04: charts reflow; they do not shrink labels below Caption.

Internal overflow is allowed. Page-level horizontal scroll is not.

---

# 6. Accessibility

- Text labels or a data table alternative.
- Contrast on series vs paper.
- Motion: no looping chart animation. See 09_MOTION_SYSTEM.md.

---

END
