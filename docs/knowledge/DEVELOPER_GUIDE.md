# Knowledge Developer Guide

## Principles

1. `knowledge/schema/` is the only authoritative Data Contract.
2. Canon-local `*.schema.json` files are pointers (`$ref`) only.
3. Infrastructure never invents Knowledge Records.
4. Loaders never evaluate Rules or Interpretation logic.

---

## Package map

| Module | Role |
|--------|------|
| `schema_loader.py` | Load Draft 2020-12 schemas + referencing registry |
| `record_loader.py` | Discover/load Canon JSON records |
| `dependency_loader.py` | Extract `depends_on` edges |
| `cache.py` | mtime cache |
| `knowledge_loader.py` | Facade |
| `*_validator.py` | Schema / relationship / reference / integrity |
| `*_index.py` | ID / dependency / relationship / search indexes |

---

## Domain → schema map

See `services/knowledge/constants.py` (`DOMAIN_SCHEMA_MAP`).

---

## Testing

```bash
pytest tests/knowledge -q --cov=services.knowledge --cov=knowledge_cli --cov-fail-under=90
```

---

## Extending

1. Add module schema under `knowledge/schema/`.
2. Register domain mapping in `DOMAIN_SCHEMA_MAP` / `DOMAIN_CONST_MAP`.
3. Add tests with temporary fixture records (never commit fake Canon content).
