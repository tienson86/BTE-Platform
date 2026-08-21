# G3-02 — Resource baseline

Approximate. Not a benchmark suite. Linux RSS was not measured.

## Time (this host, CPython 3.14.6, TestClient)

| Work | Observation |
|------|----------------|
| Analyze (ten-case, after first) | ~0.33–0.45 s; first Sơn ~0.85 s |
| Official PDF (Playwright) | ~2.5–5 s wall (Dũng/Tuyền in G3-02 smoke) |
| Official DOCX | ~0.2 s after PDF in the same run |

Reverse-proxy timeout: allow **≥ 60 s**, prefer **120 s** to match Portal `/backend` httpx timeout. Do not add an application timeout that cuts PDF short.

## Memory

| Process | Windows working set (this host) |
|---------|----------------------------------|
| API idle (uvicorn, port 18001) | **~125 MB** |
| Portal idle | not sampled; FastAPI static is expected smaller than API+engines |
| During PDF | + Chromium process (not sampled; typically hundreds of MB) |

## Disk (this checkout / machine)

| Tree | Size |
|------|------|
| `database/` | ~0.6 MB |
| `knowledge/` entire | ~196 MB (mostly docs; do not copy all) |
| `knowledge/packages/` | ~38 MB |
| `knowledge/knowledge_catalog/` | ~0.6 MB |
| Portal `static/dist/` | ~1.8 MB |
| Playwright Chromium cache | **~1.2 GB** |
| `applications/customer_portal/node_modules` | ~85 MB (**build-time**, not in runtime image) |

Temp exports: `{tempdir}/bte_customer_export/` — deleted after download. Do not rely on them after restart.

## CPU

Analyze is short bursts (~0.4 s). PDF is Chromium print-to-PDF (~few seconds). No exhaustive profiling.

## Write paths

Production should be read-only on:

- `engines/`
- `database/`
- `knowledge/`
- application source / static dist

Writable:

- `{tempdir}/bte_customer_export/`
- `logs/` if file logging is configured later
- `applications/data` (`BTE_DATA_DIR`) for WP11 JSON if used — **not** customer History

## Non-root

API/Portal images run as system user `bte`. Chromium is installed to `/opt/ms-playwright` and owned by `bte`. Do not require root for request handling.

## Server sizing (informal)

A 2 GB DigitalOcean droplet is a plausible **beta** starting point (API + Portal + Chromium headroom). Confirm after Linux RSS. 1 GB is likely tight during PDF.
