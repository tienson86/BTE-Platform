# Platform Version

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_VERSION |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |
| **Sprint** | AF-1 |

---

## Declaration

| Item | Value |
|------|--------|
| **Platform version** | **1.0.0** |
| **Architecture freeze date** | 2026-08-09 |
| **Freeze sprint** | AF-1 |
| **Foundation version** | `1.0.0` (F-1, frozen) |
| **Knowledge version** | `1.0.0` |
| **Knowledge schema version** | `2.0.0` |
| **Package specification version** | `1.0.0` |
| **Knowledge generator version** | `1.0.0` |

Platform v1.0.0 is the official architecture baseline. It is frozen.

---

## Schema version

- Knowledge Database V2 envelope: **schema_version = 2.0.0**
- Released packages MUST declare `schema_version: "2.0.0"`.
- New schema generations require a **Platform major** (and Foundation major) upgrade.

---

## Engine versions (canonical layer)

| Engine | Version | Notes |
|--------|---------|-------|
| Calendar Engine | 1.0.0 | Chart time / calendar only |
| Bazi Engine | 1.0.0 | Chart construction only |
| Rule Engine | 1.0.0 (as of freeze) | Evaluates rules; does not own pipeline order |
| Score Engine | 1.0.0 (as of freeze) | Scoring only |
| Pattern Engine | 1.0.0 (as of freeze) | Pattern calculation only |
| Analysis Engine | AX-1 `1.0.0` / AX-2 `2.0.0` | Canonical analysis orchestration |
| Decision Engine | 1.0.0 | Canonical decision orchestration |
| Luck Timeline Foundation | 1.0.0 | LE-1 |
| Luck Analysis Engine | 1.0.0 | LE-2 |
| Luck Decision Engine | 1.0.0 | LE-3 |
| Interpretation Foundation | 1.0.0 | IE-1 |
| Knowledge Selection Engine | 1.0.0 | IE-2 |
| Interpretation Composition Engine | 1.0.0 | IE-3 |
| Report Foundation | 1.0.0 | RE-1 |
| Report Layout Engine | 1.0.0 | RE-2 |
| Report Rendering Engine | 1.0.0 | RE-3 |

---

## Pipeline versions

| Pipeline ID | Version | Status |
|-------------|---------|--------|
| `analysis_pipeline_v0` / AX-1 | 1.0.0 | Compatible legacy orchestration |
| `canonical_analysis_pipeline` | 2.0.0 | Only supported Analysis Knowledge model |
| `canonical_decision_pipeline` | 1.0.0 | Only supported Decision model |
| `canonical_luck_pipeline` | 1.0.0 | Only supported Luck model |
| `canonical_interpretation_pipeline` | 1.0.0 | Only supported Interpretation model |
| `canonical_report_pipeline` | 1.0.0 | Only supported Report model |

---

## Package versions

| package_id | package_version | schema | status |
|------------|-----------------|--------|--------|
| `bz_01_strength_core` | 1.2.0 | 2.0.0 | released |
| `bz_02_seasonal_core` | 1.0.0 | 2.0.0 | released |
| `bz_03_temperature_core` | 1.0.0 | 2.0.0 | released |
| `bz_04_pattern_core` | 1.0.0 | 2.0.0 | released |
| `bz_05_pattern_evaluation` | 1.0.0 | 2.0.0 | released |
| `bz_06_useful_god_foundation` | 1.0.0 | 2.0.0 | released |
| `bz_07_useful_god_priority` | 1.0.0 | 2.0.0 | released |
| `bz_08_useful_god_override` | 1.0.0 | 2.0.0 | released |
| `bz_09_luck_foundation` | 1.0.0 | 2.0.0 | released |

---

## Compatibility

See `PLATFORM_COMPATIBILITY_MATRIX.md` and `knowledge/releases/v1.0/VERSION_MATRIX.json`.

Platform v1.0.0 is backward compatible with Foundation v1.0.0 and Knowledge schema 2.0.0.

---

## Version identity

```text
BTE Platform 1.0.0
```

Any later platform line MUST increment SemVer per `PLATFORM_SEMVER_POLICY.md` and MUST NOT reuse `1.0.0`.
