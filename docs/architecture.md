# BTE-Platform Architecture

Version: 1.0
Status: Official Architecture

---

# 1. Project Goal

BTE-Platform là nền tảng phân tích Bát Tự (BaZi) theo kiến trúc Engine-Based.

Mọi module đều hoạt động độc lập và giao tiếp thông qua các Data Models.

Không Engine nào được phép truy cập trực tiếp vào Engine khác ngoài Public API.

---

# 2. Core Pipeline

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

# 3. Engine Responsibilities

Calendar Engine

Trách nhiệm

- Solar Calendar
- Lunar Calendar
- Julian Day
- Solar Terms

Không được

- Luận giải
- Chấm điểm

--------------------------------

Bazi Engine

Trách nhiệm

- Four Pillars
- Hidden Stems
- Ten Gods
- ShenSha

Không được

- Chấm điểm
- Sinh báo cáo

--------------------------------

Score Engine

Trách nhiệm

- Strength
- Useful God
- Pattern Score
- Wuxing Score

Không được

- Sinh văn bản

--------------------------------

Pattern Engine

Trách nhiệm

- Pattern Recognition

--------------------------------

Interpretation Engine

Trách nhiệm

- Rule Matching
- Rule Scoring
- Sentence Builder

Không được

- Định dạng báo cáo

--------------------------------

Report Engine

Trách nhiệm

- Markdown
- HTML
- JSON
- PDF

Không được

- Tính toán Bát Tự

---

# 4. Dependency Rules

Calendar

↓

Bazi

↓

Score

↓

Pattern

↓

Interpretation

↓

Report

Không được import ngược.

Ví dụ:

Report Engine

×

import score_engine

là sai.

---

# 5. Public API

Mỗi Engine chỉ được export Service.

Ví dụ

CalendarService

BaziService

ScoreService

PatternService

InterpretationService

ReportService

Không được import file nội bộ.

---

# 6. Database

Database chỉ được đọc.

Không Engine nào được phép ghi dữ liệu vào database.

---

# 7. Tests

tests/

unit/

integration/

golden_dataset/

Mỗi Engine phải có test riêng.

---

# 8. Compatibility

Không được xóa Public API.

Nếu thay đổi API

→ phải giữ backward compatibility.

---

# 9. Coding Principle

Simple

Independent

Modular

Reusable

Testable

Commercial Ready

---

END
