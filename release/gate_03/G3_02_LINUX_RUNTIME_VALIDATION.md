# G3-02 — Linux runtime validation

## Result on this freeze host

**PASS** — G3-02L-R1. Linux container smoke after knowledge packaging repair.

Evidence: `release/gate_03/G3_02_SMOKE.json`, `release/gate_03/G3_02L_R1_RUNTIME_KNOWLEDGE_PACKAGING_REPAIR.md`.

| Check | Result |
|-------|--------|
| CPython | 3.14.6 (`python:3.14.6-slim`) |
| `runtime.system` | Linux |
| Ten control cases | 0 diffs |
| Dũng PDF/DOCX | `%PDF-` 149551 bytes; DOCX zip 40788; Hỷ string present |
| Tuyền PDF/DOCX | `%PDF-` 146972 bytes; DOCX zip 40859; Hỷ string present |
| `ZoneInfo("Asia/Ho_Chi_Minh")` | available |
| Locale | `C.UTF-8` / UTF-8 |
| Chromium | `/opt/ms-playwright` (Playwright install in API image) |
| Interpretation registry | `/app/knowledge/interpretation/knowledge_registry.json` present |

Windows supporting evidence remains valid and is not a substitute; Linux is now proven in `bte-api:g3-02-smoke`.

## Required Linux environment

| Item | Freeze |
|------|--------|
| OS | Debian via `python:3.14.6-slim` **or** Ubuntu 24.04 host with 3.14.6 in a venv/container |
| Locale | `C.UTF-8` or `en_US.UTF-8` (`LANG`/`LC_ALL`) |
| Timezone database | OS `tzdata` **and/or** PyPI `tzdata==2026.3` |
| Application timezone | `Asia/Ho_Chi_Minh` (Calendar input / API `default_timezone`). Server OS may stay **UTC**. |
| Fonts | `fonts-noto-core` + `fonts-liberation` + `fonts-dejavu-core` (no proprietary fonts shipped) |
| Chromium | `python -m playwright install chromium` after OS deps (`playwright install-deps chromium`) |
| Layout | repo root: `engines/`, `applications/`, `database/`, `knowledge/expert_translation`, `knowledge/packages`, `knowledge/knowledge_catalog`, `knowledge/interpretation` |

## Command to run when Docker exists

```
docker compose -f deployment/docker/docker-compose.g3-02-smoke.yml up --build
```

Then from a checkout that includes `release/gate_03/_g3_02_linux_smoke.py` (bind-mount recommended):

```
python -m pip check
python release/gate_03/_g3_02_linux_smoke.py
```

In-image:

```
docker compose -f deployment/docker/docker-compose.g3-02-smoke.yml exec api python /app/release/gate_03/_g3_02_linux_smoke.py
```

Wrapper: `release/gate_03/_g3_02_linux_smoke.sh`.

PASS requires `mismatch_count: 0` **and** `runtime.system == Linux`.

## Timezone

Control cases already pin `timezone` on the Analyze body (`Asia/Bangkok` or `Asia/Ho_Chi_Minh`). Expected vs Frozen Truth: **0 pillar diffs**. Do not change Calendar semantics. Missing tz database must fail clearly (`ZoneInfoNotFoundError`), not silently use local time.

## Locale

Recommended production locale: `C.UTF-8`. Analytical calculations must not depend on it. JSON and CSV are UTF-8.

## Startup failure (expected, not mocked)

| Missing | Expected |
|---------|----------|
| `database/` | loader / engine error, HTTP 500 pipeline — no mock rules |
| `knowledge/interpretation/knowledge_registry.json` | `KnowledgeLoadError` / HTTP 500 pipeline — no empty/mock registry |
| `knowledge/expert_translation/*.json` | `ExpertTranslationLoadError` |
| Chromium | PDF export `CustomerExportError` / renderer failure; Analyze may still succeed |
| API down | Portal `/healthz` still `ok`; `/backend/*` fails |

## Knowledge copied into the API image

| Tree | Class | Why |
|------|-------|-----|
| `database/` | RUNTIME REQUIRED | Gate-1 rules |
| `knowledge/expert_translation/` | RUNTIME REQUIRED | Narrative translation JSON |
| `knowledge/packages/` | RUNTIME REQUIRED | Luck foundation package + related packages |
| `knowledge/knowledge_catalog/` | RUNTIME REQUIRED (safe copy) | PACK_01 catalog loader path |
| `knowledge/interpretation/` | RUNTIME REQUIRED | Analyze knowledge registry + domain JSON + concepts |
| Remainder of `knowledge/` | DOCUMENTATION / BUILD/TEST | not copied (196 MB mostly authoring/docs) |

Do not modify knowledge content.

## UTF-8 / Vietnamese PDF on Linux

Image installs Noto/Liberation/DejaVu. Report CSS stack remains `"Segoe UI", Arial, "Noto Sans", sans-serif`. Linux smoke generated Dũng/Tuyền PDF (`%PDF-`) and DOCX (zip + Vietnamese glyphs in DOCX text). Naive PDF byte grep is not an authoritative tofu audit (G2-04 `pdf_searchable: false`); DOCX Vietnamese and Hỷ checks passed.
