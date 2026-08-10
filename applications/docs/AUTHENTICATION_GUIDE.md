# Authentication Guide

Version: 1.0.0  
Sprint: Beta-2  
Status: Placeholder only

No login implementation in this sprint.

## Bearer Token

```
Authorization: Bearer <token>
```

The public middleware records that a Bearer token is present. It does not validate signature, expiry, or claims.

## API Key (reserved)

```
X-API-Key: <key>
```

Reserved. Not validated.

## Refresh Token (reserved)

```
X-Refresh-Token: <token>
```

Reserved. No refresh or session flow.

## Role (reserved)

```
X-Role: <role>
```

Reserved. No RBAC enforcement in this layer.

## Future behavior

When authentication is enabled:

- Missing credentials → `BTE-401-UNAUTHORIZED`
- Insufficient role → `BTE-403-FORBIDDEN`
- Public probes `/health` `/live` `/ready` `/version` remain unauthenticated

---

END
