# Component Flow — Sprint 02

```text
ProductionRequest
        ↓
ProductionEngineRunner
  CalendarEngine → BaziEngine → StrengthEngine → TemperatureEngine
  → PatternEngine → UsefulGodEngine → ScoreEngine
  → TenGodsEngine → LuckEngine → InterpretationEngine V1
        ↓
StrengthInterpretationService (V2, CASE-0001)
        ↓
master_interpretation_loader (Parts 01–06, 08)
        ↓
ReportInputV1Adapter → ReportInputV1 (enriched)
        ↓
ReportExportServiceV1 → PDF
        ↓
customer_projection → CustomerDeliverable
        ↓
ProductionPipelineResult
```

## Connection points

| From | To | Bridge |
|------|-----|--------|
| Birth input | Engines | `ProductionEngineRunner` |
| StrengthEngine | V2 Strength | `load_case_0001_facts()` (CASE-0001) |
| Frozen markdown | Customer | `master_interpretation_loader` |
| V1 + consulting | Report V1 | `ProductionEndToEndOrchestrator._enrich_report_with_consulting` |
| ReportInputV1 | PDF | `ReportExportServiceV1.export_pdf` |
| All outputs | Customer | `customer_projection` |

## Existing SSOT preserved

- `OrchestratorService` remains API SSOT for `/api/v1/analyze`
- Sprint 2 adds **parallel** `ProductionEndToEndOrchestrator` for customer PDF path
- `tests/report_engine/case_0001_runtime.py` delegates to `ProductionEngineRunner` (no duplicate engine logic)
