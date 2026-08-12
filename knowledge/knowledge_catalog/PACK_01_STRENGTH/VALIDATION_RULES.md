# Validation Rules — PACK-01 Strength

| Field | Value |
|-------|-------|
| Document | VALIDATION_RULES |
| Pack | PACK_01_STRENGTH |
| Version | 1.0.0 |

---

# 1. Purpose

This document is how a Draft Knowledge Unit becomes **Validated**.

It is review, not runtime code.

No unit in this delivery has passed this gate yet.

---

# 2. Roles

| Role | Job |
|------|-----|
| Author | Normalize source → Draft unit |
| Knowledge Reviewer | Claim, So what, class gate, limitations, no new doctrine |
| Governance Reviewer | Schema, IDs, clusters, reason codes, mode flags |

Official Validated requires both reviewers.

---

# 3. Schema gate

Fail (stay Draft) if any:

- A §2 field is missing
- `knowledge_id` does not match `IK-STR-<TOPIC>-<NNNN>`
- `topic` / `purpose` / `domain` / `strength_class` not in the closed lists
- `duplicate_cluster` missing
- `status` not one of Draft / Validated / Frozen / Deprecated
- `source_document` not an exact PACK-01 Strength knowledge filename
- A reason code is not on the frozen Reason Codes list

---

# 4. Source gate

Fail if:

- The claim cannot be traced to the cited `source_document`
- The claim adds a new interpretation (Useful God, Pattern name, medical diagnosis, job destiny, guaranteed year)
- The claim is a dictionary definition
- Supporting points introduce a second independent claim

---

# 5. So-what gate

Fail if the claim could be deleted without changing a customer decision or a consultant warning.

Fail if the claim only restates the class name.

---

# 6. Evidence gate

Fail if:

- A CONTEXTUAL unit has empty `required_facts` (except documented class-agnostic edge governance)
- A luck unit does not require `luck_interaction`
- A drain-leak unit does not forbid `drain_inactive` or otherwise name drain evidence
- An example unit is `customer_mode = ALLOWED`

`INACTIVE` must not be treated as `MISSING`.

---

# 7. Safety gate

Fail if the unit:

- Promises returns, marriage, death, bankruptcy, or promotion
- Names diseases as destiny
- Sells a product
- Uses gender as a Strength class
- Ranks classes morally
- Gives absolute career/investment commands from Strength alone (`REJECTED_ADVICE_UNSAFE` if it slipped through)

---

# 8. Duplicate gate

Fail if two official (Validated) units overlap in claim and do not share a `duplicate_cluster`, unless both are `NONE` **and** the overlap is recorded as an open gap.

PACK-01 named clusters:

- `DUP-STR-FULL_TANK`
- `DUP-STR-ENDURANCE_AS_PROOF`
- `DUP-STR-CARRY_LOAD`
- `DUP-STR-BATTERY`
- `DUP-STR-C1_QUALIFIER`

Do not invent runtime clusters. New named clusters require catalog governance, not a silent authoring choice during production selection.

---

# 9. Conflict gate

Reviewer checks `conflicts_with`.

Declare. Do not resolve.

Fail if two units are true contradictions and neither lists the other, when both are intended as Customer headlines.

---

# 10. Mode gate

| Kind | customer_mode | validation_mode |
|------|---------------|-----------------|
| Normal consulting unit | ALLOWED | ALLOWED |
| Alternative-class meaning | ALLOWED only when that class is published | ALLOWED as runner-up with `REJECTED_ALTERNATIVE_CLASS_AS_PRIMARY` / `DEFERRED_TO_VALIDATION` |
| Teaching example | FORBIDDEN | ALLOWED |
| Luck content | ALLOWED only if luck published | ALLOWED to record `INSUFFICIENT_DATA_LUCK` |

---

# 11. Source bans that remain governance (not Customer units)

From the knowledge library, never validate a unit that says:

- Strong means the Day Master is strong
- Weak people fail
- Balanced people are average
- Very Strong is the best class
- Any Rule ID, score, or threshold
- Useful God element commands as Strength cause
- Gender, luck, or a single Ten God as the whole Strength story
- “mệnh xấu”
- Organ-by-organ folklore as medical fact

---

# 12. Review record

A Validated unit must have a review note (outside the unit schema, in catalog governance history) stating:

1. Reviewer names
2. Date
3. Source paragraph checked
4. Duplicate cluster checked
5. Pass / fail list from §3–§10

This delivery includes no review records. All units remain Draft.

---

END
