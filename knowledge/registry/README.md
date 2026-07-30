# BTE Global Knowledge Registry Framework

**Module:** Knowledge Global Registry  
**Version:** V1.0.0  
**Status:** Official Framework  
**Governance Alignment:** Governance V1.0 (frozen — not modified)  

Frozen modules (not modified by this framework):

- Governance V1.0 (including `knowledge/governance/registry/`)
- Reference Library
- Terminology Framework
- Knowledge Canon Framework
- Rule Database Framework
- Sentence Library Framework
- Golden Dataset Framework
- Report Template Framework

---

## Purpose

The Global Knowledge Registry Framework provides a unified, documentary catalog layer for locating Knowledge Infrastructure identities across modules.

It indexes:

- References
- Terminology
- Knowledge Assets
- Rules
- Sentences
- Datasets
- Reports
- Versions
- Traceability links

This release is **framework only**. It does not create actual registry entries.

---

## Scope

In scope:

- Global registry architecture
- Per-registry README / INDEX / TEMPLATE / SPEC
- Cross-module identity conventions

Out of scope:

- Populating registry rows
- Modifying domain module registries already frozen
- Modifying Governance registries
- Runtime registry services

---

## Directory Structure

```
knowledge/registry/
├── README.md
├── CHANGELOG.md
├── references/
├── terminology/
├── knowledge_assets/
├── rules/
├── sentences/
├── datasets/
├── reports/
├── versions/
└── traceability/
```

Each registry module contains:

- `README.md`
- `INDEX.md`
- `TEMPLATE.md`
- `SPEC.md`

---

## Identity Prefix Map

| Registry | Primary ID Pattern | Source Module |
|----------|--------------------|---------------|
| references | `REF-NNNNNN` | `knowledge/references/` |
| terminology | `TERM-NNNNNN` | `knowledge/terminology/` |
| knowledge_assets | `KNO-NNNNNN` | `knowledge/knowledge_canon/` |
| rules | `RUL-NNNNNN` | `knowledge/rule_database/` |
| sentences | `SEN-NNNNNN` | `knowledge/sentence_library/` |
| datasets | `CASE-NNNNNN` | `knowledge/golden_dataset/` |
| reports | `RPT-NNNNNN` | `knowledge/report_templates/` |
| versions | Version labels (`V#.#.#`) + asset ID | Cross-module |
| traceability | Trace records linking IDs | Cross-module |

---

## Design Principles

1. **Index, do not own content** — authoritative records remain in domain modules
2. **One ID, one row** — no duplicate catalog identities
3. **Empty over fake** — no invented entries in framework phase
4. **Governance compatibility** — complements Governance registries without editing them
5. **Frozen boundaries** — do not modify completed modules

---

## How Registries Relate to Domain Modules

```
Domain Module Record (authoritative)
            ↓
   Global Registry INDEX (locator)
            ↓
 Governance Registry (policy/control plane; frozen)
```

If a Global Registry INDEX and a domain module INDEX disagree, the **domain module record wins** until reconciliation.

---

## Framework Phase Status

All registry INDEX tables are empty by design in V1.0.0.
