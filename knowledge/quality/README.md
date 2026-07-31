# BTE Knowledge Quality — Specification

**Sprint:** 3C  
**Location:** `knowledge/quality/`  
**Status:** Specification only (no scoring engine runtime)

---

## Purpose

Defines canonical quality metrics, review checklist, academic/technical/governance scorecards, and the golden-record promotion checklist for Knowledge Records.

Does not score live records, modify golden datasets, or change authored Knowledge Records.

---

## Folder tree

```text
knowledge/quality/
├── README.md
├── quality_metrics.json
├── review_checklist.json
├── academic_scorecard.json
├── technical_scorecard.json
├── governance_scorecard.json
├── golden_record_checklist.json
└── examples/
    └── quality_evaluation_example.json
```

---

## Scoring dimensions

| Metric ID | Name |
|-----------|------|
| QM-COMPLETENESS | Completeness |
| QM-CONSISTENCY | Consistency |
| QM-TRACEABILITY | Traceability |
| QM-COMPILER_COMPATIBILITY | Compiler Compatibility |
| QM-RELATIONSHIP_INTEGRITY | Relationship Integrity |
| QM-BIBLIOGRAPHY_INTEGRITY | Bibliography Integrity |
| QM-GRAPH_INTEGRITY | Graph Integrity |
| QM-GOVERNANCE_COMPLIANCE | Governance Compliance |

Defaults: 0–100 scale, pass threshold **80**, overall rollup = weighted average (`quality_metrics.json`).

---

## Scorecards

| File | Scope |
|------|--------|
| `academic_scorecard.json` | Completeness, Consistency, Traceability, Bibliography Integrity |
| `technical_scorecard.json` | Compiler Compatibility, Relationship Integrity, Graph Integrity |
| `governance_scorecard.json` | Governance Compliance (+ supporting completeness/traceability) |

`review_checklist.json` maps RC-* checklist items to metric IDs.  
`golden_record_checklist.json` requires all eight metrics pass with overall ≥ **90** for golden promotion.

---

## Examples

`examples/quality_evaluation_example.json` — synthetic evaluation of fixture `KR-000000`. Not a review of production records.

---

## Validation

Structural validation for this folder:

1. All JSON files parse.
2. Exactly the eight metric codes above exist in `quality_metrics.json`.
3. Default metric weights sum to `1.0`.
4. Scorecards and checklists reference only registered `QM-*` IDs.
5. Example evaluation covers all eight metrics.

---

## Out of scope

- Automated scorer / CI gate implementation
- Changes to `knowledge/bazi/**`, bibliography, compiler, graph runtime, or KR content
