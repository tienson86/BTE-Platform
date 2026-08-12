# Executive Summary Planning

| Field | Value |
|-------|-------|
| Document | EXECUTIVE_SUMMARY_PLANNING |
| Version | 1.0.0 |

---

# 1. Principle

Reasoning Engine chooses the **claim set**.

Sentence Composer writes the 5–8 lines.

No new claims in the summary.

---

# 2. ExecutiveSummaryPlan

```text
ExecutiveSummaryPlan
├── claim_slots[]          5–8
│   ├── role
│   ├── source_section
│   ├── knowledge_ids[]
│   └── language_strength
└── omit_luck              true if luck insufficient
```

**Roles (priority):**

```text
Conclusion
Main cause
Main strength (usable capacity)
Main challenge
Main implication
Main recommendation
Close
```

Optional: second cause if C1 requires both polarities in one compressed line.

---

# 3. CASE-0001 slot sketch

1. Conclusion Strong (qualified)
2. Main causes: feed (season/root/support) AND control
3. Capacity: can carry load
4. Challenge: endurance as proof
5. Implication: recovery as operating condition
6. Recommendation: rest + one reviser
7. Close: strong ≠ no brake

No luck slot.

---

END
