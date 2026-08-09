# Report Foundation

Version: 1.0.0  
Engine ID: `report_engine`  
Sprint: RE-1  
Status: Canonical foundation  
Foundation: v1.0.0 (frozen)

This document is the canonical architecture for the Report Engine foundation.

RE-1 does **not** render reports and does **not** export PDF, DOCX, HTML, Markdown, or other formats.

RE-1 defines the contracts, context, models, registry, validation, and package-loader interfaces consumed by all future Report Engine components.

Legacy Report Engine runtimes remain unchanged. RE-1 is additive.

---

## Architecture

```
Canonical Analysis Result (AX-2 2.0.0)
        ↓
Canonical Decision Result (AX-3 1.0.0)
        ↓
Canonical Luck Result (AX-4 1.0.0)
        ↓
Canonical Interpretation Result (IX-1 1.0.0)
        ↓
Report Context (append-only)
        ↓
CanonicalReportResult (empty shell)
```

Upstream snapshots are copied and sealed. Stages may publish new foundation outputs only. They may never overwrite Analysis, Decision, Luck, or Interpretation payloads.

---

## Contracts

Published contract id: `bte.report.foundation.v1`

| Contract | Role |
|---|---|
| `ReportContext` | Sealed upstream snapshots + published output names |
| `ReportDocument` | Structural document slot |
| `ReportSection` | Structural section slot |
| `ReportBlock` | Structural block slot |
| `ReportMetadata` | Versions and module catalog |
| `ReportAsset` | Asset identity only |
| `CanonicalReportResult` | Empty official result shell |

`rendering`, `export`, `formatting`, `pdf`, `docx`, `html`, and `markdown` are `false`.

---

## Context

`CanonicalReportContext` is the runtime Report Context.

Inputs:

- `CanonicalAnalysisResult` (AX-2 2.0.0)
- `CanonicalDecisionResult` (AX-3 1.0.0)
- `CanonicalLuckResult` (AX-4 1.0.0)
- `CanonicalInterpretationResult` (IX-1 1.0.0)

Rules:

- append-only `publish()`
- immutable upstream copies
- reserved snapshot keys cannot be republished

---

## Registry

All future modules are registered. None are implemented.

| Order | module_id | implemented |
|---|---|---|
| 1 | cover | no |
| 2 | overview | no |
| 3 | chart | no |
| 4 | analysis | no |
| 5 | decision | no |
| 6 | luck | no |
| 7 | interpretation | no |
| 8 | appendix | no |
| 9 | summary | no |

`cover` has no dependencies. Other modules depend on `cover`. `summary` depends on every preceding module.

---

## Runtime models

Structural only:

- `DocumentModel`
- `SectionModel`
- `BlockModel`
- `AssetModel`
- `PlaceholderModel` (status `unbound`)
- `MetadataModel`
- `ResultModel`

---

## Validation

RE-1 validates:

- published contracts
- schema `2.0.0`
- duplicate identifiers
- registry catalog and dependency declarations
- version compatibility (AX-2 `2.0.0`, AX-3 `1.0.0`, AX-4 `1.0.0`, IX-1 `1.0.0`, RE-1 `1.0.0`)
- context integrity and forbidden render/export fields

---

## Future package loading

`ReportPackageLoader` is a read-only interface.

RE-1:

- `list_available()` → empty
- `load(package_id)` → fail closed (`no_report_packages_released`)

Future Report Packages will admit through this loader only. Knowledge Packages are not modified here.

---

## Future layout engine

A later sprint will map unbound `PlaceholderModel` records onto document/section/block layout identities.

RE-1 stores no layout geometry, spacing, or visual hierarchy.

---

## Future rendering engine

A later sprint will render admitted layout identities into presentation surfaces.

RE-1 forbids rendering. No PDF, DOCX, HTML, or Markdown is produced.

---

## Future export engine

A later sprint will export rendered artifacts.

RE-1 forbids export bytes, file writers, and format serializers.

---

## Compliance

- Foundation v1.0.0 frozen
- Canonical Analysis Pipeline AX-2
- Canonical Decision Pipeline AX-3
- Canonical Luck Pipeline AX-4
- Canonical Interpretation Pipeline IX-1
- Additive only
- Ready for RE-2
