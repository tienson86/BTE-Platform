# G3-01 — Refreeze checklist

Use before G3-02. Do not unfreeze Gate-1/Gate-2 to “fix” packaging.

## Confirm

- [x] Gate-1 Frozen Truth hash intact
- [x] Gate-2 customer semantics intact
- [x] Python version recorded (3.14.6 proven)
- [x] `requirements-prod.txt` + `constraints-v1.0.txt` identified
- [x] `pip check` acceptable
- [x] Node/npm recorded
- [x] `npm ci` + `build:result` succeed
- [x] Playwright/Chromium documented
- [x] DOCX runtime documented (python-docx, no local template)
- [x] Runtime data inventoried
- [x] No blocking developer `C:\` path in app code
- [x] Environment variables inventoried; `.env.example` placeholders
- [x] No committed production secret
- [x] Backend startup without `--reload`
- [x] Portal FastAPI static serving documented
- [x] UTF-8 / timezone documented
- [x] Filesystem writes documented
- [x] Clean Python runtime starts; health/version pass
- [x] Clean Analyze matches Frozen Truth
- [x] Clean PDF/DOCX pass
- [x] Ten cases 0 analytical diffs
- [x] 0 analytical semantic source changes
- [x] 0 Gate-2 customer semantic source changes

## Must not

- [ ] Upgrade libraries for convenience
- [ ] Rewrite engines or Result UI
- [ ] Treat Docker 3.12 image completeness as already done
- [ ] Start G3-02 from this checklist automatically
