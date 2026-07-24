# Release Process

## Overview

```text
prepare VERSION
    ↓
python tools/build_release.py --version X.Y.Z
    ↓
python tools/package_release.py --version X.Y.Z
    ↓
git tag vX.Y.Z && git push origin vX.Y.Z
    ↓
GitHub Actions release.yml publishes zip
```

## Local release build

1. Ensure a clean working tree (or only intentional release edits).
2. Choose the next semantic version (see [VERSIONING.md](VERSIONING.md)).
3. Run:

```bash
python tools/build_release.py --version 1.0.1
python tools/package_release.py --version 1.0.1 --out dist
```

Artifacts:

- `dist/bte-platform-1.0.1-YYYYMMDD.zip` (timestamped)
- `dist/bte-platform-1.0.1.zip` (stable name)

## GitHub release (tag)

```bash
git add VERSION
git commit -m "chore: release v1.0.1"
git tag v1.0.1
git push origin HEAD
git push origin v1.0.1
```

Pushing `v*.*.*` tags triggers `.github/workflows/release.yml`, which:

1. Installs dependencies
2. Lints and runs CI tests
3. Builds and packages zip artifacts
4. Creates a GitHub Release with the zip attached

You can also run **Release** via `workflow_dispatch` and pass a version input.

## Checklist

- [ ] `python tools/lint.py` passes
- [ ] `python tools/run_tests.py --ci` passes
- [ ] Deployment docs still accurate (`deployment/docs/`)
- [ ] Release notes drafted under `docs/release_notes/` when meaningful
- [ ] No accidental changes to golden datasets / snapshots

## Hotfix

1. Branch from the release tag.
2. Apply the minimal patch.
3. Bump PATCH version.
4. Follow the same build → tag → push flow.
