# N-REL-01 PORTAL PRODUCTION SWITCH REPORT

Sprint: N-REL-01
Module: Customer Portal + Analyze attach (controlled release)
Mode: Production switch with Pack05 fallback
Status: READY FOR PRODUCT OWNER REVIEW

STOP. N-REL-02 was not started.

---

## 1. Status

PASS

Customer Portal production `/result` now renders Narrative V2 as the primary narrative provider. Pack05 remains stored, callable, and the rollback / automatic fallback path. Dashboard, cards, and PDF were not redesigned.

---

## 2. Architecture

```
Analyze
  → Canonical Analysis
  → Pack05 NarrativeResult          (always stored)
  → Narrative V2 Runtime            (always attached)
  → NarrativeV2Presentation v2.1
  → ResultStore
       narrative_result             Pack05
       narrative_v2_shadow          Narrative V2
  → NARRATIVE_PROVIDER
       pack05 | v2 | auto
  → Commercial Dashboard            (same UI)
       Overview / Interpretation / Action Plan
```

Portal copies Presentation fields into existing cards. It does not compose, rewrite, join, or interpret Narrative.

---

## 3. Feature flag

Name: `NARRATIVE_PROVIDER`

| Value | Meaning |
| --- | --- |
| `v2` | Default for this release. Render NarrativeV2Presentation. |
| `pack05` | Rollback. Render Pack05. |
| `auto` | Prefer V2 when valid; otherwise Pack05. |

Resolution order:

1. Query `?provider=`
2. Boot `window.__BTE_NARRATIVE_PROVIDER__`
3. Env `NARRATIVE_PROVIDER`
4. Default `v2`

Rollback is a flag change. No rebuild. No migration. No data loss.

Query override allows an emergency drill on a live session.

---

## 4. Portal provider

`/result` still mounts `CommercialDashboardPage`.

When `provider=v2` and Presentation `bte.presentation.v2.1` is valid:

- Overview insight ← `overview.headline` (or `summary` if headline is null; never joined)
- Interpretation lead ← `interpretation.consulting_flow`
- Zones copied independently: observation, reasoning, impact, recommendation
- Action Plan ← `top_priority`, `actions`, `warnings`, `current_period`

`?narrative=v2-shadow` remains a diagnostic review surface. It is not production.

---

## 5. ResultStore

Both layers are preserved independently:

| Key | Content |
| --- | --- |
| `data.narrative_result` | Pack05 |
| `data.narrative_v2_shadow` | Narrative V2 envelope |

`ResultStore.selectNarrativeLayers()` returns both without mutating either.

Switch chooses which Presentation the Portal renders. It does not rewrite storage.

---

## 6. Rollback

`provider=pack05`

Verified on CASE-0001:

Pack05 production → V2 production → Pack05 rollback

After rollback, both stored layers remain. The customer is not asked to re-analyze.

---

## 7. Monitoring

Logged fields only (no personal data):

- `provider`
- `duration_ms` / `runtime_ms`
- `presentation_version`
- `fallback` / `fallback_count`
- `fallback_reason`

Backend: `narrative.release provider=… status=… presentation_version=… duration_ms=…`

Portal: `narrative.release` operational event.

---

## 8. Failure handling

If Narrative V2 Presentation is missing or invalid:

- Portal falls back to Pack05 automatically
- Fallback is recorded
- Customer flow is not interrupted
- No partial JSON, stack traces, internal ids, rule ids, or pipeline traces

Pack05 remains callable even when V2 is healthy.

---

## 9. CASE-0001 switch

Birth: Nguyễn Tiến Sơn · 1987-01-21 04:30

| Step | URL | Result |
| --- | --- | --- |
| Pack05 | `/result?provider=pack05` | Canonical overview (Nhật chủ Canh Kim). Pack05 interpretation. |
| V2 | `/result?provider=v2` | Headline + consulting_flow + action titles from Presentation v2.1 |
| Rollback | `/result?provider=pack05` | Same Pack05 dashboard. Stored V2 retained. |

All three succeeded.

---

## 10. Tests

Portal:

`npx vitest run tests/js/n_rel_01_portal_production_switch.test.tsx`

**15 passed**

- Provider switch (`pack05` / `v2` / `auto`)
- Presentation selection
- Fallback (invalid + missing)
- Rollback on the same payload
- ResultStore layer independence
- Portal rendering on Commercial Dashboard
- No composition / no leak
- Pack05 adapters still callable

Also:

- `tests/js/narrative_v2_shadow.test.tsx` 14 passed
- `tests/js/ui11_interpretation.test.tsx` 20 passed
- `tests/js/ui12_action_plan.test.tsx` 19 passed
- `applications/api/tests/test_narrative_provider.py` 6 passed
- `applications/api/tests/test_narrative_v2_shadow.py` passed in the prior module run
- `applications/customer_portal/tests/test_result_store.py` 13 passed

---

## 11. Screenshots

`implementation/narrative_release/n_rel_01/screenshots/`

| File | Capture |
| --- | --- |
| `01_pack05_production.png` | Pack05 production |
| `02_narrative_v2_production.png` | Narrative V2 production |
| `02a_v2_overview.png` | V2 Overview card |
| `02b_v2_interpretation.png` | V2 Interpretation card |
| `02c_v2_action.png` | V2 Action Plan card |
| `03_rollback_pack05.png` | Rollback Pack05 |

---

## 12. Out-of-scope

| Item | Status |
| --- | --- |
| No Pack05 retirement | YES |
| No Freeze | YES |
| No Dashboard redesign | YES |
| No card redesign | YES |
| No PDF redesign | YES |
| N-REL-02 Dual Run & Monitoring | Not started |

---

## 13. Verdict

READY FOR PRODUCT OWNER REVIEW

STOP.

Do not start N-REL-02.

---

## Files changed

Created:

- `applications/customer_portal/src/resultState/narrativeProvider.ts`
- `applications/customer_portal/src/resultState/narrativePresentationSelection.ts`
- `applications/customer_portal/src/resultState/narrativeReleaseMonitor.ts`
- `applications/customer_portal/src/adapters/narrativeV2DashboardAdapter.ts`
- `applications/customer_portal/tests/js/n_rel_01_portal_production_switch.test.tsx`
- `applications/api/tests/test_narrative_provider.py`
- `applications/customer_portal/scripts/capture_n_rel_01_screenshots.py`
- `implementation/narrative_release/n_rel_01/provider_matrix.md`
- `implementation/narrative_release/n_rel_01/rollback_test.md`
- `implementation/narrative_release/n_rel_01/case0001_switch.md`
- `implementation/narrative_release/n_rel_01/screenshots/*.png`
- `implementation/narrative_release/N_REL_01_REPORT.md`

Modified:

- `applications/customer_portal/src/screens/commercial_dashboard/CommercialDashboardPage.tsx`
- `applications/customer_portal/src/entries/resultApp.tsx`
- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/config.py`
- `applications/customer_portal/templates_util.py`
- `applications/customer_portal/templates/result_desktop.html`
- `applications/customer_portal/static/js/result_store.js`
- `applications/customer_portal/tests/js/result_store_flow.js`
- `applications/api/services/narrative_v2_shadow.py`

Reason: controlled production switch with rollback.

Impact: `/result` default provider is Narrative V2. Pack05 is fallback and rollback. Analyze, engines, Pack05 runtime, PDF, and dashboard geometry are unchanged.

---

## Remaining failures

`tests/js/ui04_overview.test.tsx` O15 (`resolveResultBoot` expected `current`, received `empty`) fails in isolation. Cause: `isIncompatibleCalendarRule` rejects payloads without `calendar.calendar_rule_version`. N-REL-01 did not change Result boot or that test. Out of scope.
