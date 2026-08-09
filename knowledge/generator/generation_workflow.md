# Generation Workflow

| Field | Value |
|-------|-------|
| **Generator version** | 1.0.0 |
| **Aligns with** | KD-4 `knowledge/authoring/` |
| **Status** | Canonical |
| **Runtime** | None |

The Generator does not replace the Authoring Pipeline. It **feeds** it.

---

## 1. Dual state model

| Generator pipeline stage | KD-4 workflow state | KD-3 `PACKAGE.json` status |
|--------------------------|---------------------|----------------------------|
| profile | `idea` | none / workspace |
| package_skeleton → tests | `draft` | `draft` |
| validation (PVP-STANDARD) + documentation | `internal_review` → `technical_validation` → `knowledge_review` | `review` |
| release_candidate | `release_candidate` | `validated` |
| released_package | `released` | `released` |

Deprecation and archive remain KD-4-only. The Generator does not emit deprecated packages.

---

## 2. Actors

| Role | Generator rights |
|------|------------------|
| Knowledge Author | Create/edit profiles and drafts; cannot sole-release |
| AI agent | Same as Author, **ceiling `draft`** |
| Technical Reviewer | Schema, ids, deps, integrity, determinism, GV-* |
| Domain Reviewer | Meaning, references, evidence/reasoning honesty |
| Release Manager | RC freeze, checksum, publication, immutability |

Separation of duties (KD-4) is unchanged: Author MUST NOT be the sole Domain Reviewer or Release Manager for official release.

---

## 3. Transition rules

1. No skip of GEN-PIPELINE-V1 stages.
2. No skip of KD-4 workflow states for official packages.
3. Reject returns to `draft` (fix-forward). Never edit a `released` artifact in place.
4. AI-produced files remain `draft` until a human Author accepts them into the review queue.
5. Parallel instance profiles MAY proceed independently if `package_id` and `rule_id_prefix` are reserved (GC-UNIQUE-IDS).

---

## 4. Reservation

Before skeleton stage, record:

| Reserved | Example |
|----------|---------|
| `package_id` | `bz_02_seasonal_core` |
| `rule_id_prefix` | `SEA` or `SKC`-style unique prefix |
| Evidence ids | `EVD-<prefix>-*` if used |
| Reasoning ids | `RN-` / `RE-` / `RC-` / `RT-` / `RG-*` with package token |

Collisions with published Strength (`SKC-*`, `bz_01_strength_core`) are forbidden.

---

## 5. Human approval gates

| Gate | Required for |
|------|----------------|
| Author accept | AI draft → human draft |
| Internal review | Enter technical validation |
| Technical Reviewer | PVP-STANDARD integrity |
| Domain Reviewer | Knowledge meaning + quality_target |
| Release Manager + Domain Reviewer | `released` |

No gate may be performed solely by the generating AI session.

---

## 6. Relationship to existing Strength Core

Strength Core was authored before Generator v1.0. It remains the gold-standard analytical package.

- Do **not** regenerate or rewrite `knowledge/packages/strength/core/`.
- Use `examples/strength_profile.json` only as a retrospective instance profile for future similar packages.
- Future Strength *extensions* (new `package_id` / new version) MUST use this workflow.
