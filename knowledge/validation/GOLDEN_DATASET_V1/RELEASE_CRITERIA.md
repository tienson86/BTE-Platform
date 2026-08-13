# RELEASE_CRITERIA

| Field | Value |
|-------|-------|
| Document | RELEASE_CRITERIA |
| Dataset | GOLDEN_DATASET_V1 |
| Status | **FROZEN** |
| Date | 2026-08-13 |

These criteria govern **validation-laboratory and commercial-acceptance readiness**.

They do not authorize engine, Knowledge, or product-code changes.

Engineering tests are a prerequisite, not a substitute.

Related: `knowledge/consulting_quality/05_ACCEPTANCE_CRITERIA.md`.

---

## RC1 — Laboratory + Golden reference

**Intent:** The validation laboratory exists and CASE_0001 is the frozen commercial reference.

| Requirement | Gate |
|-------------|------|
| GOLDEN_DATASET_V1 tree present with protocol, tracker, metrics, governance | Required |
| CASE_0001 indexed, Golden, Frozen | Required |
| CASE_0001 commercial acceptance PASS (existing review) | Required |
| CASE_0001 regression contract documented | Required |
| CASE_0002 and CASE_0003 registered (not required Golden) | Required |
| CASE_0004–0010 exist as placeholders | Required |
| No engines / Knowledge / pipeline modified to create the lab | Required |
| Existing reports referenced, not duplicated or moved | Required |

**RC1 status (2026-08-13): MET** by creation of this laboratory, provided CASE_0001 freeze artifacts remain untouched.

RC1 does **not** mean commercial product V1.0.

---

## RC2 — Three-case governance

**Intent:** Adult generalization and extreme stress are measured under the same protocol. Golden must still pass.

| Requirement | Gate |
|-------------|------|
| RC1 still MET | Required |
| CASE_0001 regression PASS after any intervening improvement | Required |
| CASE_0002 completed through Issue Register + Root Cause (already recorded) | Required |
| CASE_0002 Commercial Score ≥ 7.0 **or** Product classifies it STRESS/GAP in CASE_INDEX | Required for RC2 close |
| CASE_0003 completed through Issue Register + Root Cause (already recorded) | Required |
| CASE_0003 child/weak packaging decision recorded (policy or remaining OPEN S1 with owner) | Required |
| Open S0 on CASE_0002 = 0 | Required |
| No Golden regression FAIL | Required |
| Issue tracker current | Required |

**RC2 status (2026-08-13): NOT MET.**

Reasons:

- CASE_0002 latest published overall ~6.7 / 10 (below 7.0); not formally classified STRESS/GAP as a substitute.
- CASE_0003 still has open S1 packaging / bias issues; commercial 4.2 / 10.

---

## V1.0 — Commercial validation set

**Intent:** The designated commercial set is accepted. The laboratory coverage matrix is filled.

| Requirement | Gate |
|-------------|------|
| RC2 MET | Required |
| CASE_0004–CASE_0010 bound **or** Product records written deferral per slot | Required |
| Coverage includes at least: strong adult, second adult type, weak or stress, one control (no UG or thin evidence) | Required |
| Every case in the **commercial ship set** meets acceptance below | Required |
| Frozen Golden regression = 100% PASS | Required |
| S0 = 0 across commercial ship set | Required |
| Unwaived S1 = 0 across commercial ship set | Required |
| Product written sign-off | Required |
| Dataset Steward freeze of GOLDEN_DATASET_V1 commercial set | Required |

**V1.0 status (2026-08-13): NOT MET.**

Seven placeholders. One Golden. Two registered non-Golden cases below commercial floor.

---

## Acceptance requirements (per commercial case)

A case may enter the commercial ship set only if all hold:

| Rule | Minimum |
|------|---------|
| Identity Score | ≥ 7.0 |
| Career Score | ≥ 7.0 (or N/A with policy: e.g. child — Career hidden) |
| Executive Score | ≥ 7.0 |
| Commercial Score | ≥ 7.0 |
| Customer Test | All applicable questions PASS or PARTIAL with no FAIL on identity/safety |
| Domain Review | Chart facts reflected; no invented facts |
| Blockers | S0 = 0 |
| High | S1 = 0 open (or Product waiver with expiry) |
| Consulting gate | `knowledge/consulting_quality/05_ACCEPTANCE_CRITERIA.md` §3–§5 |
| Hard fails | None of: fact contradiction, invention, ethics breach, technical residue, reversed Dụng thần, lost provenance |

CASE_0001 published floors are **higher** than these minima (see [REGRESSION_RULES.md](REGRESSION_RULES.md)). Minima do not authorize lowering a Frozen case.

---

## What each label is not

| Label | Is not |
|-------|--------|
| RC1 | Permission to sell beyond CASE_0001 packaging conditions |
| RC2 | Full coverage dataset |
| V1.0 laboratory | Product marketing V1.0 if Product has a separate launch checklist |
| A single passing Golden | Generalization |

---

END
