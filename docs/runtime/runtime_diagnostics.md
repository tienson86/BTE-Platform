# Runtime Diagnostics

| Field | Value |
|-------|--------|
| **Document** | `runtime_diagnostics.md` |
| **Version** | `2.0.0` |
| **Module** | `runtime/diagnostics.py` |

---

## 1. Purpose

Define the three diagnostic artifacts produced during Runtime preflight so operators can debug startup without reading Engine code.

---

## 2. Report types

### 2.1 Environment Report

Snapshot of the interpreter hosting Runtime.

| Field | Source |
|-------|--------|
| `python_version` | `platform.python_version()` |
| `executable` | `sys.executable` |
| `platform` / `machine` | `platform.*` |
| `cwd` | `Path.cwd()` |
| `project_root` | repository root |
| `timestamp_utc` | UTC ISO-like stamp |
| `python_ok` | `>= 3.10` |

Builder: `build_environment_report()`.

### 2.2 Dependency Report

Output of Dependency Resolver V2 for the Version Policy set.

| Field | Description |
|-------|-------------|
| `packages[]` | Per-package diagnosis |
| `ok` | All packages status=`ok` |
| `summary` | One-line rollup |
| `counts` | `total`, `ok`, `not_installed`, `import_error`, `version_conflict` |

Each package row:

| Field | Description |
|-------|-------------|
| `package` | Distribution name |
| `import_name` | Module imported |
| `installed` | Version or null |
| `required` | Specifier |
| `status` | See policy doc |
| `suggested_command` | Exact pip command |
| `error` | Optional detail |

Builder: `build_dependency_report()`.

### 2.3 Startup Diagnostics

Combined payload used at preflight:

```text
StartupDiagnostics
  ├─ environment: EnvironmentReport
  ├─ dependencies: DependencyReport
  ├─ ready: python_ok AND dependencies.ok
  ├─ timestamp_utc
  └─ notes[]
```

Builder: `build_startup_diagnostics()`.

---

## 3. Persistence

On every Requirements preflight check, Runtime writes:

| File | Role |
|------|------|
| `runtime/logs/startup_diagnostics_latest.json` | Machine-readable latest |
| `runtime/logs/startup_diagnostics_latest.txt` | Human-readable latest |
| `runtime/logs/startup_diagnostics_<UTC>.json` | Run archive |
| `runtime/logs/startup_diagnostics_<UTC>.txt` | Run archive |

API: `write_diagnostics_files(diag)`.

---

## 4. Console presentation

On failure, `check_requirements()` prints:

1. Summary line (counts)
2. Table: **Package | Installed | Required | Status | Suggested command**
3. Optional `detail:` lines for import/version errors
4. Pointer: `See runtime/logs/startup_diagnostics_latest.txt`

---

## 5. Distinguishing failures

| Symptom | Status | Typical fix |
|---------|--------|-------------|
| `pip list` has package under another name | Use distribution name in table (`python-dateutil` not `dateutil`) | Already handled by Resolver |
| Row `Installed=—`, `not_installed` | Not in this interpreter | Run suggested `pip install` with **same** `python` |
| Row has version, `import_error` | Broken / incomplete install | Reinstall; check DLL / architecture |
| Row has version, `version_conflict` | Too old/new | Upgrade via suggested command |
| `pip list` shows package but Runtime fails | Different interpreter | Align `python -m pip` with `python runtime/start.py` |

---

## 7. Import Forensics V3

When any package status is `import_error`, Runtime also writes:

| File | Role |
|------|------|
| `runtime/logs/import_forensics_latest.json` | Machine-readable forensic bundle |
| `runtime/logs/import_forensics_latest.txt` | Human-readable forensic bundle |
| `runtime/logs/import_forensics_<UTC>.*` | Run archive |

Each record includes:

1. `sys.executable`  
2. Python version  
3. CWD  
4. Full `sys.path`  
5. `find_spec()` payload  
6. Distribution metadata (version, requires, top_level, locate_init)  
7. `module.__file__` when partially available  
8. Full traceback  
9. Timestamp (UTC)  
10. Platform information  
11. Env: `PYTHONPATH`, `VIRTUAL_ENV`, `PYTHONHOME`, …  
12. Dependency chain (e.g. `pandas → python-dateutil → dateutil`)

Module: `runtime/import_forensics.py`.

Goal: even a **single** transient ImportError leaves enough evidence for post-incident investigation.

---

## 8. Related documents

- [runtime_startup_spec.md](runtime_startup_spec.md)
- [runtime_dependency_policy.md](runtime_dependency_policy.md)
- RCA L2: `docs/reports/runtime_dateutil_import_rca_l2.md`
