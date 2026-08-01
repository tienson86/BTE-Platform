# Registry Package

> **Path:** `engines/analysis_engine/registry/`

Registry layer compatible with Pack 01 Registry responsibilities
(register / index / manage / lookup / resolve / serve).

## Modules

| Module | Surface |
|--------|---------|
| `registry.py` | `Registry` |
| `registry_builder.py` | `RegistryBuilder` |
| `registry_loader.py` | `RegistryLoader` |
| `registry_validator.py` | `RegistryValidator` |
| `registry_cache.py` | `RegistryCache` |
| `registry_models.py` | Entry / Snapshot / QuerySpec |
| `registry_index.py` | `RegistryIndex` |
| `registry_query.py` | `RegistryQuery` |
| `registry_export.py` | `RegistryExport` |
| `registry_contract.py` | `RegistryContract` |
| `query_contract.py` | `RegistryQueryContract` |
| `loader_contract.py` | `RegistryLoaderContract` |
| `cache_contract.py` | `RegistryCacheContract` |
| `provider_contract.py` | `RegistryProviderContract` |

Interfaces only. No Pack 01 mutation.
