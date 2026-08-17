# Versioning Policy

| Field | Value |
|-------|-------|
| Document | VERSIONING_POLICY |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Release Manager + Product Owner |

A version name is a product claim.
A branch name is not a version.
A document title is not a version.
The Product Owner signed name is the version.

---

## 1. Version families

| Name | When it is used | Sold? |
|------|-----------------|-------|
| **0.x** | Research and Development before a named Beta train | No |
| **Beta0** | Freeze declaration and freeze records | No |
| **Beta1** | First quality train after freeze | No |
| **Beta2** | Second quality train after freeze | No |
| **RC1** | First Release Candidate for 1.0 | No |
| **RC2** | Subsequent candidate if RC1 is not accepted | No |
| **1.0** | First Production of this product generation | Yes |
| **1.0.1** | Patch or hotfix on 1.0 | Yes, as repair of 1.0 |
| **1.1** | Minor Production train: quality or authorised small product improvement, same generation | Yes, after signoff |
| **2.0** | New product generation | Only after a new Product Owner decision |

Further Beta trains, if required, continue as Beta3, Beta4, …
Further candidates continue as RC3, RC4, …
Further patches continue as 1.0.2, 1.0.3, …

---

## 2. Naming rules

1. Write the commercial version as the family above. Do not invent parallel schemes for the same issue.
2. **0.x** is `0.MINOR` or `0.MINOR.PATCH`. It never means Production.
3. **BetaN** is a quality train identifier, not a SemVer prerelease of a sold 1.0.
4. **RCN** is a candidate for **1.0** (or for the next Production major/minor under signoff). It is not Production.
5. **1.0** is issued once. Later repairs are **1.0.x**, not a second 1.0.
6. **1.1** requires a Product Owner decision that the train is a minor Production version, not a Beta quality issue labelled as 1.1.
7. **2.0** requires an Architecture and Product decision. It is not a Beta escape hatch.
8. Emergency Patch and Hotfix use the next **PATCH** on the live Production version (for example 1.0.1). They do not create a new major.
9. Capability versions and knowledge-unit versions remain as defined in `knowledge/releases/process/07_VERSIONING_POLICY.md`. They do not rename the commercial version.

---

## 3. What each bump means

| From → To | Meaning |
|-----------|---------|
| 0.x → Beta0 | Freeze. Platform locked. |
| Beta0 → Beta1 | First quality issue under freeze. |
| Beta1 → Beta2 | Further quality issue. Still no features. |
| BetaN → RC1 | Product Owner opens the candidate for 1.0. |
| RC1 → RC2 | Candidate rejected or incomplete; new candidate. |
| RCN → 1.0 | Production accepted. |
| 1.0 → 1.0.1 | Repair. No new product generation. |
| 1.0 → 1.1 | Authorised minor Production train. |
| 1.x → 2.0 | New generation. Explicit Product Owner decision. |

---

## 4. Tagging

When a version is signed:

- the version name on `RELEASE_SIGNOFF.md` is the official name
- a repository tag, if used, must match that name exactly
- artifacts are stored under the matching stage folder (`beta1/`, `rc/`, `production/`, …)

An unsigned tag is not a release.

---

## 5. Current V1 name

Until Product Owner signs otherwise, the platform state is **Beta0**.
No 1.0 exists.
No Production version exists.
