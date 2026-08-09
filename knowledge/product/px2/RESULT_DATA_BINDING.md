# Result Data Binding

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Contract family: `bte.portal.result_ui.v2`

---

## 1. Law

Every visible content field binds to **one and only one** Report contract path.

No duplicated ownership.  
No implicit data.  
No computed business logic.  
Formatting only.

---

## 2. Binding stack

```
CanonicalReportResult                 (official Report root)
  ├── layout_result  → CanonicalReportLayout
  ├── canonical_report_artifact → CanonicalReportArtifact (metadata only)
  └── presentation   → Report Presentation Envelope (reserved; see §4)
        ↓
Portal Presentation Adapter           (format · group · visibility)
        ↓
UI Contract / PortalResultModel
        ↓
Component props
```

React never receives Analysis, Decision, Luck, Interpretation, package, or engine objects.

---

## 3. Two binding families

| Family | Prefix | Source | Used for |
|--------|--------|--------|----------|
| **Content** | `report.*` | Canonical Report presentation envelope + allowed structural/metadata paths | User-visible case data |
| **Chrome** | `i18n.*` | Language catalog (PX-1 Vietnamese) | Section titles, field labels, CTA microcopy, empty/error chrome |

Chrome is not Report truth.  
Content is not invented by i18n.

A field is either content or chrome. Never both. Never a third source.

---

## 4. Report Presentation Envelope

RX-1 `CanonicalReportResult` is a pipeline aggregate (`foundation_result`, `layout_result`, `rendering_result`, traces).

Portal must not walk those graphs ad hoc.

PX-2 declares a sealed **Report Presentation Envelope** addressed as `report.*`.

| Rule | Detail |
|------|--------|
| Logical root | `report` |
| Physical home (future) | `CanonicalReportResult.presentation` |
| Today | Envelope may be absent → Partial Ready / Empty / Error per visibility rules |
| Adapter | May **read** envelope fields; may **not** assemble them from Analysis/Decision/Luck/Interpretation |
| Artifact | Only `metadata`, identity, mime, success, errors — never `content` bytes/HTML/PDF |

If Report has not published a field, the adapter leaves it null/empty. It does not infer.

---

## 5. Allowed structural reads (non-content)

These paths feed **page/section state only**, not consulting copy:

| Path | Use |
|------|-----|
| `CanonicalReportResult.success` | Page error vs proceed |
| `CanonicalReportResult.errors` | Error presence (not raw display) |
| `CanonicalReportResult.report_pipeline_version` | Technical metadata only |
| `layout_result.success` | Layout failure → Partial / Error |
| `layout_result.sections[].module_id` | Adapter routing key only — never UI label |
| `layout_result.sections[].status` | assembled / empty → visibility |
| `layout_result.blocks[].block_type` | chart_placeholder / warning presence |
| `layout_result.blocks[].status` | Block availability |
| `canonical_report_artifact.success` | Artifact health |
| `canonical_report_artifact.metadata` | Technical section only |
| `canonical_report_artifact.artifact_id` | Technical section only |
| `canonical_report_artifact.mime_type` | Technical section only |

`layout_result.blocks[].source_refs` (e.g. `interpretation.overview`) are **adapter-internal routing keys**. They must never become React props or visible labels.

---

## 6. Mapping rule

```
ui_id  →  exactly one contract_path
```

Examples (normative):

| ui_id | contract_path |
|-------|---------------|
| `Hero.name` | `report.identity.full_name` |
| `Hero.headline` | `report.identity.headline` |
| `Hero.one_line_summary` | `report.identity.one_line_summary` |
| `Hero.status` | `report.identity.consultation_status` |
| `Recommendation.title` | `report.recommendations[].title` |
| `Recommendation.reason` | `report.recommendations[].reason` |
| `Recommendation.expected_result` | `report.recommendations[].expected_result` |
| `Recommendation.action` | `report.recommendations[].action` |

Full catalog: `FIELD_CATALOG.md`.

---

## 7. Formatting (allowed)

- Trim whitespace  
- Clamp summary bullets to 5 (drop overflow; do not rewrite)  
- Map domain enum → i18n domain label  
- Map status enum → i18n status string  
- Collapse default flags  
- Null → empty state, not placeholder invention  

## 8. Forbidden

- Scoring, ranking, or merging recommendations  
- Writing Why/Action from other fields  
- Reading Knowledge CSV / packages  
- Importing engine result types into React  
- Showing `module_id`, UUIDs, schema names in P1/P2  
- Using Artifact `content` as the Result Page body  

---

## 9. Stop line

Binding is mechanical. Meaning stays in Report. Experience stays in PX-1. Presentation stays in the adapter.

END
