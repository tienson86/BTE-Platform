# CHANGELOG — Cross-Domain Reasoning V1.1

## Added

- `applications/production/interpretation/cross_domain/` — models, normalizer, relations, themes, executive plan, reasoner, input builder
- Identity + Career feature composers wired to CDR
- Executive consulting consumes `ExecutiveClaimPlan`
- CustomerDeliverable: `identity_report`, `career_report` + section statuses
- Tests: `tests/production/test_cross_domain_reasoning.py`
- Docs: this package

## Changed

- `MultiDomainInterpretationService` runs CDR for GENERAL / IDENTITY / CAREER
- `ExecutiveConsultingComposer` no longer hard-stitches ENDURANCE+OUTPUT_RELEASE insight
- CASE-0002 fixture documents Thu Phương request (SYNTHETIC_B retained)

## DoD

| Criterion | Status |
|-----------|--------|
| generic cross-domain input | PASS |
| domain claims normalized | PASS |
| scope-aware conflict detection | PASS |
| precedence evidence/policy-based | PASS |
| unsupported precedence → UNRESOLVED | PASS |
| chart-specific primary themes | PASS |
| ExecutiveClaimPlan | PASS |
| Identity uses CDR | PASS |
| Career uses CDR | PASS |
| Executive uses claim plan | PASS |
| CASE-0001 no regress | PASS |
| CASE-0002 improves | PASS |
| no case-specific branches | PASS |
| no LLM reasoning | PASS |
| tests pass | PASS (47 production suite) |
