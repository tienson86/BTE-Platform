# LIUYUE SPECIFICATION

Version: 1.0

Status: Stable

Module

03_liuyue

---

# 1. Purpose

The LiuYue Module is responsible for generating and evaluating Monthly Luck (流月)
within the BTE Platform.

A LiuYue represents the influence of one Solar Month (节令月) on an individual's
BaZi chart.

The module evaluates interactions between the Monthly Pillar and:

- Natal Chart
- Current Dayun
- Current LiuNian
- Hidden Heavenly Stems
- Ten Gods
- Five Elements
- Seasonal Qi
- Rule Database
- Priority Rules

The output is a normalized Monthly Context.

---

# 2. Design Goals

The module SHALL

- Produce deterministic results.
- Be completely rule-based.
- Produce immutable outputs.
- Avoid AI-generated reasoning.
- Be independent from Report Engine.
- Be independent from UI.
- Support future LiuRi integration.
- Support future LiuShi integration.

---

# 3. Scope

Included

✓ Monthly Heavenly Stem

✓ Monthly Earthly Branch

✓ Hidden Heavenly Stems

✓ Ten Gods

✓ Five Element Mapping

✓ Stem Relations

✓ Branch Relations

✓ Hidden Stem Relations

✓ LiuNian Interaction

✓ Dayun Interaction

✓ Seasonal Influence

✓ Transformation Rules

✓ Priority Events

✓ Monthly Context

Excluded

✗ Daily Luck

✗ Hour Luck

✗ AI Interpretation

✗ Natural Language Rendering

✗ Report Formatting

---

# 4. Responsibilities

The LiuYue Module SHALL

1.
Determine Solar Month

2.
Generate Monthly Pillar

3.
Generate Hidden Stems

4.
Calculate Ten Gods

5.
Evaluate Five Elements

6.
Evaluate Stem Relations

7.
Evaluate Branch Relations

8.
Compare against Natal Chart

9.
Compare against Dayun

10.
Compare against LiuNian

11.
Apply Priority Rules

12.
Generate Monthly Context

---

# 5. Inputs

The module requires

Natal Chart

Current Dayun Context

Current LiuNian Context

Gregorian Date

Solar Term Calendar

Rule Database

Priority Rules

Configuration

---

# 6. Input Objects

NatalChart

contains

Year Pillar

Month Pillar

Day Pillar

Hour Pillar

Hidden Stems

Strength Result

Pattern Result

Useful God

Unfavorable God

---

Current Date

contains

Gregorian Date

Gregorian Time

Timezone

---

Current LiuNian

contains

Annual Pillar

Annual Hidden Stems

Annual Ten Gods

Annual Context

---

Current Dayun

contains

Current Dayun Pillar

Hidden Stems

Current Age

Remaining Years

---

Rule Database

contains

Strength Rules

Season Rules

Combination Rules

Transformation Rules

Priority Rules

---

# 7. Outputs

The module returns

MonthlyContext

Containing

Monthly Pillar

Hidden Stems

Ten Gods

Five Elements

Interactions

Priority Events

Risk Flags

Metadata

---

# 8. Output Structure

MonthlyContext

├── Monthly Pillar

├── Hidden Stems

├── Stem Relations

├── Branch Relations

├── Hidden Stem Relations

├── Ten Gods

├── Five Elements

├── Seasonal Influence

├── LiuNian Relations

├── Dayun Relations

├── Combination Result

├── Clash Result

├── Transformation Result

├── Priority Events

├── Risk Flags

└── Metadata

---

# 9. Monthly Determination

Monthly Pillars SHALL always be determined
using Solar Terms (节气).

The Lunar Calendar SHALL NOT be used.

The Gregorian calendar SHALL only be used
to locate Solar Terms.

---

# 10. Monthly Boundary

Every Monthly Pillar begins at

Major Solar Term

and ends immediately before
the next Major Solar Term.

The boundary SHALL be precise
to the second.

---

# 11. Monthly Sequence

The sequence SHALL follow

Yin Month

↓

Mao Month

↓

Chen Month

↓

Si Month

↓

Wu Month

↓

Wei Month

↓

Shen Month

↓

You Month

↓

Xu Month

↓

Hai Month

↓

Zi Month

↓

Chou Month

---

# 12. Monthly Stem Generation

Monthly Heavenly Stem SHALL be generated from

Current Annual Heavenly Stem

↓

Stem Cycle Rules

↓

Monthly Heavenly Stem

The calculation SHALL follow
the official Five Tiger Dunjia (五虎遁) rules.

---

# 13. Monthly Branch Generation

Monthly Earthly Branch SHALL always follow
the Solar Month sequence.

No alternative sequence is permitted.

---

# 14. Hidden Stems

Each Monthly Branch SHALL expose

Primary Hidden Stem

Secondary Hidden Stem

Tertiary Hidden Stem

The order MUST match the Hidden Stem Database.

---

# 15. Ten Gods

Ten Gods SHALL be calculated from

Day Master

↓

Monthly Heavenly Stem

↓

Monthly Hidden Stems

Each Hidden Stem receives
an independent Ten God.

---

# 16. Five Element Mapping

Map

Monthly Stem

↓

Element

Monthly Branch

↓

Dominant Element

Hidden Stems

↓

Elements

Generate

Monthly Element Summary

---

# 17. Seasonal Influence

Determine

Current Season

Current Solar Qi

Season Strength

Temperature Context

Humidity Context

Dryness Context

The Seasonal Result SHALL become part of
Monthly Context.

---

# 18. Stem Interaction

Evaluate

Generation

Control

Combination

Transformation

Competition

Store every interaction.

No interaction may overwrite another.

---

# 19. Branch Interaction

Evaluate

Six Harmony

Six Clash

Three Harmony

Three Meetings

Punishment

Harm

Destruction

Self Punishment

Transformation

All interactions SHALL coexist.

---

# 20. Hidden Stem Interaction

Evaluate interactions between

Monthly Hidden Stems

and

Natal Hidden Stems

↓

LiuNian Hidden Stems

↓

Dayun Hidden Stems

Store every detected interaction.

```

**Continue...**

---

## Phần tiếp theo của `LIUYUE_SPEC.md`

Trong **Part 2**, chúng ta sẽ hoàn thiện các mục:

- **21. LiuNian Interaction**
- **22. Dayun Interaction**
- **23. Natal Chart Interaction**
- **24. Combination Resolution**
- **25. Transformation Rules**
- **26. Seasonal Strength Evaluation**
- **27. Useful God Interaction**
- **28. Unfavorable God Interaction**
- **29. Monthly Risk Flags**
- **30. Priority Resolution**
- **31. Metadata**
- **32. Validation Rules**
- **33. Error Handling**
- **34. Performance Requirements**
- **35. API Contract**
- **36. Future Extensions**

Hai phần này ghép lại sẽ tạo thành **đặc tả hoàn chỉnh** của module **03_liuyue**, tương đương về mức độ chi tiết với các tài liệu `DAYUN_SPEC.md` và `LIUNIAN_SPEC.md`.