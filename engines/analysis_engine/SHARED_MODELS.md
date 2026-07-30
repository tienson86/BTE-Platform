# Analysis Engine Shared Models

**Module:** `engines/analysis_engine`  
**Version:** 1.0.0  
**Status:** Frozen (Shared Model Specification)

---

# 1. Purpose

This document defines the shared domain models used across all Analysis Engine stages.

Shared models provide stable contracts and eliminate duplicate data definitions.

---

# 2. Design Principles

Shared models shall be:

- Immutable
- Strongly typed
- Versioned
- Serializable
- Backward compatible within V1.x

---

# 3. Core Shared Models

The Analysis Engine defines the following shared contracts:

- AnalysisContext
- AnalysisResult
- StageResult
- ExecutionMetadata
- RuleReference
- RuleEvidence
- ConfidenceEvaluation
- DiagnosticInfo

---

# 4. AnalysisContext

Shared analytical input.

Produced after Calendar Engine and BaZi Engine complete.

Contains:

- Calendar information
- BaZi chart
- Runtime configuration
- Shared metadata

---

# 5. StageResult

Base contract implemented by every stage result.

Common fields include:

- status
- execution metadata
- confidence
- matched rules
- diagnostics

---

# 6. AnalysisResult

Top-level immutable output.

Contains:

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

# 7. RuleReference

Represents a matched rule.

Includes:

- Rule ID
- Version
- Category
- Priority
- Evidence reference

---

# 8. ExecutionMetadata

Shared execution information.

Includes:

- timestamps
- duration
- engine version
- rule version
- correlation identifier

---

# 9. Compatibility Rules

Shared models shall remain backward compatible within Version 1.x.

Breaking changes require a major version.