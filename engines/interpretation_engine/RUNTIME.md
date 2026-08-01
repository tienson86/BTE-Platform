# RUNTIME.md

> Pack 03 — Interpretation Runtime Foundation
> Status: Infrastructure Only
> Scope: Runtime framework (no BaZi logic, no rendering)

---

## Purpose

Provide the Pack 03 runtime infrastructure that executes structural stages
against `PackInterpretationContext` and produces an `InterpretationResult` shell.

## Public Runtime Contract

Every runtime exposes only:

- `initialize()`
- `shutdown()`
- `validate()`
- `execute(context)`
- `metrics()`
- `health()`

## Stage Runtimes

| Runtime | Package |
|---------|---------|
| Interpreter | `interpreter_runtime` |
| Sentence | `sentence_runtime` |
| Template | `template_runtime` |
| Placeholder | `placeholder_runtime` |
| Explanation | `explanation_runtime` |

## Shared Base

- `runtime/contracts.py` — HealthStatus, metrics, execute result, RuntimeContract
- `runtime/base.py` — BaseRuntime lifecycle/metrics/health
- `runtime/registry_base.py` — BaseRegistry DI registry
- `runtime/legacy_adapter.py` — Legacy compatibility adapter

## Context

Canonical Pack 03 context: **`PackInterpretationContext`**

Legacy BaZi-field context remains under `legacy_runtime` and must not be deleted.

## Dependency Injection

Registries and runtimes are constructed and injected.
No singleton globals.
