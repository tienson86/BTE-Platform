# Packaging Guidelines

**Status:** Canonical  
**Package spec version:** 1.0.0

---

## When to create a package

Create a new package when knowledge:

- can be versioned independently
- has a single primary domain and type
- is validated and deployed as a unit
- may be distributed offline

Do not put unrelated domains in one package unless `package_type` is `mixed` and the rationale is documented.

---

## Recommended size

| Guidance | Value |
|----------|-------|
| Soft target | hundreds to a few thousand exported objects |
| Hard conceptual limit | none — 100,000+ objects are supported across packages |
| Split when | independent release cadence, different schools/languages, or different consumers |

Prefer more small packages over one monolith.

---

## Folder and file rules

1. Root folder name equals `package_id`.
2. Identity file name is exactly `PACKAGE.json`.
3. Manifest file name is exactly `MANIFEST.json`.
4. Paths inside the package use `/` separators in manifests even on Windows.
5. Paths are relative to the package root.
6. Paths in `components.*.paths` and checksum `scope` are sorted ascending (C locale).
7. No secrets, credentials, or engine source code inside a package.
8. Examples in the package are illustrative; they are not Golden Dataset or snapshots.

---

## Type-specific contents

### minimal

Required: `PACKAGE.json`, `MANIFEST.json`, `README.md`.  
No rules, interpretation, or report exports required.

### analytical

Required: `rules/` (or a single rules JSON listed in components).  
Exports: rules / conditions / results as applicable.  
May include examples and tests.

### interpretation

Required: interpretation sections and/or sentence templates under `rules/` or a dedicated listed path.  
Should declare required analytical package(s).

### report

Required: report blocks / templates.  
Should declare required interpretation package(s).

### metadata / reference / sentence

Ship only that concern. Do not embed analytical match logic.

### feng_shui / qi_men / i_ching

Same anatomy. Different `package_type` and `domain_id`.

---

## Checksum scope

Default scope (sorted):

1. `PACKAGE.json` (checksum value treated as null/empty during digest computation — see release_process.md)
2. `MANIFEST.json`
3. `DEPENDENCIES.json` if present
4. `CHANGELOG.md` if present
5. `README.md`
6. all files listed in `components.*.paths`
7. `RELEASE.json` is included **after** its checksum field is filled via the two-pass rule in `release_process.md`

Do not include `VALIDATION.json` in the release checksum unless explicitly listed (validation reports are derived).

---

## Authoring checklist

- [ ] `package_id` matches folder name and naming rules
- [ ] primary `domain_id` exists in taxonomy
- [ ] `required_packages` sorted and matches dependency entries
- [ ] `exported_objects` sorted by id
- [ ] no version in ids
- [ ] `compatible_with_v1` declared
- [ ] lifecycle status matches actual files (e.g. no `released` without `RELEASE.json`)
