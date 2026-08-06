# S09 Final Hotfix

| Item | Value |
|------|-------|
| Task | **S09 Final Hotfix** |
| Status | **Complete — awaiting Product Owner freeze** |
| Date | **2026-08-06** |

---

## Scope

Final layout polish only.

- `Bagua_HauThien.svg` **not** modified
- Geometry / colors / component tree / business logic **unchanged**

---

## Adjustments

| Area | Change |
|------|--------|
| Bagua scale | 132 → **148px** (~+12%, target 145–150) |
| Grid column | 140 → **156px** (~40% visual bagua / 60% info) |
| Center title | 13 → **14** (+≈10%) |
| Center number | 18 → **21** (+≈15%) |
| Info line-height | 1.55 → **1.65** |
| Quai → Nhóm Trạch gap | 14 → **7px** (−7px) |

---

## Screenshot

`knowledge/ui_reference/migration_report/screenshots/s09_phase2/01_s09_only.png`

---

## Files

| File | Change |
|------|--------|
| `canonical-desktop.css` | S09 scale / spacing / line-height |
| `S09FengShuiGuidance.tsx` | Display size + center overlay scale |

---

## Verification

| Check | Result |
|-------|--------|
| Typecheck | PASS |
| Tests | PASS |
| Build | PASS |

---

## Freeze note

After Product Owner approval, S09 is permanently frozen for Desktop Canonical UI V1.
