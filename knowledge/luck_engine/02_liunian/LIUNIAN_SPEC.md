# LIUNIAN SPECIFICATION

Version: 1.0

Status: Stable

Module:
02_liunian

---

# 1. Purpose

The LiuNian Module is responsible for generating and evaluating the influence of a
single annual pillar (流年) on a natal BaZi chart.

The module calculates all interactions between the Annual Pillar and:

- Natal Chart
- Dayun (Major Luck Cycle)
- Hidden Heavenly Stems
- Ten Gods
- Five Elements
- Seasonal Strength
- Pattern Rules
- Special Rules
- Priority Rules

The output is a normalized Annual Context that can be consumed by downstream
engines.

---

# 2. Design Goals

The module shall:

- Produce deterministic results.
- Avoid interpretation.
- Avoid natural language generation.
- Preserve reproducibility.
- Remain independent of UI.
- Remain independent of Report Engine.
- Support future LiuYue extension.

---

# 3. Scope

Included

✓ Annual Heavenly Stem

✓ Annual Earthly Branch

✓ Hidden Stems

✓ Ten Gods

✓ Five Element Interaction

✓ Stem Combination

✓ Stem Clash

✓ Branch Combination

✓ Branch Clash

✓ Harm

✓ Punishment

✓ Destruction

✓ Transformation

✓ Fu Yin

✓ Fan Yin

✓ Tai Sui

✓ Kong Wang Detection

✓ Annual Element Distribution

✓ Priority Events

Excluded

✗ Monthly Luck

✗ Daily Luck

✗ Hour Luck

✗ AI Interpretation

✗ Report Formatting

✗ Sentence Generation

---

# 4. Responsibilities

The LiuNian Module is responsible for:

1.
Generate Annual Pillar

2.
Generate Hidden Stems

3.
Generate Ten Gods

4.
Detect interactions with Natal Chart

5.
Detect interactions with Dayun

6.
Detect all combinations

7.
Detect all clashes

8.
Detect transformations

9.
Compute Five Element balance

10.
Build structured Annual Context

---

# 5. Inputs

The module requires:

Birth Chart

Current Gregorian Year

Solar Term Calendar

Dayun Context

Rule Database

Priority Database

Configuration

No external interpretation engine is required.

---

# 6. Input Objects

Required object:

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

CurrentYear

contains

Gregorian Year

Solar Year

Annual Stem

Annual Branch

---

Dayun Context

contains

Current Dayun

Current Dayun Stem

Current Dayun Branch

Remaining Years

Starting Age

Ending Age

---

Rule Database

contains

Strength Rules

Season Rules

Combination Rules

Priority Rules

Transformation Rules

---

# 7. Outputs

The module returns

AnnualContext

The object contains

Annual Pillar

Hidden Stems

Ten Gods

Interactions

Transformations

Priority Events

Element Distribution

Risk Flags

Metadata

---

# 8. Output Structure

AnnualContext

├── Annual Pillar
├── Hidden Stems
├── Stem Relations
├── Branch Relations
├── Ten Gods
├── Five Elements
├── Combination Result
├── Clash Result
├── Transformation Result
├── Tai Sui Result
├── Kong Wang Result
├── Priority Events
├── Metadata

---

# 9. Annual Pillar Generation

The Annual Pillar shall be generated from:

Gregorian Year

↓

Solar Calendar

↓

Solar Terms

↓

Sexagenary Cycle

↓

Annual Heavenly Stem

Annual Earthly Branch

---

The Annual Pillar SHALL begin at:

Li Chun (立春)

NOT Lunar New Year.

---

# 10. Solar Term Rule

If

Birth Date

<

Li Chun

then

Previous Annual Pillar

Else

Current Annual Pillar

---

# 11. Annual Hidden Stems

Each Earthly Branch shall expose all Hidden Heavenly Stems.

Example

Zi

癸

Chou

己

癸

辛

Yin

甲

丙

戊

...

The Hidden Stem order MUST follow the Hidden Stem Database.

---

# 12. Ten Gods Calculation

Ten Gods shall always be calculated from

Day Master

↓

Annual Heavenly Stem

↓

Hidden Stems

Every Hidden Stem receives an independent Ten God.

---

# 13. Five Element Mapping

The module shall map every

Stem

↓

Element

Every

Branch

↓

Dominant Element

Hidden Stem

↓

Element

The output is normalized.

---

# 14. Interaction Detection

Interactions are divided into

Stem Layer

Branch Layer

Hidden Stem Layer

Dayun Layer

Annual Layer

Each layer is independent.

---

# 15. Stem Interaction

Detect

Combination

Control

Generation

Competition

Transformation

Priority

Combination

>

Transformation

>

Control

---

# 16. Branch Interaction

Detect

Six Clash

Six Harmony

Three Harmony

Three Meetings

Punishment

Harm

Destruction

Self Punishment

Transformation

All interactions must be preserved.

No interaction may overwrite another.

---

# 17. Hidden Stem Interaction

Each Hidden Stem interacts independently with

Natal Hidden Stem

Natal Stem

Annual Stem

Dayun Stem

---

# 18. Dayun Interaction

Annual Pillar

↓

Dayun Stem

↓

Dayun Branch

↓

Combined Context

The interaction is preserved separately.

---

# 19. Tai Sui Detection

Detect

Annual Branch

vs

Natal Branches

vs

Dayun Branch

vs

Special Rules

Store

Tai Sui Flags

Tai Sui Severity

Tai Sui Type

---

# 20. Kong Wang

If

Annual Branch

belongs to

Current Kong Wang

Generate

Void Event

Store

Severity

Affected Layers

```
Continue...
```

---

# Phần tiếp theo của `LIUNIAN_SPEC.md`

File này còn khoảng **25–30 mục** nữa mới hoàn chỉnh, bao gồm:

- **21. Fu Yin Detection**
- **22. Fan Yin Detection**
- **23. Combination Priority**
- **24. Clash Priority**
- **25. Transformation Rules**
- **26. Priority Resolution**
- **27. Annual Strength Evaluation**
- **28. Useful God Interaction**
- **29. Unfavorable God Interaction**
- **30. Risk Flag System**
- **31. Metadata**
- **32. Error Handling**
- **33. Validation Rules**
- **34. Performance Requirements**
- **35. API Contract**
- **36. Future Extensions**

Mình khuyến nghị chia thành **Part 2** và **Part 3** để giữ mỗi phần ở kích thước dễ kiểm soát, đồng thời thống nhất với cách chúng ta đã xây dựng các module trước như **DAYUN** và **RULE_DATABASE**.