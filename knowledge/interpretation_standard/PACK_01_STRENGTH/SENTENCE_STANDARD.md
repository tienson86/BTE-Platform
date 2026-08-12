# Sentence Standard

| Field | Value |
|-------|-------|
| Document | SENTENCE_STANDARD |
| Pack | PACK-01 Strength |
| Version | 1.0.0 |
| Status | DESIGN ONLY |

---

# 1. Purpose

This document defines how Strength interpretation sentences are written.

It is a writing contract for all future interpretation packs.

It is not a production sentence library.

Do not copy examples into engines as hard-coded output.

---

# 2. The Master Test

Every sentence must survive:

> So what?

If the customer can still ask “So what?” after the sentence, the sentence is unfinished.

---

# 3. One Sentence, One Job

A sentence may do only one of:

| Job | Typical section |
|-----|-----------------|
| Name | Conclusion |
| Explain | Why |
| Interpret | Meaning |
| Upside | Advantages |
| Cost | Challenges |
| Domain effect | Influence |
| Time effect | Luck Cycles |
| Direct | Recommendations (do) |
| Caution | Recommendations (avoid) |
| Close | Executive Summary |

If a sentence names + explains + advises, split it.

---

# 4. Person-Specific, Not Dictionary

Wrong:

> Thân Vượng means the Day Master is strong.

Wrong:

> Official Officer represents authority and discipline.

The second sentence is forbidden in PACK-01 even as a side lecture.

Correct direction:

> With this standing, you enter work already carrying force. That helps you hold responsibility, and it can make you slow to accept correction.

Explain what it means **for this person**.

---

# 5. Fact → Value

Never leave a fact unconverted.

| Fact sentence (fail) | Value sentence (pass) |
|----------------------|------------------------|
| You have Strong Metal. | You tend to be determined and resilient. This helps in leadership roles but may also make you less receptive to criticism. |
| Season supports the Day Master. | You are not starting from empty. Seasonal support gives you a default stamina that others may need to build. |
| There is drain. | Effort leaks when you take on too many demands at once. Pace is part of strength, not a denial of it. |
| Luck will support you. | When luck adds force, you can take larger load — and you can over-commit before you notice. |

---

# 6. Grammar Preferences

| Prefer | Avoid |
|--------|-------|
| Second person to the chart owner | System voice (“the algorithm detected”) |
| Active, calm verbs | Destiny commands |
| Concrete life referents | Empty grandeur |
| One main clause | Nested clause chains |
| Evidence-matched modality | Fake precision |

Modality:

- Allowed: tend to, often, in this structure, when luck adds force
- Forbidden: certainly will, doomed, guaranteed, 80% chance of promotion
- Forbidden: using “may” to hide missing evidence

---

# 7. Leak Ban at Sentence Level

A sentence fails if it contains:

- Rule IDs
- confidence / percent
- raw scores
- raw enums (`male`, `strong`, `success`, `hot`)
- dict/list dumps
- engine or pack names
- matcher/priority talk
- English UI labels inside Vietnamese body (`Observation:`, `Critical`)

Natural class language is allowed:

- nhóm Thân Vượng
- Strong category

---

# 8. Vietnamese / English

Primary commercial language: Vietnamese.

English must follow the same jobs and bans.

Do not mix undeclared languages in one sentence.

Technical BaZi terms in Vietnamese are allowed when they help, and must be framed in plain language on first use in Customer Mode.

Example of framing:

> Nhật chủ (bản thân trong lá số) thuộc nhóm Thân Vượng.

Do not stack unexplained terms to sound expert.

---

# 9. Strength Class Sentence Patterns

These are **pattern shapes**, not templates to paste.

## Very Strong

Must convert surplus into operating cost, not worship.

Fail: You are extremely powerful.

Pass direction: You have surplus force. Used well, you can carry a heavy load. Used without a brake, you override people and timing.

## Strong

Fail: You are strong.

Pass direction: You can persist and lead. The same force can close the ear that needs to hear correction.

## Balanced

Fail: You are average.

Pass direction: You can adjust to more than one environment. The risk is waiting for perfect balance instead of choosing.

## Weak

Fail: You are weak. This is bad.

Pass direction: You do more with the right support than by forcing a solo push. The work is to choose environments that feed you, not to prove you need no one.

## Very Weak

Fail: Your fate is poor.

Pass direction: The chart asks for protection of energy and strong external structure. This is a design constraint, not a verdict on worth.

---

# 10. Recommendation Sentences

Do-sentences start from capability + structure.

Avoid-sentences name the specific overuse of that structure.

Paired example (illustrative):

- Do: Put stamina into a role with clear load and a feedback loop.
- Avoid: Treat disagreement as an attack on competence.

Do not recommend a new career from Strength alone.

Do not recommend buying a product.

---

# 11. Insufficient Data Sentences

When data is missing:

- Say the limit
- Keep dignity
- Do not fill with “có thể là…”

Fail: Even without the birth hour, you are definitely Strong and will marry late.

Pass: Without complete time data, this reading cannot specify the luck-cycle effect. The natal standing above still holds from the available pillars.

---

# 12. Anti-Patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Dictionary definition | No person-specific value |
| Fact leftover | So what unanswered |
| Rule-engine prose | Leak + no consulting value |
| Fear sales | Brand and ethics fail |
| Flattery | No challenge, no trust |
| Repetition with synonyms | Value Framework fail |
| Mega-sentence | Mixed jobs |
| New fact in closing line | Honesty fail |
| Shame | “You are weak so you fail” |
| Prophecy | “Next year you will…” without published luck fact |

---

# 13. Future Pack Reuse

Every later pack MUST apply:

- So what test
- one sentence one job
- person-specific meaning
- leak ban
- no dictionary lectures

Ten Gods pack must not explain “what Official Officer means”.

It must explain what that Officer structure does in this person’s life.

---

END
