# 05 — Post-Release Policy

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Owner: BTE Product  

---

## 1. Purpose

Govern work **after** a Commercial version is Released (GO / GO WITH MINOR FIXES).

Does not apply to RC phases still awaiting Product Approval.

---

## 2. Allowed post-release work classes

### 2.1 Bug Fix

| Rule | Detail |
|------|--------|
| Intent | Correct defects without changing commercial meaning |
| Versioning | Usually **Patch** (`07_VERSIONING_POLICY.md`) |
| Gates | Engineering + regression; consulting re-review if customer-facing meaning shifts |
| Hotfix | Use `06_HOTFIX_POLICY.md` when severity warrants |

### 2.2 Quality Improvement

| Rule | Detail |
|------|--------|
| Intent | Clarity, density, tone, framing polish inside frozen architecture |
| Versioning | Patch or Minor (Product decides) |
| Forbidden | Silent Capability expansion; Foundation redesign without approval |
| Review | Commercial Quality + selective Human Review if Exec/Rec change |

### 2.3 Knowledge Revision

| Rule | Detail |
|------|--------|
| Intent | Revise approved Knowledge Units / commercial wording |
| Versioning | Knowledge version bump; may trigger Capability minor/patch |
| Rules | Database / Golden Dataset rules respected; no expected-output cheating |
| Review | Golden Case Gate + consulting sample review |

### 2.4 Capability Expansion

| Rule | Detail |
|------|--------|
| Intent | New Capability or major expansion of an existing one |
| Versioning | Usually Commercial **Minor** or **Major**; new Capability version `1.0.0` |
| Process | Full Capability Release Policy + Commercial gates for the train that ships it |
| Forbidden | Shipping expansion as “bugfix” |

---

## 3. Decision table

| Change type | Typical track | Needs Human Consulting Gate? |
|-------------|---------------|:----------------------------:|
| Bug Fix (low customer meaning) | Patch / Hotfix | No (unless Rec/Exec meaning changes) |
| Quality Improvement (Exec/Rec) | Patch/Minor | Yes (sample set) |
| Knowledge Revision | Patch/Minor | Yes (affected cases) |
| Capability Expansion | Minor/Major | Yes (full set for that Capability) |

---

## 4. Maintenance freeze windows

Product may declare a **maintenance freeze** (e.g. first N days after Commercial release) allowing only Critical/High hotfixes.

---

## 5. Stop line

Post-release work must not bypass Capability Registry or Release Gates by renaming expansion as maintenance.

---

END
