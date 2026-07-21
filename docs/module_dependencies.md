# BTE Platform - Module Dependencies

Version: 1.0

---

# Dependency Graph

Input

↓

Calendar Engine

↓

Bazi Engine

↓

Score Engine

↓

Pattern Engine

↓

Interpretation Engine

↓

Report Engine

↓

Output

---

# Engine Dependencies

## Calendar Engine

Depends On

- None

Used By

- Bazi Engine

Cannot Import

- Score Engine
- Pattern Engine
- Interpretation Engine
- Report Engine

---

## Bazi Engine

Depends On

- Calendar Engine

Used By

- Score Engine
- Pattern Engine
- Interpretation Engine

Cannot Import

- Report Engine

---

## Score Engine

Depends On

- Bazi Engine
- Database

Used By

- Interpretation Engine

Cannot Import

- Report Engine

---

## Pattern Engine

Depends On

- Bazi Engine
- Database

Used By

- Interpretation Engine

Cannot Import

- Report Engine

---

## Interpretation Engine

Depends On

- Score Engine
- Pattern Engine
- Database

Used By

- Report Engine

Cannot Import

- Calendar Engine
  (trừ Data Models)

---

## Report Engine

Depends On

- Interpretation Engine

Cannot Import

- Calendar Engine
- Bazi Engine
- Score Engine
- Pattern Engine

---

# Shared Modules

Các module sau được phép dùng chung:

models/

schemas/

utils/

common/

exceptions/

constants/

config/

Không Engine nào được sửa dữ liệu của Engine khác.

---

# Database Access

Database

↓

Read Only

Engine

Không được

Engine

↓

Write Database

---

# Allowed Imports

Ví dụ đúng

from engines.score_engine.service import ScoreService

Ví dụ sai

from engines.score_engine.rule_loader import RuleLoader

---

# Public APIs

Mỗi Engine chỉ export:

Service

Engine

Models

Không export file nội bộ.

---

# Pipeline Contract

CalendarResult

↓

BaziResult

↓

ScoreResult

↓

PatternResult

↓

InterpretationResult

↓

ReportResult

Mỗi Engine chỉ nhận đúng Result của Engine trước.

---

END
