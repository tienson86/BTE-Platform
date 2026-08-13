# IMPLEMENTATION

| Field | Value |
|-------|-------|
| Epic | EPIC-A |
| Layer | Commercial Language writer / service |
| Engines / CDR / Knowledge / Golden Dataset | Unchanged |

---

## Changes

### `applications/production/language/writer.py`

Deterministic, feature-aware paragraphs:

- WHO observation weaves output + balanced + Tòng (or self-carry path for CASE-0001)
- WORK_STYLE differs for Career vs Identity
- STRENGTHS names lived strengths (not cooling dump)
- CAREER RISK is a career risk, not identity dual-scope paste
- CAREER ENVIRONMENT includes illustrated role frames (not destiny titles)
- CAREER BALANCE = weekly work practice
- INSIGHT / memory chart-specific for output+follow
- PRESSURE no longer appends the same limitation paragraph
- SELF_CARRY paths kept distinct for Golden regression

### `applications/production/language/service.py`

- Pass theme / style / structure / capacity into the sections that needed them
- Identity STRENGTHS receives operating style
- PRESSURE no longer receives limitation keys
- Memory lines for output+Tòng tightened

No orchestrator branch. No CASE-id special-case. No engine publish edit.

---

## Tests

```text
py -3.14 -m pytest tests/production/test_commercial_language.py -q
```

**15 passed** (including `test_case_0001_regression`, `test_case_0002_acceptance`, `test_cross_case_language_divergence`).

Tests were not modified.

---

END
