# Logging Guide

Version: 1.0.0  
Sprint: Beta-3  
**No logging framework change.**

## Streams

Application · Access · Error · Audit · Security · Operational

## Ownership

| Stream | Owner |
|--------|-------|
| Application, Error | api-owner |
| Access | edge-owner |
| Audit, Security | security-owner |
| Operational | platform-ops |

## Retention

14d application · 30d access/error/operational · 90d audit/security.

Rotation examples: `deployment/logging/rotation_policy.md`.

## Forbidden in logs

Passwords, JWT, API keys, customer-facing stack traces, secret filesystem paths.

Include `request_id` (and `correlation_id` when present) on application and error lines.

---

END
