# Platform Risk Register

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_RISK_REGISTER |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | Architecture Board |

---

| ID | Risk | Impact | Likelihood | Mitigation | Ownership |
|----|------|--------|------------|------------|-----------|
| R-01 | Informal bypass of canonical pipelines | Divergent results, untestable paths | Medium | Freeze rule: new work binds canonical pipelines; wrappers keep BC | Architecture Board |
| R-02 | Sealed package mutation to “make tests pass” | Lost reproducibility, checksum break | Low | Forbidden; new package version only | Knowledge Board |
| R-03 | Reverse engine imports | Circular architecture, hidden coupling | Medium | Layer direction + review | Engine owners |
| R-04 | Contract drift without SemVer | Silent consumer break | Medium | Contract checksums in v1.0 release; verifier gates | Architecture Board |
| R-05 | Golden Dataset edits to force green | False confidence | Low | Immutable golden / snapshot / expected policy | Release Manager |
| R-06 | Enabling AI rewrite without ADR | Non-deterministic interpretation | Medium | Stage registered disabled; MINOR/MAJOR + ADR to enable | Interpretation owner |
| R-07 | Filesystem persist / print / email from Report | Side effects, non-determinism | Medium | RX-1 in-memory only; stages disabled | Report owner |
| R-08 | Mixing UI Foundation packs with engine models | Presentation/business bleed | Medium | UI Foundation V1 freeze + engine isolation | Product + Architecture |
| R-09 | Schema 3.0 introduced as silent field | Dual-read collapse | Low | Schema generation requires Platform/Foundation MAJOR | Knowledge Board |
| R-10 | Multiple `CanonicalReportResult` types confused | Wrong official output | Medium | RX-1 pipeline result is official Report output; RE-1 shell remains BC | Report owner |
| R-11 | Full-repo pytest used as substitute for root-cause | Noise, accidental out-of-scope edits | Medium | Module-scoped pytest rule | All agents |
| R-12 | Commercial seal confused with architecture freeze | Premature product claims | Low | Certificate distinguishes architecture freeze date vs RM commercial seal | Release Manager |

Residual risk after AF-1 is accepted under the mitigations above. New architectural risks require an ADR and register update on the *next* platform version — not an in-place silent edit of v1.0 meaning.
