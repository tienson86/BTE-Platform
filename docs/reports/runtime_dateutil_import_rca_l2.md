# Runtime Preflight — RCA Level 2: python-dateutil installed, import dateutil failed

| Field | Value |
|-------|--------|
| **Date** | 2026-08-02 |
| **Symptom** | Resolver V2: distribution `python-dateutil` present, status `import_error` for import `dateutil` |
| **Interpreter under test** | `C:\Python314\python.exe` (3.14.6) |

---

## Executive conclusion

On the current workspace interpreter, **`import dateutil` succeeds**.  
There is **no** project-local `dateutil.py` / `dateutil/` shadow.

So the reported `import_error` is **not reproducible now** as a broken install on this interpreter.  
The highest-risk latent cause for that exact symptom class remains:

1. **`sys.path` shadowing** (repo root inserted at `sys.path[0]` by Runtime entrypoints), or  
2. **Broken / partial wheel** (metadata present, importable files missing or failing), or  
3. **Different interpreter** than the one used for `pip list`.

Resolver V2 was hardened to distinguish (1) vs (2) via isolated file-location import + shadow scan.

---

## Checklist results

### 1. Direct `import dateutil` (same interpreter)

```text
OK
file: C:\Users\MG\AppData\Roaming\Python\Python314\site-packages\dateutil\__init__.py
version: 2.9.0.post0
submodules: parser, tz, relativedelta OK
```

### 2. `sys.path` at preflight (with repo root inserted like `start.py`)

```text
00  <repo root>\BTE-Platform
01  C:\Python314\python314.zip
02  C:\Python314\DLLs
03  C:\Python314\Lib
04  C:\Python314
05  C:\Users\MG\AppData\Roaming\Python\Python314\site-packages
06  C:\Python314\Lib\site-packages
```

Runtime entrypoints **do** put the project root at index 0 (`runtime/start.py`, `stop.py`, `status.py`).  
That is required so `import runtime` resolves to the local package. It is also the mechanism that would make a future `dateutil/` under the repo shadow site-packages.

### 3. `importlib.util.find_spec("dateutil")`

```text
ModuleSpec(
  name='dateutil',
  origin='...\Python314\site-packages\dateutil\__init__.py',
  submodule_search_locations=['...\site-packages\dateutil']
)
```

### 4. `python -m pip show python-dateutil`

```text
Name: python-dateutil
Version: 2.9.0.post0
Location: C:\Users\MG\AppData\Roaming\Python\Python314\site-packages
Requires: six
Required-by: pandas
```

### 5. site-packages layout

```text
...\site-packages\dateutil\           EXISTS
...\site-packages\dateutil\__init__.py EXISTS
contents include: parser/, tz/, zoneinfo/, relativedelta.py, rrule.py, ...
```

`six` is installed (`1.17.0`) — required by python-dateutil.

### 6. Project shadowing scan

| Candidate | Found in repo? |
|-----------|----------------|
| `dateutil.py` | **No** |
| `dateutil/` package | **No** |

Only site-packages `dateutil/` appears on `sys.path`.

### 7. Broken package?

**Not on this interpreter.** Distribution files import cleanly.

If `import_error` returns with:

- `distribution_importable=False` → reinstall same interpreter  
- `distribution_importable=True` + shadows → remove shadow / fix `sys.path`

Repair command (same interpreter as Runtime):

```bash
python -m pip uninstall -y python-dateutil
python -m pip install "python-dateutil>=2.9"
python -c "import dateutil; print(dateutil.__file__)"
python runtime/start.py
```

### 8. Runtime `sys.path` changes

| Location | Behavior |
|----------|----------|
| `runtime/start.py` | inserts repo root at `sys.path[0]` before `import runtime` |
| `runtime/stop.py` | same |
| `runtime/status.py` | same |
| `runtime.manager.load_environment` | sets `PYTHONPATH=<repo>` for **child** service processes only |

**Preflight runs in the parent process after root insert.**  
That does **not** currently break `dateutil` (no local shadow). It remains the correct place to watch if `import_error` reappears.

Mitigations applied:

- Shared bootstrap comment / consistent path insert  
- `probe_import()` in Resolver: `find_spec`, shadow candidates, isolated dist import  
- On `import_error`, suggested command becomes **reinstall** or **remove shadow** depending on probe

---

## Root-cause matrix for the symptom class

| Condition | distribution metadata | `import dateutil` | Isolated dist import | Classification |
|-----------|----------------------|-------------------|----------------------|----------------|
| Healthy | present | OK | OK | `ok` |
| Shadowed by project/`sys.path` | present | FAIL or wrong module | OK | `import_error` + shadow detail |
| Broken wheel / missing files | present | FAIL | FAIL | `import_error` → reinstall |
| Wrong interpreter vs pip | present on A | FAIL on B | n/a | operator mismatch |

---

## Confirmation (this machine)

```text
DependencyResolver.diagnose(python-dateutil) → OK 2.9.0.post0
probe_import("dateutil") → importable True, shadowed False
```

Tests: `pytest tests/runtime -q`
