# Compatibility Report — Epic 03 Milestone 10

## API compatibility

| Contract | Status |
|----------|--------|
| `PUBLIC_PIPELINE_ORDER` | Unchanged |
| `POST /api/v1/analyze` required keys | Unchanged |
| `report` / `narrative` shapes | Unchanged |
| `POST /api/v1/discussion` | Additive |
| `data.knowledge_expert` on analyze | Additive optional status |

## UI compatibility

- No portal presenter/template changes in M10
- Discussion tab continues to render `narrative || report`
- Extra `knowledge_expert` key is ignored by existing presenters

## Engine compatibility

- No calculation engine Public API renames/removals
- Knowledge Expert depends forward on RuleContext-like mappings only
