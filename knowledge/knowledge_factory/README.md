# Knowledge Factory — BTE Platform

| Field | Value |
|-------|-------|
| Layer | Platform Production System |
| Version | 1.0.0 |
| Status | Official |
| Scope | All Interpretation Knowledge packs |
| Date | 2026-08-12 |

---

# 1. What this is

The **Knowledge Factory** is the platform-wide production system that creates, reviews, validates, freezes, and publishes **Knowledge Units** for every Interpretation Knowledge pack.

It is the **orchestration layer** — not the content layer.

---

# 2. Document set

| File | Owns |
|------|------|
| [KNOWLEDGE_FACTORY_ARCHITECTURE.md](KNOWLEDGE_FACTORY_ARCHITECTURE.md) | Purpose, scope, responsibilities |
| [PRODUCTION_PIPELINE.md](PRODUCTION_PIPELINE.md) | End-to-end frozen pipeline |
| [AUTHORING_PIPELINE.md](AUTHORING_PIPELINE.md) | Knowledge Library creation |
| [CATALOG_PIPELINE.md](CATALOG_PIPELINE.md) | Library → Catalog conversion |
| [QA_PIPELINE.md](QA_PIPELINE.md) | QA stage (references QA Standard) |
| [VALIDATION_PIPELINE.md](VALIDATION_PIPELINE.md) | Golden Case validation |
| [FREEZE_PIPELINE.md](FREEZE_PIPELINE.md) | Immutability gate |
| [RELEASE_PIPELINE.md](RELEASE_PIPELINE.md) | Frozen → Production |
| [CHANGE_PIPELINE.md](CHANGE_PIPELINE.md) | Post-release change management |
| [LIFECYCLE.md](LIFECYCLE.md) | Unit and pack lifecycle |
| [ROLE_MODEL.md](ROLE_MODEL.md) | Frozen roles |
| [WORKFLOW.md](WORKFLOW.md) | Operational workflow |
| [APPROVAL_FLOW.md](APPROVAL_FLOW.md) | Human approval chain |
| [VERSIONING.md](VERSIONING.md) | Version dimensions |
| [QUALITY_GATES.md](QUALITY_GATES.md) | Gate definitions |
| [CHECKLISTS.md](CHECKLISTS.md) | Role checklists |
| [PACK_ONBOARDING.md](PACK_ONBOARDING.md) | New pack entry |
| [PIPELINE_EXAMPLES.md](PIPELINE_EXAMPLES.md) | PACK-01 walkthrough |
| [METRICS.md](METRICS.md) | Official metrics |
| [CHANGELOG.md](CHANGELOG.md) | Factory history |

---

# 3. What this is not

| Not | Layer |
|-----|-------|
| A pack | Content is per-pack |
| Rule Database | Facts and scores |
| Interpretation Standard | How to say |
| Interpretation Knowledge | What to say (authored content) |
| Knowledge Catalog | Machine-readable units (output artifact) |
| Knowledge QA Standard | Review criteria (referenced, not owned) |
| Reasoning Engine | Runtime selection |
| Report Engine | Layout and export |
| Production Engine code | Implementation |

---

# 4. Frozen pipeline (summary)

```text
Idea
  ↓
Draft (Knowledge Library)
  ↓
Knowledge Catalog
  ↓
QA
  ↓
Review
  ↓
Validation
  ↓
Freeze
  ↓
Production
  ↓
Release
```

Detail: [PRODUCTION_PIPELINE.md](PRODUCTION_PIPELINE.md).

---

# 5. External references (read-only)

| System | Path |
|--------|------|
| Interpretation Knowledge | `knowledge/interpretation_knowledge/PACK_XX_*/` |
| Knowledge Catalog | `knowledge/knowledge_catalog/PACK_XX_*/` |
| Knowledge QA Standard | `knowledge/knowledge_qa/STANDARD/` |
| Reasoning FREEZE | `knowledge/reasoning_engine/PACK_XX_*/FREEZE/` |
| Interpretation Standard | `knowledge/interpretation_standard/` |

The Factory **coordinates** these layers. It does not replace them.

---

# 6. Current state

| Pack | Factory stage |
|------|---------------|
| PACK-01 Strength | Library + Catalog authored (Draft); QA Phases 01–03 complete; not Validated/Frozen/Released |

Example: [PIPELINE_EXAMPLES.md](PIPELINE_EXAMPLES.md).

---

END
