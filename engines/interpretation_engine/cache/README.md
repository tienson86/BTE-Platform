# Cache

Memory-only cache infrastructure for Pack 03.

## Domains

| Cache | Module |
|-------|--------|
| Context | `context_cache.py` |
| Sentence | `sentence_cache.py` |
| Template | `template_cache.py` |
| Placeholder | `placeholder_cache.py` |
| Registry | `registry_cache.py` |

## Rules

- No Redis
- Memory cache only
- Dependency Injection via `CacheManager`
- No singleton globals
- Legacy `InterpretationCache` remains re-exported for compatibility
