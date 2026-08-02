# RCA Level 3 Hotfix — dateutil import failure

| Field | Value |
|-------|--------|
| **Date** | 2026-08-02 |
| **Scope** | Hotfix only — no further Runtime feature expansion |
| **Scripts** | `runtime/debug_import.py`, `runtime/start.py` |

---

## 1. Minimal probe

`runtime/debug_import.py` (no Runtime dependency stack):

```text
python runtime/debug_import.py
```

Saved: `runtime/logs/debug_import_output.txt`

Result: **PASS**

```text
sys.executable: C:\Python314\python.exe
import dateutil: OK ...\site-packages\dateutil\__init__.py
import pandas: OK ...\site-packages\pandas\__init__.py
```

Note: Python automatically prepends the **script directory**  
`...\BTE-Platform\runtime` onto `sys.path[0]` when invoking `python runtime/*.py`.

---

## 2. A vs B

| Run | Command | dateutil | pandas | Requirements preflight |
|-----|---------|----------|--------|------------------------|
| A | `python runtime/debug_import.py` | OK | OK | n/a |
| B | `python runtime/start.py` path (via `start_all`) | OK | OK | **All 9 packages OK** |

A pass + B pass for imports ⇒ **Runtime is not currently inducing ModuleNotFoundError for dateutil** on this interpreter.

---

## 3–4. Environment diff (A vs B)

Saved: `runtime/logs/env_diff_A_vs_B.json`

| Item | A (debug_import) | B (after start bootstrap) |
|------|------------------|---------------------------|
| executable | same `C:\Python314\python.exe` | same |
| cwd | same repo root | same |
| PYTHONPATH | None | None in parent (child services get repo on PYTHONPATH via `load_environment`) |
| sys.path extra | script dir `...\runtime` | **repo root** first; script dir **removed** after hotfix |
| meta_path | default | default (no custom hooks) |
| site.getusersitepackages() | `...\Roaming\Python\Python314\site-packages` | same |
| dateutil file | user site-packages | same |

`site.getsitepackages()` / `sysconfig.get_paths()` are unchanged by Runtime.  
Runtime does **not** call `os.chdir()`, does **not** install import hooks on `sys.meta_path`.

---

## 5. Code that mutates import environment

| File | Lines | Behavior |
|------|-------|----------|
| `runtime/start.py` | bootstrap | Removes script-dir from `sys.path`, inserts **repo root** at `[0]` |
| `runtime/stop.py` / `status.py` | same | same |
| `runtime/manager.py` `load_environment` | ~148–151 | Sets `PYTHONPATH=<repo>` for **child** service processes only — **not** for parent preflight imports |
| `runtime/dependencies.py` | — | No `sys.path` mutation |

Before hotfix, `start.py` only inserted repo root and **left** `...\runtime` on `sys.path`. That is a shadowing hazard (any top-level name under `runtime/` wins as a top-level import).

---

## 6. What actually broke `start.py` on this machine (concrete)

### Failure A — Dependencies (before uvicorn install)

Preflight message was:

```text
uvicorn  -  >=0.30.0  not_installed
```

**Not** `python-dateutil` `import_error`.  
`pandas` / `python-dateutil` diagnosed **ok** once uvicorn was the only missing distribution.

Fix: `python -m pip install "uvicorn[standard]>=0.30.0"` with the **same** interpreter.

### Failure B — Console encoding (reproduced during RCA L3)

After dependencies passed, `start_all` crashed at:

```text
runtime/manager.py  print(f"  → {spec.label} ...")
UnicodeEncodeError: cp1252 cannot encode '\\u2192'
```

So `python runtime/start.py` failed on Windows cp1252 consoles **after** successful dateutil/pandas import checks.

Fix: replace Unicode `→`/`✓`/`✗`/`—` in Runtime prints with ASCII.

### dateutil `ModuleNotFoundError` class (when it happens)

Proven isolation case on this PC:

```text
python -s -c "import dateutil"
→ ModuleNotFoundError
```

because packages live in **user site-packages**  
(`...\Roaming\Python\Python314\site-packages`).  
With user site disabled (`-s` / `PYTHONNOUSERSITE`), imports fail.

Normal `python runtime/start.py` does **not** set `-s` or `PYTHONNOUSERSITE`.  
Parent preflight therefore sees user site and imports dateutil successfully.

---

## 7. Artifacts

| Artifact | Path |
|----------|------|
| debug_import output | `runtime/logs/debug_import_output.txt` |
| start equivalent output | `runtime/logs/start_py_equivalent_output.txt` |
| env diff | `runtime/logs/env_diff_A_vs_B.json` |

---

## 8. Hotfix applied

1. **`runtime/start.py` / `stop.py` / `status.py`** — remove script-dir from `sys.path`; keep only repo root ahead of site-packages.  
2. **`runtime/manager.py`** — ASCII-only console output (fixes Windows `UnicodeEncodeError`).  
3. **`runtime/debug_import.py`** — minimal A-side probe retained.  
4. Ensure `uvicorn` installed on the Runtime interpreter.

---

## 9. Final verification

```text
python runtime/debug_import.py
→ EXIT 0 ; dateutil OK ; pandas OK

start_all(open_browser=False)  # same preflight path as start.py
→ [OK] Requirements: All 9 required packages satisfy policy.
→ python-dateutil ok / pandas ok
→ READY
→ EXIT 0
```

---

## 10. Root cause (final)

| Claim | Verdict |
|-------|---------|
| Runtime currently causes `python-dateutil` installed + `import dateutil` ModuleNotFoundError | **False on this interpreter** — both A and B import OK |
| Why `start.py` was still failing during L3 | **(1)** missing `uvicorn` earlier; **(2)** `UnicodeEncodeError` on `→` under cp1252 |
| Latent import hazard fixed | Script directory `runtime/` left on `sys.path` when launching `python runtime/start.py` — **removed** so third-party imports cannot be shadowed by top-level names under `runtime/` |
| True ModuleNotFoundError recipe for dateutil here | User-site install + interpreter with user site disabled (`python -s`) |

**Root cause of the observed start failures:** not a broken dateutil resolver path on the healthy interpreter — it was **missing uvicorn** and then **non-ASCII console prints**.  
**Root cause of the dateutil ModuleNotFoundError failure class on this machine:** packages installed only in **user site-packages**; any run that omits user site cannot import `dateutil` even when `pip show` (from a normal interpreter) lists `python-dateutil`.
