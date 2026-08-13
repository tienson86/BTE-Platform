# BETA_USERS

| Field | Value |
|-------|-------|
| Slots | **10** |
| Id | `BU-nn` |
| PII | Offline only — never commit names, phones, emails |

One slot = one persona = one chart = one form.

---

## Slots

| Slot | Persona | Reader | Chart | Bind | Invite | Form |
|------|---------|--------|-------|------|--------|------|
| **BU-01** | P01 Over-carrier | SELF | CASE_0001 | **Bound** (Frozen Golden replay) | **READY** | empty |
| **BU-02** | P02 Output Maker | SELF | CASE_0002 | **Bound** | **READY** | empty |
| **BU-03** | P03 Caregiver Parent | PARENT | CASE_0003 | **Bound** | **READY** | empty |
| **BU-04** | P04 Conserving Adult | SELF | Discovery Pilot CASE-0006 | **Reserved** — not Golden CASE_0004 | QUEUED | empty |
| **BU-05** | P05 Special-structure | SELF | CASE_0005 | **Unbound** | BLOCKED | — |
| **BU-06** | P06 Tension Holder | SELF | CASE_0006 | **Unbound** | BLOCKED | — |
| **BU-07** | P07 Founder | SELF | CASE_0007 | **Unbound** | BLOCKED | — |
| **BU-08** | P08 Relationship | SELF | CASE_0008 | **Unbound** | BLOCKED | — |
| **BU-09** | P09 Honesty Skeptic | SELF / CONSULTANT | CASE_0009 | **Unbound** | BLOCKED | — |
| **BU-10** | P10 Rhythm / Resource | SELF | CASE_0010 | **Unbound** | BLOCKED | — |

Participant id lives in the offline invite list. Git keeps `BU-nn` only.

---

## Status legend

| Status | Meaning |
|--------|---------|
| READY | Chart bound · production path runnable · may invite |
| QUEUED | Chart exists offline / discovery; Product confirms invite; Golden slot still placeholder |
| BLOCKED | No real chart bind — PB-009 · do not invent |

---

## Bind rules (unchanged)

From `../RC3/CASE_SELECTION.md`:

1. Product picks an anonymized **real** chart matching the persona.
2. Birth input stays offline; this file stays label-only.
3. If live signals do not match the persona, **reclassify** — do not force.
4. Child charts use PARENT delivery. Do not bind a child to P07–P10.
5. CASE_0001 remains Frozen Golden. BU-01 **replays** it; do not edit Golden artifacts.
6. BU-04 must not be treated as a Golden CASE_0004 bind.

Discovery pilots for P05/P06 exist under `../DISCOVERY/` as **lab lenses only**. They are not execution binds until Product writes them into CASE_SELECTION.

---

## Cohort fill order

```text
Wave 1 (soft launch)   BU-01 · BU-02 · BU-03
Wave 2 (after confirm) BU-04
Wave 3 (after binds)   BU-05 … BU-10
```

Do not skip to Wave 3 by inventing charts.

---

END
