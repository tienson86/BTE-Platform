# BTE Platform Architecture

Version: 1.0

Status: CANONICAL

---

# 1. Purpose

This directory contains the canonical architecture documentation of the BTE Platform.

It is the single source of truth for:

- System architecture
- Engine architecture
- Data flow
- Public APIs
- Shared models
- Runtime pipeline
- Integration rules
- Development roadmap

All implementation must follow the architecture defined here.

No module may introduce its own architecture outside this specification.

---

# 2. Architecture Principles

The BTE Platform is built using a layered architecture.

Presentation Layer
↓

Application Layer
↓

Engine Layer
↓

Knowledge Layer
↓

Infrastructure Layer

Each layer has clearly defined responsibilities.

Dependencies always point downward.

Reverse dependencies are forbidden.

---

# 3. Core Philosophy

The platform is designed around five principles.

## 3.1 Single Source of Truth

Every business concept has exactly one authoritative source.

Examples

BirthContext

BaziChart

AnalysisResult

InterpretationResult

ReportResult

No duplicated models are allowed.

---

## 3.2 Engine Independence

Every Engine is independent.

Each Engine has:

- public API
- models
- tests
- documentation

An Engine must never directly manipulate another Engine's internals.

Communication happens only through shared models.

---

## 3.3 Immutable Pipeline

The processing pipeline is fixed.

Birth Request

↓

Calendar Engine

↓

BirthContext

↓

BaZi Engine

↓

BaziChart

↓

Score Engine

↓

AnalysisResult

↓

Interpretation Engine

↓

InterpretationResult

↓

Report Engine

↓

ReportResult

↓

Desktop / Tablet / Mobile / PDF

No Engine may skip or reorder the pipeline.

---

## 3.4 Separation of Responsibilities

Each Engine has exactly one responsibility.

Calendar Engine

Calendar calculation only.

BaZi Engine

Chart construction only.

Score Engine

Analytical scoring only.

Interpretation Engine

Business interpretation only.

Report Engine

Presentation only.

---

## 3.5 UI is Consumer Only

The UI never performs calculations.

The UI only renders ViewModels.

Business logic inside UI is prohibited.

---

# 4. Engine Overview

The BTE Platform consists of five core Engines.

## Calendar Engine

Produces BirthContext.

Input

BirthRequest

Output

BirthContext

---

## BaZi Engine

Produces BaziChart.

Input

BirthContext

Output

BaziChart

---

## Score Engine

Produces AnalysisResult.

Input

BaziChart

Output

AnalysisResult

---

## Interpretation Engine

Produces InterpretationResult.

Input

AnalysisResult

Output

InterpretationResult

---

## Report Engine

Produces ReportResult.

Input

InterpretationResult

Output

ReportResult

---

# 5. Shared Models

The following models are shared across the platform.

BirthRequest

BirthContext

BaziChart

AnalysisResult

InterpretationResult

ReportResult

These models are immutable contracts.

Breaking changes require a major version.

---

# 6. Integration Strategy

All Engines communicate using strongly typed models.

No Engine accesses another Engine's private implementation.

All integrations occur through public APIs.

Adapters may be used when transforming data between layers.

---

# 7. Runtime Flow

The runtime execution is always:

User Input

↓

BirthRequest

↓

Calendar Engine

↓

BirthContext

↓

BaZi Engine

↓

BaziChart

↓

Score Engine

↓

AnalysisResult

↓

Interpretation Engine

↓

InterpretationResult

↓

Report Engine

↓

ReportResult

↓

Canonical Desktop

↓

PDF Export

---

# 8. Documentation Structure

architecture/

README.md

ROADMAP.md

PIPELINE.md

cross_engine/

pack_01_calendar_engine/

pack_02_bazi_engine/

pack_03_score_engine/

pack_04_interpretation_engine/

pack_05_report_engine/

int_02_narrative_framework/

Each Pack contains:

- Architecture
- API Specification
- Data Model
- Pipeline
- Test Plan
- Checklist

---

# 9. Development Rules

Every implementation must satisfy:

✓ Architecture document

✓ Public API

✓ Unit tests

✓ Integration tests

✓ Golden Dataset

✓ Documentation

Code without documentation is incomplete.

Documentation without tests is incomplete.

Tests without architecture approval are incomplete.

---

# 10. Review Workflow

The development lifecycle follows six stages.

Architecture

↓

Specification

↓

Implementation

↓

Testing

↓

Review

↓

Merge

Architecture approval is mandatory before implementation.

---

# 11. Source of Truth

When documentation conflicts occur, the priority is:

1. Architecture
2. Public API Specification
3. Data Model
4. Pipeline
5. Implementation

Implementation must always follow architecture.

Never the opposite.

---

# 12. Long-Term Vision

The BTE Platform is designed to become a modular expert system.

Future modules such as:

- Feng Shui Engine
- Qi Men Dun Jia Engine
- Zi Wei Engine
- Numerology Engine
- AI Advisory Engine

must integrate through the same architecture without changing the existing pipeline.

The architecture is intended to remain stable across future versions.

---

END OF DOCUMENT