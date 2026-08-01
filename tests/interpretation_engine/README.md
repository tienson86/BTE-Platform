# Interpretation Engine Test Framework

> **Path:** `tests/interpretation_engine/`

Pytest framework for Pack 03 Interpretation Engine infrastructure.

## Layout

```text
tests/interpretation_engine/
├── conftest.py
├── mocks/                 # Mock stages (no BaZi / no NLG)
├── pipeline/
├── registry/
├── context/
├── sentence_engine/
├── template_engine/
├── output/
└── .coveragerc
```

Runtime tests use mocks only. No business logic. No sentence library. No templates.

```bash
python -m pytest tests/interpretation_engine -q
```

Infrastructure coverage:

```bash
python -m coverage run --rcfile=tests/interpretation_engine/.coveragerc -m pytest tests/interpretation_engine -q
python -m coverage report --rcfile=tests/interpretation_engine/.coveragerc
```

Target: >90% on Pack 03 infrastructure modules
(pipeline / context / registry / sentence_engine / template_engine / output models).
