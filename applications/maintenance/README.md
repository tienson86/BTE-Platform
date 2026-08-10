# Maintenance

Version: 1.0.0  
Sprint: Beta-3

Contracts only. Do not flip nginx, do not SIGTERM services from this package.

| Mode | Traffic | Writes |
|------|---------|--------|
| `normal` | yes | yes |
| `maintenance` | no (edge 503) | no |
| `read_only` | yes | no |
| `drain` | no new | no |
| `startup` | after ready | after ready |
| `shutdown` | draining | no |

See `applications/runbooks/MAINTENANCE_WINDOW.md`.

---

END
