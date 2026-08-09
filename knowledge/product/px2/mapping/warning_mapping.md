# Warning Mapping

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## Source

`report.warnings[]` ← `presentation.warnings[]`

Layout `block_type == warning` without envelope items → hide section.

---

## Fields

| ui_id | contract_path | type | required | nullable | default | visibility | format | owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-------|
| Warning.title | report.warnings[].title | string | yes | no | — | hidden_if_empty | sentence | WarningCard |
| Warning.body | report.warnings[].body | string | yes | no | — | hidden_if_empty | sentence | WarningCard |
| Warning.mitigation | report.warnings[].mitigation | string | no | yes | null | collapsed | sentence | WarningCard |
| Warning.severity | report.warnings[].severity | enum | yes | no | attention | hidden | severity_enum | WarningCard |

Severity `attention` → component `warning`.  
Severity `critical` → `warning` + Danger token.

---

## Visibility

`length == 0` → **section hidden**. No blank warning card. No invented “all clear” copy.

END
