# DESKTOP V2 — Assembly Completion

**Status:** Assembled (layout shell only)  
**Date:** 2026-08-07  
**Preview:** `http://127.0.0.1:5177/?page=desktop`  
**Marker:** `data-canonical="desktop-v2"`

## Scope

Assemble approved modules **S00–S11** into one Desktop Result page per `CANONICAL_PORTAL_UI_DESKTOP_V2`.

No section redesign. No color/typography/internal spacing changes beyond layout tokens required by V2.

## Layout applied

| Token | Value |
|-------|-------|
| Gap / section gap | `24px` |
| Outer margin (content pad) | `32px` |
| Content max-width | `1600px` |
| Card radius | `16px` |

| Row | Modules | Grid |
|-----|---------|------|
| 1 | S00 | `1fr` (full) |
| 2 | S01 \| S02 \| S09 | `1fr 1fr 1fr` |
| 3 | S03 \| S04 \| S05 \| S10 | `4fr 4fr 2fr 2fr` |
| 4 | S06 \| S07 \| S08 \| S11 | `4fr 2fr 3fr 3fr` |

## Module constraints (verified)

| Module | Requirement | Status |
|--------|-------------|--------|
| S04 | Horizontal balance bars only | OK (5 tracks) |
| S06 | 10 ten-god cards (icon / name / score) | OK (reused approved) |
| S09 | Approved Bagua SVG only | OK (`Bagua_HauThien.svg`) |
| S11 | Title **BÁO CÁO TỔNG KẾT** | OK |

## Files modified

- `applications/customer_portal/src/screens/canonical_desktop/PortalPage.tsx`
- `applications/customer_portal/src/styles/canonical-desktop.css`
- `applications/customer_portal/tests/js/canonical_desktop.test.tsx` (marker `desktop-v1` → `desktop-v2` only)

## Components updated

- `PortalPage` — V2 shell wrapper (`cd-content__inner`), row structure, `data-canonical="desktop-v2"`
- Section components **reused unchanged** (S00–S11)

## Screenshots

- `knowledge/ui_reference/migration_report/screenshots/desktop_v2/01_desktop_full.png`
- `knowledge/ui_reference/migration_report/screenshots/desktop_v2/02_desktop_viewport_1920x1080.png`

Reference: `knowledge/ui_master/assets/CANONICAL_PORTAL_UI_DESKTOP_V2.png`

## Tests

- `npm run typecheck` — pass
- `npm test -- tests/js/canonical_desktop.test.tsx` — pass (1)

## Route note

There is no `applications/portal/` package. Desktop Result lives in `customer_portal` Canonical Desktop:

- Preview: `/?page=desktop`
- Same page is the Result screen for review

## Remaining issues

1. **Content width at 1920:** With sidebar `280px` + pad `32px×2`, content inner measures **~1576px** (not 1600). `max-width: 1600px` applies when the main column is wider. Not adjusted (no spacing redesign).
2. **Row stretch:** Narrow columns (S05/S10/S07) still stretch to row height via existing `align-items: stretch` — not changed.
3. **S11 not formally frozen** in this task (assembly only).
4. **Tablet/Mobile:** intentionally ignored.
