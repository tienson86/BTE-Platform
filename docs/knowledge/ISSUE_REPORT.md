# Knowledge Infrastructure — Issues / TODOs

## TODO

1. Add CI workflow job for `knowledge_cli.py validate` + `pytest tests/knowledge`.
2. When first official JSON Knowledge Records are authored, add golden fixture validation under `tests/knowledge/golden/` (without inventing academic content in Canon).
3. Optionally resolve Canon pointer schemas through the same `SchemaLoader` registry for end-to-end `$ref` checks from Canon paths.
4. Wire `tools/run_tests.py` / lint targets to include `services/knowledge` and `knowledge_cli.py`.
5. Consider full graph cycle detection beyond pairwise `depends_on` cycles.

## Review Notes for Chief Architect

1. **Canon schema pointer** — `01_five_elements/five_element.schema.json` is now a `$ref` wrapper only. Confirm this is the desired coexistence model until domain docs are updated.
2. **Relationships extensibility** — Base schema now permits additional relationship slots (object or array of `relationship_link`). Confirm this matches Wu Xing relationship modeling.
3. **Domain map ownership** — `DOMAIN_SCHEMA_MAP` lives in Python (`services/knowledge/constants.py`). Prefer promoting it to a JSON catalog under `knowledge/schema/` later.
4. **Empty Canon records** — Infrastructure is ready; content authorship remains a separate Canon sprint.
5. **Dual plane** — Registry metadata schemas (`knowledge/registry/schemas/`) remain separate from Knowledge Record schemas (`knowledge/schema/`).
