# 03 — Contracts

| Field | Value |
|-------|--------|
| Document | INT-03A Contracts |
| Version | 1.0.0 |
| Status | Canonical for INT-03A |
| Contract id | `bte.commercial.composer.v1` |

---

## 1. Public contract surface

Frozen Python: `commercial_composer_contract()`.

---

## 2. CommercialNarrativeUnit

| Field | Description |
|-------|-------------|
| `executive_summary` | Commercial section block |
| `overall_reading` | Commercial section block |
| `current_situation` | Commercial section block |
| `strengths` | Commercial section block |
| `risks` | Commercial section block |
| `key_recommendation` | Commercial section block |
| `conclusion` | Commercial section block |
| `status` | `complete` / `partial` / `insufficient` |
| `source_path` | `integrated_narrative` |
| `schema_version` | `1.0.0` |
| `evidence_refs` | Integrated source paths cited by published sentences |

Invariants:

1. All seven sections are always present, in framework order.
2. No calculator fields. No UI fields. No engine scores.
3. Every published sentence cites at least one Integrated block slot.

---

## 3. CommercialNarrativeBlock

| Field | Description |
|-------|-------------|
| `slot` | One of the seven commercial slots |
| `sentences` | Ordered commercial sentences |
| `available` | True when at least one customer sentence exists |
| `insufficient` | True when the empty outcome must show |

---

## 4. CommercialSentence

| Field | Description |
|-------|-------------|
| `text` | Customer prose copied or summarized from Integrated |
| `slot` | Parent commercial slot |
| `integrated_slots` | Integrated block names this sentence came from |
| `source_paths` | Integrated source paths |
| `topic_ids` | Integrated topic ids, when published |

A sentence with empty `integrated_slots` is not eligible.

---

## 5. Status

| Condition | Status |
|-----------|--------|
| All seven sections available | `complete` |
| Some sections insufficient | `partial` |
| Current Situation insufficient | `insufficient` |

Without a published current situation, the commercial reading is not responsible.

---

END
