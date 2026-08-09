# AI Generation Specification

| Field | Value |
|-------|-------|
| **Generator version** | 1.0.0 |
| **Status** | Canonical |
| **Runtime** | None — policy only |

This document tells AI agents how to generate Knowledge Packages from Generator v1.0. It does not implement a runner.

---

## 1. Allowed generation scope

AI MAY:

1. Read this Generator, KD-1→KD-4, KX-1B/KX-1C, taxonomy, ontology.
2. Instantiate type profiles into instance profiles (new `package_id` only).
3. Emit **draft** skeletons from `generation_templates/`.
4. Fill rule / evidence / reasoning / example / documentation templates from a declared profile and cited canon.
5. Suggest reserved prefixes and zero-padded ids.
6. Produce package-local tests that do not import engines.
7. Record `generator_version`, `profile_id`, and session/author in metadata.

Status ceiling: **`draft`** (GC-AI-CEILING).

---

## 2. Prohibited behaviors

AI MUST NOT:

| Ban | Reason |
|-----|--------|
| Modify Rule / Analysis / Interpretation / Report engines | Architecture boundary |
| Modify API or contracts | Compatibility |
| Modify existing released packages (including Strength Core) | Immutability |
| Create new analytical theory or unpublished schools | GC-NO-NEW-THEORY |
| Hard-code business rules in Python `if/elif` | Database-first |
| Edit Golden Dataset, snapshots, expected engine outputs | Test integrity |
| Skip pipeline stages or KD-4 reviews | Governance |
| Set `status` to `review`, `validated`, or `released` | Human gates |
| Seal checksums as released | Release Manager only |
| Change taxonomy / ontology / package_spec schemas to “make generation easier” | Foundation freeze |
| Collide with reserved ids (`SKC-*`, `bz_01_strength_core`, V1 prefixes without reservation) | GC-UNIQUE-IDS |
| Claim a quality gate that is not measured | GV-QUALITY-CLAIM |
| Implement a runtime scorer or validator in this folder | Spec only |

---

## 3. Traceability requirements

Every generated artifact MUST record, where the schema allows:

| Field | Location |
|-------|----------|
| `generator_id` | metadata / manifest |
| `generator_version` | `1.0.0` |
| `profile_id` | instance profile used |
| `pipeline_id` | `GEN-PIPELINE-V1` |
| `author` / `created_by` | human owner; AI session may be noted |
| `created_at` | ISO-8601 |
| rule/evidence/reasoning ids | stable, prefixed |
| reasoning traces | activated rules, evidence, package_version |

QM-GEN-TRACE = 1.0 is required from Bronze upward.

---

## 4. Review requirements

| Review | Actor | AI role |
|--------|-------|---------|
| Accept AI draft | Knowledge Author (human) | Submitter only |
| Internal completeness | Internal reviewer | None |
| Technical | Technical Reviewer | None |
| Domain / academic | Domain Reviewer | None |

Technical pass does not waive Domain Review. Domain pass does not waive technical failures.

---

## 5. Human approval requirements

Official release requires:

1. Author ≠ sole Domain Reviewer
2. Author ≠ sole Release Manager
3. `PVP-RELEASE` conceptual pass
4. Quality target met (minimum Bronze for RC; declared target otherwise)
5. Release Manager + Domain Reviewer recorded on `RELEASE.json`

No AI session may approve its own release.

---

## 6. Prompt / session hygiene (future runner)

When a runner exists, each run SHOULD store:

- profile snapshot (resolved inheritance)
- template versions (`generator_version`)
- prompt id / model id (optional, non-secret)
- file list emitted (locale `C`)

Secrets (API keys, credentials) MUST NOT be written into packages.

---

## 7. Future visual builder

A visual package builder MUST emit the same profiles, templates, and metadata as an AI runner. UI convenience must not bypass GC-* or KD-4 gates.
