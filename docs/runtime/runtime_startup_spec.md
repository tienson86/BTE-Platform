# Runtime Startup Specification

| Field | Value |
|-------|--------|
| **Document** | `runtime_startup_spec.md` |
| **Version** | `2.0.0` |
| **Status** | Normative for desktop Runtime |
| **Entry** | `python runtime/start.py` |

---

## 1. Purpose

Define the commercial startup sequence for BTE Platform desktop Runtime: preflight → start services → health → ready.

Runtime orchestrates processes only. It does **not** execute Engine business logic.

---

## 2. Startup sequence

```text
python runtime/start.py
        │
        ▼
ensure_dirs (logs/, run/, …)
        │
        ▼
Preflight
  ├─ Python >= 3.10
  ├─ Dependency Resolver V2 (distribution + import + version)
  └─ Configuration (VERSION, services.json, app modules)
        │
        ▼ (all OK)
Start services (API → Admin → Portal)
        │
        ▼
Health poll (timeout)
        │
        ▼
Open Customer Portal (optional)
        │
        ▼
READY
```

Abort immediately on any preflight failure. Diagnostics are written under `runtime/logs/`.

---

## 3. Preflight gates

| Gate | Module | Pass criterion |
|------|--------|----------------|
| Python | `runtime.manager.check_python` | `sys.version_info >= (3,10)` |
| Requirements | `DependencyResolver` + `diagnostics` | All policy packages OK |
| Configuration | `check_configuration` | VERSION + services.json + importable service modules |

---

## 4. Dependency Resolver V2 (summary)

For each policy package:

1. **Resolve names** — distribution ↔ import (metadata + alias hints)
2. **Distribution** — `importlib.metadata`
3. **Import** — `importlib.import_module`
4. **Version** — compare installed vs Version Policy specifier

Failure classes:

| Status | Meaning |
|--------|---------|
| `not_installed` | Distribution absent |
| `import_error` | Distribution present, import failed |
| `version_conflict` | Import OK, version outside policy |
| `ok` | All checks passed |

See [runtime_dependency_policy.md](runtime_dependency_policy.md) and [runtime_diagnostics.md](runtime_diagnostics.md).

---

## 5. Services

Loaded from `configs/services.json` (order fixed):

1. API  
2. Web Admin  
3. Customer Portal  

Each service: spawn uvicorn module, PID file under `runtime/run/`, log under `runtime/logs/`, health URL poll.

---

## 6. Exit codes

| Code | Meaning |
|------|---------|
| `0` | READY |
| `1` | Preflight failed, start failed, or health failed |

---

## 7. Operator contract

Always use the **same interpreter** for install and start:

```bash
python -m pip install -r requirements.txt -r applications/requirements.txt
python runtime/start.py
```

Do not compare `pip` from Python A with Runtime from Python B.

---

## 8. Artifacts

| Artifact | Path |
|----------|------|
| Latest diagnostics (JSON) | `runtime/logs/startup_diagnostics_latest.json` |
| Latest diagnostics (text) | `runtime/logs/startup_diagnostics_latest.txt` |
| Per-run copies | `runtime/logs/startup_diagnostics_<UTC>.{json,txt}` |
| Service logs | `runtime/logs/*.log` |
| PID files | `runtime/run/*.pid` |
