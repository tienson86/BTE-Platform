# INT-03 Commercial Composer — Index

| Field | Value |
|-------|--------|
| Epic | INT-03 Commercial Composer |
| Sprint | INT-03A Commercial Composition Framework |
| Version | 1.0.0 |
| Status | Architecture freeze |
| Runtime | Composition only (no engine, no LLM) |

---

## Purpose

Define the canonical Commercial Composer.

```
IntegratedNarrativeUnit
        ↓
Commercial Composer
        ↓
CommercialNarrativeUnit
```

This sprint is framework plus a faithful mapper.

It does not change engines, Identity, Integrated Narrative source, Workspace, Report, PDF, or DOCX.

---

## Documents

| File | Contents |
|------|----------|
| `01_ARCHITECTURE.md` | Position, boundaries, consumers |
| `02_FRAMEWORK.md` | Seven commercial sections |
| `03_CONTRACTS.md` | CommercialNarrativeUnit |
| `04_COMPOSITION_RULES.md` | Allowed operations, source map, traceability (INT-03A freeze) |
| `05_COMMERCIAL_COMPOSITION_RULES.md` | INT-03B editorial rules. No runtime. |

Python:

`engines/commercial_composer/`

Tests:

`tests/commercial_composer/`

---

## Required commercial sections

```
Executive Summary
    ↓
Overall Reading
    ↓
Current Situation
    ↓
Main Strengths
    ↓
Main Risks
    ↓
Key Recommendation
    ↓
Conclusion
```

---

## Relationship to frozen layers

| Layer | Role relative to INT-03 |
|------|-------------------------|
| Analytical engines | Unchanged. Composer never calls them. |
| INT-02 Integrated Narrative | Frozen input. Read only. |
| Pack 05 NarrativeResult | Separate commercial contract. Unchanged in INT-03A. |
| Workspace | Unchanged. Still consumes Integrated Narrative. |
| Report / PDF / DOCX | Unchanged. Not wired in INT-03A. |

---

## Stop

Do not wire Commercial Narrative into Report, PDF, DOCX, or Workspace until this framework is accepted.

---

END
