# LiuYue Module (流月)

## Overview

The LiuYue Module is responsible for calculating and evaluating Monthly Luck (流月) within the BTE Platform.

A LiuYue represents the energetic influence of one Solar Month (节令月) on an individual's BaZi chart.

Unlike the Gregorian calendar or Lunar calendar, LiuYue is determined exclusively by the Twenty-Four Solar Terms (二十四节气), beginning with Li Chun (立春).

The module evaluates how each Monthly Pillar interacts with:

- Natal Chart (命局)
- Current Dayun (大运)
- Current LiuNian (流年)
- Hidden Heavenly Stems
- Ten Gods
- Five Elements
- Combination Rules
- Clash Rules
- Transformation Rules
- Priority Rules

The result is a structured Monthly Context that is consumed by higher-level engines.

---

# Responsibilities

The module is responsible for

- Generating Monthly Heavenly Stem
- Generating Monthly Earthly Branch
- Expanding Hidden Stems
- Calculating Monthly Ten Gods
- Evaluating Monthly Five Elements
- Detecting Monthly interactions
- Comparing Monthly Pillar with Natal Chart
- Comparing Monthly Pillar with Dayun
- Comparing Monthly Pillar with LiuNian
- Computing Monthly Priority Events
- Producing immutable Monthly Context

---

# Module Position

```
Calendar Engine
        │
        ▼
BaZi Engine
        │
        ▼
Dayun Module
        │
        ▼
LiuNian Module
        │
        ▼
LiuYue Module
        │
        ▼
Priority Engine
        │
        ▼
Interpretation Engine
```

---

# Scope

Included

- Monthly Heavenly Stem
- Monthly Earthly Branch
- Hidden Stems
- Ten Gods
- Five Elements
- Stem Relations
- Branch Relations
- Transformations
- Priority Events
- Seasonal Influence

Excluded

- Daily Luck
- Hourly Luck
- AI Interpretation
- Report Rendering
- Natural Language Generation

---

# Inputs

The module consumes

- Natal Chart
- Current Dayun Context
- Current LiuNian Context
- Gregorian Date
- Solar Term Calendar
- Rule Database
- Priority Rules

---

# Outputs

The module produces

- Monthly Pillar
- Hidden Stems
- Monthly Ten Gods
- Monthly Interactions
- Monthly Element Summary
- Monthly Priority Events
- Monthly Risk Flags
- Monthly Context

---

# Design Principles

The LiuYue Module follows the core principles of the BTE Platform.

- Deterministic
- Rule-based
- Immutable
- Testable
- Reproducible
- Independent from UI
- Independent from AI

---

# Dependencies

This module depends on

- Calendar Engine
- BaZi Engine
- Dayun Module
- LiuNian Module
- Rule Database
- Priority Engine

---

# Directory Structure

```
03_liuyue/

README.md
LIUYUE_SPEC.md
LIUYUE_ALGORITHM.md
LIUYUE_EDGE_CASES.md
LIUYUE_TEST_CASES.md
CHANGELOG.md
```

---

# Future Compatibility

Designed to integrate seamlessly with

- LiuRi Module
- LiuShi Module
- Unified Fortune Timeline Engine

---

# Version

Current Version

V1.0