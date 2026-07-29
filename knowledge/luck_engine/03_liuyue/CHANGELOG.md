# CHANGELOG

All notable changes to the **03_liuyue** module are documented in this file.

This project follows

- Keep a Changelog
- Semantic Versioning
- Deterministic Rule Engine Design

---

# Version 1.0.0

Status

Stable

Release

Initial Official Release

---

# Summary

Introduced the complete Monthly Luck (LiuYue) specification for the BTE Platform.

This module provides deterministic generation and evaluation of Monthly Luck
based entirely on Solar Terms (节气), integrating with the Natal Chart, Dayun,
and LiuNian modules.

---

# Added

## Documentation

Added

README.md

Includes

- Overview
- Responsibilities
- Scope
- Dependencies
- Inputs
- Outputs
- Design Principles
- Module Architecture

---

Added

LIUYUE_SPEC.md

Defines

- Monthly Context
- Input Contracts
- Output Contracts
- Solar Month Rules
- Monthly Pillar Rules
- Seasonal Context
- Interaction Model
- Validation Requirements
- API Contract

---

Added

LIUYUE_ALGORITHM.md

Defines the deterministic processing pipeline

- Input Validation
- Solar Month Resolution
- Monthly Pillar Generation
- Hidden Stem Expansion
- Ten Gods
- Five Elements
- Seasonal Analysis
- Relationship Analysis
- Transformation
- Priority Resolution
- Context Construction
- Output Validation

---

Added

LIUYUE_EDGE_CASES.md

Defines

- Solar Term Boundary Cases
- Monthly Pillar Errors
- Hidden Stem Validation
- Seasonal Exceptions
- Dayun Transition Cases
- LiuNian Interaction Cases
- Transformation Conflicts
- Priority Conflicts
- Validation Rules
- Error Codes

---

Added

LIUYUE_TEST_CASES.md

Introduces the official compliance suite

Containing

- Calendar Tests
- Monthly Pillar Tests
- Hidden Stem Tests
- Ten Gods Tests
- Seasonal Tests
- Natal Relation Tests
- Dayun Tests
- LiuNian Tests
- Validation Tests
- Performance Tests
- Regression Tests

---

# Architecture

Established the official LiuYue processing pipeline

Input

↓

Validation

↓

Solar Month Resolution

↓

Monthly Pillar

↓

Hidden Stems

↓

Ten Gods

↓

Five Elements

↓

Seasonal Context

↓

Relationship Analysis

↓

Transformation

↓

Priority Resolution

↓

Monthly Context

↓

Validation

↓

Return Result

---

# Data Contracts

Introduced immutable objects

MonthlyContext

MonthlyPillar

SeasonalContext

InteractionResult

TransformationResult

PriorityEvent

RiskFlags

Metadata

---

# Validation

Added

Mandatory Input Validation

Mandatory Output Validation

Metadata Validation

Priority Validation

Deterministic Validation

---

# Error Codes

Defined

LIUYUE_001

SOLAR_TERM_NOT_FOUND

LIUYUE_002

INVALID_MONTHLY_STEM

LIUYUE_003

INVALID_MONTHLY_BRANCH

LIUYUE_004

INVALID_MONTHLY_PILLAR

LIUYUE_005

MISSING_HIDDEN_STEM

LIUYUE_006

INVALID_TRANSFORMATION

LIUYUE_007

DAYUN_CONTEXT_NOT_FOUND

LIUYUE_008

LIUNIAN_CONTEXT_NOT_FOUND

LIUYUE_009

INVALID_PRIORITY

LIUYUE_010

INVALID_MONTHLY_CONTEXT

LIUYUE_011

OUTPUT_VALIDATION_FAILED

LIUYUE_012

INVALID_SEASON_CONTEXT

---

# Performance Targets

Average evaluation

<10 ms

Average complexity

O(n)

Deterministic execution

100%

---

# Compatibility

Compatible with

Calendar Engine V1

BaZi Engine V1

Dayun Module V1

LiuNian Module V1

Rule Database V1

Priority Engine V1

Interpretation Engine V1

Golden Dataset Framework V1

---

# Security

No AI dependency

No network dependency

Immutable outputs

Rule-based execution only

---

# Known Limitations

Current version does not include

- LiuRi
- LiuShi
- Cross-Month Timeline
- Event Prediction
- AI Interpretation
- Probability Model

These capabilities are reserved for future releases.

---

# Roadmap

## Version 1.1.0

Planned

- LiuRi Integration
- Daily Context Support
- Daily Priority Rules

---

## Version 1.2.0

Planned

- LiuShi Integration
- Hourly Context
- Hourly Interaction Engine

---

## Version 2.0.0

Planned

Unified Fortune Timeline Engine

Integrating

- Natal Chart
- Dayun
- LiuNian
- LiuYue
- LiuRi
- LiuShi

into a single deterministic Fortune Timeline.

---

# Migration Notes

Initial release.

No migration required.

---

# Contributors

BTE Platform Architecture Team

---

# License

Internal Technical Specification

BTE Platform

Version 1.0

Confidential

End of Document