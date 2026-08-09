# Foundation Component Catalog

| Field | Value |
|-------|-------|
| **Document** | FOUNDATION_COMPONENT_CATALOG |
| **Foundation version** | 1.0.0 |
| **Status** | Frozen inventory |
| **Owner** | BTE Architecture Board |

Every row below is Foundation-frozen unless marked *reserved / inactive*.

---

## Knowledge Database V2

| Field | Value |
|-------|-------|
| **Purpose** | Canonical knowledge envelope, identity, checksum, dual-read with V1. |
| **Status** | Frozen |
| **Version** | Schema `2.0.0` |
| **Owner** | Knowledge Board |
| **Extension point** | New packages / new domains; not a new envelope generation without Foundation major. |
| **Reference** | `knowledge/docs/architecture/KNOWLEDGE_DATABASE_V2.md` |

---

## Knowledge Generator

| Field | Value |
|-------|-------|
| **Purpose** | Deterministic authoring of Knowledge Packages from profiles and templates. |
| **Status** | Frozen |
| **Version** | `1.0.0` |
| **Owner** | Knowledge Board |
| **Extension point** | New profiles and templates; Generator identity stays 1.0.0 until Foundation minor/major. |
| **Reference** | `knowledge/docs/architecture/KNOWLEDGE_PACKAGE_GENERATOR.md` |

---

## Knowledge Package Specification

| Field | Value |
|-------|-------|
| **Purpose** | Package identity, SemVer, lifecycle, PVP profiles, two-pass checksum, immutability. |
| **Status** | Frozen |
| **Version** | `1.0.0` |
| **Owner** | Knowledge Board |
| **Extension point** | New `package_id` artifacts; additive optional fields only via Foundation minor. |
| **Reference** | `knowledge/docs/architecture/KNOWLEDGE_PACKAGE_SPECIFICATION.md` |

---

## Knowledge Taxonomy

| Field | Value |
|-------|-------|
| **Purpose** | Stable domain → category → package → record hierarchy. |
| **Status** | Frozen |
| **Version** | `1.0.0` |
| **Owner** | Knowledge Board |
| **Extension point** | Reserved domains (Feng Shui / Qi Men / I Ching) as new packages, not renamed ids. |
| **Reference** | `knowledge/docs/architecture/KNOWLEDGE_TAXONOMY_ONTOLOGY.md` |

---

## Knowledge Ontology

| Field | Value |
|-------|-------|
| **Purpose** | Semantic types, relations, and multilingual axes for knowledge objects. |
| **Status** | Frozen |
| **Version** | `1.0.0` |
| **Owner** | Knowledge Board |
| **Extension point** | New relation types as additive ontology records; no rewrite of frozen types. |
| **Reference** | `knowledge/docs/architecture/KNOWLEDGE_TAXONOMY_ONTOLOGY.md` |

---

## Rule Engine

| Field | Value |
|-------|-------|
| **Purpose** | Evaluate rules from the Rule Database / package records. Does not own pipeline order. |
| **Status** | Frozen (public contract relative to Foundation) |
| **Version** | Platform Rule Engine as of F-1 freeze |
| **Owner** | Engine owner — Rule |
| **Extension point** | New rule records in new packages; no in-engine hard-coded rule trees. |

---

## Analysis Engine

| Field | Value |
|-------|-------|
| **Purpose** | Orchestrate Analysis Knowledge stages; publish Canonical Analysis Result. Does not decide Useful God. |
| **Status** | Frozen orchestration |
| **Version** | AX-1 pipeline `1.0.0`; AX-2 canonical `2.0.0` |
| **Owner** | Engine owner — Analysis |
| **Extension point** | New integration stages via registry + Foundation version bump; new analytical packages. |

---

## Canonical Analysis Pipeline

| Field | Value |
|-------|-------|
| **Purpose** | Deterministic Analysis Knowledge flow Calendar → … → Useful God Foundation signal. |
| **Status** | Frozen |
| **Version** | `2.0.0` (`canonical_analysis_pipeline`) |
| **Owner** | Architecture Board |
| **Extension point** | Reserved Luck / Interpretation / Report stages remain inactive until Phase IV–VI + catalog update. |
| **Reference** | `engines/analysis_engine/documentation/ANALYSIS_PIPELINE_V2.md` |

Active order:

```
Calendar → Four Pillars → Seasonal → Strength → Temperature
  → Pattern → Pattern Evaluation → Useful God → Analysis Result
```

---

## Decision Engine

| Field | Value |
|-------|-------|
| **Purpose** | Orchestrate Decision Packages into a Canonical Decision Result. Does not recompute analysis. |
| **Status** | Frozen |
| **Version** | `1.0.0` |
| **Owner** | Engine owner — Decision |
| **Extension point** | New decision packages and reserved luck/annual/monthly/interpretation stages. |

---

## Canonical Decision Pipeline

| Field | Value |
|-------|-------|
| **Purpose** | Deterministic Decision flow Foundation → Priority → Override. |
| **Status** | Frozen |
| **Version** | `1.0.0` (`canonical_decision_pipeline`) |
| **Owner** | Architecture Board |
| **Extension point** | Reserved Luck Cycle / Annual / Monthly / Interpretation stages (inactive). |
| **Reference** | `engines/decision_engine/documentation/DECISION_PIPELINE.md` |

---

## Package Contracts

| Field | Value |
|-------|-------|
| **Purpose** | Declared published inputs/outputs per package (`assets/published_*.json`). |
| **Status** | Frozen per sealed package version |
| **Version** | Bound to each `package_version` |
| **Owner** | Knowledge Board |
| **Extension point** | New fields on new package versions; never rename sealed fields. |

Sealed Foundation packages:

| package_id | version | checksum prefix |
|------------|---------|-----------------|
| `bz_01` Strength Core | 1.2.0 | `74fd4ac8…` |
| `bz_02` Seasonal Core | 1.0.0 | `f394ba18…` |
| `bz_03` Temperature Core | 1.0.0 | `a2e4826b…` |
| `bz_04` Pattern Core | 1.0.0 | `24911267…` |
| `bz_05` Pattern Evaluation | 1.0.0 | `c4fa911d…` |
| `bz_06` Useful God Foundation | 1.0.0 | `78a6f7c8…` |
| `bz_07` Useful God Priority | 1.0.0 | `0bd55841…` |
| `bz_08` Useful God Override | 1.0.0 | `ce73017c…` |

---

## Analysis Contracts

| Field | Value |
|-------|-------|
| **Purpose** | Canonical Analysis Result and stage publication contracts. |
| **Status** | Frozen |
| **Version** | AX-2 `2.0.0` |
| **Owner** | Architecture Board |
| **Extension point** | New optional published outputs from new analytical packages. |

---

## Decision Contracts

| Field | Value |
|-------|-------|
| **Purpose** | Canonical Decision Result: `final_*`, traces, audit. |
| **Status** | Frozen |
| **Version** | AX-3 `1.0.0` |
| **Owner** | Architecture Board |
| **Extension point** | New decision layers publish new names; do not overwrite `final_useful_god` meaning. |

---

## Stage Registry

| Field | Value |
|-------|-------|
| **Purpose** | Named stages, dependency edges, active vs reserved. |
| **Status** | Frozen for AX-2 and AX-3 registries |
| **Version** | Analysis registry AX-2; Decision registry `1.0.0` |
| **Owner** | Architecture Board |
| **Extension point** | Additive reserved → active only via Foundation version + approval. |

---

## Execution Trace

| Field | Value |
|-------|-------|
| **Purpose** | Append-only Analysis execution history (stages, publications, diagnostics). |
| **Status** | Frozen |
| **Version** | AX-2 `2.0.0` |
| **Owner** | Engine owner — Analysis |
| **Extension point** | New step names for new stages; existing step names immutable. |

---

## Decision Trace

| Field | Value |
|-------|-------|
| **Purpose** | Append-only Decision history: candidate generation, priority, conflict, override, final publication. |
| **Status** | Frozen |
| **Version** | AX-3 `1.0.0` |
| **Owner** | Engine owner — Decision |
| **Extension point** | New TRACE_STEPS for future reserved stages. |

---

## Diagnostics

| Field | Value |
|-------|-------|
| **Purpose** | Structured, non-throwing public diagnostics on pipeline `run()`. |
| **Status** | Frozen code families already issued |
| **Version** | Analysis + Decision diagnostic sets as of F-1 |
| **Owner** | Architecture Board |
| **Extension point** | New codes for new engines/packages; do not reuse codes with new meanings. |

---

## Validation Framework

| Field | Value |
|-------|-------|
| **Purpose** | KD-4 authoring/validation stages and PVP admission (MINIMAL / STANDARD / RELEASE). |
| **Status** | Frozen |
| **Version** | KD-4 `1.0.0` |
| **Owner** | Knowledge Board |
| **Extension point** | New package-local tests; no lowering of RELEASE gates. |
| **Reference** | `knowledge/docs/architecture/KNOWLEDGE_AUTHORING_VALIDATION_PIPELINE.md` |

---

## Evidence Framework

| Field | Value |
|-------|-------|
| **Purpose** | Evidence bundles bound to knowledge records (KX-1B pattern). |
| **Status** | Frozen |
| **Version** | `1.0.0` |
| **Owner** | Knowledge Board |
| **Extension point** | New bundles in new packages; same identity rules. |

---

## Reasoning Framework

| Field | Value |
|-------|-------|
| **Purpose** | Deterministic reasoning chains (RC-*) bound to published results. |
| **Status** | Frozen |
| **Version** | `1.0.0` |
| **Owner** | Knowledge Board |
| **Extension point** | New chain ids in new packages; do not reuse RC identifiers. |
| **Reference** | `knowledge/docs/architecture/KNOWLEDGE_REASONING_FRAMEWORK.md` |

---

## Package Generator

| Field | Value |
|-------|-------|
| **Purpose** | Same as Knowledge Generator v1.0 — production generator surface for sealed packages. |
| **Status** | Frozen |
| **Version** | `1.0.0` |
| **Owner** | Knowledge Board |
| **Extension point** | New generator profiles (`package_profile.schema.json` additive fields only via approved schema minor). |

---

## Supporting frozen documentation (not separately versioned)

| Component | Path |
|-----------|------|
| Analysis dependency map | `knowledge/docs/architecture/ANALYSIS_DEPENDENCY_MAP.md` |
| Knowledge architecture | `knowledge/docs/architecture/KNOWLEDGE_ARCHITECTURE.md` |
| Versioning policy (knowledge) | `knowledge/docs/standards/VERSIONING_POLICY.md` |

These documents remain in force. F-1 freeze docs govern them; F-1 does not rewrite them.
