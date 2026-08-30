# N-IMP-11 PRESENTATION EXPORT LAYER REPORT

Sprint: N-IMP-11
Module: `engines.narrative_v2.export`
Mode: Shadow only
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

The Presentation Export Layer is the only component that exposes `NarrativeV2Presentation` to Portal, PDF, DOCX, and JSON. Consumers render. They do not compose, rewrite, or merge Narrative. Production Portal, Pack05, customer PDF, and customer DOCX are unchanged.

---

## 2. Architecture

```
Narrative Runtime
  → NarrativeV2Presentation (v2.1)
  → Presentation Export Layer
       → PortalExport   (shadow JSON / blocks)
       → PdfExport      (shadow PDF)
       → DocxExport     (shadow DOCX)
       → JsonExport     (canonical JSON == Presentation)
```

Shared `ExportContext.blocks` is built once from Presentation fields. Every consumer prints those blocks. Null fields are omitted from render blocks and left `null` in JSON.

---

## 3. Export Layer

Location: `engines/narrative_v2/export/`

| File | Role |
| --- | --- |
| `export_builder.py` | Copy Presentation → ordered `ExportBlock`s |
| `export_context.py` | Immutable shared context |
| `export_validator.py` | Version, shadow, public/private |
| `export_serializer.py` | JSON serialize / hydrate |
| `portal_export.py` | Portal shadow payload |
| `pdf_export.py` | Shadow PDF (Playwright print, no Report Builder) |
| `docx_export.py` | Shadow DOCX (python-docx, no Report Builder) |
| `json_export.py` | Canonical JSON |
| `export_registry.py` | `PresentationExportLayer` facade |
| `export_errors.py` | Typed errors, no silent fallback |

Facade: `PresentationExportLayer.export_all()`.

---

## 4. Portal Export

Shadow only. `PortalExport` copies Presentation + the same blocks.

- `shadow_mode=true`
- `replaces_pack05=false`
- version `bte.presentation.v2.1`

Customer Portal production rendering was not modified in this sprint. N-IMP-10 Portal shadow already renders Presentation; this layer is the canonical export contract those consumers must match.

---

## 5. PDF Export

Shadow PDF from Presentation blocks only.

- One HTML `<p>` per block
- Visible text = Presentation strings
- No `HtmlReportV1Renderer`, no Report Engine, no composed summary

Artifact: `implementation/narrative_v2/n_imp_11/pdf_shadow.pdf`

---

## 6. DOCX Export

Same blocks. One Word paragraph per block. No extra titles invented. Action titles come from Presentation.

Artifact: `implementation/narrative_v2/n_imp_11/docx_shadow.docx`

---

## 7. JSON Export

`json.dumps(serialize_customer(presentation))`. Round-trip equals Presentation. Includes null identity/balance/conclusion and `commercial: null`.

Artifact: `implementation/narrative_v2/n_imp_11/json_shadow.json`

`portal_shadow.json` is the same payload.

---

## 8. Parity Validation

CASE-0001 ordered customer strings: **20 blocks**.

Portal blocks = PDF HTML paragraphs = DOCX paragraphs = JSON block list.

No sentence added. No sentence dropped. Null fields not filled. Formatting (PDF vs DOCX paragraph styling) may differ; content does not.

See `n_imp_11/parity_report.md`.

---

## 9. CASE-0001

Generated from live Narrative Runtime (luck canonical → Presentation v2.1).

- consulting_flow exact 07C wording
- structured Interpretation copied independently (including closing = observation, upstream)
- Action: “Ưu tiên giữ nền tảng hiện tại” + three practice actions + warning
- identity / balance / conclusion / commercial / current_period remain null

---

## 10. Files

Created:

- `engines/narrative_v2/export/*.py` (layer + `write_case0001_artifacts.py`)
- `tests/narrative_v2/test_presentation_export.py`
- `implementation/narrative_v2/n_imp_11/portal_shadow.json`
- `implementation/narrative_v2/n_imp_11/pdf_shadow.pdf`
- `implementation/narrative_v2/n_imp_11/docx_shadow.docx`
- `implementation/narrative_v2/n_imp_11/json_shadow.json`
- `implementation/narrative_v2/n_imp_11/parity_report.md`
- `implementation/narrative_v2/n_imp_11/before_after.md`
- `implementation/narrative_v2/n_imp_11/01_pdf_preview.png`
- `implementation/narrative_v2/N_IMP_11_REPORT.md`

Modified: none of customer Portal, Pack05, `applications/api/routes/export.py`, astrology engines.

---

## 11. Tests

`py -m pytest tests/narrative_v2/test_presentation_export.py -q`

**9 passed**

- JSON equals Presentation
- Portal copy
- Portal / PDF / DOCX / JSON parity
- No private tokens
- Consumers do not compose
- Incompatible version rejected
- Production export route and Pack05 untouched
- Frozen CASE-0001 round-trip
- Null fields not invented

Remaining failures: **none**.

---

## 12. Screenshots

`implementation/narrative_v2/n_imp_11/01_pdf_preview.png` — shadow PDF HTML, CASE-0001 blocks only.

---

## 13. Shadow Mode

Portal production unchanged. PDF production unchanged. DOCX production unchanged. Exports set `shadow_mode=true`, `replaces_pack05=false`.

---

## 14. Out-of-scope

No Portal switch: **YES**

No Pack05 replacement: **YES**

No new Narrative: **YES**

No consumer compose: **YES**

No astrology engine modified: **YES**

N-IMP-12 not started.

---

## 15. Verdict

**READY FOR PRODUCT OWNER REVIEW**
