# BTE Platform — Development Workflow

**Version:** 1.0.0  
**Architecture:** V1.0 Frozen  
**Last updated:** 2026-07-27

Official workflow for features, bugs, hotfixes, and documentation in BTE Platform.

---

## Standard feature workflow

```
Idea
  ↓
Issue
  ↓
Planning
  ↓
Feature Branch
  ↓
Implementation
  ↓
Regression
  ↓
Smoke Test
  ↓
Code Review
  ↓
Merge
  ↓
Release
```

### 1. Idea

- Product or engineering proposes capability
- Check `docs/project/PRODUCT_ROADMAP.md` for version alignment (1.0.x vs 1.1+)

### 2. Issue

- Create issue with: goal, version impact (patch/minor/major), architecture touch?
- Link to bug ID if fixing `docs/production_bug_tracker.md` entry

### 3. Planning

- Confirm **no violation** of `docs/releases/architecture_v1_frozen.md` for V1.0.x
- Minor features: design note in issue — no new producers without approval
- Major / architecture: separate proposal before coding

### 4. Feature branch

```bash
git checkout -b feature/v1.1-calendar-ssot
```

See branch strategy in `CONTRIBUTING.md`.

### 5. Implementation

- Follow `CODING_STANDARDS.md`
- Engines: module-only changes where possible
- API: wrappers for contract extensions
- Portal: presenters only — no engine logic
- Update docs in same PR if contracts change

### 6. Regression

**Minimum:**

```powershell
py -3.13 -m pytest applications/api/tests applications/customer_portal/tests -q
```

**Module tests** for touched engines:

```powershell
py -3.13 -m pytest tests/bazi -q
py -3.13 -m pytest tests/report -q
```

### 7. Smoke test

**Required** if production path touched:

```powershell
py -3.13 validation/production_smoke_runner.py
```

Expect **105 PASS** (or updated baseline documented in PR).

### 8. Code review

- Open PR with checklist from `CONTRIBUTING.md`
- Address architecture, SSOT, test evidence

### 9. Merge

- Target: `main` or `develop` per branch policy
- No merge with failing smoke on production changes

### 10. Release

- Update `docs/project/CHANGELOG.md`
- Tag `v1.x.y` per `VERSION_POLICY.md`
- Release notes if user-visible

---

## Bug workflow

```
Report (production_bug_tracker)
  ↓
Triage (Severity)
  ↓
Critical/High → hotfix branch → fix → smoke → merge → patch release
Medium/Low    → bugfix branch → queue → minor/patch batch
```

### Severity actions

| Severity | Action |
|----------|--------|
| **Critical** | Immediate hotfix — production broken |
| **High** | Immediate hotfix — wrong data / blocking UX |
| **Medium** | `bugfix/*` branch; target next patch or minor |
| **Low** | Queue; batch with related work |
| **Info** | Document only |

### Bug fix branch

```bash
git checkout -b bugfix/prod-001-timezone-docs
```

### Verification

1. Repro steps from bug tracker
2. Module + API regression
3. Smoke if production path
4. Update `production_bug_tracker.md` status on release

**Do not** fix by changing Golden Dataset / snapshots / expected output without approval.

---

## Hotfix workflow

For **Critical/High** production issues on `main`:

```
main
  ↓
hotfix/1.0.1-<issue>
  ↓
Minimal fix (patch scope)
  ↓
Regression + smoke
  ↓
Merge to main
  ↓
Tag v1.0.1
  ↓
Deploy
  ↓
Backport to develop (if used)
```

### Hotfix rules

- **Minimal diff** — one defect root cause
- **No architecture change**
- **No feature creep**
- Patch version only (`VERSION_POLICY.md`)
- Update CHANGELOG under `[1.0.1]` section

### Rollback

See `docs/releases/release_candidate_rc1.md` rollback strategy.

---

## Documentation workflow

For **docs-only** changes (governance, release notes, knowledge guides):

```
Issue or direct PR
  ↓
docs/* or docs/project/* branch
  ↓
Peer review (accuracy, links)
  ↓
Merge — no smoke required
  ↓
CHANGELOG docs entry if release-related
```

### Documentation types

| Type | Location | Review focus |
|------|----------|----------------|
| Release / contract | `docs/releases/` | Accuracy vs code contracts |
| Governance | `docs/project/` | Process clarity |
| Production status | `docs/production_*.md` | Evidence, metrics |
| Knowledge editorial | `knowledge_base/` | Domain review + validator |

**Frozen docs:** Changes to `api_contract_v1.md` or `architecture_v1_frozen.md` require explicit approval — they are legal references for V1.0.

---

## Knowledge / database workflow

```
Domain author edits CSV/JSON
  ↓
Validation (loader, schema)
  ↓
Module regression
  ↓
Smoke (if output changes)
  ↓
Domain + technical review
  ↓
Merge → patch CHANGELOG
```

See `KNOWLEDGE_BASE_GUIDE.md`.

---

## Release workflow (patch / minor)

| Step | Action |
|------|--------|
| 1 | `release/1.0.x` branch from `main` |
| 2 | Finalize CHANGELOG, version strings in docs |
| 3 | Full smoke + API/Portal pytest |
| 4 | RC review (`release_candidate_rc1.md` checklist) |
| 5 | Tag `v1.0.x`, merge to `main` |
| 6 | Deploy API + Portal |
| 7 | Post-deploy smoke on critical case 1987-01-21 |

---

## CI expectations (recommended)

| Gate | Command |
|------|---------|
| API + Portal | `pytest applications/api/tests applications/customer_portal/tests -q` |
| Smoke | `validation/production_smoke_runner.py` |
| Golden (optional) | `pytest tests/golden_dataset` (needs `jsonschema`) |

---

## Workflow decision tree

```
Change touches production pipeline?
  ├─ Yes → Architecture frozen check → smoke required
  └─ No  → module tests only

Breaking API/Portal field?
  ├─ Yes → Major version path (2.0) — stop
  └─ No  → patch or minor

Critical/High production bug?
  ├─ Yes → hotfix workflow
  └─ No  → bugfix queue
```

---

## Related documents

| Document | Topic |
|----------|-------|
| `CONTRIBUTING.md` | Branches, PRs, commits |
| `VERSION_POLICY.md` | When to bump version |
| `PRODUCT_ROADMAP.md` | What goes in which release |
| `docs/releases/release_candidate_rc1.md` | Deploy checklist |

---

**BTE Platform Development Workflow — 1.0.0 — 2026-07-27**
