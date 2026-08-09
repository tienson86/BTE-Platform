# Backup Strategy

Version: 1.0.0  
Sprint: Beta-1

---

## What to back up

| Set | Path / volume | Cadence |
|-----|---------------|---------|
| Application data | `bte-data` / `applications/data` | Daily |
| Reports | `bte-reports` | Daily |
| Configuration templates | `deployment/docker/*.example`, nginx | On change + weekly |
| Knowledge (read-only product tree) | `engines/*/knowledge`, `knowledge/` | On release tag (immutable copy) |
| Secrets | **secret manager only** — not disk backup into git | Per org policy |

Logs: optional 7-day copy; not a restore source of truth.

---

## Method

Use `deployment/backup/backup.sh` to create a timestamped archive:

- `data/`  
- `reports/`  
- `config/` (compose + nginx + env **examples** only)  
- `knowledge-manifest.txt` (git SHA + tree list)

---

## Retention

See [backup/backup_policy.md](./backup/backup_policy.md).

---

## Verification

Restore to a scratch directory monthly (`restore.sh --verify`). Confirm file counts and SHA256 of archive.

---

END
