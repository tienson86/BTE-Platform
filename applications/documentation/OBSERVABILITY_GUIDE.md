# Observability Guide

Version: 1.0.0  
Sprint: Beta-3

## Identifiers

| Name | Header / field | Status |
|------|----------------|--------|
| Request-ID | `Request-ID` | Required, pass-through |
| Correlation-ID | `Correlation-ID` | Optional, pass-through |
| Trace-ID | `Trace-ID` | Reserved — no tracer |
| Operation-ID | `operation_id` | Service operation name |
| Pipeline-ID | `pipeline_id` | Canonical pipeline name |

## Rules

- Correlate incidents with Request-ID from access logs.
- Do not implement OpenTelemetry in this sprint.
- Do not add middleware or change public API contracts.
- Never log secrets with identifiers.

Code: `applications/observability/`.

---

END
