# Conflict Resolution — PACK-01 Prototype

| Field | Value |
|-------|-------|
| Document | CONFLICT_RESOLUTION |
| Pack | PACK-01 Prototype |
| Version | 1.0.0 |

---

# 1. Purpose

Handle disagreement **without flipping the published class** and without hiding a polarity.

---

# 2. Conflict types

| Type | Example | Resolution |
|------|---------|------------|
| C1 Dimension polarity | Season/support strengthen vs control weaken | Keep both in Evidence and Why. Primary class unchanged. Confidence penalty. |
| C2 Neighbor class | Facts could be read as Balanced | Alternative Analysis only. Do not load Balanced meaning as primary. |
| C3 Special vs ordinary | Special present but not an override | Trace special as support, not as a second class. |
| C4 Missing vs story | Luck missing | Insufficient Data. Do not load luck units. |
| C5 Knowledge vs facts | A unit requires drain, drain is 0 | Reject unit (CAUSE_ABSENT). |
| C6 Cross-pack temptation | Useful God / Pattern sitting nearby in the case file | Out of input scope. Ignore. Not a Strength conflict. |

---

# 3. Hard rules

1. Engine mapped class wins for Conclusion.
2. Losing polarities stay visible in Mode A.
3. Mode B may synthesize **one lived weather** (“force is real, and something sits on you”) — not two classes.
4. Knowledge units from the losing class are not selected as Meaning/Advantage/Challenge primaries.
5. Edge units may add a qualifier only if `conflict_support_vs_control` or `root_thin` is true.
6. Never “average” Strong and Weak into Balanced inside the composer.

---

# 4. Unit-level conflict

If two kept units contradict (e.g. Advantage “unbreakable stress tolerance” vs Health “you must downshift”):

- Prefer the unit whose `use_when` is more specific to present facts
- Drop the absolute (“unbreakable”)
- Keep the operating cost if Challenges already own it

Strong + control present → do not select Very Strong “other people’s fatigue does not register” as if control were absent. Control is a steering fact; Challenges should include receptivity / pressure, not omnipotence.

---

# 5. CASE-0001 mapping

Present: season strengthen, root strengthen (thin), support strengthen, special strengthen, control weaken, drain inactive.

| Conflict | Handling |
|----------|----------|
| Support-side vs control | C1 — Why names both |
| Thin root vs “deep floor” knowledge | Reject `root_deep` units |
| Drain leak knowledge | Reject drain units |
| Balanced meaning | Reject as primary; allow Alternative in Mode A |
| Luck overdrive knowledge | Reject; Luck = insufficient |
| Temperature `hot` | Not a Strength fact — ignore |

---

# 6. Mode B qualifier (optional)

Only if C1 is live and root is thin:

Allowed (leak-free):

> Nhật chủ thuộc nhóm Thân Vượng, nhưng không phải dạng dư lực không bị kiểm.

Forbidden:

> Strong 87% / Balanced 13%.
> Expert said Weak so we split the difference.

Expert labels are not S0 input and must not appear in Mode B.

---

END
