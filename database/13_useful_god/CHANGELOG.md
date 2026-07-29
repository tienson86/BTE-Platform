# Useful God Database Changelog

## 2026-07-29 — v2.0.0

- Rebuilt `database/13_useful_god/01_strength_rules.csv` from empty placeholder to production-ready schema.
- Added new rule sets:
  - `02_season_rules.csv`
  - `03_temperature_rules.csv`
  - `04_flow_rules.csv`
  - `05_priority_rules.csv`
  - `06_special_rules.csv`
- Added references:
  - `07_examples.csv`
  - `08_rule_conditions.csv`
- Added `README.md` documenting schema and rule philosophy.

## Business-data assumptions

- Priority order applied from database: special > season > strength > temperature > flow.
- Element balancing is based on stem + hidden-stem distribution from PatternContext V2.
- Follow/special pattern behavior is inherited from Pattern Engine outputs (`follow_type` / special pattern codes).

These assumptions are fully represented in CSV rules, not hard-coded in engine logic.
