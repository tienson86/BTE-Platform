# Priority Model

| Field | Value |
|-------|-------|
| Document | PRIORITY_MODEL |
| Version | 1.0.0 |

---

# 1. Three different priorities

| Kind | Owner | Means |
|------|-------|-------|
| **Rule Priority** | Strength Engine / Rule Database | Which rule wins when scoring |
| **Knowledge Priority** | Knowledge unit metadata | Which unit is preferred among similar knowledge |
| **Narrative Priority** | Reasoning Engine | Where the claim sits in the customer story |

They are not interchangeable.

A special rule with priority 102 can be a **supporting Why clause**, not the opening of the report.

A high knowledge-priority generic unit can lose to a lower-priority cause-specific unit (specificity / salience).

---

# 2. Narrative Priority (canonical order)

```text
1. Core conclusion
2. Causal explanation (Why)
3. Major practical implication (Meaning)
4. Major challenge / risk
5. Domain implications (per Domain Ordering)
6. Recommendations
7. Secondary details
8. Executive Summary (authored last; may display first)
```

Advantages sit with (3) as “usable capacity” after Meaning, before Challenges (4), matching Interpretation Standard conversation order.

Default customer sequence:

```text
Conclusion → Why → Meaning → Advantages → Challenges
→ Domain implications → Luck → Recommendations → Executive Summary
```

---

# 3. Why-cause order (when present)

Among WHY units, narrative order is:

1. Special (if present and not override — as weather)
2. Season
3. Root
4. Support
5. Drain (skip if inactive)
6. Control
7. Combination / clash / void

This is **narrative** order for explanation, not rule priority.

---

# 4. Knowledge priority use

Use knowledge `priority` only as a **tie-break** inside the same purpose, same specificity, same salience band.

Never as the report outline.

---

# 5. Rule priority use

Reasoning Engine **reads** rule priority only inside Evidence / Rule Trace (Mode A).

It does not sort Customer Mode by `sea_002` priority 95.

---

END
