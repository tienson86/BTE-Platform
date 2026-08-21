# G3-02L-R1 — Linux container runtime knowledge packaging repair

## Status

**G3-02: PRODUCTION PROCESS MODEL FROZEN — READY FOR G3-03**

Packaging defect only. Gate-1 / Gate-2 analytical semantics unchanged. G3-03 not started.

## Root cause

`deployment/docker/Dockerfile.api` copied a knowledge subset:

- `knowledge/expert_translation`
- `knowledge/packages`
- `knowledge/knowledge_catalog`

It did **not** copy `knowledge/interpretation`. Analyze loads that tree via `__file__`-relative repo root and hard-fails when the registry is missing. No loader fallback was added (and must not be added).

## Missing path

Container: `/app/knowledge/interpretation/knowledge_registry.json`

Exception: `KnowledgeLoadError: missing registry: /app/knowledge/interpretation/knowledge_registry.json`

## Source path (host / frozen tree)

| Field | Value |
|-------|--------|
| Path | `knowledge/interpretation/knowledge_registry.json` |
| Size | 842 bytes |
| SHA256 | `1307A4068CFA4CB373642589225992CEC9CD1797E924036BD28EA5D07393F537` |
| Git | tracked (`git ls-files`); working tree clean before this repair |

Source existed. Nothing was invented.

## Runtime load (unchanged)

| Item | Value |
|------|--------|
| Loader | `engines.interpretation_engine.foundation.knowledge.loader.JsonKnowledgeLoader` |
| Registry | `KnowledgeRegistry.default()` → `DEFAULT_KNOWLEDGE_ROOT` |
| Path construction | `Path(__file__).resolve().parents[4] / "knowledge" / "interpretation"` then `knowledge_registry.json` |
| Working-directory assumption | none — `__file__` relative to repo root (`/app` in the image) |
| Concepts | `ConceptRegistry.default()` → `knowledge/interpretation/concepts` + `concept_registry.json` |

Loader semantics were not changed.

## Registry dependency closure

`knowledge_registry.json` `sources` (JSON only):

| Domain | Relative path | Host JSON count | Class |
|--------|---------------|-----------------|--------|
| UsefulGod | `domains/useful_god` | 20 | RUNTIME REQUIRED |
| Strength | `domains/strength` | 3 | RUNTIME REQUIRED |
| Pattern | `domains/pattern` | 26 | RUNTIME REQUIRED |
| TenGods | `domains/ten_gods` | 11 | RUNTIME REQUIRED |
| ShenSha | `domains/shensha` | 12 | RUNTIME REQUIRED |

`concept_registry.json` `sources` (Analyze narrative retrieval):

| Category | Relative path | Class |
|----------|---------------|--------|
| core | `concepts/core` (27 JSON) | RUNTIME REQUIRED |
| symbolic | `concepts/symbolic` | RUNTIME REQUIRED (empty `.gitkeep` today) |
| application | `concepts/application` | RUNTIME REQUIRED (empty `.gitkeep` today) |

Also already in the image (unchanged):

| Tree | Class |
|------|--------|
| `database/` | RUNTIME REQUIRED |
| `knowledge/expert_translation/` | RUNTIME REQUIRED |
| `knowledge/packages/` | RUNTIME REQUIRED |
| `knowledge/knowledge_catalog/` | RUNTIME REQUIRED (safe copy) |

Not copied (authoring / docs, ~196 MB remainder of `knowledge/`):

`01_DESKTOP`, `authoring`, `ui_reference`, numbered knowledge books, `golden_dataset`, etc.

Those are **NOT REQUIRED FOR V1.0 RUNTIME**. The full `knowledge/interpretation` tree (~386 KB) was copied rather than a brittle JSON-only subset.

## Docker build context

From `deployment/docker/docker-compose.g3-02-smoke.yml`:

| Service | `build.context` | `dockerfile` |
|---------|-----------------|--------------|
| api | `../..` (repository root) | `deployment/docker/Dockerfile.api` |
| portal | `../..` (repository root) | `deployment/docker/Dockerfile.portal` |

`knowledge/` and `database/` are inside the context. A COPY of `knowledge/interpretation` is valid.

## .dockerignore

`deployment/docker/.dockerignore` does **not** exclude `knowledge/`, `database/`, JSON, or CSV. `*.md` is excluded except `knowledge/**/*.md`. No root `.dockerignore`. No ignore-list repair required.

## Files added to the image

```
COPY knowledge/interpretation /app/knowledge/interpretation
```

Repo-relative structure preserved. No second knowledge location. No flatten.

Compose smoke bind-mount of `release/` was changed from `:ro` to read-write so `_g3_02_linux_smoke.py` can write `G3_02_SMOKE.json`.

## Container verification

```
-rwxr-xr-x 1 root root 842 Aug 15 10:03 /app/knowledge/interpretation/knowledge_registry.json
```

One-time audit (`release/gate_03/_g3_02l_r1_runtime_audit.py`) against `G3_01_RUNTIME_DATA_MANIFEST.md`:

`missing_count=0`

Present: `/app/database`, `/app/knowledge`, `/app/knowledge/interpretation`, registry + concepts, all five domain dirs, expert translation, luck package, calendar data + solar terms, hidden stems, temperature, strength, useful god, pattern, score, shensha, origin/relation CSVs, commercial knowledge CSVs, interpretation rules, report V1 templates, portal templates/static, `applications/data`.

No remaining missing G3-01 runtime paths.

## Health

| Endpoint | Result |
|----------|--------|
| `GET /health` | PASS `{"status":"ok"}` |
| `GET /version` | PASS `api_version=1.0.0` |
| `GET /api/v1/health` | PASS |
| Portal `GET /healthz` | PASS |

## Analyze

One known case first: **Ngô Đắc Dũng** `POST /api/v1/analyze` → **HTTP 200**. No missing-registry exception.

## 10-case result

Evidence: `release/gate_03/G3_02_SMOKE.json`

| Check | Result |
|-------|--------|
| `runtime.system` | Linux |
| Python | 3.14.6 |
| `mismatch_count` | 0 |
| 10/10 control cases | PASS (MATCH) |

## PDF / DOCX (Linux Playwright Chromium)

| Case | PDF | DOCX |
|------|-----|------|
| Ngô Đắc Dũng | `%PDF-` 149551 bytes | zip 40788; Hỷ string; Vietnamese Đ/ă/â |
| Vũ Thị Thanh Tuyền | `%PDF-` 146972 bytes | zip 40859; Hỷ string; Vietnamese Đ/ă/â |

`PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright`. Smoke `pass: true`.

## Remaining blockers

None for G3-02 Linux process/runtime packaging.

Do not start G3-03 from this repair automatically.

## Diff policy

| Class | Count |
|-------|--------|
| Analytical engine/rule semantic changes | 0 |
| Gate-2 customer semantic changes | 0 |
| Allowed packaging / G3 docs / smoke | Dockerfile.api COPY; compose release mount; G3_01 manifest row; smoke facts; this report |
