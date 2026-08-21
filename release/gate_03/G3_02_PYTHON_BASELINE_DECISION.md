# G3-02 — Python baseline decision

## Decision

**PRODUCTION PYTHON: CPython 3.14.6**

Do not leave this ambiguous. Do not use Ubuntu’s default 3.12 as the V1.0 interpreter until a Linux 3.12 ten-case probe is 0 diffs **and** a later gate explicitly re-freezes.

## Why 3.14.6

| Interpreter | Frozen Truth reproduced? | Notes |
|-------------|--------------------------|-------|
| CPython **3.14.6** Windows | **Yes** (Gate 1, Gate 2, G3-01, G3-02 smoke) | Canonical |
| CPython **3.12** Linux (CI/old Docker) | **No** — not run | Previous Dockerfiles used `python:3.12-slim` |
| CPython **3.13** Windows (present on host) | Not used | Not a freeze candidate |

G3-01 `constraints-v1.0.txt` was generated on **Windows 3.14.6**. It pins package **versions**, not wheel filenames. Linux 3.14.6 should install with:

```
python -m pip install -r requirements-prod.txt -c constraints-v1.0.txt
python -m playwright install chromium
```

Do not assume `constraints-v1.0.txt` on 3.12 (platform extras such as `colorama` are harmless; `pydantic-core` / `greenlet` / `numpy` wheels are ABI-specific).

## Python 3.12 installability (not approval)

`pandas==3.0.5` `Requires-Python: >=3.11` and publishes `cp312` `manylinux_2_28` wheels.

`playwright==1.62.0` publishes `py3-none-manylinux1_x86_64` (and aarch64 manylinux2014). Native Linux `pip install` can mix those tags. A single `pip download --platform manylinux_2_28` **cannot** pull Playwright; that is a pip tag limitation, not proof that 3.12 cannot install.

**Installable ≠ Frozen Truth.** G3-02 does not approve 3.12.

If a future Linux 3.12 probe is 0 diffs, a later gate may re-decide. This gate does **not** rewrite engines to make 3.12 work.

## Other frozen tool versions (from G3-01)

| Tool | Version |
|------|---------|
| Node (build-time) | v24.18.0 |
| npm | 11.16.0 |
| Playwright (Python) | 1.62.0 |
| Chromium | Playwright-managed (this host: `chromium-1234`) |
| python-docx | 1.2.0 |
| FastAPI | 0.140.1 |
| uvicorn | 0.52.1 |

OS baseline for the smoke image: **Debian** (`python:3.14.6-slim`). DigitalOcean Ubuntu 24.04 remains a valid **host** if processes run in that image/compose, so host Python 3.12 is unused.
