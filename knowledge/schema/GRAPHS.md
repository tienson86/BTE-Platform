# Knowledge Schema Graphs (V1.0.0)

## Dependency Graph

Edges mean “references / depends on for validation”.

```text
knowledge_record.schema.json
        ▲
        │ $ref
        │
   ┌────┴────────────────────────────────────────┐
   │                                             │
five_element.schema.json                   (all modules)
heavenly_stem.schema.json
earthly_branch.schema.json
hidden_stem.schema.json
yin_yang.schema.json
ten_god.schema.json
strength.schema.json
pattern.schema.json
useful_god.schema.json
combination.schema.json
clash.schema.json
punishment.schema.json
harm.schema.json
transformation.schema.json
seasonal_qi.schema.json
temperature.schema.json
shensha.schema.json
luck_cycle.schema.json
special_case.schema.json
```

Additional dependency:

- `five_element.schema.json` → `knowledge_record.schema.json#/$defs/relationship_link`
  (for extended Wu Xing relationship slots)

No module-to-module `$ref` edges exist in V1.0.0 (no circular references).

---

## Inheritance Graph

```text
                    knowledge_record (Base)
                               │
                               │ allOf
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
   five_element         heavenly_stem         earthly_branch
   hidden_stem          yin_yang              ten_god
   strength             pattern               useful_god
   combination          clash                 punishment
   harm                 transformation        seasonal_qi
   temperature          shensha               luck_cycle
   special_case
```

Each leaf:

1. Inherits Base required sections
2. Adds one domain extension object
3. Locks `classification.domain` / `category`
4. Closes with `unevaluatedProperties: false`
