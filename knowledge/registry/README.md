# BTE Registry Module

**Module:** Knowledge Registry  
**Path:** `knowledge/registry/`  
**Version:** V1.0.0  
**Status:** Official Implementation Scaffold  
**Governance Alignment:** Governance V1.0 (frozen — not modified)  

Architecture specifications (read-only references):

- `knowledge/knowledge_canon/registry/REGISTRY_SPEC.md`
- `knowledge/knowledge_canon/registry/REGISTRY_TEMPLATE.md`
- `knowledge/knowledge_canon/registry/REGISTRY_MAPPING_STANDARD.md`
- `knowledge/knowledge_canon/registry/REGISTRY_TRACEABILITY_SPEC.md`
- `knowledge/knowledge_canon/registry/REGISTRY_QUALITY_STANDARD.md`
- `knowledge/knowledge_canon/registry/REGISTRY_REVIEW_GUIDE.md`
- `knowledge/knowledge_canon/registry/REGISTRY_JSON_SCHEMA.md`
- `knowledge/knowledge_canon/registry/REGISTRY_ID_STANDARD.md`
- `knowledge/knowledge_canon/registry/REGISTRY_STATE_MODEL.md`
- `knowledge/knowledge_canon/registry/CHANGELOG.md`
- `knowledge/knowledge_canon/registry/EDGE_CASES.md`

---

## Purpose

The Registry Module is the authoritative **metadata catalog** for canonical objects managed by the BTE Platform.

It indexes:

- References
- Terminology
- Knowledge Assets
- Rules
- Sentences
- Datasets
- Reports
- Cross-domain Global Registry metadata

This release is an **implementation scaffold**. Catalog `records` arrays are empty by design. No business logic, Rule Engine, or Interpretation Engine is included.

---

## Directory Structure

```
knowledge/registry/
├── README.md
├── CHANGELOG.md
├── schemas/
│   ├── registry_record.schema.json
│   └── registry_container.schema.json
├── samples/
│   └── empty_registry_record.json
├── global_registry/
├── knowledge_registry/
├── rule_registry/
├── sentence_registry/
├── reference_registry/
├── terminology_registry/
├── dataset_registry/
├── report_registry/
├── references/              # Prior locator framework (preserved)
├── terminology/             # Prior locator framework (preserved)
├── knowledge_assets/        # Prior locator framework (preserved)
├── rules/                   # Prior locator framework (preserved)
├── sentences/               # Prior locator framework (preserved)
├── datasets/                # Prior locator framework (preserved)
├── reports/                 # Prior locator framework (preserved)
├── versions/                # Prior locator framework (preserved)
└── traceability/            # Prior locator framework (preserved)
```

---

## Registry Domains (V1.0 Implementation)

| Directory | Prefix | Object ID | Source Module |
|-----------|--------|-----------|---------------|
| `global_registry/` | `GREG` | `REG-*` | Cross-domain |
| `knowledge_registry/` | `KREG` | `KNO-*` | `knowledge/knowledge_canon/` |
| `rule_registry/` | `RREG` | `RUL-*` | `knowledge/rule_database/` |
| `sentence_registry/` | `SREG` | `SEN-*` | `knowledge/sentence_library/` |
| `reference_registry/` | `REFREG` | `REF-*` | `knowledge/references/` |
| `terminology_registry/` | `TREG` | `TERM-*` | `knowledge/terminology/` |
| `dataset_registry/` | `DREG` | `CASE-*` | `knowledge/golden_dataset/` |
| `report_registry/` | `PREG` | `RPT-*` | `knowledge/report_templates/` |

Each domain registry contains:

- `README.md`
- Domain `*_REGISTRY_SPEC.md`
- Primary `*_registry.json`
- Index JSON files
- `samples/empty_registry_record.json`

---

## Global Registry Artifacts

| File | Role |
|------|------|
| `global_registry/GLOBAL_REGISTRY_SPEC.md` | Domain specification |
| `global_registry/global_registry.json` | Global catalog |
| `global_registry/namespace_registry.json` | Canonical namespaces |
| `global_registry/object_type_registry.json` | Canonical object types |
| `global_registry/registry_index.json` | Master domain index |
| `global_registry/registry_statistics.json` | Aggregate statistics |

---

## Identity Prefix Map

| Registry | Registry Prefix | Object ID Pattern |
|----------|-----------------|-------------------|
| Global | `GREG` | `REG-NNNNNN` |
| Knowledge | `KREG` | `KNO-NNNNNN` |
| Rule | `RREG` | `RUL-NNNNNN` |
| Sentence | `SREG` | `SEN-NNNNNN` |
| Terminology | `TREG` | `TERM-NNNNNN` |
| Dataset | `DREG` | `CASE-NNNNNN` |
| Report | `PREG` | `RPT-NNNNNN` |
| Reference | `REFREG` | `REF-NNNNNN` |
| Generic | `REG` | — |

---

## Design Principles

1. **Index, do not own content** — authoritative records remain in domain modules
2. **One Registry Record ↔ One Canonical Object**
3. **Empty over fake** — no invented catalog entries
4. **Schema-validated structure** — records conform to `schemas/registry_record.schema.json`
5. **Governance compatibility** — complements Governance registries without editing them
6. **Frozen boundaries** — do not modify completed source modules

---

## Authority Model

```
Domain Module Record (authoritative)
            ↓
   Registry Catalog (metadata / locator)
            ↓
 Governance Registry (policy/control plane; frozen)
```

If a Registry catalog and a domain module disagree, the **domain module record wins** until reconciliation.

---

## Schema Validation

- Record contract: `schemas/registry_record.schema.json`
- Container contract: `schemas/registry_container.schema.json`
- Empty structural sample: `samples/empty_registry_record.json`

Status values follow `REGISTRY_STATE_MODEL.md`:

`draft` → `validated` → `approved` → `registered` → `published` → `deprecated` → `archived`

---

## Prior Locator Framework

Directories `references/`, `terminology/`, `knowledge_assets/`, `rules/`, `sentences/`, `datasets/`, `reports/`, `versions/`, and `traceability/` remain as the earlier framework-phase locator docs.

They are preserved for backward compatibility. New registration work SHALL use the `*_registry/` catalogs above.

---

## Out of Scope (V1.0)

- Business logic
- Rule Engine
- Interpretation Engine
- Populated catalog records
- Runtime Registry Service
- Changes to Knowledge Canon content
- Changes to frozen Governance registries

---

## Infrastructure Layer (V1.1)

Runtime services (do not modify catalogs' architecture contracts):

- `services/registry_*.py`
- `registry_cli.py`
- Docs: `docs/registry/`
- Tests: `tests/registry/`
- CI: `.github/workflows/registry.yml`

```bash
python registry_cli.py validate --include-samples
python registry_cli.py stats
```

## TODOs

- TODO: Root architecture Markdown specs currently reside under `knowledge/knowledge_canon/registry/` while Document Module declares `knowledge/registry`. Confirm canonical documentation home with Chief Architect (no move performed).
- TODO: Confirm minimal index sets for Reference / Terminology / Dataset / Report registries.
- TODO: Confirm language-code enumeration for Sentence `language_index.json`.
- See also `docs/registry/ISSUE_REPORT.md` for infrastructure TODOs.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
