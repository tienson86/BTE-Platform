# CHANGE_POLICY

| Field | Value |
|-------|-------|
| Document | CHANGE_POLICY |
| Dataset | GOLDEN_DATASET_V1 |
| Status | **FROZEN** |
| Date | 2026-08-13 |

---

## How Golden Cases evolve

Golden Cases do **not** evolve by silent rewrite.

```text
Proposed change
  ↓
New Run (new capture, new path or dated file)
  ↓
Customer Review + Domain Review
  ↓
Issue Register + Root Cause
  ↓
Regression against current Frozen Golden
  ↓
Approval chain (GOVERNANCE)
  ↓
New freeze version
```

Allowed evolution:

| Allowed | Not allowed |
|---------|-------------|
| Add a new case slot | Edit frozen Master Interpretations in place |
| Add a new review cycle folder (e.g. REVALIDATION_V1_1) | Move historical files |
| Raise a case from ACTIVE → GOLDEN → FROZEN | Delete a Frozen case |
| Supersede a Frozen case with a new version id | Change recorded scores so an old run “passes” |
| Bind a placeholder after Product approval | Copy CASE_0001 prose onto another case |

If customer language or engine publish changes, the **new** output is a new capture. The old capture remains Ground Truth for that freeze.

---

## How versions are frozen

| Object | Freeze unit |
|--------|-------------|
| Laboratory | `GOLDEN_DATASET_V1` (this tree). Next lab generation is `GOLDEN_DATASET_V1_1` or `V2`, not in-place mutation of frozen policy without CHANGELOG. |
| Case | Status FROZEN in [CASE_INDEX.md](CASE_INDEX.md) + FINAL_SCORE snapshot + pointers to immutable artifacts |
| Narrative plan | Existing freeze docs (e.g. PACK-01 CASE_0001 GOLDEN_REFERENCE) |
| Feature sample | Existing CASE_0001 Identity / Career samples |

Freeze checklist:

1. Protocol complete through Regression.
2. Scores recorded in FINAL_SCORE.md.
3. Approvers recorded (Dataset Steward, Domain, Product as required).
4. CHANGELOG row added.
5. Original artifacts remain at original paths.

Unfreeze requires the same approval chain as freeze, plus a written reason. Unfreeze is not an edit; it is a new cycle.

---

## How historical results remain reproducible

| Rule | Practice |
|------|----------|
| Do not move | Validation PDFs, `_raw_pipeline.json`, Master Interpretations, feature samples stay where they are |
| Do not rewrite | Laboratory files point; they do not replace report bodies |
| Do not overwrite captures | New runs go to dated / versioned files (pattern already used: `CASE_0002/REVALIDATION_V1_1/`) |
| Pin input | INPUT.md points to frozen input (JSON or published birth fields) |
| Pin pipeline identity | Record orchestrator / pipeline name used for the capture |
| Pin reviews | Customer and Domain reviews are dated documents |
| Pin scores | FINAL_SCORE.md quotes published numbers and source paths |

Reproducing a Frozen result means: same input + same frozen pipeline version + same artifact files. It does **not** mean regenerating and replacing the Golden files.

If the live pipeline has moved, historical Frozen results are still valid as Ground Truth for **that freeze**. A new live run is a new cycle, not an overwrite.

---

## Laboratory documents vs case artifacts

| This tree (`GOLDEN_DATASET_V1/`) | Existing artifact trees |
|----------------------------------|-------------------------|
| Governance, protocol, index | Reports, JSON, PDFs, reviews |
| Status and KPI snapshots | Ground Truth bodies |
| Placeholders | — |

Changing a pointer here does not change Ground Truth. Changing Ground Truth requires CHANGE_POLICY + approval.

---

## Compatibility with other golden systems

| System | Policy |
|--------|--------|
| `knowledge/golden_dataset/` | Knowledge Infrastructure framework — do not merge |
| `tests/golden_dataset/` | Engine fixtures — do not edit to pass commercial reviews |
| `knowledge/validation/CASE_0002/` and `CASE_0003/` | Canonical captures for those cases — do not move |
| `knowledge/master_interpretations/CASE_0001/` | Frozen commercial depth — do not edit from this lab |

---

## Changelog duty

Every freeze, bind, status change, or tracker-significant resolution gets a row in [CHANGELOG.md](CHANGELOG.md).

No silent status edits.

---

END
