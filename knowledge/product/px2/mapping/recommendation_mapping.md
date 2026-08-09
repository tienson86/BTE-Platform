# Recommendation Mapping

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## Source

`report.recommendations[]` ← `presentation.recommendations[]`

Layout `decision` emptiness may inform region empty — not copy.

Group in UI by `domain` enum. Group titles = `i18n.domain.*`.  
Grouping is formatting (bucket by declared field), not ranking logic.  
Optional `priority` is a sort key only if present; adapter does not invent priority.

---

## Fields

| ui_id | contract_path | type | required | nullable | default | visibility | format | owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-------|
| Recommendation.id | report.recommendations[].id | string | yes | no | — | never_hero | opaque_id | RecommendationCard |
| Recommendation.domain | report.recommendations[].domain | enum | yes | no | — | visible | domain_enum | RecommendationCard |
| Recommendation.title | report.recommendations[].title | string | yes | no | — | visible | sentence | RecommendationCard |
| Recommendation.reason | report.recommendations[].reason | string | yes | no | — | visible | sentence | RecommendationCard |
| Recommendation.expected_result | report.recommendations[].expected_result | string | yes | no | — | visible | sentence | RecommendationCard |
| Recommendation.action | report.recommendations[].action | string | yes | no | — | visible | sentence_or_bullets | RecommendationCard |
| Recommendation.detail | report.recommendations[].detail | string | no | yes | null | collapsed | prose | RecommendationCard |

Normative examples:

```
Recommendation.title           → report.recommendations[].title
Recommendation.reason          → report.recommendations[].reason
Recommendation.expected_result → report.recommendations[].expected_result
```

---

## CTA

`report.cta.primary.enabled` + `i18n.cta.primary`  
`report.cta.secondary.enabled` + `i18n.cta.secondary`

One Primary on the region, not per card.

---

## Empty

`[]` → region EmptyStateCard. Keep section. No blank rec cards.

---

## Forbidden

- Inventing reason from another field  
- Reading Decision engine types  
- Displaying `id`  

END
