# Cache Package

> **Path:** `engines/analysis_engine/cache/`

In-memory cache subsystem for Analysis Engine runtime.

## Modules

| Module | Surface |
|--------|---------|
| `cache_manager.py` | `CacheManager` |
| `cache_policy.py` | `CachePolicy`, `EvictionPolicy` |
| `memory_cache.py` | `MemoryCache`, `CacheStats` |
| `context_cache.py` | `ContextCache` |
| `registry_cache.py` | `RegistryCache` |

Memory only. No Redis, disk, or network cache backends.

Related registry contract: `registry/cache_contract.py`.
Distinct from legacy `runtime.cache_manager.CacheManager`.
