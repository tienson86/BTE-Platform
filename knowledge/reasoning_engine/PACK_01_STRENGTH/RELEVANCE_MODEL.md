# Relevance Model

| Field | Value |
|-------|-------|
| Document | RELEVANCE_MODEL |
| Version | 1.0.0 |

---

# 1. Purpose

`RelevanceScore` answers: **does this unit belong in the candidate conversation at all?**

It is not Strength Score.

It is not Salience (“what to say first”).

---

# 2. Factors (design weights, not frozen production formula)

| Factor | Direction | Notes |
|--------|-----------|-------|
| Fact Match | + | required facts present and polarity matches |
| Specificity | + | cause_specific > class_level > generic |
| Customer Value | + | metadata `customer_value` |
| Evidence Strength | + | published polarity magnitude / completeness of that dimension — **not** total strength_score |
| Domain Importance | + | default domain weight, overridable by `question_context` |
| Novelty | + | not already covered by a kept claim |
| Conflict Penalty | − | unresolved TRUE CONTRADICTION |
| Duplicate Penalty | − | overlap with a higher-ranked unit |
| Missing Data Penalty | − | optional facts missing that the claim leans on |

Prototype policy (inspectable, replaceable by versioned policy):

```text
relevance = fact_match
          + specificity
          + customer_value
          + evidence_strength
          + domain_importance
          + novelty
          − conflict_penalty
          − duplicate_penalty
          − missing_data_penalty
```

Each term is a declared 0–1 contribution in a future implementation table. This design forbids opaque ML scores.

---

# 3. What Relevance must not use

- Total `strength_score` as a proxy for “this career unit is relevant”
- Rule Database priority
- How dramatic the sentence would be
- Expert labels not in `ReasoningInput`

---

# 4. Use

1. Sort eligible units inside a purpose bucket.
2. Feed Salience (salience may use relevance as one input).
3. Budget cuts start from lowest relevance among non-required shells.

A unit can be relevant (about this chart) and still not salient (not the thing to lead with).

---

END
