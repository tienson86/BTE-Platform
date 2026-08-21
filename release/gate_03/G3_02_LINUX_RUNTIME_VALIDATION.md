# G3-02 — Linux runtime validation

## Result on this freeze host

**NOT EXECUTED** — no Docker engine, no WSL distro, no Linux Python.

Windows supporting evidence (not a Linux substitute):

| Check | Result |
|-------|--------|
| CPython | 3.14.6 |
| Ten control cases | 0 diffs |
| Dũng PDF/DOCX | `%PDF-` 174266 bytes; DOCX zip 39414; Hỷ string present |
| Tuyền PDF/DOCX | `%PDF-` 171708 bytes; DOCX zip 39497; Hỷ string present |
| `ZoneInfo("Asia/Ho_Chi_Minh")` | available (`tzdata` 2026.3) |
| API process restart | Dũng Dụng unchanged (`G3_02_RESTART.json`) |
| Host locale | Windows `cp1252` (application uses UTF-8 in JSON/files; do not depend on locale for Calendar) |

Evidence: `release/gate_03/G3_02_SMOKE.json`.

## Required Linux environment

| Item | Freeze |
|------|--------|
| OS | Debian via `python:3.14.6-slim` **or** Ubuntu 24.04 host with 3.14.6 in a venv/container |
| Locale | `C.UTF-8` or `en_US.UTF-8` (`LANG`/`LC_ALL`) |
| Timezone database | OS `tzdata` **and/or** PyPI `tzdata==2026.3` |
| Application timezone | `Asia/Ho_Chi_Minh` (Calendar input / API `default_timezone`). Server OS may stay **UTC**. |
| Fonts | `fonts-noto-core` + `fonts-liberation` + `fonts-dejavu-core` (no proprietary fonts shipped) |
| Chromium | `python -m playwright install chromium` after OS deps (`playwright install-deps chromium`) |
| Layout | repo root: `engines/`, `applications/`, `database/`, `knowledge/expert_translation`, `knowledge/packages`, `knowledge/knowledge_catalog` |

## Command to run when Docker exists

```
docker compose -f deployment/docker/docker-compose.g3-02-smoke.yml up --build
```

Then from a checkout that includes `release/gate_03/_g3_02_linux_smoke.py` (bind-mount recommended):

```
python -m pip check
python release/gate_03/_g3_02_linux_smoke.py
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
| Remainder of `knowledge/` | DOCUMENTATION / BUILD/TEST | not copied (196 MB mostly authoring/docs) |

Do not modify knowledge content.

## UTF-8 / Vietnamese PDF on Linux

Not empirically verified here. Image installs Noto/Liberation/DejaVu. Report CSS stack remains `"Segoe UI", Arial, "Noto Sans", sans-serif`. Linux should resolve Noto. Tofu check must be done by generating Dũng/Tuyền PDF **on Linux** and inspecting glyphs (naive PDF byte grep is not authoritative; G2-04 `pdf_searchable: false`).
