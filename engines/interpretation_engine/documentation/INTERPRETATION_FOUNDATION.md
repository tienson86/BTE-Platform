# Interpretation Foundation

Version: 1.0.0  
Engine ID: `interpretation_engine`  
Sprint: IE-1  
Status: Canonical foundation  
Foundation: v1.0.0 (frozen)

This document is the canonical architecture for the Interpretation Engine foundation.

IE-1 does **not** generate interpretation text, sentences, reports, or AI copy.

IE-1 defines the contracts, context, models, registry, validation, and package-loader interfaces consumed by all future Interpretation Packages.

---

## Architecture

```
Canonical Analysis Result (AX-2 2.0.0)
        ↓
Canonical Decision Result (AX-3 1.0.0)
        ↓
Canonical Luck Result (AX-4 1.0.0)
        ↓
Interpretation Context (append-only)
        ↓
CanonicalInterpretationResult (empty shell)
```

Upstream snapshots are copied and sealed. Stages may publish new foundation outputs only. They may never overwrite Analysis, Decision, or Luck payloads.

Legacy Interpretation Engine runtimes remain unchanged. IE-1 is additive.

---

## Contracts

Published contract id: `bte.interpretation.foundation.v1`

| Contract | Role |
|---|---|
| `InterpretationContext` | Sealed upstream snapshots + published output names |
| `InterpretationSection` | Structural section slot |
| `InterpretationChapter` | Structural chapter slot |
| `InterpretationParagraph` | Structural paragraph slot |
| `InterpretationReference` | Upstream field pointer |
| `InterpretationMetadata` | Versions and module catalog |
| `CanonicalInterpretationResult` | Empty official result shell |

No templates. No sentence bodies. `text_generation`, `reports`, and `ai` are `false`.

---

## Context

`CanonicalInterpretationContext` is the runtime Interpretation Context.

Inputs:

- `CanonicalAnalysisResult` (or equivalent snapshot)
- `CanonicalDecisionResult` (or equivalent snapshot)
- `CanonicalLuckResult` (or equivalent snapshot)

Rules:

- append-only `publish()`
- immutable upstream copies
- reserved snapshot keys cannot be republished

---

## Registry

All future modules are registered. None are implemented.

| Order | module_id | implemented |
|---|---|---|
| 1 | overview | no |
| 2 | personality | no |
| 3 | career | no |
| 4 | wealth | no |
| 5 | relationship | no |
| 6 | health | no |
| 7 | children | no |
| 8 | luck | no |
| 9 | summary | no |

`summary` depends on every preceding module. Other modules depend on `overview`.

---

## Runtime models

Structural only:

- `SectionModel`
- `ChapterModel`
- `ParagraphModel`
- `ReferenceModel`
- `PlaceholderModel` (status `unbound`)
- `MetadataModel`
- `ResultModel`

---

## Validation

IE-1 validates:

- published contracts
- schema `2.0.0`
- duplicate identifiers
- registry catalog and dependency declarations
- version compatibility (AX-2 `2.0.0`, AX-3 `1.0.0`, AX-4 `1.0.0`, IE-1 `1.0.0`)
- context integrity and forbidden text fields

---

## Future package loading

`InterpretationPackageLoader` is a read-only interface.

IE-1:

- `list_available()` → empty
- `load(package_id)` → fail closed (`no_interpretation_packages_released`)

Future Interpretation Packages will admit through this loader only. Knowledge Packages are not modified here.

---

## Future sentence engine

A later sprint will bind unbound `PlaceholderModel` records to sentence library identifiers.

IE-1 forbids sentence generation and stores no sentence text.

---

## Future template engine

A later sprint will map sections/chapters onto report templates.

IE-1 stores template references only as identifiers, never template bodies.

---

## Future AI integration

AI may later assist drafting against published contracts.

IE-1 forbids AI output. Deterministic packages remain the source of interpretation structure.

---

## Compliance

- Foundation v1.0.0 frozen
- Canonical Analysis Pipeline AX-2
- Canonical Decision Pipeline AX-3
- Canonical Luck Pipeline AX-4
- Additive only
- Ready for IE-2
