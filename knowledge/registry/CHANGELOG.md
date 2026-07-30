# Registry Module Changelog

**Module:** `knowledge/registry`  
**Versioning:** Semantic (`MAJOR.MINOR.PATCH`)

Architecture change history for specifications also appears in:

`knowledge/knowledge_canon/registry/CHANGELOG.md`

---

## [1.0.0] — 2026-07-30

### Added

- Registry Module Implementation Scaffold under `knowledge/registry/`
- Domain registries:
  - `global_registry/`
  - `knowledge_registry/`
  - `rule_registry/`
  - `sentence_registry/`
  - `reference_registry/`
  - `terminology_registry/`
  - `dataset_registry/`
  - `report_registry/`
- Shared schemas: `schemas/registry_record.schema.json`, `schemas/registry_container.schema.json`
- Shared empty sample: `samples/empty_registry_record.json`
- Global artifacts: namespace, object type, registry index, statistics
- Domain SPECs, READMEs, catalogs, and index JSON files

### Changed

- Root `README.md` updated to document Implementation Scaffold layout while preserving prior locator framework directories

### Deprecated

None

### Removed

None

### Fixed

None

### Notes

- Catalog `records` arrays remain empty by design
- No fabricated business entries
- Frozen Knowledge Infrastructure modules and Governance registries not modified
- Prior locator framework directories (`references/`, `terminology/`, `knowledge_assets/`, `rules/`, `sentences/`, `datasets/`, `reports/`, `versions/`, `traceability/`) preserved

---

## [1.1.0] — 2026-07-30

### Added

- Registry infrastructure services under `services/registry_*.py`
- `registry_cli.py` (validate / stats / list / search / export / import / reindex)
- Unit tests in `tests/registry/`
- Docs in `docs/registry/`
- GitHub Actions workflow `.github/workflows/registry.yml`

### Notes

- Infrastructure only; Knowledge Canon and Rule Database untouched
- See `docs/registry/ISSUE_REPORT.md` for TODOs

---

## Unreleased

_No unreleased changes recorded._
