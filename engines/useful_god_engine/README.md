# Useful God Engine V2

Useful God Engine V2 là engine xác định Dụng Thần/Hỷ Thần/Kỵ Thần theo kiến trúc data-driven.

## Pipeline

PatternContext V2
-> Strength Analyzer
-> Season Analyzer
-> Temperature Analyzer
-> Flow Analyzer
-> Balance Analyzer
-> Candidate Generator
-> Priority Resolver
-> UsefulGodResult

## Database

Mặc định đọc dữ liệu từ `database/13_useful_god/`.

## Public API

- `UsefulGodEngine.calculate(context) -> UsefulGodResult`
- `UsefulGodResult.to_portal_dict()`

## Notes

- Không hard-code nghiệp vụ Dụng Thần trong Python.
- Ưu tiên chọn winner theo `05_priority_rules.csv` + điểm rule.
- Trace nằm trong `UsefulGodResult.metadata.trace`.
