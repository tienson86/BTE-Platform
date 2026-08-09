# Chart Mapping

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## Source

`report.charts[]` ← `presentation.charts[]`

Layout `chart` / `chart_placeholder` = availability hint only.

Asset bytes are not in PX-2. `asset_ref` is an opaque reference for a future renderer **inside Portal presentation**, not Artifact HTML.

---

## Fields

| ui_id | contract_path | type | required | nullable | default | visibility | format | owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-------|
| Chart.title | report.charts[].title | string | yes | no | — | hidden_if_empty | vi_title | ChartCard |
| Chart.caption | report.charts[].caption | string | yes | no | — | hidden_if_empty | sentence | ChartCard |
| Chart.asset_ref | report.charts[].asset_ref | string | yes | no | — | hidden | asset_ref | ChartCard |
| Chart.table | report.charts[].table | object | no | yes | null | collapsed | table | ChartCard |

---

## Visibility

`length == 0` → **section hidden**. Never a blank chart card.  
Never before recommendations in render order.

---

## Forbidden

- Artifact `content` as the chart  
- English-only titles  
- Advice essays inside chart chrome  

END
