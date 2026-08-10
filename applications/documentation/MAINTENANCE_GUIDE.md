# Maintenance Guide

Version: 1.0.0  
Sprint: Beta-3

Modes are **declared contracts**. Runtime gates are not implemented in this sprint.

| Mode | Intent |
|------|--------|
| Maintenance | Edge 503; no writes |
| Read only | Reads yes; writes no |
| Drain | No new traffic; finish in-flight |
| Startup | live then ready then traffic |
| Shutdown | drain timeout 30s then exit |

Operator procedure: `applications/runbooks/MAINTENANCE_WINDOW.md`.  
Edge 503 pattern: `deployment/OPERATIONS_RUNBOOK.md`.

---

END
