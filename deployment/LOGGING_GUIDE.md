# Logging Guide

Version: 1.0.0  
Sprint: Beta-1  
**No logging framework changes.**

---

## Streams

| Stream | Producer | Destination |
|--------|----------|-------------|
| Application | uvicorn / Python logging | `bte-logs/app.log` (stdout also) |
| Access | Nginx | `/var/log/nginx/access.log` |
| Error | Nginx + app exceptions | `/var/log/nginx/error.log`, app stderr |
| Audit | Auth / admin actions (existing app logs) | app log with `AUDIT` logger name if present |

Format (app, existing): `%(asctime)s | %(levelname)s | %(name)s | %(message)s`

Request correlation: existing `X-Request-ID` (do not change middleware).

---

## Rotation & retention

See [logging/rotation_policy.md](./logging/rotation_policy.md) and [logging/logback.md](./logging/logback.md).

Default: daily rotate, 14 days app, 30 days access, do not log secrets or JWT.

---

END
