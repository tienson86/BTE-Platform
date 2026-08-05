# Canonical UI Migration Report

**Product:** BTE Platform V1.0  
**Date:** 2026-08-05  
**Mode:** Release — UI only (no Integration)  
**Status:** Ready for Product Owner Review  

---

## Summary

Portal React UI (`applications/customer_portal`) đã được tái bố cục theo **Canonical Portal UI** principles:

- Reference: `knowledge/ui_reference/CANONICAL_PORTAL_UI.png`
- Baseline: `knowledge/ui_reference/CURRENT_PORTAL_UI.png`
- Principles: `UI_DESIGN_PRINCIPLES.md` + `CANONICAL_PORTAL_UI.md`

**Không** copy pixel. **Không** đổi Design System / Theme / Component API / Business Logic.  
**Không** API · Backend · Engine · TASK_003A (vẫn tạm dừng).

---

## Information Flow (After)

1. Executive Summary  
2. BaZi Overview  
3. Four Pillars  
4. Five Elements  
5. Strength (+ Dụng/Kỵ glance)  
6. Ten Gods  
7. ShenSha  
8. Interpretation  
9. Knowledge  

Shell: **Top primary nav** + **MỤC LỤC** TOC sidebar.

---

## Files Modified

### Layout / Navigation
- `src/layouts/AppLayout.tsx`
- `src/layouts/Header/Header.tsx`
- `src/layouts/Sidebar/Sidebar.tsx`
- `src/layouts/Navigation/navItems.ts`
- `src/layouts/Navigation/PrimaryNav.tsx` *(new)*
- `src/layouts/Navigation/index.ts`

### BaZi Result
- `src/screens/bazi/BaZiResultScreen.tsx`
- `src/screens/bazi/ExecutiveSummaryCard.tsx`
- `src/screens/bazi/BaZiResultHeader.tsx`
- `src/screens/bazi/FourPillarsCard.tsx`
- `src/screens/bazi/FiveElementsCard.tsx` *(order only)*
- `src/screens/bazi/StrengthCard.tsx` *(order only)*
- `src/screens/bazi/TenGodsCard.tsx`
- `src/screens/bazi/ShenShaCard.tsx`
- `src/screens/bazi/InterpretationCard.tsx`
- `src/screens/bazi/KnowledgeCard.tsx`
- `src/screens/bazi/SpiritGodsRow.tsx` *(new)*
- `src/screens/bazi/CoreAnalysisSection.tsx` *(kept for reuse)*
- `src/screens/bazi/mockData.ts`
- `src/screens/bazi/index.ts`

### Dashboard
- `src/screens/DashboardScreen.tsx`
- `src/screens/dashboard/*` *(structure / TOC anchors)*

### Styles
- `src/styles/app-shell.css`
- `src/styles/bazi-result.css`
- `src/styles/dashboard.css`

### Docs
- `knowledge/ui_reference/UI_CHANGELOG.md`
- `knowledge/roadmap/SPRINTS/SPRINT_01_5_INTEGRATION/TASK_003A_FRONTEND_BACKEND.md` *(CANCELLED / paused)*

### Adapter (shape compat only)
- `src/adapters/baziResultAdapter.ts`

---

## Screens Updated

| Screen | Status |
|--------|--------|
| BaZi Result | ✅ Canonical information flow |
| Dashboard | ✅ Canonical shell + section hierarchy |
| Report / Settings / History / Account | ⏳ Placeholder nav only |

---

## Responsive

| Viewport | Evidence |
|----------|----------|
| Desktop 1440 | `03_after_bazi_result_desktop.png` |
| Tablet 768 | `04_after_bazi_result_tablet.png` |
| Mobile 390 | `05_after_bazi_result_mobile.png` |

Breakpoints: metrics/pillars 4→2→1; strength row stacks; TOC drawer on mobile.

---

## Screenshot Before

| File | Description |
|------|-------------|
| `screenshots/01_before_current_portal.png` | Copy of `CURRENT_PORTAL_UI.png` (baseline / legacy) |
| `screenshots/00_canonical_reference.png` | Copy of `CANONICAL_PORTAL_UI.png` (PO layout target) |

---

## Screenshot After

| File | Description |
|------|-------------|
| `screenshots/02_after_dashboard_desktop.png` | Dashboard after migration |
| `screenshots/03_after_bazi_result_desktop.png` | BaZi Result — Canonical flow |
| `screenshots/04_after_bazi_result_tablet.png` | BaZi Result — tablet |
| `screenshots/05_after_bazi_result_mobile.png` | BaZi Result — mobile |

Path: `knowledge/ui_reference/migration_report/screenshots/`

---

## Build

**PASS** — `npm run build` (`tsc --noEmit`)

---

## TypeScript

**PASS**

---

## Tests

**PASS** — `tests/js/wave3_bazi_result.test.tsx` (3/3)

---

## Notes

1. Accent colors remain Design System tokens (emerald) — Canonical blue in reference is **layout cue**, not a new theme.
2. Mock data only. TASK_003A remains paused until UI Freeze.
3. Jinja runtime `:8081` is legacy shell; React Canonical lives in `customer_portal/src` (preview `:5177`).

---

## STOP

Migration complete for PO review.

**Next (human):** Product Owner Review → UI Freeze → Sprint 01.5 Integration.

**Not started:** TASK_003A · API · Backend · Engine.
