# BETA0 Narrative Lock

| Field | Value |
|-------|-------|
| Document | BETA0_NARRATIVE_LOCK |
| Date | 2026-08-17 |
| Status | **FROZEN** |
| Owner | Interpretation Foundation + Product Owner |
| Production composer | Narrative Composer V2 |

---

## Final narrative pipeline

This is the only supported narrative path for Beta:

```
Decision
    ↓
State
    ↓
Relationship
    ↓
Knowledge
    ↓
Narrative Composer
    ↓
Published Narrative
    ↓
Professional Publisher
    ↓
PDF
```

Decision, State, Relationship, and Knowledge are **inputs**.
Narrative Composer is the **only** composer of customer sentences.
Published Narrative **selects** what may leave the composer (PUBLISH / DROP / APPENDIX).
Professional Publisher **editions** already-composed evidence.
PDF is **format**, not interpretation.

---

## Owners on the pipeline

| Stage | Owner | Location |
|-------|-------|----------|
| Decision / State / Relationship | Decision, Analysis, Luck, Interpretation foundation | Existing engine results and interpretation bundles |
| Knowledge | Knowledge Board | Rule DB + packages |
| Narrative Composer | Interpretation Engine | Narrative Composer V2 |
| Published Narrative | Publish package | `PublishedNarrativeBuilder` (PNB001) |
| Professional Publisher | Publish package | `ProfessionalReportPublisher` (PUBLISH01) |
| PDF | Report Engine commercial | `CommercialReportBuilder` → HTML → PDF |

Pack 05 `NarrativeEngine` remains a compatibility fallback only.
It is not the Beta production composer.
It must not be expanded into a second narrative system.

---

## What Narrative may not do

- Calculate Calendar, BaZi, Strength, Pattern, Useful God, Ten Gods, Shen Sha, Luck, Temperature, or Five Elements
- Invent a second composer
- Dump glossary or encyclopedia into consultation editions
- Rewrite knowledge records into a new canon

---

## Explicit prohibition

During Beta, do **not** add:

- a new Narrative system
- a Story Engine
- a Case Identity Engine
- a second Composer
- a second Published Narrative builder

Narrative Improvement inside Composer V2 and existing publish policy is Product / Editorial work, not a new system.

---

## Official status

**Narrative pipeline is frozen for Beta 0.**
