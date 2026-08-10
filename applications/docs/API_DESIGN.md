# API Design

Version: 1.0.0  
Sprint: Beta-2

## Principles

- Contract first
- Versioned under `/api/v1/`
- Service layer only
- Canonical pipelines only
- No engine objects in responses
- Deterministic envelopes
- Backward compatible within v1

## Layers

```
Client
  → Public routers (applications/api/v1)
    → Public services (applications/services)
      → CanonicalPipelinePort
        → Canonical pipelines (runtime binding)
```

Routers validate HTTP and identifiers.  
Services validate request models and call the pipeline port.  
No business rules live in this layer.

## Resource style

Nouns, not engine names:

- `/analysis`
- `/report`
- `/knowledge`

Do not expose `/calendar`, `/bazi`, `/pattern`, or other engine routes on the public service API.

## Compatibility

Additive fields are allowed in v1.  
Breaking changes require `/api/v2/` and a deprecation cycle.  
v2 is reserved and not mounted.

---

END
