# G2-01R — ResultStore precedence

## Frozen order

1. **Explicit fresh current analysis** (`bte_last_result` + `bte_current_analysis_id`)
2. **Explicit History selection** (`?from=history&id=<canonical-id>` **and** matching `bte_view_result`)
3. **No result** → empty gate

No implicit legacy/history takeover on normal `/result`.

## Required scenarios

| Action | `/result` shows |
|--------|-----------------|
| Fresh Analyze A | A (current) |
| Open History B with `?from=history&id=B` | B (view only) |
| Normal `/result` (no history query) | current A |
| Fresh Analyze C | current becomes C |
| Refresh | C |
| History selection | does **not** mutate current |

There is no Product Owner “make current” behavior in V1.0.

## API

- `load()` / `loadCurrent()` — current Analyze result only.
- `resolveForDisplay(fromHistory, expectedId)` — History only when **both** `fromHistory` and matching `expectedId`.
- `selectForView()` — writes `bte_view_result` (session) without touching last result.
- `loadForView()` — **EXPLICIT LEGACY ONLY** (`/result?legacy=1` + `result.js`). Normal Desktop `/result` never calls it.
- Fresh `save()` clears the view pointer.

## URL

History open links:

```
/result?from=history&id=<analysis_id>
```

`?from=history` without `id` is **not** an explicit History view. Normal current wins.

If the explicit History id disappears from the URL, `/result` resolves current.

## Isolation

`bte_view_result` must not win on default `/result`. Desktop boot uses `resolveForDisplay`, not `loadForView`.
