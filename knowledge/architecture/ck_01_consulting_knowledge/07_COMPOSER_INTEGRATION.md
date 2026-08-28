# 07 — Composer Integration

| Field | Value |
|-------|--------|
| Document | CK-01D Consulting Knowledge Composer Integration |
| Version | 1.0.0 |
| Status | Canonical for CK-01D |
| Catalog id | `bte.consulting.knowledge.catalog.v1` |

---

## Purpose

Feed already-matched Consulting Knowledge Units into the commercial Composer.

Composer creates commercial consulting sections. It does not match. It does not calculate. It does not invent wording.

---

## Architecture

```
Canonical Analysis
        ↓
Consulting Knowledge Context
        ↓
Knowledge Matching          (CK-01C, orchestrator)
        ↓
Matched Knowledge Units
        ↓
Commercial Composer         (CK-01D, this sprint)
        ↓
Commercial Consulting Sections
        ↓
Report / Portal consumer    (structured field only)
```

Separation:

```
Knowledge Catalog  ≠  Knowledge Matcher  ≠  Commercial Composer  ≠  Renderer
```

Canonical consulting composition path:

`compose_commercial_consulting`

INT-03 `compose_commercial_narrative` remains the Integrated Narrative editorial path. It is not replaced.

---

## Input contract

`CommercialComposerInput`

| Field | Role |
|-------|------|
| `matched_units` | Frozen catalog units already matched. Canonical order kept. |
| `analysis` | Opaque published context. Not used to rematch. |

Composer does not call `match_consulting_knowledge` or `match_published_knowledge`.

---

## Output contract

`CommercialComposerResult.sections` of `CommercialConsultingSection`

| Field | Source |
|-------|--------|
| `domain` | Canonical consulting domain |
| `title` | Canonical domain title |
| `summary` | Deduped customer wording |
| `meaning` | Deduped consulting meaning |
| `recommendations` | Deduped recommended actions |
| `references` | Deduped references |
| `source_unit_ids` | Catalog `unit_id` list, required |

No HTML blob. No engine ids. No raw conditions.

---

## Composition rules

- Group by `CONSULTING_DOMAINS` order. Do not sort alphabetically.
- Copy catalog wording. Do not rewrite meaning.
- `stable_unique`: first occurrence wins.
- Do not add recommendations outside the catalog.

---

## Traceability

Every published section cites `source_unit_ids`.

```
Commercial statement → knowledge unit → canonical condition
```

A section without source ids is invalid.

---

## Determinism

Same matched unit set + same catalog version → same `CommercialComposerResult`.

No random. No timestamp copy. No LLM. No network.

---

## Empty-state

Unmatched domains are omitted.

No matched units → empty result, status `insufficient`. No generic astrology advice.

---

## Runtime path

Orchestrator:

```
publish_integrated_narrative
        ↓
publish_commercial_consulting
    match_published_knowledge
            ↓
    compose_commercial_consulting
        ↓
payload["commercial_consulting"]
```

Report: optional `ReportInputV1.commercial_consulting`. Omitted when absent so existing snapshots stay stable. Not rendered to HTML/PDF/DOCX in CK-01D.

---

## Tests

`tests/commercial_composer/test_ck01d_composer_integration.py`

D1 accept matched units, D2 domain grouping, D3 determinism, D4 stable dedupe, D5 traceability, D6 empty, D7 no rematch, D8 no catalog mutation, D9 report adapter.

---

## Known exclusions

- Catalog content frozen (CK-01B)
- No Calendar / Bazi / Strength / Useful God / Luck change
- No Portal UI
- No PDF / DOCX layout
- No LLM
- No CK-01E

---

END
