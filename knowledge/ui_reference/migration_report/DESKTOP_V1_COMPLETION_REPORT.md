# TASK_UI_IMPLEMENTATION_001 — Desktop Canonical UI

## Completion Report

| Item | Value |
|------|-------|
| Task | **TASK_UI_IMPLEMENTATION_001** |
| Scope | Desktop Canonical UI — full page |
| Golden Reference | `knowledge/ui_master/assets/CANONICAL_PORTAL_UI_DESKTOP_V1.png` |
| Status | **Implemented — awaiting Product Owner visual review** |
| Language | 100% Vietnamese |
| Backend | None (static mock data) |

---

## Verdict

Built **from scratch** as an isolated module. Legacy Portal (`BaZiResultScreen`, `AppLayout`, `bazi/*`) was **not** modified for this layout.

Preview: `http://127.0.0.1:5177/?page=desktop`

---

## 1. Build Result

PASS — Vite preview serves `PortalPage` at `?page=desktop`.

## 2. TypeScript Result

PASS — `npm run typecheck` (tsc --noEmit) in `applications/customer_portal`.

## 3. Test Result

PASS — `npm test -- tests/js/canonical_desktop.test.tsx`

| File | Tests | Result |
|------|-------|--------|
| `tests/js/canonical_desktop.test.tsx` | 1 | PASS |

## 4. Desktop Screenshot

| File | Notes |
|------|-------|
| `knowledge/ui_reference/migration_report/screenshots/desktop_v1/01_desktop_full.png` | Full page, 1920×~1556, 100% |
| `knowledge/ui_reference/migration_report/screenshots/desktop_v1/02_desktop_viewport_1920x1080.png` | First viewport 1920×1080 |

Compare side-by-side with:

`knowledge/ui_master/assets/CANONICAL_PORTAL_UI_DESKTOP_V1.png`

---

## 5. Files Modified / Added

### New (canonical module — isolated)

| Path | Role |
|------|------|
| `applications/customer_portal/src/screens/canonical_desktop/PortalPage.tsx` | Root page |
| `applications/customer_portal/src/screens/canonical_desktop/index.ts` | Barrel |
| `applications/customer_portal/src/screens/canonical_desktop/mockData.ts` | Static Vietnamese mock |
| `applications/customer_portal/src/screens/canonical_desktop/icons.tsx` | Inline SVG icons |
| `applications/customer_portal/src/screens/canonical_desktop/shell/PortalChrome.tsx` | Header / Sidebar / Footer |
| `applications/customer_portal/src/screens/canonical_desktop/sections/Sections.tsx` | S00–S11 |
| `applications/customer_portal/src/styles/canonical-desktop.css` | Desktop-only styles |
| `applications/customer_portal/tests/js/canonical_desktop.test.tsx` | Smoke test |

### Wiring only (no legacy layout rewrite)

| Path | Change |
|------|--------|
| `applications/customer_portal/src/screens/index.ts` | Export `PortalPage` |
| `knowledge/release_review/review_01/preview/main.tsx` | `?page=desktop` route |

### Screenshots / report

| Path | Role |
|------|------|
| `knowledge/ui_reference/migration_report/screenshots/desktop_v1/*` | Screenshots |
| `knowledge/ui_reference/migration_report/DESKTOP_V1_COMPLETION_REPORT.md` | This report |

---

## 6. Component Tree (implemented)

```
PortalPage
├── PortalSidebar
├── PortalHeader
├── PortalContent
│   ├── S00 Context Header
│   ├── Row: S01 | S02 | S09
│   ├── Row: S03 | S04 | S05 | S10
│   └── Row: S06 | S07 | S08 | S11
└── PortalFooter
```

Section order matches the approved Canonical Desktop image (S00–S11).

---

## 7. Explicitly NOT done (per STOP condition)

- Tablet / Mobile
- Dark Mode
- Animations
- Accessibility improvements beyond basic landmarks
- Backend integration
- Refactor of legacy Portal
- Responsive breakpoints

---

## 8. Review checklist for Product Owner

□ Header matches canonical  
□ Sidebar (maroon + gold) matches canonical  
□ S00–S11 present and ordered as in image  
□ Grid rows match (3 / 4 / 4 cards)  
□ Vietnamese labels intact  
□ No legacy BaZi Result chrome  

**Decision needed:** PASS / PASS WITH CHANGES / REJECT

---

## STOP

Desktop implementation delivered. Waiting for Product Owner review before any Tablet / Mobile / Responsive work.
