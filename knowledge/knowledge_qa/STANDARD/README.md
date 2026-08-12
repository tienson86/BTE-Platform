# Knowledge QA Standard — BTE Platform

| Field | Value |
|-------|-------|
| Layer | Platform Standard |
| Version | 1.0.0 |
| Status | Official |
| Scope | All Interpretation Knowledge |
| Date | 2026-08-12 |

---

# 1. What this is

This directory is the **official Knowledge QA Standard** for the BTE Platform.

Every Interpretation Knowledge pack, catalog, and future pack **must follow this standard**.

Future packs **must not redefine QA**. They reference this standard only.

This standard does **not** replace:

- Rule Database
- Interpretation Standard
- Knowledge Catalog schema (per pack)
- Reasoning Engine design
- Report Engine

It governs **how knowledge is reviewed before production use**.

---

# 2. Document set

| File | Owns |
|------|------|
| [KNOWLEDGE_QA_STANDARD.md](KNOWLEDGE_QA_STANDARD.md) | Master standard — all sections |
| [QA_CRITERIA.md](QA_CRITERIA.md) | Twelve frozen criteria |
| [QA_SCORING.md](QA_SCORING.md) | 0–10 scoring anchors |
| [QA_WORKFLOW.md](QA_WORKFLOW.md) | End-to-end QA workflow |
| [UNIT_LIFECYCLE.md](UNIT_LIFECYCLE.md) | Draft → Reviewed → Validated → Frozen → Deprecated |
| [REVIEW_PROCESS.md](REVIEW_PROCESS.md) | Roles and review flow |
| [PASS_REVIEW_FAIL.md](PASS_REVIEW_FAIL.md) | Verdicts and thresholds |
| [DUPLICATE_POLICY.md](DUPLICATE_POLICY.md) | Duplicate taxonomy and rules |
| [CROSS_PACK_POLICY.md](CROSS_PACK_POLICY.md) | Pack isolation and dependencies |
| [EXPLAINABILITY_STANDARD.md](EXPLAINABILITY_STANDARD.md) | So what and removal test |
| [COMMERCIAL_QUALITY_STANDARD.md](COMMERCIAL_QUALITY_STANDARD.md) | Paying-customer readiness |
| [ACTIONABILITY_STANDARD.md](ACTIONABILITY_STANDARD.md) | Fact → interpretation → action |
| [EVIDENCE_STANDARD.md](EVIDENCE_STANDARD.md) | Published-facts-only rule |
| [TRACEABILITY_STANDARD.md](TRACEABILITY_STANDARD.md) | Audit chain |
| [CONSISTENCY_STANDARD.md](CONSISTENCY_STANDARD.md) | Knowledge / Reasoning / Narrative alignment |
| [FREEZE_POLICY.md](FREEZE_POLICY.md) | When a unit may become Frozen |
| [QA_CHECKLIST.md](QA_CHECKLIST.md) | Pre-validation checklist |
| [QA_TEMPLATE.md](QA_TEMPLATE.md) | Standard review template |
| [QA_EXAMPLES.md](QA_EXAMPLES.md) | PACK-01 examples only |
| [CHANGELOG.md](CHANGELOG.md) | Standard history |

---

# 3. Pack reviews

Pack-specific phase reviews live under:

```text
knowledge/knowledge_qa/PACK_XX_<DOMAIN>/
```

Example: `knowledge/knowledge_qa/PACK_01_STRENGTH/PHASE_01_MEANING_REVIEW.md`

Pack reviews **apply** this standard. They do not override it.

---

# 4. Who uses this

| Role | Uses |
|------|------|
| Author | QA_CHECKLIST before submission |
| QA Assistant (including Cursor) | QA_TEMPLATE, QA_CRITERIA, scoring — **not final authority** |
| Domain Reviewer | REVIEW_PROCESS, PASS_REVIEW_FAIL |
| Governance | FREEZE_POLICY, UNIT_LIFECYCLE |

---

# 5. Non-goals

- Not runtime code
- Not Reasoning Engine implementation
- Not catalog schema definition (per-pack catalogs conform to pack schema **and** this QA standard)
- Not modification of existing knowledge during QA

---

END
