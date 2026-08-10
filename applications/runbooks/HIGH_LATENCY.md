# Runbook — High Latency

Trigger example: API `request_latency` p95 above SLO, or user-visible analysis delay.

## Detect

- Synthetic probe time for `/health` rising (should stay well under 200 ms).
- Analysis duration complaints (pipeline histograms are catalogued, not instrumented in Beta-3).
- Nginx upstream timed out.

## Triage

1. Separate edge latency vs API vs portal.
2. Check CPU/memory (`HIGH_MEMORY.md`) and disk (`DISK_FULL.md`).
3. Check concurrent analysis load. JSON storage is single-writer — do not scale API replicas as a first fix.
4. Confirm no accidental engine debug logging flood.

## Mitigate

1. Drain extra traffic if a misconfigured client is looping.
2. Restart API if event-loop blocked (capture logs first).
3. Defer non-critical ops jobs (backup) if they saturate disk I/O.
4. Do not tune engines or pipelines during the incident.

## Recover

Record p95 before/after. File a capacity note if load is genuine (`CAPACITY_PLANNING.md`).

---

END
