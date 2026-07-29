# BTE Data Models Specification

Version: 1.0

---

# 1. Purpose

Định nghĩa các Data Model dùng chung trong toàn bộ BTE Platform.

Mọi Engine phải giao tiếp thông qua các Model này.

---

# 2. Core Models

BirthInput

↓

CalendarResult

↓

BaziChart

↓

ScoreResult

↓

PatternResult

↓

InterpretationResult

↓

ReportResult

---

# 3. BirthInput

Thuộc tính

- birth_date
- birth_time
- gender
- timezone
- longitude
- latitude

---

# 4. CalendarResult

Thuộc tính

- solar_datetime
- lunar_datetime
- julian_day
- solar_term
- year_pillar
- month_pillar
- day_pillar
- hour_pillar

---

# 5. BaziChart

Thuộc tính

- four_pillars
- hidden_stems
- ten_gods
- na_yin
- twelve_growth_stages
- shen_sha

---

# 6. ScoreResult

Thuộc tính

- strength_score
- five_elements
- ten_gods_score
- useful_god
- unfavorable_god
- pattern_score

---

# 7. PatternResult

Thuộc tính

- primary_pattern
- secondary_pattern
- special_patterns
- confidence

---

# 8. InterpretationResult

Thuộc tính

- personality
- career
- wealth
- marriage
- health
- children
- fortune
- recommendations

---

# 9. ReportResult

Thuộc tính

- markdown
- html
- json
- pdf_path

---

# 10. Design Rules

- Ưu tiên dùng dataclass(slots=True).
- Immutable nếu có thể.
- Có type hints đầy đủ.
- Không dùng dict làm kiểu trả về mặc định.
- Không truyền tuple giữa các Engine.

---

# 11. Serialization

Mọi Result Object phải hỗ trợ:

- to_dict()
- from_dict()
- to_json()

---

# 12. Versioning

Mỗi Model có trường:

model_version

Để hỗ trợ tương thích ngược.

---

END
