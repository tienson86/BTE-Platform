# 00 — Product Index · Capability Registry V1

Version: 1.0.0  
Status: **OFFICIAL — Capability Registry V1**  
Date: 2026-08-08  
Owner: BTE Product  
Depends on: Product Manifesto · V1 Architecture Freeze · Domain 01 CAP-D1-CA-SEL Production V1  
Scope: **Documentation only** — no runtime, no Knowledge Units, no implementation  

---

## 1. Purpose

BTE has transitioned from architecture-driven development to **capability-driven product evolution**.

This folder is the **product governance surface** for every customer-facing commercial capability.

```
Product Manifesto (constitution)
        ↓
Capability Registry (this pack) ← single source of truth for capabilities
        ↓
Domain packs / Knowledge / Narrative / Portal (implementation & delivery)
```

---

## 2. Reading order

| Order | File | Content |
|------:|------|---------|
| 0 | `00_PRODUCT_INDEX.md` | This index |
| 1 | `01_CAPABILITY_REGISTRY.md` | Official registry of capabilities |
| 2 | `02_CAPABILITY_RELEASE_POLICY.md` | Stages, entry/exit, rollback |
| 3 | `03_CAPABILITY_LIFECYCLE.md` | Idea → Retirement lifecycle |
| 4 | `04_CAPABILITY_ACCEPTANCE_STANDARD.md` | Mandatory acceptance gates |
| 5 | `05_PRODUCT_ROADMAP.md` | Capability-ordered roadmap |
| 6 | `06_PRODUCT_CHANGELOG.md` | Official capability release log |
| — | `BTE_PRODUCT_MANIFESTO.md` | Product constitution (pre-existing) |

---

## 3. Architectural principles

| Principle | Meaning |
|-----------|---------|
| **Capability is the release unit** | Product ships capabilities, not engines or CSV rows |
| **Knowledge Units are implementation** | Tracked in Domain / Database — not as product releases |
| **Narrative is presentation** | Composes capability meaning; does not redefine it |
| **Portal is delivery** | Surfaces capability on Result / Report paths |
| **Registry tracks customer value** | Only commercial, customer-facing capabilities |

---

## 4. Current production snapshot

| Registry ID | Name | Status | Production |
|-------------|------|--------|------------|
| **CAP-CAREER-SEL-001** | Career Selection Assessment | Released | **Yes (V1)** |

Domain alias: `CAP-D1-CA-SEL` · Domain 01 · Version 1.0.0  

**Do not start Promotion Readiness until Product approval.**

---

## 5. Non-goals (this pack)

- Authoring Knowledge Units  
- Modifying Wave 1.1, Foundation, Narrative, Portal, APIs, or runtime  
- Starting Release 2 (Promotion Readiness)  

---

## 6. Stop line

Capability Registry V1 is established.  

**Wait for Product approval before the next capability.**

---

END
