# Score Engine Specification

Version: 1.0

Status: Official

---

# 1. Purpose

Score Engine đánh giá sức mạnh và cấu trúc của lá số.

Đây là Engine chịu trách nhiệm tính điểm, không đưa ra kết luận bằng ngôn ngữ.

---

# 2. Responsibilities

Tính:

- Day Master Strength
- Five Elements Score
- Ten Gods Score
- Useful God
- Favorable Elements
- Unfavorable Elements
- Pattern Score
- Seasonal Score
- Temperature Score

---

# 3. Non-Responsibilities

Không:

- Sinh văn bản
- Sinh Report
- Định dạng kết quả

---

# 4. Input

BaziChart

---

# 5. Output

ScoreResult

Bao gồm:

- strength_score

- wuxing_scores

- ten_gods_scores

- useful_god

- favorable_elements

- unfavorable_elements

- pattern_score

- confidence

---

# 6. Public API

ScoreService

Các phương thức:

calculate_strength()

calculate_wuxing()

calculate_ten_gods()

calculate_useful_god()

calculate_pattern_score()

calculate()

---

# 7. Internal Components

strength/

temperature/

season/

pattern/

useful_god/

calculator.py

rule_loader.py

validators.py

service.py

---

# 8. Processing Flow

BaziChart

↓

Strength

↓

Season

↓

Temperature

↓

Useful God

↓

Pattern Score

↓

Five Elements

↓

Ten Gods

↓

ScoreResult

---

# 9. Dependencies

Bazi Engine

Rule Database

Không phụ thuộc:

Interpretation Engine

Report Engine

---

# 10. Error Handling

ScoreError

RuleNotFoundError

InvalidScoreError

UsefulGodError

---

# 11. Performance

Một lá số

< 150 ms

Rule Database phải cache.

---

# 12. Testing Strategy

Unit Test

- Strength
- Useful God
- Five Elements
- Ten Gods
- Pattern

Golden Dataset

Regression Test

---

# 13. Future Extensions

- Multiple Scoring Models
- AI Assisted Scoring
- School-specific Rule Sets
- Confidence Analysis
- Explainable Scoring

---

END
