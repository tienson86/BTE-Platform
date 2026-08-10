# Runbook — High Memory / Exhaustion

## Detect

Container OOMKill, `memory` gauge near limit, host swap thrash.

## Triage

1. Which service? API (analysis) vs portal vs nginx.
2. `docker stats` and recent restart count.
3. Check for unbounded log growth (`DISK_FULL.md` often coincides).

## Mitigate

1. Restart the offending service (`SERVICE_RESTART.md`).
2. Raise container memory **only** as a temporary vertical scale (document the change).
3. Reduce concurrent analysis if operators can shed load at the edge.
4. Worker remains reserved — do not start extra workers to "help."

## Prevent

Single-node and medium topologies assume one API replica. Large topologies need shared storage before horizontal API scale.

---

END
