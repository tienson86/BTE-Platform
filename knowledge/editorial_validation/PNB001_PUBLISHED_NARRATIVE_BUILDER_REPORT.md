# PNB001 Published Narrative Builder Report

| Field | Value |
|-------|-------|
| Work item | PNB-001_PUBLISHED_NARRATIVE_BUILDER |
| Date | 2026-08-16 |
| Role | Publication stage between Narrative Composer and Customer Report |
| Engine changes | **NONE** |
| Architecture changes | **NONE** |

This sprint added a publication layer only. It does not generate narrative, does not explain astrology, and does not rewrite knowledge. It answers one question: which already-composed paragraphs deserve to appear in the customer report.

---

## 1. Status

Complete.

Published Narrative Builder is wired as the last step of `build_narrative_result_dict`. Portal, commercial PDF, and report export consume that payload. Internal Narrative Composer V2 remains untouched.

Three customer PDFs were regenerated:

- `knowledge/editorial_validation/exports/pnb001/BTE_CASE-0001_Production_E2E.pdf` — Nguyễn Tiến Sơn
- `knowledge/editorial_validation/exports/pnb001/BTE_HUYNH_Production_E2E.pdf` — Lương Ngọc Huỳnh
- `knowledge/editorial_validation/exports/pnb001/BTE_TAN_Production_E2E.pdf` — Ngô Đặng Minh Tân

---

## 2. Architecture

Inserted stage only. No new analytical engine. No routing change. No UI or PDF redesign.

```
Decision / State / Relationship / Knowledge
        ↓
Narrative Composer V2          (internal, unchanged)
        ↓
Published Narrative Builder    (publication decisions)
        ↓
Portal / PDF / Report Export   (published sections only)
```

The choke point is `applications/api/services/narrative_result_truth.py` → `build_narrative_result_dict`. API analyze and `ProductionEndToEndOrchestrator` already compose through this function. The builder replaces customer-facing `sections`, rebuilds `summary` / `recommendations` from published paragraphs, and stores decision codes in `metadata.publication` without copying dropped bodies into the customer payload.

---

## 3. Publication pipeline

1. Receive NarrativeResult V2 (Pack 05 contract shape).
2. Classify every paragraph as PUBLISH, DROP, or APPENDIX. Never split a paragraph.
3. Deduplicate by meaning (fingerprint + token Jaccard), not identical strings.
4. Enforce publication limits. Keep higher-priority customer value when space collides.
5. Replace consumer `sections` with PUBLISH text only.
6. Rebuild summary from published Executive Summary / Recommendations / Warnings.

Priority when space or meaning collides:

Executive Summary → Reasoning → Recommendations → Impact → Warnings → Observation → Conclusion

---

## 4. Publish criteria

A node is PUBLISH only if it:

- supports this chart (observation facts, selected useful god, current Da Yun)
- supports current reasoning or the case thesis
- supports a recommendation or warning
- or deepens understanding of the same consultation

Not merely because knowledge exists.

Publication limits (internal narrative may contain more):

| Section | Limit |
|---------|-------|
| Executive Summary | 4–6 sentences (max 6 published) |
| Observation | 5–8 |
| Reasoning | one chain (max 3) |
| Impact | one paragraph per spine domain (max 4) |
| Recommendation | max 5 |
| Warning | max 3 |
| Conclusion | one ending |

---

## 5. Drop criteria

DROP the whole node when it contains:

- engine / implementation / debug language (`Loaded`, `Winner`, `priority`, `score`, `engine`, `token`, `alias`, `detector`, `rule_id`, `Production`, `Knowledge không sửa engine`, `Decision Explanation`)
- English domain dumps (`Career:`, `Health:`, `Decision:`)
- glossary or multi-topic knowledge dump
- unused-god / hypothetical-role explanation
- duplicate customer value
- a paragraph that weakens the thesis

Dropped text stays inside the composer. It is not deleted internally.

---

## 6. Appendix criteria

APPENDIX is correct knowledge that must not occupy the customer spine:

- extended Ten Gods definitions
- star aliases
- internal comparisons
- candidate explanations
- rule commentary
- non-spine impact domains (Học hỏi / Ra quyết định)

APPENDIX is not written into the customer PDF. Customer PDF contains published narrative only.

On these three charts, composer output after WP-001 no longer carried encyclopedia paragraphs into the seven sections, so appendix count is 0. The gate is implemented and fires when that class of text reaches publication.

---

## 7. Editorial filtering

Every paragraph is evaluated before publication:

| Gate | Result |
|------|--------|
| Relevant to this chart | keep or drop unused-god |
| Supports the thesis | keep; weaken → DROP |
| Advances the consultation | keep |
| Practical value | keep |
| Glossary / dump | DROP |
| Duplicate meaning | keep one |
| Engine language | DROP |
| Implementation language | DROP |

---

## 8. Sơn

Cover class: Người tự gánh. PDF: 3 pages.

| Decision | Count |
|----------|------:|
| Published | 27 |
| Dropped | 1 |
| Appendix | 0 |

Dropped reason: `duplicate_meaning` in Recommendations (same customer value already published at higher priority).

Published section counts: Exec 5 · Observation 8 · Reasoning 2 · Impact 4 · Recommendation 4 · Warning 3 · Conclusion 1.

Word count: 433. Leak hits in published narrative and HTML: 0.

---

## 9. Huỳnh

Cover class: Người kiến tạo. PDF: 3 pages.

| Decision | Count |
|----------|------:|
| Published | 27 |
| Dropped | 1 |
| Appendix | 0 |

Dropped reason: `hypothetical_unused_god` in Recommendations.

Published section counts: Exec 5 · Observation 8 · Reasoning 2 · Impact 4 · Recommendation 4 · Warning 3 · Conclusion 1.

Word count: 434. Leak hits: 0.

---

## 10. Tân

Cover class: Người chỉnh trục. PDF: 3 pages.

| Decision | Count |
|----------|------:|
| Published | 25 |
| Dropped | 3 |
| Appendix | 0 |

Dropped reasons: `hypothetical_unused_god` × 2, `duplicate_meaning` × 1, all in Recommendations.

Published section counts: Exec 5 · Observation 8 · Reasoning 2 · Impact 4 · Recommendation 2 · Warning 3 · Conclusion 1.

Word count: 387. Leak hits: 0.

---

## 11. Commercial metrics

| Chart | Words | Readability | Customer relevance | Commercial score | Leaks |
|-------|------:|------------:|-------------------:|-----------------:|------:|
| Sơn | 433 | 100 | 0.964 | 100 | 0 |
| Huỳnh | 434 | 100 | 0.964 | 100 | 0 |
| Tân | 387 | 100 | 0.893 | 100 | 0 |

Commercial score rewards leak-free publication, section limits, thesis presence, recommendations, and domain impact. It does not reward knowledge completeness.

Distinctive leak fragments (`Career:`, `Loaded`, `Winner`, `Engine chọn`, `Production phải truyền stems`, `Knowledge không sửa engine`) are absent from published sections and from the generated HTML.

---

## 12. Regression

Module tests only. Tests were not modified.

| Suite | Result |
|-------|--------|
| `pytest tests/interpretation_engine/narrative tests/report_engine/test_narrative_canonical_binding.py -q` | 72 passed |
| `pytest tests/domain01 tests/commercial_knowledge/test_integration.py -q` | 29 passed |

Internal composer for Sơn still renders 28 sentences. Publication keeps 27. Composer output is not mutated.

Remaining failures: none in the executed modules.

---

## 13. Files changed

- `applications/api/services/narrative_result_truth.py` — apply publication as the last step
- `engines/interpretation_engine/foundation/narrative/publish/__init__.py`
- `engines/interpretation_engine/foundation/narrative/publish/constants.py`
- `engines/interpretation_engine/foundation/narrative/publish/models.py`
- `engines/interpretation_engine/foundation/narrative/publish/criteria.py`
- `engines/interpretation_engine/foundation/narrative/publish/metrics.py`
- `engines/interpretation_engine/foundation/narrative/publish/builder.py`
- `knowledge/editorial_validation/pnb001_product_test.py`
- `knowledge/editorial_validation/exports/pnb001/` — three HTML/PDF sets + `_metrics.json`
- `knowledge/editorial_validation/PNB001_PUBLISHED_NARRATIVE_BUILDER_REPORT.md`

---

## 14. Engine changes

NONE

Calendar, Bazi, Score, Pattern, Useful God, Knowledge, and Narrative Composer were not modified in this sprint.

---

## 15. Architecture changes

NONE

No new consumer contract. No portal redesign. No PDF template redesign. No routing change. Publication is an inserted stage on the existing NarrativeResult choke point.

---

## 16. Final verdict

**READY_FOR_PUBLISHING**

STOP.
