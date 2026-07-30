# Registry Developer Guide

## Overview

Registry infrastructure lives under `services/` and operates on JSON catalogs in `knowledge/registry/`.

Authoritative architecture specs remain under:

`knowledge/knowledge_canon/registry/REGISTRY_*.md`

Those specs are read-only for this infrastructure sprint.

---

## Environment

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install pytest-cov
```

`jsonschema` is required for schema validation.

---

## Core Types

- `RegistryLoader` — lazy load + mtime cache
- `RegistryValidator` — JSON / schema / consistency / duplicates
- `RegistryIndexer` — parallel derived indexes
- `RegistryQuery` — list / get / search
- `RegistryExporter` / `RegistryImporter` — IO
- `RegistryStatistics` / `RegistrySync` — aggregates and derived writes

Result models are dataclasses in `services/registry_models.py`.

---

## Adding a Catalog

1. Create `knowledge/registry/<name>/<name>.json` with `{ "version", "records": [] }`
2. Register it in `global_registry/registry_index.json`
3. Run `python registry_cli.py validate`
4. Do **not** invent Knowledge / Rule business content in this layer

---

## Testing

```bash
pytest tests/registry -q --cov=services --cov=registry_cli --cov-report=term-missing
```

Coverage target: **>= 90%** for `services/` registry modules.

---

## Performance Notes

- Catalogs are lazy-loaded and cached by file mtime
- Index rebuild supports `ThreadPoolExecutor` parallelism
- Duplicate detection is O(n) via hash maps

---

## TODO

- TODO: Full graph cycle detection beyond pairwise mutual dependencies
- TODO: Optional content-addressed object checksum excluding the checksum field itself
