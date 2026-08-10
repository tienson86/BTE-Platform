# Incident Response

Version: 1.0.0  
Sprint: Beta-3

## Flow

```
Detect → Triage → Mitigate → Recover → Review
```

1. **Detect** — health, logs, user report, backup job.
2. **Triage** — SEV, blast radius (API vs portal vs edge vs storage).
3. **Mitigate** — restart, rollback, disk, maintenance 503. No engine edits.
4. **Recover** — smoke probes; exit maintenance.
5. **Review** — timeline, Request-IDs, error-budget minutes, follow-ups.

## Communication

- Internal: ops channel with SEV and next update time.
- External: maintenance or incident note; no stack traces or paths.

## Roles

See `ONCALL_GUIDE.md`.

---

END
