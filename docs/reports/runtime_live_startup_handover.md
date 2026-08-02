# Live Startup Debug — Handover

| Field | Value |
|-------|--------|
| **Date** | 2026-08-02 |
| **Command** | `python runtime/start.py` |
| **Result** | **READY** (exit 0) — no Startup aborted |

Trace log: `runtime/logs/startup_trace_live.txt`

---

## 1. Startup Trace (last successful run)

```text
STEP 1: force UTF-8 stdio
STEP 2: bootstrap sys.path
STEP 2 OK: repo root = ...\BTE-Platform
STEP 3: import runtime.manager
STEP 3 OK
STEP 4: critical imports (dateutil, pandas)
  [before import dateutil] sys.executable / cwd / sys.path / find_spec logged
STEP 4 OK: import dateutil
STEP 4 OK: import pandas
STEP 5: call start_all
STEP 5.1: ensure_dirs
STEP 5.2: preflight Python     OK
STEP 5.3: preflight Requirements
STEP 5.3a: build_startup_diagnostics() [Dependency Resolver once]
STEP 5.3b: write_diagnostics_files()
STEP 5.3 Requirements OK
STEP 5.4: preflight Configuration OK
STEP 5.5: load_environment + load_services
STEP 5.6: start api / web_admin / customer_portal
STEP 5.7: wait_healthy — all Running
STEP 5.8: open_browser
READY
STEP FINAL: start_all returned exit=0
```

Last executed success marker: **`STEP FINAL: READY`**

---

## 2. Full traceback

None on the successful path.  
If STEP 4 import fails, `start.py` prints `traceback.print_exc()` then exits 1.

---

## 3. Call graph

```text
python runtime/start.py
  _force_utf8_stdio()
  _bootstrap_sys_path()          # remove runtime/ script-dir; insert repo root
  import runtime.manager
  main()
    _probe_critical_imports()    # import_module("dateutil"); import_module("pandas")
    start_all(open_browser=True)
      ensure_dirs()
      check_python()             # once
      check_requirements()       # once
        build_startup_diagnostics()
          build_dependency_report()
            DependencyResolver.diagnose_all()   # imports each policy package
        write_diagnostics_files()
          write_import_forensics_from_diagnoses()  # only if import_error
      check_configuration()      # import_module(service modules) once each
      load_environment()         # sets PYTHONPATH for child procs only
      _start_service(api|admin|portal)
      wait_healthy(...)
      open_portal()              # non-fatal on error
      print READY
```

**Dependency Resolver call count in start path:** **1** (`check_requirements` → `build_startup_diagnostics`).

---

## 4. Other `pandas` / `dateutil` imports (grep)

### `dateutil`
No production `import dateutil` / `from dateutil` outside Runtime probe/resolver/tests.  
Engines do not import dateutil directly (pulled in via pandas).

### `pandas` (engines — loaded when API workers import app code, not in start.py parent until Configuration/service spawn)

| File |
|------|
| `engines/core/base_loader.py` |
| `engines/core/base_validator.py` |
| `engines/calendar_engine/core/loader.py` |
| `engines/calendar_engine/core/exporter.py` |
| `engines/score_engine/loader.py` |
| `engines/pattern_engine/loader.py` |
| `engines/pattern_engine/calculator.py` |
| `engines/pattern_engine/validator.py` |
| `engines/pattern_engine/rules/rule_loader.py` |
| `engines/strength_engine/loader.py` |
| `engines/temperature_engine/loader.py` |
| `engines/useful_god_engine/loader.py` |
| `engines/interpretation_engine/interpreter_runtime/interpreters/*/...` |

Runtime parent process critical imports: `runtime/start.py` STEP 4 + Dependency Resolver.

---

## 5. Root cause (this machine)

| Issue | Status |
|-------|--------|
| `dateutil` / `pandas` ModuleNotFoundError during start | **Not present** — STEP 4 OK, Requirements OK |
| Prior start blockers fixed earlier | missing `uvicorn`; Unicode `→` on cp1252; `runtime/` on `sys.path` |
| Current live run | **READY**, exit 0 |

---

## 6. Patch (this hotfix)

- `runtime/start.py` — STEP logs, UTF-8 stdio, pre-import probe with full traceback, sys.path bootstrap
- `runtime/manager.py` — STEP logs inside `start_all`; open_browser non-fatal; full traceback on service start failure

---

## 7. Confirmation

```text
python runtime/start.py
→ ... READY
→ STEP FINAL: start_all returned exit=0
→ no "Startup aborted"
```
