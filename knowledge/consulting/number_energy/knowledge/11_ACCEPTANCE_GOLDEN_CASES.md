Được. `11_ACCEPTANCE_GOLDEN_CASES.md` sẽ là file **khóa kiểm thử chuẩn cuối cùng của Knowledge Pack**. Mục tiêu của file này là bảo đảm Cursor có thể code engine nhưng **không được thay đổi kết quả tri thức đã chốt**.

Điểm quan trọng: Golden Cases không kiểm tra giao diện đẹp hay không; nó kiểm tra **truth pipeline**:

**Input → Pair → Energy → Strength → Modifier → Interaction → Position → Control → Chain → Domain → Narrative Key.**

```markdown
# 11_ACCEPTANCE_GOLDEN_CASES.md

# BTE NUMBER ENERGY — ACCEPTANCE & GOLDEN CASES

**Module:** Number Energy Consulting  
**Vietnamese Name:** Tư vấn Năng lượng số  
**Method:** Bát Cực Linh Số  
**Document:** Acceptance & Golden Cases  
**Knowledge Status:** CANONICAL  
**Version:** 1.0  
**Authority Level:** ACCEPTANCE STANDARD  
**Parent Standard:** `00_NUMBER_ENERGY_MASTER.md`

**Depends On:**
- `01_BAGUA_DIGIT_MAPPING.md`
- `02_EIGHT_ENERGY_CATALOG.md`
- `03_PAIR_STRENGTH_MATRIX.md`
- `04_DIRECTED_INTERACTION_MATRIX.md`
- `05_ZERO_FIVE_MODIFIERS.md`
- `06_POSITION_AND_TAIL_RULES.md`
- `07_CONTROL_REMEDY_RULES.md`
- `08_CHAIN_INTERPRETATION_RULES.md`
- `09_DOMAIN_INTERPRETATION.md`
- `10_CUSTOMER_NARRATIVE_CATALOG.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa Golden Dataset
và Acceptance Contract
cho Number Energy Engine.

Mỗi Golden Case dùng để xác nhận:

INPUT
↓
NORMALIZATION
↓
PAIR RESOLUTION
↓
ENERGY CLASS
↓
STRENGTH
↓
MODIFIER
↓
DIRECTED INTERACTION
↓
POSITION
↓
CONTROL / REMEDY
↓
CHAIN
↓
DOMAIN
↓
NARRATIVE SELECTION

Nếu runtime cho kết quả khác Golden Case
mà chưa có thay đổi Knowledge được phê duyệt:

```text
TEST = FAIL
```

---

# 2. GOLDEN DATASET PRINCIPLE

Golden Dataset là:

```text
TRUTH TEST
```

Không phải:

```text
EXAMPLE ONLY
```

Mỗi Golden Case phải deterministic
ở tầng Knowledge.

LLM không được phép
thay đổi expected semantic truth.

---

# 3. ACCEPTANCE LEVELS

Canonical acceptance levels:

```text
A0 — INPUT
A1 — PAIR
A2 — ENERGY
A3 — STRENGTH
A4 — MODIFIER
A5 — INTERACTION
A6 — POSITION
A7 — CONTROL
A8 — CHAIN
A9 — DOMAIN
A10 — NARRATIVE
```

Một case chỉ PASS khi
tất cả level áp dụng đều PASS.

---

# 4. GLOBAL INVARIANTS

Mọi Golden Case phải tuân thủ:

```text
ORDER_IS_SEMANTIC = TRUE
```

```text
AB != BA
at sequence interpretation level
```

```text
0 != normal Bagua digit
```

```text
5 != normal Bagua digit
```

```text
0 != Phục Vị
5 != Phục Vị
```

```text
Strength != Goodness
```

```text
Tail != Whole Sequence
```

```text
Control != Delete
```

```text
One Pair != Whole Number Conclusion
```

```text
Customer Narrative != Medical Diagnosis
```

---

# 5. GOLDEN CASE ID FORMAT

Canonical:

```text
NE-GD-XXXX
```

Example:

```text
NE-GD-0001
```

Optional profile suffix:

```text
-PHONE
-CAR
-MOTORBIKE
```

---

# 6. CASE TEMPLATE

Every case SHOULD contain:

```text
case_id
input
profile

normalized_digits

pairs
energies
strengths

modifiers
interactions
positions

control_rules
chain

dominant_energy
terminal_state

domains
narrative_keys

must_not
status
```

---

# 7. NE-GD-0001 — 813

## Input

```text
813
```

Profile:

```text
PHONE
```

## Pair Resolution

```text
81 = WU_GUI
13 = TIAN_Y
```

## Strength

```text
81 = WU_GUI_T1
13 = TIAN_Y_T1
```

## Directed Interaction

```text
WU_GUI → TIAN_Y
```

Interaction ID:

```text
INT-WG-TY
```

## Semantic

```text
INTELLIGENCE / CREATIVITY
→
WEALTH / RESOURCE
```

## Position

Only one interaction.

Therefore:

```text
PRIMARY = TRUE
TERMINAL = TRUE
```

Terminal Energy:

```text
TIAN_Y
```

## Control

No primary canonical control rule triggered
from the three base control mappings.

## Domain

WEALTH:

```text
PRIMARY
```

CAREER:

```text
creative/intellectual tendency
```

BALANCE:

```text
contextual
```

## Expected Narrative Key

```text
NAR-WEALTH-WG-TY-001
```

## Customer Meaning

> Khả năng dùng trí tuệ, ý tưởng hoặc sáng tạo
> để tạo ra giá trị tài chính.

## MUST NOT

```text
813 = bad because WU_GUI exists
```

MUST NOT:

```text
ignore terminal TIAN_Y
```

Status:

```text
GOLDEN
```

---

# 8. NE-GD-0002 — 318

## Input

```text
318
```

## Pairs

```text
31 = TIAN_Y_T1
18 = WU_GUI_T1
```

## Interaction

```text
TIAN_Y → WU_GUI
```

ID:

```text
INT-TY-WG
```

## Semantic

```text
RESOURCE
→
VOLATILITY / CHANGE
```

## Terminal

```text
WU_GUI
```

## Expected Domain

WEALTH:

```text
resource flow unstable
```

BALANCE:

```text
challenging convergence
```

## Narrative Candidate

```text
NAR-WEALTH-VOLATILE-001
```

## Critical Comparison

```text
318 != 813
```

Even though both contain:

```text
TIAN_Y
WU_GUI
```

Order changes meaning.

## MUST NOT

```text
sort energies
```

MUST NOT:

```text
return same result as 813
```

Status:

```text
GOLDEN
```

---

# 9. NE-GD-0003 — 213

## Input

```text
213
```

## Pairs

```text
21 = JUE_MING_T1
13 = TIAN_Y_T1
```

## Interaction

```text
JUE_MING → TIAN_Y
```

ID:

```text
INT-JM-TY
```

## Semantic

```text
ACTION / INVESTMENT
→
WEALTH
```

## Control

Match:

```text
CTRL-JM-TY
```

Canonical:

```text
Thiên Y chế Tuyệt Mệnh
```

## Important

Interaction meaning AND control meaning
must both be preserved.

Do NOT collapse to only:

```text
remedy
```

## Investment Matrix

```text
JUE_MING = T1
TIAN_Y = T1
```

Relative:

```text
HIGH ACTION / HIGH RESULT POTENTIAL
```

Not guaranteed profit.

## Terminal

```text
TIAN_Y
```

## Domains

WEALTH:

```text
PRIMARY
```

INVESTMENT:

```text
STRONG
```

BALANCE:

```text
CONTROL PRESENT
```

## Narrative Keys

```text
NAR-WEALTH-JM-TY-001
NAR-CTRL-JM-TY-001
NAR-INV-HRHR-001
```

## MUST NOT

```text
213 guarantees investment profit
```

Status:

```text
GOLDEN
```

---

# 10. NE-GD-0004 — 312

## Input

```text
312
```

## Pairs

```text
31 = TIAN_Y_T1
12 = JUE_MING_T1
```

## Interaction

```text
TIAN_Y → JUE_MING
```

## Semantic

```text
RESOURCE
→
INVESTMENT / EXPENDITURE / RISK
```

## Control

```text
CTRL-JM-TY = NO MATCH
```

Reason:

Wrong direction.

## Terminal

```text
JUE_MING
```

## Critical Comparison

```text
312 != 213
```

## Domain

INVESTMENT:

```text
resource sent into risk/action
```

BALANCE:

```text
challenging terminal
```

## MUST NOT

Call Thiên Y as controlling Tuyệt Mệnh
because Thiên Y appears before it.

Status:

```text
GOLDEN
```

---

# 11. NE-GD-0005 — 719

## Input

```text
719
```

## Pairs

```text
71 = HUO_HAI_T1
19 = YAN_NIAN_T1
```

## Interaction

```text
HUO_HAI → YAN_NIAN
```

ID:

```text
INT-HH-YN
```

## Semantic

```text
COMMUNICATION
→
CAREER
```

## Domain

CAREER:

```text
PRIMARY
```

Possible themes:

- bán hàng;
- tư vấn;
- giảng dạy;
- truyền thông;
- đàm phán;
- nghề sử dụng ngôn ngữ.

## Terminal

```text
YAN_NIAN
```

## Narrative Key

```text
NAR-CAREER-HH-YN-001
```

## MUST NOT

```text
Họa Hại exists = bad career
```

Status:

```text
GOLDEN
```

---

# 12. NE-GD-0006 — 619

## Input

```text
619
```

## Pairs

```text
61 = LIU_SHA_T1
19 = YAN_NIAN_T1
```

## Interaction

```text
LIU_SHA → YAN_NIAN
```

ID:

```text
INT-LS-YN
```

## Semantic

```text
SERVICE / SOCIAL
→
CAREER
```

## Control

Match:

```text
CTRL-LS-YN
```

Canonical:

```text
Diên Niên yểm Lục Sát
```

## Domains

CAREER:

```text
PRIMARY
```

BALANCE:

```text
CONTROL PRESENT
```

SOCIAL:

```text
STRONG
```

## Narrative Keys

```text
NAR-CAREER-LS-YN-001
NAR-CTRL-LS-YN-001
```

## MUST NOT

Delete Lục Sát
after detecting control.

Status:

```text
GOLDEN
```

---

# 13. NE-GD-0007 — 916

## Input

```text
916
```

## Pairs

```text
91 = YAN_NIAN_T1
16 = LIU_SHA_T1
```

## Interaction

```text
YAN_NIAN → LIU_SHA
```

## Semantic

```text
CAREER
→
EMOTIONAL / SOCIAL PRESSURE
```

## Control

```text
CTRL-LS-YN = NO MATCH
```

Reason:

Order reversed.

## Terminal

```text
LIU_SHA
```

## Critical

```text
916 != 619
```

Status:

```text
GOLDEN
```

---

# 14. NE-GD-0008 — 103

## Input

```text
103
```

## Active Underlying Relation

```text
1 ↔ 3
=
13
=
TIAN_Y_T1
```

## Modifier

```text
0
```

Position:

```text
INTERPOSED
```

## Result

```text
TIAN_Y_HIDDEN
```

## Domains

WEALTH:

```text
wealth/resource hidden or reduced
```

RELATIONSHIP:

```text
relationship expression hidden
```

## Terminal State

```text
TIAN_Y_HIDDEN
```

## Narrative Keys

```text
NAR-MOD-ZERO-001
NAR-WEALTH-HIDDEN-001
NAR-REL-HIDDEN-001
```

## MUST NOT

Parse as:

```text
10
03
```

normal Du Niên pairs.

MUST NOT:

```text
0 deletes TIAN_Y
```

MUST NOT:

```text
103 = affair
```

Status:

```text
GOLDEN
```

---

# 15. NE-GD-0009 — 153

## Input

```text
153
```

## Underlying

```text
13 = TIAN_Y_T1
```

## Modifier

```text
5
```

Position:

```text
INTERPOSED
```

## State

```text
TIAN_Y_AMPLIFIED
```

## Domains

WEALTH:

```text
resource visibility increased
```

RELATIONSHIP:

```text
relationship visibility increased
```

## Narrative Keys

```text
NAR-MOD-FIVE-001
NAR-WEALTH-AMPLIFIED-001
NAR-REL-AMPLIFIED-001
```

## Critical Comparison

```text
153 != 103
```

Status:

```text
GOLDEN
```

---

# 16. NE-GD-0010 — 130

## Input

```text
130
```

## Pair

```text
13 = TIAN_Y_T1
```

## Modifier

```text
0 = POST
```

## State

```text
formed TIAN_Y
→
HIDDEN / REDUCED
```

## Terminal

```text
TIAN_Y_HIDDEN
```

## Important

```text
130 != 103
```

Both involve Zero + Thiên Y,
but modifier position differs.

## MUST NOT

Normalize modifier position away.

Status:

```text
GOLDEN
```

---

# 17. NE-GD-0011 — 135

## Input

```text
135
```

## Pair

```text
13 = TIAN_Y_T1
```

## Modifier

```text
5 = POST
```

## State

```text
TIAN_Y_AMPLIFIED
```

## Terminal

```text
TIAN_Y_AMPLIFIED
```

## Critical

```text
135 != 153
```

Both amplify Thiên Y,
but modifier position must remain traceable.

Status:

```text
GOLDEN
```

---

# 18. NE-GD-0012 — 104

## Input

```text
104
```

## Underlying

```text
14 = SHENG_QI_T1
```

## Modifier

```text
ZERO / INTERPOSED
```

## State

```text
SHENG_QI_HIDDEN
```

## Domain

SOCIAL / SUPPORT:

```text
benefactor / opportunity less visible
```

## MUST NOT

Output:

```text
no benefactor exists
```

Status:

```text
GOLDEN
```

---

# 19. NE-GD-0013 — 154

## Input

```text
154
```

## Underlying

```text
14 = SHENG_QI_T1
```

## Modifier

```text
FIVE / INTERPOSED
```

## State

```text
SHENG_QI_AMPLIFIED
```

## Meaning

- quý nhân/cơ hội rõ hơn;
- trợ lực dễ nhận biết.

Status:

```text
GOLDEN
```

---

# 20. NE-GD-0014 — 109

## Input

```text
109
```

## Underlying

```text
19 = YAN_NIAN_T1
```

## Modifier

```text
ZERO / INTERPOSED
```

## State

```text
YAN_NIAN_HIDDEN
```

## Career

- có năng lực;
- khó phát huy;
- chuyên môn khó được nhìn thấy đầy đủ.

## MUST NOT

```text
no career ability
```

Status:

```text
GOLDEN
```

---

# 21. NE-GD-0015 — 159

## Input

```text
159
```

## Underlying

```text
19 = YAN_NIAN_T1
```

## Modifier

```text
FIVE / INTERPOSED
```

## State

```text
YAN_NIAN_AMPLIFIED
```

## Career

- năng lực dễ biểu hiện;
- chuyên môn nổi bật;
- tính chủ động rõ.

Status:

```text
GOLDEN
```

---

# 22. NE-GD-0016 — 181

## Input

```text
181
```

## Pairs

```text
18 = WU_GUI_T1
81 = WU_GUI_T1
```

## Interaction

```text
WU_GUI → WU_GUI
```

ID:

```text
INT-WG-WG
```

## State

```text
REINFORCED_WU_GUI
```

## Meaning

Positive:

- phản ứng nhanh;
- sáng tạo;
- tư duy mạnh.

Risk:

- biến động tăng;
- thiếu ổn định;
- thay đổi nhiều.

## Terminal

```text
WU_GUI
```

## Domains

PERSONALITY:

```text
STRONG
```

BALANCE:

```text
VOLATILITY ELEVATED
```

## MUST NOT

```text
WU_GUI repeated = automatic disaster
```

Status:

```text
GOLDEN
```

---

# 23. NE-GD-0017 — 131

## Input

```text
131
```

## Pairs

```text
13 = TIAN_Y_T1
31 = TIAN_Y_T1
```

## Interaction

```text
TIAN_Y → TIAN_Y
```

## State

```text
REINFORCED_TIAN_Y
```

## Domains

WEALTH:

```text
STRONG
```

RELATIONSHIP:

```text
STRONG
```

## Caution

More Thiên Y does not automatically mean
unlimited benefit.

## Narrative Key

Possible:

```text
NAR-REL-TY-TY-001
```

Status:

```text
GOLDEN
```

---

# 24. NE-GD-0018 — 611

## Input

```text
611
```

## Pairs

```text
61 = LIU_SHA_T1
11 = FU_WEI_T1
```

## Interaction

```text
LIU_SHA → FU_WEI
```

## Semantic

```text
emotion / relationship
→
continuation
```

## State

```text
EXTENDED_LIU_SHA
```

## Domains

RELATIONSHIP:

- cảm xúc kéo dài;
- do dự;
- khó dứt;
- cần cảm giác an toàn.

BALANCE:

```text
challenging state extended
```

## Narrative Key

```text
NAR-REL-LS-FW-001
NAR-FW-EXTEND-CHALLENGING-001
```

Status:

```text
GOLDEN
```

---

# 25. NE-GD-0019 — 144

## Input

```text
144
```

## Pairs

```text
14 = SHENG_QI_T1
44 = FU_WEI_T4
```

## Interaction

```text
SHENG_QI → FU_WEI
```

## State

```text
EXTENDED_SHENG_QI
```

## Meaning

- quý nhân/cơ hội được duy trì;
- trạng thái thuận được kéo dài.

## Narrative Key

```text
NAR-FW-EXTEND-POSITIVE-001
```

Status:

```text
GOLDEN
```

---

# 26. NE-GD-0020 — 108

## Input

```text
108
```

## Underlying

```text
18 = WU_GUI_T1
```

## Modifier

```text
0 / INTERPOSED
```

## State

```text
WU_GUI_HIDDEN
WU_GUI_INTERNALIZED
```

## Meaning

- hoạt động trí óc mạnh;
- biểu hiện bên ngoài thấp hơn;
- suy nghĩ/biến động mang tính nội tại.

## MUST NOT

```text
WU_GUI removed
```

MUST NOT output
medical/extreme source claims.

Status:

```text
GOLDEN
```

---

# 27. NE-GD-0021 — 219

## Input

```text
219
```

## Pairs

```text
21 = JUE_MING_T1
19 = YAN_NIAN_T1
```

## Interaction

```text
JUE_MING → YAN_NIAN
```

## Semantic

```text
ACTION / RISK
→
CAREER / STRUCTURE
```

## Domain

CAREER:

- kinh doanh;
- hành động;
- phát triển;
- công việc cần quyết đoán.

INVESTMENT:

contextual.

## Control

No direct canonical control rule
among base three.

## Terminal

```text
YAN_NIAN
```

## Narrative Key

```text
NAR-CAREER-JM-YN-001
```

Status:

```text
GOLDEN
```

---

# 28. NE-GD-0022 — 913

## Input

```text
913
```

## Pairs

```text
91 = YAN_NIAN_T1
13 = TIAN_Y_T1
```

## Interaction

```text
YAN_NIAN → TIAN_Y
```

## Semantic

```text
PROFESSIONAL CAPACITY
→
WEALTH
```

## Wealth Source

```text
SKILL / PROFESSIONAL ABILITY
```

## Terminal

```text
TIAN_Y
```

## Narrative Key

```text
NAR-WEALTH-YN-TY-001
```

Status:

```text
GOLDEN
```

---

# 29. NE-GD-0023 — 713

## Input

```text
713
```

## Pairs

```text
71 = HUO_HAI_T1
13 = TIAN_Y_T1
```

## Interaction

```text
HUO_HAI → TIAN_Y
```

## Semantic

```text
COMMUNICATION
→
WEALTH
```

## Wealth Source

- bán hàng;
- tư vấn;
- đào tạo;
- đàm phán;
- truyền thông.

## Terminal

```text
TIAN_Y
```

## Narrative Key

```text
NAR-WEALTH-HH-TY-001
```

Status:

```text
GOLDEN
```

---

# 30. NE-GD-0024 — 317

## Input

```text
317
```

## Pairs

```text
31 = TIAN_Y_T1
17 = HUO_HAI_T1
```

## Interaction

```text
TIAN_Y → HUO_HAI
```

## Meaning

```text
RESOURCE
→
SOCIAL / SPEECH / EXPENDITURE
```

## Terminal

```text
HUO_HAI
```

## Critical

```text
317 != 713
```

Status:

```text
GOLDEN
```

---

# 31. NE-GD-0025 — 8139

## Input

```text
8139
```

## Pairs

```text
81 = WU_GUI_T1
13 = TIAN_Y_T1
39 = SHENG_QI_T3
```

## Chain

```text
WU_GUI
→
TIAN_Y
→
SHENG_QI
```

## Interactions

```text
INT-WG-TY
INT-TY-SQ
```

## Flow

```text
INTELLIGENCE / CREATIVITY
→
RESOURCE
→
NETWORK / SUPPORT
```

## Terminal

```text
SHENG_QI
```

## Expected Synthesis

- trí tuệ/sáng tạo tạo tài;
- tài nguyên có xu hướng đi vào quan hệ/trợ lực;
- cuối dãy quy về Sinh Khí.

## MUST NOT

Only report:

```text
WU_GUI → TIAN_Y
```

and ignore remaining chain.

Status:

```text
GOLDEN
```

---

# 32. NE-GD-0026 — 81396

## Input

```text
81396
```

## Pairs

```text
81 = WU_GUI_T1
13 = TIAN_Y_T1
39 = SHENG_QI_T3
96 = JUE_MING_T2
```

## Chain

```text
WU_GUI
→
TIAN_Y
→
SHENG_QI
→
JUE_MING
```

## Flow

```text
CREATIVITY
→
RESOURCE
→
SUPPORT
→
ACTION / RISK
```

## Terminal

```text
JUE_MING
```

## General

```text
MIXED
```

Reason:

positive middle process
but challenging terminal.

## Narrative Candidate

```text
NAR-BAL-GOODPROC-BADTAIL-001
```

## MUST NOT

Declare whole chain strongly supportive
because first three states are favorable.

Status:

```text
GOLDEN
```

---

# 33. NE-GD-0027 — 141319

## Input

```text
141319
```

## Relevant Pairs

At minimum engine must identify:

```text
14 = SHENG_QI_T1
13 = TIAN_Y_T1
19 = YAN_NIAN_T1
```

within ordered sequence.

Engine MUST NOT rely solely on
literal substring hard-coding.

## Canonical Remedy Pattern

Recognize ordered energy sequence:

```text
SHENG_QI
→
TIAN_Y
→
YAN_NIAN
```

as:

```text
CTRL-WG-STRONG-CHAIN
```

when used in appropriate Ngũ Quỷ remedy context.

## Critical Rule

```text
ORDER_IS_FIXED
```

## MUST NOT

Treat any permutation
of SQ/TY/YN as equivalent.

Status:

```text
GOLDEN_PATTERN
```

---

# 34. NE-GD-0028 — WRONG STRONG REMEDY ORDER

Conceptual chain:

```text
WU_GUI
→
TIAN_Y
→
SHENG_QI
→
YAN_NIAN
```

Expected:

```text
CTRL-WG-STRONG-CHAIN = NO MATCH
```

Individual interactions still valid.

## MUST NOT

Reorder energy sequence before matching remedy.

Status:

```text
GOLDEN_NEGATIVE
```

---

# 35. NE-GD-0029 — WU_GUI → SHENG_QI

Conceptual chain:

```text
WU_GUI_T1
→
SHENG_QI_T1
```

Expected:

```text
CTRL-WG-SQ
order_valid = TRUE
```

Control:

```text
STRONG
```

subject to position/modifier.

## MUST NOT

Delete WU_GUI from evidence.

Status:

```text
GOLDEN
```

---

# 36. NE-GD-0030 — SHENG_QI → WU_GUI

Conceptual chain:

```text
SHENG_QI_T1
→
WU_GUI_T1
```

Expected:

```text
CTRL-WG-SQ = NO MATCH
```

Terminal:

```text
WU_GUI
```

Critical:

```text
reverse != same control
```

Status:

```text
GOLDEN_NEGATIVE
```

---

# 37. NE-GD-0031 — WU_GUI → FU_WEI → SHENG_QI

Conceptual:

```text
WU_GUI
→
FU_WEI
→
SHENG_QI
```

Expected sequence:

1. WU_GUI appears.
2. FU_WEI extends WU_GUI.
3. SHENG_QI later attempts control.

Expected:

```text
control exists
but is weaker than direct WG → SQ
all else equal
```

## MUST NOT

Simplify chain to:

```text
WU_GUI → SHENG_QI
```

Status:

```text
GOLDEN
```

---

# 38. NE-GD-0032 — WU_GUI → SHENG_QI → ZERO

Conceptual chain:

```text
WU_GUI
→
SHENG_QI
→
ZERO
```

Expected:

```text
CTRL-WG-SQ exists
```

But:

```text
SHENG_QI = HIDDEN / REDUCED
```

Therefore final control:

```text
PARTIAL / REDUCED
```

not full.

Status:

```text
GOLDEN
```

---

# 39. NE-GD-0033 — WU_GUI → SHENG_QI → FIVE

Conceptual:

```text
WU_GUI
→
SHENG_QI
→
FIVE
```

Expected:

```text
CTRL-WG-SQ exists
SHENG_QI_AMPLIFIED
```

Control prominence:

```text
INCREASED
```

subject to full chain.

Status:

```text
GOLDEN
```

---

# 40. NE-GD-0034 — REAPPEARING WU_GUI

Chain:

```text
WU_GUI
→
SHENG_QI
→
WU_GUI
```

Expected:

First WU_GUI:

```text
locally controlled
```

Later WU_GUI:

```text
reappears
```

Terminal:

```text
WU_GUI
```

Global control:

```text
FALSE
```

Critical rule:

```text
LOCAL_CONTROL != GLOBAL_CONTROL
```

Status:

```text
GOLDEN
```

---

# 41. NE-GD-0035 — STRONG CONTROLLED CHAIN

Chain:

```text
WU_GUI
→
SHENG_QI
→
TIAN_Y
→
YAN_NIAN
```

Expected:

```text
CTRL-WG-SQ
```

and:

```text
CTRL-WG-STRONG-CHAIN
```

Flow:

```text
VOLATILITY
→
SUPPORT
→
RESOURCE
→
STRUCTURE
```

Terminal:

```text
YAN_NIAN
```

Convergence:

```text
FAVORABLE / STRUCTURED
```

subject to strength/modifier.

Status:

```text
GOLDEN
```

---

# 42. NE-GD-0036 — POSITIVE → FUNCTIONAL CHALLENGE → POSITIVE

Chain:

```text
SHENG_QI
→
JUE_MING
→
TIAN_Y
```

Interpretation:

```text
OPPORTUNITY
→
ACTION / INVESTMENT
→
RESOURCE
```

Expected principle:

```text
Cát làm chủ
Hung làm dụng
```

if:

- JUE_MING not uncontrolled;
- terminal TIAN_Y healthy;
- modifiers do not reverse structure.

## MUST NOT

Mark entire chain bad
because JUE_MING is present.

Status:

```text
GOLDEN
```

---

# 43. NE-GD-0037 — ALL CHALLENGING

Conceptual chain:

```text
HUO_HAI
→
WU_GUI
→
LIU_SHA
→
JUE_MING
```

Expected:

```text
HIGH_CHALLENGE_DENSITY
HIGH_VARIABILITY
```

But must still preserve functional meanings:

```text
HUO_HAI = communication
WU_GUI = creativity
LIU_SHA = social/emotional
JUE_MING = action
```

## MUST NOT

Customer output:

```text
Đại hung.
```

Status:

```text
GOLDEN
```

---

# 44. NE-GD-0038 — ALL AUSPICIOUS

Conceptual:

```text
SHENG_QI
→
TIAN_Y
→
YAN_NIAN
```

Expected:

```text
SUPPORT
→
RESOURCE
→
STRUCTURE
```

General:

```text
SUPPORTIVE
```

But:

```text
MORE AUSPICIOUS != AUTOMATICALLY PERFECT
```

Need balance and purpose.

Status:

```text
GOLDEN
```

---

# 45. NE-GD-0039 — HIGH RISK / LOW RESULT

Conceptual:

```text
JUE_MING_T1
→
TIAN_Y_T4
```

Expected Investment Finding:

```text
HIGH_RISK_LOW_REWARD
```

Narrative key:

```text
NAR-INV-HRLR-001
```

MUST NOT output
guaranteed financial loss.

Status:

```text
GOLDEN
```

---

# 46. NE-GD-0040 — LOWER RISK / STRONG RESULT

Conceptual:

```text
JUE_MING_T4
→
TIAN_Y_T1
```

Expected:

```text
LOWER_RISK_STRONGER_RESULT
```

Narrative key:

```text
NAR-INV-LRHR-001
```

Not guaranteed profit.

Status:

```text
GOLDEN
```

---

# 47. NE-GD-0041 — STRONG DIÊN NIÊN → WEAK DIÊN NIÊN

Conceptual:

```text
YAN_NIAN_T1
→
YAN_NIAN_T4
```

Expected:

```text
CAREER_STRENGTH_TREND = DECLINING
```

Meaning:

- capacity starts strong;
- later professional intensity reduces.

MUST preserve tier transition.

Status:

```text
GOLDEN
```

---

# 48. NE-GD-0042 — WEAK DIÊN NIÊN → STRONG DIÊN NIÊN

Conceptual:

```text
YAN_NIAN_T4
→
YAN_NIAN_T1
```

Expected:

```text
CAREER_STRENGTH_TREND = INCREASING
```

Critical:

```text
T1→T4 != T4→T1
```

Status:

```text
GOLDEN
```

---

# 49. NE-GD-0043 — HỌA HẠI → PHỤC VỊ

Conceptual:

```text
HUO_HAI
→
FU_WEI
```

Expected:

```text
EXTENDED_HUO_HAI
```

Meaning:

- lời nói/tranh luận kéo dài;
- mạnh miệng;
- khó nhường.

Narrative key:

```text
NAR-FW-EXTEND-CHALLENGING-001
```

Status:

```text
GOLDEN
```

---

# 50. NE-GD-0044 — THIÊN Y → PHỤC VỊ

Conceptual:

```text
TIAN_Y
→
FU_WEI
```

Expected:

```text
EXTENDED_TIAN_Y
```

Meaning:

- tài nguyên/tình cảm được duy trì;
- state prolonged.

Narrative may use:

```text
NAR-FW-EXTEND-POSITIVE-001
```

Status:

```text
GOLDEN
```

---

# 51. NE-GD-0045 — TAIL ZERO

Conceptual terminal:

```text
TIAN_Y
→
ZERO
```

Expected:

```text
terminal_state = TIAN_Y_HIDDEN
convergence = HIDDEN_CONVERGENCE
```

Narrative:

```text
NAR-TAIL-ZERO-001
```

MUST NOT trim trailing zero.

Status:

```text
GOLDEN
```

---

# 52. NE-GD-0046 — TAIL FIVE

Conceptual terminal:

```text
TIAN_Y
→
FIVE
```

Expected:

```text
terminal_state = TIAN_Y_AMPLIFIED
```

Narrative:

```text
NAR-TAIL-FIVE-001
```

Status:

```text
GOLDEN
```

---

# 53. NE-GD-0047 — CHALLENGING TAIL

Conceptual:

```text
SHENG_QI
→
TIAN_Y
→
WU_GUI
```

Expected:

Process:

```text
supportive
```

Terminal:

```text
WU_GUI
```

Convergence:

```text
CHALLENGING
```

Narrative:

```text
NAR-BAL-GOODPROC-BADTAIL-001
```

Status:

```text
GOLDEN
```

---

# 54. NE-GD-0048 — CHALLENGING PROCESS / AUSPICIOUS TAIL

Conceptual:

```text
HUO_HAI
→
TIAN_Y
```

Expected:

```text
functional challenge
→
auspicious result
```

Convergence:

```text
FAVORABLE
```

Narrative:

```text
NAR-BAL-BADPROC-GOODTAIL-001
```

Status:

```text
GOLDEN
```

---

# 55. NE-GD-0049 — SAME DOMINANT / DIFFERENT TERMINAL

Case A:

```text
dominant = YAN_NIAN
terminal = SHENG_QI
```

Expected summary:

> Dãy thiên về sự nghiệp/năng lực,
> nhưng phần cuối quy về quý nhân/trợ lực.

MUST NOT replace dominant
with terminal.

Status:

```text
GOLDEN_INVARIANT
```

---

# 56. NE-GD-0050 — TERMINAL ≠ DOMINANT

Expected engine support:

```text
PRIMARY_ENERGY
SECONDARY_ENERGY
TERMINAL_ENERGY
```

All must be separately available.

Status:

```text
GOLDEN_INVARIANT
```

---

# 57. NE-GD-0051 — PHONE PROFILE

Input:

Any valid long phone sequence.

Expected domains:

```text
GENERAL
WEALTH
CAREER
RELATIONSHIP
PERSONALITY
SOCIAL
INVESTMENT
LEARNING
WELLNESS_REFERENCE
BALANCE
```

Customer priority:

```text
GENERAL
WEALTH
CAREER
RELATIONSHIP
PERSONALITY
BALANCE
RECOMMENDATION
```

## MUST NOT

Analyze only last four digits.

Status:

```text
GOLDEN_PROFILE
```

---

# 58. NE-GD-0052 — CAR PLATE PROFILE

Input:

Valid car plate numeric sequence.

Expected priorities:

```text
GENERAL
BALANCE
STABILITY
CAREER
WEALTH
ACTION
TERMINAL
```

Reduced:

```text
RELATIONSHIP
DEEP_PERSONALITY
```

## MUST NOT

Copy Phone narrative unchanged.

Status:

```text
GOLDEN_PROFILE
```

---

# 59. NE-GD-0053 — MOTORBIKE PLATE PROFILE

Same intrinsic engine as car plate.

Expected:

```text
SAME ENERGY TRUTH
DIFFERENT USAGE PROFILE ALLOWED
```

No new mystical mapping.

Status:

```text
GOLDEN_PROFILE
```

---

# 60. NE-GD-0054 — VEHICLE SAFETY LANGUAGE

If chain contains:

```text
JUE_MING
WU_GUI
HUO_HAI
```

customer output MUST NOT say:

```text
biển số gây tai nạn
```

Allowed:

> Cấu trúc có mức hành động hoặc biến động cao,
> vì vậy tính ổn định chưa phải điểm mạnh nổi bật.

Status:

```text
GOLDEN_SAFETY
```

---

# 61. NE-GD-0055 — WELLNESS SAFETY

If Knowledge Source contains
health associations:

Customer output MUST include:

```text
Nội dung sức khỏe chỉ mang tính tham khảo
theo hệ thống Bát Cực Linh Số,
không thay thế đánh giá y khoa.
```

MUST NOT diagnose.

Status:

```text
GOLDEN_SAFETY
```

---

# 62. NE-GD-0056 — RELATIONSHIP SAFETY

Input may contain:

```text
103
608
LIU_SHA
WU_GUI
```

MUST NOT output:

```text
ngoại tình chắc chắn
ly hôn chắc chắn
```

Allowed:

```text
relationship hidden
relationship complex
emotional volatility
```

Status:

```text
GOLDEN_SAFETY
```

---

# 63. NE-GD-0057 — FINANCIAL SAFETY

For:

```text
JUE_MING → TIAN_Y
```

MUST NOT say:

```text
đầu tư chắc thắng
```

For:

```text
TIAN_Y → WU_GUI
```

MUST NOT say:

```text
chắc chắn phá sản
```

Allowed:

- khả năng tạo tài;
- biến động;
- risk/reward;
- dòng tiền.

Status:

```text
GOLDEN_SAFETY
```

---

# 64. NE-GD-0058 — NARRATIVE DEDUPLICATION

If three findings all reference:

```text
creativity
```

customer output MUST NOT repeat
same sentence three times.

Expected:

- GENERAL: tổng hợp;
- WEALTH: creativity → wealth;
- CAREER: creative profession.

Semantic variation allowed.
Meaning must remain canonical.

Status:

```text
GOLDEN_NARRATIVE
```

---

# 65. NE-GD-0059 — NO FREE-FORM KNOWLEDGE

If no canonical Narrative Key
matches a Finding:

Runtime MUST NOT invent
new spiritual meaning.

Expected:

```text
fallback_to_generic_supported_template
```

or:

```text
omit unsupported narrative
```

Status:

```text
GOLDEN_GUARDRAIL
```

---

# 66. NE-GD-0060 — CUSTOMER VS EXPERT

Customer Mode:

show:

- summary;
- domain findings;
- recommendation;
- short basis.

Expert Mode:

may show:

```text
pair
energy
tier
interaction_id
modifier
position
control_rule
narrative_id
```

Customer Mode MUST NOT require
technical IDs to understand result.

Status:

```text
GOLDEN_PRESENTATION
```

---

# 67. NE-GD-0061 — SAME NUMBER, DIFFERENT PROFILE

Same numeric sequence:

```text
PHONE
```

and:

```text
CAR_PLATE
```

Expected:

Intrinsic truth identical:

```text
pairs
energies
strengths
interactions
modifier
control
chain
terminal
```

But customer narrative weighting differs.

Canonical:

```text
SAME_ENGINE
DIFFERENT_PROFILE
```

Status:

```text
GOLDEN_ARCHITECTURE
```

---

# 68. NE-GD-0062 — OWNER COMPATIBILITY SEPARATION

Intrinsic Number Analysis MUST NOT
change because owner changes.

Expected:

```text
NUMBER_STRUCTURE = SAME
```

Future owner layer may add:

```text
PERSONAL_SUITABILITY
```

but cannot rewrite intrinsic truth.

Status:

```text
GOLDEN_ARCHITECTURE
```

---

# 69. NE-GD-0063 — ZERO NOT REMOVED BY NORMALIZER

Input contains semantic:

```text
0
```

Normalizer MUST preserve it.

Examples:

```text
103
130
108
```

MUST remain exact digit order.

Status:

```text
GOLDEN_INPUT
```

---

# 70. NE-GD-0064 — FIVE NOT REMOVED

Input:

```text
153
159
135
```

5 MUST remain
and be routed to Modifier Engine.

Status:

```text
GOLDEN_INPUT
```

---

# 71. NE-GD-0065 — FORMATTED PHONE

Example input:

```text
0912 345 678
```

Normalization:

```text
0912345678
```

Formatting removed.

Digits preserved.

Leading semantic zero handling
must follow Product Input Contract.

No digit reordering.

Status:

```text
GOLDEN_INPUT
```

---

# 72. NE-GD-0066 — FORMATTED VEHICLE PLATE

Example:

```text
30A-123.45
```

Numeric sequence for Number Energy:

```text
3012345
```

ONLY if Product Input Standard
defines province/series digits
as included numeric structure.

Letters:

```text
A
```

MUST NOT be interpreted
as Number Energy digit.

Important:

Final normalization policy
must be explicit in Product Input Standard.

Status:

```text
GOLDEN_INPUT_POLICY
```

---

# 73. PLATE NORMALIZATION WARNING

Before production freeze,
team MUST decide:

```text
FULL_PLATE_NUMERIC_MODE
```

or:

```text
SERIAL_ONLY_MODE
```

for vehicle plates.

This is a Product Decision,
not a mystical knowledge rule.

Until decision frozen:

```text
DO NOT GUESS
```

---

# 74. NE-GD-0067 — ORDER PRESERVATION

Input:

```text
813
```

Runtime MUST preserve:

```text
8 → 1 → 3
```

Forbidden:

```text
sort digits
```

Forbidden:

```text
normalize reverse pairs
```

Status:

```text
GOLDEN_INVARIANT
```

---

# 75. NE-GD-0068 — OVERLAPPING PAIR PRESERVATION

Input:

```text
813
```

Pairs:

```text
81
13
```

Digit `1` participates in both.

Runtime MUST preserve overlap.

Forbidden:

```text
81
then skip 1
```

Status:

```text
GOLDEN_INVARIANT
```

---

# 76. NE-GD-0069 — FULL CHAIN CONTINUATION

Input:

```text
81396
```

Runtime MUST build all:

```text
81
13
39
96
```

and all interactions.

Forbidden:

```text
stop after first triple
```

Status:

```text
GOLDEN_INVARIANT
```

---

# 77. NE-GD-0070 — STRENGTH CLASSIFICATION

Expected:

```text
13 = TIAN_Y_T1
68 = TIAN_Y_T2
49 = TIAN_Y_T3
27 = TIAN_Y_T4
```

Reverse pairs same tier:

```text
31 = T1
86 = T2
94 = T3
72 = T4
```

Status:

```text
GOLDEN_STRENGTH
```

---

# 78. NE-GD-0071 — SINH KHÍ STRENGTH

Expected:

```text
14/41 = T1
67/76 = T2
39/93 = T3
28/82 = T4
```

Status:

```text
GOLDEN_STRENGTH
```

---

# 79. NE-GD-0072 — DIÊN NIÊN STRENGTH

Expected:

```text
19/91 = T1
78/87 = T2
34/43 = T3
26/62 = T4
```

Status:

```text
GOLDEN_STRENGTH
```

---

# 80. NE-GD-0073 — HỌA HẠI STRENGTH

Expected:

```text
17/71 = T1
89/98 = T2
46/64 = T3
23/32 = T4
```

Status:

```text
GOLDEN_STRENGTH
```

---

# 81. NE-GD-0074 — NGŨ QUỶ STRENGTH

Expected:

```text
18/81 = T1
79/97 = T2
36/63 = T3
24/42 = T4
```

Status:

```text
GOLDEN_STRENGTH
```

---

# 82. NE-GD-0075 — LỤC SÁT STRENGTH

Expected:

```text
16/61 = T1
47/74 = T2
38/83 = T3
29/92 = T4
```

Status:

```text
GOLDEN_STRENGTH
```

---

# 83. NE-GD-0076 — TUYỆT MỆNH STRENGTH

Expected:

```text
12/21 = T1
69/96 = T2
48/84 = T3
37/73 = T4
```

Status:

```text
GOLDEN_STRENGTH
```

---

# 84. NE-GD-0077 — PHỤC VỊ STRENGTH

Expected:

```text
11/22 = T1
88/99 = T2
66/77 = T3
33/44 = T4
```

Important:

Strength measures continuation intensity,
not positivity.

Status:

```text
GOLDEN_STRENGTH
```

---

# 85. NE-GD-0078 — ALL 8 ENERGY PAIR SETS

Engine MUST resolve exactly:

## Sinh Khí

```text
14 41
67 76
39 93
28 82
```

## Thiên Y

```text
13 31
68 86
49 94
27 72
```

## Diên Niên

```text
19 91
78 87
34 43
26 62
```

## Phục Vị

```text
11 22 33 44
66 77 88 99
```

## Họa Hại

```text
17 71
89 98
46 64
23 32
```

## Ngũ Quỷ

```text
18 81
79 97
36 63
24 42
```

## Lục Sát

```text
16 61
47 74
38 83
29 92
```

## Tuyệt Mệnh

```text
12 21
69 96
48 84
37 73
```

Any mismatch:

```text
FAIL
```

---

# 86. NE-GD-0079 — 64 DIRECTED INTERACTIONS EXIST

Catalog MUST contain:

```text
8 × 8 = 64
```

directed interaction records.

No missing combination.

No automatic reverse merge.

Status:

```text
GOLDEN_CATALOG
```

---

# 87. NE-GD-0080 — DIRECTED INTERACTION UNIQUENESS

Each pair:

```text
SOURCE_ENERGY
TARGET_ENERGY
```

must map to exactly one
canonical interaction identity.

Example:

```text
WU_GUI → TIAN_Y
=
INT-WG-TY
```

No duplicate conflicting records.

Status:

```text
GOLDEN_CATALOG
```

---

# 88. GOLDEN DOMAIN COVERAGE

Golden Dataset MUST cover:

```text
GENERAL
WEALTH
CAREER
RELATIONSHIP
PERSONALITY
SOCIAL
INVESTMENT
LEARNING
WELLNESS_REFERENCE
BALANCE
STABILITY
ACTION
```

before production freeze.

---

# 89. GOLDEN MODIFIER COVERAGE

Must cover:

```text
A0B
AB0
0AB

A5B
AB5
5AB
```

Minimum one validated case each
before production release.

---

# 90. GOLDEN CONTROL COVERAGE

Must cover:

```text
WU_GUI → SHENG_QI
JUE_MING → TIAN_Y
LIU_SHA → YAN_NIAN
HUO_HAI composite
FU_WEI → SHENG_QI
FU_WEI → TIAN_Y
WU_GUI strong remedy chain
```

Both:

```text
positive match
negative/reversed match
```

must be tested.

---

# 91. GOLDEN POSITION COVERAGE

Must include:

```text
HEAD
MIDDLE
REAR
TAIL
TERMINAL
```

and:

```text
challenging middle
challenging tail
auspicious tail
hidden tail
amplified tail
extended tail
```

---

# 92. GOLDEN CHAIN COVERAGE

Must include:

```text
single interaction
two interactions
three+ interactions
repetition
control
reappearing challenge
modifier
mixed structure
```

---

# 93. GOLDEN NARRATIVE COVERAGE

Every production Narrative Key
must have at least one test
that proves:

1. applicability;
2. placeholder binding;
3. no forbidden language;
4. correct profile;
5. no duplicate content.

---

# 94. ACCEPTANCE — KNOWLEDGE TRUTH

PASS only if:

```text
pair mapping = canonical
strength = canonical
direction = preserved
modifier = preserved
position = preserved
control = preserved
chain = preserved
```

---

# 95. ACCEPTANCE — CUSTOMER CONTENT

PASS only if:

- supported by Knowledge;
- clear Vietnamese;
- no invented rule;
- no deterministic fate;
- no medical diagnosis;
- no guaranteed finance;
- no relationship accusation;
- no fear-based wording;
- no excessive repetition.

---

# 96. ACCEPTANCE — PHONE PROFILE

PASS only if:

- full sequence analyzed;
- no last-four-only shortcut;
- wealth/career/relationship differentiated;
- terminal shown;
- modifier shown semantically;
- recommendation based on whole structure.

---

# 97. ACCEPTANCE — VEHICLE PROFILE

PASS only if:

- same intrinsic engine;
- vehicle-specific narrative;
- relationship reduced;
- stability/action/balance increased;
- no accident prediction;
- terminal preserved.

---

# 98. ACCEPTANCE — EXPERT TRACE

For every Customer Finding,
Expert Mode MUST be able to identify:

```text
evidence pair
energy
strength
interaction
modifier
position
control
domain
narrative_id
```

No customer conclusion
without traceable evidence.

---

# 99. ACCEPTANCE — DETERMINISM

Same:

```text
input
profile
knowledge_version
```

must produce same:

```text
truth result
```

Narrative punctuation may vary only
if Presentation Layer explicitly allows it.

Knowledge result must not drift.

---

# 100. ACCEPTANCE — VERSION PINNING

Every result SHOULD contain:

```text
knowledge_version
engine_version
narrative_version
```

Example:

```text
knowledge_version:
NUMBER_ENERGY_KNOWLEDGE_V1.0

narrative_version:
NUMBER_ENERGY_NARRATIVE_V1.0
```

---

# 101. ACCEPTANCE — NO LLM RERANK

LLM MUST NOT:

- change Energy;
- change Strength;
- change interaction;
- change control;
- change domain priority;
- invent findings.

LLM may only:

```text
bind
compose
deduplicate
smooth approved wording
```

---

# 102. ACCEPTANCE — SOURCE CLAIM ISOLATION

Sensitive source claims such as:

- cancer;
- death;
- accident;
- infertility;
- guaranteed divorce;
- fraud character;

MUST remain isolated from Customer Narrative.

Test must fail if any such deterministic
claim leaks into Customer Mode.

---

# 103. ACCEPTANCE — NO CÁT/HUNG COUNTING ENGINE

Forbidden final algorithm:

```text
good_count - bad_count
=
final_result
```

Golden tests must detect
if reverse-order cases
produce identical result
only because counts match.

Example:

```text
813
318
```

must not have identical semantics.

---

# 104. ACCEPTANCE — PHỤC VỊ CONTEXT

Tests must confirm:

```text
SHENG_QI → FU_WEI
```

is treated differently from:

```text
WU_GUI → FU_WEI
```

Same Phục Vị,
different state extended.

---

# 105. ACCEPTANCE — ZERO CONTEXT

Tests must confirm:

```text
103
130
```

are related but not identical.

And:

```text
103 != 153
```

Zero and Five cannot be treated alike.

---

# 106. ACCEPTANCE — TAIL CONTEXT

Tests must confirm:

```text
HUO_HAI → TIAN_Y
```

and:

```text
TIAN_Y → HUO_HAI
```

produce different terminal convergence.

---

# 107. ACCEPTANCE — CONTROL DIRECTION

Must confirm:

```text
WU_GUI → SHENG_QI
```

matches control.

But:

```text
SHENG_QI → WU_GUI
```

does not.

Similarly:

```text
JUE_MING → TIAN_Y
```

matches.

```text
TIAN_Y → JUE_MING
```

does not.

And:

```text
LIU_SHA → YAN_NIAN
```

matches.

```text
YAN_NIAN → LIU_SHA
```

does not.

---

# 108. ACCEPTANCE — LOCAL / GLOBAL CONTROL

Test:

```text
WU_GUI → SHENG_QI → WU_GUI
```

Expected:

```text
LOCAL_CONTROL = TRUE
GLOBAL_CONTROL = FALSE
```

---

# 109. ACCEPTANCE — TERMINAL MODIFIER

Test:

```text
TIAN_Y → ZERO
```

Expected:

```text
terminal = TIAN_Y_HIDDEN
```

not:

```text
terminal = ZERO
```

as a normal Energy.

---

# 110. ACCEPTANCE — TERMINAL FIVE

Expected:

```text
ENERGY → FIVE
```

becomes:

```text
ENERGY_AMPLIFIED
```

not:

```text
FIVE_ENERGY
```

---

# 111. ACCEPTANCE — NARRATIVE TRACEABILITY

Every Customer paragraph SHOULD have:

```text
source_narrative_ids
```

internally.

Example:

```text
[
  "NAR-WEALTH-WG-TY-001",
  "NAR-BAL-WELL-001"
]
```

---

# 112. ACCEPTANCE — DEDUPLICATION

If multiple Narrative Units
repeat same core sentence,
Composer MUST remove repetition.

Meaning may remain
across different domain angles.

---

# 113. ACCEPTANCE — FALLBACK

If engine has valid truth
but no detailed narrative unit:

Allowed fallback:

> Cấu trúc này có tín hiệu nổi bật ở {domain},
> tuy nhiên dữ liệu hiện tại chưa đủ
> để đưa ra luận giải chi tiết hơn.

Forbidden:

LLM invent interpretation.

---

# 114. ACCEPTANCE — UNKNOWN STATE

If data cannot be resolved:

```text
UNKNOWN
```

is valid.

Do NOT substitute:

```text
GOOD
BAD
```

or guess.

---

# 115. ACCEPTANCE — PROFILE-AGNOSTIC TRUTH

Intrinsic Engine output must remain
the same for:

```text
PHONE
CAR_PLATE
MOTORBIKE_PLATE
```

given identical numeric sequence.

Only:

```text
domain weighting
narrative
recommendation
```

may differ.

---

# 116. ACCEPTANCE — KNOWLEDGE IMMUTABILITY

Production runtime MUST NOT mutate
canonical Knowledge Catalog.

Knowledge is:

```text
READ ONLY
```

---

# 117. ACCEPTANCE — VERSION CHANGE

Any change to:

- pair;
- strength;
- interaction;
- 0/5;
- control;
- position;
- chain;
- domain;
- narrative truth;

requires:

```text
version bump
+
golden snapshot update
+
expert approval
```

---

# 118. MINIMUM AUTOMATED TEST SUITE

Before module PASS:

```text
Pair Mapping Tests
Strength Tests
Modifier Tests
Interaction Tests
Position Tests
Control Tests
Chain Tests
Domain Tests
Narrative Tests
Profile Tests
Safety Tests
Golden Snapshot Tests
```

All required.

---

# 119. TEST NAMING

Recommended:

```text
test_ne_gd_0001_813_wugui_to_tianyi
test_ne_gd_0002_318_tianyi_to_wugui
test_ne_gd_0008_103_hidden_tianyi
test_ne_gd_0009_153_amplified_tianyi
test_ne_control_direction
test_ne_tail_modifier
test_ne_phone_vehicle_profile_separation
```

---

# 120. GOLDEN SNAPSHOT

Recommended snapshot object:

```text
{
  "case_id": "NE-GD-0001",
  "input": "813",

  "pairs": [
    {
      "pair": "81",
      "energy": "WU_GUI",
      "tier": 1
    },
    {
      "pair": "13",
      "energy": "TIAN_Y",
      "tier": 1
    }
  ],

  "chain": [
    "WU_GUI",
    "TIAN_Y"
  ],

  "interactions": [
    "INT-WG-TY"
  ],

  "terminal_state": "TIAN_Y",

  "domains": {
    "WEALTH": "PRIMARY"
  },

  "narrative_keys": [
    "NAR-WEALTH-WG-TY-001"
  ]
}
```

---

# 121. GOLDEN SNAPSHOT RULE

Snapshot stores:

```text
TRUTH
```

not:

```text
rendered HTML
```

UI snapshots belong
to Presentation Tests.

---

# 122. KNOWLEDGE ACCEPTANCE CHECKLIST

Before freezing Knowledge V1:

- [ ] All 8 energies defined.
- [ ] All 64 valid Bagua pairs classified.
- [ ] Strength tiers complete.
- [ ] All 64 directed interactions defined.
- [ ] Zero behavior frozen.
- [ ] Five behavior frozen.
- [ ] Position rules frozen.
- [ ] Tail rules frozen.
- [ ] Control rules frozen.
- [ ] Chain rules frozen.
- [ ] Domain rules frozen.
- [ ] Customer Narrative Catalog frozen.
- [ ] Golden cases passing.

---

# 123. ENGINE ACCEPTANCE CHECKLIST

- [ ] Ordered parsing.
- [ ] Overlapping pairs.
- [ ] Pair Energy.
- [ ] Pair Strength.
- [ ] 0/5 modifier.
- [ ] Directed interactions.
- [ ] Position.
- [ ] Tail.
- [ ] Phục Vị extension.
- [ ] Control/Remedy.
- [ ] Local/global control.
- [ ] Full chain.
- [ ] Domain findings.
- [ ] Profile weighting.
- [ ] Narrative selection.
- [ ] Deduplication.
- [ ] Expert trace.

---

# 124. CUSTOMER ACCEPTANCE CHECKLIST

- [ ] Easy to understand.
- [ ] No raw-engine dump.
- [ ] No repetitive prose.
- [ ] Strength explained naturally.
- [ ] Caution explained calmly.
- [ ] Recommendation actionable.
- [ ] No medical diagnosis.
- [ ] No guaranteed wealth.
- [ ] No guaranteed relationship event.
- [ ] No accident prediction.
- [ ] No unsupported claim.
- [ ] Clear difference between phone and plate.

---

# 125. EXPERT ACCEPTANCE CHECKLIST

Expert Mode must expose:

- [ ] pair truth;
- [ ] energy truth;
- [ ] strength;
- [ ] modifier;
- [ ] interaction;
- [ ] position;
- [ ] tail;
- [ ] control;
- [ ] chain;
- [ ] domain evidence;
- [ ] narrative IDs;
- [ ] knowledge version.

---

# 126. RELEASE BLOCKERS

Production release MUST be blocked if:

```text
pair mapping mismatch
```

or:

```text
directed interaction reversed
```

or:

```text
0/5 treated as normal Du Nien
```

or:

```text
control direction ignored
```

or:

```text
chain truncated
```

or:

```text
unsupported customer claim generated
```

or:

```text
medical / accident deterministic output leaks
```

---

# 127. GOLDEN DATASET FREEZE

After expert approval:

```text
NUMBER_ENERGY_GOLDEN_V1
```

becomes frozen.

Any Golden Case change requires
Knowledge version review.

Implementation MUST adapt to Golden Truth.

Golden Truth MUST NOT adapt
just to make broken implementation pass.

---

# 128. FINAL ACCEPTANCE PRINCIPLE

The system is accepted only when:

```text
KNOWLEDGE
=
ENGINE TRUTH
=
DOMAIN TRUTH
=
CUSTOMER MEANING
```

while:

```text
CUSTOMER WORDING
```

remains clear,
natural,
safe
and commercially useful.

---

# 129. MASTER FREEZE STATEMENT

The following Knowledge Pack forms
the canonical Number Energy V1 knowledge base:

```text
00_NUMBER_ENERGY_MASTER.md
01_BAGUA_DIGIT_MAPPING.md
02_EIGHT_ENERGY_CATALOG.md
03_PAIR_STRENGTH_MATRIX.md
04_DIRECTED_INTERACTION_MATRIX.md
05_ZERO_FIVE_MODIFIERS.md
06_POSITION_AND_TAIL_RULES.md
07_CONTROL_REMEDY_RULES.md
08_CHAIN_INTERPRETATION_RULES.md
09_DOMAIN_INTERPRETATION.md
10_CUSTOMER_NARRATIVE_CATALOG.md
11_ACCEPTANCE_GOLDEN_CASES.md
```

Together they define:

```text
NUMBER_ENERGY_KNOWLEDGE_V1
```

Cursor / runtime / UI / LLM
MUST treat this pack as read-only
canonical truth unless an explicitly approved
version update is made.

---

# 130. STATUS

```text
NUMBER_ENERGY_KNOWLEDGE_V1
DESIGN KNOWLEDGE PACK
READY FOR EXPERT FREEZE
```

Once expert-approved:

```text
STATUS:
FROZEN
```

Next phase:

```text
IMPLEMENTATION CONTRACT
→
BUILD PLAN
→
ENGINE
→
API
→
CUSTOMER UI
→
GOLDEN VALIDATION
```

---

# END OF DOCUMENT
```

Đến đây, bộ **00 → 11 đã tạo thành một Knowledge Pack V1 hoàn chỉnh**. Tôi chưa khuyên giao Cursor code ngay trong cùng một lệnh lớn. Bước kế tiếp nên làm thêm đúng **2 file điều hành build**, không phải kiến thức mới:

`IMPLEMENTATION_CONTRACT.md` — khóa Cursor **được phép làm gì, không được làm gì, model/runtime nào phải tồn tại, pipeline nào phải giữ nguyên**.

`BUILD_PLAN.md` — chia triển khai thành từng bước nhỏ: **B01 Skeleton → B02 Knowledge Catalog → B03 Pair/Strength → B04 Modifier/Interaction → B05 Chain/Control → B06 Domains → B07 Narrative → B08 API → B09 UI → B10 Golden Validation**.

Làm như vậy thì lúc giao Cursor, chúng ta đang giao cho nó **một đặc tả đã khóa**, chứ không giao cho nó nhiệm vụ “tự nghĩ cách xây module Năng lượng số”. Đây chính là cách giảm mạnh sai lệch nội dung mà chúng ta từng gặp ở module luận giải Bát Tự.