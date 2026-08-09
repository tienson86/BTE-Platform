# Node Model

See `reasoning_node.schema.json`.

Observation nodes carry chart facts in `metadata.chart_facts`. Inference nodes MUST set `source_rule`. Evidence nodes SHOULD set both `source_rule` and `source_evidence`.
