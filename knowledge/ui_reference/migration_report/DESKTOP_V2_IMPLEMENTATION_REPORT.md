# DESKTOP V2 — Implementation Report

**Status:** Implemented against locked Design System  
**Date:** 2026-08-07  
**Preview:** `http://127.0.0.1:5177/?page=desktop`  
**Marker:** `data-canonical="desktop-v2"`

## Source of truth

| Document | Role |
|----------|------|
| `DESKTOP_LAYOUT_SPEC.md` | Row order + column spans |
| `DESKTOP_GRID_SPEC.md` | 12-col grid, spacing, container |
| `DESKTOP_COMPONENT_MAPPING.md` | Section → component mapping |
| `CANONICAL_PORTAL_UI_DESKTOP_V2.md` | Canonical identity (companion) |

## Layout implemented

| Token | Spec | Implemented |
|-------|------|-------------|
| Grid | `repeat(12, 1fr)` | `repeat(12, minmax(0, 1fr))` |
| Gap | `24px` | `24px` |
| Outer pad L/R | `32px` | `32px` |
| Top/bottom margin | `24px` | `24px` (content padding) |
| Content max-width | `1600px` | `1600px` |
| Card radius | `16px` | `16px` |
| Shared `.cd-card` pad | `24px` | `24px` |
| Auto-flow | row / disabled pack | `grid-auto-flow: row` |
| Masonry | forbidden | not used |

| Row | Modules | Spans |
|-----|---------|-------|
| 1 | S00 | 12 |
| 2 | S01 \| S02 \| S09 | 4 \| 4 \| 4 |
| 3 | S03 \| S04 \| S05 \| S10 | 4 \| 4 \| 2 \| 2 |
| 4 | S06 \| S07 \| S08 \| S11 | 4 \| 2 \| 3 \| 3 |

## Component mapping (reused modules)

| Spec name | Existing component |
|-----------|-------------------|
| ContextHeader | `S00ContextHeader` |
| LifeProfileCard | `S01IdentityDecision` |
| OverviewCard | `S02OverviewActions` |
| BaguaCard | `S09CungPhi` |
| FourPillarsCard | `S03FourPillars` |
| ElementBalanceCard | `S04ElementBalance` |
| StrengthCard | `S05Strength` |
| BoneWeightCard | `S10CanXuong` |
| TenGodCard | `S06TenGods` |
| ShenShaCard | `S07ShenSha` |
| SummaryCard | `S08Interpretation` |
| FinalReportCard | `S11ReportSummary` |

`data-component` attributes on grid cells mirror the mapping names. Section internals unchanged.

## Special requirements

| Module | Requirement | Status |
|--------|-------------|--------|
| S04 | Horizontal bars only | OK (5 bars) |
| S06 | 10 cards: icon / name / score | OK |
| S09 | Approved Bagua SVG | OK (`Bagua_HauThien.svg`) |
| S11 | Title **BÁO CÁO TỔNG KẾT** | OK (mock title updated) |

## Screenshots

- `screenshots/desktop_v2/02_desktop_viewport_1920x1080.png`
- `screenshots/desktop_v2/01_desktop_full.png`

## Tests

- `npm run typecheck` — pass
- `npm test -- tests/js/canonical_desktop.test.tsx` — pass (1)

## Deviations

1. **Content width at 1920:** Main column after sidebar (280) + L/R pad (32×2) yields **~1576px** inner width; `max-width: 1600px` cannot engage until the main column is wider. Sidebar width is outside DESKTOP_GRID_SPEC and was not changed.
2. **Canonical doc status:** `CANONICAL_PORTAL_UI_DESKTOP_V2.md` is still marked PLACEHOLDER in Design System; layout/grid/mapping docs are CANONICAL and were followed.
3. **Folder path:** Mapping recommends `applications/portal/`; implementation remains under `applications/customer_portal/` (existing architecture).
4. **Section-internal padding:** Approved module cards keep their frozen internal paddings (not force-normalized to 24px) to avoid visual redesign of S00–S11.

## Out of scope

- Tablet / Mobile
- Typography / color redesign
- Masonry or auto-packing
- New components / IA changes
