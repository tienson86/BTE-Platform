# 06 — Product Changelog

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Owner: BTE Product  
Depends on: `01_CAPABILITY_REGISTRY.md`  

---

## 1. Purpose

Official changelog for **capability releases**.

Every production capability release records:

| Field | Required |
|-------|----------|
| Version | Capability semver |
| Capability | Registry ID + name |
| Changes | Customer-visible summary |
| Golden Cases | Result summary |
| Regression | Wave 1.1 / prior caps |
| Production date | YYYY-MM-DD |

---

## 2. Entries

### 2026-08-08 — Commercial V1 · RC1 human consulting package

| Field | Value |
|-------|-------|
| **Version** | RC1 (product gate — not a capability semver) |
| **Capability** | — (Commercial V1 product validation) |
| **Changes** | Published Release Candidate human consulting validation package under `knowledge/product/release_candidate/` (`01`–`05`). Engineering complete; Commercial V1 **not** declared Released pending Product Owner decision on `05_RC1_RELEASE_DECISION.md`. |
| **Golden Cases** | Prerequisites verified in Domain / `tests/domain01` (not re-run here) |
| **Regression** | Prerequisites documented in `commercial_v1/09` |
| **Production date** | N/A — awaiting human GO |

### 2026-08-08 — CAP-CAREER-PRO-001 · v1.0.0

| Field | Value |
|-------|-------|
| **Version** | `1.0.0` |
| **Capability** | `CAP-CAREER-PRO-001` — Promotion Readiness Assessment |
| **Domain alias** | `CAP-D1-CA-PRO` |
| **Status** | Released · Production |
| **Changes** | Second Commercial Capability on production Result path. Customers receive readiness posture, management-role acceptance, competency gaps, advancement posture/window, timing, risks + mitigation, and 90-day promotion plan via existing Result slots. Career Selection remains Frozen companion. |
| **Golden Cases** | D1-GC-PROMOTE-READY, PREPARE, MIXED — **3/3 PASS** |
| **Regression** | `tests/domain01` + `tests/commercial_knowledge` PASS (41) |
| **Production date** | **2026-08-08** |
| **Evidence** | Domain `24`–`30`; Acceptance Standard Pass |

**Non-goals this release:** Leadership Assessment (full); Partnership; Wave 1.1 edits; SEL content edits; new Result screens.

### 2026-08-08 — CAP-CAREER-SEL-001 · Freeze notice

| Field | Value |
|-------|-------|
| **Version** | `1.0.0` (unchanged) |
| **Capability** | `CAP-CAREER-SEL-001` — Career Selection Assessment |
| **Changes** | Stage moved to **Frozen** as Promotion Readiness ships. No content change. |
| **Golden Cases** | Prior 3/3 retained |
| **Regression** | PASS |
| **Production date** | 2026-08-08 (freeze notice) |

### 2026-08-08 — CAP-CAREER-SEL-001 · v1.0.0

| Field | Value |
|-------|-------|
| **Version** | `1.0.0` |
| **Capability** | `CAP-CAREER-SEL-001` — Career Selection Assessment |
| **Domain alias** | `CAP-D1-CA-SEL` |
| **Status** | Released · Production |
| **Changes** | First Commercial Capability on production Result path. Customers receive career direction, environment, role, leadership/employment posture, strengths, risks, mitigation, development, timing, and 90-day plan via existing Result slots. Wave 1.1 cores remain. No new Result screen/route/layout. |
| **Golden Cases** | D1-GC-STRONG-EMP, D1-GC-WEAK-EMP, D1-GC-MIXED-EMP — **3/3 PASS** |
| **Regression** | `tests/commercial_knowledge` PASS; Wave 1.1 Adapter default path preserved |
| **Production date** | **2026-08-08** |
| **Evidence** | Domain `20`–`23`; `tests/domain01` (17 PASS); Acceptance Standard Pass |

**Non-goals this release:** Promotion Readiness; Leadership Assessment (full); Partnership; new Knowledge Units; Wave 1.1 edits; Foundation/Narrative/Portal redesign.

---

### 2026-08-08 — Product governance pack (meta)

| Field | Value |
|-------|-------|
| **Version** | Registry pack `1.0.0` |
| **Capability** | — (governance, not a customer capability) |
| **Changes** | Established Capability Registry V1, Release Policy, Lifecycle, Acceptance Standard, Product Roadmap, and this Changelog under `knowledge/product/`. |
| **Golden Cases** | N/A |
| **Regression** | N/A (documentation only) |
| **Production date** | 2026-08-08 (docs published) |

---

## 3. Template (copy for next release)

```markdown
### YYYY-MM-DD — CAP-… · vX.Y.Z

| Field | Value |
|-------|-------|
| **Version** | |
| **Capability** | |
| **Changes** | |
| **Golden Cases** | |
| **Regression** | |
| **Production date** | |
| **Evidence** | |
```

---

## 4. Stop line

Changelog: Career Selection **Frozen** · Promotion Readiness **v1.0.0** released.  

Next entry only after Product-approved Leadership Assessment work.

---

END
