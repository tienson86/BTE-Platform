# Sentence Composer — PACK-01 Prototype

| Field | Value |
|-------|-------|
| Document | SENTENCE_COMPOSER |
| Pack | PACK-01 Prototype |
| Version | 1.0.0 |

---

# 1. Purpose

Demonstrate how **multiple knowledge units** become paragraphs.

The composer does not invent claims.

It does not call an LLM.

It assigns each surviving unit a **sentence job**, then concatenates in official order.

---

# 2. Input

- Surviving knowledge units (after selection, priority, conflict, duplicate removal)
- Evidence Layer (for Mode A and for Mode B provenance, hidden)
- Interpretation Standard sentence jobs
- Transition catalog

---

# 3. One unit, one job

| Unit topic | Sentence job | Mode B section |
|------------|--------------|----------------|
| Meaning lived | Interpret | Meaning |
| Meaning tendency | Interpret (second sentence only if not duplicate) | Meaning |
| Cause | Explain | Why |
| Advantage facet | Upside | Advantages |
| Challenge facet | Cost | Challenges |
| Personality facet | Domain effect | Life Influence / personality |
| Career facet | Domain effect | Career |
| Wealth facet | Domain effect | Wealth |
| Marriage facet | Domain effect | Marriage |
| Health facet | Domain effect | Health |
| Luck facet | Time effect | Luck |
| Recommendation do | Direct | Recommendations |
| Recommendation avoid | Caution | Recommendations |
| Edge qualifier | Interpret (bounded) | Why or Meaning, never a second class |

Conclusion is **not** a knowledge unit. It is the mapped class rendered in leak-free language from the Standard.

Executive Summary is **not** new units. It compresses already composed sections.

---

# 4. Assembly order (Mode B)

```text
1  Conclusion          (class render)
2  Why                 (cause units, priority order)
3  Meaning             (meaning units)
4  Advantages          (advantage units)
5  Challenges          (challenge units)
6  Life Influence
     Personality
     Career
     Wealth
     Marriage
     Health
     (Learning / Leadership / Decision making if units survived caps)
7  Luck                (or Insufficient Data)
8  Recommendations     (do then avoid)
9  Executive Summary   (compress 1–8, 5–8 lines)
```

This is the official narrative order.

Display may put Executive Summary first. The text is still authored last.

---

# 5. How a paragraph is built

For one section:

```text
units_in_section (already de-duplicated, priority-sorted)
        ↓
for each unit:
    take unit.so_what
    apply Sentence Standard (one job, So What, leak ban)
    attach hidden evidence_ids
        ↓
join with transitions from Transition Engine
        ↓
paragraph exists because: section job + selected units
```

If `units_in_section` is empty and the section is required:

- Luck / optional cause → Insufficient Data shell
- Meaning with class mapped → prototype error (knowledge gap)
- Conclusion → class render still emits (not a knowledge unit)

---

# 6. Provenance (required)

Every Mode B sentence stores, hidden:

```text
sentence_id
section
unit_ids[]
evidence_ids[]
job
why_this_paragraph_exists
```

`why_this_paragraph_exists` is a short audit phrase, for example:

- “Customer Why must explain present season + root + support + control”
- “Career influence must not repeat Meaning stamina as a job title”

Mode A may list this provenance. Mode B text must not.

---

# 7. What the composer must not do

- Rewrite meaning with an LLM
- Add a career the units do not support
- Merge Why and Recommendations into one sentence
- Print Rule IDs, scores, `male`, `strong` as a raw token, `hot`, dumps
- Fill Luck when luck facts are missing
- Use `13_EXAMPLES.md` vignettes as output (those are teaching, not this person’s life)

---

# 8. Demonstration vs production templates

This prototype composes from the **so_what / consultant phrasing already in the knowledge pack**.

That is selection + assembly.

It is not a new sentence library (`SEN-*`).

A later production Sentence Engine may bind the same unit IDs to `SEN-*` records. The selection logic stays.

---

END
