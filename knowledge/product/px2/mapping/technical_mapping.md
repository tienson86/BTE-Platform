# Technical Mapping

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## Source

`report.technical.*` ← `presentation.technical`

Plus **metadata-only** artifact / result fields copied into technical (never Hero):

| May copy into | From |
|---------------|------|
| report.technical.ids | presentation.technical.ids OR artifact.artifact_id (if presentation ids null) |
| report.technical.schema | presentation.technical.schema OR result.report_pipeline_version |
| report.technical.metadata | presentation.technical.metadata ∪ artifact.metadata ∪ mime_type |

Precedence: presentation field wins. Artifact/result fill only nulls.  
This is formatting/fallback of **metadata**, not consulting copy.

---

## Fields

| ui_id | contract_path | type | required | nullable | default | visibility | format | owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-------|
| Technical.calendar | report.technical.calendar | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| Technical.pillars | report.technical.pillars | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| Technical.timezone | report.technical.timezone | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| Technical.schema | report.technical.schema | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| Technical.ids | report.technical.ids | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| Technical.metadata | report.technical.metadata | object | no | yes | null | collapsed | metadata_map | TechnicalInfo |

Labels: `i18n.technical.*`.

---

## Visibility

Default **collapsed**.  
All null and no artifact metadata → **hidden**.  
Do not show traces/audits.

---

## Forbidden

- Artifact `content`  
- Promoting schema/ids into Hero  
- Displaying `engine_id` as a section title  

END
