# Translation Rule Specification

| Field | Value |
|-------|-------|
| Document ID | BTE-ET-001 |
| Version | 1.0.0 |
| Status | Official |

---

## Contract

Every rule is a `TranslationRule`:

| Field | Required | Meaning |
|-------|----------|---------|
| id | yes | Immutable rule id |
| source_pattern | yes | Regular expression |
| target_pattern | yes | Deterministic replacement |
| scope | yes | Translation category |
| priority | yes | Higher applies first |
| examples | yes | `[[source, target], ...]` |
| notes | no | Why the rule exists |

Rules are deterministic. No LLM rewriting.

---

## Categories

- `engine_terms`
- `ranking_terms`
- `confidence_terms`
- `rule_terms`
- `candidate_terms`
- `debug_terms`
- `relationship_terms`
- `knowledge_terms`

---

## Invariants

1. Do not change selected decisions.
2. Do not remove evidence / engine_truth_ref / bundle ids.
3. Do not expose rule ids, scores, or debug tokens in customer text.
4. Domain-neutral: no Useful God / Pattern / Strength hardcoding.
5. Debug mode may bypass translation.
