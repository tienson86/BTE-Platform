# Hotfix Policy

| Field | Value |
|-------|-------|
| Document | HOTFIX_POLICY |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Product Owner + Release Manager |

Hotfix and Emergency Patch exist to repair Production.
They are not a path for features, and not a path around Freeze.

---

## 1. Classes

| Class | Meaning |
|-------|---------|
| **Critical bug** | Harm, ethics breach, wrong person, systematically wrong advice, or total failure of the consultation artifact. |
| **Emergency patch** | Production repair of a Critical or otherwise severe defect on the frozen path. Wider than a hotfix if several related defects must be closed together. Still not a feature train. |
| **Hotfix** | Narrow Production repair of a Critical or High defect. Smallest change that restores the signed consultation. |

Medium defects prefer the next planned patch train.
Low defects are not hotfix-eligible.

This classification matches the intent of `knowledge/releases/process/06_HOTFIX_POLICY.md` and `knowledge/product/PRODUCT_RELEASE_POLICY.md`.
This document is the operational rule from 2026-08-17.

---

## 2. Hotfix workflow

```
Detect Critical / High defect
    ↓
Classify (Hotfix vs Emergency Patch vs wait for planned patch)
    ↓
Product Owner authorises start
    ↓
Minimal repair inside frozen owners
    ↓
Regenerate artifacts (if customer-facing)
    ↓
Engineering Gate
    ↓
Editorial Gate (if prose or PDF changes)
    ↓
Commercial Gate (if customer meaning changes)
    ↓
Product Owner signoff
    ↓
Patch version (for example 1.0.1)
    ↓
Post-hotfix validation
```

No new Engine, Framework, Matrix, Publisher, Composer, Canon, Layer, or Runtime component.
No Golden Dataset rewrite to hide the defect.

---

## 3. Hotfix review

| Review | Required |
|--------|----------|
| Engineering | Always |
| Editorial | If any customer sentence or PDF changes |
| Commercial | If customer meaning changes |
| QA | Artifact pack completeness |
| Product Owner | Always, before issue |
| Customer Pilot | Not a new public pilot; appointed spot-check if advice changed |

---

## 4. Post-hotfix validation

Within the issue record, after issue:

1. After PDFs (or a recorded proof that no consultation artifact changed)
2. Golden anchors re-read for the defect class
3. Confirmation that the original defect is closed
4. Confirmation that no new High/Critical defect was introduced
5. Changelog category Engine, Editorial, Narrative, Report, or Knowledge as applicable
6. Rollback readiness: previous signed version retained as Before

If post-hotfix validation fails, `ROLLBACK_POLICY.md` applies immediately.

---

## 5. Naming

Hotfix and Emergency Patch consume the next **PATCH** on the live Production version.

They do not create Beta trains.
They do not create 2.0.
They do not retag 1.0.
