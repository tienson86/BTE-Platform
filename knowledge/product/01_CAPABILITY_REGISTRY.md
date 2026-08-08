# 01 — Capability Registry

Version: 1.0.0  
Status: **OFFICIAL — Single Source of Truth**  
Date: 2026-08-08  
Owner: BTE Product  
Scope: Customer-facing commercial capabilities only  

---

## 1. Purpose

The Capability Registry is the **single source of truth** for every commercial capability in BTE.

If a capability is not listed here, it is **not** an official product capability — regardless of Domain docs, Knowledge Units, or engineering work-in-progress.

---

## 2. Registry field schema

Every capability entry must include:

| Field | Description |
|-------|-------------|
| Capability ID | Stable product registry id (`CAP-…`) |
| Capability Name | Customer-facing commercial name |
| Domain | Domain pack (e.g. Domain 01 Career & Business) |
| Domain Alias | Domain-local id (e.g. `CAP-D1-CA-SEL`) when applicable |
| Version | Semver of the capability release |
| Status | Registry status (see Release Policy) |
| Current Stage | Lifecycle / release stage |
| Production | Yes / No / Partial |
| Golden Cases | Pass count vs required set |
| Knowledge Coverage | Coverage of required KU slots for the capability |
| Acceptance Status | Pass / Fail / Pending against Acceptance Standard |
| Dependencies | Wave, Domain, other capabilities |
| Owner | Product owner |
| Priority | P0 / P1 / P2 |
| Commercial Value | High / Medium / Strategic |
| Future Release | Target release slot on Product Roadmap |

---

## 3. Official registry (V1)

### 3.1 CAP-CAREER-SEL-001 — Career Selection Assessment

| Field | Value |
|-------|-------|
| **Capability ID** | `CAP-CAREER-SEL-001` |
| **Capability Name** | Career Selection Assessment |
| **Domain** | Domain 01 — Career & Business |
| **Domain Alias** | `CAP-D1-CA-SEL` |
| **Version** | `1.0.0` |
| **Status** | **Released** |
| **Current Stage** | **Frozen** |
| **Production** | **Yes** |
| **Golden Cases** | **3/3** (P0: STRONG-EMP, WEAK-EMP, MIXED-EMP) |
| **Knowledge Coverage** | **100%** of SEL required slots (11/11 units) |
| **Acceptance Status** | **Pass** |
| **Dependencies** | Wave 1.1 Core |
| **Owner** | BTE Product |
| **Priority** | P0 |
| **Commercial Value** | High — primary career entry / conversion capability |
| **Future Release** | Released in Release 1 — **Frozen**; maintenance/revision only |

**Customer outcome:** Work-direction families, environment, role, leadership/employment posture, strengths, risks, mitigation, development, timing, 90-day plan — on the existing Result Page.

**Out of scope:** Job-title prophecy; salary guarantees; Promotion / Leadership / Partnership packs.

---

### 3.2 CAP-CAREER-PRO-001 — Promotion Readiness Assessment

| Field | Value |
|-------|-------|
| **Capability ID** | `CAP-CAREER-PRO-001` |
| **Capability Name** | Promotion Readiness Assessment |
| **Domain** | Domain 01 — Career & Business |
| **Domain Alias** | `CAP-D1-CA-PRO` |
| **Version** | `1.0.0` |
| **Status** | **Released** |
| **Current Stage** | **Production** |
| **Production** | **Yes** |
| **Golden Cases** | **3/3** (PROMOTE-READY, PROMOTE-PREPARE, PROMOTE-MIXED) |
| **Knowledge Coverage** | **100%** (10/10 PRO units) |
| **Acceptance Status** | **Pass** |
| **Dependencies** | Wave 1.1 · CAP-CAREER-SEL-001 (Frozen companion on Result path) |
| **Owner** | BTE Product |
| **Priority** | P1 → shipped as Production V1 |
| **Commercial Value** | High — upsell after career selection |
| **Future Release** | Released in Release 2 — maintenance until revision |

**Customer outcome:** Ready / prepare / defer posture; management-role acceptance; competency gaps; risks + mitigation; timing + advancement window; 90-day promotion plan — on the existing Result Page.

**Out of scope:** Guaranteed titles/salary; full Leadership Assessment; Partnership packs.

**Gate:** Product Review before Leadership Assessment (Release 3).

---

### 3.3 CAP-CAREER-LED-001 — Leadership Assessment

| Field | Value |
|-------|-------|
| **Capability ID** | `CAP-CAREER-LED-001` |
| **Capability Name** | Leadership Assessment |
| **Domain** | Domain 01 — Career & Business |
| **Domain Alias** | `CAP-D1-CA-LED` |
| **Version** | — |
| **Status** | Proposed |
| **Current Stage** | Proposed |
| **Production** | No |
| **Golden Cases** | 0 / planned |
| **Knowledge Coverage** | P0 light unit exists in Domain CSV — **not** production-allow-listed |
| **Acceptance Status** | Pending |
| **Dependencies** | Wave 1.1 · CAP-CAREER-SEL-001 |
| **Owner** | BTE Product |
| **Priority** | P0 light → P1 deep |
| **Commercial Value** | High |
| **Future Release** | **Release 3** |

---

### 3.4 CAP-BUSINESS-SUIT-001 — Business Suitability Assessment

| Field | Value |
|-------|-------|
| **Capability ID** | `CAP-BUSINESS-SUIT-001` |
| **Capability Name** | Business Suitability Assessment |
| **Domain** | Domain 01 — Career & Business (BU) |
| **Domain Alias** | `CAP-D1-BU-ENP` (seed) / Business Suitability product name |
| **Version** | — |
| **Status** | Proposed |
| **Current Stage** | Proposed |
| **Production** | No |
| **Golden Cases** | 0 / planned |
| **Knowledge Coverage** | Not started (product scope TBD at Planned) |
| **Acceptance Status** | Pending |
| **Dependencies** | Wave 1.1 · CAP-CAREER-SEL-001 |
| **Owner** | BTE Product |
| **Priority** | P1 |
| **Commercial Value** | High — founder / independent path |
| **Future Release** | **Release 4** |

---

### 3.5 CAP-FINANCE-PLAN-001 — Finance Planning Assessment

| Field | Value |
|-------|-------|
| **Capability ID** | `CAP-FINANCE-PLAN-001` |
| **Capability Name** | Finance Planning Assessment |
| **Domain** | Future Domain (Finance / CK-FI supporting) |
| **Domain Alias** | TBD at Planned |
| **Version** | — |
| **Status** | Proposed |
| **Current Stage** | Proposed |
| **Production** | No |
| **Golden Cases** | 0 / planned |
| **Knowledge Coverage** | Not started |
| **Acceptance Status** | Pending |
| **Dependencies** | Wave 1.1 · Domain Finance architecture |
| **Owner** | BTE Product |
| **Priority** | P2 |
| **Commercial Value** | Strategic |
| **Future Release** | **Release 5** |

---

### 3.6 CAP-MARRIAGE-COMPAT-001 — Marriage Compatibility Assessment

| Field | Value |
|-------|-------|
| **Capability ID** | `CAP-MARRIAGE-COMPAT-001` |
| **Capability Name** | Marriage Compatibility Assessment |
| **Domain** | Future Domain (Relationship) |
| **Domain Alias** | TBD at Planned |
| **Version** | — |
| **Status** | Proposed |
| **Current Stage** | Proposed |
| **Production** | No |
| **Golden Cases** | 0 / planned |
| **Knowledge Coverage** | Not started |
| **Acceptance Status** | Pending |
| **Dependencies** | Wave 1.1 · Relationship domain architecture |
| **Owner** | BTE Product |
| **Priority** | P2 |
| **Commercial Value** | High (consumer) |
| **Future Release** | **Release 6** |

---

### 3.7 CAP-HEALTH-BAL-001 — Health Balance Assessment

| Field | Value |
|-------|-------|
| **Capability ID** | `CAP-HEALTH-BAL-001` |
| **Capability Name** | Health Balance Assessment |
| **Domain** | Future Domain (Health) |
| **Domain Alias** | TBD at Planned |
| **Version** | — |
| **Status** | Proposed |
| **Current Stage** | Proposed |
| **Production** | No |
| **Golden Cases** | 0 / planned |
| **Knowledge Coverage** | Not started |
| **Acceptance Status** | Pending |
| **Dependencies** | Wave 1.1 · Health domain architecture · ethics review |
| **Owner** | BTE Product |
| **Priority** | P2 |
| **Commercial Value** | Strategic (ethics-gated) |
| **Future Release** | **Release 7** |

---

### 3.8 CAP-LUCK-TIMING-001 — Luck Timing Decision Support

| Field | Value |
|-------|-------|
| **Capability ID** | `CAP-LUCK-TIMING-001` |
| **Capability Name** | Luck Timing Decision Support |
| **Domain** | Cross-domain (CK-LU + decision timing) |
| **Domain Alias** | `CAP-D1-TM-DEC` (Domain 01 seed) / product expansion TBD |
| **Version** | — |
| **Status** | Proposed |
| **Current Stage** | Proposed |
| **Production** | No |
| **Golden Cases** | 0 / planned |
| **Knowledge Coverage** | Not started as standalone capability |
| **Acceptance Status** | Pending |
| **Dependencies** | Wave 1.1 · Luck / timing evidence model · prior career/business caps recommended |
| **Owner** | BTE Product |
| **Priority** | P1/P2 |
| **Commercial Value** | High — decision timing upsell |
| **Future Release** | **Release 8** |

---

## 4. Registry summary table

| Capability ID | Name | Domain | Version | Status | Stage | Production | Priority | Release |
|---------------|------|--------|---------|--------|-------|------------|----------|---------|
| CAP-CAREER-SEL-001 | Career Selection Assessment | Domain 01 | 1.0.0 | Released | Frozen | Yes | P0 | R1 |
| CAP-CAREER-PRO-001 | Promotion Readiness Assessment | Domain 01 | 1.0.0 | Released | Production | Yes | P1 | R2 |
| CAP-CAREER-LED-001 | Leadership Assessment | Domain 01 | — | Proposed | Proposed | No | P1 | R3 |
| CAP-BUSINESS-SUIT-001 | Business Suitability Assessment | Domain 01 | — | Proposed | Proposed | No | P1 | R4 |
| CAP-FINANCE-PLAN-001 | Finance Planning Assessment | Finance (TBD) | — | Proposed | Proposed | No | P2 | R5 |
| CAP-MARRIAGE-COMPAT-001 | Marriage Compatibility Assessment | Relationship (TBD) | — | Proposed | Proposed | No | P2 | R6 |
| CAP-HEALTH-BAL-001 | Health Balance Assessment | Health (TBD) | — | Proposed | Proposed | No | P2 | R7 |
| CAP-LUCK-TIMING-001 | Luck Timing Decision Support | Cross / Luck | — | Proposed | Proposed | No | P1/P2 | R8 |

---

## 5. What the Registry does **not** list

- Engines (Calendar, Bazi, Score, Pattern, Interpretation, Narrative, Report)  
- Individual Knowledge Units  
- Design System packs  
- Internal adapters / allow-lists / CSV filenames  

Those are implementation details supporting capabilities.

---

## 6. Change control

1. New capabilities enter as **Proposed** via Product approval.  
2. Status/stage changes follow `02_CAPABILITY_RELEASE_POLICY.md`.  
3. Every production release updates `06_PRODUCT_CHANGELOG.md`.  
4. Domain alias IDs remain stable for Domain packs; Registry ID is the product SoT.

---

## 7. Stop line

Registry updated: **two** production capabilities (SEL Frozen · PRO Production V1).  

**Do not start Leadership Assessment without Product approval.**

---

END
