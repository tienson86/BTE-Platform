# Swagger Guide

Version: 1.0.0  
Sprint: Beta-2

Canonical spec: [`openapi.yaml`](openapi.yaml)

## Local preview

When a host mounts `register_public_service_layer(app)`:

```
http://127.0.0.1:8000/docs
```

FastAPI serves Swagger UI from the live OpenAPI schema.

## Static spec

```
applications/openapi/openapi.yaml
```

Import this file into Swagger Editor or any OpenAPI 3.1 viewer.

## Scope

Swagger documents public v1 endpoints only.

Do not publish `/api/v2/`.

Do not document engine-internal routes in this spec.

---

END
