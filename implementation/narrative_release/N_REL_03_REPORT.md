# N-REL-03 PACK05 RETIREMENT REPORT

Sprint: N-REL-03
Module: Narrative V2 Release
Mode: Pack05 Legacy Archive (not deletion)
Status: READY FOR PRODUCT OWNER REVIEW

STOP. N-REL-04 was not started. Release was not frozen.

---

## 1. Status

PASS

Pack05 is retired from production routing. It is not deleted. Historical reports, stored Pack05 narrative, and old exports remain. Production Portal and new Narrative exports are Narrative V2 only. `PACK05_LEGACY` is read-only archive access. Production rollback to Pack05 is removed. CASE-0001: Production V2, Historical Pack05, Comparison PASS.

---

## 2. Architecture

```
Narrative V2  → Production
Pack05        → Legacy Narrative Archive (read only)
```

Retirement ≠ deletion.

| Layer | Role |
| --- | --- |
| `resolveNarrativeProvider` | Production provider is `v2` only. `pack05` / `auto` ignored. |
| `selectNarrativePresentation` | Always V2. No Pack05 fallback. |
| `PACK05_LEGACY` | Read-only archive flag. Not a production switch. |
| `load_pack05_archive` / `ResultStore.loadPack05Archive` | Read stored Pack05. No overwrite. |
| Narrative Studio Compare | Historical Pack05 vs V2. |
| `export_production_json` / Presentation Export Layer | New Narrative PDF / DOCX / JSON from Presentation. |
| Official Report Engine `/export/pdf` `/export/docx` | Unchanged analytical report path. Pack05 engine not deleted. |

---

## 3. Production routing

Production provider is Narrative V2 only.

| Request | Production result |
| --- | --- |
| `NARRATIVE_PROVIDER=pack05` | `v2` |
| `NARRATIVE_PROVIDER=auto` | `v2` |
| `NARRATIVE_PROVIDER=v2` | `v2` |
| `?provider=pack05` | `v2` |
| missing / invalid | `v2` |

Pack05 cannot be selected through production flags.

---

## 4. Legacy mode

`PACK05_LEGACY` (`1` / `true` / `pack05`) is read-only.

It does not switch Customer Portal to Pack05.

It does not enable production rollback.

It allows archive inspection of stored `narrative_result`.

---

## 5. History

ResultStore keeps both layers:

```
data.narrative_result       → Pack05 archive
data.narrative_v2_shadow    → Narrative V2
```

No overwrite. No migration. `replaces_pack05` remains `false`.

Historical reports remain. Old exports remain.

---

## 6. Portal

Customer Portal `/result` always renders Narrative V2 on the existing Commercial Dashboard.

No Pack05 switch.

No Pack05 fallback when Presentation is missing: Interpretation / Action show the existing empty states. Overview keeps canonical chart facts (not Pack05 narrative).

Dashboard layout, cards, and PDF chrome are not redesigned.

---

## 7. Studio

Narrative Studio Compare remains.

Heading: `Pack05 (legacy archive)`.

Attribute: `data-pack05-archive="historical"`.

Comparison is historical only. Pack05 is not a production provider.

---

## 8. Exports

New Narrative exports (PDF / DOCX / JSON) read `NarrativeV2Presentation` through `PresentationExportLayer`.

Pack05 cannot be selected as the production Narrative export source.

`PACK05_LEGACY` reads the archive; it does not export Pack05 as production Narrative.

Official customer Report Engine routes `/api/v1/export/pdf` and `/export/docx` are unchanged (analytical report, not deleted). `applications/api/routes/export.py` still contains no `narrative_v2` string.

---

## 9. CASE-0001

| Check | Result |
| --- | --- |
| Production | Narrative V2 |
| Historical Pack05 | `pack05_narrative_result_v1` present, read-only |
| `replaces_pack05` | `false` |
| Export source | `v2` |
| Comparison | PASS |

Artifact: `implementation/narrative_release/n_rel_03/case0001_archive.md`

---

## 10. Tests

Executed (module only):

| Suite | Result |
| --- | --- |
| `tests/narrative_v2/test_pack05_retirement.py` | 9 passed |
| `tests/js/n_rel_03_pack05_retirement.test.tsx` | 6 passed |
| `tests/narrative_v2/test_narrative_studio.py` | passed |
| `tests/narrative_v2/test_release_monitor.py` | passed |
| `applications/api/tests/test_narrative_v2_shadow.py` | passed |

Coverage: provider removal, legacy access, history, compare, regression.

Existing N-REL-01 / provider-flag tests were not modified. They still expect production Pack05 switch and rollback. See remaining failures.

---

## 11. Artifacts

```
implementation/narrative_release/n_rel_03/legacy_matrix.md
implementation/narrative_release/n_rel_03/pack05_archive.md
implementation/narrative_release/n_rel_03/case0001_archive.md
implementation/narrative_release/N_REL_03_REPORT.md
```

---

## 12. Out-of-scope

No Freeze: **YES**

N-REL-04 was not started.

Pack05 was not deleted.

Golden Dataset was not modified.

Presentation Contract was not frozen in this sprint.

Existing N-REL-01 tests were not edited.

---

## 13. Verdict

**READY FOR PRODUCT OWNER REVIEW**

STOP.
