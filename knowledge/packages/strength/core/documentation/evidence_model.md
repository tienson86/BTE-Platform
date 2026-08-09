# Strength Core — Evidence Model

| Field | Value |
|-------|-------|
| **Document** | evidence_model |
| **Package** | `bz_01_strength_core` |
| **Evidence version** | 1.0.0 |
| **Package version** | 1.1.0 |
| **Sprint** | KX-1B |
| **Status** | Canonical |

This document is the canonical Evidence Layer specification for Strength Core and the gold-standard pattern for later packages (Seasonal, Pattern, Temperature, Combination, Shen Sha, …).

---

## 1. Philosophy

A rule without evidence is an instruction, not knowledge.

The Evidence Layer makes every analytical rule:

- **explainable** — a reader can see why it exists and when it applies
- **traceable** — origin, version, and review status are explicit
- **reviewable** — examples, conflicts, and confidence are inspectable
- **reusable** — future interpretation, reports, citations, and AI assistants consume the same deterministic text

Evidence does **not** change match logic. Rule conditions and weights remain in `rules/`. Evidence lives beside them.

Principles:

1. One Evidence Bundle per rule id.
2. Explanations are deterministic (same rule → same text).
3. No engine or implementation details in explanations.
4. No copyrighted source quotations — titles, authors, editions, and notes only.
5. Identifiers stay language-neutral; explanation text may be localized later (`language` field).
6. Related-rule links are acyclic unless an exclusive group conflict is explicitly symmetric.

---

## 2. Evidence structure

Each rule has an **Evidence Bundle**:

| Field | Required | Meaning |
|-------|----------|---------|
| `rule_id` | yes | Canonical `SKC-*` id |
| `explanation` | yes | Why / when / when-not (+ summary) |
| `rationale` | yes | Knowledge rationale (not code) |
| `confidence_level` | yes | `experimental` \| `low` \| `medium` \| `high` \| `canonical` |
| `confidence_reason` | yes | Why that level was assigned |
| `references` | yes | Structured source metadata ids |
| `positive_examples` | yes | ≥1 activating case |
| `negative_examples` | yes | ≥1 non-activating case |
| `boundary_cases` | optional | Edge of the predicate |
| `related_rules` | yes | Directed `SKC-*` links (may be empty) |
| `conflicting_rules` | yes | Exclusive / opposing `SKC-*` (may be empty) |
| `traceability` | yes | Package, versions, author, review |
| `reviewer_notes` | optional | Review comments |

Canonical files: `evidence/bundles/SKC-XXXXXX.json`.

Browse indexes (same content, grouped):

```
evidence/explanations/
evidence/positive_examples/
evidence/negative_examples/
evidence/boundary_cases/
evidence/related_rules/
evidence/conflicting_rules/
evidence/references/
evidence/confidence/
evidence/traceability/
```

---

## 3. Explanation strategy

Every explanation has four deterministic parts:

| Part | Question |
|------|----------|
| `why` | Why does this knowledge exist in strength evaluation? |
| `when` | When does the rule apply? |
| `when_not` | When must it not apply? |
| `summary` | One short reader-facing paragraph |

Rules:

- Describe chart meaning, not Python/CSV loaders.
- Do not mention engines, matchers, or APIs.
- Do not invent classical citations.
- Keep `language` = `vi` for this package; future `en` / `zh-Hans` packs share the same `rule_id`.

---

## 4. Confidence strategy

| Level | Meaning | Typical use here |
|-------|---------|------------------|
| `canonical` | Locked BTE traditional table / threshold | Month-status weights, root levels, 0.65/0.35 bands, baseline 50 |
| `high` | Stable traditional mapping used across BTE | 旺相休囚死 by season, month command branch, core thập thần ± |
| `medium` | Sound but context-sensitive | Seat-root extras, false-strong/weak, hidden residual, combinations |
| `low` | Advisory / weak signal | Zero-weight hygiene, distant year-stem support |
| `experimental` | Not yet endorsed for official scoring | Reserved; unused in KX-1B |

Confidence is **not** a probability from the engine. It is a knowledge-governance label for reviewers and future AI.

---

## 5. Traceability strategy

Every bundle records:

- `originating_package` = `bz_01_strength_core`
- `package_version` = current package SemVer
- `author`
- `review_status`
- `evidence_version`
- `last_reviewed`

Rule bytes (conditions/results) are not copied into traceability. Evidence version may increment without changing rule version when only prose/examples change.

---

## 6. Relationship strategy

- `related_rules` are **directed** see-also links, sorted ascending, **no cycles**.
- `conflicting_rules` list exclusive-group peers. Mutual conflict inside an exclusive group is **explicitly justified** (only one member may apply).
- IDs must exist in this package. No invented relationships.

---

## 7. Future AI usage

AI-assisted authoring and report generation SHOULD:

1. Read the Evidence Bundle, not invent a new why/when.
2. Cite `references[]` metadata only — never quote copyrighted books.
3. Surface `confidence_level` to the consultant UI.
4. Use positive/negative/boundary examples as few-shot checks, not as Golden Dataset expected output.
5. Propose new evidence as `draft`; humans still own Domain Review (KD-4).

This layer is the contract between knowledge authors and future explanation / citation / confidence-scoring tools.

---

## 8. Validation

See `evidence/validation/EVIDENCE_VALIDATION.md`. Specification only — no runtime validator in this sprint.
