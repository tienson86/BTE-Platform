# Golden Dataset Report

Total Cases : 3

Passed      : 0

Failed      : 3

---

## case_0001 [FAIL]

### Validation Errors

- <root>: Additional properties are not allowed ('diagnostics', 'engine_version', 'execution_time_ms', 'generated_at', 'grade', 'warnings', 'weight' were unexpected) ({'case_id': 'case_0001', 'engine_version': '1.0.0', 'generated_at': '2026-07-19T00:00:00Z', 'execution_time_ms': 6, 'warnings': [], 'score': {'strength': 56, 'pattern': 91, 'useful_god': 94, 'ten_gods': 83, 'five_elements': 78, 'hidden_stems': 82, 'combinations': 65, 'conflicts': 18, 'shen_sha': 74, 'luck': 0, 'total': 82}, 'weight': {'strength': 0.2, 'pattern': 0.2, 'useful_god': 0.2, 'ten_gods': 0.15, 'five_elements': 0.1, 'hidden_stems': 0.05, 'combinations': 0.05, 'conflicts': 0.03, 'shen_sha': 0.02, 'luck': 0.0}, 'grade': {'level': 'A', 'description': 'Lá số có chất lượng tốt.'}, 'diagnostics': {'missing_scores': [], 'normalized': True}})
- score: Additional properties are not allowed ('combinations', 'conflicts', 'five_elements', 'hidden_stems' were unexpected) ({'strength': 56, 'pattern': 91, 'useful_god': 94, 'ten_gods': 83, 'five_elements': 78, 'hidden_stems': 82, 'combinations': 65, 'conflicts': 18, 'shen_sha': 74, 'luck': 0, 'total': 82})

### Differences

- text
  - expected: Nhat chu Canh Kim sinh thang Suu, than can bang, Chinh Quan thanh cach, Dung Than la Thuy.
  - actual  : BTE interpretation

## expected_schema [FAIL]

### Validation Errors

- <root>: Cannot detect schema. (None)

## input_schema [FAIL]

### Validation Errors

- <root>: Cannot detect schema. (None)

