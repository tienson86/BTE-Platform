# BTE Validation Console

Sprint 2 Golden Dataset Manager — FastAPI + React workspace for creating, importing, comparing, and approving golden datasets.

This console does **not** write or mutate `tests/golden_dataset/` or published knowledge golden fixtures. It manages an isolated editor workspace under `api/data/`.

## Features

| Capability | Description |
|---|---|
| Create Dataset | Empty or seeded draft datasets |
| Import Dataset | JSON bundle import |
| Compare Results | Expected vs actual field diffs |
| Regression Test | Full-dataset compare + stored report |
| Approval | `draft → review → approved → released` |
| Statistics | Case / actual / tag / pass-rate stats |
| Coverage | Tag + coverage-goal completeness |

## Run API

```bash
uvicorn applications.validation_console.api.app:app --reload --port 8003
```

Docs: http://127.0.0.1:8003/docs

## Run UI

```bash
cd applications/validation_console
npm install
npm run dev
```

UI: http://127.0.0.1:5175 (proxies to :8003)

## Tests

```bash
pytest tests/validation_console -q
```
