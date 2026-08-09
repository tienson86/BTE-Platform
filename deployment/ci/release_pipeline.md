# Release pipeline

```
Build images
    ↓
Test (existing module CI)
    ↓
Package + tag (git SHA)
    ↓
Deploy Beta (compose.beta)
    ↓
Smoke /health /version /healthz
    ↓
Manual approval
    ↓
Deploy Production (compose.production)
    ↓
Smoke + monitor 30m
    ↓
Rollback tag if fail
```

See [../RELEASE_PLAYBOOK.md](../RELEASE_PLAYBOOK.md).

---

END
