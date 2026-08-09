# Luck Decision Engine

| Field | Value |
|-------|-------|
| **Document** | LUCK_DECISION_ENGINE |
| **Sprint** | LE-3 |
| **Decision version** | 1.0.0 |
| **Foundation** | 1.0.0 (frozen) |
| **Status** | Canonical |

---

## Decision philosophy

LE-3 converts LE-2 structural impacts into **normalized decision indexes**.

It does **not**:

- generate consultant narrative
- produce fortune reports
- mutate LE-1 timeline, LE-2 analysis, AX-2, or AX-3 results
- override Useful God

Opportunity and risk are indexes derived from amplifying vs dampening overlap. They are decision inputs for AX-4 / Interpretation, not prose judgments.

---

## Opportunity model

`OpportunityScore` (`unit = opportunity_index`, 0–100) =

mean over LE-2 impacts of `overlap_score × max(delta, 0)`.

Positive delta (amplifying identity overlap) raises opportunity. No auspiciousness label is attached.

---

## Risk model

`RiskScore` (`unit = risk_index`, 0–100) =

mean over LE-2 impacts of `overlap_score × max(−delta, 0)`.

Negative delta (dampening overlap) raises risk. This is not a report-ready danger statement.

---

## Priority model

Legal classes:

| Value | Rule |
|-------|------|
| `withheld` | `decision_confidence = none` |
| `balanced` | `abs(opportunity − risk) < 5` |
| `opportunity_first` | opportunity > risk by ≥ margin |
| `risk_first` | risk > opportunity by ≥ margin |

Illegal class values fail audit / validation.

---

## Confidence model

`DecisionConfidence` is the minimum LE-2 impact confidence, capped at `low` when luck analysis, AX-2, or AX-3 `success` is false.

Labels: `high` | `medium` | `low` | `none`.

---

## Decision trace

Records timeline / luck-analysis / AX-2 / AX-3 identities consumed, stages executed, outputs published, timestamps.

Not an interpretation log.

---

## Decision audit

Machine-readable only:

- contract validation
- dependency validation
- priority legality
- confidence validation
- deterministic execution
- version compatibility

---

## Future AX-4 integration

AX-4 Luck Pipeline Integration may bind `LuckDecisionResult` as the luck_cycle / annual / monthly decision surface. It must not rewrite AX-3 Useful God packages or LE-2 impact meanings.

---

## Future Interpretation integration

Interpretation Engine consumes published fields only:

`opportunity_score`, `risk_score`, `luck_priority`, `decision_confidence`, `decision_reasoning`, `decision_trace`, `decision_audit`, `overall_luck_decision`, `decision_version`.

Interpretation must not be performed inside this engine.
