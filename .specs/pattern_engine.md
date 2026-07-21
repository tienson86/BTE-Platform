# Pattern Engine Specification

Version: 1.0

Status: Official

---

# 1. Purpose

Pattern Engine xác định Cách Cục (Pattern) của lá số dựa trên dữ liệu từ Bazi Engine và Score Engine.

Đây là Engine chuyên nhận diện cấu trúc lá số, không thực hiện luận giải bằng ngôn ngữ.

---

# 2. Responsibilities

Pattern Engine phải xác định:

- Main Pattern
- Secondary Pattern
- Follow Pattern
- Special Pattern
- Combination Pattern
- Transformation Pattern
- Pattern Confidence
- Pattern Priority

---

# 3. Non-Responsibilities

Không:

- Chấm điểm
- Luận giải
- Sinh Report
- Định dạng dữ liệu

---

# 4. Input

BaziChart

ScoreResult

---

# 5. Output

PatternResult

Bao gồm:

- primary_pattern
- secondary_patterns
- follow_pattern
- transformation_pattern
- special_patterns
- confidence
- matched_rules
- rejected_rules

---

# 6. Public API

PatternService

Các phương thức:

calculate()

identify_pattern()

match_rules()

resolve_conflicts()

calculate_confidence()

---

# 7. Internal Components

pattern.py

calculator.py

rule_loader.py

rule_matcher.py

rule_priority.py

validators.py

service.py

exceptions.py

---

# 8. Processing Flow

BaziChart

↓

Load Rules

↓

Match Conditions

↓

Calculate Priority

↓

Resolve Conflicts

↓

Calculate Confidence

↓

PatternResult

---

# 9. Dependencies

Depends On

- Bazi Engine
- Score Engine
- Rule Database

Không phụ thuộc

- Interpretation Engine
- Report Engine

---

# 10. Error Handling

PatternError

RuleConflictError

PatternNotFoundError

InvalidPatternError

---

# 11. Performance

Mục tiêu

<100ms

Rule phải cache.

Không đọc CSV nhiều lần.

---

# 12. Testing Strategy

Unit Test

- Rule Loader
- Rule Matcher
- Priority
- Confidence

Integration Test

Golden Dataset

Regression Test

---

# 13. Future Extensions

- Multi-school Pattern Recognition
- AI-assisted Pattern Ranking
- User-defined Pattern Rules
- Plugin Architecture

---

END
