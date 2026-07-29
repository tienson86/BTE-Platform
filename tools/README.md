# Engineering tools (WP18)

| Script | Purpose |
|--------|---------|
| `build.py` | Sanity checks + `compileall` |
| `run_tests.py` | Run pytest suites |
| `lint.py` | Syntax, deployment config, optional ruff |
| `package.py` | Create zip artifact |
| `build_release.py` | Release orchestration |
| `package_release.py` | Stable release zip |
| `test_infra.py` | Self-tests for these tools |

Run from repository root:

```bash
python tools/lint.py
python tools/run_tests.py --ci
python tools/package.py --out dist
```
