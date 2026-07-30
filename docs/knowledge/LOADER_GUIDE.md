# Knowledge Loader Guide

## Components

### SchemaLoader

Loads every `*.schema.json` under `knowledge/schema/`, caches by mtime, and builds a Draft 2020-12 `referencing.Registry`.

### RecordLoader

Walks Canon domain directories (`01_five_elements`, …), loads `*.json` records, and **skips** `*.schema.json` pointer files.

### DependencyLoader

Reads only `relationships.depends_on[*].knowledge_id`.

### KnowledgeLoader

Facade exposing:

- `load_schemas()`
- `load_records(domain_dir=None)`
- `load_dependencies()`
- `get_record(knowledge_id)`
- `stats()`
- `export_bundle()`

## Cache

`MtimeCache` invalidates when file mtime changes. Call `clear_cache()` after external writes.

## Non-goals

- No Rule loading
- No Interpretation
- No writes into Knowledge Canon
