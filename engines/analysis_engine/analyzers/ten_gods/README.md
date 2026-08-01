# Ten Gods Analyzer

> **Path:** `engines/analysis_engine/analyzers/ten_gods/`
>
> **Analyzer ID:** `ten_gods`
>
> **Version:** see `VERSION`
>
> **Status:** Architecture skeleton

## Package Files

| File | Role |
|------|------|
| `analyzer.py` | Analyzer class skeleton |
| `models.py` | Input/result dataclasses |
| `interfaces.py` | Analyzer/validator ABCs |
| `validator.py` | Validator skeleton |
| `contracts.py` | Input/output/dependency/metadata/rules/result contracts |
| `SPEC.md` | Specification placeholder |
| `VERSION` / `CHANGELOG.md` | Versioning |

## Architecture Position

```text
Analysis Engine Pipeline
        │
        ▼
analyzers/ten_gods/
        │
        ▼
Registry / Validation contracts
        │
        ▼
Pack 01 (read-only)
```

Architecture and contracts only. No analysis logic.
