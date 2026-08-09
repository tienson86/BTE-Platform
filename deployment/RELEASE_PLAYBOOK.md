# Release Playbook

Version: 1.0.0  
Sprint: Beta-1

---

## Pipeline stages

1. **Build** images (`api`, `portal`, `worker`).  
2. **Test** — existing module CI (do not expand scope here).  
3. **Package** — tag `bte-api:<gitsha>`, `bte-portal:<gitsha>`.  
4. **Deploy Beta** — compose.beta + beta env; smoke.  
5. **Manual approval** — product + ops.  
6. **Deploy Production** — compose.production.  
7. **Rollback** — previous tag if smoke fails.

## Smoke (minimum)

- `GET /health` 200  
- `GET /version` 200  
- `GET /healthz` portal 200  
- Open `/dashboard` HTML 200  
- Optional: one known `/analysis` fixture (existing tests; no new contract)

## Freeze

Do not ship engine, pipeline, Knowledge, or API contract diffs in a Beta-1 hotfix unless a separate change request exists.

---

END
