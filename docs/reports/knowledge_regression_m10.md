# Knowledge Integration Regression Report — Epic 03 Milestone 10

## Checks

- Public analyze pipeline order preserved
- Narrative/report contracts preserved
- Additive `/api/v1/discussion` endpoint
- Additive `knowledge_expert` analyze status block
- 100-chart KnowledgePipeline validation executed

## 100-chart results

- Grounded: 100/100
- Validation passed: 100/100
- Failures remaining in this suite: **0** (threshold grounded >= 70)

## Notes

- Classical corpus may still be schema-only; tests inject knowledge records.
- Deterministic LLM adapter is used (no external LLM dependency).
