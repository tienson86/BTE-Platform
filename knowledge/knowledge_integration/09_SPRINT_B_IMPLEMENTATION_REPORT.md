# 09 — Sprint B Implementation Report

Version: 1.0  
Status: **EPIC 4 · SPRINT B COMPLETE — awaiting Product Review**  
Date: 2026-08-08  
Epic: Knowledge Integration  
Wave: W-P0-1.1-CORE only  

---

## 1. Summary

Sprint B implemented the **first production integration** of Wave 1.1 Golden Baseline Knowledge Units via a new `engines/commercial_knowledge` package.

Commercial Knowledge Adapter retrieves only the allow-listed five units, builds a `CommercialKnowledgeBundle` (no raw KU dump), merges advisory text into Narrative inputs, and attaches the serialized bundle on NarrativeResult for Portal provenance.

**Analytical meaning is unchanged.** Interpretation Engine, Narrative architecture, Foundation, Design System, Rule Database, Knowledge Model, and Wave 1.1 CSV content were not redesigned or rewritten.

---

## 2. Deliverables

### 2.1 Runtime package — `engines/commercial_knowledge/`

| File | Role |
|------|------|
| `models.py` | Contract ids, Wave 1.1 allow-list, Bundle / Payload dataclasses |
| `signal_projection.py` | Analysis → signals; condition eval; placeholder bind |
| `retrieval_service.py` | CSV load; allow-list / condition / confidence / dedupe |
| `bundle_builder.py` | Assemble Bundle + NarrativeKnowledgePayload; `bundle_to_dict` |
| `commercial_bundle.py` | Bundle helper re-exports |
| `commercial_adapter.py` | Public Adapter entrypoint |
| `narrative_merge.py` | Enrich analysis/interpretation (append/soft-enrich only) |
| `__init__.py` | Public exports |

### 2.2 Pipeline wiring (minimal)

| Location | Change |
|----------|--------|
| `applications/api/services/narrative_result_truth.py` | Adapter → enrich → `compose_narrative_result`; attach `commercial_knowledge_bundle` |
| `engines/narrative_engine/composer/source_factory.py` | Additive read of `useful_god.commercial_recommendation` for action evidence raw_text |

Orchestrator Stage 11 still calls `build_narrative_result_dict` unchanged.

### 2.3 Tests — `tests/commercial_knowledge/`

| File | Focus |
|------|-------|
| `test_allow_list.py` | Only KU-ID/ST/WK/UG/RC-001 |
| `test_bundle.py` | Bundle fields; no raw KU leak |
| `test_adapter.py` | Adapt / UG+RC drop / dedupe / technical filter |
| `test_traceability.py` | Chain + per-item provenance |
| `test_integration.py` | Enrich-without-replace; API attach |

### 2.4 Reports

| File | Role |
|------|------|
| `09_SPRINT_B_IMPLEMENTATION_REPORT.md` | This report |
| `10_SPRINT_B_VALIDATION_REPORT.md` | Validation gates |
| `11_BEFORE_AFTER_COMPARISON.md` | Exec / Rec comparison |

---

## 3. Pipeline (implemented)

```
Knowledge Units (21_knowledge_units.csv)
        ↓ allow-list Wave 1.1
CommercialKnowledgeAdapter
        ↓
CommercialKnowledgeBundle (+ NarrativeKnowledgePayload)
        ↓ enrich_narrative_inputs
Narrative Runtime → Composer
        ↓
NarrativeResult (+ commercial_knowledge_bundle)
        ↓
API → Portal Adapter → Result Page
```

---

## 4. Allow-list

Only:

- `KU-ID-001`
- `KU-ST-001`
- `KU-WK-001`
- `KU-UG-001`
- `KU-RC-001`

All other corpus rows are ignored (`not_in_wave_1_1_allow_list`).

**Product note:** Units remain `awaiting_review` in CSV. Sprint B retrieves by **id allow-list** (Wave 1.1 production gate requested by this sprint), not by publish workflow. Formal Publish remains HOLD for Product Review.

---

## 5. Bundle contract

Bundle exposes: identity, strengths, weaknesses, useful_god, recommendations, warnings, opportunities, confidence, selected_units, dropped_units, traceability, metadata.

Bundle **does not** expose raw KU fields (`modern_interpretation`, `author_notes`, `condition`, etc.).

---

## 6. Enrichment policy

| Target | Behavior |
|--------|----------|
| Executive Summary | Identity / Strength / Weakness / Useful God cores enrich observation/reasoning paths |
| Recommendation | Core Recommendation (`KU-RC-001`) supplies action prose; analytical code retained as `analytical_recommendation` when short enum-like |
| Interpretation | Sections append-only (`ck-{KU-ID}`); baseline sections preserved |
| Scores / grades | Untouched |

---

## 7. Explicit non-work (STOP)

Not started / not done:

- Wave 1.2  
- Knowledge authoring / editing / review / publish workflow  
- Report Engine  
- New UI / Design System / Foundation  
- Narrative redesign / Interpretation redesign  
- Rule Database / Knowledge Model / Wave 1.1 content edits  

---

## 8. Files changed (source)

```
engines/commercial_knowledge/*          (new)
applications/api/services/narrative_result_truth.py
engines/narrative_engine/composer/source_factory.py  (minimal additive)
tests/commercial_knowledge/*            (new)
knowledge/knowledge_integration/09–11   (new)
knowledge/knowledge_integration/00_INTEGRATION_INDEX.md (Sprint B status)
```

Wave 1.1 CSV content: **unchanged**.

---

## 9. Stop line

Sprint B implementation complete.  
**Wait for Product Review. Do not start Wave 1.2.**

---

END
