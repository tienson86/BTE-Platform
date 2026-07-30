# Knowledge Infrastructure

**Module:** Knowledge Infrastructure  
**Version:** V1.1.0  
**Status:** Official  

---

## Purpose

Runtime infrastructure for Knowledge Canon:

- Load schemas and records
- Validate against `knowledge/schema/`
- Index / search / graph
- Operator CLI

Does **not** author Knowledge Records or Rules.

---

## Layout

```
knowledge/schema/                 # single Data Contract source
services/knowledge/               # loader / validator / index
knowledge_cli.py
docs/knowledge/
tests/knowledge/
```

Canon-local schema pointers (if any) must `$ref` into `knowledge/schema/`.

---

## Quick Start

```bash
python knowledge_cli.py validate
python knowledge_cli.py stats
python knowledge_cli.py list
python knowledge_cli.py search "Wood"
python knowledge_cli.py graph --include-relationships
python knowledge_cli.py export --output out/knowledge_bundle.json
```

---

## Guides

- [Developer Guide](DEVELOPER_GUIDE.md)
- [CLI Guide](CLI_GUIDE.md)
- [Loader Guide](LOADER_GUIDE.md)
- [Validator Guide](VALIDATOR_GUIDE.md)
