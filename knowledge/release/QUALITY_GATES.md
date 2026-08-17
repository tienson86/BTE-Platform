# Quality Gates

| Field | Value |
|-------|-------|
| Document | QUALITY_GATES |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Release Manager |
| Depends on | `knowledge/product/PRODUCT_ACCEPTANCE_POLICY.md` |

Gates run in order.
An earlier PASS does not create a later PASS.

```
Engineering Gate
    ↓
Editorial Gate
    ↓
Commercial Gate
    ↓
Product Gate
    ↓
Customer Pilot Gate
```

Customer Pilot is required for RC and Production.
For Beta, named real-case editorial and commercial review on the Golden Dataset is the appointed substitute. It is not public sale.

---

## 1. Engineering Gate

| Field | Value |
|-------|-------|
| Purpose | Confirm the frozen path produces a correct, reproducible artifact from stated birth data. |
| Owner | Engineering owner of the touched surface, with Architecture Board if ownership is in doubt. |

**Pass criteria**

- Analytical owners unchanged; truth copied, not recalculated
- Issue contains no unauthorised Engine, Framework, Matrix, Publisher, Composer, Canon, Layer, or Runtime component
- Touched-surface tests pass **and** are filed as supporting evidence only
- Artifact is reproducible from the same birth data

**Blockers**

- Dual truth across layers
- Silent fallback that changes the consultation
- Unreproducible PDF
- Architecture change hidden as a fix
- Tests offered as the only evidence

---

## 2. Editorial Gate

| Field | Value |
|-------|-------|
| Purpose | Confirm customer language may reach the intended audience for this state. |
| Owner | Chief Editor, Editorial Standard V1 |

**Pass criteria**

- Consultant-grade language
- No engine leaks
- No glossary dump on Executive or Professional
- No duplicate recommendations
- No broken fragments
- Life-stage of the case respected

**Blockers**

- Engine language in customer prose
- Encyclopedia or unmatched catalogues in the consultation
- Template collapse across cases
- **Professional PDF score below threshold** (threshold set by Chief Editor and Product Owner for that edition; a score below it is FAIL even if Engineering PASS)
- READY_FOR_CUSTOMERS claimed without this gate

---

## 3. Commercial Gate

| Field | Value |
|-------|-------|
| Purpose | Confirm the artifact is a consultation BTE would stand behind at the stated package and state. |
| Owner | Commercial reviewer |

**Pass criteria**

- Recognition, understanding, and ranked action are present
- Claims are bounded
- Edition matches the offer (Executive default; Professional only when selected)
- Named real cases; no synthetic proof

**Blockers**

- Score dump or module stack sold as consulting
- Guaranteed luck, income, title, medical, or legal outcomes
- Professional content shipped as unmarked default
- Commercial score or review FAIL on Golden anchors

---

## 4. Product Gate

| Field | Value |
|-------|-------|
| Purpose | Confirm the version may carry the BTE name at the claimed state. |
| Owner | Product Owner |

**Pass criteria**

- Definition of Done complete: Artifact → Editorial → Product Review → Approval
- Change class legal for the phase (Beta = quality only)
- Checklist complete
- Version name legal under `VERSIONING_POLICY.md`

**Blockers**

- Implied or chat-only approval
- Completion Report offered as Done
- Feature work inside Beta
- Unsigned move to RC or Production

---

## 5. Customer Pilot Gate

| Field | Value |
|-------|-------|
| Purpose | Confirm an appointed consulting reviewer or intended customer can use the reading. |
| Owner | Product Owner, with appointed reviewer |

**Pass criteria**

- Named case, real birth data, reviewed as a reading
- Confusion and unused advice logged, not ignored
- Required PASS before Production; required as consulting review before RC issue as Production-candidate

**Blockers**

- Internal enthusiasm treated as pilot
- Laboratory test scores treated as customer acceptance
- Silence treated as PASS

---

## 6. Gate independence

QA may confirm that evidence files exist.
QA may not pass Editorial, Commercial, or Product gates by that confirmation.
