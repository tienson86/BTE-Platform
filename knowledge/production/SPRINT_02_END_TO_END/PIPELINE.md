# Pipeline — Sprint 02

## Stages (execution order)

| # | Stage | Component | Output |
|---|-------|-----------|--------|
| 1 | calendar | `CalendarEngine` | Solar/lunar calendar |
| 2 | bazi | `BaziEngine` | Four pillars, shensha |
| 3 | strength | `StrengthEngine` | StrengthView |
| 4 | temperature | `TemperatureEngine` | TemperatureView |
| 5 | pattern | `PatternEngine` | PatternView |
| 6 | useful_god | `UsefulGodEngine` | UsefulGodView |
| 7 | score | `ScoreEngine` | ScoreView |
| 8 | ten_gods | `TenGodsEngine` (core) | TenGodsResult |
| 9 | luck | `LuckEngine` | LuckContext (internal) |
| 10 | interpretation_v1 | `InterpretationEngine` | V1 InterpretationResult |
| 11 | interpretation_v2_strength | `StrengthInterpretationService` | Customer sections |
| 12 | master_interpretation | Frozen markdown Parts 01–06 | Customer prose |
| 13 | executive_consulting | Part 08 markdown | Consulting report |
| 14 | report_input_v1 | `ReportInputV1Adapter` | ReportInputV1 |
| 15 | pdf_export | `ReportExportServiceV1` | PDF file |

## Customer-visible stages

Customer deliverable exposes stage names only — no internal payloads.

## Not in Sprint 2 scope

- New knowledge authoring
- New reasoning design
- New report format
- Public API route (orchestrator is library + test entry)
- Full DaYun sequence publish (uses existing adapter fallback)
