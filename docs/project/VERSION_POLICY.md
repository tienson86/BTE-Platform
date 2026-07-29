# BTE Platform — Version Policy

| Field | Value |
|-------|-------|
| **Policy version** | 1.0 |
| **Applies to** | BTE Platform from 1.0.0 onward |
| **Last updated** | 2026-07-27 |

---

## Purpose

This document defines how BTE Platform versions are numbered, what each level means, and what changes are permitted without a major version bump.

**Semantic versioning:** `MAJOR.MINOR.PATCH` (e.g. `1.0.2`)

---

## Major version (X.0.0)

**When to increment:** Breaking or architectural changes that require consumer migration or explicit approval.

| Includes | Examples |
|----------|----------|
| Architecture changes | New pipeline order, new engine responsibilities, removal of SSOT model |
| Breaking API | Remove/rename required JSON fields, change endpoint paths under `/api/v1/` |
| Breaking Portal binding | Remove fields consumed by `presenters/*.js` |
| Breaking AnalysisResult | Remove/rename frozen `*View` fields |
| New major architecture document | V2.0 freeze replacing V1.0 |

**Process:** Architecture review, updated contracts in `docs/releases/`, migration guide, coordinated API + Portal release.

**Current major:** `1` — Architecture V1.0 Frozen (see `docs/releases/architecture_v1_frozen.md`).

---

## Minor version (1.X.0)

**When to increment:** New features or modules that **do not break** frozen V1.0 contracts.

| Includes | Examples |
|----------|----------|
| New features | CRM history (V1.4), PDF export (V1.3) |
| New modules | `calendar_truth`, export service |
| New optional API fields | Additive JSON keys |
| New endpoints | Under `/api/v1/` or versioned `/api/v2/` if isolated |
| Legacy cleanup | Remove internal dead code (no public API removal) |
| Calendar SSOT | `CalendarView` as additive slice |

**Must not include:** Breaking changes listed under Major version without bumping to `2.0.0`.

**Backward compatibility:** Existing clients and Portal must work without modification.

---

## Patch version (1.0.X)

**When to increment:** Maintenance releases with no new features and no contract changes.

| Includes | Examples |
|----------|----------|
| Bug fixes | Production defects (Critical/High immediate; Medium/Low batched) |
| Performance | Loader cache, warm-up (no behavior change) |
| Documentation | Governance, release notes, knowledge guides |
| Knowledge updates | CSV rule additions/corrections in `database/` |
| Test / smoke | New cases only; no production code contract change |

**Must not include:** New user-facing features, schema changes, pipeline changes.

---

## Version component summary

| Component | Format | Meaning |
|-----------|--------|---------|
| **Major** | `X` | Architecture / breaking contract |
| **Minor** | `Y` | Features, additive contracts |
| **Patch** | `Z` | Fixes, perf, docs, knowledge |

---

## Examples

| Version | Type | Description |
|---------|------|-------------|
| **1.0.0** | Major (initial) | Initial production release — Architecture Freeze, SSOT pipeline, official release |
| **1.0.1** | Patch | Bug fix — e.g. timezone documentation, Portal display fix |
| **1.0.2** | Patch | Performance — cold-start warm-up, no API change |
| **1.0.3** | Patch | Knowledge — interpretation rule CSV updates |
| **1.1.0** | Minor | Legacy cleanup, Calendar SSOT, Golden Dataset CI |
| **1.2.0** | Minor | Narrative enhancement, sentence optimization |
| **1.3.0** | Minor | PDF export, customer report branding |
| **1.4.0** | Minor | CRM, case management, customer history |
| **2.0.0** | Major | Architecture upgrade — distributed services, contract V2 |

---

## Pre-release labels

| Label | Meaning |
|-------|---------|
| `-rc.N` | Release candidate (e.g. `1.0.0-rc1`) |
| `-alpha` / `-beta` | Internal or limited preview — not production |

Production Stable releases use **no suffix** (e.g. `1.0.0`).

---

## Contract versioning

| Artifact | Version field | Document |
|----------|---------------|----------|
| AnalysisResult / API | `contract_version: "1.0"` | `docs/releases/api_contract_v1.md` |
| Architecture | V1.0 Frozen | `docs/releases/architecture_v1_frozen.md` |

Minor releases may bump internal contract docs (e.g. `api_contract_v1.1.md`) only if changes remain additive.

---

## Release approval

| Release type | Approval |
|--------------|----------|
| Patch | Engineering lead + smoke green |
| Minor | Product + Engineering + regression + smoke |
| Major | Architecture board + migration plan + full certification |

See `docs/releases/release_candidate_rc1.md` for RC checklist.

---

## Git tags

- Production releases tagged `v1.0.0`, `v1.0.1`, etc.
- Tag points to commit that matches `docs/project/CHANGELOG.md` entry

---

## Related documents

- `docs/project/CHANGELOG.md` — released versions
- `docs/project/PRODUCT_ROADMAP.md` — planned versions
- `docs/releases/architecture_v1_frozen.md` — what must not change in 1.0.x

---

**BTE Platform Version Policy — 1.0 — 2026-07-27**
