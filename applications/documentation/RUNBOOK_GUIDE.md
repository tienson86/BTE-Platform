# Runbook Guide

Version: 1.0.0  
Sprint: Beta-3

## How to use

1. Identify symptom (unavailable, slow, full disk, failed backup).
2. Open the matching file in `applications/runbooks/`.
3. Capture identifiers (Request-ID). Mitigate. Then recover and smoke.
4. File incident with timeline and error-budget impact.

## Severity (ops)

| SEV | Meaning |
|-----|---------|
| 1 | API or portal down; data-loss risk |
| 2 | SLO burn (latency/errors) or backup RPO risk |
| 3 | Degraded single non-critical job |

## Do not

Change engines, knowledge, pipelines, UI, or AF-1 during incident response.

---

END
