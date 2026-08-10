# Dual Expert Review Workflow

## Preconditions

- Chart calendar-verified under tiết khí SSOT  
- Evidence snapshot available  
- Reviewers assigned as EXPERT-A / EXPERT-B (anonymized)  
- Expert-B must not see Expert-A classification before independent pass

## Steps

1. **Prepare blind pack:** pillars, evidence checklist, no runtime band/score.  
2. **Expert-A:** fill `templates/EXPERT_REVIEW_TEMPLATE.json` → store as `reviews/CAL-XXXXXX_review1.json`.  
3. **Expert-B:** independent fill → `reviews/CAL-XXXXXX_review2.json`.  
4. **Agreement:** compute EXACT_MATCH / ADJACENT_MATCH / WITHIN_TWO_LEVELS / EXPERT_DISAGREEMENT / INSUFFICIENT_EVIDENCE.  
5. **Adjudicate** if >1 level apart, LOW confidence, boundary anchor, or conflicting evidence interpretation.  
6. **Update** case JSON: review_status, inclusion_status, agreement class.  
7. **Never overwrite** original expert_review_1 / expert_review_2.

## Anti-patterns

- Asking experts to match the engine  
- Inventing Expert-B to close coverage gaps  
- Promoting to Golden Dataset during acquisition sprints  
- Case-specific production rules from a single disagreement
