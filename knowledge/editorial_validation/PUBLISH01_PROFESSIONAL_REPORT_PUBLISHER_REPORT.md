# PUBLISH01 Professional Report Publisher Report

| Field | Value |
|-------|-------|
| Work item | PUBLISH_01_PROFESSIONAL_REPORT_PUBLISHER |
| Date | 2026-08-17 |
| Role | Publication editions over one Narrative |
| Engine changes | **NONE** |
| Architecture changes | **NONE** |

This sprint added a publication edition layer only. It does not calculate astrology, generate narrative, modify knowledge, or rewrite customer text. It answers one question: which already-composed paragraphs appear in which report edition.

---

## 1. Status

Complete.

Professional Report Publisher sits after Published Narrative Builder. Default production remains the Executive edition. Professional and Technical Appendix are edition policies over the same analytical truth.

Six customer PDFs were generated (Executive + Professional × three charts):

- `knowledge/editorial_validation/exports/publish01/executive/`
- `knowledge/editorial_validation/exports/publish01/professional/`

---

## 2. Architecture

Inserted edition policy only. No new analytical engine. No narrative composer change. No knowledge change. No routing change. No UI redesign. No PDF template redesign.

```
Decision / State / Relationship / Knowledge
        ↓
Narrative Composer V2                 (internal, unchanged)
        ↓
Published Narrative Builder           (PUBLISH / DROP / APPENDIX)
        ↓
Professional Report Publisher         (edition policy)
        ↓
Portal / PDF / Report Export
```

Default choke point stays `build_narrative_result_dict`.

- `publication_edition=executive` — current 7-section briefing (backward compatible)
- `publication_edition=professional` — 10-page consultation from the same evidence
- `publication_edition=technical_appendix` — supporting material only

Production may select the edition through `ProductionRequest.options["publication_edition"]`. Unset options keep Executive.

---

## 3. Publication editions

All editions originate from one NarrativeResult.

| Edition | Purpose | Source | Customer mix |
|---------|---------|--------|----------------|
| Executive | 5-minute briefing | Published spine | Identity, summary, key findings, current Da Yun, top recs, top warnings, one conclusion |
| Professional | Paid consultation | Same spine + additional PUBLISH-eligible evidence | Deepen reasoning; do not copy Executive Summary into core |
| Technical Appendix | Optional supporting material | DROP/APPENDIX knowledge that is correct but not spine | Never mixed into the consultation |

No duplicated engines. No duplicated narrative generation.

---

## 4. Executive edition

Unchanged customer spine.

Contains:

- Cover identity
- Executive Summary
- Observation / key findings
- Current Da Yun in the briefing
- Top recommendations
- Top warnings
- One-page conclusion

Target: 3–4 pages. Live PDFs: **4 pages** on all three charts.

---

## 5. Professional edition

Ten consultation pages from the same truth. Empty pages are omitted rather than filled with glossary.

| Page | Section | Policy |
|------|---------|--------|
| 1 | Cover + Tóm tắt | Same short briefing as Executive. Nothing more. |
| 2 | Lá số | Chart facts already composed. No encyclopedia. |
| 3 | Luận giải cốt lõi | Pattern / Strength / Useful God reasoning. Does not reprint Executive Summary. |
| 4 | Thập thần | Chart-relevant roles. Why this role matters here. No ten-god catalogue. |
| 5 | Thần sát | Matched stars only. No alias education. |
| 6 | Đại vận hiện tại | Current cycle, meaning, risk. Next cycle is published only when already in the Narrative. Not all ten cycles. |
| 7 | Sự nghiệp | Operating style, decision style, suitable / unsuitable environments. No profession catalogue. |
| 8 | Tài chính · Quan hệ · Sức khỏe · Học hỏi | One coherent consultation per area. |
| 9 | Khuyến nghị | Ranked 3–5 with already-composed rationale joined to the action. |
| 10 | Kết luận | One mature synthesis. No glossary. No restart. |

Paragraphs already used on an earlier consulting page are not copied later.

---

## 6. Appendix

Technical Appendix is a separate edition.

It receives correct supporting material that must not occupy the consultation:

- extended Ten Gods definitions
- star-alias education
- candidate / comparison notes
- additional concept references

On these three charts the appendix pool is 8–16 nodes. They are not written into the Professional PDF.

---

## 7. Expansion policy

```
Executive  → short briefing
Professional → deeper already-composed reasoning
```

Never copy the Executive Summary into core interpretation.

Expansion comes from evidence the composer already collected and Executive omitted for brevity:

- additional Pattern / Strength / Useful God reasons
- chart-relevant Ten God / Shen Sha consulting lines
- career and life-area applications
- recommendation actions plus their existing rationale

Dropped engine language, glossary dumps, unused gods, and unused stars stay unpublished.

---

## 8. Three live PDFs

| Chart | Cover class | Executive | Professional |
|-------|-------------|----------:|-------------:|
| Nguyễn Tiến Sơn | Người tự gánh | 4 pages · 433 words · 7 sections | 11 pages · 966 words · 10 sections |
| Lương Ngọc Huỳnh | Người kiến tạo | 4 pages · 434 words · 7 sections | 11 pages · 1206 words · 10 sections |
| Ngô Đặng Minh Tân | Người chỉnh trục | 4 pages · 387 words · 7 sections | 11 pages · 1107 words · 10 sections |

Leak hits in published narrative and HTML: **0** on all six PDFs.

Executive Summary is not copied into core interpretation on any chart.

Paths:

- `knowledge/editorial_validation/exports/publish01/executive/BTE_CASE-0001_Production_E2E.pdf`
- `knowledge/editorial_validation/exports/publish01/professional/BTE_CASE-0001_Production_E2E.pdf`
- `knowledge/editorial_validation/exports/publish01/executive/BTE_HUYNH_Production_E2E.pdf`
- `knowledge/editorial_validation/exports/publish01/professional/BTE_HUYNH_Production_E2E.pdf`
- `knowledge/editorial_validation/exports/publish01/executive/BTE_TAN_Production_E2E.pdf`
- `knowledge/editorial_validation/exports/publish01/professional/BTE_TAN_Production_E2E.pdf`

---

## 9. Comparison

| Measure | Sơn | Huỳnh | Tân |
|---------|----:|------:|----:|
| Added words | +533 | +772 | +720 |
| Token overlap Executive↔Professional | 0.496 | 0.358 | 0.388 |
| Professional has more sections | yes | yes | yes |
| Core reprints Executive Summary | no | no | no |
| Glossary / engine leaks | 0 | 0 | 0 |

Sơn example of expansion, not duplication:

- Executive reasoning: 2 sentences (thesis + compressed useful-god line).
- Professional core: 8 paragraphs — why Chính Ấn + Thân vượng require visible completion, what Thực Thần does on this chart, where Hỷ / Kỵ sit, and the endurance condition.
- Professional recommendations keep the same actions and add the already-composed rationale (`Ấn hữu dụng khi nuôi vừa`, `Thân vượng cần dẫn, không cần thêm nền`).

Career pages say how the person operates and which environments fit. They do not list professions.

---

## 10. Commercial evaluation

| Criterion | Result |
|-----------|--------|
| Added reasoning | Yes. Core, Ten Gods, and life areas publish composer evidence Executive left unpublished. |
| Added consulting value | Yes. Recommendations carry why-this-action. Career carries environment and decision style. |
| Added practical guidance | Yes. Stop/start conditions stay in customer prose. |
| Added understanding | Yes. The customer can read the governing pattern at briefing length, then the same pattern in depth. |
| Repetition | No increase. Overlap is the shared thesis, not copied paragraphs. |
| Glossary | Not in the consultation. Encyclopedia Ten God / Shen Sha text stays in Appendix. |

Professional reads as a longer consultation of the same case, not as a software dump of extra labels.

---

## 11. Files

- `engines/interpretation_engine/foundation/narrative/publish/editions.py` — edition ids, page map, limits
- `engines/interpretation_engine/foundation/narrative/publish/professional.py` — Professional Report Publisher
- `engines/interpretation_engine/foundation/narrative/publish/__init__.py` — public exports
- `applications/api/services/narrative_result_truth.py` — optional `publication_edition` (default Executive)
- `applications/production/orchestrator.py` — pass edition from request options
- `engines/report_engine/commercial/builder.py` — one chapter per Professional page; do not duplicate career
- `engines/report_engine/commercial/html_renderer.py` — consecutive chapters start on a new page (pagination only)
- `knowledge/editorial_validation/publish01_product_test.py`
- `knowledge/editorial_validation/exports/publish01/`
- `knowledge/editorial_validation/PUBLISH01_PROFESSIONAL_REPORT_PUBLISHER_REPORT.md`

---

## 12. Engine changes

**NONE**

Calendar, Bazi, Score, Pattern, Useful God, Knowledge, and Narrative Composer were not modified.

---

## 13. Architecture changes

**NONE**

No new consumer contract. No portal redesign. No PDF template redesign. Default Executive path is unchanged. Edition policy is an inserted publication stage.

One pagination rule was added so Professional chapters do not collapse into a longer Executive PDF. Layout, typography, and cover template are unchanged.

---

## 14. Tests

Module tests only. Tests were not modified.

| Suite | Result |
|-------|--------|
| `pytest tests/interpretation_engine/narrative tests/report_engine/test_narrative_canonical_binding.py -q` | 72 passed |

Remaining failures: none in the executed modules.

---

## 15. Final verdict

**READY_FOR_PROFESSIONAL_REPORT**

STOP.
