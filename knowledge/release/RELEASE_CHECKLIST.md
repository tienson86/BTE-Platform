# Release Checklist

| Field | Value |
|-------|-------|
| Document | RELEASE_CHECKLIST |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Use | Before every Beta, RC, Production, Emergency Patch, and Hotfix issue |

Every box must be checked for the intended state.
Tests PASS does not check these boxes.
A Completion Report does not check these boxes.

Copy this list into the version’s stage folder and complete it there.
Do not tick boxes on this master file to record a specific issue.

---

## Mandatory

- [ ] Golden Dataset regenerated
- [ ] Executive PDFs regenerated
- [ ] Professional PDFs regenerated
- [ ] No engine leaks
- [ ] No glossary dump
- [ ] No duplicate recommendations
- [ ] No broken fragments
- [ ] Editorial PASS
- [ ] Commercial PASS
- [ ] Product Owner approval
- [ ] Version tagged
- [ ] Release notes completed

---

## Evidence

| Item | Evidence |
|------|----------|
| Golden Dataset regenerated | Fresh artifacts for frozen cases in `beta/BETA0_GOLDEN_DATASET.md` |
| Executive PDFs regenerated | Anchors at minimum: Nguyễn Tiến Sơn, Lương Ngọc Huỳnh, Ngô Đặng Minh Tân |
| Professional PDFs regenerated | Same anchors, Professional edition |
| No engine leaks | Editorial review of customer prose |
| No glossary dump | Consultation editions contain no encyclopedia dump |
| No duplicate recommendations | Cross-page and ranked-recommendation review |
| No broken fragments | Product read of PDF / consultation surface |
| Editorial PASS | Chief Editor, ES-V1, scorecards in the issue record |
| Commercial PASS | Commercial review in the issue record |
| Product Owner approval | Signed `RELEASE_SIGNOFF.md` for this version |
| Version tagged | Tag matches `VERSIONING_POLICY.md` and the signoff version |
| Release notes completed | Changelog per `CHANGELOG_POLICY.md` |

Also required in the issue record (`ARTIFACT_POLICY.md`):

- Before PDFs
- After PDFs
- Diff summary
- Golden Dataset results

---

## State overlays

| State | Extra rule |
|-------|------------|
| Beta | Feature work must be absent. Quality only. |
| RC | Customer Pilot / human consulting review required as Product policy states. |
| Production | Customer Pilot PASS. No unsigned 1.0. |
| Emergency Patch / Hotfix | Scope limited per `HOTFIX_POLICY.md`. Same artifact rule if customer PDF changes. |

---

## Fail closed

If any mandatory box is unchecked, the version is not issued.

Do not substitute a verbal approval, a test summary, or an unsigned tag.
