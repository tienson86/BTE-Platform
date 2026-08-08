# D1 — Narrative Runtime Coverage Report

Version: 1.0

Status: COMPLETE — Sprint D1

Pack: 05 (Narrative Engine)

Date: 2026-08-08

---

# 1. Test Command

```
python -m pytest tests/narrative_engine -q --cov=engines.narrative_engine.runtime --cov-report=term-missing
```

---

# 2. Results

| Metric | Value |
|--------|-------|
| Tests | **8 passed** |
| Runtime package coverage | **~86%** statements |

---

# 3. Coverage by Module

| Module | Cover | Notes |
|--------|------:|-------|
| `__init__.py` | 100% | |
| `component_ordering.py` | 100% | |
| `runtime.py` | 100% | |
| `exceptions.py` | 100% | |
| `composer.py` | ~98% | |
| `component_selector.py` | ~97% | |
| `confidence_resolver.py` | ~95% | |
| `tree_builder.py` | ~95% | |
| `models.py` | ~95% | |
| `evidence_validation.py` | ~91% | |
| `validator.py` | ~74% | Rare invalid-shape branches |
| `dependency_resolver.py` | ~70% | INVALID/BLOCKED edge paths |
| `input_adapter.py` | ~70% | Object-style AnalysisResult path less exercised |

---

# 4. Behavioral Coverage

| Behavior | Covered by tests |
|----------|------------------|
| Official 7-node order | Yes |
| No prose fields on nodes | Yes |
| Rich evidence → READY components | Yes |
| Observation insufficient cascade | Yes |
| Invalid analysis gate | Yes |
| Invalid interpretation gate | Yes |
| Empty input → all insufficient | Yes |
| Dict adapter + technical interp gating | Yes |
| Engine `compose_tree` wrapper | Yes |
| Evidence dedupe / confidence clamp | Yes |

---

# 5. Remaining Misses (Acceptable for D1)

- Object-attribute AnalysisResult extraction branches in `input_adapter`
- Synthetic INVALID upstream → BLOCKED paths
- Validator branches for malformed node shapes (not constructible via public composer)

---

# 6. Verdict

**Coverage adequate for Sprint D1 Narrative Runtime.**

No Golden Dataset modified.

No Snapshot modified.

---

END
