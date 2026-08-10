# OpenAPI Guide

Version: 1.0.0  
Sprint: Beta-2

## Source of truth

```
applications/openapi/openapi.yaml
```

OpenAPI 3.1. Covers all public Beta-2 endpoints, success envelope, error model, pagination metadata, and reserved `/metrics` + 429 responses.

## Companion docs

- [`../openapi/swagger.md`](../openapi/swagger.md)
- [`../openapi/redoc.md`](../openapi/redoc.md)
- [`../openapi/curl_examples.md`](../openapi/curl_examples.md)
- [`../openapi/python_examples.md`](../openapi/python_examples.md)
- [`../openapi/javascript_examples.md`](../openapi/javascript_examples.md)

## Completeness checklist

- [x] `/health` `/live` `/ready` `/version`
- [x] `/metrics` reserved
- [x] `/api/v1/analysis` POST + GET
- [x] `/api/v1/report/{id}`
- [x] `/api/v1/knowledge/{id}`
- [x] Success envelope schema
- [x] Canonical error schema
- [x] Request-ID / Correlation-ID / Idempotency-Key
- [x] Bearer + API Key security schemes (placeholder / reserved)
- [x] No `/api/v2/` paths

---

END
