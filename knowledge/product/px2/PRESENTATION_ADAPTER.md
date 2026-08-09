# Presentation Adapter

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Adapter ID: `bte.portal.presentation_adapter.v2`

---

## 1. Purpose

The Portal Presentation Adapter is the only bridge from Report to UI Contract.

```
CanonicalReportResult
        ↓
map + format + visibility
        ↓
PortalResultModel  (bte.portal.result_ui.v2)
        ↓
React components     (future — not this sprint)
```

React must never know Analysis, Decision, Luck, Interpretation, packages, or engines.

---

## 2. Inputs (allowed)

| Input | Role |
|-------|------|
| `CanonicalReportResult` | Official root |
| `CanonicalReportLayout` via `layout_result` | Section/block availability |
| `CanonicalReportArtifact` via `canonical_report_artifact` | **Metadata only** |
| i18n catalog | Vietnamese chrome |

## 3. Inputs (forbidden)

- Direct engine clients  
- Pipeline runners  
- Knowledge loaders  
- Package loaders  
- Interpretation / Narrative / Decision / Luck / Analysis types  
- Artifact `content`, HTML, PDF, DOCX bytes  

---

## 4. Responsibilities

Allowed:

- Validate contract presence  
- Bind `report.*` → `ui_id`  
- Resolve `i18n.*` chrome  
- Clamp lists (max 5 summary bullets)  
- Set visibility / collapsed defaults  
- Map enums → Vietnamese labels  
- Derive **page state** from success + required field presence  
- Pass through formatting (trim, null → empty)  

Forbidden:

- Calculating scores  
- Ranking or inventing recommendations  
- Writing consulting copy  
- Merging domains by business rule beyond declared `domain` field  
- Filling Why from another field  
- Promoting technical metadata into Hero  

This matches PACK_04 adapter spirit (presentation only) without importing engine ViewModels that leak Analysis types.

---

## 5. Output

Exactly one `PortalResultModel`.

Never a tuple. Never a mixed engine dict.

---

## 6. Envelope rule

Preferred content source:

```
CanonicalReportResult.presentation   →   report.*
```

This envelope is **reserved** on the Report result. PX-2 specifies it; PX-2 does not implement Report publication.

If `presentation` is absent:

- Adapter still reads structural success/errors/section status  
- Content fields are null/empty  
- Page state becomes `empty`, `partial_ready`, or `error` per `states/page_state_machine.md`  
- Adapter does **not** reconstruct `report.identity` from foundation snapshots of Analysis  

---

## 7. Layout usage

Layout is used for **availability**, not copy.

| Layout signal | Adapter effect |
|---------------|----------------|
| `sections[].status == empty` | Domain/section `available=false` when envelope also lacks content |
| `block_type == chart_placeholder` and no `report.charts` | Charts section hidden |
| `block_type == warning` and no `report.warnings` | Warnings hidden |
| `module_id` | Internal route key only |

Never render `LSEC-decision` or `MODULE_LUCK` to the user.

---

## 8. Artifact usage (metadata only)

Allowed to copy into `report.technical.metadata` / ids (collapsed technical):

- `artifact_id`  
- `mime_type`  
- `render_version`  
- `success`  
- `metadata` dict  

Forbidden:

- `content`  
- embedding HTML into Result sections  
- using renderer name as Hero status  

---

## 9. Failure policy

| Condition | Adapter output |
|-----------|----------------|
| Result null | Page `error` |
| `success=false` and no Hero envelope | Page `error` |
| Hero missing required fields | Page `error` |
| Hero ok, summary empty | Page `error` (cannot lead) |
| Hero + summary ok, recs empty | Page `partial_ready` + rec Empty |
| Isolated domain missing | `partial_ready`, domain Empty card |
| Isolated chart missing | hide charts |
| Technical missing | technical `available=false`, stay collapsed |

Never throw engine exceptions through the UI contract.

---

## 10. Stop line

One adapter. Formatting only. Report in. UI Contract out.

END
