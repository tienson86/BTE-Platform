# Product Acceptance Policy

| Field | Value |
|-------|-------|
| Document | PRODUCT_ACCEPTANCE_POLICY |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Product Owner |

Acceptance is a chain of gates.
Passing an earlier gate does not pass a later one.

---

## 1. Gates

```
Engineering
    ↓
Editorial
    ↓
Commercial
    ↓
Product Owner
    ↓
Customer Pilot
    ↓
Accepted for the intended release state
```

Customer Pilot is required before Production.
It is not required to enter Beta, but named real cases already under editorial review are the Beta substitute for a public pilot.

---

## 2. Engineering gate

**Question:** Does the frozen path produce a correct, reproducible artifact from the stated birth data?

| Pass | Fail |
|------|------|
| Analytical owners unchanged; truth copied, not recalculated | Dual truth, silent fallback, or unreproducible PDF |
| Module tests of the touched surface pass | Tests used as the only evidence of quality |
| No new subsystem introduced without approval | Architecture change hidden as a fix |

Engineering PASS means the machine worked.
It does not mean the consultation may be sold.

---

## 3. Editorial gate

**Question:** May these sentences reach a paying customer?

Owner: Chief Editor, under Editorial Standard V1.

| Pass | Fail |
|------|------|
| Language is consultant-grade | Engine language |
| Consultation is not a glossary | Encyclopedia dump on Executive or Professional |
| Recommendations are ranked and unique | Duplicate recommendations |
| Fragments read as finished prose | Broken fragments, truncated lists, template collapse |

Editorial FAIL blocks Commercial and Product Owner.
There is no editorial waiver by test score.

---

## 4. Commercial gate

**Question:** Would BTE sell this consultation at the stated package?

| Pass | Fail |
|------|------|
| Recognition, understanding, and action are present | Score dump, module stack, or unexplained labels |
| Claims are bounded | Guaranteed luck, income, title, medical, or legal outcomes |
| Edition matches the offer (Executive vs Professional) | Professional content sold as unmarked default without decision |
| Named real case, not synthetic | Synthetic or anonymous fixture used as commercial proof |

---

## 5. Product Owner gate

**Question:** May this artifact or release carry the BTE name?

Owner: Product Owner.

| Pass | Fail |
|------|------|
| Recorded signoff on the artifact and, if issuing, the release | Implied, chat, or “looks good” approval |
| Change class is legal for the current phase | Architecture change started without prior approval |
| Definition of Done complete | Completion Report offered as Done |

No release, freeze acceptance, or customer-ready claim without this gate.

---

## 6. Customer Pilot gate

**Question:** Does a real intended customer (or appointed consulting reviewer standing in for one) accept the consultation as usable?

| Pass | Fail |
|------|------|
| Named case, real birth data, reviewed as a reading | Internal-only enthusiasm |
| Confusion, offence, or unused advice logged | Silence treated as acceptance |
| Required before Production | Production declared from laboratory scores |

Until this gate passes, the product may be in Beta or Release Candidate.
It is not Production.

---

## 7. Capability overlay

Commercial capabilities also satisfy `04_CAPABILITY_ACCEPTANCE_STANDARD.md`.
That standard cannot weaken this policy.
If both apply, both must pass.
