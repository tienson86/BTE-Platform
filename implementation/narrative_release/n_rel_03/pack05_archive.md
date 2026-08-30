# Pack05 Archive

Sprint: N-REL-03

Status: Legacy Narrative Archive

---

## What retirement means

Pack05 is removed from production routing.

Pack05 is not deleted.

Pack05 is not removed from history.

Pack05 is not migrated.

Pack05 is not overwritten.

---

## Storage

```
ResultStore.data.narrative_result        → Pack05 archive (read-only)
ResultStore.data.narrative_v2_shadow     → Narrative V2 production
```

Analyze still dual-stores both layers.

`replaces_pack05` remains `false` on the V2 envelope so the stored Pack05 layer is never replaced.

---

## Access

Production Portal never selects Pack05.

`PACK05_LEGACY` enables read-only archive inspection.

Narrative Studio Compare remains available as historical comparison only.

`ResultStore.loadPack05Archive()` returns the stored Pack05 layer without choosing it for render.

---

## Rollback

Production rollback to Pack05 is removed.

Archive remains.

Release Freeze is not started (N-REL-04).
