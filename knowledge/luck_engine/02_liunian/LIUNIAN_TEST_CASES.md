# LIUNIAN TEST CASES

Version: 1.0

Status: Stable

Module:
02_liunian

---

# 1. Purpose

This document defines the official test cases for validating the LiuNian Module.

Every implementation SHALL pass all mandatory test cases before being considered compliant.

The test suite validates:

- Calendar calculations
- Annual Pillar generation
- Hidden Stem expansion
- Ten Gods calculation
- Five Element mapping
- Stem interactions
- Branch interactions
- Dayun interactions
- Special rules
- Priority resolution
- Error handling
- Output validation

---

# 2. Test Categories

| Category | Description |
|----------|-------------|
| TC001–TC010 | Calendar |
| TC011–TC020 | Annual Pillar |
| TC021–TC035 | Hidden Stems |
| TC036–TC050 | Ten Gods |
| TC051–TC065 | Five Elements |
| TC066–TC085 | Stem Relations |
| TC086–TC110 | Branch Relations |
| TC111–TC125 | Dayun Relations |
| TC126–TC140 | Special Rules |
| TC141–TC150 | Validation |

---

# 3. Test Case Template

Each test SHALL contain:

Test ID

Purpose

Input

Expected Output

Assertions

Priority

---

# 4. Calendar Test Cases

## TC001

Purpose

Generate Annual Pillar after Li Chun.

Input

Gregorian Date

2026-02-10

Expected

Annual Pillar

Bing Wu

Assertions

- Solar year updated
- Correct Stem
- Correct Branch

Priority

Critical

---

## TC002

Purpose

Date before Li Chun.

Input

2026-02-02

Expected

Previous Solar Year.

---

## TC003

Date exactly at Li Chun.

Expected

New Annual Pillar.

---

## TC004

Leap Year validation.

Expected

No impact.

---

## TC005

Missing Solar Term.

Expected

SOLAR_TERM_NOT_FOUND

---

# 5. Annual Pillar

## TC011

Valid Heavenly Stem.

Expected

Correct Stem.

---

## TC012

Valid Earthly Branch.

---

## TC013

Invalid Heavenly Stem.

Expected

INVALID_STEM

---

## TC014

Invalid Branch.

Expected

INVALID_BRANCH

---

## TC015

Verify complete Sexagenary Cycle.

Expected

60 unique pillars.

---

# 6. Hidden Stem

## TC021

Zi Branch

Expected

Gui only.

---

## TC022

Chou Branch.

Expected

Ji Gui Xin.

---

## TC023

Yin Branch.

Expected

Jia Bing Wu.

---

## TC024

Duplicate Hidden Stem.

Expected

Validation Error.

---

## TC025

Missing Hidden Stem.

Expected

DATABASE_ERROR

---

# 7. Ten Gods

## TC036

Annual Stem → Correct Ten God.

---

## TC037

Primary Hidden Stem.

---

## TC038

Secondary Hidden Stem.

---

## TC039

Tertiary Hidden Stem.

---

## TC040

All Hidden Stems receive Ten Gods.

---

## TC041

Different Day Master.

Expected

Ten Gods updated correctly.

---

# 8. Five Elements

## TC051

Stem Element Mapping.

---

## TC052

Branch Element Mapping.

---

## TC053

Hidden Stem Mapping.

---

## TC054

Balanced Elements.

---

## TC055

Dominant Element.

---

## TC056

Missing Element.

Expected

Zero Count.

---

# 9. Stem Relations

## TC066

Stem Combination.

---

## TC067

Stem Control.

---

## TC068

Stem Generation.

---

## TC069

Stem Competition.

---

## TC070

Stem Transformation.

---

## TC071

Combination without Transformation.

Expected

Transformation FALSE.

---

## TC072

Multiple Combinations.

---

## TC073

Combination + Control.

Expected

Both stored.

---

## TC074

Conflicting Transformations.

---

## TC075

No Relations.

---

# 10. Branch Relations

## TC086

Six Harmony.

---

## TC087

Six Clash.

---

## TC088

Three Harmony.

---

## TC089

Three Meetings.

---

## TC090

Punishment.

---

## TC091

Harm.

---

## TC092

Destruction.

---

## TC093

Self Punishment.

---

## TC094

Harmony + Clash.

Expected

Both stored.

---

## TC095

Triple Harmony incomplete.

Expected

Partial Harmony.

---

## TC096

Transformation Success.

---

## TC097

Transformation Failure.

---

## TC098

Multiple Clashes.

---

## TC099

Multiple Harmonies.

---

## TC100

No Branch Relations.

---

# 11. Dayun Relations

## TC111

Stem Interaction.

---

## TC112

Branch Interaction.

---

## TC113

Dayun Combination.

---

## TC114

Dayun Clash.

---

## TC115

Transition Year.

Expected

Transition Context.

---

## TC116

Transition Timestamp.

---

## TC117

Old Dayun only.

---

## TC118

New Dayun only.

---

## TC119

Missing Dayun.

Expected

DAYUN_NOT_FOUND

---

## TC120

Combined Annual + Dayun.

---

# 12. Special Rules

## TC126

Fu Yin.

---

## TC127

Fan Yin.

---

## TC128

Tai Sui.

---

## TC129

Kong Wang.

---

## TC130

Heavenly Virtue.

---

## TC131

Monthly Virtue.

---

## TC132

Peach Blossom.

---

## TC133

Travel Horse.

---

## TC134

Academic Star.

---

## TC135

Nobleman.

---

## TC136

Multiple Shen Sha.

Expected

All preserved.

---

## TC137

Special Rule Conflict.

---

## TC138

Useful God strengthened.

---

## TC139

Unfavorable God strengthened.

---

## TC140

Useful God transformed.

---

# 13. Validation

## TC141

Missing Natal Chart.

Expected

Validation Failure.

---

## TC142

Missing Day Master.

---

## TC143

Missing Rule Database.

---

## TC144

Missing Calendar.

---

## TC145

Missing Dayun.

---

## TC146

Invalid Priority Rules.

---

## TC147

Output Validation.

---

## TC148

Metadata Validation.

---

## TC149

Immutable Output.

Verify output object cannot be modified.

---

## TC150

Deterministic Validation.

Run identical input 100 times.

Expected

100 identical outputs.

---

# 14. Performance Tests

## PT001

Single Evaluation

Target

<10 ms

---

## PT002

1000 Consecutive Years

Expected

No memory leak.

---

## PT003

Batch Processing

1000 Charts.

Expected

Stable latency.

---

## PT004

Stress Test

100,000 evaluations.

Expected

No crash.

---

# 15. Regression Tests

Every bug fixed in production SHALL receive:

- Regression Test
- Permanent Test ID
- Reference Issue Number

Regression tests SHALL never be removed.

---

# 16. Compliance Requirements

An implementation is considered compliant only if:

- All Critical tests pass.
- All Validation tests pass.
- All Deterministic tests pass.
- No regression failures exist.
- Performance requirements are satisfied.

---

# 17. Test Coverage Goals

| Component | Minimum Coverage |
|-----------|-----------------:|
| Calendar | 100% |
| Annual Pillar | 100% |
| Hidden Stems | 100% |
| Ten Gods | 100% |
| Five Elements | 100% |
| Stem Relations | 100% |
| Branch Relations | 100% |
| Dayun Relations | 100% |
| Special Rules | 100% |
| Validation | 100% |

---

# 18. Golden Dataset Compatibility

Every official Golden Dataset case SHALL map to one or more test cases defined in this document.

The mapping SHALL be maintained by the Quality Assurance module.

End of Document