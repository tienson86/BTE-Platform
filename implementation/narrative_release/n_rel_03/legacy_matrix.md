# N-REL-03 Legacy Matrix

Pack05 is retired from production routing.

Retirement ≠ deletion.

---

## Production

| Surface | Provider | Pack05 selectable |
|---------|----------|:-----------------:|
| Customer Portal `/result` | Narrative V2 | No |
| `NARRATIVE_PROVIDER` | ignored; always `v2` | No |
| `?provider=pack05` | ignored; always `v2` | No |
| `?provider=auto` | ignored; always `v2` | No |
| Production rollback | removed | No |
| New Narrative PDF / DOCX / JSON | Narrative V2 Presentation | No |

---

## Archive

| Surface | Mode | Writable |
|---------|------|:--------:|
| ResultStore `data.narrative_result` | Historical Pack05 | No |
| `PACK05_LEGACY` | Read-only archive access | No |
| Narrative Studio Compare | Historical Pack05 vs V2 | No |
| Official Report Engine PDF / DOCX | Analytical report archive path | No overwrite |

---

## Flags

| Flag | Production meaning |
|------|--------------------|
| `NARRATIVE_PROVIDER=pack05` | Ignored. Production stays V2. |
| `NARRATIVE_PROVIDER=auto` | Ignored. Production stays V2. |
| `NARRATIVE_PROVIDER=v2` | Production. |
| `PACK05_LEGACY=pack05` | Read-only archive. Not a production switch. |

---

## Resolution

```
Requested pack05 / auto / invalid
        ↓
Production provider = v2
```

Pack05 remains in storage.

Pack05 remains in Studio comparison.

Pack05 cannot enter production Portal or new Narrative exports.
