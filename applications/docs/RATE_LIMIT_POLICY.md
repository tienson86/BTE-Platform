# Rate Limit Policy

Version: 1.0.0  
Sprint: Beta-2  
Status: Placeholder only

Enforcement is **not** enabled. Middleware exposes reserved headers only.

## Intended signal

| Item | Value |
|------|--------|
| HTTP | `429 Too Many Requests` |
| Error code | `BTE-429-RATE_LIMITED` |
| Header | `Retry-After: <seconds>` |
| Header | `X-RateLimit-Limit` |
| Header | `X-RateLimit-Remaining` |

## Example policy (not enforced)

| Class | Limit | Window |
|-------|-------|--------|
| Anonymous | 60 requests | 60 seconds |
| Authenticated | 300 requests | 60 seconds |
| Analysis POST | 10 requests | 60 seconds |

## Example error

```json
{
  "code": "BTE-429-RATE_LIMITED",
  "message": "Rate limit exceeded. Retry after the indicated interval.",
  "details": {
    "reason": "Placeholder policy. Enforcement is not enabled in Beta-2."
  },
  "request_id": "req_123",
  "timestamp": "2026-08-10T00:00:00Z"
}
```

```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 0
```

---

END
