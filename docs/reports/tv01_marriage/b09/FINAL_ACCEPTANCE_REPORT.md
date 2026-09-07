# TV-01 Marriage Consulting — Final Acceptance Report

Document: TV1-B09  
Module: TV-01_MARRIAGE  
Date: 2026-09-07  
Evaluator: B09 Acceptance Gate  

**Final status: PASS WITH BETA LIMITATIONS — FREEZE READY**

This phase did not add features, redesign architecture, or change business semantics. Production TV-01 code was not modified. Golden expected files were not regenerated.

B01–B07 written completion reports are not stored as markdown in this repository (B07 left screenshots; B08 left `docs/reports/tv01_marriage/b08/ACCEPTANCE_REPORT.md`). Acceptance is based on frozen code, B08 evidence, and B09 re-execution.

---

## Executive Status

TV-01 is architecturally complete and decision-correct for the frozen semantic pipeline. It is customer-usable on the isolated host and via the Customer Portal HTTP proxy. It is not full-production ready because persistence is process-local memory, History UI is absent, Score/Grade are unavailable by design, and D4/D6/D7 remain unpublished.

Highest truthful readiness:

1. **ARCHITECTURAL COMPLETE** — yes  
2. **COMMERCIAL BETA READY** — yes, controlled demo / supervised beta  
3. **FULL PRODUCTION READY** — no, deferred  

---

## Architecture Gate — PASS

- COMMON documents and consulting framework packages were not modified.
- Canonical engines were not imported by `consulting.marriage` (`test_canonical_and_apps_do_not_import_tv01`, `test_applications_still_do_not_import_consulting`).
- Portal talks to Marriage API over HTTP proxy only.
- No duplicate Decision Engine or Canonical Mathematics inside TV-01.
- Decision after Evidence/Finding; Recommendation after Decision; Narrative after Recommendation; Report after Narrative; API serializes stored facts; UI maps DTOs.
- One-way pipeline preserved.

## Runtime Gate — PASS

Live and test traces include: request_validation → birth_input_normalization → canonical_analysis_a/b → canonical_contract_validation → snapshot_builder → evidence_builder → evidence_validation → domain_decision → overall_decision → decision_validation → recommendation_builder → narrative_composer → report_builder. No skipped stage on the B06/B07 bound runtime.

## Canonical Boundary Gate — PASS

TV-01 consumes Canonical output through the adapter and snapshot builder. Extractors read snapshots only. Correlation ids remain `{consultation_id}-A/B`. Calendar/BaZi/Strength/Pattern/Useful God/Ten Gods/Luck are not recomputed after snapshot.

## Decision Gate — PASS

Policy token `marriage.policy.v1@1.0.0`. Decision Mathematics reference `common.decision_mathematics.v1` unchanged. Tier 1 determines natal overall. Timing does not rewrite natal (CASE-M02 vs CASE-M10; LIVE-P1 vs LIVE-P2). Secondary cannot dominate (CASE-M06). No hard veto/guarantee. Score/Grade unavailable (`score_model_version=unavailable`).

## Evidence/Finding Gate — PASS

B08 Golden + B09 re-run: every Finding has Evidence; every Evidence has Canonical source refs; conflicts and rescue preserved; semantic dedup preserved; D4/D6/D7 do not fabricate structural Findings.

## Recommendation Gate — PASS

Every published action has source Finding. No generic sourceless action. Timing only when luck evidence exists. P5/secondary do not publish high-priority actions. Action Model only.

## Narrative Gate — PASS

Communication only. No new Finding/Recommendation/Decision. No score fabrication. No customer `EV-`/`F-` leak. Catalog-bound Vietnamese. Repetition guard remains in composer.

## Report Gate — PASS

Observed order: identity → executive_summary → compatibility_hero → strengths → risks → (timing if available) → domain_analysis → action_plan → confidence_limitations → conclusion → appendix. Unavailable domains omitted from domain_analysis.

## API Gate — PASS

POST, GET consultation/summary/report/history. Customer DTOs hide internal ids. Expert query is controlled and does not mutate Decision. `score=null`, `grade=null`. Idempotency valid for in-memory repository.

## UI Gate — PASS

Route `/marriage-consulting`. Person A/B. No gender default. Birth time optional. Semantic-only Hero. No fake gauge. No empty unavailable-domain cards. Action Plan and confidence readable. Desktop + mobile smoke captured. No reverse Python dependency.

## Validation Gate — PASS

Request validation, Canonical contract validation, evidence/decision/recommendation/narrative/report validation stages remain on the runtime. Failed requests return typed FAILED envelopes.

## Testing Gate — PASS

| Suite | Result |
|-------|--------|
| `pytest tests/consulting -q` | 214 passed |
| Portal marriage + UI-01 + portal | 29 passed |
| Vitest B07 + B08 + nav | 22 passed |
| Golden CASE-M01..M12 | unchanged PASS |
| Repo-wide `tsc --noEmit` | known unrelated debt |

## Traceability Gate — PASS

B08 J-tests plus B09 Golden re-run: Customer text → Recommendation/Finding → Decision → Finding → Evidence → Canonical source. No broken chain.

## Determinism Gate — PASS

B08 ×10 signatures still pass inside `tests/consulting`. Same semantic input + same version bundle → same semantic output. Volatile ids/timestamps ignored.

## Version Gate — PASS (with beta limitation)

Live `version_bundle`:

- `api_version`: v1  
- `api_contract`: consulting.marriage.api.v1  
- `module_version`: 0.0.0-b01 (B01 identity token, frozen by design)  
- `policy_version`: marriage.policy.v1@1.0.0  
- `score_model_version`: unavailable  
- `narrative_version`: marriage.narrative.v1@1.0.0 (bound, not unbound)  
- `report_profile_version`: marriage.report.profile.v1@1.0.0  

Also bound in code/report metadata: evidence catalog, finding model, recommendation catalog, decision engine/math. Public API DTO is the frozen B06 subset and does not enumerate every internal token. Active Narrative is not left unbound.

## Security / Privacy Gate — PASS

No Canonical write. No Decision bypass. Customer JSON leak checks pass. Expert mode is opt-in. Internal ids stripped in customer mode. Process-local store is a beta limitation, not a Canonical integrity failure.

## Performance Baseline

Canonical dominates runtime. TV-01 layers stay in the millisecond range. No SLA. Correctness not traded for speed.

| Stage | B08 recorded (ms) | B09 re-run (ms) |
|-------|-------------------|-----------------|
| API total | 4381.491 | 1098.561 |
| Canonical | 4335.213 | 1050.767 |
| Decision | 5.365 | 8.904 |
| Recommendation | 0.622 | 1.291 |
| Narrative + Report | 6.360 | 16.633 |

## Golden Dataset Status — PASS

CASE-M01 → CASE-M12 unchanged. Expected JSON not regenerated. All overall states remain `mixed` as frozen. Score/grade null.

## Live E2E Status — PASS

Three B08 pairs re-run:

| Pair | Overall | Score/Grade | Notes vs B08 |
|------|---------|-------------|--------------|
| LIVE-P1 1987-01-21 / 1990-05-15 | mixed | null/null | same action family; no timing section |
| LIVE-P2 1988-02-02 / 1990-05-15 | mixed | null/null | `timing_awareness` + timing section |
| LIVE-P3 hours omitted | mixed | null/null | `birth_time_unknown`; not marital risk |

Report order unchanged. No score/grade.

## Browser Verification — PASS

Desktop + mobile smoke. Files under `docs/reports/tv01_marriage/b09/screenshots/`. `browser_verification.json`: semantic-only hero, no fake score, no ID leak, no overflow, no empty interaction card.

## Known Limitations

| Item | Class |
|------|--------|
| Score/Grade unavailable | D. FUTURE FEATURE (also contract: `unavailable`) |
| D4 Interaction insufficient | B. BETA LIMITATION |
| D6 Family insufficient | B. BETA LIMITATION |
| D7 Children insufficient | B. BETA LIMITATION |
| Overall states currently only `mixed` on Golden/live pairs | B. BETA LIMITATION |
| Durable persistence unavailable | B. BETA LIMITATION (blocks full production) |
| History UI unavailable | D. FUTURE FEATURE |
| English API warning descriptions | B. BETA LIMITATION |
| Canonical datetime.utcnow warnings | C. TECHNICAL DEBT (Canonical, not TV-01) |
| Pre-existing mypy stop-stage typing | C. TECHNICAL DEBT |
| Repo-wide unrelated tsc debt | C. TECHNICAL DEBT |
| PDF/DOCX unavailable | D. FUTURE FEATURE |
| `BUILD_PHASE` / `MODULE_VERSION` still B01 tokens | C. TECHNICAL DEBT (B01 freeze) |
| Public version_bundle is B06 subset | B. BETA LIMITATION |

None classified as A. RELEASE BLOCKER.

## Technical Debt

- Canonical `<string>` `datetime.utcnow` (~449 warnings on `tests/consulting`).
- `mypy consulting`: `canonical_runtime.py` stop-stage typed `str`.
- `tsc --noEmit`: baziResultAdapter, canonicalDesktopAdapter, CanonicalWorkspaceCard, fullReportViewModel, luckAdapter, ui09_shensha.test.
- Skeleton `BUILD_PHASE=TV1-B01`, `MODULE_VERSION=0.0.0-b01`.

## Commercial Readiness

- Architectural / Decision Framework: **PASS**
- Customer demo / controlled beta: **PASS** (isolated host + portal proxy; live route usable)
- Full production: **DEFERRED** until durable persistence, deployment integration, History durability, and release operations exist

## Final Decision

**PASS WITH BETA LIMITATIONS — FREEZE READY**

Recommend Product Owner approve `TV1_FINAL_FREEZE.md`. Do not start TV-02 until that approval is explicit.
