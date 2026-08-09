# Component State Model

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2

---

## 1. Universal states

Every Result component defines:

| State | Meaning |
|-------|---------|
| `loading` | Waiting for bind |
| `ready` | Bound, displayable |
| `empty` | Bound, no content |
| `collapsed` | Ready but section/detail closed |
| `expanded` | Detail open |
| `warning` | Ready with caution severity |
| `error` | Bind/display failed |
| `disabled` | Visible, not interactive |
| `hidden` | Not mounted / not painted |

A component occupies **one primary state**.  
`collapsed` / `expanded` are disclosure modifiers on `ready` (or `warning`).

See `states/component_states.md` for the machine.

---

## 2. Defaults (PX-1 + PX-2)

| Component | Default |
|-----------|---------|
| Hero | `ready` or page `error` |
| ExecutiveSummary | `ready` |
| Recommendation region | `ready` or `empty` |
| RecommendationCard | `ready` + detail `collapsed` |
| ImportantWarnings | `hidden` if no items; else `ready` / `warning` |
| DomainSection | `ready` or `empty` |
| AnalysisCard | `ready` + `collapsed` detail |
| Charts | `hidden` if none; else `ready` |
| TechnicalInfo | `ready` + section `collapsed` (or `empty` collapsed) |
| Knowledge | `hidden` if none; else section `collapsed` |
| Appendix | `hidden` if empty |
| CTA Primary | `disabled` while loading or `enabled=false` |

---

## 3. Transitions (normative)

```
hidden → loading → ready
                 → empty
                 → error

ready → collapsed ↔ expanded
ready → warning          (severity critical/attention; still readable)
ready → disabled         (CTA / exporting)
any ready/empty → hidden (visibility rules)
any → error
error → loading          (retry)
```

Forbidden: `empty → ready` without new bind.  
Forbidden: inventing content to escape `empty`.

---

## 4. Warning vs error

| State | When |
|-------|------|
| `warning` | Content present; severity attention/critical |
| `error` | Cannot display this unit honestly |

Empty is not warning. Empty is not error.

---

## 5. Disabled

Applies to controls (CTA, retry), not to reading surfaces.

Disabled Primary stays visible. Do not hide it and spawn another Primary.

---

## 6. Hidden

Hidden means **no blank card**.  
Not a white empty shell.

---

## 7. Stop line

State is presentation. Report data does not change when expanded.

END
