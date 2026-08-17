# Release Strategy

| Field | Value |
|-------|-------|
| Document | RELEASE_STRATEGY |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Product Owner + Release Manager |
| Current V1 phase | **Freeze (Beta0)** |

---

## 1. Philosophy

BTE is released as a **consultation**, not as a collection of merged changes.

A version may leave the company only when:

- the platform path is the frozen path
- real-case artifacts exist
- editorial and commercial review have passed for that state
- the Product Owner has signed

Speed of delivery is not a strategy.
Stability of meaning is the strategy.

---

## 2. Phases

### Research

The company decides what the product is.
No version is sold.
No consultation is claimed.

### Development

The consultation path is built.
Scope may include product features **only while this phase is open**.
Exit is Feature Complete for the intended train, not “tests green.”

### Freeze

The platform stops expanding.
V1 Freeze is **Beta0**: architecture, truth, narrative, publishing, editorial ownership, and Golden Dataset are locked.

Freeze is a product decision.
It is not a git tag by itself.

### Beta

The consultation is improved on the frozen platform.

**No feature development during Beta.**
**Only quality improvement.**

Allowed: defect repair, editorial quality, knowledge record quality, engine correctness inside frozen owners, consultation readability.

Forbidden: new engines, frameworks, matrices, publishers, composers, canons, layers, runtime components, new commercial capabilities, new editions — unless Product Owner approved an Architecture change before work started.

Beta0 is the freeze declaration.
Beta1 and Beta2 are quality trains under that freeze.

### RC

The consultation is the intended commercial article.
Scope is frozen.
Remaining work is defect and admission, not expansion.

### Production

The consultation is sold under the BTE name.
Change is controlled.
Regression is artifact-first.

### Maintenance

After Production: patches, hotfixes, editorial corrections, knowledge corrections inside frozen owners.

Maintenance is not a covert Beta for new features.
New commercial scope is a new version decision (for example 1.1 or 2.0), not a maintenance issue.

---

## 3. What a release is for

| Phase | Customer promise |
|-------|------------------|
| Research / Development / Freeze | None |
| Beta | Appointed review of a quality train. Not general sale. |
| RC | Appointed commercial and consulting review of the intended article. |
| Production | Paying customers receive the signed consultation. |
| Maintenance | Existing Production customers receive a repair of that consultation. |

---

## 4. Strategy rules

1. One commercial train at a time for V1 until Production.
2. Quality trains (Beta1, Beta2) do not reopen feature scope.
3. RC does not restart Development.
4. Production does not begin because a calendar slot arrived.
5. A later phase may not skip Artifact First.

This strategy implements `knowledge/product/PRODUCT_RELEASE_POLICY.md` and `knowledge/product/PRODUCT_ROADMAP.md`.
It does not replace them.
