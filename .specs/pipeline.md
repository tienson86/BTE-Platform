# BTE Platform Pipeline Specification

Version: 1.0

---

# 1. Purpose

Định nghĩa luồng xử lý dữ liệu xuyên suốt toàn bộ BTE Platform.

Pipeline là tuyến xử lý duy nhất từ đầu vào đến đầu ra.

Không Engine nào được bỏ qua hoặc thay đổi thứ tự Pipeline nếu chưa được thiết kế lại.

---

# 2. Overall Flow

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

# 3. Pipeline Stages

## Stage 1 - Input

Input gồm:

- Ngày sinh
- Giờ sinh
- Giới tính
- Địa điểm sinh
- Múi giờ

Output

BirthInput

---

## Stage 2 - Calendar Engine

Input

BirthInput

Output

CalendarResult

Bao gồm

- Solar Date
- Lunar Date
- Julian Day
- Solar Terms
- Heavenly Stem
- Earthly Branch
- Time Zone

---

## Stage 3 - Bazi Engine

Input

CalendarResult

Output

BaziChart

Bao gồm

- Four Pillars
- Hidden Stems
- Ten Gods
- Twelve Growth Stages
- Na Yin
- Shen Sha

---

## Stage 4 - Score Engine

Input

BaziChart

Output

ScoreResult

Bao gồm

- Day Master Strength
- Five Elements Score
- Ten Gods Score
- Useful God
- Unfavorable God
- Pattern Score

---

## Stage 5 - Pattern Engine

Input

BaziChart

ScoreResult

Output

PatternResult

Bao gồm

- Main Pattern
- Secondary Pattern
- Special Pattern
- Combination Pattern
- Confidence Score

---

## Stage 6 - Interpretation Engine

Input

BaziChart

ScoreResult

PatternResult

Output

InterpretationResult

Bao gồm

- Personality
- Career
- Wealth
- Marriage
- Health
- Children
- Luck Cycle
- Annual Luck
- Recommendations

---

## Stage 7 - Report Engine

Input

InterpretationResult

Output

ReportResult

Định dạng

- Markdown
- HTML
- JSON
- PDF

---

# 4. Pipeline Principles

- Chỉ xử lý theo một chiều.
- Không Engine nào gọi ngược Engine phía sau.
- Dữ liệu luôn truyền bằng Result Object.
- Không truyền dict tự do giữa các Engine.

---

# 5. Error Propagation

Nếu Engine thất bại:

- Trả về Exception rõ ràng.
- Không trả None.
- Không tiếp tục Pipeline nếu dữ liệu không hợp lệ.

---

# 6. Extensibility

Engine mới phải được chèn vào Pipeline thông qua Service Layer.

Không sửa trực tiếp Engine hiện có nếu không cần thiết.

---

END
