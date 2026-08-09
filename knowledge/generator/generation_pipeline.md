# Generation Pipeline

| Field | Value |
|-------|-------|
| **Pipeline id** | `GEN-PIPELINE-V1` |
| **Generator version** | 1.0.0 |
| **Status** | Canonical |
| **Runtime** | None |

Every generated package walks these thirteen stages in order. Each stage declares inputs, outputs, dependencies, and completion criteria.

N/A for a package type is still a recorded result (`not_applicable`), never a silent skip.

---

## Stage map

| # | Stage id | KD-4 status after stage | Typical actor |
|---|----------|-------------------------|---------------|
| 1 | `profile` | idea / pre-draft | Knowledge Author |
| 2 | `package_skeleton` | `draft` | Author / AI (draft) |
| 3 | `metadata` | `draft` | Author / AI (draft) |
| 4 | `manifest` | `draft` | Author / AI (draft) |
| 5 | `rules` | `draft` | Author / AI (draft) |
| 6 | `evidence` | `draft` | Author / AI (draft) |
| 7 | `reasoning` | `draft` | Author / AI (draft) |
| 8 | `examples` | `draft` | Author / AI (draft) |
| 9 | `tests` | `draft` | Author / AI (draft) |
| 10 | `validation` | `review` when PVP-STANDARD requested | Technical Reviewer |
| 11 | `documentation` | `review` / `validated` | Author + Domain Reviewer |
| 12 | `release_candidate` | `validated` | Release Manager |
| 13 | `released_package` | `released` | Release Manager + Domain Reviewer |

---

## 1. Profile

**Purpose.** Bind identity, type, domain, counts, and quality target.

| | |
|--|--|
| **Inputs** | Type profile (`GEN-TYPE-*`) and/or instance profile (`GEN-INST-*`); taxonomy `domains.json`; reserved id ranges |
| **Outputs** | Resolved profile (inheritance merged); reserved `package_id` and `rule_id_prefix` |
| **Dependencies** | KD-2 taxonomy/ontology; KD-3 naming; `package_profile.schema.json` |
| **Completion** | Profile validates against schema; `domain.domain_id` exists; inheritance acyclic; placeholders resolved for instance profiles; `target_rule_count.minimum` ≤ recommended |

---

## 2. Package Skeleton

**Purpose.** Create KD-3 folder anatomy without analytical content.

| | |
|--|--|
| **Inputs** | Resolved profile; `generation_templates/`; `knowledge/authoring/package_template/` |
| **Outputs** | `<package_id>/` with `PACKAGE.json` (`status=draft`), empty component folders required by type, `README.md` stub, `CHANGELOG.md` stub |
| **Dependencies** | Stage 1; KD-3 folder layout; folder name = `package_id` |
| **Completion** | Folder exists; `PACKAGE.json` required identity fields present; checksum `value` is `null`; no production rules yet |

Monorepo note: BTE may nest packages under `knowledge/packages/<domain>/<name>/` while `package_id` remains the KD-3 id (Strength Core pattern). Generator MUST record `layout.monorepo_path` in metadata when nested.

---

## 3. Metadata

**Purpose.** Fill package-level and object-level metadata.

| | |
|--|--|
| **Inputs** | Skeleton; `package_metadata.json` template; profile `domain`, `language`, `school` |
| **Outputs** | `metadata/package_metadata.json`; optional localized labels |
| **Dependencies** | Stage 2; KD-1 / METADATA_STANDARD |
| **Completion** | Required metadata fields non-empty; `domain_id` matches profile; `generator_version` and `profile_id` recorded |

---

## 4. Manifest

**Purpose.** Declare components, exports, dependencies, validation profile.

| | |
|--|--|
| **Inputs** | Metadata; `package_manifest.json` template; profile `components` and `dependencies` |
| **Outputs** | `MANIFEST.json`; optional `DEPENDENCIES.json` |
| **Dependencies** | Stage 3; KD-3 manifest schema |
| **Completion** | Component `required` flags match profile; dependency graph acyclic; `validation_profile` set; `exported_objects` listed or explicitly empty |

---

## 5. Rules

**Purpose.** Author knowledge objects (rules, sentences, blocks, catalogs) — **not** engine logic.

| | |
|--|--|
| **Inputs** | Manifest; `rule_template.json`; reserved prefix; profile `target_rule_count` |
| **Outputs** | `rules/*.json` objects |
| **Dependencies** | Stage 4; KD-1 object schema; KD-4 rule authoring; Database-first principle (no hard-coded engine ifs) |
| **Completion** | Count ≥ `target_rule_count.minimum` when rules are required; ids unique and prefixed; no duplicate keys; enabled flags honest (`false` until review if required by type policy); metadata.package_id matches |

For `metadata` / some `sentence` packages, this stage may emit catalog objects instead of analytical rules and record `not_applicable` for analytical-rule count.

**Forbidden:** new unpublished analytical theory; modifying Rule Engine; editing existing released rule files in other packages.

---

## 6. Evidence

**Purpose.** Attach KX-1B evidence to every rule that requires it.

| | |
|--|--|
| **Inputs** | Rules; `evidence_template.json`; references |
| **Outputs** | `evidence/` bundles, explanations, examples, conflicts, traceability, index |
| **Dependencies** | Stage 5; KX-1B Strength evidence model as gold standard |
| **Completion** | If `evidence_required`: one bundle per production rule; positive + negative example present; `confidence_level` declared; references exist or `todo_review` recorded |

If `evidence_required` is false: write `VALIDATION` note `evidence: not_applicable`.

---

## 7. Reasoning

**Purpose.** Declare KX-1C reasoning graphs for conclusions the package owns.

| | |
|--|--|
| **Inputs** | Rules + evidence; `reasoning_template.json`; `knowledge/reasoning/*.schema.json` |
| **Outputs** | `reasoning/nodes`, `edges`, `chains`, `traces`, `confidence`, `examples` |
| **Dependencies** | Stage 6; Reasoning Framework 1.0.0 |
| **Completion** | If `reasoning_required`: ≥1 chain with Observation → Evidence → Inference → Intermediate → Final; all `source_rule` / `source_evidence` resolve; graph acyclic; confidence modes declared |

If `reasoning_required` is false: record `not_applicable`.

---

## 8. Examples

**Purpose.** Package-local worked examples (not Golden Dataset).

| | |
|--|--|
| **Inputs** | Rules / evidence / reasoning; `example_template.json` |
| **Outputs** | `examples/` JSON (+ optional Markdown walkthroughs) |
| **Dependencies** | Stages 5–7 as required by type |
| **Completion** | If `example_required`: at least one complete example per primary conclusion class (e.g. Strong / Weak / Balanced for Strength-like packs) |

---

## 9. Tests

**Purpose.** Package-local fixtures and assertions. Not platform pytest of engines.

| | |
|--|--|
| **Inputs** | Examples; KD-4 test expectations |
| **Outputs** | `tests/` fixtures (schema/id/count/status assertions) |
| **Dependencies** | Stage 8 when examples exist; otherwise stage 5 |
| **Completion** | Analytical / interpretation / report types have tests folder when quality_target ≥ gold; tests MUST NOT import engines; tests MUST NOT mutate Golden Dataset |

---

## 10. Validation

**Purpose.** Run the specified validation profile (conceptually). No runtime in Generator v1.0.

| | |
|--|--|
| **Inputs** | Full draft package; `generation_validation.md`; KD-4 `VALIDATION_PIPELINE.md` |
| **Outputs** | `VALIDATION.json` from `validation_template.json` |
| **Dependencies** | Stages 2–9; PVP-* profile from resolved profile (may upgrade toward release) |
| **Completion** | Required stages for the active PVP are `pass` or honest `not_applicable`; errors block; warnings listed |

---

## 11. Documentation

**Purpose.** Human-readable package docs.

| | |
|--|--|
| **Inputs** | `documentation_template.json`; profile notes; assumptions |
| **Outputs** | `README.md`, `CHANGELOG.md`, `documentation/overview.md`, type-specific docs |
| **Dependencies** | Stage 10 findings included honestly |
| **Completion** | README states purpose, domain, version, limitations; CHANGELOG has Unreleased or version section; no engine implementation claims |

---

## 12. Release Candidate

**Purpose.** Freeze content; upgrade validation to `PVP-RELEASE` minus final checksum seal.

| | |
|--|--|
| **Inputs** | Validated package; KD-4 release checklist; `package_release.json` draft |
| **Outputs** | `status=validated`; `RELEASE.json` draft; quality gate ≥ Bronze (default official target Silver) |
| **Dependencies** | Stages 10–11; KD-4 `release_candidate` state; separation of duties |
| **Completion** | Content frozen; Technical + Domain review recorded; checksum scope listed; `value` still placeholder or two-pass ready |

---

## 13. Released Package

**Purpose.** Immutable publication unit.

| | |
|--|--|
| **Inputs** | Release candidate; Release Manager + Domain Reviewer approval |
| **Outputs** | `status=released`; sealed SHA-256; `RELEASE.json`; index entry (when platform index is updated in a later sprint) |
| **Dependencies** | Stage 12; KD-3 immutability; two-pass checksum |
| **Completion** | Bytes immutable; `package_version` published; generator_version + profile_id retained in metadata; no further edits without a new version |

---

## Determinism

Same resolved profile + same templates + same authored content + locale `C` sort ⇒ same file set and same checksum after seal.

Random UUIDs, wall-clock-only ids, and unordered object emission are prohibited (GC-DETERMINISTIC).
