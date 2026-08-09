# Knowledge Package Specification

| Field | Value |
|-------|-------|
| **Document** | KNOWLEDGE_PACKAGE_SPECIFICATION |
| **Sprint** | KD-3 |
| **Package spec version** | 1.0.0 |
| **Schema version** | 2.0.0 |
| **Status** | Canonical architecture reference |
| **Scope** | Architecture and specification only |

Canonical files: `knowledge/package_spec/`

---

## 1. Package philosophy

A Knowledge Package is the smallest independently versioned, validated, and deployable knowledge unit.

BTE treats packages—not loose files—as the unit of trust for deterministic loading, validation, multilingual distribution, multi-school BaZi knowledge, and future Feng Shui / Qi Men / I Ching packages.

Principles: immutable identity, immutable released bytes, acyclic dependencies, dual-read with V1, taxonomy-aligned `domain_id`, scale to 100,000+ objects.

---

## 2. Package anatomy

```
<package_id>/
    PACKAGE.json          identity
    MANIFEST.json         contents, exports, dependencies
    DEPENDENCIES.json     optional explicit graph
    RELEASE.json          required when released
    VALIDATION.json       last validation report
    README.md / CHANGELOG.md
    rules/ metadata/ references/ examples/ tests/ documentation/ assets/
```

Identity fields: `package_id`, `package_name`, `package_type`, `package_version`, `schema_version`, `knowledge_version`, `author`, `owner`, `status`, `language`, `created_at`, `updated_at`, `compatibility`, `checksum`, `license`, `description`.

---

## 3. Lifecycle

```
draft → review → validated → released → deprecated → archived
```

Released packages are immutable. Corrections ship as a new `package_version`.

---

## 4. Dependency model

- Required, optional, and conflict declarations
- SemVer constraints (`exact`, range, `^`, `~`, `x`)
- Deterministic resolution: highest satisfying version, topological order, `package_id` ascending tie-breaker
- Circular required dependencies prohibited

---

## 5. Validation model

Profiles: `PVP-MINIMAL` → `PVP-STANDARD` → `PVP-RELEASE`.

Checks: schema, metadata, dependency, reference, integrity, checksum, compatibility.

Specification only in KD-3. No runtime implementation.

---

## 6. Release strategy

`RELEASE.json` records notes, migration notes, checksum, date, author, supported platform versions, and immutability. Checksum uses the two-pass placeholder rule so the digest does not depend on itself.

Offline bundles = package index + complete package directories.

---

## 7. Compatibility strategy

- Existing Rule Database and KD-1 schemas are unchanged
- V1 packages remain authoritative until a migration sprint
- Dual-read projection is allowed in memory
- New work follows this spec
- Reserved types: `feng_shui`, `qi_men`, `i_ching`

---

## 8. Future extension strategy

Add enum values, optional fields, and validation checks. Do not rename identity fields. MAJOR bumps of `package_spec_version` / `schema_version` require a migration ledger entry.

---

## 9. Related documents

- `knowledge/package_spec/PACKAGE_SPECIFICATION.md`
- `knowledge/docs/architecture/KNOWLEDGE_DATABASE_V2.md`
- `knowledge/docs/architecture/KNOWLEDGE_TAXONOMY_ONTOLOGY.md`
- `knowledge/docs/KNOWLEDGE_VERSIONING.md`
