# Package Release Process

**Status:** Canonical  
**Package spec version:** 1.0.0

---

## Release unit

The release unit is one `(package_id, package_version)` artifact.

Modules or deployment indexes MAY group many package releases, but each package is signed/checksummed independently.

---

## Preconditions

1. Status is `validated`.
2. `PVP-RELEASE` checks are specified and pass (future runtime) / recorded as passing in spec examples.
3. Every required dependency is `released` at a satisfying version.
4. `CHANGELOG.md` describes this version.
5. `breaking_changes` is non-empty if `package_version` MAJOR increased after a prior release.
6. Owner and release author are identified.

---

## Release record

Write `RELEASE.json` conforming to `package_release.schema.json`:

| Field | Required |
|-------|----------|
| `release_id` | yes — `REL-<PACKAGE_ID_UPPER>-<package_version>` |
| `package_id` | yes |
| `package_version` | yes |
| `release_date` | yes (`YYYY-MM-DD`) |
| `release_author` | yes |
| `release_notes` | yes |
| `migration_notes` | yes (empty string if none) |
| `checksum` | yes, non-null SHA-256 |
| `supported_platform_versions.min_platform_version` | yes |
| `immutability.immutable` | yes, `true` |

Optional: `supersedes`, `breaking_changes`, `released_at`, engine/API bounds.

---

## Checksum two-pass rule

Released checksum MUST be deterministic.

1. Assemble scope file list (sorted, C locale).
2. For `RELEASE.json`, compute digest using a canonical copy where `checksum.value` is the 64-character zero hex `000...0` (64 zeros) as a placeholder.
3. For `PACKAGE.json`, compute digest using a canonical copy where `checksum.value` is `null`.
4. Concatenate file bytes in scope order with a single `\n` and the relative path header per file: `<path>\n<byte_length>\n<bytes>`.
5. SHA-256 the concatenation; lowercase hex.
6. Write that digest into both `RELEASE.json` and `PACKAGE.json` `checksum.value`.
7. Re-reading the package MUST use the same placeholder substitution when verifying.

This avoids circular dependency between the digest and the files that store it.

---

## Status promotion

After checksum write:

1. Set identity `status` to `released` inside the artifact being sealed (this is the last content mutation).
2. Set `updated_at` / `released_at` to the release timestamp.
3. Set manifest `release_information` to point at `RELEASE.json`.
4. Publish the directory/archive unchanged thereafter.
5. Add/update the package index entry.

Index-level deprecation later does not rewrite the sealed artifact.

---

## Offline distribution

A distribution bundle contains:

- `package_index` JSON
- each referenced package directory in full
- optional signature file (out of scope for KD-3)

Consumers verify checksums before load. Partial bundles that omit a required dependency are invalid.

---

## Post-release changes

| Change | Action |
|--------|--------|
| Typo in a rule | new PATCH package version |
| New optional export | new MINOR version |
| Removed export / semantic break | new MAJOR version + migration notes |
| Deprecation | index status + successor pointer |
