# Test Plan — PACK-01 Prototype

| Field | Value |
|-------|-------|
| Document | TEST_PLAN |
| Pack | PACK-01 Prototype |
| Version | 1.0.0 |
| Runtime tests now | None — no production code |

---

# 1. Purpose

How a future implementation of this prototype must be tested.

Do not modify existing Golden Dataset expected analysis outputs.

Do not run full-project pytest unless requested.

---

# 2. Fixture

Primary fixture: **CASE-0001 Strength Facts only**, taken from published replay evidence:

`knowledge/pilot/replay/root_cause/strength_calibration/evidence/CASE-0001.json`

`published_contract` is the S0 input.

Do not add Pattern, Useful God, Temperature, or luck to the fixture.

Do not add expert_expected to the selector input.

---

# 3. Assertions (future)

| ID | Assert |
|----|--------|
| T01 | Mapped class = `strong` |
| T02 | Mode B conclusion class matches Mode A matches engine |
| T03 | Drain cause units rejected (`drain_score` 0 / `drain_type` null) |
| T04 | Luck units rejected; Luck section insufficient |
| T05 | Hidden stems listed in Missing Data |
| T06 | Control and support-side both appear in Mode A Evidence and in Why |
| T07 | No Balanced/Weak meaning units in Mode B Meaning |
| T08 | Alternative runner-up is Balanced, not a class flip |
| T09 | Engine confidence 1.0 is recorded as input; interpretation confidence ≠ silent copy of 1.0 |
| T10 | Mode B contains no Rule IDs, scores, `male`, `hot`, dumps, unit IDs |
| T11 | Selected unit list is stable across two runs |
| T12 | Duplicate log drops at least the full-tank synonym from Advantages if Meaning kept it |
| T13 | Executive Summary is 5–8 lines and adds no new cause |
| T14 | `13_EXAMPLES` vignettes are not in Mode B |
| T15 | Temperature / Useful God / Pattern strings are absent from both modes |

---

# 4. Manual review

A reviewer checks CASE-0001 Mode B:

- So What in Meaning
- Why uses only present causes
- Career/Wealth/Marriage/Health are distinct
- No shame, no hype, no invented job title for the subject

---

# 5. Out of scope

- Strength score correctness (Strength Engine tests)
- Expert vs engine discrepancy as a selector input
- PDF export
- Other cases (CASE-0002…) in this prototype pack

---

END
