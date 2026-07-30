# Knowledge Validator Guide

## Pipeline

```text
Foundation schema check
        │
        ▼
Integrity (IDs / duplicates / domain match)
        │
        ▼
JSON Schema validation (knowledge/schema)
        │
        ▼
Relationship validation
        │
        ▼
Reference validation
```

## Modules

| Module | Checks |
|--------|--------|
| `schema_validator.py` | Draft 2020-12 foundation + per-record schema |
| `integrity_validator.py` | `KNO-NNNNNN`, duplicates, domain directory consistency |
| `relationship_validator.py` | link shape, broken targets, pairwise cycles on `depends_on` |
| `reference_validator.py` | reference object shape; official/approved require refs |
| `knowledge_validator.py` | composite orchestration |

## Usage

```python
from services.knowledge.knowledge_loader import KnowledgeLoader
from services.knowledge.knowledge_validator import KnowledgeValidator

loader = KnowledgeLoader(project_root=".")
result = KnowledgeValidator(loader).validate_all()
assert result.ok
```
