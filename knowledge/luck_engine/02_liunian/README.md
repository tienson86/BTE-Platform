# LiuNian Module (流年)

## Overview

The LiuNian Module is responsible for calculating and interpreting Annual Luck (流年) in the BTE Platform.

A LiuNian represents the energetic influence of a single calendar year on an individual's BaZi chart.

This module evaluates how the current year's Heavenly Stem and Earthly Branch interact with:

- Natal Chart (命局)
- Dayun (大运)
- Hidden Stems
- Ten Gods
- Five Elements
- Combination Rules
- Clash Rules
- Punishment Rules
- Harm Rules
- Transformation Rules

The output is a structured LiuNian Context used by higher-level Interpretation Engines.

---

# Responsibilities

The module is responsible for:

- Generating annual Heavenly Stem and Earthly Branch
- Comparing annual stem with natal stems
- Comparing annual branch with natal branches
- Comparing annual branch with Dayun
- Detecting all interactions
- Computing annual elemental balance
- Producing normalized Annual Context

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
Priority Engine
        │
        ▼
Interpretation Engine
```

---

# Scope

Included

- Annual Stem
- Annual Branch
- Hidden Stems
- Ten Gods
- Five Elements
- Combination Detection
- Clash Detection
- Punishment
- Harm
- Destruction
- Transformation
- Tai Sui
- Fu Yin
- Fan Yin

Excluded

- Monthly Luck (LiuYue)
- Daily Luck (LiuRi)
- Hour Luck
- AI Interpretation
- Report Rendering

---

# Inputs

The module consumes

- Natal Chart
- Dayun Context
- Current Gregorian Year
- Solar Term Information
- Calendar Engine Output

---

# Outputs

The module produces

- Annual Pillar
- Annual Hidden Stems
- Annual Ten Gods
- Annual Interactions
- Annual Element Distribution
- Annual Priority Events
- Structured LiuNian Context

---

# Design Principles

- Deterministic
- Rule-based
- No AI dependency
- Immutable outputs
- Fully testable
- Version controlled

---

# Dependencies

Depends on

- Calendar Engine
- BaZi Engine
- Dayun Module
- Rule Database
- Priority Engine

---

# Directory

```
02_liunian/

README.md
LIUNIAN_SPEC.md
LIUNIAN_ALGORITHM.md
LIUNIAN_EDGE_CASES.md
LIUNIAN_TEST_CASES.md
CHANGELOG.md
```

---

# Version

Current Version

V1.0