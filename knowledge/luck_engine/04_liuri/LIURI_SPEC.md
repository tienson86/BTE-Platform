# LIURI SPECIFICATION

Version

1.0

Status

Stable

Module

04_liuri

---

# 1. Purpose

The LiuRi Module is responsible for generating and evaluating Daily Luck (流日)
within the BTE Platform.

A LiuRi represents the energetic influence of one Sexagenary Day (干支日) on an
individual's BaZi chart.

The module evaluates interactions between the Daily Pillar and

- Natal Chart
- Current Dayun
- Current LiuNian
- Current LiuYue
- Hidden Heavenly Stems
- Ten Gods
- Five Elements
- Seasonal Context
- Rule Database
- Priority Rules

The output is a normalized Daily Context.

---

# 2. Design Goals

The module SHALL

- Produce deterministic results.
- Be completely rule-based.
- Produce immutable outputs.
- Be independent from AI.
- Be independent from Report Engine.
- Be independent from UI.
- Support future LiuShi integration.
- Support Unified Fortune Timeline Engine.

---

# 3. Scope

Included

✓ Daily Heavenly Stem

✓ Daily Earthly Branch

✓ Hidden Heavenly Stems

✓ Ten Gods

✓ Five Element Mapping

✓ Stem Relations

✓ Branch Relations

✓ Hidden Stem Relations

✓ LiuYue Interaction

✓ LiuNian Interaction

✓ Dayun Interaction

✓ Natal Chart Interaction

✓ Transformation Rules

✓ Priority Events

✓ Daily Context

Excluded

✗ Hourly Luck

✗ AI Interpretation

✗ Natural Language Rendering

✗ Report Formatting

---

# 4. Responsibilities

The LiuRi Module SHALL

1.

Determine Daily Pillar

2.

Generate Hidden Stems

3.

Calculate Ten Gods

4.

Evaluate Five Elements

5.

Evaluate Stem Relations

6.

Evaluate Branch Relations

7.

Compare against Natal Chart

8.

Compare against Dayun

9.

Compare against LiuNian

10.

Compare against LiuYue

11.

Apply Priority Rules

12.

Generate Daily Context

---

# 5. Inputs

The module requires

Natal Chart

Current Dayun Context

Current LiuNian Context

Current LiuYue Context

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

DailyContext

Containing

Daily Pillar

Hidden Stems

Ten Gods

Five Elements

Interactions

Priority Events

Risk Flags

Metadata

---

# 8. Output Structure

DailyContext

├── Daily Pillar

├── Hidden Stems

├── Stem Relations

├── Branch Relations

├── Hidden Stem Relations

├── Ten Gods

├── Five Elements

├── Seasonal Context

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

# 9. Daily Pillar Determination

The Daily Pillar SHALL be generated exclusively by the Calendar Engine.

The LiuRi Module SHALL NOT calculate the Sexagenary Day independently.

The Calendar Engine SHALL provide

- Julian Day Number
- Sexagenary Day Index
- Heavenly Stem
- Earthly Branch

---

# 10. Day Boundary

The beginning of a new LiuRi SHALL follow the configured Day Boundary Policy.

Supported policies include

Midnight Boundary

or

Zi Hour Boundary

The boundary policy SHALL be supplied by Configuration.

No hard-coded implementation is permitted.

---

# 11. Daily Heavenly Stem

The Daily Heavenly Stem SHALL be obtained directly from the Calendar Engine.

The LiuRi Module SHALL treat the result as immutable.

---

# 12. Daily Earthly Branch

The Daily Earthly Branch SHALL be obtained directly from the Calendar Engine.

No recalculation is permitted.

---

# 13. Hidden Stems

Every Daily Branch SHALL expose

Primary Hidden Stem

Secondary Hidden Stem

Tertiary Hidden Stem

The ordering MUST follow the Hidden Stem Database.

---

# 14. Ten Gods

Ten Gods SHALL be calculated from

Day Master

↓

Daily Heavenly Stem

↓

Daily Hidden Stems

Every Hidden Stem SHALL receive an independent Ten God.

---

# 15. Five Element Mapping

Map

Daily Stem

↓

Element

Daily Branch

↓

Dominant Element

Hidden Stems

↓

Elements

Generate

Daily Element Summary

---

# 16. Seasonal Context

The Seasonal Context SHALL be inherited from the active LiuYue.

The LiuRi Module SHALL NOT recalculate seasonal strength independently.

Seasonal Context includes

Season

Solar Qi

Temperature

Humidity

Dryness

Season Strength

---

# 17. Stem Interaction

Evaluate

Generation

Control

Combination

Transformation

Competition

Every detected interaction SHALL be stored.

No interaction may overwrite another.

---

# 18. Branch Interaction

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

# 19. Hidden Stem Interaction

Evaluate interactions between

Daily Hidden Stems

and

Natal Hidden Stems

↓

Monthly Hidden Stems

↓

Annual Hidden Stems

↓

Dayun Hidden Stems

Store every detected interaction independently.

---

# 20. Natal Chart Interaction

Evaluate

Daily Stem

↓

Natal Heavenly Stems

Daily Branch

↓

Natal Earthly Branches

Daily Hidden Stems

↓

Natal Hidden Stems

Generate

Natal Interaction Context

---

# 21. LiuYue Interaction

Evaluate

Daily Stem

↓

Monthly Stem

Daily Branch

↓

Monthly Branch

Daily Hidden Stems

↓

Monthly Hidden Stems

Store every interaction.

---

# 22. LiuNian Interaction

Evaluate

Daily Stem

↓

Annual Stem

Daily Branch

↓

Annual Branch

Daily Hidden Stems

↓

Annual Hidden Stems

Generate

Annual Interaction Context

---

# 23. Dayun Interaction

Evaluate

Daily Stem

↓

Dayun Stem

Daily Branch

↓

Dayun Branch

Daily Hidden Stems

↓

Dayun Hidden Stems

Generate

Dayun Interaction Context.

---

# 24. Multi-Layer Interaction

The module SHALL support simultaneous evaluation across

Natal Chart

↓

Dayun

↓

LiuNian

↓

LiuYue

↓

LiuRi

Every interaction layer SHALL remain independent.

No layer may overwrite another.

---

# 25. Combination Resolution

Detect

Stem Combination

Branch Combination

Hidden Stem Combination

Potential Combination

Transformation Candidate

All results SHALL be preserved.

---

# 26. Transformation Rules

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

# 27. Useful God Interaction

Evaluate

Useful God strengthened

Useful God weakened

Useful God transformed

Generate corresponding Positive or Warning Flags.

---

# 28. Unfavorable God Interaction

Evaluate

Unfavorable God strengthened

Unfavorable God weakened

Unfavorable God transformed

Generate corresponding Risk or Opportunity Flags.

---

# 29. Daily Risk Flags

Generate standardized Risk Flags including

High Risk

Medium Risk

Low Risk

Neutral

Risk Flags SHALL remain descriptive only.

No interpretation SHALL be generated.

---

# 30. Priority Resolution

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

# 31. Metadata

DailyContext SHALL contain

Module Version

Generation Timestamp

Calendar Version

Rule Database Version

Priority Version

Processing Duration

Validation Status

Unique Context Identifier

---

# 32. Validation Rules

The module SHALL reject processing if

Natal Chart is missing

Dayun Context is missing

LiuNian Context is missing

LiuYue Context is missing

Calendar Engine Output is missing

Rule Database is missing

Priority Rules are missing

---

# 33. Error Handling

Every failure SHALL return

Error Code

Message

Processing Stage

Affected Object

Suggested Resolution

No partial DailyContext SHALL be returned.

---

# 34. Performance Requirements

Average processing time

< 10 ms

Average complexity

O(n)

Memory usage SHALL remain stable during continuous batch processing.

---

# 35. API Contract

The public interface SHALL accept

Input

- NatalChart
- DayunContext
- LiuNianContext
- LiuYueContext
- CalendarContext

Return

DailyContext

The returned object SHALL be immutable.

---

# 36. Future Extensions

Reserved for

- LiuShi Integration
- Unified Fortune Timeline Engine
- Cross-Day Event Engine
- Continuous Fortune Evaluation
- Predictive Timeline Engine

End of Document