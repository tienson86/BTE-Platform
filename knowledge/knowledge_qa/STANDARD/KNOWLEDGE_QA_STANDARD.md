# Knowledge QA Standard V1.0

| Field | Value |
|-------|-------|
| Document | KNOWLEDGE_QA_STANDARD |
| Version | 1.0.0 |
| Status | Official — Platform Standard |
| Scope | All Interpretation Knowledge |
| Date | 2026-08-12 |

---

# Section 1 — QA Objective

## 1.1 Why Knowledge QA exists

Interpretation Knowledge is the **what to say** layer of BTE.

The Rule Database decides **what is true**.

The Interpretation Standard decides **how to say it**.

The Knowledge Catalog records **selectable units**.

Knowledge QA exists because **correct prose is not production-ready knowledge**.

A paragraph can be:

- Professionally true
- Source-faithful
- Well written

and still be **unfit for machine selection** because it:

- Requires facts the engine never published
- Duplicates another unit’s customer value
- Bleeds into the wrong topic
- Cannot be traced to evidence
- Adds no insight if removed
- Would embarrass a paying consultant in Customer Mode

QA is the **gate between authoring and Validated/Frozen knowledge**.

## 1.2 Why correct knowledge is still not enough

| Condition | Why it fails production |
|-----------|-------------------------|
| Correct but untraceable | Cannot audit a customer claim |
| Correct but evidence-loose | Composer may invent causes or luck |
| Correct but duplicated | Narrative budget waste; contradictory emphasis |
| Correct but wrong topic | MEANING printed as ADVANTAGE; career as strength |
| Correct but generic | Customer pays for insight, not dictionary |
| Correct but non-actionable | Describes; does not steer |
| Correct but cross-pack dependent | Breaks when Pattern/Luck packs are absent |
| Correct but inconsistent | Reasoning selects A; Composer prints B |

**Correctness is necessary. QA proves suitability.**

## 1.3 What QA is not

- Not rewriting knowledge (unless a separate authoring task authorizes it)
- Not validating Rule Database scores
- Not approving Reasoning Engine code
- Not a substitute for human Domain Reviewer approval
- Not final when performed by Cursor or any AI assistant

Detail: [QA_WORKFLOW.md](QA_WORKFLOW.md), [REVIEW_PROCESS.md](REVIEW_PROCESS.md).

---

# Section 2 — QA Criteria

Twelve frozen criteria. Full definitions: [QA_CRITERIA.md](QA_CRITERIA.md).

| # | Criterion | One-line purpose |
|---|-----------|------------------|
| 1 | Professional Correctness | Claim is professionally sound and source-faithful |
| 2 | Evidence Compatibility | Claim needs only published facts |
| 3 | Domain Purity | Unit belongs to its declared topic/purpose |
| 4 | Duplicate Risk | Same customer value not already owned elsewhere |
| 5 | Customer Value | Removing it loses pay-worthy insight |
| 6 | Actionability | Customer or consultant can use it to steer |
| 7 | Readability | Clear, natural, single-claim prose |
| 8 | Explainability | Passes removal test; answers So what |
| 9 | Commercial Quality | Consultant would say it to a paying client |
| 10 | Cross-Pack Dependency | Depends only on owning pack + published facts |
| 11 | Consistency | Aligns with Reasoning, Narrative, Customer Mode policy |
| 12 | Traceability | Source → claim → evidence → fact chain is complete |

Every unit review scores **all twelve** criteria unless a criterion is marked N/A with documented reason (e.g. governance-only unit with `customer_mode: FORBIDDEN` may mark Commercial Quality N/A).

---

# Section 3 — QA Scoring

Frozen **0–10** integer scores per criterion. Anchors: [QA_SCORING.md](QA_SCORING.md).

| Score | Meaning |
|-------|---------|
| 0 | Absent or harmful; block promotion |
| 3 | Major defect; FAIL candidate |
| 5 | Material gap; REVIEW minimum |
| 7 | Acceptable with documented gap |
| 9 | Production-ready minor note only |
| 10 | No defect under this criterion |

**Unit average** = sum of scored criteria ÷ count of scored criteria (exclude N/A).

No fractional scores. No “about 7”.

---

# Section 4 — PASS / REVIEW / FAIL

Frozen verdicts: [PASS_REVIEW_FAIL.md](PASS_REVIEW_FAIL.md).

| Verdict | Meaning |
|---------|---------|
| **PASS** | No blocking defect; eligible for Domain Reviewer promotion to Reviewed |
| **REVIEW** | Usable Draft; defect documented; not Validated until resolved |
| **FAIL** | Blocking defect; must not promote; requires authoring fix |
| **Borderline** | Average in borderline band **and** no criterion ≤ 3; human must decide |

### After each outcome

| Outcome | Next step |
|---------|-----------|
| PASS | Domain Reviewer may set status **Reviewed** |
| REVIEW | Author or governance resolves gap; re-QA same unit id |
| FAIL | Author fixes claim/schema/limitations; re-QA from Draft |
| Borderline | Domain Reviewer documents decision; no auto-promote |

**QA PASS ≠ Validated.** **QA PASS ≠ Frozen.**

Cursor output is **QA Assistant input**, not Approval.

---

# Section 5 — Knowledge Unit Lifecycle

Frozen states: [UNIT_LIFECYCLE.md](UNIT_LIFECYCLE.md).

```text
Draft
  ↓ QA PASS + Domain Reviewer
Reviewed
  ↓ Validation gate
Validated
  ↓ Governance freeze
Frozen
  ↓ Deprecation
Deprecated
```

| Transition | Entry | Exit | Approval | Rollback |
|------------|-------|------|----------|----------|
| → Reviewed | QA PASS on all blocking criteria | Domain Reviewer sign-off | Domain Reviewer | Revert to Draft with note |
| → Validated | QA_CHECKLIST complete | Governance validation | Domain Reviewer + Governance | Revert to Reviewed |
| → Frozen | Pack/catalog version lock | FREEZE_POLICY satisfied | Governance | Deprecated only (no unfreeze silently) |
| → Deprecated | Split, merge, unsafe, superseded | Successor id if any | Governance | Never reuse id |

---

# Section 6 — Review Process

Frozen flow: [REVIEW_PROCESS.md](REVIEW_PROCESS.md).

```text
Author
  ↓ submits unit(s) + source trace
QA Assistant (may include Cursor)
  ↓ scores + PASS/REVIEW/FAIL + written rationale
Domain Reviewer
  ↓ accepts or rejects QA; may override with documented reason
Approval (Governance)
  ↓ Validated / pack release
Freeze
  ↓ Frozen units for production Reasoning consumption
```

**Cursor is never final authority.** AI may score, classify, and recommend. Only human Domain Reviewer + Governance approve lifecycle promotion.

---

# Section 7 — Duplicate Policy

Frozen taxonomy: [DUPLICATE_POLICY.md](DUPLICATE_POLICY.md).

| Term | Definition |
|------|------------|
| Duplicate | Same customer insight, same conditions, interchangeable in Customer Mode |
| Semantic duplicate | Different words; same So what |
| Near duplicate | Partial overlap; one subsumes the other |
| Cross-pack duplicate | Same insight in two packs without declared dependency |
| Representative | One unit per cluster kept under budget |
| Cluster | Declared `duplicate_cluster` id; governance-owned |

Runtime must not discover duplicates by embedding similarity. Clusters are declared at catalog authoring time.

---

# Section 8 — Cross-Pack Policy

Frozen rules: [CROSS_PACK_POLICY.md](CROSS_PACK_POLICY.md).

| Term | Rule |
|------|------|
| Required Packs | Only packs whose facts are published for the case |
| Cross-Pack Dependency | Unit requires another pack’s facts or doctrine to be true |
| Pack isolation | Unit must be selectable with owning pack facts only |
| Safe omission | If dependency pack absent, unit is rejected — not guessed |
| Future activation | Cross-pack fields documented; inactive until pack is published |

---

# Section 9 — Explainability

Frozen rules: [EXPLAINABILITY_STANDARD.md](EXPLAINABILITY_STANDARD.md).

Every unit must answer **So what?**

**Removal test:** If this unit is removed from the Customer narrative, does the customer lose an important insight?

- If **no** → LOW EXPLAINABILITY → REVIEW or omit under budget
- If **yes** → explainability satisfied for that narrative context

Explainability is **contextual** (budget, co-selected units), not absolute.

---

# Section 10 — Commercial Quality

Frozen rules: [COMMERCIAL_QUALITY_STANDARD.md](COMMERCIAL_QUALITY_STANDARD.md).

A unit is commercially ready when:

1. A **paying customer** would benefit from hearing it once, in context.
2. A **consultant** would actually say it — not a textbook, not a rule dump.
3. It is not a dictionary definition, score explanation, or moral ranking.

---

# Section 11 — Actionability

Frozen rules: [ACTIONABILITY_STANDARD.md](ACTIONABILITY_STANDARD.md).

Advice and advantage units must connect:

```text
Published Fact
  ↓
Interpretation (claim)
  ↓
Action (what to do, what to protect, what to choose)
```

Descriptive-only units may PASS for MEANING; RECOMMENDATION units must score Actionability ≥ 7 or FAIL.

---

# Section 12 — Evidence

Frozen rules: [EVIDENCE_STANDARD.md](EVIDENCE_STANDARD.md).

Knowledge **must never require facts not published**.

| State | QA rule |
|-------|---------|
| MISSING | Unit must not narrate that dimension |
| INACTIVE | Unit must not treat as MISSING; reject leak units |
| AVAILABLE | Unit may use if `required_facts` satisfied |
| PARTIAL | Unit may use only if `required_evidence` allows |

Absence of evidence is **not** negative evidence.

---

# Section 13 — Traceability

Frozen chain: [TRACEABILITY_STANDARD.md](TRACEABILITY_STANDARD.md).

```text
Knowledge Unit (knowledge_id)
  ↓
Claim (one So what)
  ↓
Reason (reason_codes at selection time — Reasoning layer)
  ↓
Evidence (published fact keys + states)
  ↓
Fact (Engine output)
```

Every catalog unit must set `source_document` to exact Interpretation Knowledge filename.

---

# Section 14 — Consistency

Frozen rules: [CONSISTENCY_STANDARD.md](CONSISTENCY_STANDARD.md).

Consistency required across:

| Layer | Check |
|-------|-------|
| Knowledge | Claim matches limitations and class gate |
| Reasoning | `required_facts`, `duplicate_cluster`, `conflicts_with` honored |
| Narrative | Budget, section order, purpose |
| Customer Mode | No Validation-only content; no forbidden fields |

Inconsistency between catalog metadata and claim → REVIEW minimum.

---

# Section 15 — Freeze Policy

When a unit may become **Frozen**: [FREEZE_POLICY.md](FREEZE_POLICY.md).

Summary:

- Status **Validated** on all production units in scope
- QA record archived for each Frozen unit
- Pack/catalog version incremented
- Golden references (if any) pinned
- No open FAIL or unresolved REVIEW on Frozen units
- Governance sign-off

Frozen units change only by new version + re-QA + re-freeze.

---

# Section 16 — QA Checklist

Pre-validation checklist: [QA_CHECKLIST.md](QA_CHECKLIST.md).

Used by Domain Reviewer before promoting Reviewed → Validated.

---

# Section 17 — QA Template

Standard review template: [QA_TEMPLATE.md](QA_TEMPLATE.md).

All pack phase reviews (e.g. `PHASE_01_MEANING_REVIEW.md`) should follow this template.

---

# Section 18 — QA Examples

PACK-01 examples only: [QA_EXAMPLES.md](QA_EXAMPLES.md).

No new knowledge invented.

---

# Section 19 — Final Decision

## 19.1 Is this standard sufficient to QA thousands of Knowledge Units?

**Yes — as a governance and review standard.**

It provides:

- Frozen criteria and scoring anchors
- Deterministic PASS/REVIEW/FAIL
- Lifecycle and human approval chain
- Duplicate, evidence, cross-pack, explainability, and traceability rules
- Checklist and template for scale

At thousands of units, QA is executed **by topic phase** (as PACK-01 demonstrated), not in one batch. Automation (QA Assistant) scales scoring; humans scale approval.

## 19.2 Remaining gaps (not in V1.0)

| Gap | Owner | Notes |
|-----|-------|-------|
| Tooling / database for QA records | Platform | Markdown reviews suffice for V1.0; thousands need indexed QA history |
| Automated schema validation against catalog | Platform | QA assumes schema valid; separate validator |
| Inter-rater calibration sessions | Governance | Two reviewers same unit — process not automated |
| Pack-specific criterion weighting | Per pack | Standard uses equal criteria; packs may add **constraints**, not new criteria |
| Regression QA on Reasoning golden changes | Reasoning + QA | When golden plan changes, re-QA affected units |
| Localization QA (VI/EN composer output) | Interpretation Standard | This standard QA’s catalog claims, not composed sentences |
| Performance / load testing | N/A | Not applicable to knowledge QA |

## 19.3 Production readiness of this standard

| Aspect | Ready? |
|--------|--------|
| Authoring guidance | Yes |
| QA Assistant (Cursor) reviews | Yes |
| Human validation gate | Yes |
| Automated production enforcement | No — requires Reasoning + catalog tooling |
| Thousands of units without tooling | Partial — process scales; storage/search does not yet |

**Standard status: OFFICIAL V1.0 — sufficient to begin platform-wide QA. Tooling is a separate work package.**

---

END
