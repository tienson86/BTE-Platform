# Public API Guide

Version: 1.0.0  
Sprint: Phase XI · Beta-2

The public API is the only supported integration surface for external clients.

## Base

```
/api/v1/
```

Health and identity stay at the root:

```
GET /health
GET /live
GET /ready
GET /version
```

## Resources

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/analysis` | Submit analysis |
| GET | `/api/v1/analysis/{id}` | Get analysis |
| GET | `/api/v1/report/{id}` | Get report |
| GET | `/api/v1/knowledge/{id}` | Get published knowledge |

`/api/v2/` is not available.

## Envelope

Success responses always include:

- `status`
- `data`
- `metadata`
- `request_id`
- `timestamp`
- `api_version`

Errors always include:

- `code`
- `message`
- `details`
- `request_id`
- `timestamp`

## Identifiers

Pass-through headers:

- `Request-ID`
- `Correlation-ID`
- `Idempotency-Key`

No persistence in this layer.

## Auth

Placeholder only. See [`AUTHENTICATION_GUIDE.md`](AUTHENTICATION_GUIDE.md).

## Spec

[`../openapi/openapi.yaml`](../openapi/openapi.yaml)

---

END
