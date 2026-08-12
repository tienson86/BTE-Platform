# Consistency Standard — V1.0

| Field | Value |
|-------|-------|
| Document | CONSISTENCY_STANDARD |
| Standard | Knowledge QA V1.0 |

---

# 1. Purpose

Align Knowledge with Reasoning, Narrative, and Customer Mode policy.

Inconsistency causes correct units to print wrong content.

---

# 2. Frozen alignment layers

| Layer | Consistency check |
|-------|-------------------|
| **Knowledge** | Claim matches class gate, topic, limitations |
| **Reasoning** | `required_facts`, `forbidden_conditions`, `duplicate_cluster`, `conflicts_with` |
| **Narrative** | `priority`, `narrative_weight`, section purpose, budget |
| **Customer Mode** | `customer_mode` ALLOWED/FORBIDDEN matches claim safety |

---

# 3. Rules

| Rule | Consequence |
|------|-------------|
| customer_mode ALLOWED + Validation-only claim | FAIL Consistency |
| limitation forbids Customer + ALLOWED flag | REVIEW minimum |
| golden plan pins unit + QA REVIEW on same | Hold until golden updated |
| MEANING class Strong + ADVANTAGE Weak gate | FAIL Professional Correctness |
| conflicts_with violated at selection | Reasoning bug — flag in QA if metadata missing |

---

# 4. Scoring

| Score | Condition |
|-------|-----------|
| 10 | Full alignment |
| 7 | Minor metadata drift |
| 5 | Limitation contradicts schema |
| 3 | Golden or mode conflict |
| 0 | Unsafe Customer leak |

---

# 5. PACK-01 golden alignment

Units referenced in CASE-0001 must not REVIEW on golden-critical paths without Reasoning sign-off:

- MEAN-0006, CAUS-0002, CAUS-0007, CAUS-0010, CAUS-0016
- ADV-0009, ADV-0013

Golden reference: `knowledge/reasoning_engine/PACK_01_STRENGTH/FREEZE/CASE_0001_GOLDEN_REFERENCE.md` (read-only for QA).

---

END
