# Operational Platform

Version: 1.0.0  
Sprint: Phase XI · Beta-3

Operational contracts for continuous production operation.

No business logic. No new HTTP endpoints. No engine or pipeline calls.

```
OperationsRegistry
  → Service catalog (api, portal, nginx, worker reserved, backup)
  → Health registry (service / pipeline / dependency / overall)
  → Operations context (env, role, maintenance flags)
```

Related:

- Observability: `applications/observability/`
- Metrics: `applications/metrics/`
- Logging: `applications/logging/`
- Maintenance: `applications/maintenance/`
- Runbooks: `applications/runbooks/`
- Deployment ops (Beta-1): `deployment/`

---

END
