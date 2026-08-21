# G3-01 — Clean runtime validation

## Matrix

| Test | Result |
|------|--------|
| Existing frozen Python `pip check` | PASS |
| Clean venv + `requirements-prod.txt` | PASS |
| Clean venv `pip check` | PASS |
| `python -m playwright install chromium` | PASS |
| `GET /health` + `/version` + `/api/v1/health` | PASS |
| Ten control Analyze vs Frozen Truth | **0 diffs** |
| Official PDF Dũng | PASS |
| Official DOCX Dũng (Dụng / Hỷ / Điều hậu / reason) | PASS |
| `npm ci` | PASS |
| `npm run build:result` | PASS |
| Rebuilt `result.js` hash | `114A1761F94FF3EE4B8135F1E3B2D7C88C63D233E17B19B60472730D7DF4ECE5` |

Evidence: `release/gate_03/G3_01_SMOKE.json`.

## Reproducibility hashes

| Artifact | SHA256 |
|----------|--------|
| `G1_PREFINAL_101_TRUTH.json` | `46386BC955119F5DFE9482E7D620767BFB8BB74003A0968A17A6F82017FFA5CC` |
| `applications/customer_portal/package-lock.json` | `EEB6C40C3A0A93953D51DB112C1B36712E828A2A366F6D450032FD4FD1EC8B21` |
| `requirements-prod.txt` | `5E8C458B663345829EF355C393171D1AB10899B416FE97A128B24F161C829B84` |
| `constraints-v1.0.txt` | `1646630123E77D6A3CF511B8A198A44C34E9EA871737FF3DFF3A5188A65479D5` |
| Portal `result.js` (post-G2 / G3-01 rebuild) | `114A1761F94FF3EE4B8135F1E3B2D7C88C63D233E17B19B60472730D7DF4ECE5` |

## Network

After install, Analyze / calendar / engines are **local**. No required SaaS. Build-time needs PyPI + npm registry. Playwright downloads Chromium once.

External runtime services for V1.0 customer Analyze: **NONE**.

## Windows → Linux

No `C:\` or drive-letter paths in production application code. Temp exports use `tempfile.gettempdir()`. Case-sensitive Linux must preserve repository filename case. Playwright on Linux needs distro libraries (G3-02). Python 3.12 images are **not** this freeze’s proven interpreter.
