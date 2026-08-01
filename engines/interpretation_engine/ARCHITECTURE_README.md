# Interpretation Engine — Pack 03 Architecture

> **Path:** `engines/interpretation_engine/`
>
> **Architecture Version:** `0.0.0-architecture`
>
> **Status:** Architecture skeleton (coexists with legacy runtime)
>
> **Input:** Pack 02 `FinalAnalysisResult` / `FinalResult` only
>
> **Pack 01:** Read-only (via registry contracts). No mutation.

## Purpose

Pack 03 Interpretation Engine architecture defines interfaces and contracts for
turning Pack 02 final analytical results into interpretation outputs.

This skeleton does **not** implement BaZi interpretation logic.
It does **not** hard-code sentences or templates.

## Canonical Packages

| Package | Role |
|---------|------|
| `api/` | Public API facade interfaces |
| `pipeline/` | Interpretation pipeline contracts |
| `registry/` | Pack-compatible registry access contracts |
| `context/` | Interpretation context contracts |
| `interpreters/` | Interpreter module skeletons |
| `sentence_engine/` | Sentence assembly interfaces |
| `template_engine/` | Template binding interfaces |
| `placeholder_engine/` | Placeholder resolution interfaces |
| `explanation_engine/` | Explanation assembly interfaces |
| `report/` | Report assembly contracts |
| `output/` | Output format contracts |
| `models/` | Immutable interpretation models |
| `contracts/` | Cross-cutting contracts |
| `validators/` | Validation interfaces |
| `cache/` | Cache interfaces |
| `metrics/` | Metrics interfaces |
| `events/` | Internal event interfaces |
| `exceptions/` | Exception hierarchy |
| `utils/` | Shared utilities skeleton |
| `tests/architecture/` | Architecture test placeholders |

## Coexistence

Legacy runtime modules live under `legacy_runtime/`.
Architecture packages are the canonical Pack 03 skeleton going forward.
