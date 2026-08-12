# Duplicate Reasoning

| Field | Value |
|-------|-------|
| Document | DUPLICATE_REASONING |
| Version | 1.0.0 |

---

# 1. Information gain

A kept unit must add information not already in the plan.

If B only restates A:

```text
reject B
```

or

```text
merge A + B into the more specific representative
```

---

# 2. Overlap kinds

| Kind | Meaning | Action |
|------|---------|--------|
| `same_fact` | Same published fact retold | keep once in Why |
| `same_implication` | Same So What | keep highest salience |
| `same_advice` | Same do/avoid | keep more specific |
| `same_domain` | Same domain, no new constraint | drop extra |
| `semantic_overlap` | synonym family (tank / stamina / persist / backbone) | one family member in Meaning; later only if domain-specialized |

---

# 3. Pipeline

```text
Candidate Units
      ↓
Exact duplicate          same knowledge_id or identical claim_id
      ↓
Semantic duplicate       declared duplicates[] or overlap key
      ↓
Near duplicate           same_implication across purposes
      ↓
Retain best representative
```

---

# 4. Representative criteria (in order)

1. more specific
2. better supported (gate eligible > partial)
3. higher customer_value
4. less generic
5. higher evidence confidence / salience

---

# 5. Merge vs reject

Merge when two units add compatible qualifiers (thin root + season) into one Why paragraph plan (still two unit_ids in trace).

Reject when the second unit adds no qualifier.

---

END
