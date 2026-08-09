# Monitoring Guide

Version: 1.0.0  
Sprint: Beta-1  
**No application instrumentation changes.** Specs only.

---

## Stack (optional sidecar)

- Prometheus scrapes nginx stub_status (if enabled) and container `/health` via blackbox or scrape of existing endpoints.  
- Grafana dashboards: `deployment/monitoring/grafana/dashboards/`.

---

## Metrics catalog (expected / external)

| Metric | Source | Meaning |
|--------|--------|---------|
| `up` | Prometheus | Job reachable |
| `probe_success` | Blackbox → `/health` | Liveness |
| `nginx_http_requests_total` | Nginx exporter (optional) | Traffic |
| Container CPU/mem | cAdvisor / Docker | Saturation |
| Restart count | Docker | Instability |

Application-level business metrics are **out of scope** (no code change).

---

## Dashboards

- `bte-platform-overview.json` — health + restart + latency placeholder panels.  
- Datasource: Prometheus UID `bte-prom`.

---

END
