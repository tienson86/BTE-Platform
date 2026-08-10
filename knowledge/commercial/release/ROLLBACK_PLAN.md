# Rollback Plan

Version: 1.0.0  
Sprint: Beta-4

Commercial wrapper around deployment rollback. Technical steps: `deployment/OPERATIONS_RUNBOOK.md` and `applications/runbooks/DEPLOYMENT_FAILURE.md` (do not modify those in this sprint).

## Trigger

Failed smoke after go-live, SEV-1 lasting beyond first mitigate, or data-risking defect.

## Steps

1. Announce internal rollback (ops + support).  
2. Stop further customer invites.  
3. Redeploy previous `BTE_IMAGE_TAG`.  
4. Smoke `/health`, `/version`, portal `/healthz`.  
5. Customer note: brief, no blame, no stack traces (`COMMUNICATION_PLAN.md`).  
6. Defect ticket; no emergency engine rewrite.

## Commercial

Do not invent refunds here. Finance + counsel decide if any commercial remedy applies.

---

END
