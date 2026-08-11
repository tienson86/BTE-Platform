# SOURCE_FIELD_CATALOG

| Source Field | Source Module | Output Field | Transformation | Availability | Provenance | Notes |
|---|---|---|---|---|---|---|
| runtime.raw_total / runtime_score.raw | synthetic result / CAL case | score_reference.raw_score | identity | AVAILABLE | engine_rule/derived | no reconstruction |
| runtime.score / normalized | synthetic / CAL | score_reference.normalized_score | identity | AVAILABLE | derived | |
| runtime.v1_band / current_v1_band | synthetic / CAL | score_reference.current_v1_band | lowercase | AVAILABLE | engine_rule | |
| runtime.profile.* | synthetic / CAL | evidence buckets / states | identity | AVAILABLE | derived | |
| runtime.context.month_status | synthetic / CAL evidence | seasonal_state.day_master_relation | identity | AVAILABLE | derived | state enum NOT inferred |
| runtime.context.root_level | synthetic / CAL | rooting_state.root_strength | identity label | AVAILABLE | derived | |
| runtime.context.root_count | synthetic / CAL | rooting_state.root_count / multiple_roots | count>=2 | AVAILABLE | derived | loci NOT available |
| runtime.context.support_type | synthetic / CAL | support_state | identity | PARTIAL | derived | |
| runtime.context.control_type | synthetic | pressure_state | identity | PARTIAL | derived | CAL may use ledger reason |
| runtime.context.drain_type | synthetic | drain_state | identity | PARTIAL | derived | |
| runtime.matched_rules | synthetic / CAL ledger | structural items / evidence | prefix cmb_/spc_ | PARTIAL | engine_rule | |
| temperature contexts | CAL evidence / synthetic context | temperature_state | identity | PARTIAL | derived | may conflict across engines |
| strength_evidence_ledger | CAL evidence | evidence_records | ledger->evidence | AVAILABLE for CAL | engine_rule | absent in SYN results |
| clash/punishment/harm/follow | none | structural_state.* | none | NOT_AVAILABLE | unknown | |
