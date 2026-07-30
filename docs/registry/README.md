# Registry Infrastructure

**Module:** Registry Service Layer  
**Version:** V1.1.0  
**Status:** Official Infrastructure  

---

## Purpose

This package provides the infrastructure layer for the BTE Registry Module:

- Load and cache registry catalogs
- Validate JSON / schema / consistency / duplicates
- Index, query, export, import, and synchronize derived artifacts
- Provide a CLI for operators and CI

It does **not** author Knowledge Canon content, Rules, or interpretation logic.

---

## Layout

```
services/
  registry_loader.py
  registry_validator.py
  registry_indexer.py
  registry_query.py
  registry_exporter.py
  registry_importer.py
  registry_statistics.py
  registry_sync.py
  registry_checksum.py
  registry_constants.py
  registry_exceptions.py
  registry_models.py
registry_cli.py
knowledge/registry/          # data catalogs (scaffold)
docs/registry/               # developer / CLI / service guides
tests/registry/              # unit tests
```

---

## Quick Start

```bash
# Validate the real scaffold
python registry_cli.py validate --include-samples

# Statistics
python registry_cli.py stats

# Reindex (derived indexes only; does not modify Knowledge Canon)
python registry_cli.py reindex
```

---

## Documentation

- [Developer Guide](DEVELOPER_GUIDE.md)
- [CLI Guide](CLI_GUIDE.md)
- [Registry Service Guide](REGISTRY_SERVICE_GUIDE.md)

---

## Architecture Boundary

| Allowed | Forbidden |
|---------|-----------|
| Read `knowledge/registry/` | Edit `knowledge/knowledge_canon/` |
| Validate metadata catalogs | Create Rules / Knowledge content |
| Derived indexes under `.derived/` | Modify locked Specs |
| CLI / CI validation | Interpretation Engine changes |
