# Platform Directory Structure

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_DIRECTORY_STRUCTURE |
| **Platform version** | 1.0.0 |
| **Status** | Canonical map |
| **Owner** | BTE Architecture Board |

This is an architecture map of freeze-relevant surfaces. It does not authorize moving or renaming frozen paths.

---

## Repository (selected)

```
BTE-Platform/
  api/                         # Legacy / companion HTTP routers
  applications/
    api/                       # Application API
    customer_portal/           # Portal UI
    knowledge_console/
    validation_console/
  database/                    # Rule / reference data (engine read-only)
  engines/
    calendar_engine/
    bazi_engine/
    rule_engine/
    score_engine/
    pattern_engine/
    analysis_engine/
    decision_engine/
    luck_engine/
    interpretation_engine/
    report_engine/
    …                          # supporting engines (not new AF-1 surfaces)
  knowledge/
    docs/
      foundation/              # F-1 freeze (do not edit for convenience)
      platform/                # AF-1 freeze (this set)
      architecture/
      standards/
    packages/                  # Sealed bz_01 … bz_09
    generator/
    package_spec/
    governance/
      architecture/ADR/        # AF-1 ADRs
    releases/
      v1.0/                    # AF-1 release seal
      v1/                      # Prior commercial/visual release records
  tests/
    analysis_engine/
    decision_engine/
    luck_engine/
    interpretation_engine/
    report_engine/
    golden_dataset/            # Immutable expected outputs
  registry/
```

---

## Canonical engine internals (typical)

```
engine/
  contracts/
  pipeline/          # canonical orchestration (where applicable)
  integration/       # wrappers around released components
  documentation/
  … domain modules
```

Report example: `foundation` / `layout` / `rendering` remain independent; `pipeline/` is the only supported new execution model.

---

## Freeze documentation paths

| Path | Role |
|------|------|
| `knowledge/docs/platform/` | Platform architecture freeze |
| `knowledge/governance/architecture/ADR/` | ADRs |
| `knowledge/releases/v1.0/` | Manifest, checksums, certificate |

AF-1 created these paths additively. Existing Knowledge, Foundation, and release-process files were not modified.

---

## Forbidden moves

Renaming `engines/*`, `knowledge/packages/*`, `database/*`, or public contract modules is a breaking change and requires Platform MAJOR.
