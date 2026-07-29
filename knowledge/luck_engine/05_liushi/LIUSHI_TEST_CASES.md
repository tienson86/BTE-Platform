# LIUSHI TEST CASES

Version

1.0

Status

Stable

Module

05_liushi

---

# 1. Purpose

Defines the official compliance test suite for the LiuShi Module.

---

# 2. Test Categories

| Category | Test IDs |
|-----------|----------|
| Calendar | TC001–TC010 |
| Hourly Pillar | TC011–TC020 |
| Hidden Stems | TC021–TC035 |
| Ten Gods | TC036–TC050 |
| Five Elements | TC051–TC065 |
| Natal Relations | TC066–TC085 |
| LiuRi Relations | TC086–TC100 |
| LiuYue Relations | TC101–TC115 |
| LiuNian Relations | TC116–TC130 |
| Dayun Relations | TC131–TC145 |
| Validation | TC146–TC160 |

---

# 3. Representative Test Cases

TC001

Calendar Context loaded successfully.

TC002

Hour Boundary resolved correctly.

TC005

Sexagenary Hour generated correctly.

TC010

Verify complete hourly cycle.

TC011

Generate Hourly Stem.

TC012

Generate Hourly Branch.

TC020

Validate Hourly Pillar.

TC021

Expand Hidden Stems.

TC036

Calculate Hourly Ten Gods.

TC051

Map Five Elements.

TC066

Hourly vs Natal interaction.

TC086

Hourly vs Daily interaction.

TC101

Hourly vs Monthly interaction.

TC116

Hourly vs Annual interaction.

TC131

Hourly vs Dayun interaction.

TC140

Multiple simultaneous interactions.

TC146

Missing Natal Chart.

TC147

Missing Calendar Context.

TC150

Missing Rule Database.

TC155

Deterministic Validation.

Execute identical input 100 times.

Expected

100 identical outputs.

TC160

Golden Dataset Compatibility.

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