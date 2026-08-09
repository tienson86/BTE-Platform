# Disaster Recovery

Version: 1.0.0  
Sprint: Beta-1

---

## Objectives

| Objective | Target (Beta-1) |
|-----------|-----------------|
| RPO | 24 hours (daily backup) |
| RTO | 4 hours (restore + smoke + DNS/TLS intact) |

Tighten after postgres + multi-AZ (future).

---

## Scenarios

| Failure | Response |
|---------|----------|
| Single container crash | Restart policy + healthcheck |
| Host loss | New host, restore volumes, same compose + env from secret store |
| Bad release | Rollback image tag (RELEASE_PLAYBOOK) |
| Data corruption | Restore last verified backup |
| Knowledge mismatch | Checkout matching git tag; do not mix engine SHA with API SHA |

## Recovery checklist

1. Declare incident.  
2. Maintenance 503.  
3. Restore per RESTORE_PROCEDURE.  
4. Verify `/health` `/version`.  
5. One analysis smoke.  
6. Open traffic.  
7. Postmortem within 48h.

---

END
