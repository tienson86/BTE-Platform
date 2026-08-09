# Generation Constraints

| Field | Value |
|-------|-------|
| **Generator version** | 1.0.0 |
| **Status** | Canonical |
| **Runtime** | None |

Every generation run MUST satisfy these constraints. Violation blocks the active stage.

---

## Constraint catalog

| Id | Name | Rule |
|----|------|------|
| GC-DETERMINISTIC | Deterministic generation | Same inputs ⇒ same outputs. Locale `C` sort for ids, paths, checksum scope. No random ids. |
| GC-UNIQUE-IDS | Unique identifiers | `package_id`, rule ids, evidence ids, reasoning ids unique within the Knowledge Database generation. Prefixes reserved before emit. |
| GC-IMMUTABLE-RELEASE | Immutable released package | `status=released` bytes never change. Corrections ⇒ new `package_version`. |
| GC-TAXONOMY | Taxonomy compliance | `domain.domain_id` exists in `knowledge/taxonomy/domains.json`. Classifications from taxonomy only. |
| GC-ONTOLOGY | Ontology compliance | Declared `ONT-*` concepts exist in KD-2 ontology sources. |
| GC-PACKAGE-COMPLETE | Package completeness | KD-3 required files present for type + lifecycle state. |
| GC-EVIDENCE-COMPLETE | Evidence completeness | If `evidence_required`, every production rule has a bundle with explanation, ± examples, confidence, traceability. |
| GC-REASONING-COMPLETE | Reasoning completeness | If `reasoning_required`, every primary conclusion class has a chain Observation→…→Final citing existing rule ids. |
| GC-NO-NEW-THEORY | No unpublished theory | Generator fills declared templates; it does not invent schools, gods, or scoring systems absent from profile + canon. |
| GC-NO-ENGINE | No engine mutation | Must not modify Rule / Analysis / Interpretation / Report engines, API, or contracts. |
| GC-NO-EXISTING-PKG | No existing package mutation | Must not edit released packages, including Strength Core. |
| GC-NO-GOLDEN | Golden Dataset integrity | Must not create or edit Golden Dataset, snapshots, or expected engine outputs. |
| GC-INHERIT-ACYCLIC | Acyclic profile inheritance | Profile `inherits` graph has no cycles. |
| GC-DEP-ACYCLIC | Acyclic package dependencies | Required package dependencies have no cycles. |
| GC-SCHEMA | Schema compliance | Emitted JSON validates against the referenced KD-1/KD-3/KX-1C schemas after placeholder substitution. |
| GC-NAMING | Naming compliance | `package_id`, files, rule ids follow KD-2 / KD-3 naming. |
| GC-MULTILINGUAL | Language honesty | `language` / `languages` match object payloads. Mixed packs use `mul` only when truly mixed. |
| GC-TRACE | Traceability | Metadata records `generator_version`, `profile_id`, author, timestamps. Reasoning traces record package version. |
| GC-PVP | Validation profile honesty | Declared PVP matches lifecycle; release requires `PVP-RELEASE`. |
| GC-QUALITY | Quality target honesty | Declared `quality_target` metrics met or package must not claim that gate. |
| GC-SCALE | Scale readiness | Id formats and folder layout must remain valid at 100,000+ records (zero-padded numeric suffixes, no per-file global lock). |
| GC-INDEPENDENCE | Independent releases | A package MUST be releasable without regenerating unrelated packages. |
| GC-PLACEHOLDER | Placeholder resolution | No `{{…}}` tokens remain in files when status ≥ `review`. |
| GC-CHECKSUM | Checksum discipline | SHA-256 two-pass placeholder rule (KD-3). Null checksum only before `released`. |
| GC-AI-CEILING | AI status ceiling | AI-emitted artifacts MUST stay `draft` until human acceptance. |

---

## Enforcement (specification)

Future tooling evaluates constraints in id order (locale `C`). Fail closed.

This sprint defines the catalog only. No runtime enforcer.
