# Rotation policy

| Stream | Rotate | Keep |
|--------|--------|------|
| Application | daily / 50 MB | 14 days |
| Nginx access | daily | 30 days |
| Nginx error | daily | 30 days |
| Audit (if split) | daily | 90 days |

Host: `logrotate` example:

```
/var/lib/docker/volumes/bte-*_bte-logs/_data/*.log {
    daily
    rotate 14
    missingok
    compress
    delaycompress
    notifempty
    copytruncate
}
```

Never rotate into git. Never persist JWT or passwords.

---

END
