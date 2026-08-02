# Runtime Dependency Policy

| Field | Value |
|-------|--------|
| **Document** | `runtime_dependency_policy.md` |
| **Version** | `2.0.0` |
| **Module** | `runtime/dependency_policy.py` + `runtime/dependency_resolver.py` |

---

## 1. Purpose

Freeze **which packages** Runtime requires, **minimum versions**, and **how names are resolved** so preflight never confuses pip distribution names with import module names.

---

## 2. Version Policy (baseline)

Canonical map: `RUNTIME_VERSION_POLICY` in `runtime/dependency_policy.py`.

| Distribution (pip) | Specifier | Import module |
|--------------------|-----------|---------------|
| `fastapi` | `>=0.115.0` | `fastapi` |
| `uvicorn` | `>=0.30.0` | `uvicorn` |
| `pydantic` | `>=2.0.0` | `pydantic` |
| `httpx` | `>=0.27.0` | `httpx` |
| `pandas` | `>=2.3.1` | `pandas` |
| `numpy` | `>=2.3.1` | `numpy` |
| `pyyaml` | `>=6.0` | `yaml` |
| `openpyxl` | `>=3.1` | `openpyxl` |
| `python-dateutil` | `>=2.9` | `dateutil` |

Extras (suggested install only):

| Distribution | Extras |
|--------------|--------|
| `uvicorn` | `standard` |

Policy is merged with `requirements.txt` and `applications/requirements.txt` (startup gate keeps only keys listed above).

---

## 3. Resolver V2 (not static mapping)

`DependencyResolver` resolves names dynamically:

1. **Alias hints** (fallback only) — e.g. `python-dateutil` → `dateutil`
2. **Reverse alias** — import token `dateutil` → distribution `python-dateutil`
3. **Metadata `top_level.txt`** — when distribution is installed
4. **Identity** — `pandas` / `fastapi` style packages

Static tables alone are **not** the resolver. Hints exist because some wheels omit or obscure top-level metadata.

---

## 4. Check order

For each `PolicyRequirement`:

```text
Resolve names
    → Distribution installed?  (importlib.metadata.version)
        no  → NOT_INSTALLED
        yes → Import module?
                fail → IMPORT_ERROR
                ok   → Version satisfies specifier?
                        no  → VERSION_CONFLICT
                        yes → OK
```

---

## 5. Failure presentation

Every non-OK package exposes:

| Field | Description |
|-------|-------------|
| **Package** | Pip / distribution name |
| **Installed** | Version or `—` |
| **Required** | Specifier from policy |
| **Suggested command** | `python -m pip install "<token>"` |

Example:

```text
Package                Installed    Required       Status
----------------------------------------------------------------------
python-dateutil        —            >=2.9          not_installed
  suggested: python -m pip install "python-dateutil>=2.9"
```

---

## 6. Status definitions

| Status | Operator meaning |
|--------|------------------|
| `not_installed` | Package not in this interpreter — install with suggested command |
| `import_error` | Wheel/metadata present but import failed (broken install, DLL, path) |
| `version_conflict` | Installed version outside policy — upgrade/downgrade via suggested command |
| `ok` | Safe for startup |

---

## 7. Extending the policy

1. Add distribution + specifier to `RUNTIME_VERSION_POLICY`
2. Add extras to `RUNTIME_EXTRAS` if needed
3. If import name ≠ distribution name and metadata is unreliable, add a hint to `IMPORT_ALIAS_HINTS`
4. Add/adjust requirements files
5. Extend tests in `tests/runtime/test_dependency_resolver_v2.py`

Do **not** hard-code one-off checks inside `start.py`.
