# RELEASE_POLICY

| Field | Value |
|-------|-------|
| Document | RELEASE_POLICY |
| System | Quality Gate System V1.0 |
| Status | **FROZEN** |
| Date | 2026-08-13 |

---

## SECTION 6 — Pass policy

**No release without all mandatory gates.**

```text
Mandatory gates for the target version
        ALL GREEN
            ↓
     Product sign-off
            ↓
      Release allowed
```

If any mandatory gate is amber or red, the version **does not advance**. Partial progress is not a pass.

---

## Mandatory vs evidence

| Class | Meaning |
|-------|---------|
| Mandatory gate | Blocks the named version |
| Evidence | QC1–QC4, engine tests, UI sprints, consulting scorecards — necessary inputs, never sufficient |

Engineering green + UI complete + Knowledge QC high **cannot** pass RC2 or Commercial V1.

---

## What “all mandatory gates” means per version

| Version | Mandatory set |
|---------|----------------|
| RC0 | System files present; policy frozen |
| RC1 | Q1 · Golden lab · CASE_0001 Frozen PASS · this system active |
| RC2 | Q2 · CASE_0002 floors · CASE_0001 regression PASS · 0003 decision · S0 = 0 |
| Commercial V1 | RC2 · adult ship-set floors · unwaived S1 = 0 on ship set · SKU excludes minors unless Q3 · Product sign-off |
| Commercial V1.1 | Commercial V1 · Q3 · 0003 S1/policy · coverage bind/defer · Product sign-off |

Checklists: [RC_CHECKLIST.md](RC_CHECKLIST.md).

---

## Hard fails (any version)

Any one fails the version regardless of averages:

1. Frozen Golden regression FAIL
2. Open S0 on the version’s ship set
3. Invented chart facts or reversed Dụng thần without evidence
4. Ethics breach (shame, medical diagnosis, guaranteed outcomes)
5. Child / weak SKU shipped with adult Career body (Context FAIL)
6. Lowering floors or editing Golden expected output to pass
7. Case-id special-case in production orchestrator

---

## Waivers

| Item | Allowed | Authority |
|------|---------|-----------|
| S3 polish deferred | Yes | Validation Owner + note |
| S2 deferred to next version | Yes, listed on backlog | Product |
| S1 | Written waiver + expiry only | Product |
| S0 | Never | — |
| Golden FAIL | Never | — |
| Skip a release stage | Never | — |

Expired waiver = gate FAIL.

---

## Scope cuts

A version may **exclude** a SKU (e.g. no child product in Commercial V1). That is not a waiver of CASE_0003 quality. It is a written scope cut:

- Named SKU excluded
- Context FAIL must not be reachable in production for that SKU
- Q3 remains required before that SKU is sold

---

## Authority

| Decision | Owner |
|----------|-------|
| Gate pass / fail | This system + recorded evidence |
| Product sign-off | Product |
| Golden freeze | Dataset Steward (Golden Dataset governance — not modified here) |
| Waiver | Product only, as above |

No other document may declare RC2 or Commercial V1 passed.

---

END
