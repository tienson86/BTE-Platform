# CK-01 Consulting Knowledge — Index

| Field | Value |
|-------|--------|
| Epic | CK-01 Consulting Knowledge Engine |
| Sprint | CK-01D Composer Integration |
| Version | 1.0.0 |
| Status | Catalog freeze + matching runtime + composer integration |
| Runtime | Match then compose. Composer does not rematch. No LLM. |

---

## Purpose

Design the Consulting Knowledge Platform.

It is not an analytical engine. It is not an LLM. It is not a Report engine.

It is a deterministic consulting knowledge base: published truth is matched to consulting units.

---

## Documents

| File | Contents |
|------|----------|
| `01_ARCHITECTURE.md` | Position, boundaries, consumers |
| `02_DOMAINS.md` | Frozen consulting domains |
| `03_KNOWLEDGE_UNIT.md` | Unit model and required fields |
| `04_MATCHING_PIPELINE.md` | Match order, no calculation |
| `05_CATALOG.md` | Deterministic catalog entries (CK-01B) |
| `06_MATCHING_RUNTIME.md` | Signal matching runtime (CK-01C) |
| `07_COMPOSER_INTEGRATION.md` | Matched units → commercial composer (CK-01D) |

Python freeze:

`engines/consulting_knowledge/`

Tests:

`tests/consulting_knowledge/`

---

## Pipeline

```
Integrated Narrative
Identity
Canonical Analysis Result
        ↓
Match signals (read-only)
        ↓
Condition match
        ↓
Consulting Knowledge Units
```

---

## Relationship to frozen layers

| Layer | Role relative to CK-01 |
|------|-------------------------|
| Analytical engines | Own facts. Unchanged. Knowledge never calls them. |
| INT-02 Integrated Narrative | Frozen input. Read only. |
| Identity | Frozen input. Read only. |
| Pack 05 / Report / PDF / DOCX | Unchanged. Not wired in CK-01A. |
| Workspace | Unchanged. |

---

## Stop

CK-01D composes commercial consulting from matched units. Do not change Portal UI, PDF, or DOCX until a later sprint. Do not start CK-01E.

---

END
