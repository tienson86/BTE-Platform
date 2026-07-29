# LIUYUE TEST CASES

Version

1.0

Status

Stable

Module

03_liuyue

---

# 1. Purpose

This document defines the official compliance test suite for the LiuYue Module.

The objective is to verify that every implementation produces deterministic,
repeatable and standards-compliant Monthly Context results.

The test suite covers

- Solar Month determination
- Monthly Pillar generation
- Hidden Stem expansion
- Ten Gods calculation
- Five Element analysis
- Seasonal influence
- Natal interactions
- Dayun interactions
- LiuNian interactions
- Transformation rules
- Priority rules
- Validation
- Performance
- Regression

---

# 2. Test Categories

| Category | Test IDs |
|------------|----------------|
| Calendar | TC001–TC010 |
| Monthly Pillar | TC011–TC020 |
| Hidden Stems | TC021–TC035 |
| Ten Gods | TC036–TC050 |
| Five Elements | TC051–TC065 |
| Seasonal Context | TC066–TC080 |
| Natal Relations | TC081–TC100 |
| Dayun Relations | TC101–TC115 |
| LiuNian Relations | TC116–TC130 |
| Special Rules | TC131–TC145 |
| Validation | TC146–TC160 |

---

# 3. Standard Test Template

Every test SHALL contain

Test ID

Purpose

Input

Expected Result

Assertions

Priority

---

# 4. Calendar Tests

## TC001

Purpose

Date after Li Chun.

Expected

Correct Solar Month.

---

## TC002

Date before Li Chun.

Expected

Previous Solar Month.

---

## TC003

Exactly at Solar Term.

Expected

New Monthly Pillar.

---

## TC004

Leap Year.

Expected

No influence.

---

## TC005

Missing Solar Term.

Expected

LIUYUE_001

---

## TC006

Timezone validation.

---

## TC007

Boundary timestamp.

---

## TC008

Last second of previous month.

---

## TC009

First second of new month.

---

## TC010

Continuous month sequence.

Expected

12 valid Solar Months.

---

# 5. Monthly Pillar Tests

## TC011

Generate Monthly Stem.

---

## TC012

Generate Monthly Branch.

---

## TC013

Verify Stem sequence.

---

## TC014

Verify Branch sequence.

---

## TC015

Verify Five Tiger Dunjia rules.

---

## TC016

Invalid Stem.

---

## TC017

Invalid Branch.

---

## TC018

Invalid Pillar.

---

## TC019

Duplicate Pillar.

---

## TC020

Complete 60-cycle verification.

---

# 6. Hidden Stem Tests

## TC021

Zi Hidden Stem.

---

## TC022

Chou Hidden Stems.

---

## TC023

Yin Hidden Stems.

---

## TC024

Canonical ordering.

---

## TC025

Missing Hidden Stem.

---

## TC026

Duplicate Hidden Stem.

---

## TC027

Primary Hidden Stem.

---

## TC028

Secondary Hidden Stem.

---

## TC029

Tertiary Hidden Stem.

---

## TC030–TC035

Verify all twelve Earthly Branches.

---

# 7. Ten Gods Tests

## TC036

Monthly Stem Ten God.

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

Different Day Master.

---

## TC041

Useful God interaction.

---

## TC042

Unfavorable God interaction.

---

## TC043

All Hidden Stems assigned.

---

## TC044

No duplicate Ten Gods.

---

## TC045–TC050

Mixed chart scenarios.

---

# 8. Five Element Tests

## TC051

Stem mapping.

---

## TC052

Branch mapping.

---

## TC053

Hidden Stem mapping.

---

## TC054

Element count.

---

## TC055

Balanced Elements.

---

## TC056

Dominant Element.

---

## TC057

Weak Element.

---

## TC058

Strong Element.

---

## TC059

Element transformation.

---

## TC060–TC065

Combined Element scenarios.

---

# 9. Seasonal Context Tests

## TC066

Spring.

---

## TC067

Summer.

---

## TC068

Autumn.

---

## TC069

Winter.

---

## TC070

Transition season.

---

## TC071

Temperature.

---

## TC072

Humidity.

---

## TC073

Dryness.

---

## TC074

Season strength.

---

## TC075

Weak seasonal support.

---

## TC076–TC080

Complex seasonal combinations.

---

# 10. Natal Relation Tests

## TC081

Stem Combination.

---

## TC082

Stem Clash.

---

## TC083

Branch Combination.

---

## TC084

Branch Clash.

---

## TC085

Punishment.

---

## TC086

Harm.

---

## TC087

Destruction.

---

## TC088

Self Punishment.

---

## TC089

Three Harmony.

---

## TC090

Three Meetings.

---

## TC091

Transformation.

---

## TC092

Failed Transformation.

---

## TC093

Multiple Combination.

---

## TC094

Multiple Clash.

---

## TC095

Harmony + Clash.

---

## TC096

Transformation conflict.

---

## TC097

Hidden Stem interaction.

---

## TC098

Useful God strengthened.

---

## TC099

Unfavorable God strengthened.

---

## TC100

No interaction.

---

# 11. Dayun Relation Tests

## TC101

Stem relation.

---

## TC102

Branch relation.

---

## TC103

Combination.

---

## TC104

Clash.

---

## TC105

Transformation.

---

## TC106

Dayun transition month.

---

## TC107

Old Dayun.

---

## TC108

New Dayun.

---

## TC109

Triple interaction.

---

## TC110–TC115

Mixed scenarios.

---

# 12. LiuNian Relation Tests

## TC116

Stem interaction.

---

## TC117

Branch interaction.

---

## TC118

Combination.

---

## TC119

Clash.

---

## TC120

Transformation.

---

## TC121

Monthly + Annual + Natal.

---

## TC122

Monthly + Annual + Dayun.

---

## TC123

Four-layer interaction.

---

## TC124

Useful God.

---

## TC125

Unfavorable God.

---

## TC126–TC130

Complex annual scenarios.

---

# 13. Special Rule Tests

## TC131

Fu Yin.

---

## TC132

Fan Yin.

---

## TC133

Tai Sui.

---

## TC134

Kong Wang.

---

## TC135

Peach Blossom.

---

## TC136

Travel Horse.

---

## TC137

Heavenly Virtue.

---

## TC138

Monthly Virtue.

---

## TC139

Academic Star.

---

## TC140

Nobleman.

---

## TC141

Multiple Shen Sha.

---

## TC142

Priority conflict.

---

## TC143

Transformation priority.

---

## TC144

Useful God priority.

---

## TC145

Multiple simultaneous events.

---

# 14. Validation Tests

## TC146

Missing Natal Chart.

---

## TC147

Missing Dayun.

---

## TC148

Missing LiuNian.

---

## TC149

Missing Solar Terms.

---

## TC150

Missing Rule Database.

---

## TC151

Missing Priority Rules.

---

## TC152

Output Validation.

---

## TC153

Metadata Validation.

---

## TC154

Immutable Output.

---

## TC155

Deterministic Output.

---

## TC156

Invalid Configuration.

---

## TC157

Performance Validation.

---

## TC158

Memory Leak Test.

---

## TC159

Regression Validation.

---

## TC160

Golden Dataset Compatibility.

---

# 15. Performance Requirements

Single evaluation

<10 ms

1000 evaluations

Stable

100000 evaluations

No crash

Memory leak

None

---

# 16. Regression Policy

Every production bug SHALL receive

- Permanent Test ID
- Regression Test
- Issue Reference

Regression tests SHALL never be removed.

---

# 17. Compliance

An implementation SHALL pass

- 100% Validation Tests
- 100% Deterministic Tests
- 100% Critical Tests

before being considered compliant.

End of Document