# DESKTOP V2 — Row Architecture Refactor

**Status:** Complete  
**Date:** 2026-08-07  
**Spec:** `DESKTOP_ROW_SPEC.md` (+ LAYOUT / GRID / COMPONENT_MAPPING)

## 1. PortalPage architecture — before / after

### Before (incorrect framing)

```
PortalPage
└── .cd-content__inner
    ├── .cd-row (inline) → S00
    ├── .cd-row (inline) → S01 S02 S09
    ├── .cd-row (inline) → S03 S04 S05 S10
    └── .cd-row (inline) → S06 S07 S08 S11
```

Rows existed as CSS classes only — not as first-class Row container components.
Risk: easy to collapse back into one page-wide grid.

### After (required)

```
ResultPage / PortalPage
└── .cd-result-page          ← flex column stack (NOT a CSS Grid)
    ├── <Row01 />           ← owns .cd-row-grid → S00
    ├── <Row02 />           ← owns .cd-row-grid → S01 S02 S09
    ├── <Row03 />           ← owns .cd-row-grid → S03 S04 S05 S10
    └── <Row04 />           ← owns .cd-row-grid → S06 S07 S08 S11
```

## 2. Files modified / added

| File | Change |
|------|--------|
| `…/PortalPage.tsx` | Composes `Row01`–`Row04` only; exports `ResultPage` |
| `…/rows/Row01.tsx` | **Added** — S00 |
| `…/rows/Row02.tsx` | **Added** — S01 S02 S09 |
| `…/rows/Row03.tsx` | **Added** — S03 S04 S05 S10 |
| `…/rows/Row04.tsx` | **Added** — S06 S07 S08 S11 |
| `…/rows/RowGridCell.tsx` | **Added** — fixed span cell |
| `…/rows/index.ts` | **Added** |
| `…/index.ts` | Export `ResultPage`, rows |
| `…/styles/canonical-desktop.css` | Stack = flex; grid only inside `.cd-row-grid` |

Section components **not** modified.

## 3–4. Screenshots

- Viewport 1920×1080: `screenshots/desktop_v2/02_desktop_viewport_1920x1080.png`
- Full page: `screenshots/desktop_v2/01_desktop_full.png`

## 5. Row container hierarchy

```
.cd-result-page [display: flex; flex-direction: column]
│
├── Row01 (.cd-row-container--auto-height)
│   └── .cd-row-grid [display: grid; 12 cols]
│       └── ContextHeader (span 12) → S00
│
├── Row02 (.cd-row-container--equal-height)
│   └── .cd-row-grid [display: grid; 12 cols; align-items: stretch]
│       ├── LifeProfileCard (span 4) → S01
│       ├── OverviewCard (span 4) → S02
│       └── BaguaCard (span 4) → S09
│
├── Row03 (.cd-row-container--equal-height)
│   └── .cd-row-grid [display: grid; 12 cols; align-items: stretch]
│       ├── FourPillarsCard (span 4) → S03
│       ├── ElementBalanceCard (span 4) → S04
│       ├── StrengthCard (span 2) → S05
│       └── BoneWeightCard (span 2) → S10
│
└── Row04 (.cd-row-container--equal-height)
    └── .cd-row-grid [display: grid; 12 cols; align-items: stretch]
        ├── TenGodCard (span 4) → S06
        ├── ShenShaCard (span 2) → S07
        ├── SummaryCard (span 3) → S08
        └── FinalReportCard (span 3) → S11
```

## 6. Confirmation — no page-wide content grid

Runtime check (`data-architecture="independent-row-containers"`):

| Check | Result |
|-------|--------|
| `.cd-result-page` display | `flex` |
| `.cd-result-page` is CSS Grid | **false** |
| Row container count | **4** |
| Each `.cd-row-grid` display | `grid` (12 columns) |
| Row 4 begins after Row 3 | **true** |
| Equal height within Row 2 / 3 / 4 | **true** (identical cell heights) |
| Masonry / dense packing | not used |

## Tests

- `npm run typecheck` — pass
- `npm test -- tests/js/canonical_desktop.test.tsx` — pass (1)
