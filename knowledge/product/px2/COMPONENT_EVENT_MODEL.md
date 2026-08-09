# Component Event Model

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2

---

## 1. Purpose

Events change **view state** or request **page-level actions**.  
They never recalculate Report truth.

---

## 2. Event catalog

| Event | Emitter | Consumer | Effect |
|-------|---------|----------|--------|
| `onPrimaryCta` | Recommendation region | ResultPage / product shell | Primary action if enabled |
| `onSecondaryCta` | Recommendation region | ResultPage | Secondary action if enabled |
| `onToggle` | Rec / Warning / Analysis / Knowledge card | Parent state | Flip `expanded` |
| `onToggleSection` | Technical / Knowledge headers | Parent | Flip section `collapsed` |
| `onToggleTable` | ChartCard | Charts | Flip `table_expanded` |
| `onNavigate` | InPageNav / Summary jump | ResultPage | Scroll to section |
| `onRetry` | ErrorStateCard | ResultPage | Retry scope |
| `onNext` | EmptyStateCard | ResultPage | Navigate to next useful section |

No `onRecalculate`. No `onFetchEngine`.

---

## 3. Payload rules

- Include instance `id` or index when toggling lists  
- Include `expanded` / `collapsed` target boolean  
- Never include Report snapshots  
- Never include engine errors raw  

---

## 4. CTA events

| Condition | Event behavior |
|-----------|----------------|
| Primary disabled | Do not emit `onPrimaryCta` |
| Page loading / exporting / printing | Do not emit CTA |
| Page error | Only `onRetry` |
| Duplicate Primary controls | Forbidden — one emitter |

---

## 5. Expand events vs content

Expand reveals already-bound `detail` / `body` / `table`.  
It must not trigger adapter re-bind that invents fields.

If detail is null, expand control is hidden (not an error).

---

## 6. Navigation events

`target_ui_id` values:

`Summary` · `Recommendation` · `Warnings` · `DomainCareer` · `DomainWealth` · `DomainRelationship` · `DomainHealth` · `DomainLuck` · `Charts` · `Technical` · `Knowledge` · `Appendix`

Skip hidden sections.

---

## 7. Stop line

Events steer attention. They do not create meaning.

END
