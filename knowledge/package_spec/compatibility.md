# Knowledge Package Compatibility

**Status:** Canonical  
**Package spec version:** 1.0.0

---

## Goals

- Keep existing Knowledge Database V2 and Rule Database fully compatible.
- Allow new packages to adopt KD-3 without rewriting V1 content.
- Support multilingual knowledge, multiple BaZi schools, and future Feng Shui / Qi Men / I Ching packages.

---

## Dual-read policy

| Source | After KD-3 |
|--------|------------|
| `knowledge/rule_database/*` | Unchanged, authoritative V1 packages |
| `knowledge/schema/v2/knowledge_package.schema.json` | Unchanged inline V2 envelope |
| `knowledge/package_spec/` | Additive packaging standard |
| `knowledge/taxonomy/` / `knowledge/ontology/` | Unchanged; packages reference them |

Loaders MAY project V1 → KD-3 in memory:

| KD-3 field | V1 Rule Database source |
|------------|-------------------------|
| `package_id` | `MANIFEST.json` `package.name` |
| `package_name` | same or README title |
| `package_type` | implied `analytical` |
| `package_version` | `package.version` |
| `schema_version` | map `1.0.0` → compatible V1; V2 emission uses `2.0.0` |
| `knowledge_version` | corpus / metadata version when present, else `1.0.0` |
| `author` / `owner` | `package.author` / default `BTE Knowledge Board` |
| `status` | `active` → `released`; others per `lifecycle.md` mapping |
| `language` | default `vi` unless declared |
| `created_at` / `updated_at` | manifest timestamps |
| `compatibility.compatible_with_v1` | `true` |
| `checksum` | null until a release sprint computes one |
| `license` | metadata license or `BTE Internal Use` |
| `description` | manifest description |
| `required_packages` | `DEPENDENCIES.json` `depends_on[].module` |

No V1 file is rewritten by this specification.

---

## KD-1 envelope vs KD-3 package

KD-1 `knowledge_package.schema.json` describes an **inline object array**.

KD-3 describes a **folder-deployable unit** with identity, manifest, and components.

A KD-3 analytical package MAY later be projected to a KD-1 envelope by collecting `exported_objects` into `objects[]`. That projection is a future loader concern, not a rewrite of either schema.

---

## Language compatibility

- `language` is the primary tag.
- `languages[]` lists all shipped tags.
- Translation variants SHOULD share stable ids and declare language on the object, or use `translation_of` per ontology `CON-LANGUAGE-COMPAT`.
- A consumer requesting `vi` may load a `mul` package if `vi` is listed in `languages` or `compatibility.supported_languages`.

---

## School compatibility

- School-neutral packages omit `school` or set a documented default school id.
- School-specific packages MUST set `school` and `compatibility.supported_schools`.
- Two schools MUST NOT silently override each other; use ontology override classes only when `overrides` is declared.

---

## Platform and engine compatibility

`compatibility.min_platform_version` (and optional max) bound software.

`RELEASE.json` `supported_platform_versions` MUST agree with identity `compatibility` ranges.

This spec does not modify API, contracts, or engines. Packages MUST remain loadable as data only.

---

## Future disciplines

| Discipline | `package_type` | Domain prefix (taxonomy) |
|------------|----------------|--------------------------|
| BaZi | `analytical` / `interpretation` / `report` | `DOM-BAZI` and children |
| Feng Shui | `feng_shui` | reserved `DOM-FENG_SHUI` |
| Qi Men | `qi_men` | reserved `DOM-QI_MEN` |
| I Ching | `i_ching` | reserved `DOM-I_CHING` |

New disciplines do not require a new packaging model.

---

## Index compatibility

Package indexes follow the same determinism rules as `knowledge/indexes/index_manifest.json`:

- sort keys ascending
- locale `C`
- rebuildable
- checksum optional until populated
