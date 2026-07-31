# Compiler Infrastructure Changelog

**Module:** `knowledge/compiler`  
**Versioning:** Semantic (`MAJOR.MINOR.PATCH`)

---

## [1.0.0] — 2026-07-31

### Status

Infrastructure Ready (metadata freeze candidate)

### Added — Sprint 2A (Registry Foundation)

- `compiler_config.json`
- `compiler.schema.json` (initial config schema)
- `pipeline.json` (LOAD…PUBLISH)
- `stage_registry.json`
- Initial artifact / plugin / error / version / statistics registries
- Example pipeline run + stage invocation samples

### Added — Sprint 2B (Artifact Registry)

- Artifact contracts with `id`, `name`, `description`, `version`, `schema`, `producer`, `consumer`
- Required artifacts: `knowledge_record_json`, `knowledge_graph`, `dependency_graph`, `metadata_index`, `search_index`, `validation_report`, `compilation_report`, `statistics_report`
- Version registry components: Compiler, Pipeline, Schema, Pack, Knowledge Canon, Artifact Registry, Bibliography
- Statistics model (`model` + zeroed `current`)
- Expanded `compiler.schema.json` (`oneOf` for config / artifact / version / statistics)

### Added — Sprint 2C (Error Registry)

- Namespaces: VAL, PAR, DEP, REF, SCH, CMP, PUB, SYS
- Placeholder ranges `*-000001` … `*-000100`
- Seed error definitions (code/title/severity/description/recommended_action)
- Examples: `compiler_error.sample.json`, `validation_report.sample.json`

### Changed — Sprint 2D (Validation)

- Consistency audit → `VALIDATION_REPORT.md` (PASS with warnings)
- Fixed sample artifact ID prefix drift (`artifact:` → snake_case)
- Added `document_kind` / `document_name` consistency fields

### Added — Sprint 2E (Finalize docs)

- Improved `README.md`
- `examples/README.md`
- `CHANGELOG.md`
- `VERSION.md`
- `ROADMAP.md` (infrastructure only)

### Notes

- No runtime compiler code
- No academic document modifications
- No Knowledge Record JSON generation

---

## Unreleased

_No unreleased changes recorded._
