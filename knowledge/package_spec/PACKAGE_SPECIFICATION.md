# BTE Knowledge Package Specification

| Field | Value |
|-------|-------|
| **Document** | PACKAGE_SPECIFICATION |
| **Sprint** | KD-3 |
| **Package spec version** | 1.0.0 |
| **Schema version** | 2.0.0 |
| **Status** | Canonical |
| **Scope** | Specification only — no runtime, no analytical rules |

---

## 1. Package philosophy

A Knowledge Package is the **unit of trust**.

Engines do not load loose files as the unit of deployment. They load packages that are:

- identified
- versioned
- validated
- checksummed
- dependency-resolved
- independently distributable (including offline)

Principles:

1. **One package, one primary purpose** — analytical, interpretation, report, metadata, or a declared mixed type.
2. **Identity is immutable** — `package_id` never changes meaning; new meaning requires a new id.
3. **Released artifacts are immutable** — edits ship as a new `package_version`.
4. **Determinism over convenience** — same package set + same index always loads in the same order.
5. **Dual-read with V1** — existing Rule Database and KD-1 envelopes remain valid; this spec is additive.
6. **Taxonomy-aligned** — every package declares a primary domain from `knowledge/taxonomy/domains.json`.
7. **Scale** — the model must support 100,000+ knowledge objects across many packages without changing identity rules.

This specification is the canonical packaging standard for the entire BTE Platform.

---

## 2. Package anatomy

### 2.1 Identity (required)

Every package MUST define the following fields in `PACKAGE.json`:

| Field | Meaning |
|-------|---------|
| `package_id` | Immutable machine id |
| `package_name` | Display name |
| `package_type` | `minimal` \| `analytical` \| `interpretation` \| `report` \| `metadata` \| `sentence` \| `reference` \| `mixed` \| `feng_shui` \| `qi_men` \| `i_ching` |
| `package_version` | SemVer of this distribution |
| `schema_version` | Knowledge Database envelope generation (`2.0.0`) |
| `knowledge_version` | Corpus generation this package targets |
| `author` | Creator |
| `owner` | Governance owner |
| `status` | Lifecycle state |
| `language` | Primary BCP 47 tag (`mul` if mixed) |
| `created_at` | ISO-8601 creation timestamp |
| `updated_at` | ISO-8601 last edit timestamp (frozen after release) |
| `compatibility` | Version/language/school/platform ranges |
| `checksum` | SHA-256 over declared scope |
| `license` | License string |
| `description` | Short purpose statement |

Recommended: `package_spec_version` = `1.0.0`.

Schema: `package.schema.json`.

### 2.2 Manifest (required)

`MANIFEST.json` MUST include:

- `metadata`
- `components`
- `dependencies`
- `exported_objects`
- `required_packages`
- `optional_packages`
- `validation_profile`
- `release_information`

Schema: `package_manifest.schema.json`.

### 2.3 Canonical folder layout

```
<package_id>/
    PACKAGE.json
    MANIFEST.json
    DEPENDENCIES.json          # optional if fully inlined in manifest
    RELEASE.json               # required when status = released
    VALIDATION.json            # last validation report
    README.md                  # required documentation
    CHANGELOG.md               # required for validated+ and released
    rules/                     # optional
    metadata/                  # optional
    references/                # optional
    examples/                  # optional
    tests/                     # optional
    documentation/             # optional extra docs
    assets/                    # optional
```

V1 Rule Database layouts (`MANIFEST.json`, `*_rules.json`, `DEPENDENCIES.json`) remain valid and map into this anatomy via `compatibility.md`.

### 2.4 Components

| Component | Required | Notes |
|-----------|----------|--------|
| documentation (`README.md`) | **Yes** | Always |
| changelog (`CHANGELOG.md`) | Required from `validated` onward | Recommended in `draft` |
| rules | Required for `analytical` | Fixture or production rules |
| metadata | Optional | Package-level or object metadata |
| references | Optional | Citations, canon links |
| examples | Optional | Illustrative, not Golden Dataset |
| tests | Optional | Package-local fixtures only |
| assets | Optional | Non-rule media or tables |
| release record | Required for `released` | `RELEASE.json` |
| validation report | Required from `review` onward | `VALIDATION.json` |

No component may contain executable engine logic.

---

## 3. Manifest specification

The manifest is the **table of contents** used by loaders, validators, and indexes.

### 3.1 metadata

Mirrors identity fields needed to catalog the package without opening every object: type, status, language(s), author, owner, `domain_id`, optional `category_id` / `school` / tags.

### 3.2 components

Each supported component declares:

- `present` — whether files exist
- `required` — whether this package type demands them
- `paths` — relative paths, sorted ascending (C locale)

### 3.3 exported_objects

Deterministic list of public knowledge object ids the package publishes.

- Sorted by `id` ascending.
- Private/internal fixtures MAY be omitted if not exported.
- Ids MUST be unique within the release corpus (ontology constraint `CON-UNIQUE-ID`).

### 3.4 required_packages / optional_packages

Convenience id lists that MUST match `dependencies.required` / `dependencies.optional` `package_id` values, sorted ascending.

### 3.5 validation_profile

One of `PVP-MINIMAL`, `PVP-STANDARD`, `PVP-RELEASE`.

### 3.6 release_information

`null` before release. After release, a pointer/summary that MUST agree with `RELEASE.json`.

---

## 4. Dependency model

Dependencies are directed, version-constrained edges between packages.

### 4.1 Kinds

| Kind | Behavior |
|------|----------|
| required | Target MUST resolve or validation fails |
| optional | Included only when explicitly selected or present under declared policy |
| conflict | Target MUST NOT be co-loaded |

Aligns with taxonomy `DEP-PACKAGE` / `DEP-DOMAIN` / `DEP-RULE` / `DEP-METADATA`.

### 4.2 Version constraints

Supported forms (evaluated deterministically):

| Form | Meaning |
|------|---------|
| `1.2.3` | Exact version |
| `>=1.0.0 <2.0.0` | Inclusive/exclusive range (space-separated comparators) |
| `^1.2.0` | `>=1.2.0 <2.0.0` |
| `~1.2.3` | `>=1.2.3 <1.3.0` |
| `1.x` | `>=1.0.0 <2.0.0` |

Optional `compatibility_range` constrains the target's `compatibility.compatibility_version`.

### 4.3 Resolution algorithm

1. Start from the requested root set (deployment index).
2. Add all required dependencies recursively.
3. Add optional dependencies only if selected or `optional_inclusion=default_include_if_present` and the package exists in the index.
4. Reject self-dependencies.
5. Reject missing required targets.
6. Reject cycles in the required graph. Cycles are **prohibited**. No allowlist at package level.
7. Reject any selected package that matches a `conflicts` entry.
8. For each `package_id`, select the **highest SemVer** that is `released` (or the highest allowed non-released only in explicit draft workspaces) and satisfies all constraints.
9. Topologically order packages. Tie-breaker: `package_id` ascending (C locale).
10. Emit a reproducible resolution trace.

Same inputs always yield the same graph and order.

### 4.4 Domain vs package dependency

Domain dependencies (`knowledge/taxonomy/dependency_graph.json`) constrain **meaning**.  
Package dependencies constrain **loading**. Both must be acyclic. A package may not depend on another package whose primary domain is forbidden by the domain graph unless an explicit mixed-type rationale is recorded in `reason`.

---

## 5. Validation model

Specification only. No runtime validator is introduced in KD-3.

Profiles:

| Profile | When | Checks |
|---------|------|--------|
| `PVP-MINIMAL` | `draft` | schema, metadata |
| `PVP-STANDARD` | `review`, `validated` | + dependency, reference, integrity, compatibility |
| `PVP-RELEASE` | `released` and later | + checksum (required non-null), immutability, full compatibility |

Checks:

1. **schema_validation** — `PACKAGE.json`, `MANIFEST.json`, and present `DEPENDENCIES.json` / `RELEASE.json` / `VALIDATION.json` match schemas.
2. **metadata_validation** — required identity fields consistent across `PACKAGE.json` and manifest metadata; `domain_id` exists in taxonomy.
3. **dependency_validation** — resolution algorithm succeeds; no cycles; lists agree.
4. **reference_validation** — exported and referenced knowledge ids resolve within the package or declared dependencies (ontology `CON-REF-INTEGRITY`).
5. **package_integrity** — declared `components.paths` and `files[]` exist; no undeclared required files missing; exported ids unique.
6. **checksum_validation** — SHA-256 over sorted scope paths; required non-null for `released+`.
7. **compatibility_validation** — active schema/knowledge/platform versions fall inside declared ranges; language/school compatibility.

Severity: `error` blocks promotion/release; `warning` requires acknowledgment; `info` is advisory.

Report envelope: `package_validation.schema.json`. Aligns with `knowledge/validation/v2/VALIDATION_SPEC.md`.

---

## 6. Lifecycle

```
draft → review → validated → released → deprecated → archived
```

| State | Editable | Deployable by default | Immutable |
|-------|----------|----------------------|-----------|
| draft | yes | no | no |
| review | yes (limited) | no | no |
| validated | no content edits | staging only | frozen candidate |
| released | no | yes | **yes** |
| deprecated | no | yes with warning | yes |
| archived | no | no | yes |

Transition rules: `lifecycle.md`.

Mapping to existing taxonomy / V1 `active` states: `compatibility.md`.

---

## 7. Versioning strategy

Four version axes:

| Axis | Field | Tracks |
|------|-------|--------|
| Package | `package_version` | This distribution |
| Schema | `schema_version` | Envelope contract (`2.0.0`) |
| Knowledge | `knowledge_version` | Corpus generation |
| Compatibility | `compatibility.compatibility_version` | Resolver generation |

SemVer rules, breaking changes, and upgrades: `versioning.md`.

Aligned with `knowledge/docs/KNOWLEDGE_VERSIONING.md`.

---

## 8. Release strategy

A release is a dated, authored, checksummed event.

`RELEASE.json` MUST contain:

- release notes
- migration notes (empty string if none)
- checksum (non-null SHA-256)
- release date
- release author
- supported platform versions
- `immutability.immutable = true`

Process: `release_process.md`.

---

## 9. Compatibility strategy

- Do not modify existing Rule Database or KD-1 files.
- V1 packages remain authoritative until a future migration sprint.
- Loaders MAY dual-read V1 → KD-3 identity in memory.
- New packages SHOULD emit KD-3 files from day one.
- Feng Shui / Qi Men / I Ching use reserved `package_type` values without changing this spec's identity rules.

Details: `compatibility.md`.

---

## 10. Future extension strategy

Extend by addition, not by rewriting identity:

- new `package_type` enum values for new disciplines
- new optional components (never remove required ones)
- new validation checks appended to `PVP-RELEASE`
- new optional manifest fields (`additionalProperties` allowed)
- new taxonomy domains referenced via `domain_id`

Breaking changes increment `package_spec_version` MAJOR and `schema_version` MAJOR together, with a migration entry under `knowledge/migrations/`.

---

## 11. Deterministic loading

Load order for a deployment index:

1. Read `package_index` sorted by `package_id`, then `package_version`.
2. Resolve dependencies (section 4.3).
3. Validate each package with its profile.
4. Load objects in package order, then `exported_objects[].id` ascending.
5. Apply ontology override resolution only after the full set is loaded.

Offline distribution is a folder or archive containing the index plus complete package directories. Checksums MUST match before use.

---

## 12. Non-goals (this sprint)

- No Rule Engine / Analysis / Interpretation / Report Engine changes
- No API or contract changes
- No new analytical rules
- No modification of existing knowledge content
- No runtime package loader implementation
