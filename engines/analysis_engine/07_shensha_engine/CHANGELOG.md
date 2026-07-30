# ShenSha Engine Changelog

**Module:** `engines/analysis_engine/07_shensha_engine`

This document records architecture and specification changes for the ShenSha Engine.

The changelog follows Semantic Versioning (SemVer).

---

# Version 1.0.0

**Status:** Frozen

## Overview

Version 1.0.0 establishes the enterprise architecture baseline for the ShenSha Engine as Analysis Engine stage 07.

The engine consumes AnalysisContext, published upstream stage results through Combination, and ShenSha Knowledge through Knowledge SDK, and produces immutable ShenShaResult.

No implementation code is included in this milestone.

---

## Added

### Documentation

- README.md
- ARCHITECTURE.md
- FLOW.md
- MODELS.md
- PUBLIC_API.md
- ALGORITHM.md
- RULE_MAPPING.md
- VALIDATION.md
- ERROR_HANDLING.md
- CACHE.md
- CHANGELOG.md

### Runtime Contract

```text
ShenShaEngine.evaluate(context: AnalysisContext) -> ShenShaResult
```

### Inputs

- AnalysisContext
- StrengthResult
- TemperatureResult
- PatternResult
- UsefulGodResult
- TenGodsResult
- CombinationResult
- Knowledge SDK

### Output

- ShenShaResult

### Domain Coverage

Auspicious ShenSha · Inauspicious ShenSha · Calculation References · Lookup Tables · Mapping Tables · Priority Concepts · Interaction Rules · Compatibility · Exceptions · Confidence Concepts

---

## Compatibility

Compatible with:

- Analysis Engine / Analysis Runtime V1.x
- Knowledge SDK V1.x
- ShenSha Knowledge V1.x
- Upstream Strength / Temperature / Pattern / Useful God / Ten Gods / Combination result contracts V1.x
- Downstream Luck / Summary / Interpretation consumption model V1.x

---

## Known Limitations

Concrete knowledge content packages are authored separately under Knowledge Module governance.

Runtime implementation is outside this documentation baseline.

---

## Upgrade Policy

### Minor Versions (1.x)

Additive compatible clarifications only.

### Major Versions (2.x)

Required for breaking ShenSha semantics or public API changes.

---

## Freeze Declaration

Version **1.0.0** is designated as the official Frozen Architecture Baseline for the ShenSha Engine.
