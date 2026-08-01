# Analyzers Package

Architecture skeleton for Analysis Engine analyzers.

## Analyzer Modules

| Directory | Analyzer |
|-----------|----------|
| `strength/` | Strength Analyzer |
| `pattern/` | Pattern Analyzer |
| `temperature/` | Temperature Analyzer |
| `useful_god/` | Useful God Analyzer |
| `ten_gods/` | Ten Gods Analyzer |
| `combination/` | Combination Analyzer |
| `shensha/` | Shen Sha Analyzer |
| `dayun/` | Dayun Analyzer |
| `liunian/` | Liunian Analyzer |
| `liuyue/` | Liuyue Analyzer |
| `scoring/` | Scoring Analyzer |
| `conflict/` | Conflict Analyzer |

Each analyzer contains:

```text
README.md
VERSION
CHANGELOG.md
SPEC.md
analyzer.py
models.py
interfaces.py
validator.py
```

Public interfaces only. No business logic. No BaZi analysis.
