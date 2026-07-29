# CHANGELOG

All notable changes to the **02_liunian** module will be documented in this file.

This project follows the principles of:

- Keep a Changelog
- Semantic Versioning (SemVer)
- Deterministic Rule Engine Development

---

# Version 1.0.0

Release Date

TBD

Status

Stable

---

## Overview

Initial official release of the LiuNian (Annual Luck) module.

This version establishes the complete technical specification for generating,
evaluating, and validating Annual Luck (流年) within the BTE Platform.

The module is fully deterministic and designed to integrate with:

- Calendar Engine
- BaZi Engine
- Dayun Module
- Rule Database
- Priority Engine
- Interpretation Engine

---

## Added

### Documentation

Added

README.md

Provides:

- Module overview
- Scope
- Responsibilities
- Inputs
- Outputs
- Dependencies
- Design principles

---

Added

LIUNIAN_SPEC.md

Defines:

- Module specification
- Input contracts
- Output contracts
- Annual Context model
- Interaction model
- Priority model
- Validation requirements
- Performance requirements

---

Added

LIUNIAN_ALGORITHM.md

Defines the official deterministic processing pipeline.

Includes

- Input validation
- Annual Pillar generation
- Hidden Stem expansion
- Ten Gods calculation
- Five Element mapping
- Interaction detection
- Priority resolution
- Output generation
- Validation

---

Added

LIUNIAN_EDGE_CASES.md

Defines handling for exceptional situations.

Includes

- Li Chun boundary
- Dayun transition
- Missing Solar Terms
- Invalid Pillars
- Hidden Stem validation
- Combination conflicts
- Clash conflicts
- Fu Yin
- Fan Yin
- Tai Sui
- Kong Wang
- Transformation failures
- Priority conflicts
- Error codes

---

Added

LIUNIAN_TEST_CASES.md

Defines the official compliance test suite.

Includes

- Calendar tests
- Annual Pillar tests
- Hidden Stem tests
- Ten Gods tests
- Five Element tests
- Stem interaction tests
- Branch interaction tests
- Dayun tests
- Special rule tests
- Validation tests
- Performance tests
- Regression tests

---

## Architecture

Established deterministic processing pipeline.

Input

↓

Validation

↓

Annual Pillar

↓

Hidden Stems

↓

Ten Gods

↓

Five Elements

↓

Interactions

↓

Priority Resolution

↓

Annual Context

↓

Validation

↓

Return Result

---

## Data Contracts

Established immutable data contracts for

AnnualContext

AnnualPillar

InteractionResult

TransformationResult

PriorityEvent

RiskFlags

Metadata

---

## Validation Rules

Added

Mandatory input validation

Mandatory output validation

Deterministic validation

Priority validation

Metadata validation

Database validation

---

## Error Handling

Introduced standardized module error codes.

LIUNIAN_001

INVALID_YEAR

LIUNIAN_002

INVALID_STEM

LIUNIAN_003

INVALID_BRANCH

LIUNIAN_004

MISSING_HIDDEN_STEM

LIUNIAN_005

INVALID_TRANSFORMATION

LIUNIAN_006

DAYUN_NOT_FOUND

LIUNIAN_007

SOLAR_TERM_NOT_FOUND

LIUNIAN_008

INVALID_PRIORITY

LIUNIAN_009

INVALID_CONTEXT

LIUNIAN_010

OUTPUT_VALIDATION_FAILED

---

## Performance Targets

Target evaluation latency

<10 ms

Expected complexity

O(n)

Deterministic execution

100%

---

## Compatibility

Compatible with

Calendar Engine V1

BaZi Engine V1

Rule Database V1

Priority Engine V1

Interpretation Engine V1

Golden Dataset Framework V1

---

## Security

No external API dependency.

No network dependency.

No AI dependency.

No runtime mutation.

Immutable outputs.

---

## Known Limitations

Current version does not include

- LiuYue (Monthly Luck)
- LiuRi (Daily Luck)
- LiuShi (Hourly Luck)
- Dynamic Timeline
- Event Prediction
- Probability Model
- AI Interpretation

These features are reserved for future versions.

---

# Roadmap

## Version 1.1.0

Planned

- LiuYue integration
- Monthly interaction support
- Monthly Context generation
- Monthly priority resolution

---

## Version 1.2.0

Planned

- LiuRi integration
- Daily interaction engine
- Daily Context

---

## Version 1.3.0

Planned

- LiuShi integration
- Hourly Fortune Context
- Hourly interaction detection

---

## Version 2.0.0

Planned

Unified Fortune Engine

Integrating

- Natal Chart
- Dayun
- LiuNian
- LiuYue
- LiuRi
- LiuShi

into a single Fortune Timeline Engine.

---

## Migration Notes

Initial release.

No migration is required.

---

## Contributors

BTE Platform Architecture Team

---

## License

Internal Specification

BTE Platform

Version 1.0

Confidential

End of Document