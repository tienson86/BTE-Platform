# Transition Engine — PACK-01 Prototype

| Field | Value |
|-------|-------|
| Document | TRANSITION_ENGINE |
| Pack | PACK-01 Prototype |
| Version | 1.0.0 |

---

# 1. Purpose

Transitions move the reader from one **job** to the next.

They never add analysis.

They are a closed catalog, not LLM glue.

---

# 2. When a transition is inserted

After section N is composed, before section N+1, if both sections have content (or an Insufficient Data shell).

No transition inside a single-sentence section.

No transition that restates the previous paragraph.

---

# 3. Catalog (structural)

| From → To | Job of the bridge | Allowed stem (VI) | Allowed stem (EN) |
|-----------|-------------------|-------------------|-------------------|
| Conclusion → Why | what → why | `Điều này đứng vững vì` | `This standing holds because` |
| Why → Meaning | why → so what | `Với cấu trúc này` | `With this structure` |
| Meaning → Advantages | identity → usable capacity | `Lực này giúp` | `This force helps` |
| Advantages → Challenges | capacity → cost | `Cùng một lực đó` | `The same force` |
| Challenges → Influence | cost → life areas | `Trong đời sống` | `In lived life` |
| Influence child → child | domain switch | `Về tiền bạc` / `Trong quan hệ` / `Về sức khỏe` | `With money` / `In the bond` / `In the body` |
| Influence → Luck | natal → time | `Theo thời` | `Over time` |
| Influence → Luck (missing) | honest gap | `Phần vận trình` | `The luck chapter` |
| Luck or Influence → Recommendations | meaning → action | `Vì vậy` | `Therefore` |
| Recommendations → Executive Summary | none (summary is a new block, not a bridge sentence) | — | — |

Stems are **structural**. The following clause must come from a knowledge unit or from the Insufficient Data shell — not from the stem.

---

# 4. Forbidden transitions

- “Ngoài ra bạn còn có Dụng thần…” (other-pack theft)
- “Điểm số cho thấy…” (leak)
- “Nhưng có thể bạn là Thân Nhược…” (second class)
- Literary decoration with no job
- A bridge that contains a new cause

---

# 5. Duplicate guard

If the first sentence of section N+1 already contains the bridge idea, skip the catalog stem.

Example: Meaning unit already starts with “Với cấu trúc này” → do not prepend the same stem.

---

# 6. CASE-0001 application

See [EXAMPLE_CASE_0001.md](EXAMPLE_CASE_0001.md) stage S9.

Luck is missing → use the **honest gap** stem, then the Insufficient Data shell, then skip to Recommendations with `Vì vậy` based on natal sections only.

---

END
