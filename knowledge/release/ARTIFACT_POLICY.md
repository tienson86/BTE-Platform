# Artifact Policy

| Field | Value |
|-------|-------|
| Document | ARTIFACT_POLICY |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Release Manager + Product Owner |

---

## 1. Artifact First Rule

A release is a set of customer-facing artifacts plus the reviews of those artifacts.

Tests alone are insufficient.
A Completion Report alone is insufficient.
A metric JSON alone is insufficient.

Definition of Done remains:

```
Artifact
    ↓
Editorial Review
    ↓
Product Review
    ↓
Product Owner Approval
    ↓
Done
```

This policy states **which artifacts** a release record must contain.

---

## 2. Mandatory pack for every Beta-or-later issue

| Item | Meaning |
|------|---------|
| **Before PDFs** | The previously signed (or previously reviewed) Executive and Professional PDFs for the comparison set. If this is the first train, the Beta0 / editorial baseline PDFs are the Before set. |
| **After PDFs** | Newly generated Executive and Professional PDFs from the issue under review. |
| **Diff summary** | A product-readable account of what changed in the consultation: meaning, structure, length, recommendations, defects closed, defects remaining. Not a source diff dump. |
| **Editorial review** | ES-V1 result for the After PDFs. |
| **Commercial review** | Commercial result for the After PDFs. |
| **Golden Dataset results** | Regeneration record for frozen real cases: which cases, which editions, pointers to files, editorial/commercial scores. |

Minimum comparison set: Nguyễn Tiến Sơn, Lương Ngọc Huỳnh, Ngô Đặng Minh Tân.
Remaining validated cases follow `beta/BETA0_GOLDEN_DATASET.md` as Product Owner requires for that issue.

---

## 3. Filing

Store the pack in the version’s stage folder:

```
knowledge/release/<stage>/<version>/
```

Until a version subfolder is opened, the stage README states that the folder is empty of issues.

Do not overwrite Before PDFs with After PDFs.
Do not edit Golden Dataset expected outputs so that After matches a desired story.

---

## 4. What is not an artifact

- Unit or integration test logs
- Completion reports
- Architecture notes
- Chat approvals
- Unsigned tags
- Synthetic or anonymous fixture PDFs used as commercial proof

Those may be attached as supporting files.
They do not replace the mandatory pack.

---

## 5. Hotfix and Emergency Patch

If customer-facing PDFs change, the full pack is required, with Before = last Production (or last signed) PDFs.

If only non-customer internals change and no consultation text or PDF changes, Product Owner must record that fact on signoff.
The default assumption is that a patch **does** change the artifact until proven otherwise.
