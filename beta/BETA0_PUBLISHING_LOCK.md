# BETA0 Publishing Lock

| Field | Value |
|-------|-------|
| Document | BETA0_PUBLISHING_LOCK |
| Date | 2026-08-17 |
| Status | **FROZEN** |
| Owner | Report Engine + Interpretation publish package |
| Default production edition | **executive** |

Publishing is edition policy.
It is not astrology.
It is not narrative generation.
It is not knowledge rewrite.

---

## Frozen publication stack

```
Narrative Composer V2
    ↓
Published Narrative Builder     (PUBLISH / DROP / APPENDIX)
    ↓
Professional Report Publisher   (edition: executive | professional | appendix)
    ↓
CommercialReportBuilder
    ↓
HTML / PDF
    ↓
Portal
```

Production choke point: `publication_edition` on the narrative result / production request.
Default remains **executive**.

---

## Edition ownership

| Edition | Owner | Role |
|---------|-------|------|
| Executive | Professional Report Publisher | Default customer consultation |
| Professional | Professional Report Publisher | Same analytical truth; more already-composed evidence |
| Appendix | Professional Report Publisher | Glossary / encyclopedia; not the consultation |

No fourth edition may be added without Product Owner approval.

---

## Report formatting

| Surface | Owner | Location |
|---------|-------|----------|
| Commercial builder | Report Engine | `engines/report_engine/commercial/builder.py` |
| HTML renderer | Report Engine | `engines/report_engine/commercial/html_renderer.py` |
| PDF exporter | Report Engine | `engines/report_engine/commercial/` |
| Production orchestration | Application | `applications.production.ProductionEndToEndOrchestrator` |

Report Engine formats. It does not decide Useful God, Pattern, or customer meaning.

---

## What Publishing may not do

- Recalculate engine truth
- Compose new customer sentences
- Put Ten Gods encyclopedia or unmatched Shen Sha into Executive / Professional
- Change default production away from Executive without Product Owner approval

---

## Explicit prohibition

During Beta, do **not** add:

- a new Publisher
- a new PDF product line
- a new report architecture
- a new edition besides executive / professional / appendix

---

## Official status

**Publishing ownership and edition set are frozen for Beta 0.**
