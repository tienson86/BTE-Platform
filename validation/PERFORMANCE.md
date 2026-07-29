# BTE Platform — RC1 Performance

**Date:** 2026-07-24  
**Machine:** local Windows audit host  
**Source:** `validation/perf_raw.json` + `validation/rc1_audit_runner.py`  
**Note:** Absolute numbers are environment-specific; use for relative RC1 baselines.

---

## Pipeline latency (orchestrator)

| Metric | ms |
|--------|---:|
| Cold analyze | 594.42 |
| Warm analyze | 282.17 |
| 20-case average | 267.30 |
| 20-case min | 207.00 |
| 20-case max | 345.97 |

---

## Engine stage latency (sample case)

| Stage | ms |
|-------|---:|
| calendar | 1.10 |
| bazi | 0.06 |
| pattern | 5.85 |
| score | 272.96 |
| interpretation | 351.56 |
| report | 63.22 |
| narrative | 375.80 |
| **sum (approx)** | **~1070** |

Dominant stages: **narrative**, **interpretation**, **score**.

Knowledge/rule work is embedded in stage times (no separate cold knowledge-load counter beyond first cold analyze).

---

## Memory

| Metric | Value |
|--------|------:|
| Peak traced (one pipeline) | 1,158,760 bytes (~1.11 MB) |

`tracemalloc` peak only; not RSS of full process / multi-worker.

---

## API latency (TestClient)

| Endpoint | Observation |
|----------|-------------|
| `GET /api/v1/health` | ~0.5–1.3 s first hit (app import/startup amortization) |
| `POST /api/v1/analyze` | ~1.1–2.3 s including client/app overhead |
| Admin GETs (warm, authed) | typically &lt; 50 ms |
| License status | ~4 ms |

TestClient timings include framework overhead and are not production p99.

---

## Report / narrative time

| Component | Sample ms |
|-----------|----------:|
| Report | 63.22 |
| Narrative | 375.80 |

---

## Knowledge load

Not isolated as a dedicated timer in RC1 harness. Proxy signals:

- Cold analyze (~594 ms) includes first-touch imports + knowledge/rules.
- Warm analyze (~282 ms) approximates repeat pipeline cost.

---

## Performance observations

1. Score + Interpretation + Narrative dominate wall time.
2. Calendar/Bazi/Pattern are cheap after warm-up.
3. No hard SLA defined in repo for RC1; recommend establishing p50/p95 targets before GA.
4. API first-request latency inflated by lazy imports — consider process warm-up in deployment health checks.

---

## Performance baseline status: **Recorded (RC1)**
