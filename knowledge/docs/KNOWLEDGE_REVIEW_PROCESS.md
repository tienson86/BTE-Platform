# BTE Platform — Knowledge Review Process

| Field | Value |
|-------|-------|
| **Governance version** | 1.0 |
| **Last updated** | 2026-07-27 |

---

## Purpose

Defines the official workflow for proposing, reviewing, approving, releasing, and retiring knowledge assets.

Aligns with `docs/project/DEVELOPMENT_WORKFLOW.md` and `docs/project/CONTRIBUTING.md` — knowledge changes follow the same branch/PR discipline.

---

## Process overview

```
Draft → Technical review → Domain review → Approval → Release → (Retirement)
```

| Stage | Gate |
|-------|------|
| Draft | Author self-check + validation |
| Technical review | Engineering PR review |
| Domain review | Bát tự / content expert |
| Approval | Knowledge lead sign-off |
| Release | Changelog + version + merge |
| Retirement | Deprecation policy |

---

## 1. Draft

**Who:** Rule author, domain expert, or engineer with domain pairing.

**Actions:**

1. Create branch: `feature/knowledge-1.0.1-career-rules` or `bugfix/knowledge-ca003-prose`
2. Edit CSV/JSON in `database/`, `engines/*/knowledge/`, or `knowledge_base/`
3. Follow [RULE_AUTHORING_STANDARD.md](RULE_AUTHORING_STANDARD.md)
4. Run local validation (loaders, schema validators)
5. Self-check [DATA_QUALITY_STANDARD.md](DATA_QUALITY_STANDARD.md) checklist

**Draft status in metadata:** `status: "draft"` in JSON modules — not loaded in production until released.

**Do not:** Edit Golden Dataset expected output to match draft rules without approval.

---

## 2. Technical review

**Who:** Engineer familiar with affected engine loaders.

**Focus:**

| Area | Question |
|------|----------|
| Schema | Additive only for patch/minor? |
| Loaders | CSV loads without exception? |
| Signals | New conditions reference valid RuleContext keys? |
| Performance | Absurd rule count / cartesian explosion? |
| Security | No executable code in CSV cells |
| Platform | No forced API JSON shape change |

**Evidence in PR:**

- `pytest` module results for affected engine
- Smoke pass if interpretation/score/calendar/bazi impact
- Diff summary: files, rule count +/-, IDs added/changed

**Outcome:** Approve, request changes, or escalate to major version path.

---

## 3. Domain review

**Who:** Authorized Bát tự / domain reviewer (not necessarily engineer).

**Focus:**

| Area | Question |
|------|----------|
| Correctness | Rule logic matches classical principles? |
| Prose | Commercial Vietnamese quality? |
| Tone | Appropriate for customer Portal? |
| Conflicts | Contradicts established rules in same file? |
| Terminology | Matches style guide? |

**Evidence:**

- Sample charts walked through (e.g. critical 1987-01-21)
- Before/after interpretation text for changed rules

**Outcome:** Approve prose/logic, request rewrite, or reject.

---

## 4. Approval

**Who:** Knowledge lead (or delegated release owner).

**Confirms:**

- [ ] Technical review complete
- [ ] Domain review complete
- [ ] Version bump assigned per [KNOWLEDGE_VERSIONING.md](KNOWLEDGE_VERSIONING.md)
- [ ] `KNOWLEDGE_CHANGELOG.md` entry drafted
- [ ] Platform `CHANGELOG` entry if shipping with code release

**Minor / major:** Product notification for customer-visible interpretation changes.

**Emergency fix:** Knowledge lead may approve hotfix with abbreviated domain review if production wrong interpretation — document in changelog.

---

## 5. Release

**Actions:**

1. Merge PR to `main` (or `release/*` branch)
2. Update `knowledge/docs/KNOWLEDGE_CHANGELOG.md` with version and date
3. If coordinated platform release: tag platform `v1.0.x` per `VERSION_POLICY.md`
4. Deploy — knowledge ships with application deployment (files on disk)
5. Post-deploy: smoke on critical case if production interpretation changed

**Communication:**

- Internal: changelog + PR link
- Customer-facing: only via platform release notes if user-visible prose change significant

**Rollback:** Revert knowledge commit or redeploy previous artifact — same as platform rollback (`docs/releases/release_candidate_rc1.md`).

---

## 6. Retirement

**When:** Rule obsolete, duplicated, or technically invalid.

**Process:**

1. **Propose** — issue with `rule_id`, reason, replacement rule if any
2. **Domain confirm** — retirement does not remove required coverage
3. **Implement:**
   - Preferred: mark `deprecated` in metadata; remove from active CSV in next minor
   - Never reuse `rule_id` per authoring standard
4. **Changelog** — `Removed` or `Deprecated` section
5. **Monitor** — smoke still PASS; no orphan references in other CSVs

**Archive:** Optional `database/archive/` or git history — do not delete audit trail.

---

## Roles (RACI summary)

| Activity | Author | Engineer | Domain | Knowledge lead | Product |
|----------|--------|----------|--------|----------------|---------|
| Draft | R | C | C | I | I |
| Technical review | C | R | I | I | — |
| Domain review | C | I | R | A | I |
| Approval | I | C | C | R/A | I (minor+) |
| Release | I | R | I | A | I |
| Retirement | C | R | R | A | I |

R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## SLAs (recommended)

| Severity | Review target |
|----------|----------------|
| Hotfix — wrong interpretation | Same business day |
| Patch — prose fix | 2–3 business days |
| Minor — new module | Sprint planning |
| Major — schema break | Release train planning |

---

## Related documents

- [KNOWLEDGE_VERSIONING.md](KNOWLEDGE_VERSIONING.md)
- [DATA_QUALITY_STANDARD.md](DATA_QUALITY_STANDARD.md)
- [../../docs/project/CONTRIBUTING.md](../../docs/project/CONTRIBUTING.md)
- [../../docs/project/DEVELOPMENT_WORKFLOW.md](../../docs/project/DEVELOPMENT_WORKFLOW.md)

---

**BTE Knowledge Review Process — 1.0 — 2026-07-27**
