# TASK — S04 Phase 1 Completion Report

| Item | Value |
|------|-------|
| Task | **S04 Phase 1 — CÂN BẰNG NGŨ HÀNH** |
| Reference | `CANONICAL_PORTAL_UI_DESKTOP_V1.png` + `S04_MASTER_LAYOUT.md` |
| Status | **Complete — awaiting Product Owner review** |

---

## Results

| Check | Status |
|-------|--------|
| Build | **PASS** |
| TypeScript | **PASS** |
| Tests | **PASS** (`canonical_desktop.test.tsx` 1/1) |

---

## Screenshot

`knowledge/ui_reference/migration_report/screenshots/s04_phase1/01_s04_only.png`

---

## Files Modified

| File | Change |
|------|--------|
| `applications/customer_portal/src/screens/canonical_desktop/sections/S04ElementBalance.tsx` | **New** isolated S04 component |
| `applications/customer_portal/src/screens/canonical_desktop/sections/Sections.tsx` | Re-export S04; remove legacy S04 + ElementDonut |
| `applications/customer_portal/src/screens/canonical_desktop/mockData.ts` | S04 rows (order + status + summary) |
| `applications/customer_portal/src/styles/canonical-desktop.css` | Replace S04 styles only |

**Not modified:** S00 · S01 · S02 · S03 · S05–S11 · Header · Sidebar · Desktop Grid · Global tokens

---

## Implementation Summary

- One card: Header → 5 horizontal element rows → Summary
- Fixed order: Mộc → Hỏa → Thổ → Kim → Thủy
- Row: Name | Proportional bar | % | Status
- Status vocabulary: Rất mạnh / Mạnh / Trung bình / Yếu / Rất yếu
- Flat ngũ hành colors · rounded bars · no pie/donut/gauge/legend/tooltip
- Typography per master · padding 20 · gap 12 · radius 12 · soft shadow
- Desktop only

---

## STOP

S04 Phase 1 complete. Do **not** start S05. Wait for Product Owner review.
