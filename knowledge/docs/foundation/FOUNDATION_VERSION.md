# Foundation Version

| Field | Value |
|-------|-------|
| **Document** | FOUNDATION_VERSION |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## Declaration

| Item | Value |
|------|--------|
| **Foundation version** | **1.0.0** |
| **Release date** | `YYYY-MM-DD` *(placeholder — set at Release Manager seal)* |
| **Freeze sprint** | F-1 |
| **Knowledge schema version** | `2.0.0` |
| **Package specification version** | `1.0.0` |
| **Knowledge generator version** | `1.0.0` |
| **Canonical Analysis Pipeline** | `2.0.0` (`canonical_analysis_pipeline`) |
| **Canonical Decision Pipeline** | `1.0.0` (`canonical_decision_pipeline`) |

Foundation v1.0.0 is the official platform baseline. It is frozen.

---

## Supported schema version

- Knowledge Database V2 envelope: **schema_version = 2.0.0**
- Released packages MUST declare `schema_version: "2.0.0"`.
- New schema generations require a **Foundation major** upgrade and explicit governance approval.
- Consumers MUST reject packages with an unsupported schema version.

---

## Supported package version policy

| Rule | Policy |
|------|--------|
| Identity | `package_id` is immutable. Version lives in `package_version` (SemVer). |
| Admission | Default constraint `^1.0.0` for Foundation-era packages unless a stage declares otherwise. |
| Status | Only `status = released` packages may execute in canonical pipelines. |
| Independence | Packages are independently versioned and independently deployable. |
| Optional peers | Optional dependencies are checked only when co-loaded. Required dependencies remain empty for Foundation decision/analysis cores (pipeline order is orchestration, not package-load hard deps). |
| Overrides | Future override / school / language packages are new package ids or new major versions — not in-place edits of sealed releases. |

---

## Compatibility statement

Foundation v1.0.0 is **backward compatible** with:

- Knowledge Database V1 dual-read where explicitly declared (`compatible_with_v1`)
- Analysis Engine V1 runtime `CANONICAL_STAGES` (unchanged; AX-1 / AX-2 are additive orchestration)
- Released Knowledge Packages sealed under KD-3 / KX / AX sprints listed in the Component Catalog

Foundation v1.0.0 does **not** authorize:

- Silent mutation of frozen components
- Bypass of published package contracts
- Independent execution of Decision Packages outside the Decision Pipeline
- Independent execution of Analysis Knowledge stages outside the Canonical Analysis Pipeline (AX-2)

Forward work extends Foundation. It does not rewrite Foundation 1.0.0.

---

## Version identity

Published identifier:

```text
BTE Foundation 1.0.0
```

Any later Foundation line MUST increment SemVer per `FOUNDATION_CHANGE_POLICY.md` and MUST NOT reuse `1.0.0`.
