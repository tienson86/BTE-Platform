# PACK-01 Prototype — Strength Interpretation Pipeline

| Field | Value |
|-------|-------|
| Pack | PACK-01 Prototype |
| Domain | Strength only |
| Location | `knowledge/prototypes/PACK_01_PROTOTYPE/` |
| Version | 1.0.0 |
| Status | PROTOTYPE DESIGN — not production |
| Date | 2026-08-12 |

---

# 1. Purpose

This folder is the **first integration** of:

1. Strength Facts (published by Strength Engine / Rule Database — read only)
2. Interpretation Standard (how to say it)
3. Interpretation Knowledge (what to say)

into one complete interpretation pipeline.

It is the reference prototype for later packs:

Pattern, Useful God, Ten Gods, ShenSha, Luck, Career, Marriage.

---

# 2. What this is

A documented, deterministic prototype of:

```text
Facts
  → Evidence Layer
    → Interpretation Standard
      → Interpretation Knowledge
        → Sentence Composer
          → Final Interpretation (Mode A + Mode B)
```

It demonstrates **knowledge-unit selection**, not a pile of hard-coded customer sentences.

The only worked example is **CASE-0001**.

---

# 3. What this is not

- Not production code
- Not a change to the production pipeline
- Not a Rule Database edit
- Not a Strength algorithm edit
- Not Report Engine / UI / PDF
- Not more knowledge authoring
- Not an LLM rewrite
- Not a real customer report

Do not copy this folder into `engines/`.

---

# 4. Document set

| File | Role |
|------|------|
| [README.md](README.md) | This index |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Layers and boundaries |
| [RUNTIME_PIPELINE.md](RUNTIME_PIPELINE.md) | Stage-by-stage run |
| [KNOWLEDGE_SELECTION.md](KNOWLEDGE_SELECTION.md) | How units are selected and rejected |
| [SENTENCE_COMPOSER.md](SENTENCE_COMPOSER.md) | How units become paragraphs |
| [MODE_A_OUTPUT.md](MODE_A_OUTPUT.md) | Validation projection |
| [MODE_B_OUTPUT.md](MODE_B_OUTPUT.md) | Customer projection |
| [TRANSITION_ENGINE.md](TRANSITION_ENGINE.md) | Structural transitions |
| [DUPLICATE_REMOVAL.md](DUPLICATE_REMOVAL.md) | One idea, one place |
| [CONFLICT_RESOLUTION.md](CONFLICT_RESOLUTION.md) | Disagreement handling |
| [PRIORITY_MODEL.md](PRIORITY_MODEL.md) | Order and keep/drop |
| [EXAMPLE_CASE_0001.md](EXAMPLE_CASE_0001.md) | Full traced run |
| [OUTPUT_SPECIFICATION.md](OUTPUT_SPECIFICATION.md) | Dual-mode output contract |
| [TEST_PLAN.md](TEST_PLAN.md) | How to test a future implementation |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

# 5. Input (only Strength Facts)

The prototype consumes nothing except published Strength facts, for example:

- Strength class
- Strength score
- Season support
- Root support
- Supporting factors
- Weakening factors
- Evidence
- Rule trace
- Confidence

It does not consume Pattern, Useful God, Temperature, Ten Gods, ShenSha, gender tokens, or luck unless luck is published **as a Strength-interaction fact**. For CASE-0001, public luck is not published.

---

# 6. Output

Two projections from one Evidence Layer:

- **Mode A** Validation
- **Mode B** Customer

See [OUTPUT_SPECIFICATION.md](OUTPUT_SPECIFICATION.md).

---

# 7. Hard-coded text ban

The prototype must not “know” CASE-0001 sentences in advance.

It must show:

1. Which knowledge units were selected
2. Why they were selected
3. Why others were rejected
4. How duplicates were removed
5. How contradictions were handled
6. How transitions were created
7. How the final narrative was ordered

Composed paragraphs in the example are **outputs of that process**, with provenance, not authored report copy.

---

# 8. Status

**PROTOTYPE COMPLETE. NO PRODUCTION IMPLEMENTATION.**

---

END
