# 03 — Contracts

| Field | Value |
|-------|--------|
| Document | INT-02A Contracts |
| Version | 1.0.0 |
| Status | Canonical for INT-02A |
| Contract id | `bte.narrative.framework.v1` |

---

## 1. Public contract surface

Frozen Python: `narrative_framework_contract()`.

This is a schema freeze, not a runtime engine.

---

## 2. TopicNarrativeUnit

| Field | Description |
|-------|-------------|
| `topic_id` | One of the analytical topic ids |
| `source_path` | Read-only path into the engine / analysis payload |
| `blocks` | Ordered map of the five required blocks |
| `status` | `complete` / `partial` / `insufficient` |
| `evidence_refs` | Fact paths supporting published prose |
| `schema_version` | `1.0.0` |

Invariants:

1. `blocks` always contains all five slots in framework order.
2. No calculator fields. No UI fields.
3. `status` is derived from block availability, not from a new score.

---

## 3. NarrativeBlock

| Field | Description |
|-------|-------------|
| `slot` | `observation` \| `reasoning` \| `impact` \| `recommendation` \| `conclusion` |
| `section_id` | `sec-*` identifier |
| `title` | Canonical Vietnamese title |
| `sentences` | Ordered sentence records |
| `available` | True when at least one publishable sentence exists |
| `insufficient` | True when the block must show the empty outcome |

A block may be present and insufficient. Absence is forbidden.

---

## 4. NarrativeSentence

| Field | Description |
|-------|-------------|
| `sentence_id` | Stable `SEN-*` or explicit unpublished marker |
| `role` | Matches the parent block slot |
| `text` | Customer prose, or empty when insufficient |
| `source_path` | Engine / knowledge path |
| `owner` | `engine_result` \| `sentence_library` \| `narrative_framework` |

Ownership rules:

- `engine_result` owns values inside slots, never full customer essays.
- `sentence_library` owns templates.
- `narrative_framework` owns order, not wording.

---

## 5. TopicEvidencePack

Internal supporting model. Not a public delivery aggregate.

| Field | Description |
|-------|-------------|
| `topic_id` | Topic being narrated |
| `facts` | Read-only copies of published engine fields |
| `missing` | Declared unpublished fields |

The pack must not contain recalculated values.

---

## 6. Compatibility aliases

Existing consumers keep their names. Framework is the canonical slot.

| Framework slot | Workspace alias | Identity key |
|----------------|-----------------|--------------|
| `observation` | `observe` | `observation_id` |
| `reasoning` | `reason` | `reasoning_id` |
| `impact` | `impact` | via `section_keys` / `sec-impact` |
| `recommendation` | `advice` | `recommendation_id` |
| `conclusion` | Panel 10 | `conclusion_id` / `conclusion` |

INT-02A does not edit Identity or Workspace to close any missing `impact_id`.

That gap is recorded for a later identity/content sprint.

---

## 7. What this contract forbids

- Recalculating strength, pattern, useful god, elements, ten gods, shensha, luck, or temperature
- Authoring topic prose in Calendar / BaZi / UI
- Dropping a required block to shorten a card
- Replacing malformed canonical text with invented copy
- Using LLM output as the system of record

---

END
