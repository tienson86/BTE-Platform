# Changelog Policy

| Field | Value |
|-------|-------|
| Document | CHANGELOG_POLICY |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Release Manager |

Every signed version has a changelog entry.
The changelog describes **what the consultation or product record changed**, not how code was arranged.

---

## 1. Entry header

```
Version:
State:          (Beta0 / Beta1 / Beta2 / RC1 / Production / …)
Date:
Product Owner:
Release Manager:
```

Then the body, using only the categories below.
Empty categories are omitted, not filled with “none” lists of implementation chores.

---

## 2. Categories

| Category | Use for | Do not use for |
|----------|---------|----------------|
| **Engine** | Correction of analytical truth inside a frozen owner | New engines |
| **Knowledge** | Record or coverage change in admissible content | A new knowledge system |
| **Narrative** | Change in composed consultation language | A second composer |
| **Editorial** | Admission quality: leaks, dumps, duplicates, fragments, life-stage | Replacing ES-V1 |
| **Report** | Edition or PDF consultation presentation | Recalculating the chart |
| **UI** | Customer-facing consultation surface | Unrelated internal tools |
| **Infrastructure** | Reliability of producing the signed artifact | New runtime product layers |
| **Documentation** | Governance or operations documents | Treating docs as the customer artifact |
| **Governance** | Policy, freeze, ownership, Done, signoff rules | Feature work |
| **Operations** | Release process, cadence, filing, rollback practice | Product meaning |

If an item fits two categories, choose the one the customer would notice first.
If the customer would not notice it, it belongs in Infrastructure, Documentation, Governance, or Operations — not Narrative.

---

## 3. Body format

For each used category:

```
### <Category>

- Change:
- Why:
- Cases / artifacts affected:
- Residual risk:
```

Do not list file paths as the change.
Do not claim “quality improved” without pointing at After PDFs.

---

## 4. Forbidden changelog behaviour

- Using the changelog as a substitute for Artifact First
- Recording Architecture change as Engine or Infrastructure without Product Owner pre-approval
- Editing prior version entries to hide regression
- Advertising Beta quality work as features

---

## 5. Filing

- Issue changelog: `knowledge/release/<stage>/<version>/CHANGELOG.md`
- Product-level capability log remains `knowledge/product/06_PRODUCT_CHANGELOG.md` and must not contradict this entry
- Historical commercial notes in `knowledge/releases/` are not updated to rewrite history
