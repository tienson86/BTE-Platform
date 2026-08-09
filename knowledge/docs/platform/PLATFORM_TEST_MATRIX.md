# Platform Test Matrix

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_TEST_MATRIX |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | Architecture Board |

Testing rules remain: prefer source fixes; do not edit tests, golden datasets, snapshots, or expected outputs to force green unless explicitly requested.

---

## Module test surfaces (canonical)

| Module | Path | Scope |
|--------|------|-------|
| Analysis | `tests/analysis_engine/` | AX-1 / AX-2 pipeline, contracts, determinism, regression |
| Decision | `tests/decision_engine/` | AX-3 |
| Luck | `tests/luck_engine/` | LE-1/2/3 + AX-4 |
| Interpretation | `tests/interpretation_engine/` | IE-1/2/3 + IX-1 |
| Report | `tests/report_engine/` | RE-1/2/3 + RX-1 |
| Calendar / Bazi / Score / Pattern | `tests/calendar`, `tests/bazi`, `tests/score`, `tests/pattern` | Engine isolation |
| Knowledge packages | `knowledge/packages/*/tests/` | Package-local assertions |

Command pattern: `python -m pytest tests/<module> -q` only. Full-repo pytest only when the user or Release Manager requests it.

---

## Cross-cutting suites (existing; not modified by AF-1)

| Suite | Path | Freeze rule |
|-------|------|-------------|
| Golden Dataset | `tests/golden_dataset/` | Immutable expected outputs |
| API | `applications/api/tests/`, `tests/analysis_api/` | Public contracts |
| Portal | `applications/customer_portal/tests/` | UI; Foundation visual packs remain frozen |
| Integration | `tests/integration/` | Cross-engine; no reverse-import exceptions |

---

## Canonical pipeline test classes

Each canonical pipeline suite covers:

- Normal execution
- Missing required inputs
- Dependency violations
- Contract / version violations
- Duplicate publication
- Deterministic repeated execution
- Regression of upstream component contracts and checksums

---

## AF-1 test impact

| Item | Status |
|------|--------|
| New tests added by AF-1 | None |
| Existing tests modified | None |
| Golden / snapshot / expected edited | None |

Documentation-only freeze. Prior module results remain the evidence of runtime readiness.
