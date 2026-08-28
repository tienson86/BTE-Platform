# 02 — Framework

| Field | Value |
|-------|--------|
| Document | INT-02A Framework |
| Version | 1.0.0 |
| Status | Canonical for INT-02A |

---

## 1. Five required blocks

Every Topic Narrative Unit contains exactly these blocks, in this order:

| Order | Slot | Section id | Vietnamese title | English title |
|-------|------|------------|------------------|---------------|
| 1 | `observation` | `sec-observation` | Quan sát | Observation |
| 2 | `reasoning` | `sec-reasoning` | Lý do | Reasoning |
| 3 | `impact` | `sec-impact` | Tác động | Impact |
| 4 | `recommendation` | `sec-recommendation` | Khuyến nghị | Recommendation |
| 5 | `conclusion` | `sec-conclusion` | Kết luận | Conclusion |

No topic may omit a block.

A block with no publishable fact uses the platform insufficient outcome. It does not disappear.

---

## 2. Block meaning

| Block | Speaks | Must not |
|-------|--------|----------|
| Observation | What the engine published | Explain why, advise, or conclude life meaning |
| Reasoning | Why that observation follows from published facts | Recalculate, introduce new facts |
| Impact | What that means for the person, bounded | Guarantee outcomes, invent domains |
| Recommendation | What to do next, from published guidance | Invent actions, medical/legal/finance advice |
| Conclusion | Settled reading of this topic | Open a new topic or contradict earlier blocks |

Optional Pack 05 chart sections (`Executive Summary`, `Warning`) are **not** topic-required blocks.

Caution belongs inside Impact or Recommendation when the topic evidence supports it.

---

## 3. Template hierarchy

```
Topic Template
    ↓
Block Template
    ↓
Sentence Template
    ↓
Slot (engine fact)
```

| Level | Owns | Example |
|-------|------|---------|
| Topic template | Which facts a topic may narrate | Strength topic may bind `strength_level` |
| Block template | Which sentence roles fill a block | Observation uses fact sentences only |
| Sentence template | Wording with placeholders | `Nhật chủ được đọc là {strength_level}` |
| Slot | A published engine field | `strength.strength_level` |

Templates do not compute slot values.

Empty slots do not receive invented fillers.

---

## 4. Sentence ownership

| Artifact | Owner | May change wording? |
|----------|--------|---------------------|
| Engine fact / classification / score | Analytical engine | No (narrative reads only) |
| Sentence template (`SEN-*`) | Sentence library / knowledge | Yes, in knowledge sprints |
| Block order and slot names | Narrative Framework | No after INT-02A freeze |
| Sentence selection among candidates | Interpretation Engine (existing) | Unchanged in INT-02A |
| Delivery layout | Report / Portal | Unchanged in INT-02A |
| LLM | None | Forbidden as author of record |

A sentence that cannot cite a published fact is not eligible.

A recommendation whose canonical text is malformed (for example a lone `"1"`) remains canonical truth until a later content sprint repairs the **source**. The framework must not replace it with fabricated prose.

---

## 5. Prose policy (architecture)

- Observation is factual and short.
- Reasoning is explanatory and cites observation facts.
- Impact is concrete and domain-bounded (career / finance / relationship / health only when evidence exists).
- Recommendation is directive and reversible. It is not a prediction.
- Conclusion restates the topic reading. It does not add new facts.

Tone remains Brand Language: consultant, not calculator.

Ban classes from `docs/architecture/interpretation/03_NARRATIVE_GUIDE.md` still apply. INT-02A does not rewrite that frozen policy.

---

## 6. Insufficient data

Use one customer outcome for unpublished topic facts:

`Chưa có dữ liệu`

Do not use `N/A`, `null`, `—`, `Không`, or `Chờ dữ liệu` as the topic-block empty contract.

CP-01 Tứ Trụ empty glyphs remain a frozen UI exception and are out of this framework.

---

END
