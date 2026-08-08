# 00 — Domain 01 Index · Career & Business

Version: 1.4  
Status: **DOMAIN 01 · PRODUCTION WIRING — Career Selection Assessment = Production Capability V1**  
Date: 2026-08-08  
Depends on: Wave 1.1 frozen · Capability Model · Sprint C SEL complete  
Scope: Production wiring only (no new KUs; no Promotion)  

---

## 1. Purpose

Establish **Domain 01 — Career & Business** as a complete commercial consultation **domain + capability** model for BTE.

- Sprint A: how the domain is structured (subdomains, decisions, KU slots, cases).  
- Sprint A.5: how the domain is sold/consumed as **capabilities** (services).  
- Sprint B–C: Career Selection Assessment content complete.  
- **This release:** wire CAP-D1-CA-SEL into the production Result pipeline.

---

## 2. Reading order

| Order | File | Content |
|------:|------|---------|
| 0 | `00_DOMAIN_INDEX.md` | This index |
| 1 | `01_DOMAIN_ARCHITECTURE.md` | Scope & subdomain map |
| 2 | `02_CONSULTATION_QUESTIONS.md` | Real customer questions |
| 3 | `03_DECISION_MODEL.md` | Decision → Evidence → Knowledge → Narrative |
| 4 | `04_KNOWLEDGE_REQUIREMENTS.md` | Required KU slots (P0/P1/P2) — no content |
| 5 | `05_GOLDEN_CASE_PLAN.md` | Domain Golden Cases |
| 6 | `06_CONSULTATION_JOURNEY.md` | End-to-end consult flow |
| 7 | `07_BUSINESS_OUTCOMES.md` | Commercial outcomes for BTE |
| 8 | `08_CROSS_DOMAIN_DEPENDENCIES.md` | Ties to Wave 1.1 & other domains |
| 9 | `09_DOMAIN_CAPABILITIES.md` | Business capability catalog |
| 10 | `10_CAPABILITY_KNOWLEDGE_MAPPING.md` | Capability → KU → Bundle → Narrative → Portal → API |
| 11 | `11_CAPABILITY_MATURITY_MODEL.md` | Levels 1–5 + current/target |
| 12 | `12_CAPABILITY_API_CONTRACT.md` | Future public capability contract (design) |
| 13 | `13_CAPABILITY_ROADMAP.md` | Phase 1–3 implementation plan |
| 14 | `14_IMPLEMENTATION_REPORT.md` | Sprint B P0 authoring report |
| 15 | `15_GOLDEN_CASE_RESULTS.md` | Offline Golden Case results |
| 16 | `16_REMAINING_GAPS.md` | Wiring + P1/P2 gaps |
| 17 | `17_CAPABILITY_COMPLETION_REPORT.md` | Career Selection completion |
| 18 | `18_ACCEPTANCE_TEST_RESULTS.md` | SEL acceptance tests |
| 19 | `19_REMAINING_GAPS.md` | Post-SEL gaps |
| 20 | `20_PRODUCTION_WIRING_REPORT.md` | Production wiring |
| 21 | `21_PRODUCT_DEMO_REPORT.md` | Before → After demo |
| 22 | `22_PRODUCTION_VALIDATION.md` | Golden Cases + tests |
| 23 | `23_RELEASE_NOTES.md` | Production Capability V1 notes |

**Reviewers (Sprint A):** 00 → 01 → … → 08.  
**Reviewers (Sprint A.5):** 09 → 10 → 11 → 12 → 13.  
**Reviewers (Sprint B):** 14 → 15 → 16.  
**Reviewers (Sprint C):** 17 → 18 → 19.  
**Reviewers (Production wiring):** 20 → 21 → 22 → 23.

---

## 3. Domain identity

| Field | Value |
|-------|-------|
| Domain pack id | `DOMAIN-01` |
| Commercial name | Career & Business |
| Model domains spanned | **CK-CA**, **CK-BU**, **CK-LE** (primary); **CK-DM**, **CK-LU**, **CK-ED**, **CK-FI** (supporting) |
| Primary scenarios | CS-CA, CS-CC, CS-PR, CS-BU, CS-ST, CS-ENP, CS-LE |
| Primary decisions | DS-CC, DS-PR, DS-BP (+ career-select / founder postures) |
| Capabilities | CAP-D1-* (see `09`) |
| Production live | **CAP-D1-CA-SEL** only |
| Depends on | Wave 1.1 core (Identity / Strength / Weakness / Useful God / Core Rec) |

---

## 4. Position in V1 stack

```
Wave 1.1 Core (frozen)
        ↓
Domain 01 architecture + capabilities (frozen)
        ↓
Career Selection Assessment content (Sprint C · frozen)
        ↓
Production wiring (this release) → Result Page
        ↓
Product Review gate → (later) Promotion Readiness
```

Capability = business service orchestrating Knowledge + Decisions + Narrative + Golden Cases.  
Not a new Engine. Not a Knowledge Unit. Not Narrative itself.

---

## 5. Non-goals (this release)

- Authoring new Knowledge Units  
- Modifying Wave 1.1 content  
- Foundation / Design System / Visual Language / Result layout  
- Interpretation Engine / Score Engine changes  
- Promotion Readiness or other Domain 01 capabilities  

---

## 6. Success criteria

| Criterion | Met by |
|-----------|--------|
| Domain capabilities defined | `09` |
| Capability mapping completed | `10` |
| Career Selection content complete | `17`–`19` |
| Production wiring | `20` |
| Product demo | `21` |
| Production validation | `22` |
| Release notes | `23` |

---

## 7. Stop line

**Career Selection Assessment = Production Capability V1.**  

**Do not start Promotion Readiness. Wait for Product Review.**

---

END
