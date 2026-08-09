# Generation Validation

| Field | Value |
|-------|-------|
| **Generator version** | 1.0.0 |
| **Status** | Canonical |
| **Runtime** | None — no validator implementation |

Generation validation composes KD-4 stages with generator-specific checks (`GV-*`).

Profiles: `PVP-MINIMAL` → `PVP-STANDARD` → `PVP-RELEASE` (`knowledge/authoring/validation/validation_profiles.json`).

---

## 1. KD-4 stages (unchanged meaning)

| Stage | Checks |
|-------|--------|
| schema_validation | JSON Schema for package, manifest, objects, evidence, reasoning |
| metadata_validation | Required identity and metadata fields |
| dependency_validation | SemVer ranges, existence, cycles |
| reference_validation | Cited refs / rules / domains exist or `todo_review` |
| integrity_validation | Checksum scope, duplicate ids, orphan files vs manifest |
| compatibility_validation | schema/knowledge/platform ranges; V1 dual-read flags |
| quality_validation | `QM-*` vs `quality_target` |
| golden_dataset_validation | Read-only; `pass` or `not_applicable` with waiver |
| release_validation | Immutability, notes, checksum seal |

---

## 2. Generator checks

| Id | Name | Fail when |
|----|------|-----------|
| GV-PROFILE-SCHEMA | Profile schema | Profile fails `package_profile.schema.json` |
| GV-INHERIT | Inheritance | Missing parent or cycle |
| GV-PIPELINE-ORDER | Pipeline order | Stage completed without predecessor `pass` / `not_applicable` |
| GV-SKELETON | Skeleton | Folder ≠ `package_id` (or undeclared monorepo nest); missing `PACKAGE.json` |
| GV-PLACEHOLDER | Placeholders | `{{` remains at status ≥ `review` |
| GV-TAXONOMY-REF | Taxonomy | Unknown `domain_id` |
| GV-ONTOLOGY-REF | Ontology | Unknown `ONT-*` |
| GV-RULE-COUNT | Rule count | Production rule count < `target_rule_count.minimum` when rules required |
| GV-RULE-PREFIX | Rule prefix | Id outside reserved prefix |
| GV-DUP-ID | Duplicate ids | Any duplicate rule / evidence / node / edge / chain / trace / package id |
| GV-EVIDENCE-GAP | Missing evidence | `evidence_required` and a production rule has no bundle |
| GV-REASONING-GAP | Missing reasoning | `reasoning_required` and a primary conclusion class has no chain |
| GV-REASONING-REF | Reasoning refs | Node `source_rule` / `source_evidence` missing |
| GV-REASONING-CYCLE | Circular reasoning | Cycle in reasoning graph (KX-1C RG-005) |
| GV-ORPHAN-NODE | Orphan reasoning node | Node not on any chain and not listed as unused alternative/contradiction |
| GV-INVALID-EDGE | Invalid edge | Edge source/target missing or illegal relationship |
| GV-EXAMPLE-GAP | Missing examples | `example_required` and zero complete examples |
| GV-TEST-ENGINE | Test purity | Package tests import engines or mutate Golden Dataset |
| GV-EXISTING-PKG | Existing package | Diff touches a released package outside the new `package_id` |
| GV-ENGINE-TOUCH | Engine touch | Diff touches engine / API / contract trees |
| GV-QUALITY-CLAIM | Quality claim | `quality_target` not met |
| GV-AI-STATUS | AI ceiling | AI-only authorship with status ≠ `draft` |
| GV-TRACE | Trace fields | Missing `generator_version` or `profile_id` in metadata |

---

## 3. When checks apply

| PVP | Generator checks |
|-----|------------------|
| PVP-MINIMAL | GV-PROFILE-SCHEMA, GV-SKELETON, GV-TAXONOMY-REF, GV-DUP-ID (identity only) |
| PVP-STANDARD | All GV-* except GV-QUALITY-CLAIM at platinum extras; golden may be optional |
| PVP-RELEASE | All GV-*; golden_dataset_validation required as pass or waived N/A; checksum sealed |

---

## 4. Graph / package integrity (summary)

Validate:

- graph integrity (reasoning + dependency)
- missing nodes
- orphan nodes
- invalid edges
- circular reasoning
- missing rule references
- missing evidence references
- missing taxonomy / ontology references
- incomplete pipeline
- mutation of existing packages or engines

No runtime validator ships in Generator v1.0.
