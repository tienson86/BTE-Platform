# Runtime Preflight Dependency Checker — Root Cause Analysis

| Field | Value |
|-------|--------|
| **Date** | 2026-08-02 |
| **Component** | `runtime/start.py` → `runtime/manager.py` → `runtime/dependencies.py` |
| **Symptoms** | Preflight reports missing `pandas` / `dateutil` while `pip list` shows them installed |

---

## 1. How Runtime checked dependencies (before fix)

| Mechanism | Used? |
|-----------|-------|
| `importlib.import_module` | **Yes** — sole pass/fail criterion in `check_requirements()` |
| `importlib.metadata` | No |
| `pkg_resources` | No |
| `pip` CLI / subprocess | No |

Code path:

```text
python runtime/start.py
  → runtime.manager.start_all
  → check_requirements()
  → import_module(name) for name in REQUIRED_IMPORTS
```

Historical `REQUIRED_IMPORTS` mixed **import module names** (`dateutil`, `yaml`) with packages whose **pip distribution names** differ (`python-dateutil`, `PyYAML`).

---

## 2. Name matrix (pip vs import vs distribution)

| Pip / requirements.txt | Distribution (`importlib.metadata`) | Import (`import_module`) |
|------------------------|--------------------------------------|---------------------------|
| `pandas` | `pandas` | `pandas` |
| `python-dateutil` | `python-dateutil` | **`dateutil`** |
| `pyyaml` / `PyYAML` | `pyyaml` | **`yaml`** |
| `numpy` | `numpy` | `numpy` |
| `fastapi` | `fastapi` | `fastapi` |

Verified on this machine:

- `import_module("dateutil")` → OK (from `python-dateutil`)
- `importlib.metadata.distribution("dateutil")` → **PackageNotFoundError**
- `importlib.metadata.distribution("python-dateutil")` → OK
- `pip show` lists **`python-dateutil`**, not `dateutil`

---

## 3. Root cause

**Primary (dateutil / yaml class of bugs):**

Requirement tokens were treated as if **pip name ≡ import name**.  
For `python-dateutil`, the importable module is `dateutil`. Any checker (or operator workflow) that looks up / installs / reports the token `dateutil` as a **distribution** disagrees with `pip list` and `importlib.metadata`.

Concretely:

1. Preflight listed / reported the **import** token `dateutil`.
2. `pip list` shows **`python-dateutil`**.
3. Operators conclude “pip has it but Runtime says missing” — naming mismatch, not necessarily a failed import.
4. If a future or parallel check used `importlib.metadata.distribution("dateutil")`, it would **false-negative** even when the package is correctly installed.

**Secondary (pandas / any identity package):**

`pandas` pip name ≡ import name. A false “missing pandas” with a working install is **not** caused by aliasing. Typical causes:

- Preflight runs under a **different interpreter** than the one used for `pip list` (multiple Pythons on PATH).
- Broken install (import raises, not `ModuleNotFoundError` only — previously swallowed into a bare “missing” list).

The redesigned checker separates:

- **Pass criterion:** import succeeds  
- **Diagnostics:** distribution metadata + **pip-facing names** in error text  

so identity packages are not mislabeled, and alias packages report `python-dateutil` not `dateutil`.

---

## 4. Fix

New module: `runtime/dependencies.py`

- General `DISTRIBUTION_IMPORT_MAP` (not dateutil-only): e.g. `python-dateutil→dateutil`, `pyyaml→yaml`, `pillow→PIL`, …
- `resolve_package_spec()` accepts **either** distribution or import token
- `check_required_packages()` imports via mapped module; reports **distribution** names
- Distinguishes “not installed” vs “distribution present but import broken”

`runtime/manager.check_requirements()` delegates to this module.  
Canonical required list uses pip names (`REQUIRED_DISTRIBUTIONS`).

---

## 5. Confirmation

```text
check_required_packages(["pandas", "python-dateutil", "dateutil", "pyyaml", "yaml"])
→ OK — none reported missing when importable

importlib.metadata.distribution("dateutil") → still missing (correct)
resolve("dateutil") → distribution=python-dateutil, import=dateutil → import OK
```

Tests: `pytest tests/runtime/test_dependency_preflight.py -q`

---

## 6. Operator note

Always run Runtime with the same interpreter that owns the install:

```text
python -m pip list
python runtime/start.py
```

Avoid comparing `pip` from Python A with `python runtime/start.py` from Python B.
