# BTE Platform Runtime Pipeline

Version: 1.0

Status: CANONICAL

---

# 1. Purpose

This document defines the canonical runtime pipeline of the BTE Platform.

It specifies:

- Runtime execution order
- Engine dependencies
- Data contracts
- Model transitions
- Integration boundaries

Every runtime execution must follow this pipeline.

No Engine may skip or reorder any stage.

---

# 2. Runtime Philosophy

The BTE Platform is a deterministic processing pipeline.

Each Engine performs exactly one responsibility.

Every Engine consumes one canonical model and produces one canonical model.

Each output becomes the input of the next Engine.

The UI never participates in calculations.

---

# 3. Canonical Runtime Pipeline

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

Presentation Layer

↓

Desktop

Tablet

Mobile

PDF

---

# 4. Pipeline Stage Overview

| Stage | Input | Output | Responsibility |
|--------|-------|--------|----------------|
| 01 | User Input | BirthRequest | Collect birth information |
| 02 | BirthRequest | BirthContext | Calendar calculation |
| 03 | BirthContext | BaziChart | Build Four Pillars |
| 04 | BaziChart | AnalysisResult | Analytical scoring |
| 05 | AnalysisResult | InterpretationResult | Generate interpretation |
| 06 | InterpretationResult | ReportResult | Build report |
| 07 | ReportResult | ViewModel | Adapt for UI |
| 08 | ViewModel | Desktop / Mobile / PDF | Render only |

---

# 5. Stage 01 — Birth Request

Input from the user.

Canonical Model

BirthRequest

Required fields

- full_name
- gender
- birth_date
- birth_time
- timezone
- longitude
- latitude

No calculations occur at this stage.

---

# 6. Stage 02 — Calendar Engine

Consumes

BirthRequest

Produces

BirthContext

Responsibilities

- Solar calendar
- Lunar calendar
- Julian Day
- Solar Terms
- Ganzhi conversion
- Calendar metadata
- Seasonal information
- Time normalization

No BaZi logic is allowed.

---

# 7. Stage 03 — BaZi Engine

Consumes

BirthContext

Produces

BaziChart

Responsibilities

- Four Pillars
- Hidden Stems
- Ten Gods
- Na Yin
- Twelve Growth Phases
- Heavenly Stem relationships
- Earthly Branch relationships

No scoring occurs here.

---

# 8. Stage 04 — Score Engine

Consumes

BaziChart

Produces

AnalysisResult

Responsibilities

- Strength evaluation
- Pattern detection
- Useful God
- Favorable Elements
- Unfavorable Elements
- Five Elements scoring
- Ten Gods scoring
- ShenSha scoring
- Overall scoring

No natural language generation occurs here.

---

# 9. Stage 05 — Interpretation Engine

Consumes

AnalysisResult

Produces

InterpretationResult

Responsibilities

- Executive summary
- Personality
- Career
- Wealth
- Marriage
- Family
- Children
- Health
- Luck
- Recommendations
- Risk analysis

No rendering occurs here.

---

# 10. Stage 06 — Report Engine

Consumes

InterpretationResult

Produces

ReportResult

Responsibilities

- Section assembly
- Report structure
- ViewModel creation
- Report metadata

The Report Engine prepares data only.

It does not render UI.

---

# 11. Stage 07 — Presentation Adapter

Consumes

ReportResult

Produces

Presentation ViewModel

Responsibilities

- Desktop mapping
- Tablet mapping
- Mobile mapping
- PDF mapping

Adapters translate business models into presentation models.

No business logic is allowed.

---

# 12. Stage 08 — Presentation Layer

Consumes

Presentation ViewModel

Responsibilities

Desktop UI

Tablet UI

Mobile UI

PDF

Print

Presentation Layer performs rendering only.

No calculations.

No rules.

No business decisions.

---

# 13. Canonical Models

The pipeline uses six immutable canonical models.

BirthRequest

↓

BirthContext

↓

BaziChart

↓

AnalysisResult

↓

InterpretationResult

↓

ReportResult

Breaking changes require architecture approval.

---

# 14. Dependency Rules

Allowed

Calendar Engine

↓

BaZi Engine

↓

Score Engine

↓

Interpretation Engine

↓

Report Engine

Forbidden

Report → Calendar

Interpretation → Calendar

UI → Calendar

Score → UI

Calendar → Report

Reverse dependencies are prohibited.

---

# 15. Error Handling

Every Engine returns

Result<T>

Example

Result<BirthContext>

Result<BaziChart>

Result<AnalysisResult>

Result<InterpretationResult>

Result<ReportResult>

Errors are propagated through the pipeline.

No Engine may silently ignore failures.

---

# 16. Validation

Each stage validates its input.

If validation fails

↓

Return Result.Error

↓

Stop downstream execution.

Invalid data must never reach later Engines.

---

# 17. Testing Strategy

Every Engine requires

✓ Unit Tests

✓ Integration Tests

✓ Golden Dataset Tests

✓ Regression Tests

Pipeline tests verify the complete runtime.

---

# 18. Runtime Example

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

Canonical Desktop ViewModel

↓

Desktop UI

---

# 19. Future Extension

Future Engines may be inserted only after architecture approval.

Possible extensions

- Feng Shui Engine
- Qi Men Dun Jia Engine
- Zi Wei Engine
- Numerology Engine
- Naming Engine
- Date Selection Engine
- AI Advisory Engine

Extensions must consume and produce canonical models.

Existing Engines must remain unchanged.

---

# 20. Source of Truth

The canonical execution order is:

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

Presentation

↓

Desktop / Tablet / Mobile / PDF

This pipeline is immutable.

Implementation must follow this document.

Never the opposite.

---

END OF DOCUMENT