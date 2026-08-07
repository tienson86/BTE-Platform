# Desktop V2 Visual Polish (Backlog)

> Status: BACKLOG
>
> Do not resume polish iterations unless product explicitly reopens Desktop V2 UI.

---

## Remaining issues (not blocking engine integration)

| ID | Area | Issue | Notes |
|----|------|-------|-------|
| VP-01 | Row A (S01/S03/S09) | Residual height parity is still partly driven by row stretch, not pure content height | Accept for freeze; revisit only with measured screenshots |
| VP-02 | Header language | S04–S11 still use per-module `__title` / `cd-section-title` instead of `ModuleHeader` | Visual close; unify class when UI reopens |
| VP-03 | Header color | Spec `#B91C1C` on `cd-module-header`; older modules still use `#9a1b1b` / `--cd-primary` | Minor inconsistency |
| VP-04 | S09 title size | S09 overrides title to 16px | Out of scope for last polish pass |
| VP-05 | After screenshots | Automated after-capture not completed in polish session | Capture when portal preview host is available |
| VP-06 | S02 optical center | Uses `margin-block: auto` under stretched row cell | Prefer content-sized card if row rhythm is revisited |

---

## Explicitly out of scope

- Redesigning dashboard layout
- Moving modules between rows
- Changing mock/demo copy for visual reasons
- Equal-height hacks / spacer divs / hardcoded heights

---

END
