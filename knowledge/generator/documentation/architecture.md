# Generator Architecture

| Field | Value |
|-------|-------|
| **Generator version** | 1.0.0 |
| **Status** | Canonical |
| **Runtime** | None |

---

## 1. What the Generator is

A **Foundation specification** composed of:

```
knowledge/generator/
    schemas          generator.schema.json, package_profile.schema.json
    pipeline         generation_pipeline.md (GEN-PIPELINE-V1)
    workflow         generation_workflow.md  → KD-4 states
    constraints      GC-*
    validation       GV-* + PVP-*
    quality          Bronze → Platinum
    templates        emit skeletons
    type profiles    GEN-TYPE-*
    instance examples GEN-INST-*
    documentation    this folder
```

It is not an engine. It is not a package. Future AI runners and a visual builder consume these files.

---

## 2. Layering

```
KD-2 Taxonomy / Ontology
        ↓
KD-3 Package Specification          ← emitted shape
KD-4 Authoring & Validation         ← human gates
        ↓
Generator v1.0                      ← how to emit
        ↓
KX-1B Evidence + KX-1C Reasoning    ← optional/required by type
        ↓
Released Knowledge Package
        ↓
Interpretation Engine → Report Engine   ← consumers only
```

Dependency direction: Generator → specs. Engines never import generator profiles.

---

## 3. Profile inheritance model

```
GEN-PROFILE-COMMON
    GEN-TYPE-ANALYTICAL | INTERPRETATION | REPORT | METADATA | SENTENCE
        GEN-INST-*  (concrete package_id)
```

Merge: child overrides; arrays replace unless `inherit_arrays=append`; inheritance acyclic (GC-INHERIT-ACYCLIC).

Type profiles carry placeholders. Instance profiles resolve identity, domain, prefix, and counts.

---

## 4. Emission anatomy

Generated package (KD-3):

```
<package_id>/   or nested knowledge/packages/<area>/<name>/ with layout.monorepo_path
    PACKAGE.json
    MANIFEST.json
    DEPENDENCIES.json?
    RELEASE.json?
    VALIDATION.json
    README.md / CHANGELOG.md
    metadata/
    rules/
    evidence/          if required
    reasoning/         if required
    examples/
    tests/
    documentation/
    references/
```

---

## 5. Deterministic control points

| Point | Rule |
|-------|------|
| Ids | reserved prefix + zero-padded sequence |
| File lists | locale `C` sort |
| Checksum | KD-3 two-pass SHA-256 |
| Pipeline | 13 stages, no skip |
| N/A stages | explicit `not_applicable` |

---

## 6. Extension points (non-breaking)

- New instance profiles
- New type profiles inheriting COMMON
- New templates that still validate against existing schemas
- New GC-* / GV-* ids (MINOR generator bump if meaning changes)

Breaking: stage reorder, required profile field removal, enum shrink → MAJOR `generator_version`.

---

## 7. Out of scope

Rule Engine, Analysis Engine, Interpretation Engine, Report Engine, API, contracts, Golden Dataset, existing released packages.
