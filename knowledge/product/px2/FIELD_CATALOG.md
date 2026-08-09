# Field Catalog

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Contract: `bte.portal.result_ui.v2`

Every visible **content** field and required **chrome** field.

---

## 1. Page / CTA

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| Page.state | report.page.state | enum | yes | no | loading | visible | page_state_enum | ResultPage |
| Page.partial | report.page.partial | boolean | yes | no | false | hidden | boolean | ResultPage |
| Page.error_message | report.page.error_message | string | no | yes | null | hidden_if_empty | vi_sentence | ResultPage |
| Page.error_code | report.page.error_code | string | no | yes | null | technical | opaque | ResultPage |
| CTA.primary_label | i18n.cta.primary | string | yes | no | — | visible | vi_label | Recommendation |
| CTA.primary_enabled | report.cta.primary.enabled | boolean | yes | no | false | visible | boolean | Recommendation |
| CTA.secondary_label | i18n.cta.secondary | string | no | yes | null | hidden_if_empty | vi_label | Recommendation |
| CTA.secondary_enabled | report.cta.secondary.enabled | boolean | no | yes | false | hidden_if_empty | boolean | Recommendation |

---

## 2. Hero

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| Hero.name | report.identity.full_name | string | yes | no | — | visible | plain_name | Hero |
| Hero.headline | report.identity.headline | string | yes | no | — | visible | sentence | Hero |
| Hero.one_line_summary | report.identity.one_line_summary | string | yes | no | — | visible | sentence | Hero |
| Hero.status | report.identity.consultation_status | enum | yes | no | — | visible | vi_status | Hero |

---

## 3. Summary

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| Summary.title | i18n.section.summary.title | string | yes | no | — | visible | vi_label | ExecutiveSummary |
| Summary.bullets | report.summary.bullets | string[] | yes | no | [] | visible | bullet_list_max_5 | ExecutiveSummary |

---

## 4. Recommendation

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| Recommendation.id | report.recommendations[].id | string | yes | no | — | never_hero | opaque_id | RecommendationCard |
| Recommendation.domain | report.recommendations[].domain | enum | yes | no | — | visible | domain_enum | RecommendationCard |
| Recommendation.title | report.recommendations[].title | string | yes | no | — | visible | sentence | RecommendationCard |
| Recommendation.reason | report.recommendations[].reason | string | yes | no | — | visible | sentence | RecommendationCard |
| Recommendation.expected_result | report.recommendations[].expected_result | string | yes | no | — | visible | sentence | RecommendationCard |
| Recommendation.action | report.recommendations[].action | string | yes | no | — | visible | sentence_or_bullets | RecommendationCard |
| Recommendation.detail | report.recommendations[].detail | string | no | yes | null | collapsed | prose | RecommendationCard |
| Recommendation.priority | report.recommendations[].priority | number | no | yes | null | hidden | sort_key_only | RecommendationCard |
| Recommendation.why_label | i18n.field.why | string | yes | no | — | visible | vi_label | RecommendationCard |
| Recommendation.expected_label | i18n.field.expected_result | string | yes | no | — | visible | vi_label | RecommendationCard |
| Recommendation.action_label | i18n.field.action | string | yes | no | — | visible | vi_label | RecommendationCard |

---

## 5. Warning

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| Warning.title | report.warnings[].title | string | yes | no | — | hidden_if_empty | sentence | WarningCard |
| Warning.body | report.warnings[].body | string | yes | no | — | hidden_if_empty | sentence | WarningCard |
| Warning.mitigation | report.warnings[].mitigation | string | no | yes | null | collapsed | sentence | WarningCard |
| Warning.severity | report.warnings[].severity | enum | yes | no | attention | hidden | severity_enum | WarningCard |

---

## 6. Domain

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| Domain.title | i18n.domain.{key} | string | yes | no | — | visible | vi_label | DomainSection |
| Domain.available | report.domains.{key}.available | boolean | yes | no | false | hidden | boolean | DomainSection |
| Domain.intro | report.domains.{key}.intro | string | no | yes | null | hidden_if_empty | sentence | DomainSection |
| Domain.recommendation_ids | report.domains.{key}.recommendation_ids | string[] | no | yes | [] | hidden | id_refs | DomainSection |
| Domain.analysis_preview | report.domains.{key}.analysis_preview | string | no | yes | null | visible | sentence | AnalysisCard |
| Domain.analysis_detail | report.domains.{key}.analysis_detail | string | no | yes | null | collapsed | prose | AnalysisCard |

Keys: `career` · `wealth` · `relationship` · `health` · `luck`.

---

## 7. Chart / Technical / Knowledge / Appendix

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| Chart.title | report.charts[].title | string | yes | no | — | hidden_if_empty | vi_title | ChartCard |
| Chart.caption | report.charts[].caption | string | yes | no | — | hidden_if_empty | sentence | ChartCard |
| Chart.asset_ref | report.charts[].asset_ref | string | yes | no | — | hidden | asset_ref | ChartCard |
| Chart.table | report.charts[].table | object | no | yes | null | collapsed | table | ChartCard |
| Technical.calendar | report.technical.calendar | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| Technical.pillars | report.technical.pillars | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| Technical.timezone | report.technical.timezone | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| Technical.schema | report.technical.schema | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| Technical.ids | report.technical.ids | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| Technical.metadata | report.technical.metadata | object | no | yes | null | collapsed | metadata_map | TechnicalInfo |
| Knowledge.title | report.knowledge[].title | string | yes | no | — | collapsed | vi_title | KnowledgeCard |
| Knowledge.teaser | report.knowledge[].teaser | string | yes | no | — | collapsed | sentence | KnowledgeCard |
| Knowledge.body | report.knowledge[].body | string | no | yes | null | collapsed | prose | KnowledgeCard |
| Appendix.scope | report.appendix.scope | string | no | yes | null | hidden_if_empty | sentence | Appendix |
| Appendix.reread | report.appendix.reread | string | no | yes | null | hidden_if_empty | sentence | Appendix |
| Appendix.limits | report.appendix.limits | string | no | yes | null | hidden_if_empty | sentence | Appendix |

---

## 8. Section chrome titles

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| Section.recommendation.title | i18n.section.recommendation.title | string | yes | no | — | visible | vi_label | Recommendation |
| Section.warnings.title | i18n.section.warnings.title | string | yes | no | — | hidden_if_empty | vi_label | ImportantWarnings |
| Section.charts.title | i18n.section.charts.title | string | yes | no | — | hidden_if_empty | vi_label | Charts |
| Section.technical.title | i18n.section.technical.title | string | yes | no | — | collapsed | vi_label | TechnicalInfo |
| Section.knowledge.title | i18n.section.knowledge.title | string | yes | no | — | collapsed | vi_label | Knowledge |
| Section.appendix.title | i18n.section.appendix.title | string | yes | no | — | hidden_if_empty | vi_label | Appendix |

---

## 9. Ownership law

One `ui_id` → one `contract_path` → one `component_owner`.

END
