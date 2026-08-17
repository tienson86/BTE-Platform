# Rollback Policy

| Field | Value |
|-------|-------|
| Document | ROLLBACK_POLICY |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Product Owner + Release Manager |

Rollback withdraws a signed version from use.
It is a product decision, not an engineering convenience.

---

## 1. Rollback conditions

Rollback is required when any of the following is true after issue:

- Customer-facing truth is wrong relative to the frozen owner
- Editorial or commercial FAIL is discovered on the issued artifacts
- Engine leakage, glossary dump, duplicate recommendations, or broken fragments reached the issued consultation
- A hotfix or patch introduced a new High or Critical defect
- Dual truth appears across layers
- An unauthorised Architecture change shipped
- Customer Pilot or Production use shows harmful or systematically unusable advice

Rollback is considered, and Product Owner decides, when:

- Golden Dataset After PDFs regress against the previous signed Before set without an accepted explanation
- Professional or Executive scores fall below the agreed threshold
- Artifact pack is found incomplete after issue

Rollback is not used to:

- retract an unsigned Internal draft
- avoid writing a changelog
- hide Golden Dataset drift by restoring edited snapshots

---

## 2. Rollback approval

| Step | Owner |
|------|-------|
| Propose rollback | Release Manager or Product Owner |
| Confirm condition | QA + Chief Editor if prose; Engineering if truth |
| Approve rollback | **Product Owner** |
| Execute recovery | Release Manager |
| Notify | Product Owner decides audience |

Engineering may halt a broken environment.
Engineering may not declare a commercial version rolled back without Product Owner approval.

---

## 3. Artifact retention

Rollback does **not** delete the failed issue.

Retain:

- Before PDFs
- After PDFs (the failed issue)
- Diff summary
- Editorial and commercial reviews
- Signoff of the version being withdrawn
- Rollback decision record

File the decision under `archive/` with a pointer from the stage folder of the withdrawn version.

Retention exists so the company can see what was issued and why it was withdrawn.
It is not permission to reissue the withdrawn artifacts.

---

## 4. Version recovery

Recovery order:

1. Restore the last **signed** version that still passes gates for that state.
2. If that version is Production 1.0.x, customers receive that patch line, not an unsigned Beta.
3. Do not recover by rebuilding from memory or from tests without regenerating the artifact pack.
4. The restored version keeps its original name. A new repair, if needed, is the next patch (for example 1.0.2) after a new signoff.
5. A withdrawn version name is not reused. RC2 follows a withdrawn RC1. 1.0.1 follows a withdrawn 1.0.0 issue only as a new signed patch, never as a silent retag of the failure.

---

## 5. Capability-scoped withdrawal

If a single commercial capability is unsafe but the rest of the signed consultation is not, Product Owner may withdraw that capability from sale without rolling back the entire version.

That decision is still recorded as a rollback-class event.
It still requires After artifacts proving what customers now receive.
