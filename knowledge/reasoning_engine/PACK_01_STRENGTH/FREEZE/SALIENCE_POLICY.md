# Salience Policy — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | SALIENCE_POLICY |
| Status | FROZEN |

---

# 1. Difference from Relevance

| | Relevance | Salience |
|--|-----------|----------|
| Question | Does it belong? | Is it worth saying / keeping under budget? |
| Example | “Strong people persist” is relevant to class Strong | Often not salient (generic) |
| Example | Control weaken on CASE-0001 | High salience (this chart, C1) |

A unit may be `REL_2` and still `SAL_4` (supporting).

---

# 2. Frozen levels

| Level | Code | When | Why |
|-------|------|------|-----|
| Required shell | `SAL_0` | Conclusion / insufficient-data shell | Story cannot omit |
| Chart-critical | `SAL_1` | C1 polarity, thin-root, present Why causes | Honesty + specificity |
| Core So What | `SAL_2` | Meaning primary; high `customer_value` challenge | Customer understanding |
| Action | `SAL_3` | Recommendation with live dependency chain | What to do |
| Domain primary | `SAL_4` | One unit per kept domain | Life implication |
| Supporting | `SAL_5` | Extra facets, generic, omit_ok | Cut first |

Lower number = more salient.

---

# 3. Customer value vs salience

`customer_value` is a **catalog field**.

Salience **uses** it:

- `critical` or `high` + chained rec → at most `SAL_3`
- `low` + `generic` → `SAL_5`
- `high` + `cause_specific` Why → `SAL_1`

Customer value is not narrative order by itself.

Knowledge `priority` (1–100) is **tie-break only** after salience, relevance, specificity.

---

# 4. Assignment order (deterministic)

1. Conclusion and luck-insufficient shell → `SAL_0`
2. WHY units whose facts participate in a declared FACT conflict, or `root_thin` → `SAL_1`
3. Other PASS WHY → `SAL_1` if `cause_specific` else `SAL_2`
4. MEANING with `narrative_weight=primary` → `SAL_2`
5. CHALLENGE/ADVANTAGE with `customer_value` high/critical → `SAL_2`
6. RECOMMENDATION with all dependencies kept → `SAL_3` else reject `REJECTED_NO_CHAIN`
7. One domain unit per kept domain → `SAL_4`
8. Else → `SAL_5`

---

# 5. Future packs

Same `SAL_0`–`SAL_5`.

Pack-specific: which facts count as “chart-critical” (e.g. Pattern clash).

---

END
