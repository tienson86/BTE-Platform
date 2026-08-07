# FINAL DESKTOP V2 LAYOUT — LOCKED

**Status:** LOCKED  
**Date:** 2026-08-07  
**Marker:** `data-canonical="desktop-v2"` · `data-layout-lock="final"`  
**Preview:** `http://127.0.0.1:5177/?page=desktop`

## Confirmation

Desktop V2 layout is **LOCKED**.

No further Desktop layout redesign after this approval gate.
Component internals, tokens, typography, colors, and icons were not changed — modules were rearranged only.

---

## Section hierarchy (reading flow)

```
STEP 1 — Context
  Row 1          S00 ContextHeader

STEP 2 — Identity + Core Chart + Feng Shui
  Section A      S01 | S03 | S09     (3 equal columns)

STEP 3 — Overall Analysis
  Section B      S02 | S04 | S06     (3 equal columns)

STEP 4 — Final Evaluation
  Section C      S05 | S07 | S08 | S10 | S11   (5 equal columns)
```

| Block | Purpose | Modules | Card type |
|-------|---------|---------|-----------|
| Row 1 | Context | S00 | Full |
| Section A | Identity / Core Chart / Feng Shui | S01, S03, S09 | Full |
| Section B | Overall / Five Elements / Ten Gods | S02, S04, S06 | Full (S02/S04) · Preview (S06) |
| Section C | Strength / ShenSha / Interpretation / Bone / Report | S05, S07, S08, S10, S11 | Preview |

Height: natural · `align-items: start` · no equal-height stretch.

---

## Screenshots

1. Viewport 1920×1080  
   `knowledge/ui_reference/migration_report/screenshots/desktop_v2_final/02_desktop_viewport_1920x1080.png`

2. Full page  
   `knowledge/ui_reference/migration_report/screenshots/desktop_v2_final/01_desktop_full.png`

---

## Files modified

- `applications/customer_portal/src/screens/canonical_desktop/PortalPage.tsx`
- `applications/customer_portal/src/screens/canonical_desktop/rows/Row01.tsx`
- `applications/customer_portal/src/screens/canonical_desktop/rows/Row02.tsx`
- `applications/customer_portal/src/screens/canonical_desktop/rows/Row03.tsx`
- `applications/customer_portal/src/screens/canonical_desktop/rows/Row04.tsx`
- `applications/customer_portal/src/screens/canonical_desktop/rows/RowGridCell.tsx`
- `applications/customer_portal/src/styles/canonical-desktop.css` (grid helpers `--3` / `--5` / `--eq` only)

Design System markdown under `knowledge/design_system/` was **not** modified.

---

## Tests

- `npm run typecheck` — pass  
- `npm test -- tests/js/canonical_desktop.test.tsx` — pass (1)

---

## Lock rule

After Product Owner approval of this layout:

- Do **not** reorder sections
- Do **not** change column counts for Sections A/B/C
- Do **not** reintroduce equal-height stretch
- Any visual change requires a new canonical version (V3+), not edits to locked V2 layout
