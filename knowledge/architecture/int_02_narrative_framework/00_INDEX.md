# INT-02 Narrative Framework — Index

| Field | Value |
|-------|--------|
| Epic | INT-02 Narrative Improvement |
| Sprint | INT-02A Narrative Framework |
| Version | 1.0.0 |
| Status | Architecture freeze (contracts only) |
| Runtime | None |

---

## Purpose

Define one reusable Narrative Framework for every analytical topic.

This sprint is architecture only.

It does not change engines, identity, workspace, report, PDF, DOCX, or UI.

---

## Documents

| File | Contents |
|------|----------|
| `01_NARRATIVE_ARCHITECTURE.md` | Position, boundaries, consumers |
| `02_FRAMEWORK.md` | Five blocks, template hierarchy, sentence ownership |
| `03_CONTRACTS.md` | Topic / block / sentence contracts |
| `04_COMPOSITION_PIPELINE.md` | Composition order |

Python freeze (no engine runtime):

`engines/narrative_framework/`

Tests:

`tests/narrative_framework/`

---

## Required topic narrative

```
Observation
    ↓
Reasoning
    ↓
Impact
    ↓
Recommendation
    ↓
Conclusion
```

---

## Relationship to frozen packs

| Pack | Role relative to INT-02 |
|------|-------------------------|
| Analytical engines | Own facts. Do not author customer prose. |
| Pack 04 Interpretation | May select sentences later. Unchanged in INT-02A. |
| Pack 05 Narrative Engine | Chart-level commercial story. Consumes topic units later. Unchanged in INT-02A. |
| Identity | Publishes section ids. Unchanged in INT-02A. |
| Workspace / Report | Display consumers. Unchanged in INT-02A. |

---

## Stop

Do not start INT-02B (topic application) until this framework is accepted.

---

END
