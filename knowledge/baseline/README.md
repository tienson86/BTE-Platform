# Pack 01 Baseline Lifecycle

Generated artifacts live under versioned directories:

```text
knowledge/baseline/v1.0.0/
knowledge/baseline/v1.1.0/   # future
knowledge/baseline/v1.2.0/   # future
knowledge/baseline/v2.0.0/   # future
knowledge/baseline/versions_index.json
knowledge/baseline/diff/v1.0.0_to_v1.1.0/
```

## Rebuild

```bash
python -m baseline build --version 1.0.0
python -m baseline build --version 1.1.0
```

Do not hand-edit generated files. Source KR / registry / governance documents are never modified by the builder.

## CLI

```bash
python -m baseline build
python -m baseline validate
python -m baseline diff 1.0.0 1.1.0
python -m baseline report --name freeze_readiness.md
python -m baseline stats
```

## Diff Engine

Modules:

- `baseline/diff/engine/baseline_diff.py`
- `baseline/diff/engine/baseline_compare.py`
- `baseline/diff/engine/snapshot_loader.py`
- `baseline/diff/engine/report_generator.py`

Outputs Markdown, JSON, and HTML comparison reports.
