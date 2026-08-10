# Operational Platform

Version: 1.0.0  
Sprint: Phase XI · Beta-3

BTE continuous-operation layer. Contracts, catalogs, and runbooks only.

```
applications/operations/        registry, catalog, health
applications/observability/     Request-ID / Correlation-ID / Trace-ID reserved
applications/metrics/           API, pipeline, system catalog
applications/logging/           streams, audit, retention
applications/maintenance/       modes + lifecycle
applications/runbooks/          incident procedures
```

Deployment topology and compose remain in `deployment/` (Beta-1). Public API contracts remain in Beta-2. This sprint does not add endpoints or instrumentation.

AF-1 unchanged.

---

END
