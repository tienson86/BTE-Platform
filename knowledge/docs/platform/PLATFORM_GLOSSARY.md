# Platform Glossary

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_GLOSSARY |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

Terms below are the freeze vocabulary. Prefer these names in contracts, traces, and release notes.

| Term | Meaning |
|------|---------|
| **ADR** | Architecture Decision Record |
| **AF-1** | Architecture Freeze sprint that seals Platform v1.0.0 |
| **API** | Public application interface; consumes official results only |
| **Artifact** | In-memory Canonical Report Artifact (mime envelope) |
| **Audit** | Machine-readable legality / determinism record |
| **AX-1 / AX-2** | Analysis Pipeline 1.0.0 / Canonical Analysis Pipeline 2.0.0 |
| **AX-3** | Canonical Decision Pipeline 1.0.0 |
| **AX-4** | Canonical Luck Pipeline 1.0.0 |
| **Canonical pipeline** | Only supported orchestration path for a package class |
| **Canonical Result** | Official dataclass aggregate published by a pipeline |
| **Checksum** | SHA-256 over a declared sealed scope |
| **Contract** | Declared published inputs, outputs, and versions |
| **Context** | Append-only runtime bag; upstream snapshots immutable |
| **Decision** | Useful God Foundation → Priority → Override |
| **Deprecation** | Public identity remains callable until MAJOR removal |
| **Diagnostic** | Structured code + message; not an exception type |
| **Engine** | Stateless module with one responsibility |
| **F-1** | Foundation Freeze v1.0.0 |
| **Foundation** | Frozen platform baseline (schema, taxonomy, AX-1/2/3 as of F-1) |
| **Golden Dataset** | Immutable expected analytical cases |
| **IE-1 / IE-2 / IE-3** | Interpretation Foundation / Knowledge Selection / Composition |
| **IX-1** | Canonical Interpretation Pipeline |
| **Knowledge Package** | Independently versioned, checksum-sealed knowledge unit |
| **Knowledge schema** | Envelope version; v1.0 freeze uses `2.0.0` |
| **LE-1 / LE-2 / LE-3** | Luck Timeline / Analysis / Decision |
| **Layout** | RE-2 theme, section, and block identities (no CSS render) |
| **Package id** | Immutable package identity (`bz_01_strength_core`, …) |
| **PATCH / MINOR / MAJOR** | SemVer classes for Platform and components |
| **PVP** | Package Validation Profile (MINIMAL / STANDARD / RELEASE) |
| **RE-1 / RE-2 / RE-3** | Report Foundation / Layout / Rendering |
| **RX-1** | Canonical Report Pipeline |
| **Registry** | Catalog of stages, modules, or renderers |
| **Rendering** | RE-3 in-memory export envelopes |
| **Reserved / inactive stage** | Registered, dependency-declared, not executed |
| **Rule Database** | CSV-first knowledge store; engines read only |
| **Sealed** | Released artifact whose checksum must not change |
| **SemVer** | `MAJOR.MINOR.PATCH` |
| **Snapshot** | Defensive copy of an upstream result |
| **Stage** | Named pipeline step with declared I/O |
| **Trace** | Machine-readable execution history |
| **Useful God** | Decision outcome (`final_useful_god` and related fields) |
| **Wrapper** | Compatibility façade preserving a public name |

See also governance glossary standard: `knowledge/governance/standards/08_GLOSSARY_STANDARD.md`.
