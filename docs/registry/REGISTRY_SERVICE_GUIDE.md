# Registry Service Guide

## Service Map

| Module | Responsibility |
|--------|----------------|
| `registry_loader.py` | Discover and load catalogs; lazy cache |
| `registry_validator.py` | JSON, schema, consistency, duplicates |
| `registry_indexer.py` | Parallel derived indexes |
| `registry_query.py` | List / get / search |
| `registry_exporter.py` | Export catalogs and bundles |
| `registry_importer.py` | Import catalogs and bundles |
| `registry_statistics.py` | Aggregate counters |
| `registry_sync.py` | Reindex + statistics refresh |
| `registry_checksum.py` | SHA-256 utilities |

---

## Loader

```python
from services.registry_loader import RegistryLoader

loader = RegistryLoader(registry_root="knowledge/registry")
catalogs = loader.load_all_catalogs()
```

---

## Validator

```python
from services.registry_validator import RegistryValidator

result = RegistryValidator(loader).validate_all(include_samples=True)
assert result.ok
```

Validation covers:

1. Container structure / semver
2. JSON Schema (record + container)
3. Duplicate `registry_id` / `object_id` / `uri`
4. Namespace / object-type consistency
5. Broken and pairwise circular dependencies

---

## Indexer / Query

```python
from services.registry_indexer import RegistryIndexer
from services.registry_query import RegistryQuery

indexes = RegistryIndexer(loader).reindex(parallel=True)
hits = RegistryQuery(loader).search("KREG")
```

---

## Sync

```python
from services.registry_sync import RegistrySync

RegistrySync(loader).sync_all(write=True)
```

`write=True` updates:

- `.derived/indexes/*.json`
- `global_registry/registry_statistics.json`

It never writes Knowledge Canon or Rule Database content.

---

## Error Model

All service errors inherit `services.registry_exceptions.RegistryError`.

---

## Non-Goals

- No Rule evaluation
- No Interpretation generation
- No Knowledge authorship
- No Schema / Spec mutation
