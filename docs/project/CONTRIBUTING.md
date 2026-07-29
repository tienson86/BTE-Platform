# Contributing to BTE Platform

**Version:** 1.0.0  
**Architecture:** V1.0 Frozen  
**Last updated:** 2026-07-27

Thank you for contributing to BTE Platform. This guide defines how changes are proposed, reviewed, tested, and merged while protecting the frozen production architecture.

---

## Before you start

1. Read `docs/releases/architecture_v1_frozen.md` — what MUST NOT change in V1.0.x
2. Read `docs/project/VERSION_POLICY.md` — patch vs minor vs major
3. Read `docs/project/CODING_STANDARDS.md` — engineering rules
4. For knowledge changes: `docs/project/KNOWLEDGE_BASE_GUIDE.md`

**Documentation-only changes** follow the documentation workflow in `DEVELOPMENT_WORKFLOW.md` — no smoke required for pure docs.

---

## Branch strategy

| Branch | Purpose | Merge target |
|--------|---------|--------------|
| `main` | Production-stable line; tagged releases | — |
| `release/*` | Release preparation (version bump, changelog) | `main` |
| `develop` | Integration branch for next minor (if used) | `release/*` or `main` |
| `feature/*` | New features (minor version scope) | `develop` or `main` |
| `bugfix/*` | Non-urgent fixes | `develop` or `main` |
| `hotfix/*` | Urgent production patches | `main` |

### Naming examples

```
feature/v1.1-calendar-ssot
feature/v1.3-pdf-export
bugfix/prod-001-timezone-docs
hotfix/1.0.1-critical-fix
release/1.0.1
```

### Rules

- **Never force-push** to `main` without explicit approval
- **One logical change** per pull request
- **Rebase or merge** per team convention; keep history readable
- **Architecture changes** require major version path — not direct to `main` without review

---

## Pull request rules

### Required for production code changes

| Requirement | Details |
|-------------|---------|
| **Code review** | At least one approving review from code owner |
| **Regression** | Module tests pass: `pytest applications/api/tests applications/customer_portal/tests -q` minimum |
| **Smoke test** | `py -3.13 validation/production_smoke_runner.py` → 105 PASS (or documented new total) |
| **Documentation** | Update CHANGELOG, contracts if API/AnalysisResult touched; governance docs if process changes |
| **Scope** | Single purpose; no drive-by refactors |

### Required for engine changes

- Run **module tests** for affected engine: e.g. `pytest tests/bazi -q`, `pytest tests/report -q`
- Do not modify Golden Dataset expected output without explicit approval
- Do not modify snapshots without explicit approval

### PR description template

```markdown
## Summary
What and why (1–3 sentences)

## Version impact
Patch / Minor / Major — per VERSION_POLICY.md

## Architecture compliance
- [ ] No pipeline reorder
- [ ] No new producers for existing slices (or approved)
- [ ] No breaking API/Portal fields

## Tests
- [ ] Module regression
- [ ] API + Portal pytest
- [ ] Production smoke (if production path touched)

## Documentation
- [ ] CHANGELOG (if releasing)
- [ ] Contract docs (if API/AnalysisResult changed)
```

---

## Code review checklist

Reviewers verify:

- [ ] Aligns with frozen architecture (V1.0.x)
- [ ] Single Source of Truth respected — no duplicate producers/serializers
- [ ] No business logic in API routes or Portal presenters
- [ ] No circular imports across engines
- [ ] Type hints and docstrings on public functions
- [ ] No `print()` in engines — use `logging`
- [ ] Tests added or smoke updated when behavior changes

---

## Commit message convention

Use [Conventional Commits](https://www.conventionalcommits.org/) prefixes:

| Prefix | Use |
|--------|-----|
| `feat:` | New feature (minor version) |
| `fix:` | Bug fix (patch) |
| `docs:` | Documentation only |
| `refactor:` | Code change without behavior change |
| `perf:` | Performance improvement |
| `test:` | Tests only |
| `build:` | Build system, dependencies |
| `ci:` | CI configuration |

### Examples

```
feat: add CalendarView slice for v1.1 calendar SSOT
fix: correct hour pillar display fallback in portal bazi presenter
docs: add project governance and version policy
perf: warm score loader on application startup
test: add Li Chun 2024 case to production smoke suite
```

### Body (optional)

- Reference issue: `Fixes BUG-PROD-001`
- Breaking change: `BREAKING CHANGE: ...` (major only)

---

## What not to contribute without approval

- Pipeline reorder or parallel production paths
- Breaking API or Portal JSON fields
- Golden Dataset / snapshot / expected output changes for test convenience
- Hard-coded rules in Python instead of `database/` CSV
- Portal engine calls or client-side scoring
- Force push to `main`

---

## Getting help

| Topic | Document |
|-------|----------|
| Architecture | `docs/releases/architecture_v1_frozen.md` |
| API contract | `docs/releases/api_contract_v1.md` |
| Workflow | `docs/project/DEVELOPMENT_WORKFLOW.md` |
| Knowledge | `docs/project/KNOWLEDGE_BASE_GUIDE.md` |

---

**BTE Platform Contributing Guide — 1.0.0 — 2026-07-27**
