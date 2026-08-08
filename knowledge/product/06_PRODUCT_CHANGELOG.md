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

Changelog opened with Career Selection Assessment **v1.0.0**.  

Next entry expected only after Product-approved capability work (not before Promotion Readiness approval).

---

END
