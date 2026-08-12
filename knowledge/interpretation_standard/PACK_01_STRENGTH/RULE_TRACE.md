# Rule Trace

| Field | Value |
|-------|-------|
| Document | RULE_TRACE |
| Pack | PACK-01 Strength |
| Version | 1.0.0 |
| Status | DESIGN ONLY |

---

# 1. Purpose

Rule Trace explains **why each activated Strength rule fired**.

It is a Validation Mode artifact.

Customers never see Rule Trace.

---

# 2. Why Rule Trace Exists

A matched rule list is not an explanation.

This is not a trace:

```text
STR-000001
STR-000007
STR-000012
```

This is a trace:

```text
STR-000001 fired because the month command is prosperous for this Day Master.
Contribution: seasonal support.
Polarity: support.
Priority: season group.
```

Without the second form, developers cannot audit, and Customer Mode “Why” cannot be grounded.

---

# 3. Trace Item Contract

Every activated rule SHALL produce one trace item:

| Field | Required | Content |
|-------|----------|---------|
| `rule_id` | Yes | Canonical ID (`STR-000001`, …) |
| `rule_name` | Yes | Human name |
| `category` | Yes | season / root / support / control / drain / special / combination / priority |
| `matched_conditions` | Yes | Which condition clauses matched |
| `satisfying_facts` | Yes | Chart facts that satisfied them |
| `unmatched_nearby` | If useful | Conditions that almost matched |
| `action` | Yes | Declared contribution / level hint / override |
| `polarity` | Yes | support / weaken / override / classify |
| `priority` | Yes | Published priority |
| `effect_on_final_class` | Yes | How this rule participates in Strong / Weak / … |
| `why_fired` | Yes | One precise analytical paragraph |
| `why_not_ignored` | If conflict | Why it was kept under priority |

Inactive rules do not get a fake “fired” trace.

---

# 4. Why-Fired Standard

`why_fired` must answer three auditor questions:

1. What did the rule look for?
2. What did this chart actually have?
3. What did the rule therefore do?

Wrong:

> Rule matched.

Wrong:

> Because the person is Strong.

Correct shape:

> The season rule looks for Day Master command in the month. This chart’s month branch places the Day Master in prosperous command. The rule therefore adds seasonal support toward a Strong classification.

`why_fired` is analytical language.

It may use technical terms.

It must not be Customer Mode copy.

---

# 5. Coverage Rules

1. Every activated rule in StrengthResult / Evidence Layer has a trace item.
2. The final level/classification rule has a trace item.
3. Special-exception overrides have a trace item that states they override ordinary scoring.
4. Priority rules that selected the winner have a trace item.
5. Rules inspected but not activated may appear in a separate `near_miss` list, never in the activated list.

---

# 6. Near Misses

Near misses help Alternative Analysis.

A near miss is a rule that:

- belongs to a competing class, and
- failed one or more conditions, and
- would have changed confidence or class if it had fired

Near-miss item:

- rule ID
- failed condition
- fact that failed it
- class it would have supported

Do not flood the trace with every unused rule in the database.

Only material near misses.

---

# 7. Order

Deterministic order:

1. Special overrides
2. Season
3. Root
4. Support (visible stem, hidden stem, generation)
5. Drain / control / restriction
6. Combination / clash / harm / punishment / void as strength factors
7. Growth stage
8. Temperature influence if present
9. Priority / level classification
10. Near misses

This order is for auditors.

It is not Customer Mode order.

---

# 8. Relationship to Customer Why

Customer Mode “Why” is a **lossy, leak-free compression** of Rule Trace.

Compression rules:

- Drop Rule IDs
- Drop scores
- Keep only material causes
- Speak in life-relevant structure (season, root, support, leak)
- Do not keep every minor rule if it does not change meaning

If Rule Trace says the class is Strong because of season + two roots, Customer Why may not say it is Strong “because you were born lucky”.

---

# 9. Forbidden Trace Behaviors

- Reconstructing a rule that the engine did not match
- Explaining a rule with a different chart fact than the one that matched
- Using Customer Mode adjectives (“resilient leader”) inside the trace
- Omitting an override because it is rare
- Collapsing all rules into one sentence “multiple factors agree” with no IDs in Mode A

---

# 10. Strength Rule Families in Trace Language

| Family | Trace must show |
|--------|-----------------|
| Season | Command phase vs Day Master |
| Root | How many / how deep / hidden vs none |
| Support | Which stems / elements support |
| Control | What restricts the Day Master |
| Drain | What exhausts the Day Master |
| Special | Why ordinary scoring is insufficient |
| Combination | Multi-factor interaction |
| Priority / level | Why this class beat the alternative |

---

# 11. Future Pack Reuse

Every later pack MUST produce Rule Trace with the same item contract.

Only rule-id prefixes and families change (`PAT-…`, `UG-…`, `TG-…`, `SS-…`).

A pack without Rule Trace cannot produce a legal Customer Why.

---

END
