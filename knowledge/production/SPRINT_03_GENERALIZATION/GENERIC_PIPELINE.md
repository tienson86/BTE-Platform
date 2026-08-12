# Generic Pipeline — Sprint 3

## Flow

```
ProductionRequest
      ↓
ProductionEngineRunner.run(request)
      Calendar → BaZi → Strength → Pattern → Useful God → Score → Ten Gods → Luck → Interpretation V1
      ↓
build_published_strength_facts(strength_result, strength_context)
      ↓
StrengthInterpretationService.interpret(published)
      ↓
build_report_input_v1(report_source)
      ↓
ReportExportServiceV1.export_pdf()  [optional]
      ↓
CustomerDeliverable
```

## ProductionRequest

| Field | Required | Notes |
|-------|----------|-------|
| `year`, `month`, `day`, `hour`, `minute` | Yes | Birth datetime |
| `gender` | Yes | |
| `timezone` | No | Default `Asia/Bangkok` |
| `full_name`, `birth_place` | No | Profile metadata |
| `case_id` | No | Optional golden/regression metadata |
| `export_pdf`, `export_dir` | No | PDF export control |
| `options` | No | Extension point |

## Section Availability

Customer deliverable exposes `section_status`:

| Section | Generic Pipeline |
|---------|-----------------|
| `strength_interpretation` | AVAILABLE (when V2 produces sections) |
| `executive_consulting` | NOT_AVAILABLE |
| `master_interpretation` | NOT_AVAILABLE |
| `report` | AVAILABLE (when PDF exported) |

## Diagnostics (Internal Only)

`ProductionPipelineResult.diagnostics` contains:

- `knowledge` — PACK-01 catalog status (Draft)
- `luck_internal.dayun_sequence` — full DaYun sequence from engine
- `engine_analysis` — pillars, strength, pattern, useful god, ten gods
- `executive_consulting` — NOT_AVAILABLE marker
- `master_interpretation_policy` — GOLDEN_REFERENCE_ONLY

Never exposed in `to_customer_dict()`.

## No CASE Branching

The orchestrator contains **zero** `if case_id == "CASE-0001"` production branches.
