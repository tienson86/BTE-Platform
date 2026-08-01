# Analysis Engine Test Framework

> **Scope:** `tests/analysis_engine/`
>
> **Status:** Framework skeleton only
>
> **Version:** 0.0.0

---

## Layout

```text
tests/analysis_engine/
├── conftest.py
├── README.md
├── unit/
├── integration/
├── golden/
├── fixtures/
├── builders/
└── snapshots/
```

## Rules

- Framework scaffolding only
- No analysis assertions
- No BaZi business logic
- No golden expected values authored yet

## Run (when tests are authored)

```bash
pytest tests/analysis_engine -q
```
