# Knowledge Authoring & Validation Pipeline

| Field | Value |
|-------|-------|
| **Document** | KNOWLEDGE_AUTHORING_VALIDATION_PIPELINE |
| **Sprint** | KD-4 |
| **Version** | 1.0.0 |
| **Status** | Canonical process reference |
| **Scope** | Process, specifications, governance — no runtime |

Canonical files: `knowledge/authoring/`

---

## 1. Authoring philosophy

Knowledge is authored as KD-3 packages, honestly sourced, deterministically validated, and released as immutable units. Parallel drafts are allowed; official publication is gated. Existing Rule Database and KR guides remain valid; new official packages MUST use this pipeline.

## 2. Validation philosophy

Nine ordered stages: schema → metadata → dependency → reference → integrity → compatibility → quality → golden dataset → release. Fail closed. Golden/snapshot/expected files are read-only. No validators are executed in KD-4.

## 3. Review philosophy

Internal completeness → Technical Reviewer → Domain Reviewer. Separation of duties: authors do not sole-approve official release. AI-assisted drafts stay `draft` until human gates pass.

## 4. Release philosophy

Release candidate + `PVP-RELEASE` + checksum + notes + compatibility + publication readiness. Released bytes never change.

## 5. Governance model

Roles: Knowledge Author, Technical Reviewer, Domain Reviewer, Release Manager.  
Gates: submit, internal, technical, knowledge, release, deprecate, archive.  
Aligned with `knowledge/governance/ROLE_DEFINITIONS.md` without modifying that module.

## 6. Quality

Rules and metrics yield Bronze / Silver / Gold / Platinum. Minimum for release candidate: Bronze. Default official target: Silver.

## 7. Compatibility

No engine, API, contract, Rule Database, or existing package content changes. Dual-read V1 remains. Future Feng Shui / Qi Men / I Ching packages use the same pipeline with different `package_type` / `domain_id`.

## 8. Related

- `knowledge/authoring/authoring_pipeline.md`
- `knowledge/package_spec/PACKAGE_SPECIFICATION.md`
- `knowledge/docs/architecture/KNOWLEDGE_DATABASE_V2.md`
- `knowledge/docs/architecture/KNOWLEDGE_TAXONOMY_ONTOLOGY.md`
- `knowledge/docs/architecture/KNOWLEDGE_PACKAGE_SPECIFICATION.md`
