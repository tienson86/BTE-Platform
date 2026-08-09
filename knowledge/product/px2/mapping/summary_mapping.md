# Summary Mapping

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## Source

`report.summary.bullets` ← `presentation.summary.bullets`  
Title ← `i18n.section.summary.title`

Layout `summary` / `overview` status = availability only.

---

## Fields

| ui_id | contract_path | type | required | nullable | default | visibility | format | owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-------|
| Summary.title | i18n.section.summary.title | string | yes | no | — | visible | vi_label | ExecutiveSummary |
| Summary.bullets | report.summary.bullets | string[] | yes | no | [] | visible | bullet_list_max_5 | ExecutiveSummary |

---

## Format

- One sentence per bullet  
- Adapter drops index > 4 (max 5)  
- Do not rewrite remaining bullets  

Empty after clamp → **page error** (consultation cannot lead).

---

## Forbidden

- Pulling `interpretation.overview` source_ref into bullets  
- Merging domain intros into summary  

END
