# Analysis Engine Test Framework

> **Path:** `tests/analysis_engine/`

Pytest framework for Analysis Engine infrastructure.

## Layout

```text
tests/analysis_engine/
├── conftest.py
├── mocks/              # Mock stages/analyzers (no BaZi rules)
├── pipeline/           # Pipeline orchestration integration tests
├── context/            # Context lifecycle integration tests
├── registry/           # Registry runtime integration tests
├── results/            # Result infrastructure integration tests
├── api/                # Public API facade integration tests
├── unit/
├── integration/
├── golden/
├── fixtures/
├── builders/
└── snapshots/
```

Runtime integration tests use mock analyzers only. No real BaZi rules.

```bash
python -m pytest tests/analysis_engine -q
```

Infrastructure coverage (pipeline / context / registry / results / API facade):

```bash
python -m coverage run --rcfile=tests/analysis_engine/.coveragerc -m pytest tests/analysis_engine -q
python -m coverage report --rcfile=tests/analysis_engine/.coveragerc
```

Target: >90% on implemented infrastructure runtime modules.
