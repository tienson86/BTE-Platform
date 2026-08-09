# Security Baseline

Version: 1.0.0  
Sprint: Beta-1

---

## Transport

- HTTPS at nginx (TLS files mounted, not baked into images).  
- HSTS enabled when TLS is on (`security.conf`).  
- No domain names hardcoded.

## Headers

CSP (report-only or strict default-src 'self'), `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`.

## Rate limit

Nginx `limit_req` **placeholder** zone in `security.conf` (conservative burst). Tune per site; not an API code change.

## Secrets

- `BTE_JWT_SECRET` and TLS keys via env file / secret mount.  
- Never commit production env.  
- Least privilege: containers run as non-root `bte`.

## Container

- Slim Python base  
- No shell in production CMD  
- Read-only engine mount  
- Drop unnecessary capabilities at orchestrator (documented; compose comment)

## Dependencies

Scan images with `pip-audit` / `docker scout` in CI (documented pipeline). Do not auto-upgrade engines.

---

END
