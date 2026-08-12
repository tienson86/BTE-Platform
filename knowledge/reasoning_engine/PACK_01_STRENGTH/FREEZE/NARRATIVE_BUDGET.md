# Narrative Budget — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | NARRATIVE_BUDGET |
| Status | FROZEN |

---

# 1. Frozen Customer Mode caps (units)

| Section | Min | Max |
|---------|-----|-----|
| Conclusion | 1 | 1 |
| Why | 2 | 4 |
| Meaning | 1 | 1 |
| Advantages | 2 | 2 |
| Challenges | 2 | 2 |
| Personality | 0 | 0 |
| Career | 0 | 1 |
| Wealth | 0 | 0 |
| Marriage | 0 | 1 |
| Health | 0 | 1 |
| Learning / Leadership / Decision | 0 | 0 |
| Luck content units | 0 | 0 if luck MISSING; else 0–2 |
| Luck shell | 1 if luck MISSING | 1 |
| Recommendations | 2 | 3 |
| Warnings | 0 | 1 |
| Edge as own section | 0 | 0 (qualifier on conclusion) |
| Executive Summary claims | 5 | 8 |

These caps freeze the **CASE-0001 golden** value audit (tighter than the pre-freeze design draft).

`question_context` in a later version may raise Wealth/Career caps. V1.0 default = table above.

Validation Mode: no cap.

---

# 2. Why overflow (5 present causes, max 4)

Frozen merge:

1. Keep control if C1 (never drop the weakening polarity).
2. Keep root-thin if `root_thin`.
3. Keep season.
4. Keep support.
5. **Merge** special into season (`MERGED_CAUSE_SPECIAL_INTO_SEASON`). Special remains on ClaimTrace.

Do not drop control to make Why prettier.

---

# 3. Compression

When over max:

1. Drop `SAL_5`
2. Drop `narrative_weight = supporting` then `omit_ok`
3. Drop `REL_4` then `REL_3` extras
4. Drop duplicate members (already)
5. Never drop Conclusion
6. Never drop the sole remaining C1 polarity

Reason: `REJECTED_NARRATIVE_BUDGET`.

---

# 4. Expansion

Under min:

- Do **not** fill with generic units
- Short plan is legal
- Empty optional domain → omit (`OMITTED_DOMAIN`)
- Luck MISSING → shell only

---

# 5. Priority of cuts

Salience ascending (cut `SAL_5` first), then knowledge_id ascending for ties.

---

END
