# Error Model

Version: 1.0.0  
Sprint: Beta-2

## Canonical body

```json
{
  "code": "BTE-404-NOT_FOUND",
  "message": "The requested resource was not found.",
  "details": {
    "field": "id",
    "reason": "Analysis resource was not found.",
    "context": []
  },
  "request_id": "req_123",
  "timestamp": "2026-08-10T00:00:00Z"
}
```

## Codes

| Code | HTTP | Meaning |
|------|------|---------|
| `BTE-400-VALIDATION` | 400 | Request failed contract validation |
| `BTE-400-UNSUPPORTED_VERSION` | 400 | API version not supported |
| `BTE-401-UNAUTHORIZED` | 401 | Auth required (reserved) |
| `BTE-403-FORBIDDEN` | 403 | Role denied (reserved) |
| `BTE-404-NOT_FOUND` | 404 | Resource not found |
| `BTE-409-CONFLICT` | 409 | State conflict (reserved) |
| `BTE-429-RATE_LIMITED` | 429 | Rate limit (placeholder) |
| `BTE-500-INTERNAL` | 500 | Unexpected failure |
| `BTE-501-NOT_IMPLEMENTED` | 501 | Reserved endpoint |
| `BTE-503-PIPELINE_UNBOUND` | 503 | Pipeline not bound |
| `BTE-503-UNAVAILABLE` | 503 | Temporary unavailability |

## Never expose

- Stack traces
- Python exception types
- Filesystem paths
- Engine internals
- Secrets or tokens

Exception mapping: `applications/errors/exception_mapper.py`

---

END
