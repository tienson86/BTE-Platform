# PACK-01 — Strength Reasoning Engine Design

| Field | Value |
|-------|-------|
| Pack | PACK-01 |
| Domain | Strength (Thân Vượng / Thân Nhược) |
| Layer | Reasoning Engine |
| Version | 1.0.0 |
| Status | DESIGN ONLY |
| Date | 2026-08-12 |

---

# 1. Purpose

This pack designs the **Reasoning Engine** for PACK-01 Strength **before** production implementation.

The engine sits between selected interpretation knowledge and sentence composition:

```text
Interpretation Knowledge
        ↓
Knowledge Selection (eligibility)
        ↓
Reasoning Engine          ← this pack
        ↓
NarrativePlan
        ↓
Sentence Composer
        ↓
Customer / Validation Interpretation
```

It decides **what is worth saying**, not what the Strength class is, and not the final wording.

---

# 2. What the Reasoning Engine does

It answers:

- which knowledge is worth saying
- which knowledge should stay silent
- what is most important
- what is only supporting
- presentation order
- emphasis
- when to warn
- when to keep the conclusion cautious
- when content belongs in Validation Mode instead of Customer Mode

---

# 3. What it does not do

- Recalculate Thân vượng / nhược
- Change Strength Class
- Invent missing facts
- Write final customer sentences
- Call an LLM
- Edit Rule Database
- Author new knowledge
- Render reports / UI / PDF

---

# 4. Document set

| File | Owns |
|------|------|
| [README.md](README.md) | Index |
| [REASONING_ENGINE_ARCHITECTURE.md](REASONING_ENGINE_ARCHITECTURE.md) | Position, stages, reuse |
| [INPUT_CONTRACT.md](INPUT_CONTRACT.md) | `ReasoningInput` |
| [KNOWLEDGE_UNIT_METADATA.md](KNOWLEDGE_UNIT_METADATA.md) | Unit fields and enums |
| [EVIDENCE_GATE.md](EVIDENCE_GATE.md) | eligible / ineligible / partial |
| [RELEVANCE_MODEL.md](RELEVANCE_MODEL.md) | RelevanceScore |
| [SALIENCE_MODEL.md](SALIENCE_MODEL.md) | What is worth saying most |
| [PRIORITY_MODEL.md](PRIORITY_MODEL.md) | Rule vs knowledge vs narrative |
| [NARRATIVE_BUDGET.md](NARRATIVE_BUDGET.md) | Caps |
| [REASONING_CHAIN.md](REASONING_CHAIN.md) | Fact → action |
| [NARRATIVE_PLAN.md](NARRATIVE_PLAN.md) | Output schema |
| [DOMAIN_ORDERING.md](DOMAIN_ORDERING.md) | Default order + question_context |
| [DUPLICATE_REASONING.md](DUPLICATE_REASONING.md) | Information gain |
| [CONFLICT_REASONING.md](CONFLICT_REASONING.md) | Conflict vs nuance |
| [CONFIDENCE_REASONING.md](CONFIDENCE_REASONING.md) | Language strength |
| [ALTERNATIVE_REASONING.md](ALTERNATIVE_REASONING.md) | Runner-up class |
| [MISSING_DATA_POLICY.md](MISSING_DATA_POLICY.md) | Absence is not evidence |
| [CLAIM_TRACEABILITY.md](CLAIM_TRACEABILITY.md) | ClaimTrace |
| [REASON_CODES.md](REASON_CODES.md) | Machine-readable reasons |
| [TRANSITION_INTENT.md](TRANSITION_INTENT.md) | Intent vs wording |
| [EXECUTIVE_SUMMARY_PLANNING.md](EXECUTIVE_SUMMARY_PLANNING.md) | Claim set, not sentences |
| [NARRATIVE_COMPRESSION.md](NARRATIVE_COMPRESSION.md) | Too many claims |
| [NARRATIVE_EXPANSION.md](NARRATIVE_EXPANSION.md) | Too few claims |
| [DETERMINISM.md](DETERMINISM.md) | Same in → same plan |
| [VERSIONING.md](VERSIONING.md) | Version fields |
| [EDGE_CASES.md](EDGE_CASES.md) | EC-01 … EC-10 |
| [ANTI_PATTERNS.md](ANTI_PATTERNS.md) | Forbidden habits |
| [CASE_0001_WALKTHROUGH.md](CASE_0001_WALKTHROUGH.md) | Review fixture |
| [TEST_STRATEGY.md](TEST_STRATEGY.md) | Future tests |
| [ACCEPTANCE_CHECKLIST.md](ACCEPTANCE_CHECKLIST.md) | Design PASS/FAIL |
| [CHANGELOG.md](CHANGELOG.md) | History |

---

# 5. Relationship to other packs

| Pack | Relationship |
|------|----------------|
| Interpretation Standard | HOW to say it (Mode A/B, leak ban) |
| Interpretation Knowledge | WHAT can be said |
| Prototype | First integration sketch; this pack is the reasoning layer that prototype implied |
| Knowledge Reasoning Framework (`knowledge/reasoning/`) | How facts justify an **analytical** conclusion graph — different job |
| Sentence Composer | Renders `NarrativePlan` into sentences |
| Strength Engine | Publishes facts only |

This pack does **not** modify the prototype, knowledge base, or engines.

---

# 6. Review gate

`CASE_0001_WALKTHROUGH.md` is the document to review first.

No production implementation until that walkthrough is accepted.

---

# 7. Status

**DESIGN ONLY. NO PRODUCTION CODE.**

---

END
