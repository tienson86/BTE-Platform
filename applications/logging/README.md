# Logging

Version: 1.0.0  
Sprint: Beta-3

Standardize streams only. Do not change Python logging or nginx config in this sprint.

| Stream | Owner | Retain |
|--------|-------|--------|
| Application | api-owner | 14 days |
| Access | edge-owner | 30 days |
| Error | api-owner | 30 days |
| Audit | security-owner | 90 days |
| Security | security-owner | 90 days |
| Operational | platform-ops | 30 days |

Deployment rotation examples remain in `deployment/logging/`.

---

END
