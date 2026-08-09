# Knowledge Package Lifecycle

**Status:** Canonical  
**Package spec version:** 1.0.0

---

## States

```
draft → review → validated → released → deprecated → archived
```

| State | Description |
|-------|-------------|
| `draft` | Authoring. Identity may still be refined before first review. |
| `review` | Submitted for academic/technical/governance review. |
| `validated` | All required validation checks passed. Release candidate. Content frozen. |
| `released` | Published deployable unit. **Immutable.** |
| `deprecated` | Still resolvable; successors preferred. |
| `archived` | Not loaded by default. Id remains reserved forever. |

---

## Transition rules

| From | To | Requires |
|------|----|----------|
| draft | review | `PACKAGE.json` + `MANIFEST.json` + `README.md` present; `PVP-MINIMAL` pass |
| review | validated | `PVP-STANDARD` pass; `CHANGELOG.md` present; `VALIDATION.json` stored |
| review | draft | Review rejected; findings recorded |
| validated | released | `PVP-RELEASE` pass; `RELEASE.json` complete; checksum non-null; required dependencies released |
| validated | review | Regression found before release |
| released | deprecated | Successor package/version or deprecation rationale |
| deprecated | archived | Governance approval; consumers migrated or explicitly accepting archive |
| * | archived | Only via `deprecated` (no skip from `released` directly) |

Forbidden:

- `released` → `draft` / `review` / `validated`
- editing released files in place
- reusing a `package_id` + `package_version` for different bytes
- promoting a package whose required dependencies are not `released` (except explicit staging indexes)

---

## Immutability

Once `status = released`:

1. All files in checksum scope are frozen.
2. `updated_at` MUST equal the release timestamp.
3. Corrections ship as a new `package_version`.
4. Lifecycle-only moves (`released` → `deprecated` → `archived`) are recorded in the **index / registry**, not by mutating the released blob. A pointer record MAY note the new status while the original `PACKAGE.json` inside the versioned artifact stays unchanged.

Draft workspaces MAY mutate files. Validated candidates MUST NOT mutate content; only release metadata is added at the release step, which produces the released artifact (new checksum including `RELEASE.json`).

---

## Mapping to existing state names

| KD-3 package status | Taxonomy object lifecycle | V1 Rule Database | `knowledge/package/package_lifecycle.json` |
|---------------------|---------------------------|------------------|--------------------------------------------|
| draft | draft | (unpublished) | planned / in_progress |
| review | review | (review) | review |
| validated | approved | (candidate) | approved |
| released | active / official | `active` | released |
| deprecated | deprecated | deprecated | deprecated |
| archived | archived | archived | retired |

V1 `disabled` maps to index exclusion, not a KD-3 package status. Disabled objects remain inside their released package bytes.
