# Knowledge Mapping

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## Source

`report.knowledge[]` ← `presentation.knowledge[]`

Adapter does **not** load Knowledge Units or packages.

Layout `interpretation` emptiness may hide the section.

---

## Fields

| ui_id | contract_path | type | required | nullable | default | visibility | format | owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-------|
| Knowledge.title | report.knowledge[].title | string | yes | no | — | collapsed | vi_title | KnowledgeCard |
| Knowledge.teaser | report.knowledge[].teaser | string | yes | no | — | collapsed | sentence | KnowledgeCard |
| Knowledge.body | report.knowledge[].body | string | no | yes | null | collapsed | prose | KnowledgeCard |

---

## Visibility

`length == 0` → **hidden**.  
If items exist → section **collapsed**; cards expand via **Đọc tiếp**.

---

## Forbidden

- Direct knowledge CSV  
- Upsell copy  
- English headings  

END
