# Capacity Planning

Version: 1.0.0  
Sprint: Beta-3  
Assumptions only. Aligns with `deployment/SCALING_GUIDE.md` (unchanged).

## Single node

| Component | Replicas | Notes |
|-----------|----------|-------|
| nginx | 1 | TLS + routing |
| api | 1 | JSON storage = single-writer |
| portal | 1 | Stateless |
| worker | 0 | Reserved — do not run |

Fits beta and small production. Vertical scale API CPU/memory first.

## Medium deployment

| Component | Replicas | Notes |
|-----------|----------|-------|
| nginx | 1 | Or 1 LB + 1 nginx |
| api | 1 | Still single-writer unless storage is shared |
| portal | 2 | `least_conn` |
| worker | 0 | Reserved |

## Large deployment

| Component | Replicas | Notes |
|-----------|----------|-------|
| Load balancer | 1+ | TLS may move off nginx |
| nginx | 2+ | Edge HA |
| api | 2+ | **Only** with shared multi-writer-safe storage |
| portal | N | Horizontal, stateless |
| worker | reserved | Do not scale; do not enable as a latency fix |

## Horizontal assumptions

- Portal scales freely.
- API does **not** scale on JSON file backend.
- Worker reservation remains: no queue-based scale-out in v1.0 ops model.
- Autoscale is off. Page ops if CPU > 70% for 10 minutes.

## Analysis concurrency

Single-node p95 analysis < 30 s assumes modest concurrent POSTs. Shed load at the edge rather than adding unbound workers.

---

END
