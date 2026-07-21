# Interpretation Engine Specification

Version: 1.0

Status: Official

---

# 1. Purpose

Interpretation Engine chuyển dữ liệu kỹ thuật thành nội dung luận giải.

Đây là Engine duy nhất sinh văn bản.

---

# 2. Responsibilities

Sinh nội dung cho:

- Personality
- Career
- Wealth
- Marriage
- Health
- Children
- Parents
- Brothers
- Useful God
- Luck Cycle
- Annual Luck
- Recommendations

---

# 3. Non-Responsibilities

Không:

- Tính Tứ Trụ
- Chấm điểm
- Xác định Pattern
- Định dạng PDF

---

# 4. Input

BaziChart

ScoreResult

PatternResult

---

# 5. Output

InterpretationResult

Bao gồm:

- overview
- personality
- career
- wealth
- marriage
- health
- children
- parents
- siblings
- useful_god
- luck_cycle
- annual_luck
- recommendations
- warnings

---

# 6. Public API

InterpretationService

Các phương thức:

generate()

match_rules()

calculate_priority()

build_context()

generate_sentences()

---

# 7. Internal Components

rule_loader.py

rule_matcher.py

rule_scoring.py

context.py

condition_parser.py

interpretation_builder.py

sentence_generator.py

template_loader.py

service.py

exceptions.py

---

# 8. Processing Flow

Input

↓

Load Rules

↓

Build Context

↓

Match Conditions

↓

Calculate Priority

↓

Generate Sentences

↓

Merge Sections

↓

InterpretationResult

---

# 9. Dependencies

Depends On

- Pattern Engine
- Score Engine
- Rule Database
- Template Database

Không phụ thuộc

- Report Engine

---

# 10. Error Handling

InterpretationError

TemplateNotFoundError

RuleNotMatchedError

SentenceGenerationError

---

# 11. Performance

Mục tiêu

<200ms

Template phải cache.

Rule Loader phải cache.

---

# 12. Testing Strategy

Unit Test

- Rule Loader
- Rule Matcher
- Builder
- Sentence Generator

Golden Dataset

Regression Test

Template Test

---

# 13. Future Extensions

- Multiple Languages
- AI Sentence Optimizer
- Style Profiles
- School-specific Interpretation
- Explanation Tree

---

END
