# CK-01D — Composer Integration

Canonical copy lives with the CK-01 series:

`knowledge/architecture/ck_01_consulting_knowledge/07_COMPOSER_INTEGRATION.md`

This file is the Product Owner entry for CK-01D.

---

## Purpose

Integrate matched Consulting Knowledge Units into the commercial Composer.

---

## Architecture

```
Matched Knowledge Units
        ↓
compose_commercial_consulting
        ↓
CommercialComposerResult
```

Catalog ≠ Matcher ≠ Composer ≠ Renderer.

Composer does not rematch. Orchestrator calls matcher first.

---

## Input contract

`CommercialComposerInput(matched_units, analysis)`

`matched_units` keep canonical catalog order. `analysis` is not used to rematch.

---

## Output contract

`CommercialComposerResult` with domain sections:

`domain`, `title`, `summary`, `meaning`, `recommendations`, `references`, `source_unit_ids`

---

## Composition rules

Canonical domain order. Customer wording from catalog. Meaning copied, not rewritten. Actions deduped by exact text, first occurrence kept. No new recommendations.

---

## Traceability

Every section has non-empty `source_unit_ids`.

---

## Determinism

Same matched units + same catalog → same result.

---

## Runtime path

`OrchestratorService._finalize_public_payload`

→ `publish_commercial_consulting` (match then compose)

→ `payload["commercial_consulting"]`

→ optional `ReportInputV1.commercial_consulting`

---

## Tests

`tests/commercial_composer/test_ck01d_composer_integration.py`

---

## Known exclusions

No engine, catalog, UI, PDF/DOCX, or LLM changes. No CK-01E.

---

END
