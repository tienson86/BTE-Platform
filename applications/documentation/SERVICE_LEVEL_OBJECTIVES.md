# Service Level Objectives

Version: 1.0.0  
Sprint: Beta-3  
Documentation only.

## Availability

| Environment | Target | Window |
|-------------|--------|--------|
| Beta | 99.5% | calendar month |
| Production | 99.9% | calendar month |

Measured on critical path: edge or API `/health` success (no new probe endpoints).

## Latency

| Probe | Target |
|-------|--------|
| `GET /health` p95 | < 200 ms |
| `GET /version` p95 | < 200 ms |
| Analysis POST p95 | < 30 s (single-node assumption; not instrumented) |

## Recovery

| Objective | Target |
|-----------|--------|
| RTO (API/portal restore to healthy) | 1 hour |
| RPO (verified backup age) | 24 hours |
| Drain timeout (contract) | 30 seconds |

## Error budget

Monthly error budget = `1 - availability_target`.

Example production: 0.1% unavailability ≈ 43 minutes / 30-day month.

Burn the budget on SEV-1/2 incidents. Freeze non-critical releases if budget is exhausted.

---

END
