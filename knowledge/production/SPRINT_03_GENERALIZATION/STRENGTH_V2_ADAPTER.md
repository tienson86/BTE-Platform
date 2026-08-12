# Strength V2 Live Adapter — Sprint 3

## Purpose

Replace CASE-0001-only `load_case_0001_facts()` in the production path with a generic adapter that maps live Strength Engine output to `PublishedStrengthFacts`.

## Location

`engines/interpretation_engine_v2/strength/runtime/published_facts_adapter.py`

## API

```python
build_published_strength_facts(
    *,
    case_id: str,
    strength_result: StrengthResult,
    strength_context: StrengthContext,
    luck_interaction_available: bool = False,
) -> PublishedStrengthFacts
```

## Mapping Rules

| PublishedStrengthFacts field | Source |
|---------------------------|--------|
| `class_id` | `strength_result.strength_level` |
| `strength_score` | `strength_result.strength_score` |
| `facts.season/root/support/control/special` | Context fields + score evidence |
| `facts.drain` | INACTIVE when `drain_count == 0` and no `drain_type` |
| `facts.root_thin` | AVAILABLE when root_level contains "Thông căn 1 chi" |
| `facts.hidden_stems`, `facts.luck_interaction` | MISSING (not exposed in live pipeline) |
| `conflicts` | `["C1"]` when `root_thin` flag active |
| `forbidden_flags` | Derived from fact states |
| `interpretation_confidence` | Derived from engine confidence |

## Pipeline Integration

```python
published = build_published_strength_facts(
    case_id=request.case_id or request.request_key,
    strength_result=engine_output.strength_result,
    strength_context=engine_output.strength_context,
)
result = strength_service.interpret(published=published)
```

## CASE-0001 Verification

Live adapter produces equivalent core facts to frozen calibration JSON:

- `class_id`: strong
- `strength_score`: 0.87
- Fact states: season, root, support, control, special, drain match
- NarrativePlan unit selection matches golden `GOLDEN_SELECTED`

## Calibration Loader (Reference Only)

`load_case_0001_facts()` remains for unit tests and golden comparison. Not used in production orchestrator.

## Knowledge Status

PACK-01 catalog units remain **Draft**. Diagnostics expose `catalog_is_draft: true`. Customer Mode never sees this.
