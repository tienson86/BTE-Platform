# Integration Guide

Version: 1.0.0  
Sprint: Beta-2

## For API consumers

1. Call only `/api/v1/` resource paths plus root health/version probes.
2. Send `Request-ID` on every call. Echo `request_id` from responses when reporting issues.
3. Parse the success envelope; never assume engine-shaped objects.
4. Treat unknown `data` fields as additive and ignore safely.
5. On errors, branch on `code`, not on HTTP text.
6. Honor `Retry-After` when `BTE-429-RATE_LIMITED` appears (policy reserved).

## For runtime hosts

```python
from fastapi import FastAPI
from applications.api.api_router import register_public_service_layer
from applications.services.service_registry import ServiceRegistry

app = FastAPI()
register_public_service_layer(app, registry=ServiceRegistry.create_default())
```

To execute real work, inject a `CanonicalPipelinePort` implementation that calls canonical pipeline public APIs only. Do not import engine internals into this layer.

## Existing Applications API

`applications.api.app:app` remains the current production host and is unchanged in Beta-2. The public service layer is additive and mountable.

---

END
