# Hero Mapping

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## Source

`report.identity.*` ← `CanonicalReportResult.presentation.identity`

Structural: missing identity + `success=false` → page error.

Layout `cover` status may signal availability only.

---

## Fields

| ui_id | contract_path | type | required | nullable | default | visibility | format | owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-------|
| Hero.name | report.identity.full_name | string | yes | no | — | visible | plain_name | Hero |
| Hero.headline | report.identity.headline | string | yes | no | — | visible | sentence | Hero |
| Hero.one_line_summary | report.identity.one_line_summary | string | yes | no | — | visible | sentence | Hero |
| Hero.status | report.identity.consultation_status | enum | yes | no | — | visible | vi_status | Hero |

Status enum → `i18n.status.*`.

---

## Forbidden sources

- `canonical_report_artifact.content`  
- foundation analysis snapshots  
- timestamps, ids, schema, versions  
- `layout_result.document.title.source_ref` as display name  

---

## Failures

Any required Hero field null → **page error**. Not an empty Hero card.

END
