# Expert Translation

| Field | Value |
|-------|-------|
| Module | expert_translation |
| Version | 1.0.0 |
| Status | Official |
| Pipeline | R2 |

---

## Purpose

Translate machine reasoning into expert reasoning **before** Narrative Composer.

This module does not calculate astrology, change decisions, or rewrite knowledge.

---

## Pipeline

```text
Engine Truth
        ↓
Decision / State / Relationship
        ↓
Knowledge
        ↓
Expert Translation Rules   ← this module
        ↓
Narrative Composer
        ↓
Customer Report
```

---

## Files

| File | Role |
|------|------|
| `TRANSLATION_RULE_SPEC.md` | Rule contract |
| `translation_rules.json` | Deterministic replacement rules |
| `confidence_bands.json` | Score → expert band |
| `forbidden_terms.json` | Customer-text leak detector |

---

## Consumers

- `engines/interpretation_engine/foundation/narrative/translation`
- Narrative Composer V2
- Golden regression for CASE-0001 / Nguyễn Tiến Sơn / Lương Ngọc Huỳnh
