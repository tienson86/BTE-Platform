# N-REL-01 Provider Matrix

Release flag: `NARRATIVE_PROVIDER`

Allowed values: `pack05` | `v2` | `auto`

Default for this release: `v2`

Rollback: `pack05` (no rebuild, no migration, no data loss)

---

## Resolution order

1. Query `?provider=`
2. Portal boot `window.__BTE_NARRATIVE_PROVIDER__` (from env)
3. Env `NARRATIVE_PROVIDER` / `VITE_NARRATIVE_PROVIDER`
4. Default `v2`

Invalid values resolve to `v2`.

---

## Matrix

| Requested | V2 Presentation | Rendered | Fallback event | Customer impact |
|-----------|-----------------|----------|----------------|-----------------|
| `pack05` | present or missing | Pack05 | no | none |
| `v2` | valid `bte.presentation.v2.1` | Narrative V2 | no | V2 copy on existing cards |
| `v2` | missing / invalid / error | Pack05 | yes | none (silent fallback) |
| `auto` | valid `bte.presentation.v2.1` | Narrative V2 | no | V2 copy on existing cards |
| `auto` | missing / invalid / error | Pack05 | yes | none (silent fallback) |

---

## What switches

Portal Overview / Interpretation / Action Plan cards.

Identity, Tứ Trụ, Ngũ Hành, Thập Thần, Mệnh Cục, Thần Sát, Đại Vận stay canonical.

Dashboard layout, cards, and PDF are not redesigned.

---

## What does not switch

| Layer | Behavior |
|-------|----------|
| Analyze pipeline | Unchanged |
| Pack05 NarrativeResult | Always stored |
| Narrative V2 runtime | Always attached beside Pack05 |
| ResultStore | Both layers preserved independently |
| PDF / DOCX | Out of scope (still Pack05 consumer) |
| Pack05 retirement | Not started |
| Freeze | Not started |

---

## Storage vs render

```
ResultStore.data.narrative_result          → Pack05
ResultStore.data.narrative_v2_shadow       → NarrativeV2Presentation
NARRATIVE_PROVIDER                         → which Presentation Portal renders
```

Switch never overwrites either stored layer.
