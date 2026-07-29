# LIUSHI SPECIFICATION

Version

1.0

Status

Stable

Module

05_liushi

---

# 1. Purpose

The LiuShi Module is responsible for generating and evaluating Hourly Luck (流时)
within the BTE Platform.

A LiuShi represents the energetic influence of one Sexagenary Hour (干支时) on an
individual's BaZi chart.

The module evaluates interactions between the Hourly Pillar and

- Natal Chart
- Current Dayun
- Current LiuNian
- Current LiuYue
- Current LiuRi
- Hidden Heavenly Stems
- Ten Gods
- Five Elements
- Seasonal Context
- Daily Context
- Rule Database
- Priority Rules

The output is a normalized Hourly Context.

---

# 2. Design Goals

The module SHALL

- Produce deterministic results.
- Be completely rule-based.
- Produce immutable outputs.
- Be independent from AI.
- Be independent from Report Engine.
- Be independent from UI.
- Support Unified Fortune Timeline Engine.
- Support future Event Timeline Engine.

---

# 3. Scope

Included

✓ Hourly Heavenly Stem

✓ Hourly Earthly Branch

✓ Hidden Heavenly Stems

✓ Ten Gods

✓ Five Element Mapping

✓ Stem Relations

✓ Branch Relations

✓ Hidden Stem Relations

✓ Natal Chart Interaction

✓ Dayun Interaction

✓ LiuNian Interaction

✓ LiuYue Interaction

✓ LiuRi Interaction

✓ Transformation Rules

✓ Priority Events

✓ Hourly Context

Excluded

✗ Minute-level calculation

✗ AI Interpretation

✗ Natural Language Rendering

✗ Report Formatting

✗ Event Prediction

---

# 4. Responsibilities

The LiuShi Module SHALL

1.

Determine Hour Branch

2.

Generate Hourly Stem

3.

Generate Hourly Pillar

4.

Generate Hidden Stems

5.

Calculate Ten Gods

6.

Evaluate Five Elements

7.

Evaluate Stem Relations

8.

Evaluate Branch Relations

9.

Compare against Natal Chart

10.

Compare against Dayun

11.

Compare against LiuNian

12.

Compare against LiuYue

13.

Compare against LiuRi

14.

Apply Priority Rules

15.

Generate Hourly Context

---

# 5. Inputs

The module requires

Natal Chart

Current Dayun Context

Current LiuNian Context

Current LiuYue Context

Current LiuRi Context

Gregorian DateTime

Calendar Engine Output

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

Current DateTime

contains

Gregorian Date

Gregorian Time

Timezone

Julian Day Number

Sexagenary Day

Sexagenary Hour

Hour Branch

Hour Stem

---

Current Dayun

contains

Current Dayun Pillar

Current Dayun Context

---

Current LiuNian

contains

Annual Pillar

Annual Context

---

Current LiuYue

contains

Monthly Pillar

Monthly Context

---

Current LiuRi

contains

Daily Pillar

Daily Context

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

HourlyContext

Containing

Hourly Pillar

Hidden Stems

Ten Gods

Five Elements

Interactions

Priority Events

Risk Flags

Metadata

---

# 8. Output Structure

HourlyContext

├── Hourly Pillar

├── Hidden Stems

├── Stem Relations

├── Branch Relations

├── Hidden Stem Relations

├── Ten Gods

├── Five Elements

├── Seasonal Context

├── Daily Context

├── LiuYue Relations

├── LiuNian Relations

├── Dayun Relations

├── Natal Relations

├── Combination Result

├── Clash Result

├── Transformation Result

├── Priority Events

├── Risk Flags

└── Metadata

---

# 9. Hour Branch Determination

The Hour Branch SHALL be determined exclusively by the Calendar Engine.

The LiuShi Module SHALL NOT calculate Hour Branch independently.

The Calendar Engine SHALL provide

- Hour Branch
- Hour Index
- Hour Boundary
- Timezone-adjusted Result

---

# 10. Hour Stem Determination

The Hour Stem SHALL be generated exclusively by the Calendar Engine.

The Hour Stem MUST be derived from

Current Day Stem

↓

Five Rat Escape Rule (五鼠遁)

↓

Hour Branch

The LiuShi Module SHALL NOT recalculate Hour Stem.

---

# 11. Hour Boundary Policy

Hour transitions SHALL follow the configured Hour Boundary Policy.

Supported policies include

Traditional Double-Hour

Timezone-adjusted Double-Hour

Custom Calendar Policy

The Hour Boundary Policy SHALL be supplied by Configuration.

Hard-coded boundaries are prohibited.

---

# 12. Hourly Pillar

The Hourly Pillar SHALL consist of

Hour Stem

+

Hour Branch

The pair SHALL always be validated before processing.

---

# 13. Hidden Stems

Every Hour Branch SHALL expose

Primary Hidden Stem

Secondary Hidden Stem

Tertiary Hidden Stem

Ordering SHALL follow the canonical Hidden Stem Database.

---

# 14. Ten Gods

Ten Gods SHALL be calculated from

Day Master

↓

Hourly Heavenly Stem

↓

Hourly Hidden Stems

Every Hidden Stem SHALL receive an independent Ten God.

---

# 15. Five Element Mapping

Map

Hourly Stem

↓

Element

Hourly Branch

↓

Dominant Element

Hourly Hidden Stems

↓

Elements

Generate

Hourly Element Summary

---

# 16. Seasonal Context

The Seasonal Context SHALL be inherited from the active LiuYue.

No seasonal recalculation is permitted.

The inherited context includes

Season

Solar Qi

Temperature

Humidity

Dryness

Season Strength

---

# 17. Daily Context

The Daily Context SHALL be inherited from the active LiuRi.

The LiuShi Module SHALL NOT regenerate Daily Context.

Daily Context SHALL remain immutable.

---

# 18. Stem Interaction

Evaluate

Generation

Control

Combination

Transformation

Competition

Store every interaction independently.

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

Multiple interactions SHALL coexist.

---

# 20. Hidden Stem Interaction

Evaluate interactions between

Hourly Hidden Stems

and

Natal Hidden Stems

↓

Dayun Hidden Stems

↓

Annual Hidden Stems

↓

Monthly Hidden Stems

↓

Daily Hidden Stems

Store every interaction independently.

---

# 21. Natal Chart Interaction

Evaluate

Hourly Stem

↓

Natal Heavenly Stems

Hourly Branch

↓

Natal Earthly Branches

Hourly Hidden Stems

↓

Natal Hidden Stems

Generate

Natal Interaction Context

---

# 22. Dayun Interaction

Evaluate

Hourly Stem

↓

Dayun Stem

Hourly Branch

↓

Dayun Branch

Hourly Hidden Stems

↓

Dayun Hidden Stems

Generate

Dayun Interaction Context

---

# 23. LiuNian Interaction

Evaluate

Hourly Stem

↓

Annual Stem

Hourly Branch

↓

Annual Branch

Hourly Hidden Stems

↓

Annual Hidden Stems

Generate

Annual Interaction Context

---

# 24. LiuYue Interaction

Evaluate

Hourly Stem

↓

Monthly Stem

Hourly Branch

↓

Monthly Branch

Hourly Hidden Stems

↓

Monthly Hidden Stems

Generate

Monthly Interaction Context

---

# 25. LiuRi Interaction

Evaluate

Hourly Stem

↓

Daily Stem

Hourly Branch

↓

Daily Branch

Hourly Hidden Stems

↓

Daily Hidden Stems

Generate

Daily Interaction Context

---

# 26. Multi-Layer Interaction

The module SHALL simultaneously evaluate

Natal Chart

↓

Dayun

↓

LiuNian

↓

LiuYue

↓

LiuRi

↓

LiuShi

Every interaction layer SHALL remain independent.

No layer may overwrite another.

---

# 27. Combination Resolution

Detect

Stem Combination

Branch Combination

Hidden Stem Combination

Potential Combination

Transformation Candidate

All detected combinations SHALL be preserved.

---

# 28. Transformation Rules

Transformation SHALL occur only if

Combination exists

AND

Seasonal requirements are satisfied

AND

Element requirements are satisfied

AND

Rule Database requirements are satisfied

Otherwise

Transformation = FALSE

---

# 29. Useful God Interaction

Evaluate

Useful God strengthened

Useful God weakened

Useful God transformed

Generate corresponding Positive or Warning Flags.

---

# 30. Unfavorable God Interaction

Evaluate

Unfavorable God strengthened

Unfavorable God weakened

Unfavorable God transformed

Generate corresponding Risk or Opportunity Flags.

---

# 31. Hourly Risk Flags

Generate standardized Risk Flags including

High Risk

Medium Risk

Low Risk

Neutral

Risk Flags SHALL remain descriptive only.

No interpretation SHALL be generated.

---

# 32. Priority Resolution

Load

Priority Database

Resolve

Interaction Priority

Transformation Priority

Risk Priority

Special Rule Priority

Store

Primary Events

Secondary Events

Suppressed Events

No event SHALL be deleted.

---

# 33. Metadata

HourlyContext SHALL contain

Module Version

Generation Timestamp

Calendar Version

Rule Database Version

Priority Version

Processing Duration

Validation Status

Unique Context Identifier

---

# 34. Validation Rules

The module SHALL reject processing if

Natal Chart is missing

Dayun Context is missing

LiuNian Context is missing

LiuYue Context is missing

LiuRi Context is missing

Calendar Engine Output is missing

Rule Database is missing

Priority Rules are missing

---

# 35. Error Handling

Every failure SHALL return

Error Code

Message

Processing Stage

Affected Object

Suggested Resolution

No partial HourlyContext SHALL be returned.

---

# 36. Performance Requirements

Average processing time

< 10 ms

Average complexity

O(n)

Memory usage SHALL remain stable during continuous batch processing.

The module SHALL support high-volume hourly evaluations.

---

# 37. API Contract

The public interface SHALL accept

Input

- NatalChart
- DayunContext
- LiuNianContext
- LiuYueContext
- LiuRiContext
- CalendarContext

Return

HourlyContext

The returned object SHALL be immutable.

---

# 38. Future Extensions

Reserved for

- Unified Fortune Timeline Engine
- Event Timeline Engine
- Continuous Fortune Evaluation
- Timeline Scoring Engine
- Predictive Event Engine

End of Document