# Product Risk Register

| Field | Value |
|-------|-------|
| Document | PRODUCT_RISK_REGISTER |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Product Owner |

Likelihood and impact: **H** high · **M** medium · **L** low.

This register is product risk, not an engineering threat model.

---

## R-001 Knowledge dump

| Field | Value |
|-------|-------|
| Risk | Consultation fills with glossary, catalogues, or unmatched lists. Customer receives a textbook. |
| Likelihood | H |
| Impact | H |
| Mitigation | Published Narrative admit/drop/appendix. Editorial FAIL on glossary in Executive and Professional. Appendix remains a separate edition. |
| Owner | Chief Editor + narrative/publish owner |

---

## R-002 Template collapse

| Field | Value |
|-------|-------|
| Risk | Different people receive the same recommendations, warnings, or thesis with names swapped. Product looks automated and untrustworthy. |
| Likelihood | H |
| Impact | H |
| Mitigation | Cross-case editorial review on Golden Dataset. Duplicate recommendation FAIL. Case-specific impact required. |
| Owner | Chief Editor |

---

## R-003 Engine leakage

| Field | Value |
|-------|-------|
| Risk | Customer prose contains calculator language, internal labels, or unexplained technical tokens. |
| Likelihood | H |
| Impact | H |
| Mitigation | Editorial Standard. Commercial FAIL. Release checklist item “No engine language.” |
| Owner | Chief Editor |

---

## R-004 Narrative duplication

| Field | Value |
|-------|-------|
| Risk | The same meaning is printed as summary, core, career, and conclusion. The reading feels long without becoming clearer. |
| Likelihood | H |
| Impact | M |
| Mitigation | Principle “Do not duplicate knowledge.” Professional edition must not reprint Executive summary as core. Ranked recommendations once. |
| Owner | Narrative owner + Product Owner |

---

## R-005 Editorial drift

| Field | Value |
|-------|-------|
| Risk | Later releases slowly ignore ES-V1 because tests pass and PDFs still generate. |
| Likelihood | M |
| Impact | H |
| Mitigation | Artifact First. Editorial gate on every release. No customer-ready claim from test PASS. |
| Owner | Chief Editor + Product Owner |

---

## R-006 Architecture creep

| Field | Value |
|-------|-------|
| Risk | Beta “improvements” add engines, publishers, composers, canons, or layers. The platform is redesigned instead of the consultation. |
| Likelihood | M |
| Impact | H |
| Mitigation | PD-006. Architecture change requires Product Owner approval before work starts. Beta 0 lock. |
| Owner | Product Owner + Architecture Board |

---

## R-007 Regression

| Field | Value |
|-------|-------|
| Risk | A later build changes frozen truth or degrades Golden PDFs while tests still pass. |
| Likelihood | M |
| Impact | H |
| Mitigation | Regenerate Golden, Executive, and Professional PDFs every Beta release. Compare as product, not as test snapshots edited to match. |
| Owner | Product Owner + Release Manager |

---

## R-008 Customer confusion

| Field | Value |
|-------|-------|
| Risk | The customer cannot answer who they are, what it means now, or what to do next. Or they believe BTE promised fate, income, or medical outcomes. |
| Likelihood | H |
| Impact | H |
| Mitigation | Vision and packaging: consultant, not oracle. Bounded claims. Readable before complete. Customer Pilot before Production. |
| Owner | Product Owner |

---

## Additional tracked risks

| ID | Risk | L | I | Mitigation | Owner |
|----|------|---|---|------------|-------|
| R-009 | Child or young cases spoken to as career clients | M | H | Life-stage editorial check on Golden set | Chief Editor |
| R-010 | Case identity collision (same CASE id, different people) | M | H | Use editorial IDs EV-0001–EV-0010; never invent names | Product Owner |
| R-011 | Declaring customer-ready while all editorial cases are NO | M | H | Signoff required; baseline recorded in Beta 0 | Product Owner |
| R-012 | Dual analytical truth across layers | L | H | One owner per truth; publishing may not recalculate | Architecture Board |

---

## Review

This register is reviewed at each Beta release and at any Architecture change request.
New product risks are added here, not only in sprint notes.
