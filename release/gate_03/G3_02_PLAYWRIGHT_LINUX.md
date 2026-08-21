# G3-02 — Playwright on Linux

## Requirement

Official PDF must run on Linux using Playwright-managed Chromium. Do not point at a developer Chrome path.

## Frozen install

After `pip install playwright==1.62.0` (via `requirements-prod.txt`):

```
python -m playwright install-deps chromium
python -m playwright install chromium
```

`install-deps` needs root (or a Dockerfile `RUN` as root) and installs OS libraries. Then drop to the `bte` user. `PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright` is set in `Dockerfile.api`.

## This host

Not executed on Linux. Windows proof:

- Playwright 1.62.0
- Chromium cache ≈ **1210 MB** at `%LOCALAPPDATA%\ms-playwright`
- Executable: `chromium-1234\chrome-win64\chrome.exe`
- Dũng/Tuyền PDF generated in-process (`G3_02_SMOKE.json`)

## Concurrency

`PlaywrightPdfBackend.html_to_pdf` launches Chromium, prints, closes in `finally`. Export routes are **sync** FastAPI handlers (Starlette thread pool).

| Topic | Freeze |
|-------|--------|
| Isolation | Unique temp file under `{tempdir}/bte_customer_export/` then delete after download |
| Browser lifecycle | One browser per export; no shared long-lived browser |
| Memory | Extra Chromium process per in-flight PDF (order-of-hundreds MB). Playwright cache on disk ~1.2 GB |
| Expected V1.0 beta concurrency | Low. **Do not** add a job queue. **Do not** raise uvicorn workers to “handle PDF load” |
| Simultaneous PDFs | Possible via thread pool; can stack Chromium processes. Acceptable for beta; not load-tested |

## Fonts

Image packages: `fonts-noto-core`, `fonts-liberation`, `fonts-dejavu-core`. No unlicensed font files are added to the repo. Vietnamese coverage on Linux is expected via Noto Sans; **must be confirmed by generating PDF on Linux**.
