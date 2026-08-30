# N-REL-01 Rollback Test

Rollback requirement: `provider=pack05` only.

No rebuild. No migration. No data loss.

---

## Mechanism

Set any one of:

- Env: `NARRATIVE_PROVIDER=pack05` then restart Portal process
- Boot: `window.__BTE_NARRATIVE_PROVIDER__ = "pack05"`
- Query (drill / emergency): `/result?provider=pack05`

Query wins so a live session can roll back without a rebuild.

---

## CASE-0001 procedure

1. Analyze CASE-0001 once. ResultStore keeps Pack05 and Narrative V2.
2. Open `/result?provider=pack05`. Production dashboard renders Pack05.
3. Open `/result?provider=v2`. Same dashboard renders NarrativeV2Presentation.
4. Open `/result?provider=pack05` again. Pack05 returns. Stored V2 remains.

---

## Pass criteria

| Check | Result |
|-------|--------|
| Pack05 production succeeds | PASS |
| V2 production succeeds | PASS |
| Rollback Pack05 succeeds | PASS |
| ResultStore still has `narrative_result` | PASS |
| ResultStore still has `narrative_v2_shadow` | PASS |
| Customer is not shown errors / JSON / traces | PASS |
| Dashboard geometry unchanged | PASS |

---

## Failure fallback (automatic)

If provider is `v2` or `auto` and Presentation is invalid, Portal renders Pack05, records `fallback_count`, and does not interrupt the customer.

That is not a rollback. Rollback is an explicit `provider=pack05` decision.
