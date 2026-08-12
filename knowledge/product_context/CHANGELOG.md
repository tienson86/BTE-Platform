# CHANGELOG — Product Context Engine

## 1.0.0

### Added

- `applications/production/product_context/` (models, life stage, feature filter, engine, delivery, input builder)
- Orchestrator stages: `product_context`, `context_delivery`
- Customer fields: `development_guidance`, `parent_guidance`
- Tests: `tests/production/test_product_context.py`
- Docs under `knowledge/product_context/`

### Unchanged

- Rule database, knowledge packs, CDR, CLL source, calculation engines, claim truth

### DoD

| Criterion | Status |
|-----------|--------|
| Child no adult Career | PASS |
| Parent guidance enabled | PASS |
| Adult output unchanged | PASS |
| CASE-0003 improves | PASS |
| CASE-0001 regression | PASS |
