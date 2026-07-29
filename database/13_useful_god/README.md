# Useful God Rule Database V2

Thư mục này là nguồn tri thức duy nhất cho Useful God Engine V2.

## Files
- 01_strength_rules.csv: rules theo thân vượng/nhược
- 02_season_rules.csv: rules theo mùa/nguyệt lệnh
- 03_temperature_rules.csv: rules theo hàn nhiệt
- 04_flow_rules.csv: rules theo lưu thông ngũ hành
- 05_priority_rules.csv: bảng priority theo nhóm rule
- 06_special_rules.csv: rules cho tòng cách/chuyên cách
- 07_examples.csv: ví dụ tham chiếu
- 08_rule_conditions.csv: thư viện điều kiện

## Rule schema
rule_id, priority, score, conditions, useful_god, favorable_gods, unfavorable_gods, reason, description, reference, status, enabled

## Notes
- `conditions` là JSON array
- `favorable_gods` và `unfavorable_gods` là JSON array
- Không hard-code tri thức trong Python
