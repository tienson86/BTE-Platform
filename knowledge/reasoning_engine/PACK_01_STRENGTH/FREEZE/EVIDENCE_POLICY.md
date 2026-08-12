# Evidence Policy — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | EVIDENCE_POLICY |
| Status | FROZEN |

---

# 1. Frozen states

Every fact key on a unit is evaluated into exactly one state:

| State | Meaning |
|-------|---------|
| `AVAILABLE` | Published, usable, polarity known. Includes **active** drain, present season, etc. |
| `PARTIAL` | Published but incomplete (e.g. root AVAILABLE as 1 chi while hidden stems not exposed). The **dimension** may still be AVAILABLE; a *deeper* claim may be PARTIAL. |
| `INSUFFICIENT` | Published but not enough to support **this unit’s** claim (e.g. special present but unit requires `special_override`). |
| `MISSING` | The engine did not publish the field at all (e.g. luck interaction absent from payload). |
| `NOT_APPLICABLE` | Dimension does not apply to this pack/case contract. |
| `INACTIVE` | The field **is published** and states that the factor is off / zero / null-as-none (CASE-0001 drain). |

`INACTIVE` is a first-class state.

---

# 2. Drain inactive ≠ missing

CASE-0001: `drain_score = 0.0`, `drain_type = null`.

That is **`INACTIVE`**, not `MISSING`.

| | INACTIVE | MISSING |
|--|----------|---------|
| Data | Published: there is no active drain | Not published: unknown whether drain exists |
| Drain-leak unit | FAIL — `REJECTED_FACT_INACTIVE` | FAIL — `REJECTED_MISSING_EVIDENCE` |
| “Luck has no effect” | Illegal if luck MISSING | Illegal — absence is not negative evidence |
| Why sentence “effort leaks” | Forbidden | Forbidden |
| Why sentence “drain not active” | Allowed only if a catalog unit exists for inactivity (PACK-01 Customer Mode has **no** such unit in the golden plan) | Forbidden (would invent) |

Never code drain inactive as `REJECTED_MISSING_EVIDENCE`.

---

# 3. Gate mapping

| Unit need | Fact state | Gate |
|-----------|------------|------|
| required AVAILABLE | AVAILABLE | pass |
| required AVAILABLE | INACTIVE | fail `REJECTED_FACT_INACTIVE` (unless unit is explicitly an inactivity unit) |
| required AVAILABLE | MISSING | fail `REJECTED_MISSING_EVIDENCE` |
| required AVAILABLE | INSUFFICIENT | fail `REJECTED_INSUFFICIENT_EVIDENCE` |
| required AVAILABLE | PARTIAL | `partially_supported` — not firm Customer conclusion |
| required AVAILABLE | NOT_APPLICABLE | fail `REJECTED_NOT_APPLICABLE` |
| optional | any | no fail; salience/relevance only |

---

# 4. Luck

Luck not in payload → `MISSING` → luck **units** rejected; luck **section** `INSUFFICIENT_DATA_LUCK`.

Do not infer “luck has no effect”.

---

# 5. Hidden stems

`NOT_EXPOSED` → `MISSING` for `hidden_stems`.

Does not fail `root` if `root_level` is published (`AVAILABLE`, and `root_thin` if 1 chi).

---

END
