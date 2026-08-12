# Versioning — V1.0

| Field | Value |
|-------|-------|
| Document | VERSIONING |
| Version | 1.0.0 |
| Section | 12 — Versioning |

---

# 12.1 Five version dimensions

| Version | What it tracks | Example | Bumps when |
|---------|----------------|---------|------------|
| **Knowledge Version** | Interpretation Knowledge (Library) prose | `1.0.0` | Any chapter edit |
| **Catalog Version** | Knowledge Catalog units + schema | `1.0.0` | Unit add/change/deprecate |
| **QA Version** | QA Standard (platform) | `1.0.0` | Criteria/scoring change |
| **Reasoning Version** | Reasoning FREEZE + selection policy | `1.0.0` | Golden or gate change |
| **Release Version** | Customer-visible bundle | `2026.08-PACK01-v1` | Production release |

Versions are **independent** but **linked in release manifest**.

---

# 12.2 Knowledge Version

| Field | Location |
|-------|----------|
| File | Pack README in `interpretation_knowledge/PACK_XX_*/` |
| Format | Semver `MAJOR.MINOR.PATCH` |

| Bump | When |
|------|------|
| MAJOR | Domain doctrine restructure |
| MINOR | New chapter or class coverage |
| PATCH | Wording correction, no new units |

---

# 12.3 Catalog Version

| Field | Location |
|-------|----------|
| File | Pack README + CHANGELOG in `knowledge_catalog/PACK_XX_*/` |
| Format | Semver |

| Bump | When |
|------|------|
| MAJOR | Schema break; mass deprecation |
| MINOR | New topic folder or many new units |
| PATCH | Unit fix within same schema |
| `-frozen` tag | Optional suffix at freeze event (e.g. `1.0.0-frozen`) |

Production loads **exact catalog version** — not “latest”.

---

# 12.4 QA Version

| Field | Location |
|-------|----------|
| File | `knowledge/knowledge_qa/STANDARD/CHANGELOG.md` |
| Current | `1.0.0` |

When QA Standard bumps:

- Re-QA not required for all units automatically
- Governance defines regression scope
- Factory CHECKLISTS updated

---

# 12.5 Reasoning Version

| Field | Location |
|-------|----------|
| File | Reasoning FREEZE docs per pack |
| Scope | Golden cases, fact keys, selection policy |

Catalog validation must target **specific Reasoning version**.

If Reasoning bumps without catalog change → re-run Validation (QG5) only.

---

# 12.6 Release Version

| Field | Format |
|-------|--------|
| Pattern | `YYYY.MM-<PACK>-v<N>` or platform semver |
| Manifest | Lists Knowledge, Catalog, QA, Reasoning versions |

Example manifest entry:

```text
Release: 2026.08-PACK01-v1
  Knowledge: 1.0.0
  Catalog: 1.0.0-frozen
  QA Standard: 1.0.0
  Reasoning: 1.0.0
  Golden: CASE-0001
```

---

# 12.7 Compatibility rule

Production requires:

```text
Catalog Version (Frozen)
  compatible with
Reasoning Version (FREEZE)
  compatible with
Rule Database Version (facts published)
```

Mismatch → Validation fail → no Release.

---

# 12.8 Version in audit trail

Every customer report (future) should log:

- Catalog version
- Reasoning version
- Release version

Factory defines requirement; Report Engine implements.

---

END
