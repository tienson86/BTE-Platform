# Analysis Engine

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine` |
| Module Type | Core Analysis Pipeline |
| Layer | Domain Analysis |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The Analysis Engine is the core analytical subsystem of the BTE Platform.

Its responsibility is to transform a validated BaZi chart into a structured, deterministic, explainable analytical model.

The Analysis Engine performs domain analysis only.

It does not generate natural-language interpretation or presentation output.

---

# 2. Responsibilities

The Analysis Engine is responsible for:

- Coordinating the execution of all analytical stages.
- Managing the shared AnalysisContext.
- Producing immutable analysis results.
- Enforcing stage ordering.
- Preserving deterministic execution.
- Maintaining cross-stage consistency.
- Publishing the final AnalysisResult.

---

# 3. Architecture Overview

The Analysis Engine consists of multiple independent analytical stages.

Each stage has:

- One responsibility.
- One public contract.
- Immutable inputs.
- Immutable outputs.
- No knowledge of downstream implementation.

---

# 4. Pipeline Overview

Execution order:

1. Strength Engine
2. Temperature Engine
3. Pattern Engine
4. Useful God Engine
5. Ten Gods Engine
6. Combination Engine
7. ShenSha Engine
8. Luck Engine
9. Summary Engine

Interpretation and report generation are external to this module.

---

# 5. Inputs

Primary input:

- AnalysisContext

Produced after:

- Calendar Engine
- BaZi Engine

---

# 6. Outputs

Primary output:

- AnalysisResult

Containing:

- StrengthResult
- TemperatureResult
- PatternResult
- UsefulGodResult
- TenGodResult
- CombinationResult
- ShenShaResult
- LuckResult
- SummaryResult

---

# 7. Module Structure

```text
analysis_engine/
│
├── shared/
├── 01_strength_engine/
├── 02_temperature_engine/
├── ...
└── 10_report_generator/
```

---

# 8. Public API

The module exposes one orchestration interface.

Downstream consumers interact only through the published AnalysisResult.

---

# 9. Related Documents

- ARCHITECTURE.md
- PIPELINE.md
- SHARED_MODELS.md
- PUBLIC_API.md
- CHANGELOG.md

---

# 10. Version

Architecture Baseline V1.0.0
Frozen.