# RELEASE_BOARD

| Field | Value |
|-------|-------|
| Release authority | `knowledge/quality/` **FROZEN** — do not edit from here |
| This board | Product view for backlog sequencing |

---

## Gates

```text
RC0 → RC1 → RC2 → RC3 (discovery) → Commercial V1 → Commercial V1.1
```

| Gate | Quality Gate file (frozen 2026-08-13) | Product evidence (do not patch the gate file) |
|------|----------------------------------------|-----------------------------------------------|
| RC0 | MET | Governance exists |
| RC1 | MET | CASE_0001 Frozen 8.0 |
| RC2 | File still lists NOT MET (0002 ~6.7, 0003 decision open) | EPIC-A 0002 **8.0** · EPIC-B 0003 packaging **live** · Product declared RC2 PASS |
| RC3 | Not a Quality Gate id | Internal beta **soft-ready** · P04/P06 below floor · 7 charts unbound |
| Commercial V1 | NOT MET | Adult 0001+0002 lab MET · live-beta 0 · P04/P06 not ship-set |
| Commercial V1.1 | NOT MET | Child packaging live · ISS-C3-001 open · binds incomplete |

**Rule:** Frozen Quality Gate documents stay as written. Product uses EPIC + analytics evidence to sequence **PB-*** only.

---

## What each gate still needs from *this* backlog

| Gate | Backlog relevance |
|------|-------------------|
| RC2 | Lab scores already at floor post-EPIC — no PB to “unfreeze engines” |
| RC3 | PB-008 live forms · PB-009 binds · PB-001/003 to lift discovery floors |
| Commercial V1 | Ship-set 0001+0002 · S0=0 · Product sign-off · PB-010 packaging |
| Commercial V1.1 | PB-006 · PB-007 · PB-012 deferred Knowledge · child SKU list |

---

## Case readiness (product analytics)

| Case | Product view | Backlog |
|------|----------------|---------|
| 0001 | Golden 8.0 · regress always | PB-010 |
| 0002 | Lab 8.0 OUTPUT | Protect in PB-002 |
| 0003 | Parent 7.5 · Career hidden | PB-006 · PB-007 |
| 0004–0010 Golden | Placeholders | PB-009 (bind, don’t invent) |

---

END
