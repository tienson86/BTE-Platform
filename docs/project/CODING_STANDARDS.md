# BTE Platform — Coding Standards

**Version:** 1.0.0  
**Applies to:** All Python and JavaScript in BTE Platform  
**Last updated:** 2026-07-27

Standards complement workspace rules in `.cursor/rules/` and engine design rules. When in conflict, **frozen architecture documents** take precedence for production path behavior.

---

## Python style

| Rule | Standard |
|------|----------|
| Classes | `PascalCase` |
| Functions / variables | `snake_case` |
| Constants | `UPPER_CASE` |
| Type hints | Required on public functions |
| Docstrings | Required on public API |
| Result types | `@dataclass(slots=True)` preferred |
| Logging | `logging` module — no `print()` in engines |
| Exceptions | Specific types — no bare `except:` |
| Imports | stdlib → third party → internal |

See `.cursor/rules/python_style.mdc` for full Python style rules.

---

## Naming convention

| Artifact | Pattern | Example |
|----------|---------|---------|
| Engine package | `engines/<name>_engine/` | `engines/bazi_engine/` |
| Engine entry | `engine.py` → `*Engine` class | `BaziEngine` |
| Result dataclass | `*Result` or domain name | `PatternResult`, `BaziChart` |
| View (API slice) | `*View` | `BaziView` |
| Truth module | `applications/api/services/*_truth.py` | `bazi_truth` |
| Portal presenter | `presenters/<stage>.js` | `bazi.js` |
| Database CSV | Vietnamese snake_case, no diacritics | `ngu_hanh.csv` |
| Test module | `test_<feature>.py` | `test_phase6_unified_report.py` |

---

## Module organization

### Engines (`engines/`)

One engine, one primary responsibility. Standard layout when applicable:

```
engine.py      — Public API (*Engine)
service.py     — Facade (optional)
models.py      — Result dataclasses
exceptions.py  — Engine-specific errors
loader.py      — Database readers
```

**Public API only** crosses engine boundaries. No internal module imports from other engines except allowed dependency direction.

### Applications (`applications/`)

```
api/           — HTTP API, orchestrator, truth modules, schemas
customer_portal/ — Portal UI (templates, static JS)
case_management/ — Case persistence (future CRM)
```

Business orchestration lives in **orchestrator**; engines do not write to database or HTTP.

---

## Folder organization

| Directory | Role |
|-----------|------|
| `engines/` | Computation engines — read-only on `database/` |
| `database/` | Rule CSVs — source of truth for rules |
| `knowledge/` / `knowledge_base/` | Templates, editorial content, extended knowledge |
| `applications/` | Deployable apps (API, Portal) |
| `tests/` | Cross-engine and integration tests |
| `validation/` | Smoke runners, RC audits, real cases |
| `docs/` | Official documentation |

Do not place business rules in `applications/` or `engines/` when they belong in `database/`.

---

## Design principles

### Single responsibility

Each engine performs one stage of the pipeline. Report Engine formats; it does not score or match rules.

### Single Source of Truth (SSOT)

| Data | One producer |
|------|------------|
| Bazi slice | `BaziEngine` → `BaziView` |
| Pattern slice | `PatternEngine` → `PatternView` |
| Score slice | `ScoreEngine` → `ScoreView` |
| Interpretation | `InterpretationEngine` → `InterpretationView` |
| Report/Narrative | `ReportEngine` → `ReportView` / `NarrativeView` |
| RuleContext build | `PatternEngine` (once) |

### Dependency direction

```
Calendar → Bazi → Pattern → Score → Interpretation → Report
Applications (orchestrator) → engines (public API only)
Portal → API JSON (no engine imports)
```

**Forbidden:** Engine imports from `applications/`. Score imports Pattern output via RuleContext, not Pattern internals.

---

## Forbidden practices

| Practice | Why forbidden |
|----------|---------------|
| **Duplicate producers** | Two code paths building same slice for production |
| **Duplicate serializers** | Orchestrator shaping what engine already owns (interpretation/report) |
| **Business logic in Portal** | Presenters render only; no scoring or pillar calculation |
| **Business logic in API routes** | Routes delegate to orchestrator; no engine orchestration in `v1.py` |
| **Circular dependency** | Breaks modular testing and layer direction |
| **Hidden side effects** | Mutating RuleContext outside documented append (Score slice) |
| **Hard-coded rules** | Rules live in `database/` CSV |
| **Global mutable state** | Engines stateless; cache in loaders only |
| **Breaking public API** | Use wrappers per `VERSION_POLICY.md` |
| **Writing to database** | Engines read-only on rule data |

---

## Engine-specific rules

- Read rules via **Loader** — not raw CSV in business logic
- Validate input → calculate → validate output → return Result object
- Return **dataclass** results — not tuples or untyped dicts for engine output
- No database writes from engines

See `.cursor/rules/engine_design.mdc` and `.cursor/rules/database.mdc`.

---

## Testing standards

### Regression (required on production changes)

```powershell
py -3.13 -m pytest applications/api/tests applications/customer_portal/tests -q
```

Run **module tests** for touched engine:

```powershell
py -3.13 -m pytest tests/bazi -q
py -3.13 -m pytest tests/report -q
```

**Do not** modify tests to pass without fixing source (unless test is wrong and approved).

### Smoke (required on production path changes)

```powershell
py -3.13 validation/production_smoke_runner.py
```

Expect 105 PASS (or updated documented count).

### Golden Dataset

- Location: `tests/golden_dataset/`
- **Do not modify** Golden Dataset, snapshots, or expected output without explicit user approval
- Requires `jsonschema` for collection (see BUG-PROD-002)

### Test rules summary

| Rule | Policy |
|------|--------|
| Fix source first | Prefer fixing engine/API over test |
| Module scope | Run affected module only during development |
| Full pytest | Only when explicitly requested |
| No skip/delete | Do not skip or delete tests to green CI |

---

## JavaScript (Portal)

- Presenters: read `data.*` from API / ResultStore
- No `fetch` to engines except via `BtePortal.post('/api/v1/...')`
- Display fallbacks allowed but must not replace missing API data with calculated values
- Match existing I18n pattern (`BteI18n.t`)

---

## Related documents

| Document | Topic |
|----------|-------|
| `.cursor/rules/architecture.mdc` | Architecture rules |
| `.cursor/rules/bte_rules.mdc` | BTE change policy |
| `.cursor/rules/testing.mdc` | Test modification policy |
| `docs/releases/architecture_v1_frozen.md` | Frozen production path |
| `docs/project/CONTRIBUTING.md` | PR and branch policy |

---

**BTE Platform Coding Standards — 1.0.0 — 2026-07-27**
