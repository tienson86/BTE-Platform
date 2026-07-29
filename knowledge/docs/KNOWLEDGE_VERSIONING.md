# BTE Platform — Knowledge Versioning

| Field | Value |
|-------|-------|
| **Governance version** | 1.0 |
| **Last updated** | 2026-07-27 |

---

## Purpose

Defines how knowledge assets are versioned independently from but aligned with **BTE Platform software versions** (`docs/project/VERSION_POLICY.md`).

Knowledge version tracks **content and schema** of rules, sentences, templates, and editorial files.

---

## Knowledge version format

```
KNOWLEDGE_MAJOR.MINOR.PATCH
```

Example: `1.0.0` — baseline with BTE Platform 1.0.0 release.

| Component | Meaning |
|-----------|---------|
| **MAJOR** | Breaking schema change, mass rule retirement, incompatible condition language |
| **MINOR** | New modules, new CSV files, new optional columns, large rule set additions |
| **PATCH** | Text fixes, new rules (additive), priority tweaks, typo corrections |

**Metadata fields** (where schemas support):

- `schema_version` in JSON schemas (e.g. `sentence_schema.json`, `template_schema.json`)
- `database_version` in project docs when shipping coordinated rule releases

---

## Patch (x.y.Z)

**When to increment:** Small, backward-compatible knowledge changes.

| Includes | Examples |
|----------|----------|
| New rules (new `rule_id`) | Add `CA015` to `career_rules.csv` |
| Prose improvement | Rewrite `recommendation` column |
| Priority adjustment | Lower conflicting rule priority |
| Sentence example updates | `sentence_examples.json` |
| Editorial guide typo | `style_guide.md` |

**Platform release:** Typically ships as **1.0.x** patch (see `VERSION_POLICY.md`).

**Approval:** Domain reviewer + technical reviewer (see Approval rules).

**Testing:** Module regression + smoke if interpretation/score output changes.

---

## Minor (x.Y.0)

**When to increment:** Significant expansion without breaking existing loaders.

| Includes | Examples |
|----------|----------|
| New CSV module folder | New score submodule under `15_score_engine/` |
| New interpretation rule file | `children_rules.csv` |
| New sentence library module | `15_new_section/` |
| New optional CSV columns | Add `confidence_weight` with default handling |
| New report template module | `11_new_section/` in templates |

**Must not include:** Removing required columns, renaming `rule_id` values in place.

**Platform release:** **1.1.0** or bundled **1.0.x** if platform code unchanged.

**Approval:** Knowledge lead + product sign-off.

**Testing:** Full module regression, smoke, coverage report update.

---

## Major (X.0.0)

**When to increment:** Breaking changes requiring loader migration or coordinated platform release.

| Includes | Examples |
|----------|----------|
| CSV schema break | Rename/remove required column |
| Condition language change | New expression syntax |
| `rule_id` namespace reset | Incompatible ID migration |
| Sentence schema break | Change `sentence_id` pattern |
| Retire entire rule family | Remove active interpretation category |

**Platform release:** May require **minor or major** platform version if loaders change.

**Approval:** Architecture + knowledge board + migration plan.

**Testing:** Golden dataset (when available), full smoke, migration scripts documented.

---

## Approval rules

| Change type | Technical review | Domain review | Knowledge lead | Product |
|-------------|------------------|---------------|----------------|---------|
| Patch — typo only | Optional | Optional | — | — |
| Patch — rule logic/text | Required | Required | — | — |
| Patch — priority/score impact | Required | Required | Notify | — |
| Minor — new module | Required | Required | Required | Notify |
| Major — schema break | Required | Required | Required | Required |

**Emergency production wrong interpretation:**

- Hotfix knowledge branch
- Minimum change to fix incorrect rule
- Patch version + `KNOWLEDGE_CHANGELOG` entry
- Smoke + interpretation module tests mandatory

---

## Compatibility policy

### Backward compatibility (default)

1. **Additive columns** — new columns optional; loaders ignore unknown columns if designed forward-compatible.
2. **New rules** — new `rule_id` only; do not reuse IDs.
3. **Deprecated rules** — mark deprecated; keep ID reserved for audit period (minimum one minor cycle).
4. **Sentence / template schemas** — `forward_compatible: true` in schema metadata when applicable.

### Forward compatibility

Engines should tolerate unknown optional fields in JSON knowledge files where schema allows.

### Breaking changes (exception)

Require:

- Major knowledge version bump
- Migration document in `KNOWLEDGE_CHANGELOG.md`
- Loader update in platform release (if needed)
- **No** silent Golden Dataset expected output changes without domain approval

### Alignment with platform API

| Rule | Policy |
|------|--------|
| Knowledge change affects API JSON shape | **Forbidden** in patch/minor without platform contract update |
| Knowledge change affects prose only | Allowed in patch |
| Knowledge change affects scores | Allowed; document in changelog; smoke required |

API and Portal contracts remain frozen in V1.0 — knowledge must not force new required JSON fields.

---

## Version recording

| Where | What to record |
|-------|----------------|
| `knowledge/docs/KNOWLEDGE_CHANGELOG.md` | Every released knowledge version |
| `docs/project/CHANGELOG.md` | Platform release when knowledge ships with code |
| Folder `README.md` | Module-level `version` or `last_updated` when module changes |
| JSON `metadata.json` | `schema_version`, `status` (`active`, `deprecated`) |

---

## Examples

| Knowledge version | Platform version | Description |
|-------------------|------------------|-------------|
| 1.0.0 | 1.0.0 | Initial baseline — rules ship with Production Stable |
| 1.0.1 | 1.0.1 | Fix career rule CA003 prose |
| 1.0.2 | 1.0.2 | Add 5 wealth interpretation rules |
| 1.1.0 | 1.1.0 | New score submodule + golden dataset alignment |
| 2.0.0 | 2.0.0 | Interpretation condition language v2 |

---

## Related documents

- [KNOWLEDGE_REVIEW_PROCESS.md](KNOWLEDGE_REVIEW_PROCESS.md)
- [KNOWLEDGE_CHANGELOG.md](KNOWLEDGE_CHANGELOG.md)
- [../../docs/project/VERSION_POLICY.md](../../docs/project/VERSION_POLICY.md)

---

**BTE Knowledge Versioning — 1.0 — 2026-07-27**
