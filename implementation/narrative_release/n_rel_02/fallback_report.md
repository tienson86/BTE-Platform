# N-REL-02 Fallback Report

CASE-0001 production dual-run. Pack05 remains fallback. No retirement.

Provider: `v2`
Automatic fallback events: 0
Manual rollback events: 0
Fallback count: 0
Overall health: PASS

## Policy

- Automatic fallback: invalid Presentation → Pack05, record event, do not interrupt.
- Manual rollback: `provider=pack05`, no rebuild.
- CASE-0001 production path in this run used Narrative V2 with no fallback.
