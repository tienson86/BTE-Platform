# Product Governance Foundation

| Field | Value |
|-------|-------|
| Document | Product Governance README |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Product Owner |
| Scope | Product constitution. Not engineering specification. |

This folder is the permanent **Product Governance Foundation** of BTE.

Every future feature, release, editorial decision, and commercial decision must align with these documents.

This pack does not describe how software is implemented.
It defines what the product is allowed to be.

---

## 1. Purpose

Product governance answers:

- What is BTE selling?
- Who is it for?
- What may ship?
- When is work Done?
- Who may approve change?
- What is out of scope?

Engineering, architecture, knowledge, and editorial work exist to serve these answers.
They do not replace them.

---

## 2. Difference between the five surfaces

| Surface | Question it answers | Official home | Does not |
|---------|---------------------|---------------|----------|
| **Architecture** | How the platform is structured and who owns analytical truth | `knowledge/docs/platform/` · `beta/BETA0_ARCHITECTURE_LOCK.md` | Decide commercial value or customer wording |
| **Knowledge** | What traditional and domain content is true and admissible | Knowledge Board · rule database · packages · `beta/BETA0_KNOWLEDGE_LOCK.md` | Compose customer sentences or ship a product |
| **Editorial** | May this sentence reach a paying customer? | `knowledge/editorial/BTE_EDITORIAL_STANDARD_V1.md` · `beta/BETA0_EDITORIAL_LOCK.md` | Recalculate charts or redesign the platform |
| **Product** | What the customer receives, and whether it is worth shipping | **This pack** · `BTE_PRODUCT_MANIFESTO.md` | Own engine internals or CSV schema |
| **Release** | Whether a build may leave the company | This pack’s release policy · `beta/BETA0_RELEASE_WORKFLOW.md` · capability release policy | Invent new product meaning |

If two surfaces conflict:

1. Product Manifesto decides identity and purpose.
2. This governance pack decides Done, change, acceptance, and commercial permission.
3. Beta 0 freeze decides what is locked for V1 Beta.
4. Architecture decides engine and pipeline boundaries.
5. Editorial Standard decides customer-facing language.
6. Knowledge Board decides admissible content.

Higher rows win product disputes.
Lower rows win their own specialised disputes.

---

## 3. How folders relate

```
BTE_PRODUCT_MANIFESTO.md          Identity and philosophy
        ↓
Product Governance Foundation     This pack — operating constitution
        ↓
beta/                             V1 Beta 0 platform freeze
        ↓
00_PRODUCT_INDEX.md               Capability registry (what commercial capabilities exist)
        ↓
Architecture / Knowledge / Editorial / Release specialised packs
        ↓
Runtime, engines, narrative, UI, reports
```

| Location | Role relative to this pack |
|----------|----------------------------|
| `knowledge/product/` (this README and the files listed below) | Product constitution and operating policy |
| `BTE_PRODUCT_MANIFESTO.md` | Highest identity document. This pack operationalises it. |
| `00_PRODUCT_INDEX.md` and `01`–`06` | Capability shipping register. Subordinate to this constitution. |
| `PACKAGING/` | Commercial packages. Must follow vision and principles here. |
| `knowledge/editorial/` | Editorial constitution for prose. |
| `knowledge/docs/platform/` | Architecture freeze and component catalog. |
| `beta/` | Beta 0 lock: no new subsystems without Product Owner approval. |
| `knowledge/releases/` | Release records. Must satisfy this pack’s Definition of Done. |

---

## 4. Documents in this foundation

| Document | Purpose |
|----------|---------|
| [BTE_PRODUCT_VISION_V1.md](BTE_PRODUCT_VISION_V1.md) | Mission, customer, positioning, success, out of scope |
| [PRODUCT_PRINCIPLES.md](PRODUCT_PRINCIPLES.md) | Frozen product principles |
| [PRODUCT_ROADMAP.md](PRODUCT_ROADMAP.md) | Product evolution by phase |
| [PRODUCT_DECISIONS.md](PRODUCT_DECISIONS.md) | Frozen product decisions |
| [PRODUCT_CHANGE_POLICY.md](PRODUCT_CHANGE_POLICY.md) | Change classes and approval |
| [PRODUCT_DEFINITION_OF_DONE.md](PRODUCT_DEFINITION_OF_DONE.md) | Official Done |
| [PRODUCT_ACCEPTANCE_POLICY.md](PRODUCT_ACCEPTANCE_POLICY.md) | Acceptance gates |
| [PRODUCT_GLOSSARY.md](PRODUCT_GLOSSARY.md) | Product vocabulary |
| [PRODUCT_RISK_REGISTER.md](PRODUCT_RISK_REGISTER.md) | Product risks and owners |
| [PRODUCT_ARCHITECTURE_PHILOSOPHY.md](PRODUCT_ARCHITECTURE_PHILOSOPHY.md) | Why product, truth, knowledge, and architecture stay separate |
| [PRODUCT_RELEASE_POLICY.md](PRODUCT_RELEASE_POLICY.md) | Release states and approval |

---

## 5. Standing rule

A Completion Report is not a product decision.
A passing test suite is not a product decision.
Only an artifact that has passed editorial, product, and Product Owner review is a product decision.

See [PRODUCT_DEFINITION_OF_DONE.md](PRODUCT_DEFINITION_OF_DONE.md).
