# PACK-01 — Strength Interpretation Standard

| Field | Value |
|-------|-------|
| Pack | PACK-01 |
| Domain | Strength (Thân Vượng / Thân Nhược) |
| Document set | Interpretation Standard V1.0 |
| Status | DESIGN ONLY — not implemented |
| Version | 1.0.0 |
| Date | 2026-08-12 |
| Owner | BTE Interpretation Architecture |
| Runtime | None |

---

# 1. Purpose

This pack defines the **Interpretation Standard** for Day Master Strength.

It is the first domain instance of the architecture that every later interpretation pack must reuse:

- Pattern
- Useful God
- Ten Gods
- ShenSha
- Luck
- Career
- Marriage
- Health
- and all future interpretation domains

The goal is not to restate whether the Day Master is Strong or Weak.

The goal is to produce the reasoning a professional BaZi consultant would explain to a paying customer.

---

# 2. The Problem This Pack Solves

Current Report V1 produces **facts**.

Examples of facts:

- Strong
- Weak
- Useful God
- ShenSha
- Pattern

Facts are not interpretations.

A customer who reads “Strong” still asks:

> So what?

This pack converts:

```text
FACTS
  → REASONING
    → CONCLUSION
      → PRACTICAL ADVICE
```

---

# 3. Two Modes

Every interpretation has exactly two modes.

| Mode | Audience | Visible in commercial report |
|------|----------|------------------------------|
| **Mode A — Validation Mode** | Developers, auditors, consultants in review | Never |
| **Mode B — Customer Mode** | Paying customer | Always |

Both modes are projections of the **same Evidence Layer**.

They must never invent separate conclusions.

---

# 4. What This Pack Is

- A content architecture
- A writing contract
- A validation contract
- A reuse contract for all future interpretation packs
- The Strength domain instantiation of that contract

---

# 5. What This Pack Is Not

This pack is **not**:

- Production code
- A UI task
- A Report / PDF / DOCX task
- A change to Strength Engine
- A change to Interpretation Engine
- A change to Rule Database
- A change to Report Engine
- A sentence library of production templates
- A replacement of Strength scoring

Do not implement until this design is accepted.

---

# 6. Document Set

| File | Role |
|------|------|
| [README.md](README.md) | Pack index and non-goals |
| [INTERPRETATION_STANDARD.md](INTERPRETATION_STANDARD.md) | Platform-wide architecture; Strength is the first instance |
| [VALIDATION_MODE.md](VALIDATION_MODE.md) | Mode A contract |
| [CUSTOMER_MODE.md](CUSTOMER_MODE.md) | Mode B contract |
| [EVIDENCE_LAYER.md](EVIDENCE_LAYER.md) | Shared evidence between both modes |
| [RULE_TRACE.md](RULE_TRACE.md) | Why each activated rule fired |
| [CONFIDENCE_MODEL.md](CONFIDENCE_MODEL.md) | Confidence, explanation, and leakage rules |
| [ALTERNATIVE_ANALYSIS.md](ALTERNATIVE_ANALYSIS.md) | Competing classifications |
| [EXECUTIVE_SUMMARY_STANDARD.md](EXECUTIVE_SUMMARY_STANDARD.md) | 5–8 line customer close |
| [SENTENCE_STANDARD.md](SENTENCE_STANDARD.md) | Sentence form, SO WHAT, leak bans |
| [QUESTION_FRAMEWORK.md](QUESTION_FRAMEWORK.md) | Mandatory questions every interpretation must answer |
| [VALUE_FRAMEWORK.md](VALUE_FRAMEWORK.md) | One new value per paragraph |
| [EDGE_CASES.md](EDGE_CASES.md) | Strength and reusable edge cases |
| [TEST_STRATEGY.md](TEST_STRATEGY.md) | How future implementation will be tested |
| [ACCEPTANCE_CHECKLIST.md](ACCEPTANCE_CHECKLIST.md) | Binary design acceptance |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

# 7. Dependency Position

```text
Product Manifesto
        ↓
Experience Principles / Brand Language
        ↓
Strength Knowledge  →  Strength Engine  →  StrengthResult (FACTS)
        ↓
Interpretation Standard (THIS PACK)
        ├── Mode A  Validation Interpretation
        └── Mode B  Customer Interpretation
        ↓
Report Engine / Portal / Developer audit views
```

Higher layers win conflicts.

This pack does not recompute Strength.

This pack does not render reports.

---

# 8. Relationship to Existing Packs

| Existing pack | Relationship |
|---------------|--------------|
| Strength Knowledge / Strength Engine | Upstream facts. Unchanged. |
| Pack 04 Interpretation Engine | Future NLG runtime must **conform** to this standard. Not modified now. |
| Pack 05 Narrative Engine | Commercial story intent is absorbed and superseded **for interpretation content architecture**. Not modified now. |
| Pack 05 Report Engine | Downstream formatting only. Not modified now. |
| Reasoning Framework | Supplies graph/trace concepts for Mode A. Not modified now. |
| Sentence Library | Future authoring target. No production sentences are created here. |

Where a later implementation of Pack 04 or Narrative Engine conflicts with this standard on interpretation content, **this standard wins**.

Product Manifesto still wins on product philosophy.

---

# 9. Future Pack Contract

Every later interpretation pack MUST provide the same document roles:

1. Dual Mode A / Mode B
2. Shared Evidence Layer
3. Rule Trace
4. Confidence Model
5. Alternative Analysis
6. Question Framework answers
7. Value Framework compliance
8. Sentence Standard compliance
9. Edge cases
10. Test strategy
11. Acceptance checklist

A pack that only outputs a label (Pattern name, Useful God name, ShenSha name) is **not** an interpretation pack.

---

# 10. Strength Scope

In scope for PACK-01:

- Day Master strength classification
- Why that classification holds
- What it means for this person
- Advantages and challenges
- Life-domain influence
- How luck cycles support or weaken the Day Master
- What to do and what to avoid
- Developer-visible evidence, trace, confidence, alternatives, missing data, conflicts

Out of scope:

- Recalculating strength scores
- Determining Pattern, Useful God, Ten Gods, or ShenSha
- Rendering HTML / PDF / DOCX
- Authoring production sentence IDs
- Changing Rule Database content

---

# 11. Source of Truth

| Question | Owner |
|----------|-------|
| Is the Day Master Strong / Weak / Balanced / …? | Strength Engine (fact) |
| Why did rules fire? | Evidence Layer + Rule Trace (this pack) |
| What should the customer understand and do? | Customer Mode (this pack) |
| How is the page or PDF laid out? | Report Engine / Portal (later) |

Interpretation never changes the analytical conclusion.

Interpretation explains it.

---

# 12. Status

**DESIGN COMPLETE. IMPLEMENTATION FORBIDDEN until this pack is accepted.**

---

END
