# Knowledge Factory Architecture — V1.0

| Field | Value |
|-------|-------|
| Document | KNOWLEDGE_FACTORY_ARCHITECTURE |
| Version | 1.0.0 |
| Section | 1 — Knowledge Factory |

---

# 1.1 What the Knowledge Factory is

The Knowledge Factory is the **platform production system** that turns professional interpretation doctrine into **production-ready Knowledge Units** consumable by the Reasoning Engine.

It defines:

- The **pipeline** every pack follows
- The **quality gates** no stage may skip
- The **roles** and approval chain
- The **versioning** and change rules after release

It is **process and governance**, not content.

---

# 1.2 Purpose

| Goal | Detail |
|------|--------|
| Repeatability | Pack 02, 03, … enter the same factory |
| Traceability | Every unit auditable from production back to source |
| Quality at scale | Thousands of units reviewed by phase, not ad hoc |
| Safe production | Frozen knowledge only in live Reasoning |
| Change control | No silent edits to production catalog |

---

# 1.3 Scope

### In scope

| Area | Factory owns |
|------|--------------|
| Authoring workflow | How Library prose is created and approved |
| Catalog conversion | How prose becomes deterministic units |
| QA orchestration | When and how QA runs (criteria = QA Standard) |
| Validation orchestration | Golden Case alignment before Freeze |
| Freeze and release | Immutability and production handoff |
| Change management | Post-release edits via new version |
| Pack onboarding | Entry requirements for new packs |
| Metrics | Official production KPIs |

### Out of scope (non-responsibilities)

| Area | Owner |
|------|-------|
| Rule Database facts | Database governance |
| Interpretation Standard (how to say) | Interpretation governance |
| Interpretation Knowledge content | Knowledge Author + Domain Reviewer |
| Catalog schema per pack | Catalog architecture (per pack) |
| QA criteria and scoring | Knowledge QA Standard V1.0 |
| Reasoning selection logic | Reasoning Engine |
| Composer sentence output | Interpretation Engine / Report |
| Production Engine implementation | Engineering |
| Customer-facing release notes | Product / Release Manager |

---

# 1.4 System boundaries

```text
                    KNOWLEDGE FACTORY
                    (orchestration)
                           │
     ┌─────────────────────┼─────────────────────┐
     ▼                     ▼                     ▼
Interpretation        Knowledge              Knowledge QA
Knowledge             Catalog                Standard
(prose)               (units)                (review rules)
     │                     │                     │
     └─────────────────────┼─────────────────────┘
                           ▼
                    Reasoning FREEZE
                    (golden validation)
                           │
                           ▼
                    Production Reasoning
                    (Frozen catalog only)
```

The Factory **does not store** knowledge. It defines **how artifacts move** between existing layers.

---

# 1.5 Artifact map

| Artifact | Location | Factory stage |
|----------|----------|---------------|
| Knowledge Library | `knowledge/interpretation_knowledge/PACK_XX_*/` | Authoring |
| Knowledge Catalog | `knowledge/knowledge_catalog/PACK_XX_*/` | Catalog |
| QA phase reviews | `knowledge/knowledge_qa/PACK_XX_*/` | QA |
| Golden references | `knowledge/reasoning_engine/PACK_XX_*/FREEZE/` | Validation |
| Factory docs | `knowledge/knowledge_factory/` | Meta |

---

# 1.6 Design principles

| Principle | Rule |
|-----------|------|
| No stage skipping | Every unit passes every gate or is explicitly waived with record |
| Human final authority | Cursor assists; humans approve Review, Validation, Freeze, Release |
| No production edit | Frozen units change only via new catalog version |
| QA not redefined | Factory references `knowledge/knowledge_qa/STANDARD/` |
| One pack, one factory | Packs do not invent parallel pipelines |
| Source fidelity | Catalog units trace to Library; no orphan knowledge |

---

# 1.7 Relationship to PACK-01

PACK-01 Strength is the **reference implementation** of the factory:

- Library: 13 chapters authored
- Catalog: 339 Draft units
- QA: Phases 01–03 (MEANING, CAUSES, ADVANTAGES)
- Validation / Freeze / Release: not yet complete

See [PIPELINE_EXAMPLES.md](PIPELINE_EXAMPLES.md).

---

END
