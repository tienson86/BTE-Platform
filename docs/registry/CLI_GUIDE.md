# Registry CLI Guide

Entrypoint: `registry_cli.py`

```bash
python registry_cli.py [--project-root PATH] [--registry-root PATH] [-v] <command>
```

---

## Commands

### validate

```bash
python registry_cli.py validate --include-samples
```

Options:

- `--include-samples`
- `--skip-schema`
- `--skip-duplicates`
- `--skip-consistency`

Exit code `0` when no error-severity issues exist.

### stats

```bash
python registry_cli.py stats
```

### list

```bash
python registry_cli.py list --registry knowledge_registry --status draft --limit 20
```

### search

```bash
python registry_cli.py search "KNO-000001" --limit 10
```

### export

```bash
python registry_cli.py export --output ./out --include-indexes
python registry_cli.py export --bundle --output bundle.json
python registry_cli.py export --registry knowledge_registry --output kr.json
```

### import

```bash
python registry_cli.py import --source incoming.json --dry-run
python registry_cli.py import --source bundle.json --bundle
```

### reindex

```bash
python registry_cli.py reindex --write --workers 4
```

Writes derived indexes under `knowledge/registry/.derived/indexes/` and refreshes `registry_statistics.json` when `--write` is set.

---

## CI Usage

```bash
python registry_cli.py validate --include-samples
python registry_cli.py stats
```
