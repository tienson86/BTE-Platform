# LIUNIAN EDGE CASES

Version: 1.0

Status: Stable

Module:
02_liunian

---

# 1. Purpose

This document defines all exceptional scenarios that may occur during
Annual Luck (LiuNian) calculation.

Every implementation SHALL follow these rules.

No implementation may invent additional behaviors.

---

# 2. Classification

Edge Cases are classified into

A.
Calendar

B.
Dayun Transition

C.
Annual Pillar

D.
Stem Relations

E.
Branch Relations

F.
Transformation

G.
Special Stars

H.
Priority Resolution

I.
Validation

---

# 3. Calendar Edge Cases

## 3.1 Before Li Chun

Condition

Gregorian Date

<

Li Chun

Result

Use previous Solar Year.

Example

2026-02-02

↓

Still belongs to

Yi Si Year

NOT

Bing Wu Year.

---

## 3.2 Exactly At Li Chun

When timestamp equals Li Chun.

Rule

Use the new Solar Year immediately.

No ambiguity is allowed.

---

## 3.3 Missing Solar Term

If Solar Term data cannot be loaded

Return

SOLAR_TERM_NOT_FOUND

Stop processing.

No fallback algorithm is allowed.

---

## 3.4 Leap Year

Gregorian leap years SHALL NOT affect
Sexagenary Year generation.

Only Solar Terms determine Annual Pillar.

---

# 4. Dayun Transition Cases

## 4.1 Normal Year

Annual Luck is evaluated inside the current Dayun.

No special handling.

---

## 4.2 Dayun Transition Year

When Dayun changes during the year

Evaluate

Old Dayun

AND

New Dayun

The output SHALL contain

Transition Context.

---

## 4.3 Transition Before Li Chun

If Dayun begins before Li Chun

Old Dayun remains valid
until transition time.

---

## 4.4 Transition After Li Chun

Annual Pillar remains unchanged.

Only Dayun Context changes.

---

## 4.5 Exact Transition Time

If exact transition timestamp exists

Use timestamp.

Otherwise

Return

DAYUN_TIME_UNKNOWN

---

# 5. Annual Pillar Edge Cases

## 5.1 Invalid Annual Pillar

If generated pillar does not exist
inside Sexagenary Cycle

Return

INVALID_ANNUAL_PILLAR

---

## 5.2 Invalid Heavenly Stem

Return

INVALID_STEM

---

## 5.3 Invalid Earthly Branch

Return

INVALID_BRANCH

---

# 6. Hidden Stem Edge Cases

## 6.1 Missing Hidden Stem

Every Branch SHALL have
Hidden Stems.

Otherwise

DATABASE_ERROR

---

## 6.2 Duplicate Hidden Stem

Duplicates are prohibited.

Validation SHALL fail.

---

## 6.3 Invalid Hidden Stem Order

Canonical order MUST follow
Hidden Stem Database.

---

# 7. Stem Interaction Cases

## 7.1 Multiple Stem Combination

Several combinations may exist simultaneously.

Store all.

Never overwrite.

---

## 7.2 Combination And Clash

If

Combination

AND

Control

exist together

Store both.

Priority Engine resolves later.

---

## 7.3 Transformation Failure

Combination exists

↓

Transformation requirements not met

↓

Transformation = FALSE

Combination remains.

---

# 8. Branch Interaction Cases

## 8.1 Multiple Clash

Annual Branch may clash
multiple Natal Branches.

Store every clash.

---

## 8.2 Harmony And Clash

Harmony

+

Clash

Both remain valid.

Priority Engine decides significance.

---

## 8.3 Triple Harmony Interrupted

Three Harmony missing one Branch

↓

No transformation.

Store as Partial Harmony.

---

## 8.4 Partial Meeting

Store

Meeting Candidate

No transformation.

---

## 8.5 Self Punishment

Store separately.

Do not merge with Punishment.

---

## 8.6 Harm + Clash

Both interactions SHALL coexist.

---

## 8.7 Destruction + Combination

Store both.

---

# 9. Transformation Cases

## 9.1 Stem Transformation

Transformation only occurs when

Combination

+

Seasonal Support

+

Element Support

are satisfied.

---

## 9.2 Branch Transformation

Requires all mandatory Branches.

Otherwise

Transformation fails.

---

## 9.3 Competing Transformations

Two transformations
cannot consume the same Branch.

Priority Engine resolves.

---

## 9.4 Broken Transformation

If one required Branch disappears

Transformation immediately fails.

---

# 10. Fu Yin

Condition

Same Stem

Same Branch

Store

Fu Yin Event

Severity

High

---

# 11. Fan Yin

Condition

Complete opposition

Store

Fan Yin Event

Severity

High

---

# 12. Tai Sui

Annual Branch equals

Natal Branch

or

Dayun Branch

Generate

Tai Sui Flag.

Do not interpret.

---

# 13. Kong Wang

If Annual Branch enters Void

Store

Void Flag

Affected Components

Severity

---

# 14. Shen Sha Cases

Every Shen Sha

is evaluated independently.

Examples

Peach Blossom

Travel Horse

Heavenly Virtue

Monthly Virtue

Academic Star

Nobleman

General Star

All remain independent.

---

# 15. Element Balance Cases

If every Element count is zero

Return

INVALID_ELEMENT_RESULT

---

If dominant Element cannot be determined

Store

Balanced Elements.

---

# 16. Useful God Cases

Useful God appears

↓

Generate Positive Flag.

Useful God attacked

↓

Generate Warning Flag.

Useful God transformed

↓

Generate Transformation Flag.

---

# 17. Unfavorable God Cases

Unfavorable God strengthened

↓

Risk Flag.

Unfavorable God weakened

↓

Opportunity Flag.

---

# 18. Priority Conflicts

If

Harmony

Clash

Transformation

Punishment

exist simultaneously

Store ALL.

No rule may delete another rule.

Priority Engine resolves significance.

---

# 19. Metadata Cases

Every Edge Case SHALL include

Case ID

Timestamp

Processing Stage

Severity

Affected Objects

Resolution Status

---

# 20. Validation Cases

Reject when

Missing Natal Chart

Missing Day Master

Missing Calendar

Missing Dayun

Missing Rule Database

Missing Priority Rules

Return structured error.

---

# 21. Error Codes

LIUNIAN_001

INVALID_YEAR

LIUNIAN_002

INVALID_STEM

LIUNIAN_003

INVALID_BRANCH

LIUNIAN_004

MISSING_HIDDEN_STEM

LIUNIAN_005

INVALID_TRANSFORMATION

LIUNIAN_006

DAYUN_NOT_FOUND

LIUNIAN_007

SOLAR_TERM_NOT_FOUND

LIUNIAN_008

INVALID_PRIORITY

LIUNIAN_009

INVALID_CONTEXT

LIUNIAN_010

OUTPUT_VALIDATION_FAILED

---

# 22. Deterministic Guarantee

The same

Natal Chart

Dayun

Gregorian Year

Solar Term Data

Rule Database

Priority Database

shall always produce an identical Annual Context.

No randomness.

No heuristic estimation.

No AI-generated decision.

---

# 23. Future Reserved Edge Cases

Reserved for

• LiuYue Integration

• LiuRi Integration

• LiuShi Integration

• Dynamic Fortune Timeline

• Cross-Year Interaction Engine

• Predictive Event Engine

End of Document