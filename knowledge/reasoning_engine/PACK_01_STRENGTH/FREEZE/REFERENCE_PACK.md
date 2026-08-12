# Reference Pack V1.0 — Immutable until V1.1

| Field | Value |
|-------|-------|
| Document | REFERENCE_PACK |
| Status | FROZEN |

---

# 1. PACK-01 is Reference Pack V1.0

Future packs copy **this freeze’s contracts**, not ad-hoc sentence logic.

---

# 2. Immutable until V1.1 (this freeze folder)

All files under:

`knowledge/reasoning_engine/PACK_01_STRENGTH/FREEZE/`

including this file.

Edits require an explicit V1.1 freeze, not a silent patch.

---

# 3. Immutable as **sources** (do not edit to make implementation easier)

These were already completed; this freeze does **not** modify them:

| Package | Path |
|---------|------|
| Interpretation Standard | `knowledge/interpretation_standard/PACK_01_STRENGTH/` |
| Interpretation Knowledge | `knowledge/interpretation_knowledge/PACK_01_STRENGTH/` |
| Prototype | `knowledge/prototypes/PACK_01_PROTOTYPE/` |
| Reasoning Design | `knowledge/reasoning_engine/PACK_01_STRENGTH/` (parent, excluding new FREEZE files) |
| Rule Database | `knowledge/rule_database/01_strength*` / engine rules |
| Report Engine | `engines/report_engine/` |

Foundation / Product Manifesto remain higher law.

---

# 4. What may still be authored without un-freezing this folder

- Catalog **instance rows** that **conform** to [KNOWLEDGE_CATALOG.md](KNOWLEDGE_CATALOG.md) (new files under a future catalog instance path, not a rewrite of freeze schema)
- Sentence library records that bind to frozen `knowledge_id`s
- Production engine code that **implements** the freeze

Instance authoring must not change golden CASE-0001 plan shape.

---

END
