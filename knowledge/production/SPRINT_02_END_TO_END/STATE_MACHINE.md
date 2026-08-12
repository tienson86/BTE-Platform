# State Machine — Sprint 02

```text
[IDLE]
  │ run(request)
  ▼
[ENGINES_RUNNING]
  │ success
  ▼
[INTERPRETATION_V2]
  │ success
  ▼
[MASTER_LOAD]
  │ success
  ▼
[REPORT_BUILD]
  │ success
  ▼
[PDF_EXPORT]  (optional: export_pdf=False skips)
  │ success
  ▼
[CUSTOMER_PROJECT]
  │ assert_no_internal_keys
  ▼
[COMPLETE]

Any stage failure → [FAILED] with stages_completed + errors[]
```

## States

| State | Description |
|-------|-------------|
| IDLE | Orchestrator ready |
| ENGINES_RUNNING | Calendar through V1 interpretation |
| INTERPRETATION_V2 | StrengthInterpretationService |
| MASTER_LOAD | Read frozen markdown |
| REPORT_BUILD | ReportInputV1Adapter + enrich |
| PDF_EXPORT | Playwright PDF generation |
| CUSTOMER_PROJECT | Strip internals |
| COMPLETE | `success=True` |
| FAILED | `success=False`, partial stages_completed |

## Idempotency

Each `run()` is stateless. No global pipeline state.
