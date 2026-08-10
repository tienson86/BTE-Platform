# Replay Validation

## Scope check

| Allowed | Done |
|---|---|
| Golden Dataset fixtures / pilot replay / harness / validation reports / snapshots | Yes (`knowledge/pilot/replay/`) |
| Modify AF-1 / engines / packages / pipelines / Foundation / API / UI / deployment / commercial | **No** |
| Modify frozen Pilot strategy docs | **No** |
| Overwrite Expected with Actual | **No** |
| Mock engine then claim PASS | **No** |
| Fabricate CASE-0009 | **No** |

## Tests executed

| Suite | Command | Result | Classification if fail |
|---|---|---|---|
| Golden Dataset | `python -m pytest tests/golden_dataset/test_golden_dataset.py -q` | **1 passed** (2020 deprecation warnings) | — |
| API tests (partial, `-x`) | `python -m pytest applications/api/tests -q --tb=line -x` | **27 passed, 1 failed** | CONTRACT |

### Remaining API failure (pre-existing / out of Pilot Replay scope)

`applications/api/tests/test_phase3_unified_pattern.py::test_pattern_view_matches_engine`

- Actual pattern view missing `success_reason` that engine dict still contains (or equality drift).
- Classified **CONTRACT** (view vs engine surface).
- Not fixed in this Pilot Replay (would touch applications/engines outside allowed “report-only” intent for freeze; user forbade engine/API changes to force green).

Full project pytest was not run (per Testing Rules).

## Replay execution

```text
PYTHONPATH=. python knowledge/pilot/replay/run_pilot_replay.py
```

| Metric | Value |
|---|---|
| Cases defined | 9 |
| Cases runtime-executed | 7 (0001–0007) |
| PASS | 2 |
| DISCREPANCY | 4 |
| BOUNDARY | 1 |
| BLOCKED | 1 |
| REFERENCE_ONLY | 1 |

## Artifact validation

| Artifact | Present |
|---|---|
| `fixtures/CASE-000x.input.json` + `.expected.json` | Yes |
| `results/CASE-000x.json` | Yes |
| `results/summary.json` / `matrix.json` | Yes |
| `snapshots/CASE-000x.json` | Yes (canonical outputs; HTML/MD bodies stripped to presence/size) |
| `cases/CASE-000x.md` | Yes |
| Summary docs (README, matrix, discrepancy, blocked, RCA, validation) | Yes |

## Validation result

**PASS as a truth-seeking Pilot Replay run.**  
**NOT a product acceptance PASS.**

BTE v1.0 currently:

- Runs end-to-end for birth-datetime cases through Interpretation/Report/Narrative
- Matches expert pillars in most expert cases
- Does not yet meet expert strength vocabulary / polarity for several cases
- Cannot claim Decision / public Luck / Transformation / Portal coverage

## Freeze statement

`engine_pipeline_package_api_ui_modified: false`
