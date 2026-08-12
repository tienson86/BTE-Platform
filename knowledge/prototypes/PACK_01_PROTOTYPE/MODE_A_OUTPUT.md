# Mode A Output — Validation

| Field | Value |
|-------|-------|
| Document | MODE_A_OUTPUT |
| Pack | PACK-01 Prototype |
| Audience | Developers / auditors |
| Customer visibility | Never |

---

# 1. Purpose

Specify the Validation projection of the prototype.

Customers never see this mode.

---

# 2. Required sections (order)

1. Final Conclusion
2. Evidence
3. Rule Trace
4. Confidence
5. Alternative Analysis
6. Missing Data
7. Conflicts

Shells are mandatory. Empty content is allowed only as `none` / `missing` / `not_applicable` with a reason.

---

# 3. Final Conclusion

- Mapped interpretation class
- Engine `strength_level` as source
- Vietnamese / English labels
- Explicit statement: class was **not** altered to match knowledge or expert taste

---

# 4. Evidence

Grouped:

- Activated rules (IDs, group, polarity, contribution if published)
- Supporting factors
- Weakening factors
- Inactive inspected (e.g. drain = 0)
- Component scores (`internal_only`)
- Classification source (level rule if published)

Every item has `evidence_id`.

---

# 5. Rule Trace

For each activated rule:

- why it fired (matched condition + satisfying fact + action)
- polarity
- effect on final class

Near misses only if material to Alternative Analysis.

---

# 6. Confidence

Numeric percent + qualitative band + why (raised / lowered / flip risk / missing).

Engine confidence is shown as an **input fact**, then interpretation confidence as the Mode A value.

Customer Mode prints neither.

---

# 7. Alternative Analysis

Primary share + runner-up or `none_plausible`.

Must explain what would have made the alternative win.

Must not change the primary class.

---

# 8. Missing Data

Every Strength-relevant field the prototype wanted and did not receive.

Typical CASE-0001 entries (only if actually absent in facts):

- luck interaction (public luck not exposed)
- hidden stems (not exposed)

Do not list Pattern or Useful God as missing Strength data. They are out of input scope.

---

# 9. Conflicts

Dimension or rule disagreements inside Strength facts.

Example shape: season/support/special strengthen vs control weaken.

Resolution: engine class remains primary; both polarities remain visible; confidence penalized.

---

# 10. Extra Mode A appendix (prototype)

Allowed in prototype, still not customer-facing:

- Selected unit IDs
- Rejected unit IDs + reasons
- Duplicate drops
- Composer provenance

This appendix answers the seven prototype questions.

---

END
