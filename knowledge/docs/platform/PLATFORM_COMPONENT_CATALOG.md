# Platform Component Catalog

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_COMPONENT_CATALOG |
| **Platform version** | 1.0.0 |
| **Status** | Frozen inventory |
| **Owner** | BTE Architecture Board |

Every row below is Platform-frozen unless marked *reserved / inactive*.

---

## Knowledge Packages

| package_id | type | version | checksum prefix | owner |
|------------|------|---------|-----------------|-------|
| `bz_01_strength_core` | analytical | 1.2.0 | `74fd4ac8…` | Knowledge Board |
| `bz_02_seasonal_core` | analytical | 1.0.0 | `f394ba18…` | Knowledge Board |
| `bz_03_temperature_core` | analytical | 1.0.0 | `a2e4826b…` | Knowledge Board |
| `bz_04_pattern_core` | analytical | 1.0.0 | `24911267…` | Knowledge Board |
| `bz_05_pattern_evaluation` | analytical | 1.0.0 | `c4fa911d…` | Knowledge Board |
| `bz_06_useful_god_foundation` | decision | 1.0.0 | `78a6f7c8…` | Knowledge Board |
| `bz_07_useful_god_priority` | decision | 1.0.0 | `0bd55841…` | Knowledge Board |
| `bz_08_useful_god_override` | decision | 1.0.0 | `ce73017c…` | Knowledge Board |
| `bz_09_luck_foundation` | reference | 1.0.0 | `57933cd4…` | Knowledge Board |

Sealed releases are immutable. New capability = new `package_id` or new SemVer, never in-place edit.

---

## Engines

| Engine | Responsibility | Version |
|--------|----------------|---------|
| Calendar | Time / calendar only | 1.0.0 |
| Bazi | Chart only | 1.0.0 |
| Rule | Rule evaluation only | freeze baseline |
| Score | Scoring only | freeze baseline |
| Pattern | Pattern calculation only | freeze baseline |
| Analysis | Analysis orchestration only | 1.0.0 / 2.0.0 |
| Decision | Decision orchestration only | 1.0.0 |
| Luck | Timeline + luck analysis + luck decision | 1.0.0 |
| Interpretation | Context, selection, assembly (no AI rewrite) | 1.0.0 |
| Report | Structure, layout, in-memory render/export | 1.0.0 |

Supporting engines (`context_engine`, `knowledge_engine`, `narrative_engine`, and others) remain in the repository. They are not new AF-1 surfaces and MUST NOT be used to bypass canonical pipelines.

---

## Pipelines

| Pipeline | Active stages | Inactive (registered) |
|----------|---------------|------------------------|
| Canonical Analysis 2.0.0 | calendar → … → useful_god | luck_cycle, interpretation, report |
| Canonical Decision 1.0.0 | foundation → priority → override | luck_cycle, annual, monthly, interpretation |
| Canonical Luck 1.0.0 | timeline → analysis → decision | interpretation, report |
| Canonical Interpretation 1.0.0 | foundation → knowledge_selection → composition | report, ai_rewrite |
| Canonical Report 1.0.0 | foundation → layout → rendering | publisher, delivery, print |

---

## Contracts

| Contract | Function / surface | Version |
|----------|--------------------|---------|
| Analysis result | `analysis_result_contract()` | AX-2 2.0.0 |
| Decision result | `decision_result_contract()` | AX-3 1.0.0 |
| Timeline | `timeline_contract()` | LE-1 1.0.0 |
| Luck pipeline | `luck_pipeline_contract()` | AX-4 1.0.0 |
| Interpretation foundation | `interpretation_foundation_contract()` | IE-1 1.0.0 |
| Interpretation pipeline | `interpretation_pipeline_contract()` | IX-1 1.0.0 |
| Report foundation | `report_foundation_contract()` | RE-1 1.0.0 |
| Report pipeline | `report_pipeline_contract()` | RX-1 1.0.0 |
| Package published I/O | `assets/published_*.json` | bound to package_version |

Checksums: `knowledge/releases/v1.0/CONTRACT_INDEX.json` and `COMPONENT_CHECKSUMS.json`.

---

## Registries

| Registry | Location | Role |
|----------|----------|------|
| Analysis stage registry | `engines/analysis_engine/pipeline/stage_registry.py` | AX-2 catalog |
| Decision stage registry | `engines/decision_engine/pipeline/stage_registry.py` | AX-3 catalog |
| Luck stage registry | `engines/luck_engine/pipeline/stage_registry.py` | AX-4 catalog |
| Interpretation stage registry | `engines/interpretation_engine/pipeline/stage_registry.py` | IX-1 catalog |
| Report stage registry | `engines/report_engine/pipeline/stage_registry.py` | RX-1 catalog |
| Report module registry | `engines/report_engine/registry/module_registry.py` | RE-1 modules |
| Layout registry | `engines/report_engine/layout/layout_registry.py` | RE-2 stages |
| Renderer registry | `engines/report_engine/rendering/renderer_registry.py` | RE-3 renderers |
| Knowledge / governance registries | `knowledge/governance/registry/` | Knowledge assets |

---

## Contexts

| Context | Owner |
|---------|-------|
| Canonical Analysis Context | Analysis Engine |
| Canonical Decision Context | Decision Engine |
| Luck Timeline / Analysis / Decision contexts | Luck Engine |
| Canonical Interpretation Context | Interpretation Foundation |
| Composition context | IE-2 |
| Assembly context | IE-3 |
| Canonical Report Context | Report Foundation |
| Layout context | RE-2 |
| Rendering context | RE-3 |

Contexts are append-only. Upstream snapshots are immutable.

---

## Models

Result objects (dataclasses) are the only official engine outputs. Tuples and ad-hoc dicts are not public contracts.

Canonical aggregates:

- Canonical Analysis Result
- Canonical Decision Result
- Canonical Luck Result
- Canonical Interpretation Result
- Canonical Report Result (RX-1 pipeline aggregate)
- Canonical Report Artifact (RE-3 mime envelope)

---

## Validation Modules

| Module | Role |
|--------|------|
| KD-4 authoring / PVP | Package admission MINIMAL / STANDARD / RELEASE |
| Analysis / Decision / Luck / Interpretation / Report validators | Stage and result legality |
| Contract verifiers | SemVer + schema + published I/O before pipeline execution |

---

## Diagnostics / Trace / Audit

Every canonical pipeline publishes machine-readable:

- **Diagnostics** — structured codes; `run()` never raises to callers
- **Trace** — execution steps, timestamps, component versions
- **Audit** — contract, dependency, legality, determinism, version compatibility

---

## Package Loaders

| Loader | Role |
|--------|------|
| Knowledge package loader | Read-only package admission |
| Report package loader | RE-1 reserved; `packages_loaded = false` at freeze |
| Interpretation knowledge loader | Selection inputs only; no text generation |

Engines read Rule / Knowledge data. They do not write, update, or delete the database.

---

## Documentation

| Surface | Path |
|---------|------|
| Foundation freeze | `knowledge/docs/foundation/` |
| Platform freeze | `knowledge/docs/platform/` |
| Knowledge architecture | `knowledge/docs/architecture/` |
| ADRs | `knowledge/governance/architecture/ADR/` |
| Release v1.0 | `knowledge/releases/v1.0/` |
| Engine docs | `engines/*/documentation/` |

---

## Extension points (not active)

- Luck / Interpretation / Report stages reserved inside Analysis and Decision registries
- Report publisher, email delivery, print
- Interpretation AI rewrite
- Renderers `xlsx` / `pptx`
- New knowledge domains (Feng Shui / Qi Men / I Ching) as new packages
