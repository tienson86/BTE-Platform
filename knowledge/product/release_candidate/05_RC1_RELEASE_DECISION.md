# 05 — RC1 Release Decision · Commercial V1

Version: 1.0.0  
Status: **AWAITING PRODUCT OWNER** — do not pre-fill GO  
Date: 2026-08-08  
Release candidate: **Commercial V1 · RC1**  

---

## 1. Purpose

Record the **official Product release decision** for Commercial V1 after Human Consulting Validation.

This decision is **independent** of:

- Capability Registry rows already marked Released for SEL / PRO (production path wiring)  
- Engineering Golden Cases / module tests PASS  

Commercial V1 **product** release requires this form signed.

**Do not declare Commercial V1 Released until a GO or GO WITH MINOR FIXES is recorded here.**

---

## 2. Official release outcomes

### GO

Commercial V1 may be announced as Released for Beta / commercial offering.

Conditions:

- Human consulting acceptance is **PASS** (aggregate)  
- Zero open Blockers  
- Prerequisites verified (below)

### GO WITH MINOR FIXES

Commercial V1 may proceed with an explicit minor-fix list.

Conditions:

- Acceptance is **PASS WITH MINOR FIXES**  
- Zero Blockers  
- Fixes owned, dated, and P1-or-lower  
- Product accepts residual risk in writing

### NO GO

Commercial V1 must **not** be announced as Released.

Conditions:

- Any **REJECT** acceptance, or open Blocker, or failed prerequisites  
- Return to polish / consulting repair — **no new Capability** as a shortcut

---

## 3. Prerequisite verification (engineering package)

Verify before signing. Mark each:

| Check | Status | Evidence |
|-------|:------:|----------|
| RC1 review package files exist (`01`–`05`) | ☐ | `knowledge/product/release_candidate/` |
| Capability Registry lists Career Selection Released | ☐ | `knowledge/product/01_CAPABILITY_REGISTRY.md` |
| Capability Registry lists Promotion Readiness Released | ☐ | same |
| Product Changelog records capability releases | ☐ | `knowledge/product/06_PRODUCT_CHANGELOG.md` |
| Career Selection release notes complete | ☐ | Domain `23_RELEASE_NOTES.md` |
| Promotion release notes complete | ☐ | Domain `30_PROMOTION_RELEASE_NOTES.md` |
| Golden Cases complete (SEL) | ☐ | Domain `22` / `tests/domain01` |
| Golden Cases complete (PRO) | ☐ | Domain `25` / `29` / `tests/domain01` |
| Regression complete (commercial + domain01) | ☐ | `09_COMMERCIAL_QA.md` · validation reports |
| P0 engineering polish complete | ☐ | `commercial_v1/07`–`09` |
| Human consulting forms completed | ☐ | Completed `02`–`04` |

---

## 4. Human consulting roll-up

| Metric | Value |
|--------|-------|
| Reviewers count | |
| Cases PASS | |
| Cases PASS WITH MINOR FIXES | |
| Cases REJECT | |
| Open Blockers | |
| Open Majors | |

---

## 5. Decision record (Product Owner only)

Select **one**:

- [ ] **GO**  
- [ ] **GO WITH MINOR FIXES**  
- [ ] **NO GO**  

| Field | Value |
|-------|-------|
| Decision date | _pending_ |
| Product Owner | |
| Rationale | |
| Minor fix list (if any) | |
| Next review date (if NO GO / minors) | |

**Commercial V1 Released?** ☐ Yes · ☐ **No (default until signed GO / GO WITH MINOR FIXES)**

---

## 6. Post-decision actions

| If | Then |
|----|------|
| GO | Update Product Changelog with Commercial V1 Released; announce Beta; freeze RC1 scope |
| GO WITH MINOR FIXES | Track minors; Changelog notes conditional release; no new Capability |
| NO GO | Keep RC1; open polish sprint from acceptance comments only |

---

## 7. Stop line

Decision form ready.  

**Wait for Product review. Do not declare Commercial V1 Released in this package.**

---

END
