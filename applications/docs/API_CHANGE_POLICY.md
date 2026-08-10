# API Change Policy

Version: 1.0.0  
Sprint: Beta-2

## Compatibility first

Public v1 is additive. Prefer new fields and new endpoints over edits to existing meaning.

## Change classes

| Class | Allowed in v1 | Action |
|-------|---------------|--------|
| Documentation | Yes | Patch release |
| Additive optional field | Yes | Minor release |
| New endpoint | Yes | Minor release |
| Rename / remove field | No | Major + new mount |
| Change type or error semantics | No | Major + new mount |
| Expose engine object | Never | Rejected |

## Process

1. Update request/response contracts.
2. Update `openapi.yaml` in the same change.
3. Update examples and public guides.
4. Record compatibility impact in the release note.
5. Do not modify engines, knowledge, pipelines, or Foundation to make an API change easier.

## Forbidden shortcuts

- Silent field meaning changes
- Version negotiation that serves v2 on `/api/v1/`
- Dual incompatible payloads on one path

See [`VERSIONING_POLICY.md`](VERSIONING_POLICY.md).

---

END
