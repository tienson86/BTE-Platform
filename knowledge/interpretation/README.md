# BaZi Interpretation Knowledge System

Version: K1 (framework)

This package is the **permanent expert knowledge layer** between Decision Explanation and Narrative.

## Role

```text
Engine Truth → Canonical Facts → Decision Explanation → BaZi Knowledge → Narrative → Report
```

Knowledge **explains meaning** of already-decided analytical truth.

Knowledge **never** calculates astrology.

## Sprint K1 scope

- Framework contracts (KnowledgeEntity, Registry, Loader, Validator)
- One golden example: `UsefulGod` → `Đinh`
- No full knowledge base population
- No customer narrative
- No UI / report changes

## Runtime

Python runtime lives at:

`engines/interpretation_engine/foundation/knowledge/`

Data and schemas live here under `knowledge/interpretation/`.

## Usage

```python
from engines.interpretation_engine.foundation.knowledge import KnowledgeRegistry

registry = KnowledgeRegistry.default()
entity = registry.get("UsefulGod", "Đinh")
```

Interpreters request knowledge by `(domain, key)` only — storage location is opaque.
