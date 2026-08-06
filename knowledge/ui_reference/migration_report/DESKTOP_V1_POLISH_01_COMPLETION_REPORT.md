# TASK_UI_POLISH_01 — Desktop UI Polish

## Completion Report

| Item | Value |
|------|-------|
| Task | **TASK_UI_POLISH_01** |
| Spec | `knowledge/01_DESKTOP/SPRINT_UI_POLISH_01.md` |
| Golden Reference | `knowledge/ui_master/assets/CANONICAL_PORTAL_UI_DESKTOP_V1.png` |
| Status | **Polish complete — awaiting Product Owner review** |
| Scope | Typography · White Space · Card · Shadow · Color · Visual Balance |

---

## Verdict

Same approved Desktop UI, refined visually. Layout / Grid / Navigation / Mock Data / Reading Flow unchanged.

Preview: `http://127.0.0.1:5177/?page=desktop`

---

## 1. Build Result

PASS — Vite preview serves polished `PortalPage`.

## 2. TypeScript Result

PASS — `npm run typecheck`

## 3. Test Result

PASS — `npm test -- tests/js/canonical_desktop.test.tsx` (1/1)

## 4. Desktop Screenshot

| File | Notes |
|------|-------|
| `knowledge/ui_reference/migration_report/screenshots/desktop_v1_polish/01_desktop_full.png` | Full page 1920 |
| `knowledge/ui_reference/migration_report/screenshots/desktop_v1_polish/02_desktop_viewport_1920x1080.png` | First viewport |

---

## 5. Files Modified

| File | Change |
|------|--------|
| `applications/customer_portal/src/styles/canonical-desktop.css` | Polish tokens: typography, gap/padding, radius, soft shadow, color system, sidebar gold active, section refinements |
| `applications/customer_portal/src/screens/canonical_desktop/sections/Sections.tsx` | S05 score hierarchy markup; S04 chart size; S07 group tones; S08 height class; restrained decorative colors |
| `knowledge/ui_reference/migration_report/DESKTOP_V1_POLISH_01_COMPLETION_REPORT.md` | This report |
| `knowledge/ui_reference/migration_report/screenshots/desktop_v1_polish/*` | Screenshots |

**Not modified:** Layout grid columns, component positions, navigation structure, mock business data, legacy Portal screens.

---

## 6. Polish Applied (by sprint section)

| Area | Change |
|------|--------|
| Typography | Unified section titles (700 / 0.5px / UPPERCASE / Primary). Card titles 600. Metadata lower opacity. Key numbers larger. |
| White Space | Section gap 20→30px. Card padding +6–8px. Content padding slightly increased. |
| Card Style | Radius 10→12px. Softer multi-layer shadow. |
| Color | Primary / Secondary / Success / Warning / Danger tokens. Ngũ Hành colors only for elements. |
| Sidebar | Dark burgundy; **Active = Gold**; Hover = dark gold; Warm white text. |
| S00 | Metadata lighter; context clearer. |
| S01 | Nhật Chủ 26px; stronger CTA. |
| S02 | Even card gaps / balanced tiles. |
| S03 | Ngày Trụ thicker border + larger glyphs. |
| S04 | Chart 140px; tighter legend. |
| S05 | `72` large / `/100` muted; thicker progress bar. |
| S06 | Taller chips; even gaps. |
| S07 | Grouped Cát / Hung / Đặc biệt panels. |
| S08 | Taller card; better line-height; stronger CTA. |
| S09 | Smaller bagua; balanced Nhóm Trạch. |
| S10 | `4 lượng 8 chỉ` larger emphasis. |
| S11 | Compact even list rows. |

---

## Acceptance Criteria

✓ Layout unchanged  
✓ Grid unchanged  
✓ Reading Flow unchanged  
✓ Typography refined  
✓ White Space improved  
✓ Cards softer  
✓ Premium / lighter feel  
✓ Business / mock data unchanged  

---

## STOP

Desktop Polish complete. Waiting for Product Owner review.

Do **not** start Tablet / Mobile / Responsive / Dark Mode until approved.
