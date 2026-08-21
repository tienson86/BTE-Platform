# G3-01 — Runtime data manifest

Engines resolve paths from `__file__` relative to repository root (`engines/` → parents[2] = repo root). Production must keep this layout. Read-only.

| Runtime data | Path | Loaded by | Required? | Freeze source |
|--------------|------|-----------|-----------|---------------|
| Calendar CSV / solar terms | `engines/calendar_engine/data/`, `…/solar_terms/data/` | CalendarEngine | Yes | Gate 1 |
| Hidden stems | `database/09_hidden_stems/` | Ten Gods | Yes | Gate 1 |
| Temperature | `database/11_temperature/` | TemperatureEngine | Yes | Gate 1 |
| Strength | `database/12_strength/` | StrengthEngine | Yes | Gate 1 |
| Useful God | `database/13_useful_god/` | UsefulGodEngine | Yes | Gate 1 |
| Pattern | `database/14_pattern/` | PatternEngine | Yes | Gate 1 |
| Score | `database/15_score_engine/` | ScoreEngine | Yes | Gate 1 |
| ShenSha maps | `database/05_phan_tich/07_than_sat/` | ShenSha loaders | Yes | Gate 1 |
| Ten Gods / relations | `database/01_du_lieu_goc/`, `database/02_quan_he/` | Ten Gods / Pattern | Yes | Gate 1 |
| Knowledge CSVs | `database/20_knowledge/` | Commercial knowledge | Yes (narrative) | Gate 1 / G2-03 |
| Interpretation rules | `database/interpretation_rules/` | Interpretation | Yes | Gate 1 |
| Report V1 templates | `engines/report_engine/templates/v1/` | HTML/PDF | Yes | G2-04 |
| Knowledge packages | `knowledge/packages/` | Composer / packages | Runtime as currently loaded | Gate 1 |
| Interpretation knowledge | `knowledge/interpretation/` (`knowledge_registry.json`, `domains/`, `concepts/`) | JsonKnowledgeLoader / ConceptRegistry | Yes (Analyze narrative) | Gate 1 / G2 |
| Portal templates | `applications/customer_portal/templates/` | Portal FastAPI | Yes | G2 |
| Portal static + dist | `applications/customer_portal/static/` | Portal FastAPI | Yes | G2 |
| WP11 JSON data dir | `applications/data/` (`BTE_DATA_DIR`) | storage factory | Optional for customer Analyze | not History |

Customer History is **browser-local** (max 30). No History database.

PDF fonts: CSS stack `"Segoe UI", Arial, "Noto Sans", sans-serif` in Report V1. No proprietary font files are shipped. Linux should provide Noto/DejaVu-equivalent Unicode coverage via Playwright/Chromium.

DOCX: `Document()` in memory; no machine-local template path.
