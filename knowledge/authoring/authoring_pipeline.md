# Knowledge Authoring Pipeline

**Status:** Canonical  
**Sprint:** KD-4  
**Scope:** Process and governance only — no runtime implementation

---

## 1. Purpose

Define how every Knowledge Package is created, validated, reviewed, approved, and released before it may join the official Knowledge Database.

This is the canonical process for all future knowledge development, including multilingual packages, multiple BaZi schools, and future Feng Shui / Qi Men / I Ching packages.

---

## 2. Workflow states

```text
idea
  → draft
  → internal_review
  → technical_validation
  → knowledge_review
  → release_candidate
  → released
  → deprecated
  → archived
```

Machine ids and KD-3 status mapping: `workflow/states.json`.  
Transition rules: `workflow/transitions.json`.  
Approval gates: `workflow/approvals.json`.

| Workflow state | KD-3 `PACKAGE.json` status | Editable |
|----------------|----------------------------|----------|
| `idea` | none (or workspace only) | yes |
| `draft` | `draft` | yes |
| `internal_review` | `review` | limited |
| `technical_validation` | `review` | no content (fix-forward via reject) |
| `knowledge_review` | `review` | no content (fix-forward via reject) |
| `release_candidate` | `validated` | no (frozen candidate) |
| `released` | `released` | **immutable** |
| `deprecated` | `deprecated` | immutable artifact |
| `archived` | `archived` | immutable artifact |

Fine-grained workflow states live in authoring records / future tooling. The sealed package still uses KD-3 status values only.

---

## 3. Transition summary

| From | To | Actor | Gate |
|------|----|-------|------|
| idea | draft | Knowledge Author | package skeleton created |
| draft | internal_review | Knowledge Author | draft checklist + `PVP-MINIMAL` |
| internal_review | draft | Internal reviewer | reject with findings |
| internal_review | technical_validation | Internal reviewer | internal review approved |
| technical_validation | draft | Technical Reviewer | technical fail |
| technical_validation | knowledge_review | Technical Reviewer | `PVP-STANDARD` minus domain quality pass |
| knowledge_review | draft | Domain Reviewer | domain reject |
| knowledge_review | release_candidate | Domain Reviewer | knowledge review approved + quality floor |
| release_candidate | knowledge_review | Release Manager | pre-release regression |
| release_candidate | released | Release Manager | `PVP-RELEASE` + release checklist |
| released | deprecated | Release Manager + Domain Reviewer | successor or rationale |
| deprecated | archived | Release Manager | consumers migrated or waiver |

No skips. No `released` → `draft`.

---

## 4. Governance model

### Roles

| Role | Responsibility |
|------|----------------|
| Knowledge Author | Draft packages and objects; complete draft checklist; cannot sole-approve release |
| Technical Reviewer | Schema, ids, dependencies, integrity, compatibility, determinism |
| Domain Reviewer | Academic/school meaning, references, interpretation quality (maps to Academic Reviewer in Foundation governance) |
| Release Manager | Release pipeline, checksum, notes, index publication, immutability |

Aligned with `knowledge/governance/ROLE_DEFINITIONS.md`. Domain Reviewer is the package-pipeline name for academic/domain accountability.

### Separation of duties

1. Author MUST NOT be the sole Domain Reviewer or Release Manager for official release of their own package.
2. Technical pass does not waive Domain Review.
3. Domain pass does not waive Technical Validation failures.
4. Release Manager MUST NOT publish if any required validation stage is `fail`.

### Parallel authoring

- Many draft packages may proceed independently.
- Shared identifier ranges MUST be reserved to avoid collisions (rule prefixes, `KR-*`, `package_id`).
- Merge/publication order is deterministic via package index sort (`package_id`, `package_version`, locale `C`).

### Future tooling / AI

- Tools MAY generate drafts from templates.
- Tools MUST emit the same files a human author would.
- Tools MUST NOT auto-transition past `draft` without recorded human approvals.
- AI output is `draft` until Technical + Domain gates pass.

---

## 5. Validation and quality hooks

After `internal_review`, run the sequence in `validation/VALIDATION_PIPELINE.md`.

Quality floor by target level (`quality/quality_levels.json`):

| Intended official level | Minimum before `release_candidate` |
|-------------------------|--------------------------------------|
| Bronze | all required metadata + identifiers valid |
| Silver | + references and documentation complete |
| Gold | + examples/tests + dependency hygiene |
| Platinum | + Golden Dataset stage pass + zero release warnings |

---

## 6. Release hook

`release_candidate` → `released` follows `release/RELEASE_PIPELINE.md` and KD-3 `knowledge/package_spec/release_process.md`.

---

## 7. Compatibility

- Do not modify existing Rule Database packages.
- Do not modify engines or API.
- V1 packages remain authoritative until a migration sprint.
- New official knowledge MUST enter through this pipeline.
