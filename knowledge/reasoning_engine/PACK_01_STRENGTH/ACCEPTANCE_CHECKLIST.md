# Acceptance Checklist

| Field | Value |
|-------|-------|
| Document | ACCEPTANCE_CHECKLIST |
| Version | 1.0.0 |

---

Design PASS only if all are true:

- [x] Reasoning Engine does: decide worth, order, emphasis, warn, caution, mode split
- [x] Does not: rescore, invent facts, write final sentences, LLM
- [x] Input contract `ReasoningInput` defined
- [x] Output `NarrativePlan` defined
- [x] Knowledge Unit metadata sufficient
- [x] Evidence Gate: eligible / ineligible / partially_supported
- [x] Relevance ≠ Salience
- [x] Priority ≠ Rule Priority
- [x] Narrative Budget defined
- [x] Duplicate policy defined
- [x] Conflict policy + nuance defined
- [x] Confidence affects reasoning
- [x] Alternative Analysis default Validation
- [x] Missing Data policy (absence ≠ evidence)
- [x] Claim Traceability
- [x] Customer / Validation separation
- [x] Deterministic
- [x] Versionable
- [x] CASE-0001 walkthrough complete
- [x] No production code changed in this task

Reviewers still **accept or reject** the CASE-0001 walkthrough as the production-standard candidate.

---

END
