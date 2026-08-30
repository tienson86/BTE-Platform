# 04_GRID_SYSTEM.md

Version: 2.0  
Status: DESIGN FOUNDATION  
Sprint: UI-13

Depends On

- PACK_02_LAYOUT_SYSTEM.md §4–6, §18–19

Do not invent column counts or breakpoints.

---

# 1. Philosophy

The grid organizes information. It does not decorate.

Content stays centered. It never stretches endlessly.

Cards wrap. Typography does not scale dramatically.

---

# 2. Columns

| Viewport | Columns |
|----------|---------|
| Desktop | 12 |
| Tablet | 8 |
| Mobile | 4 |

Standard gap: 24px.

Never use arbitrary column counts.

---

# 3. Breakpoints (PACK_02)

| Name | Range |
|------|-------|
| Mobile | < 640px |
| Tablet | 640–1023px |
| Desktop | 1024–1439px |
| Wide | 1440px+ |
| Ultra wide | 1800px+ |

PACK_02 wins over any implementation breakpoint that differs.

---

# 4. Content width

| Context | Max width |
|---------|-----------|
| Desktop | 1600px |
| Ultra wide | 1800px |
| Report reading | `--grid-reading-max-width` 760px |
| Report layout | `--grid-report-max-width` 1360px |

Content is centered.

---

# 5. Page padding

Desktop 32px. Tablet 24px. Mobile 16px.

Grid margin tokens (`--grid-margin`) must follow the same rhythm.

---

# 6. Analysis composition

Zones

↓

Rows

↓

Grid

↓

Cards

Do not invent a new Result Page architecture. PACK_06 / PACK_07 remain the Result layout standard.

---

# 7. Responsive behavior

- Cards wrap automatically.
- Avoid horizontal page scroll.
- Overflow belongs inside the component.
- Equal-height cards in the same row (PACK_04 height classes).

---

END
