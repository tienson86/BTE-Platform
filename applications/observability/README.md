# Observability

Version: 1.0.0  
Sprint: Beta-3

Identifier contracts only. No OpenTelemetry, no span export, no new middleware.

| Identifier | Status |
|------------|--------|
| Request-ID | Active (pass-through) |
| Correlation-ID | Active (pass-through) |
| Trace-ID | Reserved |
| Operation-ID | Active (field) |
| Pipeline-ID | Active (field) |

Do not modify public API middleware in this sprint.

---

END
