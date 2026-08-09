# Package Quality Report

## Rollup

| Check | Result |
| --- | --- |
| Status released | 15 / 15 |
| Schema 2.0.0 | 15 / 15 |
| Knowledge 1.0.0 | 15 / 15 |
| Language vi | 15 / 15 |
| Compatibility 1.0.0 | 15 / 15 |
| SHA-256 checksum 64 hex | 15 / 15 |
| RELEASE immutable | 15 / 15 |
| PVP-RELEASE | 15 / 15 |
| Validation errors | 0 |
| Validation warnings | 1 each (Golden Dataset N/A) |
| Package tests present | 15 / 15 (`tests/test_package.py`) |
| README / CHANGELOG / RELEASE_NOTES | 15 / 15 |
| MANIFEST.json | 15 / 15 |

## Gold quality

| Package | quality_target | Notes |
| --- | --- | --- |
| bz_01_strength_core | *(not set in metadata)* | Still PVP-RELEASE / released; metadata gap |
| bz_02 … bz_15 | gold | Declared |

## SemVer

| Version | Packages |
| --- | --- |
| 1.2.0 | bz_01_strength_core only |
| 1.0.0 | bz_02 … bz_15 |

No pre-release or 0.x packages remain in the released set.

## Documentation depth

| Band | Packages | Doc files (approx.) |
| --- | --- | --- |
| Thin (3) | bz_01 | Foundation-era |
| Standard (7–10) | bz_02–bz_15 | Wave 1 / KX packs |

## Tests

Package-local tests exist for identity, contracts (where assets exist), duplicate IDs, evidence, reasoning, validation schema. KX-6D did **not** re-execute the full pytest matrix (governance sprint; no package mutation). Last known KX-5/6 seals: 13 passed per advanced package.

## Residual quality debt

1. bz_01 missing `quality_target: gold` in metadata.
2. bz_01–bz_04 missing explicit published I/O assets.
3. bz_09 has Gold/PVP-RELEASE but 0 rules / 0 evidence / 0 reasoning.
4. Uniform `pass_with_warnings` solely from Golden Dataset policy.
