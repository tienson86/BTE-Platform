# Evidence Standard — V1.0

| Field | Value |
|-------|-------|
| Document | EVIDENCE_STANDARD |
| Standard | Knowledge QA V1.0 |

---

# 1. Purpose

Knowledge **must never require facts not published**.

The composer must not invent causes, luck, or pattern to make a claim true.

---

# 2. Frozen evidence states

| State | QA rule |
|-------|---------|
| **MISSING** | Unit must not narrate that dimension |
| **INACTIVE** | Not same as MISSING; unit must not treat as available |
| **AVAILABLE** | Unit may use if `required_facts` satisfied |
| **PARTIAL** | Unit may use only if `required_evidence` allows partial |

**Absence of evidence is not negative evidence.**

---

# 3. Rules

| Rule | Consequence |
|------|-------------|
| Claim implies drain cause | `drain` fact must be AVAILABLE or limitation gates |
| Claim implies season polarity | `season_support` or equivalent must be published |
| CLASS_ONLY schema | Claim must not need unpublished atomic causes |
| Luck interaction | Requires `luck_interaction` published — not inferred |
| Limitation vs schema | Limitation documents gap → REVIEW until schema aligned |

---

# 4. Scoring (Evidence Compatibility)

| Score | Condition |
|-------|-----------|
| 10 | All implied facts in `required_facts` and published |
| 7 | Limitation explicitly gates unpublished fact |
| 5 | CLASS_ONLY but claim needs causes |
| 3 | Requires unpublished dimension |
| 0 | Narrates missing data as present |

---

# 5. PACK-01 examples

| Unit | Issue |
|------|-------|
| CAUS-0002 vs CAUS-0003 | Season agree/disagree — polarity not in fact key |
| CAUS-0010 | Drain mild/heavy — severity not in published keys |
| CAUS-0020–0024 | CLASS_ONLY cluster passes gate without atomic facts |
| LUCK units | Require luck shell + interaction when claiming timing |

Detail: [QA_EXAMPLES.md](QA_EXAMPLES.md).

---

END
