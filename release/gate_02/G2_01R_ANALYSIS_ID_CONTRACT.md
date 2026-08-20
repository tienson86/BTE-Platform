# G2-01R — Analysis identity contract

## Canonical customer analysis ID

**Canonical ID = HTTP Analyze `request_id`.**

On successful `POST /api/v1/analyze` the API copies that value onto the payload:

| Field | Value |
|-------|--------|
| envelope `request_id` | server request id |
| `data.analysis_id` | same |
| `data.request_id` | same |
| `data.result_meta.analysis_id` | same |

Portal ResultStore persists the same string on:

- envelope `analysis_id` (save argument)
- `data.analysis_id`
- `bte_current_analysis_id`
- History row `id` / `analysis_id`

`/result`, Luận giải, Báo cáo, Print HTML, and Export composer all read that ID from the **currently selected structured blob**. They do not invent a second customer identity.

## Distinct ids

| Id | Role |
|----|------|
| `request_id` / `analysis_id` | **Canonical customer result identity** (same value after Analyze) |
| History row `id` | Same canonical id for new saves |
| Storage keys (`bte_last_result`, …) | Persistence keys, never shown as analysis id |

Orchestrator `analyze()` itself does not mint a customer id (identity is an HTTP Analyze concern). Direct engine calls may still have `analysis_id: null`. That is not a Frozen Truth mismatch.

## Frontend rule

If `data.analysis_id` or `data.request_id` or envelope `request_id` exists, **do not** generate `bte-{birth}-{timestamp}`.

Synthetic `bte-…` remains only as a last-resort display id when no server id exists (pre-G2 stored blobs). New Analyze always has a server id.

## Surfaces

```
Analyze API  →  ResultStore current  →  /result
                                  →  /interpretation (same blob)
                                  →  /reports composer
                                  →  Print HTML (selected blob)
                                  →  History snapshot (copy of blob + metadata)
```

One structured blob is sufficient. No second analytical lookup.
