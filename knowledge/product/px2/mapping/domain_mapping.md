# Domain Mapping

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## Source

`report.domains.{career|wealth|relationship|health|luck}` ← `presentation.domains.*`

Render order fixed (not layout luck/analysis order):

1. career 2. wealth 3. relationship 4. health 5. luck

---

## Fields (per key)

| ui_id | contract_path | type | required | nullable | default | visibility | format | owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-------|
| Domain.title | i18n.domain.{key} | string | yes | no | — | visible | vi_label | DomainSection |
| Domain.available | report.domains.{key}.available | boolean | yes | no | false | hidden | boolean | DomainSection |
| Domain.intro | report.domains.{key}.intro | string | no | yes | null | hidden_if_empty | sentence | DomainSection |
| Domain.recommendation_ids | report.domains.{key}.recommendation_ids | string[] | no | yes | [] | hidden | id_refs | DomainSection |
| Domain.analysis_preview | report.domains.{key}.analysis_preview | string | no | yes | null | visible | sentence | AnalysisCard |
| Domain.analysis_detail | report.domains.{key}.analysis_detail | string | no | yes | null | collapsed | prose | AnalysisCard |

---

## References

`recommendation_ids` resolve to `report.recommendations[]` by `id`.  
Domain section does **not** duplicate title/reason/action text in the envelope.

Unresolved id → skip that card (do not error the whole domain unless `available=true` and zero resolvable recs and no intro/analysis → Empty).

---

## Empty

`available=false` OR no intro, no recs, no analysis → **EmptyStateCard**, section remains in order.

---

## Forbidden

- Mapping `module_id: luck` string to the user  
- Filling wealth from career text  

END
