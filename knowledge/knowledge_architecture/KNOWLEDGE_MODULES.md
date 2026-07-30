# Knowledge Modules

**Module:** `knowledge/knowledge_architecture`  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Module Catalog)

---

# 1. Purpose

This document catalogs the canonical Knowledge Modules of the BTE Platform and defines ownership, status, consumers, and asset scope for each module.

---

# 2. Module Catalog Principles

Each Knowledge Module shall:

- own exactly one knowledge domain;
- expose an abstract contract;
- publish versioned assets;
- declare dependencies explicitly;
- remain independent of engine internals.

---

# 3. Module Status Model

| Status | Meaning |
|--------|---------|
| Planned | Architecture recognized; content not yet delivered |
| Draft | Assets under construction |
| Validated | Passed governance validation |
| Published | Consumable by engines |
| Deprecated | Superseded; migration required |

---

# 4. Canonical Knowledge Modules

## 4.1 Fundamental Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | Shared BaZi fundamentals |
| Consumers | All analytical Knowledge Modules |
| Asset Families | Taxonomy, enumerations, shared references |

Provides shared elemental, stem/branch, and relational fundamentals.

---

## 4.2 Strength Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | Day Master strength |
| Consumers | Strength Engine |
| Asset Families | Rule Database |

---

## 4.3 Temperature Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | Climatic balance |
| Consumers | Temperature Engine |
| Asset Families | Rule Database |

---

## 4.4 Pattern Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | Pattern / Ge Ju |
| Consumers | Pattern Engine |
| Asset Families | Rule Database, Taxonomy |

---

## 4.5 Useful God Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | Yong Shen / Xi Shen / Ji Shen / Xian Shen |
| Consumers | Useful God Engine |
| Asset Families | Rule Database |

---

## 4.6 Ten Gods Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | Ten Gods structure and quality |
| Consumers | Ten Gods Engine |
| Asset Families | Rule Database |

---

## 4.7 Combination Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | Combinations, clashes, transformations |
| Consumers | Combination Engine |
| Asset Families | Rule Database |

---

## 4.8 ShenSha Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | ShenSha detection and ranking |
| Consumers | ShenSha Engine |
| Asset Families | Rule Database |

---

## 4.9 Luck Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | Da Yun / Liu Nian / Liu Yue / Liu Ri impacts |
| Consumers | Luck Engine |
| Asset Families | Rule Database |

---

## 4.10 Interpretation Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | Narrative interpretation |
| Consumers | Interpretation Engine |
| Asset Families | Sentence Library |

---

## 4.11 Report Knowledge

| Field | Value |
|-------|-------|
| Status | Planned |
| Domain | Report presentation |
| Consumers | Report Engine |
| Asset Families | Report Templates |

---

# 5. Engine Mapping

| Engine Stage | Knowledge Module |
|--------------|------------------|
| Strength Engine | Strength Knowledge |
| Temperature Engine | Temperature Knowledge |
| Pattern Engine | Pattern Knowledge |
| Useful God Engine | Useful God Knowledge |
| Ten Gods Engine | Ten Gods Knowledge |
| Combination Engine | Combination Knowledge |
| ShenSha Engine | ShenSha Knowledge |
| Luck Engine | Luck Knowledge |
| Interpretation Engine | Interpretation Knowledge |
| Report Engine | Report Knowledge |

---

# 6. Dependency Graph

```text
Fundamental Knowledge
        │
        ├── Strength Knowledge
        ├── Temperature Knowledge
        ├── Pattern Knowledge
        ├── Useful God Knowledge
        ├── Ten Gods Knowledge
        ├── Combination Knowledge
        ├── ShenSha Knowledge
        └── Luck Knowledge
                │
                ▼
        Interpretation Knowledge
                │
                ▼
        Report Knowledge
```

Downstream Knowledge Modules may declare dependency on upstream modules.

They must not reverse the dependency direction.

---

# 7. Module Contract Requirements

Every Knowledge Module shall publish:

- KnowledgeModuleDescriptor
- KnowledgeManifest
- version metadata
- asset catalog
- dependency declarations
- compatibility matrix
- validation report

---

# 8. Extensibility

Additional Knowledge Modules may be introduced for future domains.

New modules must:

- follow the abstract Knowledge Module contract;
- declare ownership and consumers;
- remain path-agnostic to engines;
- preserve Version 1.x compatibility for existing consumers.

---

# 9. Non-Duplication Rule

Business knowledge that already exists in one Knowledge Module shall not be duplicated in another.

Cross-module reuse occurs through references, not copies.
