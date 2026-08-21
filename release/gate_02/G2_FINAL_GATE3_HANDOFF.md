# G2-FINAL — Gate 3 handoff

Gate 2 Customer Output Layer is frozen. Gate 3 is operations / packaging, not product semantics.

## Gate 3 may change

- Runtime packaging
- Environment configuration
- Process management
- Production deployment
- Reverse proxy
- Domain
- TLS
- Backup
- Monitoring
- Release automation

## Gate 3 must NOT change

- Gate-1 analytical truth (Calendar, BaZi, Ten Gods, Strength, Pattern, Temperature, Five Elements, Useful God, Dụng/Hỷ/Kỵ, ShenSha, Luck, Score, Golden)
- Gate-2 customer semantics:
  - analysis identity
  - ResultStore precedence
  - Canonical Desktop `/result`
  - Narrative contract `pack05_narrative_result_v1`
  - ReportInputV1 / PresentedReportV1
  - official Playwright PDF vs convenience Print
  - DOCX renderer contract
  - History snapshot / 30-row local store / no silent migration

## Inputs for Gate 3

| Item | Location |
|------|----------|
| Gate-1 freeze | `release/gate_01/G1_FINAL_FREEZE.md` |
| Gate-2 freeze | `release/gate_02/G2_FINAL_FREEZE.md` |
| This handoff | this file |
| Known limitations | `G2_FINAL_KNOWN_LIMITATIONS.md` |

Do not start Gate 3 from this document automatically.
