# BTE Knowledge Console

Sprint 2 Knowledge Editor — React UI + FastAPI workspace for drafting and approving knowledge assets.

This console does **not** write golden `knowledge/` files. It is an editor workspace with validation, preview, diff, history, versioning, and approval workflow.

## Features

| Capability | Description |
|---|---|
| Rule Editor | `rule_id`, condition, action, priority |
| Sentence Editor | templates + placeholders |
| Phrase Editor | reusable phrase text |
| Terminology Editor | term / domain / display name |
| Preview | Deterministic rendered text |
| Validation | Per-type schema checks |
| Diff | Version vs version (or current) |
| History | Actor / action timeline |
| Version | Immutable snapshots |
| Approval | `draft → review → approved → released` (reject from review) |

## Run API

From repo root:

```bash
uvicorn applications.knowledge_console.api.app:app --reload --port 8002
```

Docs: http://127.0.0.1:8002/docs

## Run UI

```bash
cd applications/knowledge_console
npm install
npm run dev
```

UI: http://127.0.0.1:5174 (proxies `/api` and `/health` to port 8002)

## Tests

```bash
pytest tests/knowledge_console -q
```

## API sketch

- `GET/POST /api/v1/assets`
- `GET/PUT /api/v1/assets/{id}`
- `POST /api/v1/assets/{id}/validate`
- `GET /api/v1/assets/{id}/preview`
- `GET /api/v1/assets/{id}/history`
- `GET /api/v1/assets/{id}/versions`
- `GET /api/v1/assets/{id}/diff?from_version=&to_version=`
- `GET /api/v1/workflow/queue`
- `POST /api/v1/workflow/{id}` with `{ "action": "submit|approve|reject|release" }`
