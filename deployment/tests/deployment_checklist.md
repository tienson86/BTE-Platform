# Deployment checklist (ops tests)

- [ ] Images build from repo root (`Dockerfile.api`, `Dockerfile.portal`, `Dockerfile.worker`).  
- [ ] Dev compose: api `/health` 200, portal `/healthz` 200.  
- [ ] Beta/prod: API not published on host; nginx `/health` `/version` 200.  
- [ ] Env files used for secrets are **outside** git.  
- [ ] No domain literal in nginx (`server_name _`).  
- [ ] JWT example strings are placeholders only.  
- [ ] Backup archive created; `--verify` restore succeeds.  
- [ ] Rollback tag documented.  
- [ ] AF-1 / engines / UI / contracts untouched in the release diff.

---

END
