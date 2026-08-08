# 07 — P0 Fix Report · Commercial V1 Polish Sprint B

Version: 1.0.0  
Status: **IMPLEMENTED — awaiting Product approval**  
Date: 2026-08-08  
Scope: Resolve P0-01 … P0-06 only — no new Capability / no Foundation redesign  

---

## 1. Summary

| ID | Resolution |
|----|------------|
| **P0-01** | Career Strategy is primary Recommendation; Promotion is secondary milestone |
| **P0-02** | Capability names exposed in existing Result slots (no new card/layout) |
| **P0-03** | Exec = 1 central + ≤3 supporting + 1 conclusion (Promotion excluded from Exec) |
| **P0-04** | Customer-facing commercialize layer replaces technical BaZi wording |
| **P0-05** | Primary Rec formatted as What / Why / How / When / Expected outcome |
| **P0-06** | Human Consulting Review package published (`10_HUMAN_CONSULTING_REVIEW_PACKAGE.md`) |

---

## 2. Implementation map

| Area | Change |
|------|--------|
| Presentation | `engines/commercial_knowledge/commercial_presentation.py` (new) |
| Retrieval | commercialize bound customer text |
| Signals | commercial default labels for useful_god / day_master / pattern |
| Narrative merge | Exec composition; Career primary; Promotion secondary |
| API truth | Attach Exec / primary / secondary / capability labels on `narrative_result` |
| Portal adapters | Prefer structured Exec/Rec; label both capabilities in existing slots |

**Not changed:** Foundation, Design System, Narrative Engine architecture, Wave 1.1 CSV content, new routes/cards.

---

## 3. Behavior after fix

```
Career Selection Assessment → Primary Career Strategy Rec
Promotion Readiness Assessment → Secondary career milestone
Executive Summary → structured short composition
Customer wording → commercial (technical optional via Knowledge zone depth)
```

---

## 4. Tests

```text
python -m pytest tests/domain01 tests/commercial_knowledge -q
41 passed
```

---

## 5. Remaining

- P0-06 requires **human** sign-off using package `10` (not closed by engineering alone).  
- P1 items from audit remain deferred.

---

## 6. Stop line

P0 engineering fixes complete. **Wait for Product approval.** Do not start new Capability.

---

END
