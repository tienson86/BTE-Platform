# TASK — S05 Phase 1 Completion Report

| Item | Value |
|------|-------|
| Task | **S05 Phase 1 — SỨC MẠNH MỆNH CỤC** |
| Reference | `CANONICAL_PORTAL_UI_DESKTOP_V1.png` + `S05_MASTER_LAYOUT.md` |
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

`knowledge/ui_reference/migration_report/screenshots/s05_phase1/01_s05_only.png`

---

## Files Modified

| File | Change |
|------|--------|
| `applications/customer_portal/src/screens/canonical_desktop/sections/S05ChartStrength.tsx` | **New** isolated S05 Decision Card |
| `applications/customer_portal/src/screens/canonical_desktop/sections/Sections.tsx` | Re-export S05; remove legacy |
| `applications/customer_portal/src/screens/canonical_desktop/mockData.ts` | S05 decision-card mock |
| `applications/customer_portal/src/styles/canonical-desktop.css` | Replace S05 styles only |

**Not modified:** S00–S04 · S06–S11 · Header · Sidebar · Desktop Grid · Global tokens

---

## Implementation Summary

- One card: Header → Strength Level + Score → Insight (≤2 lines) → Progress → 4 Key Factors → CTA
- Level first (28px semantic color); score secondary (24px neutral)
- Flat horizontal bar · no gauge / pie / donut
- Exactly 4 factors with ✓
- Full-width CTA matching S01 button style
- Title typography aligned with S01–S04
- Card: padding 20 · radius 12 · border 1 · soft shadow
- Desktop only

---

## STOP

S05 Phase 1 complete. Do **not** start S06. Wait for Product Owner review.
