# BETA0 Editorial Lock

| Field | Value |
|-------|-------|
| Document | BETA0_EDITORIAL_LOCK |
| Date | 2026-08-17 |
| Status | **FROZEN** |
| Owner | BTE Chief Editor |
| Constitution | `knowledge/editorial/BTE_EDITORIAL_STANDARD_V1.md` (ES-V1, Official, 2026-08-16) |

Editorial decides whether a sentence may reach a paying customer.
It does not calculate truth.
It does not own engines.
It does not invent architecture.

---

## Frozen standard

ES-V1 is the editorial constitution of every customer-facing BTE report.

The governing question:

```
May this sentence reach a paying customer?
```

If the sentence does not help one human understand themselves, decide, or act, it does not ship.

---

## Ownership

| Surface | Owner |
|---------|-------|
| Editorial Standard V1 | BTE Chief Editor |
| Editorial validation cases EV-0001 … EV-0010 | Chief Editor + Product Owner |
| Product review of PDFs | Product Owner with Chief Editor |
| Engine language, glossary dump, duplicate recommendations, broken fragments | Editorial gate — must FAIL the release |

---

## Frozen gates (must FAIL a Beta release)

- Engine language in customer prose
- Glossary / encyclopedia dump in consultation editions
- Duplicate recommendations
- Broken fragments
- READY_FOR_CUSTOMERS claimed without Product Owner approval

---

## Current editorial fact (frozen, not rewritten)

As of 2026-08-16 Golden Dataset Editorial Validation:

- 10 named/bound real cases reviewed
- READY_FOR_CUSTOMERS = **NO** for all ten
- Mean overall editorial score **40.6**
- Verdict then: `READY_FOR_PRODUCT_REPAIR_PLANNING` (provisional)

Beta 0 freezes this baseline.
It does **not** declare the product customer-ready.
Repair during Beta is Editorial / Product Improvement inside frozen architecture.

---

## Explicit prohibition

During Beta, do **not**:

- replace ES-V1 with a new editorial system
- move editorial rules into engine if/else
- treat tests PASS as editorial PASS

---

## Official status

**Editorial Standard and editorial ownership are frozen for Beta 0.**
