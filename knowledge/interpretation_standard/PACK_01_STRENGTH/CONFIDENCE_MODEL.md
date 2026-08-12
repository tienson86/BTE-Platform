# Confidence Model

| Field | Value |
|-------|-------|
| Document | CONFIDENCE_MODEL |
| Pack | PACK-01 Strength |
| Version | 1.0.0 |
| Status | DESIGN ONLY |

---

# 1. Purpose

The Confidence Model states how sure the Strength interpretation is about the primary class, and why.

It is a Validation Mode artifact.

Customer Mode never prints confidence.

---

# 2. What Confidence Is

Confidence is **agreement and completeness of evidence**, not a prediction of life success.

Wrong meaning:

> 92% chance this person will succeed.

Correct meaning:

> 92% of the interpretable evidence supports Strong rather than a competing class, given current data quality.

---

# 3. Dual Representation

To stay compatible with the existing Reasoning Framework and with Mode A’s numeric requirement, confidence has two linked views.

| View | Vocabulary | Where shown |
|------|------------|-------------|
| Qualitative | experimental / low / medium / high / canonical | internal alignment with Reasoning Framework |
| Numeric | integer percent 0–100 | Validation Mode |

Customer Mode: neither.

---

# 4. Qualitative Ranks

| Rank | ID | Typical numeric band |
|------|----|----------------------|
| 0 | experimental | 0–20 |
| 1 | low | 21–40 |
| 2 | medium | 41–70 |
| 3 | high | 71–90 |
| 4 | canonical | 91–100 |

Bands are reporting bands.

They are not a new Strength scorer.

A future implementation must declare the exact mapping function in code comments and tests. This document defines the **policy**, not a hidden formula in production.

---

# 5. Inputs to Confidence

Confidence MAY use only published information:

1. Completeness of required Strength dimensions
2. Agreement among supporting dimensions
3. Presence and severity of conflicts
4. Distance from class boundaries
5. Special-exception clarity (clear override vs disputed override)
6. Count and quality of activated rules (as published, not re-matched)
7. Missing data that could change class
8. Engine-published confidence, if any, as an input — never as an unexplained copy

Confidence MUST NOT use:

- How much the customer paid
- How dramatic the story would be
- Unrelated Pattern / Useful God certainty
- Random noise
- “Expert vibe”

---

# 6. Policy Formula (Design)

Logical composition:

```text
start from completeness
  + agreement among season / root / support
  − conflict penalty
  − missing-data penalty
  − boundary penalty
  + clear special-override bonus (only if override is well evidenced)
clamp to 0–100
```

Illustrative policy, not executable code:

| Condition | Direction |
|-----------|-----------|
| Season, root, and stem polarity agree | raise |
| Only one thin factor supports the class | lower |
| Special override with complete evidence | raise toward high/canonical for the override class |
| Special override with incomplete evidence | lower |
| Score/class near threshold | lower (boundary penalty) |
| Hour pillar missing but class does not depend on it | small or zero penalty |
| Hour pillar missing and hidden-root class depends on it | material penalty |
| Luck missing | does not lower natal class confidence; luck section is separately insufficient |
| Engine published confidence exists | may cap or inform, never silently replace explanation |

A later implementation must keep this policy inspectable in Mode A.

---

# 7. Required Explanation

Every numeric confidence MUST have a why.

Required explanation parts:

1. What raised confidence
2. What lowered confidence
3. Whether missing data could flip the class
4. Whether a conflict remains after engine resolution

Example (Validation Mode only):

```text
Confidence: 92% (high → canonical band)
Raised by: season command, two roots, peer stem, no special counter-rule
Lowered by: one mild drain
Flip risk: low — drain is not enough to reach Balanced unless roots were misread
Missing data: none for natal class
```

Forbidden explanation:

```text
Confidence: 92%
```

---

# 8. Boundary Cases

When the engine class sits near a threshold:

- Confidence MUST drop relative to a deep-in-class case
- Alternative Analysis MUST show the neighboring class
- Customer Mode MAY use a bounded qualifier without numbers

Allowed customer qualifier:

> Nhật chủ nghiêng về nhóm Thân Vượng, với một phần lực bị tiêu hao nên không phải dạng dư lực quá mức.

Forbidden customer qualifier:

> Strong 92% / Balanced 8%.

---

# 9. 100% Policy

100% is almost never honest.

Canonical band (91–100) is allowed when:

- required dimensions are present
- polarities agree
- no material conflict
- no missing field that could flip class
- special exceptions are either clearly off or clearly on

Even then, Mode A should prefer 91–99 unless the case is a designated golden extreme with complete data.

Customer Mode still prints no percent.

---

# 10. Leakage

| Surface | Confidence |
|---------|------------|
| Validation Mode | Required |
| Customer Mode body | Forbidden |
| Executive Summary | Forbidden |
| Report footnotes for customers | Forbidden |
| Developer audit export | Required |

Words that leak confidence into Customer Mode:

- confidence
- 92%
- probability
- canonical
- experimental
- score agreement 0.92

These words are Validation Mode only.

---

# 11. Relationship to Engine Confidence

Strength Engine currently publishes a `confidence` field.

Interpretation Standard policy:

1. Treat engine confidence as **one input**.
2. Do not copy it blindly as Mode A output if Missing Data or Conflicts were not considered.
3. Do not recompute Strength.
4. If engine confidence is absent, Mode A still computes interpretation confidence from evidence completeness and agreement.

This is not a second Strength Engine.

This is interpretation honesty about the published result.

---

# 12. Future Pack Reuse

Every later pack MUST:

- expose Mode A numeric + qualitative confidence
- explain why
- hide it from Customer Mode
- penalize missing data and conflicts
- never treat confidence as fate probability

---

END
