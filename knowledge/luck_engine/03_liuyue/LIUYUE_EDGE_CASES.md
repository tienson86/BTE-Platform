# LIUYUE EDGE CASES

Version: 1.0

Status

Stable

Module

03_liuyue

---

# 1. Purpose

This document defines every exceptional scenario that may occur during Monthly
Luck (LiuYue) calculation.

Every implementation SHALL follow these rules exactly.

No implementation may introduce undocumented behaviors.

---

# 2. Edge Case Categories

The LiuYue Module classifies edge cases into the following categories.

A.

Solar Term Boundary

B.

Monthly Pillar

C.

Hidden Stems

D.

Stem Relations

E.

Branch Relations

F.

Seasonal Influence

G.

LiuNian Interaction

H.

Dayun Interaction

I.

Transformation

J.

Priority Resolution

K.

Validation

---

# 3. Solar Term Boundary Cases

## 3.1 Before Major Solar Term

If the Gregorian timestamp is earlier than the current Major Solar Term

↓

Use the previous Solar Month.

The Lunar Calendar SHALL NOT be referenced.

---

## 3.2 Exactly At Major Solar Term

If the timestamp equals the exact Solar Term

↓

The new Solar Month begins immediately.

No ambiguity is permitted.

---

## 3.3 After Major Solar Term

The new Monthly Pillar SHALL be used.

---

## 3.4 Missing Solar Term Data

If the Solar Term Calendar cannot determine the current Solar Month

Return

LIUYUE_001

SOLAR_TERM_NOT_FOUND

Stop processing.

No fallback calculation is permitted.

---

## 3.5 Invalid Solar Month

If a month outside the twelve Earthly Branches is generated

Return

INVALID_SOLAR_MONTH

---

# 4. Monthly Pillar Cases

## 4.1 Invalid Heavenly Stem

Return

INVALID_MONTHLY_STEM

---

## 4.2 Invalid Earthly Branch

Return

INVALID_MONTHLY_BRANCH

---

## 4.3 Invalid Stem-Branch Pair

If the generated Monthly Pillar is not part of the Sexagenary Cycle

Return

INVALID_MONTHLY_PILLAR

---

## 4.4 Duplicate Monthly Pillar

Duplicate Monthly Pillars within the same Solar Month are prohibited.

---

# 5. Hidden Stem Cases

## 5.1 Missing Hidden Stem

Every Monthly Branch SHALL contain Hidden Stems.

Otherwise

Return

DATABASE_ERROR

---

## 5.2 Invalid Hidden Stem Order

The ordering SHALL follow the official Hidden Stem Database.

---

## 5.3 Duplicate Hidden Stem

Duplicate Hidden Stems are prohibited.

Validation SHALL fail.

---

# 6. Stem Relation Cases

## 6.1 Multiple Stem Combinations

Several Heavenly Stem combinations may occur simultaneously.

All combinations SHALL be stored.

---

## 6.2 Combination and Control

If Combination

AND

Control

occur together

↓

Store both.

Priority resolution occurs later.

---

## 6.3 Failed Transformation

If Combination exists

BUT

Transformation conditions are incomplete

↓

Transformation = FALSE

Combination remains valid.

---

## 6.4 Competing Transformations

Two transformations SHALL NOT consume the same Heavenly Stem.

Priority Engine resolves the conflict.

---

# 7. Branch Relation Cases

## 7.1 Multiple Branch Clashes

One Monthly Branch may clash with multiple Natal Branches.

All clashes SHALL be preserved.

---

## 7.2 Harmony and Clash Together

Harmony

+

Clash

shall coexist.

Neither interaction removes the other.

---

## 7.3 Partial Three Harmony

If one required Branch is missing

↓

Store

Three Harmony Candidate

Transformation SHALL NOT occur.

---

## 7.4 Partial Three Meetings

Store

Meeting Candidate

No transformation.

---

## 7.5 Self Punishment

Store independently.

Do not merge with Punishment.

---

## 7.6 Harm and Clash

Both interactions remain valid.

---

## 7.7 Destruction and Combination

Both SHALL coexist.

---

# 8. Seasonal Influence Cases

## 8.1 Season Transition

If the month changes exactly at a Solar Term

↓

Seasonal Context updates immediately.

---

## 8.2 Temperature Conflict

If multiple seasonal rules conflict

↓

Apply Priority Rules.

Do not discard lower-priority rules.

---

## 8.3 Undefined Seasonal Context

Return

INVALID_SEASON_CONTEXT

---

## 8.4 Weak Seasonal Influence

Store

Low Seasonal Influence

No error generated.

---

# 9. LiuNian Interaction Cases

## 9.1 Monthly Combination with Annual Stem

Store

Monthly–Annual Combination

---

## 9.2 Monthly Clash with Annual Branch

Store

Monthly–Annual Clash

---

## 9.3 Multiple Annual Interactions

All detected interactions SHALL coexist.

---

## 9.4 Annual Transformation Conflict

Resolved only by Priority Engine.

---

# 10. Dayun Interaction Cases

## 10.1 Monthly Combination with Dayun

Store independently.

---

## 10.2 Monthly Clash with Dayun

Store independently.

---

## 10.3 Triple Interaction

If

Monthly

↓

LiuNian

↓

Dayun

all interact simultaneously

↓

Store every interaction separately.

No interaction may overwrite another.

---

## 10.4 Dayun Transition Month

If Dayun changes during the current Solar Month

↓

Evaluate

Old Dayun

AND

New Dayun

Generate

Transition Context

---

# 11. Transformation Cases

## 11.1 Successful Transformation

Requires

Combination

Season Support

Element Support

Rule Satisfaction

Only then

Transformation = TRUE

---

## 11.2 Failed Transformation

Any missing prerequisite

↓

Transformation = FALSE

---

## 11.3 Broken Transformation

If one required participant disappears

↓

Transformation immediately ends.

---

## 11.4 Multiple Transformations

Store every candidate.

Priority Engine resolves.

---

# 12. Useful God Cases

Useful God strengthened

↓

Positive Flag

---

Useful God weakened

↓

Warning Flag

---

Useful God transformed

↓

Transformation Flag

---

# 13. Unfavorable God Cases

Unfavorable God strengthened

↓

Risk Flag

---

Unfavorable God weakened

↓

Opportunity Flag

---

# 14. Priority Resolution Cases

If

Harmony

Clash

Transformation

Punishment

Harm

Destruction

occur simultaneously

↓

Store ALL.

Priority Engine determines significance.

No event may be deleted.

---

# 15. Metadata Cases

Every detected edge case SHALL contain

Case ID

Timestamp

Processing Stage

Severity

Affected Components

Resolution Status

---

# 16. Validation Cases

Reject processing when

Missing Natal Chart

Missing Current LiuNian

Missing Current Dayun

Missing Solar Term Calendar

Missing Rule Database

Missing Priority Rules

Return structured error.

---

# 17. Error Codes

LIUYUE_001

SOLAR_TERM_NOT_FOUND

LIUYUE_002

INVALID_MONTHLY_STEM

LIUYUE_003

INVALID_MONTHLY_BRANCH

LIUYUE_004

INVALID_MONTHLY_PILLAR

LIUYUE_005

MISSING_HIDDEN_STEM

LIUYUE_006

INVALID_TRANSFORMATION

LIUYUE_007

DAYUN_CONTEXT_NOT_FOUND

LIUYUE_008

LIUNIAN_CONTEXT_NOT_FOUND

LIUYUE_009

INVALID_PRIORITY

LIUYUE_010

INVALID_MONTHLY_CONTEXT

LIUYUE_011

OUTPUT_VALIDATION_FAILED

LIUYUE_012

INVALID_SEASON_CONTEXT

---

# 18. Deterministic Guarantee

The same

Natal Chart

Current Dayun

Current LiuNian

Gregorian Date

Solar Term Calendar

Rule Database

Priority Rules

shall always produce an identical Monthly Context.

Random behavior is prohibited.

AI-generated decisions are prohibited.

---

# 19. Future Reserved Edge Cases

Reserved for

• LiuRi Integration

• LiuShi Integration

• Cross-Month Timeline

• Continuous Fortune Engine

• Event Prediction Engine

• Unified Fortune Timeline

End of Document