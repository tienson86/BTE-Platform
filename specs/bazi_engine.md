# Bazi Engine Specification

Version: 1.0

Status: Official

---

# 1. Purpose

Bazi Engine xây dựng lá số Tứ Trụ từ CalendarResult.

Đây là Engine trung tâm của toàn bộ BTE Platform.

---

# 2. Responsibilities

Bazi Engine phải tính:

- Four Pillars
- Hidden Stems
- Ten Gods
- Five Elements
- Na Yin
- Twelve Growth Stages
- Shen Sha
- Combinations
- Clashes
- Punishments
- Harms

---

# 3. Non-Responsibilities

Không:

- Chấm điểm
- Xác định Dụng Thần
- Luận giải
- Sinh Report

---

# 4. Input

CalendarResult

---

# 5. Output

BaziChart

Bao gồm:

- year_pillar
- month_pillar
- day_pillar
- hour_pillar

- hidden_stems

- ten_gods

- wuxing

- na_yin

- chang_sheng

- shen_sha

- combinations

- clashes

---

# 6. Public API

BaziService

Các phương thức:

calculate_chart()

calculate_hidden_stems()

calculate_ten_gods()

calculate_shen_sha()

---

# 7. Internal Components

pillar/

hidden_stems.py

ten_gods.py

na_yin.py

chang_sheng.py

shen_sha/

relationship/

validators.py

calculator.py

service.py

---

# 8. Processing Flow

CalendarResult

↓

Four Pillars

↓

Hidden Stems

↓

Ten Gods

↓

Na Yin

↓

Chang Sheng

↓

Shen Sha

↓

Relationships

↓

BaziChart

---

# 9. Dependencies

Calendar Engine

Database

Không phụ thuộc:

Score Engine

Pattern Engine

Interpretation Engine

---

# 10. Error Handling

BaziError

InvalidPillarError

HiddenStemError

ShenShaError

---

# 11. Performance

Một lá số

< 100 ms

Shen Sha có thể cache.

---

# 12. Testing Strategy

Unit Test

- Pillars
- Hidden Stems
- Ten Gods
- Na Yin
- Shen Sha

Golden Dataset

Historical Cases

---

# 13. Future Extensions

- Multiple Schools
- Classical Rules
- Rule Plug-ins
- School Selector

---

END
