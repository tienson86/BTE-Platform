# VISUAL HIERARCHY

| Field | Value |
|-------|--------|
| **Document** | `VISUAL_HIERARCHY.md` |
| **Version** | `1.1.0` |
| **Status** | Final Freeze — Blueprint V1.1 |
| **See also** | [15_VISUAL_GRAMMAR.md](15_VISUAL_GRAMMAR.md) (Addendum J) |

---

## Purpose

Define **size, type, space, card mass, highlight, color role, and motion** per information level so the Result screen cannot flatten into an admin grid.

Implementation must follow these levels — not invent a new hierarchy mid-sprint.

---

## Hierarchy levels

| Level | Name | What lives here |
|-------|------|-----------------|
| VH0 | Chrome | App header, result meta, actions |
| VH1 | Executive Hero | Day Master + core metrics + sentence |
| VH2 | Structural identity | Four Pillars |
| VH3 | Visual support | Charts |
| VH4 | Thematic analysis | Large analysis sections |
| VH5 | Narrative report | Interpretation chapters |
| VH6 | Evidence / dialogue | Knowledge |
| VH7 | Captions / unavailable | Hints, empty honesty |

**Rule:** VH1 must visually dominate VH4–VH7. Equal card mass across VH1–VH6 = fail.

---

## Typography scale (logical tokens)

| Token | Use | Relative size |
|-------|-----|---------------|
| `display` | Nhật Chủ value | Largest on page (~2–2.75rem) |
| `title` | Tier titles | ~1.5–1.85rem |
| `subtitle` | Large section titles | ~1.1–1.25rem |
| `body` | Sentences, chapter text | ~1rem, line-height ≥1.6 |
| `metric` | Metric values | ~1.15–1.35rem, semibold/bold |
| `caption` | Labels, hints, meta | ~0.8–0.9rem, muted |
| `eyebrow` | “Tóm tắt điều hành” | ~0.7–0.75rem, uppercase tracking |

**Forbidden:** Using `metric` size for every label in a dense grid (dashboard smell).

---

## Spacing (whitespace)

| Region | Spec |
|--------|------|
| Between tiers | Generous (≈ 2–3× inner card padding) |
| Inside hero | Air around Day Master; metrics not cramped |
| Pillar columns | Clear gutters; internal rows separated by hairlines |
| Analysis stack | One large card per theme with internal padding ≥ hero metric padding |
| Dense knowledge panes | Allowed only inside VH6 |

**Fail signal:** “Wallpaper of equal cards with 8px gaps everywhere.”

---

## Card / surface mass

| Surface | Mass | Notes |
|---------|------|-------|
| ExecutiveHero | XL | Single dominant surface |
| PillarColumn | L | Four siblings; Day = L+ |
| Chart card | M | Readable, not hero |
| AnalysisSection | L | Full width of stream |
| InterpretationSection | L | Full width |
| SummaryMetric | S–M | Nested inside hero only |
| Mini KPI strip (admin style) | **Banned** as primary Result pattern | |

---

## Highlight rules

| May highlight | How |
|---------------|-----|
| Nhật Chủ / Day pillar | Primary accent + scale |
| Dụng Thần | Soft primary wash |
| Hỷ Thần | Soft success-neutral wash (not neon) |
| Kỵ Thần | Soft warning-neutral wash (**not** fear red flood) |
| Thân | Soft info-neutral wash |

| Must not highlight |
|--------------------|
| Every score category equally |
| Random icons with bright fills |
| Error-red for “unfavorable” as doom |

---

## Color roles (language, not hex sheet)

| Role | Meaning on Result |
|------|-------------------|
| Neutral canvas | Majority of UI — analysis calm |
| Primary accent | Day Master / Useful God / active rail |
| Muted text | Captions, meta |
| Success-soft | Helpful god / positive lists (restrained) |
| Warning-soft | Caution / unfavorable (restrained) |
| Danger | System errors only — not BaZi “kỵ” storytelling |

Neutrals dominate. Accents are scarce by design.

---

## Iconography

- One consistent stroke set (see COMPONENT_MAP `Icon`)
- Icons label tiers and day master — not decorative sticker spam
- No random emoji as product language

---

## Animation / motion

| Moment | Motion |
|--------|--------|
| Page load | Skeleton → content fade (~200–350ms) |
| Tier enter | Subtle rise/fade once |
| Rail active | Background/color transition |
| Collapse | Height/opacity; chevron rotate |
| Chart paint | Bar width ease; no infinite pulse |

**Forbidden:** Confetti, heavy parallax, blinking badges, auto-rotating carousels of metrics.

---

## Progressive disclosure

| Default visible | May start collapsed |
|-----------------|---------------------|
| Hero, Pillars, Charts | Relations, Shen Sha, Knowledge status, empty interpretation chapters |
| Core analysis (elements, gods, pattern, useful) | Expert narrative fallback details |

Collapsed content remains in the IA spine (anchor still exists).

---

## Accessibility (IA-relevant)

- Tier headings are real headings (`h2`/`h3` semantics in future impl)
- Rail links have clear focus rings
- Color is not the only Day Master cue (label + position + scale)
- Unavailable text readable, not icon-only

---

## Version

`1.1.0`
