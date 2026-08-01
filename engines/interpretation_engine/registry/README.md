# Registry

Interpreter Registry runtime for Pack 03.

## Runtime modules

| Module | Role |
|--------|------|
| `registry.py` | Public registry facade |
| `loader.py` | Read-only descriptor loader (Pack 01 read-only) |
| `resolver.py` | Resolve by id / interpreter_id / domain / load order |
| `dependency_graph.py` | Interpreter dependency graph + topological order |
| `metadata.py` | Entry/snapshot models + metadata normalization |
| `version_manager.py` | Version parse / compare / resolve |

Registers interpreter descriptors only. No sentence generation.
