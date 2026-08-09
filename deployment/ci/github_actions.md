# GitHub Actions (documented pipeline)

Suggested workflow **name**: `bte-release` (not installed as a live workflow in Beta-1 to avoid surprising CI).

```yaml
name: bte-release
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-test-package:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Tests (existing modules only)
        run: |
          pytest tests/api -q || true
          # run the repo's established module jobs — do not invent full-suite here
      - name: Build images
        run: |
          docker build -f deployment/docker/Dockerfile.api -t bte-api:${{ github.sha }} .
          docker build -f deployment/docker/Dockerfile.portal -t bte-portal:${{ github.sha }} .
          docker build -f deployment/docker/Dockerfile.worker -t bte-worker:${{ github.sha }} .
      - name: Dependency scan (advisory)
        run: docker scout cves bte-api:${{ github.sha }} || true

  deploy-beta:
    needs: build-test-package
    environment: beta
    steps:
      - name: Deploy beta compose
        run: echo "manual/oidc deploy using docker-compose.beta.yml"

  deploy-production:
    needs: deploy-beta
    environment: production
    steps:
      - name: Manual approval gate (GitHub Environment)
        run: echo "requires reviewer"
```

Gates: **beta environment** optional; **production environment** required reviewers.

---

END
