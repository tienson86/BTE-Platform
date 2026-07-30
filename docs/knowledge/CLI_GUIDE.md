# Knowledge CLI Guide

Entrypoint: `knowledge_cli.py`

```bash
python knowledge_cli.py [--project-root PATH] [--canon-root PATH] [--schema-root PATH] <command>
```

## Commands

### validate

```bash
python knowledge_cli.py validate
```

Options: `--skip-foundation`, `--skip-schema`, `--skip-relationships`, `--skip-references`, `--skip-integrity`

### list

```bash
python knowledge_cli.py list --domain 01_five_elements --status draft --limit 20
```

### search

```bash
python knowledge_cli.py search "Wood" --limit 10
```

### stats

```bash
python knowledge_cli.py stats
```

### graph

```bash
python knowledge_cli.py graph --include-relationships --knowledge-id KNO-000001
```

### export

```bash
python knowledge_cli.py export --output ./knowledge_bundle.json
```
