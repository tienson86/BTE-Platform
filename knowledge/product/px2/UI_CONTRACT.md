# UI Contract

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Contract ID: `bte.portal.result_ui.v2`

---

## 1. Purpose

This is the only contract Portal Result components may consume.

If a value is not on this contract, it is not on the Result Page.

---

## 2. Contract object

```
PortalResultContract
├── contract_id            "bte.portal.result_ui.v2"
├── contract_version       "2.0.0"
├── page                   PageState + CTA + nav
├── hero
├── summary
├── recommendations        []
├── warnings               []
├── domains
│     ├── career
│     ├── wealth
│     ├── relationship
│     ├── health
│     └── luck
├── charts                 []
├── technical
├── knowledge              []
└── appendix
```

Language of all user-visible strings: **Vietnamese**.  
Identifiers (`ui_id`, `contract_path`, enums) stay English in the spec, never on screen.

---

## 3. Field descriptor (mandatory)

Every visible field declares:

| Attribute | Meaning |
|-----------|---------|
| `ui_id` | Stable component field id |
| `contract_path` | Single `report.*` or `i18n.*` path |
| `type` | string · string[] · enum · boolean · number · object · object[] |
| `required` | Must be present for parent ready state |
| `nullable` | Null allowed |
| `default` | Spec default when null and not required |
| `visibility` | visible · collapsed · hidden_if_empty · technical · never_hero |
| `format` | Formatting token (adapter only) |
| `component_owner` | Exactly one component |

No field may have two owners.

---

## 4. Root page fields

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| `Page.state` | `report.page.state` | enum | yes | no | `loading` | visible | page_state_enum | ResultPage |
| `Page.partial` | `report.page.partial` | boolean | yes | no | false | hidden | boolean | ResultPage |
| `CTA.primary_label` | `i18n.cta.primary` | string | yes | no | — | visible | vi_label | Recommendation |
| `CTA.primary_enabled` | `report.cta.primary.enabled` | boolean | yes | no | false | visible | boolean | Recommendation |
| `CTA.secondary_label` | `i18n.cta.secondary` | string | no | yes | null | hidden_if_empty | vi_label | Recommendation |
| `CTA.secondary_enabled` | `report.cta.secondary.enabled` | boolean | no | yes | false | hidden_if_empty | boolean | Recommendation |

Page state enum: `loading` · `ready` · `partial_ready` · `error` · `empty` · `offline` · `printing` · `exporting`.

`offline` is reserved.

---

## 5. Hero

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| `Hero.name` | `report.identity.full_name` | string | yes | no | — | visible | plain_name | Hero |
| `Hero.headline` | `report.identity.headline` | string | yes | no | — | visible | sentence | Hero |
| `Hero.one_line_summary` | `report.identity.one_line_summary` | string | yes | no | — | visible | sentence | Hero |
| `Hero.status` | `report.identity.consultation_status` | enum | yes | no | — | visible | vi_status | Hero |

Forbidden on Hero (must not exist on contract): timestamps, ids, schema, versions, engine names.

If `Hero.name` missing → page Error (not soft empty).

---

## 6. Summary

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| `Summary.title` | `i18n.section.summary.title` | string | yes | no | Tóm tắt tư vấn | visible | vi_label | ExecutiveSummary |
| `Summary.bullets` | `report.summary.bullets` | string[] | yes | no | [] | visible | bullet_list_max_5 | ExecutiveSummary |

Each bullet: one sentence. Adapter clamps to 5. Empty array after clamp → page Error if Hero exists (consultation cannot lead).

---

## 7. Recommendation item

Array path: `report.recommendations[]`  
Owner: `Recommendation` (region) + card instance.

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| `Recommendation.id` | `report.recommendations[].id` | string | yes | no | — | never_hero | opaque_id | RecommendationCard |
| `Recommendation.domain` | `report.recommendations[].domain` | enum | yes | no | — | visible | domain_enum | RecommendationCard |
| `Recommendation.title` | `report.recommendations[].title` | string | yes | no | — | visible | sentence | RecommendationCard |
| `Recommendation.reason` | `report.recommendations[].reason` | string | yes | no | — | visible | sentence | RecommendationCard |
| `Recommendation.expected_result` | `report.recommendations[].expected_result` | string | yes | no | — | visible | sentence | RecommendationCard |
| `Recommendation.action` | `report.recommendations[].action` | string | yes | no | — | visible | sentence_or_bullets | RecommendationCard |
| `Recommendation.detail` | `report.recommendations[].detail` | string | no | yes | null | collapsed | prose | RecommendationCard |
| `Recommendation.priority` | `report.recommendations[].priority` | number | no | yes | null | hidden | sort_key_only | RecommendationCard |

Domain enum: `career` · `wealth` · `relationship` · `health` · `luck`.  
Display via `i18n.domain.*` only.

`Recommendation.id` is never shown. It is instance identity for expand state.

Empty recommendations array → region Empty (not blank cards).

---

## 8. Warning item

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| `Warning.title` | `report.warnings[].title` | string | yes | no | — | hidden_if_empty | sentence | WarningCard |
| `Warning.body` | `report.warnings[].body` | string | yes | no | — | hidden_if_empty | sentence | WarningCard |
| `Warning.mitigation` | `report.warnings[].mitigation` | string | no | yes | null | collapsed | sentence | WarningCard |
| `Warning.severity` | `report.warnings[].severity` | enum | yes | no | `attention` | hidden | severity_enum | WarningCard |

Severity: `attention` · `critical`. Maps to Warning / Danger tokens — not copy.

Empty warnings array → **section hidden** (no blank card).

---

## 9. Domain section

One object per key under `report.domains.{career|wealth|relationship|health|luck}`.

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| `Domain.title` | `i18n.domain.{key}` | string | yes | no | — | visible | vi_label | DomainSection |
| `Domain.intro` | `report.domains.{key}.intro` | string | no | yes | null | hidden_if_empty | sentence | DomainSection |
| `Domain.recommendation_ids` | `report.domains.{key}.recommendation_ids` | string[] | no | yes | [] | hidden | id_refs | DomainSection |
| `Domain.analysis_preview` | `report.domains.{key}.analysis_preview` | string | no | yes | null | visible | sentence | AnalysisCard |
| `Domain.analysis_detail` | `report.domains.{key}.analysis_detail` | string | no | yes | null | collapsed | prose | AnalysisCard |
| `Domain.available` | `report.domains.{key}.available` | boolean | yes | no | false | hidden | boolean | DomainSection |

`recommendation_ids` reference `report.recommendations[].id` only. No second copy of rec text.

If `available=false` → Empty card for that domain (not hidden — order stays). Distinct from Warnings hide-if-empty.

---

## 10. Charts

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| `Chart.title` | `report.charts[].title` | string | yes | no | — | hidden_if_empty | vi_title | ChartCard |
| `Chart.caption` | `report.charts[].caption` | string | yes | no | — | hidden_if_empty | sentence | ChartCard |
| `Chart.asset_ref` | `report.charts[].asset_ref` | string | yes | no | — | hidden | asset_ref | ChartCard |
| `Chart.table` | `report.charts[].table` | object | no | yes | null | collapsed | table | ChartCard |

Charts section visible **only if** `report.charts` length > 0.  
Availability may also be signaled by layout `chart_placeholder` blocks — adapter sets `report.charts` only when presentation envelope provides chart records. Placeholder without envelope → section hidden (no blank chart card).

---

## 11. Technical (collapsed)

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| `Technical.calendar` | `report.technical.calendar` | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| `Technical.pillars` | `report.technical.pillars` | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| `Technical.timezone` | `report.technical.timezone` | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| `Technical.schema` | `report.technical.schema` | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| `Technical.ids` | `report.technical.ids` | string | no | yes | null | collapsed | technical_text | TechnicalInfo |
| `Technical.metadata` | `report.technical.metadata` | object | no | yes | null | collapsed | metadata_map | TechnicalInfo |

Section default: **collapsed**. Labels via `i18n.technical.*`.  
Metadata may include artifact metadata fields — never Hero.

---

## 12. Knowledge (collapsed)

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| `Knowledge.title` | `report.knowledge[].title` | string | yes | no | — | collapsed | vi_title | KnowledgeCard |
| `Knowledge.teaser` | `report.knowledge[].teaser` | string | yes | no | — | collapsed | sentence | KnowledgeCard |
| `Knowledge.body` | `report.knowledge[].body` | string | no | yes | null | collapsed | prose | KnowledgeCard |

Empty knowledge → section remains **collapsed header only** or hidden if no items and no toggle value. Prefer **hidden if empty** (no blank cards).

---

## 13. Appendix

| ui_id | contract_path | type | required | nullable | default | visibility | format | component_owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-----------------|
| `Appendix.scope` | `report.appendix.scope` | string | no | yes | null | hidden_if_empty | sentence | Appendix |
| `Appendix.reread` | `report.appendix.reread` | string | no | yes | null | hidden_if_empty | sentence | Appendix |
| `Appendix.limits` | `report.appendix.limits` | string | no | yes | null | hidden_if_empty | sentence | Appendix |

If all three null → **section hidden**. Adapter does not invent scope copy.

---

## 14. Stop line

`bte.portal.result_ui.v2` is the Portal Result SoT. Components bind this contract only.

END
