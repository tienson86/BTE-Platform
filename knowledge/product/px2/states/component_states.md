# Component States

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

Companion to `COMPONENT_STATE_MODEL.md`.

---

## 1. Per-component matrix

| Component | loading | ready | empty | collapsed | expanded | warning | error | disabled | hidden |
|-----------|:-------:|:-----:|:-----:|:---------:|:--------:|:-------:|:-----:|:--------:|:------:|
| ResultPage | ● | ● | ● | — | — | — | ● | — | — |
| Hero | ● | ● | — | — | — | — | ●* | — | ● loading |
| ExecutiveSummary | ● | ● | — | — | — | — | ●* | — | ● loading |
| Recommendation | ● | ● | ● | — | — | — | ● | — | — |
| RecommendationCard | — | ● | — | ● detail | ● detail | — | ● | — | — |
| ImportantWarnings | — | ● | — | — | — | ● | ● | — | ● if no items |
| WarningCard | — | ● | — | ● mitigation | ● | ● | ● | — | — |
| DomainSection | — | ● | ● | — | — | — | ● | — | — |
| AnalysisCard | — | ● | ● | ● | ● | — | ● | — | ● if no preview |
| Charts | — | ● | — | — | — | — | ● | — | ● if no items |
| ChartCard | — | ● | — | ● table | ● table | — | ● | — | — |
| TechnicalInfo | — | ● | ● | ● default | ● | — | ● | — | ● if nothing |
| Knowledge | — | ● | — | ● default | ● | — | ● | — | ● if no items |
| KnowledgeCard | — | ● | — | ● | ● | — | ● | — | — |
| Appendix | — | ● | — | — | — | — | ● | — | ● if empty |
| Primary CTA | — | ● | — | — | — | — | — | ● | ● page error/empty |

\* Hero/Summary invalid escalate to **page** error, not a local empty hero.

---

## 2. Entry defaults

See `COMPONENT_STATE_MODEL.md` §2.

---

## 3. Transition rules (all components)

1. `hidden` until parent mounts the unit  
2. `loading` only if page loading (PX-2: no independent fetch)  
3. After bind: `ready` | `empty` | `error` | `hidden`  
4. `collapsed` ↔ `expanded` only from `ready` or `warning`  
5. `disabled` only on controls  
6. Retry: `error` → parent `loading` → rebind  

---

## 4. Stop line

Nine named states. No custom ad-hoc flags beyond expand booleans.

END
