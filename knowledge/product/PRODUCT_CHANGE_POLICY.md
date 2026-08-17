# Product Change Policy

| Field | Value |
|-------|-------|
| Document | PRODUCT_CHANGE_POLICY |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Product Owner |

Every modification is classified **before work starts**.
Unclassified work is treated as Architecture change until the Product Owner says otherwise.

---

## 1. Change categories

| Category | Meaning | Typical examples | During V1 Beta |
|----------|---------|------------------|----------------|
| **Bug** | Defect against already-decided behaviour or truth | Wrong copy of an upstream fact; broken fragment in PDF | Allowed |
| **Editorial** | Customer language quality under ES-V1 | Remove engine wording; stop duplicate recommendations | Allowed |
| **Knowledge** | Admissible content records, not a new knowledge system | Correct or complete a knowledge record | Allowed |
| **Narrative** | How existing truth is composed into sentences | Composer quality inside the adopted composer | Allowed as Product/Editorial if no new composer |
| **Engine** | Correctness inside a frozen owner | Strength or luck calculation fix | Allowed inside owner; **no new engine** |
| **Architecture** | New subsystem, new owner, new pipeline, new edition, new canon | New engine, framework, matrix, publisher, composer, layer, runtime | **Forbidden** unless Product Owner approves first |
| **Release** | Whether a build may be issued | State change Beta → RC → Production; hotfix | Requires release approval in `PRODUCT_RELEASE_POLICY.md` |

Narrative change that adds a second composer, a new publication system, or a new edition is Architecture, not Narrative.

Knowledge change that adds a new canon, matrix, or knowledge system is Architecture, not Knowledge.

---

## 2. Classification test

Ask, in order:

1. Does the customer-facing artifact change? If no, it is still classified; it is not automatically Done.
2. Does a frozen owner still own the fact? If no → Architecture.
3. Is a new named system being introduced? If yes → Architecture.
4. Is the work only wording admission? → Editorial.
5. Is the work only content records? → Knowledge.
6. Is the work only correcting a frozen calculator? → Engine.
7. Is the work only repairing broken decided behaviour? → Bug.
8. Is the work issuing a build? → Release.

---

## 3. Approval workflow

```
Propose change
    ↓
Classify category
    ↓
Owner of the surface reviews
    ↓
If Architecture: Product Owner approval required before work starts
    ↓
Produce artifact (if customer-facing)
    ↓
Editorial Review (if customer-facing)
    ↓
Product Review
    ↓
Product Owner approval
    ↓
Done / Release as applicable
```

| Category | Surface owner | Product Owner |
|----------|---------------|---------------|
| Bug | Owning engine or report surface | Required if customer-facing |
| Editorial | Chief Editor | Required to ship |
| Knowledge | Knowledge Board | Required if customer-facing meaning changes |
| Narrative | Interpretation / narrative owner | Required to ship |
| Engine | Engine owner | Required if customer-facing truth changes |
| Architecture | Architecture Board | **Required before start** |
| Release | Release Manager | **Required to issue** |

---

## 4. Forbidden informal paths

The following do not authorise change:

- A completion report
- A passing test suite
- A verbal agreement
- Editing Golden Dataset, snapshots, or expected output to match a new result

---

## 5. Relation to Beta 0

`beta/BETA0_RELEASE_WORKFLOW.md` is the V1 Beta overlay.
This policy is the standing product rule.
Where Beta 0 is stricter, Beta 0 wins until Production.
