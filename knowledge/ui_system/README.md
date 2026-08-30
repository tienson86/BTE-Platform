# BTE Visual System V2

Version: 2.0  
Status: DESIGN FOUNDATION  
Owner: BTE Product Architecture  
Sprint: UI-13

Depends On

- Product Manifesto
- Experience Principles
- Brand Language
- Visual Language
- Design System PACK_01–07

Foundation V1.0 is frozen. This system specifies how those standards apply to Commercial UI V2. It does not replace Foundation. It does not invent tokens.

---

## Purpose

Visual System V2 is the official visual design standard for BTE Platform Version 2.

It defines appearance and token usage for a commercial product.

It does not implement CSS.

It does not redesign Dashboard, Cards, or PDF.

It does not change Narrative, Runtime, or Portal routing.

---

## Product identity

BTE is a professional analytical platform.

Commercial product.

Not an admin panel.

Not a developer tool.

Not a spreadsheet.

The interface should feel like an experienced consultant, not an automated calculator.

---

## Core goals

Premium · Professional · Readable · Trustworthy · Calm

---

## Documents

| Document | Role |
|----------|------|
| [00_DESIGN_PRINCIPLES.md](./00_DESIGN_PRINCIPLES.md) | Philosophy and non-goals |
| [01_COLOR_SYSTEM.md](./01_COLOR_SYSTEM.md) | Color roles and tokens |
| [02_TYPOGRAPHY.md](./02_TYPOGRAPHY.md) | Type roles and scale |
| [03_SPACING_SYSTEM.md](./03_SPACING_SYSTEM.md) | Spacing scale and rhythm |
| [04_GRID_SYSTEM.md](./04_GRID_SYSTEM.md) | Desktop / tablet / mobile |
| [05_CARD_SYSTEM.md](./05_CARD_SYSTEM.md) | Hero, Analysis, Reference, Summary, Status |
| [06_ICON_SYSTEM.md](./06_ICON_SYSTEM.md) | Unified icon style |
| [07_BADGE_SYSTEM.md](./07_BADGE_SYSTEM.md) | Unified badges |
| [08_CHART_SYSTEM.md](./08_CHART_SYSTEM.md) | Unified charts |
| [09_MOTION_SYSTEM.md](./09_MOTION_SYSTEM.md) | Allowed motion |
| [10_EMPTY_LOADING.md](./10_EMPTY_LOADING.md) | Empty, loading, error |
| [11_ACCESSIBILITY.md](./11_ACCESSIBILITY.md) | Contrast, spacing, focus |
| [12_VISUAL_VALIDATION.md](./12_VISUAL_VALIDATION.md) | Validation gate |

---

## Dependency chain

```
Product Manifesto
↓
Experience Principles
↓
Brand Language
↓
Visual Language
↓
Design System PACK_01–07
↓
Visual System V2  ← this folder
↓
Code (later sprints)
```

Higher layers win conflicts.

---

## Out of scope (UI-13)

- CSS migration
- Dashboard redesign
- Card redesign
- PDF redesign
- Runtime changes
- Narrative changes
- Portal routing changes

STOP. Do not start UI-14 from this folder.

---

END
