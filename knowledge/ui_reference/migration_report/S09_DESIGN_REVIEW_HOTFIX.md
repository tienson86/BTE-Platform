# S09 Design Review Hotfix

| Item | Value |
|------|-------|
| Task | **S09 Design Review Hotfix** |
| Status | **Complete** |
| Date | **2026-08-06** |

---

## Scope

Layout / visual polish only.

- Bagua SVG asset **not** modified
- Business logic **not** changed
- No redesign

---

## Adjustments

| Area | Change |
|------|--------|
| SVG scale | 88 → **132px** (same asset, larger display) |
| Two-column grid | `96px 1fr` → **`140px 1fr`** |
| Column gap | 16 → **18px** |
| Vertical rhythm | Quai → Nhóm Trạch margin 16 → **14px** |
| Bullet type | 12/1.6 → **13/1.55** |
| Center overlay | Title 13 / Number 18 (scaled with bagua) |
| Alignment | Bagua left-aligned in column; icons row unchanged |

---

## Screenshot

`knowledge/ui_reference/migration_report/screenshots/s09_phase2/01_s09_only.png`

---

## Files

| File | Change |
|------|--------|
| `applications/customer_portal/src/styles/canonical-desktop.css` | S09 layout polish |
| `applications/customer_portal/src/screens/canonical_desktop/sections/S09FengShuiGuidance.tsx` | Display size + center overlay scale |

Approved Bagua SVG unchanged.
