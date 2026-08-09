# Report Builder Runtime Models

**Location**

```
knowledge/10_integration_layer/02_REPORT_BUILDER/05_RUNTIME_MODELS.md
```

---

# Purpose

This document defines the canonical runtime models used by the Report Builder.

Runtime Models are internal orchestration objects used during report assembly.

They are **not** customer-facing contracts.

They are **not** API models.

They exist only during execution of the Report Builder pipeline.

---

# Status

Document Type

Architecture Specification

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture

---

# Runtime Model Hierarchy

```
BuilderContext
        │
        ▼
PipelineState
        │
        ▼
SectionResult
        │
        ▼
ValidationResult
        │
        ▼
BuilderError
BuilderWarning
```

---

# Runtime Principles

Runtime Models shall be:

- Immutable where possible
- Stateless
- Deterministic
- Serializable
- Internal only

They must never be returned to customer applications.

---

# Runtime Lifecycle

```
Inputs

↓

BuilderContext

↓

Pipeline

↓

Section Results

↓

Validation

↓

ReportResponse

↓

Runtime Objects Destroyed
```

Runtime objects exist only during report generation.

---

# BuilderContext

## Purpose

BuilderContext is the canonical runtime input model.

Every Section Builder receives one and only one object.

```
BuilderContext
```

---

## Responsibilities

BuilderContext aggregates references to:

- AnalysisResult
- InterpretationResult
- CommercialKnowledgeBundle
- Metadata
- Runtime Configuration
- Validation Context

---

## Structure

```
BuilderContext

├── metadata
├── analysis
├── interpretation
├── commercial
├── runtime
├── validation
└── options
```

---

## Rules

BuilderContext

- immutable
- read-only
- shared
- never modified

---

# PipelineState

## Purpose

Represents the current execution state of the Report Builder.

---

## Structure

```
PipelineState

├── stage
├── started_at
├── completed_at
├── current_builder
├── completed_builders
├── failed_builders
├── warnings
└── status
```

---

## Status

Allowed values

```
INITIALIZED

VALIDATING

ASSEMBLING

NORMALIZING

VALIDATING_OUTPUT

COMPLETED

FAILED
```

---

# SectionResult

## Purpose

Represents the output produced by one Section Builder.

---

## Structure

```
SectionResult

├── section_name
├── payload
├── validation
├── traceability
├── warnings
└── execution_time
```

---

## Rules

Each Builder returns exactly one SectionResult.

---

# ValidationResult

## Purpose

Represents validation outcome.

---

## Structure

```
ValidationResult

├── status
├── severity
├── errors
├── warnings
├── checked_rules
├── execution_time
└── validator
```

---

## Status Values

```
PASS

WARNING

FAILED

CRITICAL
```

---

# BuilderError

## Purpose

Represents a runtime error.

---

## Structure

```
BuilderError

├── code
├── message
├── stage
├── builder
├── severity
├── trace
└── timestamp
```

---

## Categories

```
INPUT_ERROR

SECTION_ERROR

VALIDATION_ERROR

CONTRACT_ERROR

SYSTEM_ERROR
```

---

# BuilderWarning

## Purpose

Represents non-blocking runtime issues.

---

## Structure

```
BuilderWarning

├── code
├── message
├── builder
├── recommendation
└── timestamp
```

---

# RuntimeOptions

## Purpose

Execution configuration.

---

## Structure

```
RuntimeOptions

├── locale
├── language
├── strict_validation
├── include_diagnostics
├── include_appendix
├── include_traceability
└── debug
```

---

# TraceabilityContext

## Purpose

Centralizes provenance for every generated section.

---

## Structure

```
TraceabilityContext

├── evidence_refs
├── interpretation_refs
├── knowledge_refs
├── rule_refs
└── capability_refs
```

---

## Rules

Every SectionResult shall contain a TraceabilityContext.

Traceability is mandatory.

---

# BuilderStatistics

## Purpose

Collect execution metrics.

---

## Structure

```
BuilderStatistics

├── total_builders
├── completed
├── failed
├── warnings
├── execution_time
└── validation_time
```

---

# Runtime Relationships

```
BuilderContext

↓

PipelineState

↓

Section Builder

↓

SectionResult

↓

ValidationResult

↓

ReportResponse
```

---

# Runtime Ownership

| Runtime Model | Owner |
|---------------|-------|
| BuilderContext | Report Builder |
| PipelineState | Report Builder |
| SectionResult | Section Builder |
| ValidationResult | Validator |
| BuilderError | Report Builder |
| BuilderWarning | Report Builder |
| RuntimeOptions | Applications API |
| TraceabilityContext | Report Builder |
| BuilderStatistics | Report Builder |

---

# Runtime Memory Policy

Runtime Models

- created on request
- destroyed after completion
- never persisted
- never cached
- never exposed externally

---

# Serialization

Runtime Models may be serialized only for:

- debugging
- diagnostics
- integration testing

They shall never become part of the public API.

---

# Relationship to ReportResponse

Runtime Models are implementation objects.

```
BuilderContext

↓

Section Builders

↓

SectionResult

↓

Validation

↓

ReportResponse
```

Only ReportResponse leaves the Integration Layer.

---

# Future Runtime Models

Reserved

```
PerformanceMetrics

RetryContext

PluginContext

StreamingContext

AsyncContext

CacheContext
```

These may be added without changing the Builder architecture.

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| 01_ARCHITECTURE.md | Report Builder overview |
| 02_PIPELINE.md | Builder execution pipeline |
| 03_SECTION_BUILDERS.md | Builder responsibilities |
| 04_VALIDATION.md | Validation framework |
| 05_RUNTIME_MODELS.md | Runtime model specification (this document) |

---

# Acceptance Criteria

The Runtime Model specification is accepted when:

✓ BuilderContext is the single runtime input

✓ Every Builder returns a SectionResult

✓ ValidationResult is standardized

✓ PipelineState is defined

✓ Runtime models are internal only

✓ TraceabilityContext is mandatory

✓ Runtime models are immutable

✓ Runtime models are never exposed through the public API

---

# Official Status

Document

Runtime Model Specification

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture