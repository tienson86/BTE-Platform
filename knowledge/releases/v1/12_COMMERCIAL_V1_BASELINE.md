# 12 — Commercial V1 Baseline

Version: 1.0.0  
Date: 2026-08-08  

| Field | Value |
|-------|-------|
| **Status** | **Release Candidate 1** |
| **Engineering** | **PASS** |
| **Golden Cases** | **PASS** |
| **Commercial QA** | **PASS** |
| **Human Consulting Review** | **PENDING** |
| **Product Decision** | **PENDING** |
| **Commercial Version** | **RC1** |

---

## 1. Purpose

Freeze the **Commercial V1 baseline inventory** for Product review: architecture, foundation, knowledge, capabilities, narrative, portal, registry, and versions as of RC1.

**Commercial V1 is NOT Released.**  
Until Product GO, treat this as the **RC1 candidate baseline**.

---

## 2. Architecture

| Item | Baseline |
|------|----------|
| V1 Architecture Freeze | `knowledge/releases/v1/01_V1_ARCHITECTURE_FREEZE.md` |
| Pipeline | Input → Calendar → Bazi → Score → Pattern → Interpretation → Report (+ Narrative compose) |
| Commercial Knowledge | `engines/commercial_knowledge/` · Retrieval Contract v1 |
| Freeze rule | No unauthorized engine boundary changes |

---

## 3. Foundation

| Item | Baseline |
|------|----------|
| Product Manifesto | `knowledge/product/BTE_PRODUCT_MANIFESTO.md` |
| Experience / Brand / Visual / Design System | Foundation V1.0 frozen packs |
| Result architecture | Zones → Rows → Grid → Cards (PACK_06 / PACK_07) |
| Rule | No token invention; no layout redesign without approval |

---

## 4. Knowledge

| Item | Baseline |
|------|----------|
| Wave 1.1 cores | `database/20_knowledge/21_knowledge_units.csv` (ID/ST/WK/UG/RC) — frozen content |
| Domain 01 CSV | `database/20_knowledge/22_domain01_career_business.csv` |
| SEL wave | `W-D01-C-SEL` · 11 units · CAP-D1-CA-SEL |
| PRO wave | `W-D01-E-PRO` · 10 units · CAP-D1-CA-PRO |
| DB changelog | `database/20_knowledge/CHANGELOG.md` |

---

## 5. Capabilities

| Registry ID | Name | Version | Stage |
|-------------|------|---------|-------|
| CAP-CAREER-SEL-001 | Career Selection Assessment | 1.0.0 | **Frozen** |
| CAP-CAREER-PRO-001 | Promotion Readiness Assessment | 1.0.0 | **Production** |

Allow-list production union: Wave 1.1 ∪ SEL ∪ PRO.  
LED/BU Domain rows exist in CSV but are **not** production-allow-listed in Commercial V1 RC1.

---

## 6. Narrative

| Item | Baseline |
|------|----------|
| Engine | Pack 05 Narrative Engine (frozen architecture) |
| Enrichment | Commercial Knowledge enrich-only merge |
| Exec | `commercial_executive_summary` (1+≤3+1) |
| Primary Rec | Career Strategy · What/Why/How/When/Expected outcome |
| Secondary | Promotion Readiness milestone |
| Presentation | `commercial_presentation.py` commercialize layer |

---

## 7. Portal

| Item | Baseline |
|------|----------|
| Result host | `PortalPage` / Result zones |
| Adapters | `narrativeResultAdapter` · `canonicalDesktopAdapter` |
| Rule | No new Result route/card/layout in V1 baseline |
| Framing | Capability names in existing slots |

---

## 8. Registry & product governance

| Item | Baseline |
|------|----------|
| Capability Registry | `knowledge/product/01_CAPABILITY_REGISTRY.md` |
| Release Management | `knowledge/releases/process/` |
| Product Changelog | `knowledge/product/06_PRODUCT_CHANGELOG.md` |
| RC1 human review | `knowledge/product/release_candidate/` |
| RC1 package | `09`–`13` this folder |

---

## 9. Versions (at RC1 cut)

| Track | Version |
|-------|---------|
| Commercial | **V1 RC1** (NOT Released) |
| CAP-CAREER-SEL-001 | 1.0.0 |
| CAP-CAREER-PRO-001 | 1.0.0 |
| Commercial Knowledge contract | `bte.commercial_knowledge.retrieval.v1` / 1.0.0 |
| Architecture Freeze docs | V1.0 |

---

## 10. Baseline freeze statement

**Commercial V1 RC1 baseline inventory is frozen for Product review.**  

Do not silently expand scope.  
**Do not declare Commercial V1 Released** until Product sign-off (`13` / `05_RC1_RELEASE_DECISION.md`).

---

END
