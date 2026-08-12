# Catalog Schema — PACK-01 Strength

| Field | Value |
|-------|-------|
| Document | CATALOG_SCHEMA |
| Pack | PACK_01_STRENGTH |
| Version | 1.0.0 |
| Status | Frozen for this catalog (units remain Draft) |

---

# 1. Rule

Every Knowledge Unit uses **this schema**.

No extra fields.

No missing fields.

No exceptions.

If the source does not supply a value, the field is present and **empty**. Why it is empty is documented in §8 and, when the emptiness is a use-limit, in `limitations`.

---

# 2. Fields

| Field | Closed values / type | Meaning |
|-------|----------------------|---------|
| `knowledge_id` | `IK-STR-<TOPIC>-<NNNN>` | Stable identity. Never reused. |
| `title` | short text | Consultant label. Not a customer headline dump. |
| `pack` | `PACK_01_STRENGTH` | Owning pack. |
| `topic` | see §3 | Source chapter family. |
| `purpose` | see §4 | Narrative job. One per unit. |
| `domain` | see §5 | Life / core domain. |
| `strength_class` | `very_strong` `strong` `balanced` `weak` `very_weak` `all` `edge` | Class gate. |
| `customer_mode` | `ALLOWED` `FORBIDDEN` | May appear in Customer Mode. |
| `validation_mode` | `ALLOWED` `FORBIDDEN` | May appear in Validation Mode. |
| `required_facts` | list of fact keys, or empty | All must be in an allowed evidence state. |
| `optional_facts` | list of fact keys, or empty | If present, may raise salience. Absence does not fail the gate. |
| `forbidden_conditions` | list of condition keys, or empty | If any true → ineligible. |
| `required_evidence` | `CLASS_ONLY` `FULL` `PARTIAL_OK` | How strict the evidence gate is. |
| `claim` | one So-what statement | The selectable assertion. |
| `supporting_points` | list, or empty | Same claim only. No second claim. |
| `limitations` | list | When the unit must **not** be used. |
| `customer_value` | `LOW` `MEDIUM` `HIGH` `CRITICAL` | Usefulness to a paying customer. |
| `specificity` | `GENERIC` `CONTEXTUAL` `CASE_SPECIFIC` | How tightly bound to weather. |
| `priority` | `CORE` `HIGH` `NORMAL` `OPTIONAL` | Knowledge priority. Not Rule Priority. |
| `duplicate_cluster` | cluster id or `NONE` | Exactly one. |
| `conflicts_with` | list of `knowledge_id`, or empty | Declared only. |
| `reason_codes` | subset of frozen Reason Codes | Codes this unit may carry when kept, rejected, merged, or omitted. |
| `narrative_weight` | `CORE` `SUPPORTING` `DETAIL` `OPTIONAL` | Budget preference inside a section. |
| `version` | `1.0.0` | Unit version. |
| `status` | `Draft` `Validated` `Frozen` `Deprecated` | Authoring state. PACK-01 defaults to `Draft`. |
| `source_document` | filename | Exact source chapter. |

---

# 3. Topic

```text
meaning
causes
advantages
challenges
personality
career
wealth
marriage
health
luck
recommendation
edge_cases
examples
```

---

# 4. Purpose

```text
CONCLUSION
WHY
MEANING
ADVANTAGE
CHALLENGE
PERSONALITY
CAREER
WEALTH
MARRIAGE
HEALTH
LEARNING
LEADERSHIP
DECISION_MAKING
LUCK
RECOMMENDATION
WARNING
SUMMARY
EDGE_QUALIFIER
```

`examples` topic: purpose is filled (usually MEANING or EDGE_QUALIFIER as the vignette’s job) but Customer Mode is `FORBIDDEN`. Keep/reject code: `REJECTED_TEACHING_EXAMPLE`.

PACK-01 does not author standalone CONCLUSION or SUMMARY units. Those are Reasoning composition jobs. The fields stay in the closed list for later packs.

---

# 5. Domain

```text
strength_core
personality
career
wealth
marriage
health
learning
leadership
decision_making
luck
recommendation
```

---

# 6. Fact keys (PACK-01)

Reuse the published Strength fact keys. Do not invent new keys.

```text
classification
season
root
root_thin
root_deep
support
drain
drain_active
control
special
special_override
combination
luck_interaction
hidden_stems
```

Polarity (feeds vs empties) is not a new key. It is read from the published fact’s evidence. Units that need a polarity state it in `limitations`.

---

# 7. Forbidden condition keys (PACK-01)

```text
class_mismatch
root_thin
root_deep_required
drain_inactive
luck_missing
special_is_not_override
teaching_only
```

Empty `forbidden_conditions` means the source named no extra closed condition beyond class mismatch, which is always implied by `strength_class`.

---

# 8. Empty fields

| Field | When empty | Why |
|-------|------------|-----|
| `required_facts` | Shared bans / teaching notes only — not used on consulting units | Consulting units always name at least `classification` except where the unit is class-agnostic edge governance. PACK-01 consulting units do not leave this empty. |
| `optional_facts` | Source does not name a raising fact | Do not invent optional keys. |
| `forbidden_conditions` | Source names no extra closed condition | Class mismatch remains implied. |
| `supporting_points` | The claim is already atomic | Do not pad with restated claims. |
| `conflicts_with` | Source does not name a unit-to-unit contradiction | Fact-level conflicts (e.g. support vs control) are Reasoning conflicts, not invented knowledge conflicts. |

Never fill empty fields with placeholder prose.

---

# 9. Claim design

A claim must answer **So what?**

Forbidden as a claim:

- Dictionary definitions (“Strong means the Day Master is strong”)
- Repeated restatements of the same sentence
- Rule IDs, scores, thresholds
- Moral ranking of classes

One unit, one claim. Supporting points must belong to that claim.

---

# 10. Customer value — how assigned

| Value | Assign when |
|-------|-------------|
| `CRITICAL` | Identity-level standing, energy-protection for Very Weak, luck chapter that must not be invented, safety-adjacent pacing |
| `HIGH` | Changes a real decision: career load, money leak, marriage space, headline advantage/challenge, steering-wheel recommendation |
| `MEDIUM` | Helps recognition (personality facet, secondary advantage, supporting challenge) |
| `LOW` | Detail, teaching vignette, extra tendency that is not the section’s job |

Value is not classical prestige. Very Weak protection can be CRITICAL. Very Strong surplus is not automatically CRITICAL.

---

# 11. Specificity

| Value | Meaning | PACK-01 default |
|-------|---------|-----------------|
| `GENERIC` | True for the class without extra weather | Meanings, most personality, many advantages/challenges |
| `CONTEXTUAL` | Needs a named cause, luck, or edge condition | Causes, luck, many edge units, cause-tied advantages |
| `CASE_SPECIFIC` | Bound to one biography or one case ID | PACK-01 should rarely use this. Examples are teaching, not CASE_SPECIFIC. |

PACK-01 uses GENERIC and CONTEXTUAL almost exclusively.

---

# 12. Priority

| Value | Meaning |
|-------|---------|
| `CORE` | Section cannot tell the truth without this unit (lived meaning, class-level so-what, required why-cause, luck insufficient shell) |
| `HIGH` | Headline capacity, live cost, or steering action |
| `NORMAL` | Facet that may be selected under budget |
| `OPTIONAL` | Detail / extra facet / teaching |

Do **not** copy Rule Database priority numbers.

Do **not** treat `CORE` as “print everything”. Narrative budget still applies.

---

# 13. Narrative weight

| Value | Budget behavior |
|-------|-----------------|
| `CORE` | Cut last inside the section |
| `SUPPORTING` | Keep if budget allows |
| `DETAIL` | Cut early |
| `OPTIONAL` | May omit even when budget remains |

This is not the same field as `priority`. Priority is selection preference. Weight is what to cut after selection.

---

# 14. Status

| Value | Meaning |
|-------|---------|
| `Draft` | Authored from source. Not reviewed. Default for this delivery. |
| `Validated` | Passed [VALIDATION_RULES.md](VALIDATION_RULES.md) |
| `Frozen` | Locked for a production pack version |
| `Deprecated` | Must not enter Customer Mode |

---

# 15. Markdown shape

Each unit is a heading plus a field table plus claim / supporting_points / limitations blocks.

Long text is not forced into a single table cell.

The field names in the table must match §2 exactly.

---

END
