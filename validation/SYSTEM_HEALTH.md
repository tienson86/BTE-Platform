# BTE Platform — RC1 System Health

**Date:** 2026-07-24  
**Version:** 1.0.0

---

## Overall

| Metric | Value |
|--------|-------|
| Code Health | **7.0 / 10** |
| Real cases | **20 / 20 PASS** |
| Orchestrator warnings (runner) | **0** |
| Pipeline exceptions | **0** |
| Circular import (public probe) | **None** |
| Release Ready? | **NO** |

---

## Engine health matrix

| Engine | Input | Output | Validation | Timing (sample ms) | Memory |
|--------|-------|--------|------------|-------------------:|--------|
| Calendar | Y/M/D H:M | Calendar result | Runtime OK | 1.1 | Shared trace |
| Bazi | Calendar + gender | Chart (+ day_master property) | Runtime OK; API omit day_master | 0.06 | Shared trace |
| Pattern | PatternContext | Pattern result | Runtime OK | 5.85 | Shared trace |
| Score | calendar/bazi/pattern | Score result | Runtime OK | 272.96 | Shared trace |
| Interpretation | prior stages | Interpretation | Runtime OK | 351.56 | Shared trace |
| Report | Interpretation | Report | Runtime OK | 63.22 | Shared trace |
| Narrative | Interp + Report | Narrative | Runtime OK | 375.80 | Shared trace |

Peak traced memory (one full pipeline sample): **~1.11 MB** (`tracemalloc`).

Cold analyze (orchestrator): **~594 ms**  
Warm analyze: **~282 ms**  
20-case average: **~267 ms**

---

## Surface health

| Surface | Check | Status |
|---------|-------|--------|
| API health | `GET /api/v1/health` | OK |
| API analyze | `POST /api/v1/analyze` | OK |
| Admin API | JWT + ADMIN | OK (401/403/200) |
| License | `/api/v1/license/status` | OK |
| Web Admin UI | `/`, `/healthz` | OK |
| Customer Portal | `/`→analyze, `/healthz` | OK |

---

## Contract notes

- Structural validation for real cases requires day pillar presence.
- Missing `day_master` in API JSON recorded as **NOTE** on all 20 cases (not hard FAIL).
- API response envelope: `{ success, message, data, request_id }`.

---

## Health risks

1. Public engine endpoints without auth.
2. Timezone parameter unused.
3. Legacy duplicate packages increase misconfiguration risk.
4. Default JWT secret in env examples.
5. In-memory user store unsuitable for multi-instance prod.

---

## Code Health: **7.0 / 10**
