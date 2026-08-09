# Knowledge Package Naming Rules

**Status:** Canonical  
**Package spec version:** 1.0.0

Naming is deterministic. Published identifiers are immutable.

Aligned with `knowledge/taxonomy/naming_conventions.md`.

---

## package_id

Pattern:

```
^[a-z0-9][a-z0-9_]*[a-z0-9]$
```

Length: 3–64.

Rules:

1. Lowercase ASCII only.
2. Digits allowed (V1 ids such as `01_strength_rules` remain valid).
3. Underscores separate tokens; no leading/trailing underscore; no double underscore.
4. Do not include version numbers.
5. Do not include language or school in the id unless the package is permanently school-specific and has no school-neutral twin.
6. Folder name MUST equal `package_id`.

Recommended prefixed forms:

| Form | Example | Use |
|------|---------|-----|
| `NN_descriptive_slug` | `01_strength_rules` | V1-compatible analytical packs |
| `ex_NN_slug` | `ex_00_minimal` | Specification examples |
| `bz_NN_slug` | `bz_04_pattern_rules` | Explicit BaZi packs |
| `fs_NN_slug` | `fs_01_form_school` | Future Feng Shui |
| `qm_NN_slug` | `qm_01_ju_structure` | Future Qi Men |
| `yc_NN_slug` | `yc_01_hexagram` | Future I Ching |

---

## Filenames

| Artifact | Exact name |
|----------|------------|
| Identity | `PACKAGE.json` |
| Manifest | `MANIFEST.json` |
| Dependencies | `DEPENDENCIES.json` |
| Release | `RELEASE.json` |
| Validation report | `VALIDATION.json` |
| Readme | `README.md` |
| Changelog | `CHANGELOG.md` |

Other files: `lowercase_snake` or existing V1 names (`strength_rules.json`). JSON and Markdown only unless `assets/` requires otherwise.

---

## Folders

Component folders (when used):

```
rules/
metadata/
references/
examples/
tests/
documentation/
assets/
```

No spaces. Lowercase. Singular component names as listed.

---

## Rule ids

Prefer existing module prefixes:

`STR`, `SEA`, `TMP`, `PAT`, `SPC`, `FLW`, `CMB`, `PRI`, …

Pattern: `<PREFIX>-<6 digits>` e.g. `STR-000001`.

Example-only fixtures use `EXA-`, `EXI-`, `EXR-` prefixes and MUST NOT be treated as production analytical rules.

---

## Metadata ids

```
MD-<6 digits>
```

Or package-scoped: `<package_id>:<metadata_key>` only inside the package; public exports still use `MD-` ids.

---

## Reference ids

```
REF-<6 digits>
```

Document path references may remain paths; only knowledge-id references use `REF-`.

---

## Manifest / export / index ordering

When emitting lists of ids, paths, or package_ids: sort ascending, locale `C`.

---

## release_id

```
REL-<PACKAGE_ID_UPPER>-<package_version>
```

Example: `REL-EX_01_ANALYTICAL_DEMO-1.0.0`

Underscores in `package_id` are preserved; letters uppercased.
