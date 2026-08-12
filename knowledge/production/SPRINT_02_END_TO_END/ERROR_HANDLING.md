# Error Handling — Sprint 02

## Principles

1. **No silent placeholders** — empty master parts or missing PDF raise errors
2. **Partial stage list preserved** — `stages_completed` shows how far pipeline got
3. **Customer payload never includes stack traces**
4. **Existing engine exceptions propagate** — not swallowed

## Failure modes

| Failure | Behavior |
|---------|----------|
| Missing master interpretation file | `FileNotFoundError` → `success=False` |
| Strength V2 unsupported case_id | `ValueError` → `success=False` |
| PDF export (Playwright missing) | Exception → `success=False` |
| Engine calculation error | Exception → `success=False` |
| Internal key in customer payload | `assert_no_internal_keys` raises in dev/test |

## Logging

`ProductionEndToEndOrchestrator` logs `production_pipeline_failed` at ERROR with case_id.

## Recovery

Re-run `run()` or `run_case_0001()` — no cleanup required.
