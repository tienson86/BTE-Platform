# Validation Pipeline

**Status:** Canonical specification  
**Sprint:** KD-4  
**Runtime:** None — do not implement validators in this sprint

Aligns with:

- `knowledge/package_spec/package_validation.schema.json`
- `knowledge/validation/v2/VALIDATION_SPEC.md`

---

## Philosophy

Validation is deterministic, ordered, and fail-closed.

1. Same inputs → same diagnostics (sort paths and ids, locale `C`).
2. Stages run in the sequence below; a stage may be `skipped` only when marked optional for the active profile.
3. `error` blocks promotion. `warning` requires acknowledgment before release. `info` is advisory.
4. Golden Dataset files are **read-only**. Failures mean the package is wrong or a waiver is required — never edit golden/snapshot/expected output to pass.
5. Future automated tooling MUST implement this sequence, not a different ad-hoc order.

---

## Profiles

Defined in `validation_profiles.json`.

| Profile | When | Stages |
|---------|------|--------|
| `PVP-MINIMAL` | draft submit | 1–2 |
| `PVP-STANDARD` | technical + knowledge review | 1–7 |
| `PVP-RELEASE` | release candidate → released | 1–9 |

---

## Sequence

Machine form: `validation_sequence.json`.

### 1. Schema Validation

| | |
|--|--|
| **Input** | `PACKAGE.json`, `MANIFEST.json`, present `DEPENDENCIES.json` / `RELEASE.json` / `VALIDATION.json`, exported objects |
| **Output** | Pass/fail per file; JSON Schema diagnostics |
| **Fail** | Any required file fails its KD-3 / V2 schema |

### 2. Metadata Validation

| | |
|--|--|
| **Input** | Identity + manifest `metadata` + taxonomy domains |
| **Output** | Consistency report |
| **Fail** | Missing required identity fields; `package_id` mismatch; unknown `domain_id`; status/language/author disagree across files |

### 3. Dependency Validation

| | |
|--|--|
| **Input** | Manifest dependencies, `DEPENDENCIES.json`, package index |
| **Output** | Resolved graph + order |
| **Fail** | Missing required target; cycle; self-dependency; `required_packages` list disagrees; conflict co-selected |

### 4. Reference Validation

| | |
|--|--|
| **Input** | Object `references`, exported ids, dependency exports |
| **Output** | Resolved / unresolved lists |
| **Fail** | Knowledge-id reference does not resolve. Unresolved document paths are warnings unless profile forbids them. |

### 5. Integrity Validation

| | |
|--|--|
| **Input** | Manifest `files` / `components.paths`, package tree, exported ids |
| **Output** | Missing/extra file lists; duplicate id list |
| **Fail** | Declared path missing; duplicate id in release corpus; folder name ≠ `package_id` |

Checksum non-null is **not** required here before release (see stage 9).

### 6. Compatibility Validation

| | |
|--|--|
| **Input** | `compatibility` ranges, active schema/knowledge/platform versions, languages, schools |
| **Output** | In-range / out-of-range matrix |
| **Fail** | Active schema outside min/max; incompatible language/school undeclared; `compatible_with_v1` missing |

### 7. Quality Validation

| | |
|--|--|
| **Input** | Package tree + `quality/quality_rules.json` + intended level |
| **Output** | Metric scores + level achieved |
| **Fail** | Achieved level < intended level required by the gate |

### 8. Golden Dataset Validation

| | |
|--|--|
| **Input** | Existing Golden Dataset tests for affected modules; package exports (read-only) |
| **Output** | Pass / fail / `not_applicable` |
| **Fail** | Any golden test fails. **Do not** modify golden, snapshot, or expected output. |
| **Skip** | Allowed when package type cannot affect engine outputs (`minimal`, `metadata`, `reference`) and waiver recorded |

Specification only: this stage names which existing tests *would* be invoked. KD-4 does not run pytest.

### 9. Release Validation

| | |
|--|--|
| **Input** | `RELEASE.json`, checksum scope, version fields, release checklist |
| **Output** | Publication-readiness report |
| **Fail** | Missing release notes; null checksum; version mismatch; required deps not released; immutability not declared; unacknowledged warnings |

---

## Outputs

Every run SHOULD produce / update `VALIDATION.json` matching `package_validation.schema.json`, plus optional quality attachment:

- `status`: `pass` / `pass_with_warnings` / `fail` / `not_run`
- `checks[]` for stages 1–9 (`quality_validation`, `golden_dataset_validation`, `release_validation` extend KD-3 check ids)
- `diagnostics[]` sorted by `code`, then `path`

KD-3 schema enum lists seven check ids. Reports MAY use `additionalProperties` / extended check ids in `checks[].id` as strings beyond the enum when tools emit KD-4 stages. Until the schema is revised in a future sprint, store KD-4-only stages in `diagnostics` with codes `VAL-QUALITY`, `VAL-GOLDEN`, `VAL-RELEASE` if a strict KD-3 validator is used.

---

## Failure handling

| Result | Workflow effect |
|--------|-----------------|
| fail in stages 1–6 | `technical_validation` → `draft` |
| fail stage 7 (domain quality) | `knowledge_review` → `draft` |
| fail stage 8–9 | remain / return to `release_candidate` or `knowledge_review`; do not release |
