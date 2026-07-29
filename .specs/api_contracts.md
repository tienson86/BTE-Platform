# BTE Platform API Contracts

Version: 1.0

Status: Official

---

# 1. Purpose

Tài liệu này định nghĩa các Public API chính thức của từng Engine.

Mọi Engine chỉ được giao tiếp thông qua các API này.

Không Engine nào được gọi trực tiếp Internal Components của Engine khác.

---

# 2. Pipeline API

BirthInput

↓

CalendarService

↓

CalendarResult

↓

BaziService

↓

BaziChart

↓

ScoreService

↓

ScoreResult

↓

PatternService

↓

PatternResult

↓

InterpretationService

↓

InterpretationResult

↓

ReportService

↓

ReportResult

---

# 3. CalendarService

Input

BirthInput

Output

CalendarResult

Methods

calculate()

convert_to_lunar()

calculate_julian_day()

calculate_solar_terms()

Exceptions

CalendarError

InvalidDateError

TimezoneError

---

# 4. BaziService

Input

CalendarResult

Output

BaziChart

Methods

calculate_chart()

calculate_hidden_stems()

calculate_ten_gods()

calculate_shen_sha()

calculate_relationships()

Exceptions

BaziError

InvalidPillarError

---

# 5. ScoreService

Input

BaziChart

Output

ScoreResult

Methods

calculate()

calculate_strength()

calculate_useful_god()

calculate_five_elements()

calculate_pattern_score()

Exceptions

ScoreError

RuleNotFoundError

---

# 6. PatternService

Input

BaziChart

ScoreResult

Output

PatternResult

Methods

calculate()

identify_pattern()

match_rules()

resolve_conflicts()

calculate_confidence()

Exceptions

PatternError

PatternNotFoundError

RuleConflictError

---

# 7. InterpretationService

Input

BaziChart

ScoreResult

PatternResult

Output

InterpretationResult

Methods

generate()

match_rules()

build_context()

generate_sentences()

Exceptions

InterpretationError

TemplateNotFoundError

SentenceGenerationError

---

# 8. ReportService

Input

InterpretationResult

Output

ReportResult

Methods

generate()

render_markdown()

render_html()

render_pdf()

render_docx()

export()

Exceptions

ReportError

RenderError

ExportError

---

# 9. Result Contracts

CalendarService

↓

CalendarResult

↓

Không được trả dict

↓

Không được trả tuple

↓

Phải trả CalendarResult

--------------------------------

BaziService

↓

BaziChart

--------------------------------

ScoreService

↓

ScoreResult

--------------------------------

PatternService

↓

PatternResult

--------------------------------

InterpretationService

↓

InterpretationResult

--------------------------------

ReportService

↓

ReportResult

---

# 10. Error Contracts

Engine không được:

return None

để báo lỗi.

Luôn raise Exception.

---

# 11. Compatibility Rules

Không đổi tên Public API.

Không xóa Public API.

Nếu cần thay đổi

↓

thêm Wrapper.

---

# 12. Versioning

API Version

1.0

Khi thay đổi API

↓

Tăng Minor Version.

Nếu phá Compatibility

↓

Tăng Major Version.

---

# 13. Design Principles

Public API

↓

Stable

Typed

Documented

Backward Compatible

Minimal

---

END
