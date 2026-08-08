# 05 — Product Roadmap

Version: 1.0.0  
Status: **OFFICIAL — Capability Roadmap**  
Date: 2026-08-08  
Owner: BTE Product  
Depends on: `01_CAPABILITY_REGISTRY.md`  
Scope: Roadmap by **capability** (not by Engine)  

---

## 1. Purpose

Order BTE product evolution as a sequence of commercial capability releases.

Architecture remains frozen; product grows by shipping capabilities that pass the Acceptance Standard.

---

## 2. Release sequence

| Release | Capability ID | Capability Name | Status |
|--------:|---------------|-----------------|--------|
| **1** | CAP-CAREER-SEL-001 | Career Selection Assessment | **Released (Production V1)** |
| **2** | CAP-CAREER-PRO-001 | Promotion Readiness Assessment | Proposed — awaiting Product approval |
| **3** | CAP-CAREER-LED-001 | Leadership Assessment | Proposed |
| **4** | CAP-BUSINESS-SUIT-001 | Business Suitability Assessment | Proposed |
| **5** | CAP-FINANCE-PLAN-001 | Finance Planning Assessment | Proposed |
| **6** | CAP-MARRIAGE-COMPAT-001 | Marriage Compatibility Assessment | Proposed |
| **7** | CAP-HEALTH-BAL-001 | Health Balance Assessment | Proposed |
| **8** | CAP-LUCK-TIMING-001 | Luck Timing Decision Support | Proposed |

---

## 3. Release detail

### Release 1 — Career Selection Assessment

| Field | Value |
|-------|-------|
| Capability | CAP-CAREER-SEL-001 |
| Dependencies | Wave 1.1 Core |
| Commercial value | **High** — career entry / conversion |
| Estimated maturity | **Production V1** (complete) |
| Notes | First Commercial Capability on Result path |

### Release 2 — Promotion Readiness Assessment

| Field | Value |
|-------|-------|
| Capability | CAP-CAREER-PRO-001 |
| Dependencies | Wave 1.1 · **recommended:** CAP-CAREER-SEL-001 live |
| Commercial value | **High** — upsell / timing-sensitive career |
| Estimated maturity | Content not started → target Production after full Acceptance |
| Notes | **Do not start** until Product approval |

### Release 3 — Leadership Assessment

| Field | Value |
|-------|-------|
| Capability | CAP-CAREER-LED-001 |
| Dependencies | Wave 1.1 · CAP-CAREER-SEL-001 · Domain leadership decision model |
| Commercial value | **High** |
| Estimated maturity | Domain P0 light seed only — deep assessment TBD |
| Notes | Distinct from SEL leadership *posture* field |

### Release 4 — Business Suitability Assessment

| Field | Value |
|-------|-------|
| Capability | CAP-BUSINESS-SUIT-001 |
| Dependencies | Wave 1.1 · CAP-CAREER-SEL-001 · BU decision model |
| Commercial value | **High** — independent / founder path |
| Estimated maturity | Proposed |
| Notes | Product name may refine at Planned stage |

### Release 5 — Finance Planning Assessment

| Field | Value |
|-------|-------|
| Capability | CAP-FINANCE-PLAN-001 |
| Dependencies | Wave 1.1 · Finance domain architecture (future) |
| Commercial value | **Strategic** |
| Estimated maturity | Early Proposed — Domain pack required first |
| Notes | Ethics / claims review mandatory |

### Release 6 — Marriage Compatibility Assessment

| Field | Value |
|-------|-------|
| Capability | CAP-MARRIAGE-COMPAT-001 |
| Dependencies | Wave 1.1 · Relationship domain architecture (future) |
| Commercial value | **High** (consumer) |
| Estimated maturity | Early Proposed |
| Notes | Dual-chart / compatibility evidence model TBD |

### Release 7 — Health Balance Assessment

| Field | Value |
|-------|-------|
| Capability | CAP-HEALTH-BAL-001 |
| Dependencies | Wave 1.1 · Health domain · strong ethics gate |
| Commercial value | **Strategic** |
| Estimated maturity | Early Proposed |
| Notes | Non-medical framing required; claims tightly bounded |

### Release 8 — Luck Timing Decision Support

| Field | Value |
|-------|-------|
| Capability | CAP-LUCK-TIMING-001 |
| Dependencies | Wave 1.1 · Luck/timing evidence · prior career/business caps recommended |
| Commercial value | **High** — decision timing upsell |
| Estimated maturity | Proposed (cross-cutting) |
| Notes | Distinct from light timing lines inside Career Selection |

---

## 4. Dependency overview

```
Wave 1.1 Core (frozen)
        │
        ▼
R1 Career Selection ──────────────────────────────► (live)
        │
        ├────────► R2 Promotion Readiness
        ├────────► R3 Leadership
        └────────► R4 Business Suitability
                         │
        Future domains ──┼──► R5 Finance
                         ├──► R6 Marriage
                         └──► R7 Health
        Cross-cutting ────────► R8 Luck Timing
```

---

## 5. Maturity legend

| Label | Meaning |
|-------|---------|
| Production V1 | Acceptance Pass; live |
| Proposed | Registry only |
| Planned | Scoped; not yet authoring |
| Authoring / Golden / Integration | Per Release Policy stages |

---

## 6. Change control

- Roadmap order changes require Product Owner approval  
- Inserting a capability ahead of Release 2 requires Registry + Changelog update  
- Completing a release updates Registry Status/Stage and Changelog  

---

## 7. Stop line

Release 1 complete.  

**Stop. Do not start Release 2 (Promotion Readiness) without Product approval.**

---

END
