# Compiler Infrastructure — Version

**Module:** `knowledge/compiler`  
**Version:** `1.0.0`  
**Released:** 2026-07-31  
**Status:** Infrastructure Ready (metadata freeze candidate)  

---

## Version pin

| Component | Version | Source |
|-----------|---------|--------|
| Compiler metadata | 1.0.0 | `compiler_config.json` / this document |
| Pipeline | 1.0.0 | `pipeline.json` |
| Compiler schema | 1.0.0 | `compiler.schema.json` |
| Artifact registry | 1.0.0 | `artifact_registry.json` |
| Error registry | 1.0.0 | `error_registry.json` |
| Compatibility set | COMPAT-001 | `version_registry.json` |
| Bibliography (input) | 1.0.0 | frozen external module |
| Knowledge schema (input) | 1.0.0 | frozen external module |

---

## Final folder tree

```
knowledge/compiler/
├── README.md
├── VERSION.md
├── CHANGELOG.md
├── ROADMAP.md
├── VALIDATION_REPORT.md
├── compiler_config.json
├── compiler.schema.json
├── pipeline.json
├── stage_registry.json
├── artifact_registry.json
├── plugin_registry.json
├── error_registry.json
├── version_registry.json
├── statistics.json
└── examples/
    ├── README.md
    ├── pipeline_run.sample.json
    ├── stage_invocation.sample.json
    ├── compiler_error.sample.json
    └── validation_report.sample.json
```

---

## Known limitations

1. **Deferred artifact schemas** — `knowledge/compiler/schemas/*.schema.json` paths are contracts only; files not created.
2. **Partial schema coverage** — `pipeline` / `stage` / `plugin` / `error` registries not yet in `compiler.schema.json` `oneOf`.
3. **REF error-code collision** — compiler errors `REF-*` overlap Foundation Reference IDs `REF-*`.
4. **No runtime** — statistics counters remain zero; no compile execution.
5. **Examples non-normative** — must not be treated as academic or production telemetry.
6. **Plugin registry is hooks-only** — no plugin implementations bound.
7. **Publish authorization format** — referenced as artifact; concrete auth schema deferred.

---

## Ready-for-implementation checklist

Use this before starting runtime Compiler implementation (outside this folder).

### Metadata readiness

- [x] Pipeline stages LOAD…PUBLISH defined
- [x] Stage registry synced
- [x] Artifact registry includes required compile outputs
- [x] Error namespaces + seed codes defined
- [x] Version compatibility set COMPAT-001 defined
- [x] Statistics model defined
- [x] Sprint 2D validation report PASS (0 ERROR)
- [x] Documentation pack (README / VERSION / CHANGELOG / ROADMAP)

### Implementation prerequisites (next engineering sprint)

- [ ] Decide REF error-namespace rename or ADR for disambiguation
- [ ] Add schema `oneOf` branches for remaining registries
- [ ] Create deferred `schemas/` JSON Schema files (or mark TODO explicitly)
- [ ] Implement runtime loader that reads these registries (code outside `knowledge/compiler/`)
- [ ] Wire Validation Engine to `error_registry.json` codes
- [ ] Wire publish gate to `publish_authorization` artifact
- [ ] CI job: validate schema-covered JSON + cross-ref checks
- [ ] Do **not** generate academic Knowledge Records until Academic Design + authorization gates pass

### Freeze recommendation

Metadata may be treated as **v1.0.0 freeze candidate** for implementation kickoff, accepting Known limitations as tracked follow-ups.
