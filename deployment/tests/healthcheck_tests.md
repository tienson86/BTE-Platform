# Healthcheck tests (manual / CI smoke)

```bash
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1:8000/version
curl -fsS http://127.0.0.1:8000/api/v1/health
curl -fsS http://127.0.0.1:8081/healthz
# via nginx (beta/prod)
curl -fsS http://127.0.0.1/health
curl -fsS http://127.0.0.1/live
curl -fsS http://127.0.0.1/ready
curl -fsS http://127.0.0.1/version
```

Expect HTTP 200. `/live` and `/ready` are nginx aliases to existing `/health` — no new app routes.

---

END
