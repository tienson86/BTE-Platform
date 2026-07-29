# LIURI TEST CASES

Version

1.0

Status

Stable

Module

04_liuri

---

# 1. Purpose

Defines the official compliance test suite for the LiuRi Module.

---

# 2. Test Categories

| Category | Test IDs |
|-----------|----------|
| Calendar | TC001–TC010 |
| Daily Pillar | TC011–TC020 |
| Hidden Stems | TC021–TC035 |
| Ten Gods | TC036–TC050 |
| Five Elements | TC051–TC065 |
| Natal Relations | TC066–TC085 |
| LiuYue Relations | TC086–TC100 |
| LiuNian Relations | TC101–TC115 |
| Dayun Relations | TC116–TC130 |
| Special Rules | TC131–TC145 |
| Validation | TC146–TC160 |

---

# 3. Representative Test Cases

## TC001

Calendar Context loaded successfully.

---

## TC002

Invalid Julian Day.

Expected

INVALID_JDN

---

## TC010

Verify complete Sexagenary Day sequence.

---

## TC011

Generate Daily Heavenly Stem.

---

## TC012

Generate Daily Earthly Branch.

---

## TC020

Verify complete 60-day cycle.

---

## TC021

Expand Hidden Stems correctly.

---

## TC036

Calculate Daily Ten Gods.

---

## TC051

Five Element mapping.

---

## TC066

Daily vs Natal Stem Combination.

---

## TC070

Daily vs Natal Branch Clash.

---

## TC086

Daily vs Monthly interaction.

---

## TC101

Daily vs Annual interaction.

---

## TC116

Daily vs Dayun interaction.

---

## TC131

Fu Yin.

---

## TC132

Fan Yin.

---

## TC133

Tai Sui interaction.

---

## TC134

Kong Wang.

---

## TC140

Multiple simultaneous events.

---

## TC146

Missing Natal Chart.

---

## TC147

Missing Calendar Context.

---

## TC150

Missing Rule Database.

---

## TC155

Deterministic Validation.

Run identical input 100 times.

Expected

100 identical outputs.

---

## TC160

Golden Dataset compatibility.

---

# 4. Performance Tests

Single Evaluation

<10 ms

Batch

1000 evaluations

Stress

100000 evaluations

No crash

---

# 5. Regression Policy

Every production bug SHALL receive a permanent regression test.

---

# 6. Compliance

100% Validation Tests

100% Deterministic Tests

100% Critical Tests

must pass.

End of Document