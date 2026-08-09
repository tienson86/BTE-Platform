# Knowledge Package Versioning

**Status:** Canonical  
**Package spec version:** 1.0.0

---

## Version axes

| Axis | Field | Increment owner |
|------|-------|-----------------|
| Package distribution | `package_version` | Package owner |
| Envelope contract | `schema_version` | Knowledge Database governance (currently `2.0.0`) |
| Corpus generation | `knowledge_version` | Knowledge lead |
| Resolver generation | `compatibility.compatibility_version` | Packaging governance |

All axes use SemVer `MAJOR.MINOR.PATCH`.

Do not encode any version inside `package_id`.

Aligned with `knowledge/docs/KNOWLEDGE_VERSIONING.md`.

---

## package_version

| Bump | When |
|------|------|
| PATCH | Additive records, text fixes, priority tweaks, documentation-only fixes |
| MINOR | New optional components/fields, new exported ids, new optional dependencies |
| MAJOR | Removed/renamed exported ids, tighter/breaking condition semantics, removed required fields, incompatible dependency graph |

After a version has been `released`, every change requires a bump. Released bytes never change.

---

## schema_version

Tracks the Knowledge Database V2 envelope (`2.0.0`).

- Packages targeting V2 MUST set `schema_version` to `2.0.0`.
- A future envelope break becomes `3.0.0` and requires a migration entry.
- `compatibility.min_schema_version` / `max_schema_version` bound loaders.

---

## knowledge_version

Tracks the corpus generation the package is certified against (for example `1.0.0` with Platform 1.0).

A package MAY be reused across compatible knowledge versions if ranges allow. It MUST bump `package_version` if content changes.

---

## compatibility_version

Optional but recommended. Lets resolvers distinguish compatibility generations when SemVer ranges alone are ambiguous across schools or disciplines.

Default when omitted: equal to `package_version` MAJOR.MINOR.0.

---

## Upgrade rules

1. PATCH and MINOR upgrades of a dependency MUST be accepted when the consumer's constraint allows (`^` / range).
2. MAJOR upgrades of a dependency MUST NOT be selected unless the consumer constraint explicitly includes that MAJOR.
3. When multiple constraints apply to one `package_id`, the selected version MUST satisfy **all** of them (intersection). Empty intersection is a resolution error.
4. Upgrading a released package in a deployment index is done by adding the new version and pointing consumers at it — never by overwriting the old version directory.
5. Object-level versions inside the package follow the same SemVer rules; a package MINOR MAY pin newer object MINOR/PATCH versions.

---

## Breaking changes

A change is breaking when any of the following is true:

- exported id removed, renamed, or changes meaning
- required manifest/identity field removed or type-changed
- required dependency added that consumers cannot satisfy
- condition/result contract changes so prior matches are not reproducible
- language primary tag changes without `languages[]` continuity
- school-incompatible rewrite presented under the same `package_id`

Breaking changes require:

- `package_version` MAJOR bump
- non-empty `breaking_changes` in `RELEASE.json`
- non-empty `migration_notes`

---

## Backward compatibility rules

1. Existing V1 Rule Database packages remain valid without renaming.
2. KD-1 `knowledge_package.schema.json` remains valid for inline envelopes.
3. New optional fields are always allowed (`additionalProperties: true` on identity/manifest).
4. Consumers MUST ignore unknown optional fields.
5. Released packages stay readable for the declared `max_schema_version` / `max_platform_version` window.
6. Multilingual additions are MINOR if they do not change primary `language` semantics.
7. Multiple BaZi schools are parallel packages or school-qualified exports — not silent overwrites of a school-neutral id.
