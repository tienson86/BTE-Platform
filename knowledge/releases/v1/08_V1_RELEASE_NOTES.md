# 08 — BTE V1 Release Notes

Version: 1.0  
Status: **Release Candidate A — Architecture Freeze**  
Date: 2026-08-08  
Scope: Documentation only — no runtime change in Release A

---

## 1. Summary

BTE V1 enters the **Release Candidate** phase with an **architecture freeze**.

This release documents the official V1 system. It does **not** implement features, polish UI, or redesign Report Engine.

---

## 2. Architecture Milestones

| Milestone | Status |
|-----------|--------|
| Foundation V1.0 | Frozen |
| Analysis Experience (Result Page architecture) | Unified |
| Score Engine (Pack 03) | Complete |
| Interpretation Engine (Pack 04) | Complete |
| Narrative Engine Pack 05 (A–C docs, D1 Runtime, D2 Composer) | Complete |
| Product Integration V1 (Portal prefers NarrativeResult) | Complete |
| **Release A — Architecture Freeze docs** | **This release** |

---

## 3. Foundation

- Product Manifesto → Experience Principles → Brand Language → Visual Language → Design System → Code.  
- Foundation documents and Design System packs are **frozen**.  
- Result Page keeps Zones → Rows → Grid → Cards.  
- UI work must pass Foundation compliance; no token invention.

---

## 4. Narrative

Official commercial prose path:

```
Analysis + Interpretation → Narrative Runtime → NarrativeTree
  → Narrative Composer → NarrativeResult → API → Portal → Result Page
```

- D1 produces structure (`NarrativeTree`) only.  
- D2 produces Pack 05 `NarrativeResult` with source-traced sentences.  
- Insufficient evidence uses approved insufficient narrative — does not invent facts.  
- Portal Result Page is the **official consumer** of `data.narrative_result`.

---

## 5. Portal

- Official path: Canonical Desktop adapter → Result presentation adapter → Result Page.  
- Commercial cards prefer Pack 05 NarrativeResult.  
- Legacy interpretation remains fallback + evidence.  
- Parallel BaZi / Pack 06 screens remain for BC; not the official path (see `07`).

---

## 6. Canonical Document Set (Release A)

Located at `knowledge/releases/v1/`:

| Doc | Title |
|-----|-------|
| `01_V1_ARCHITECTURE_FREEZE.md` | Layers, ownership, freeze policy |
| `02_V1_PIPELINE_REFERENCE.md` | Pipeline + interfaces |
| `03_V1_MODULE_MAP.md` | Modules + status |
| `04_V1_DEPENDENCY_GRAPH.md` | Dependencies |
| `05_V1_PUBLIC_API.md` | Public surfaces |
| `06_V1_EXTENSION_POINTS.md` | Extension policy |
| `07_V1_DEPRECATION_STATUS.md` | Legacy inventory |
| `08_V1_RELEASE_NOTES.md` | This file |

---

## 7. Known Limitations

1. **Narrative quality** — many runs still `partial_insufficient` when evidence is thin.  
2. **Report Engine** — delivery markdown path exists; redesign on NarrativeResult not started.  
3. **Parallel UI stacks** — BaZi Result + Pack 06 screens not fully retired.  
4. **Field naming** — `narrative` (delivery) vs `narrative_result` (Pack 05) can confuse integrators.  
5. **Knowledge / timeline cards** — largely structural; not full Pack 05 grammar surfaces.  
6. **Architecture ROADMAP.md** under `knowledge/architecture/` may lag this freeze set — **this `releases/v1` set is authoritative for RC A**.

---

## 8. Future Roadmap (After Freeze Approval)

Ordered recommendations (do **not** start in Release A):

1. **Architecture review & approval** of this freeze set.  
2. **Narrative Quality** — evidence enrichment / richer Pack 05 copy (no invented facts).  
3. **Deprecation cleanup** — BaZi Result screen / adapter collapse.  
4. **Pack 06 consumers** — Executive / Consultation on NarrativeResult if retained.  
5. **Report Engine epic** — consume NarrativeResult; preserve delivery BC.  
6. **UI Polish** — within Foundation; no layout redesign.  
7. **Production hardening** — ops, monitoring, license, performance (as needed).

---

## 9. What Release A Explicitly Did Not Do

- Modify runtime / tests / engines / portal / adapters / UI.  
- Modify Foundation or Design System.  
- Modify Narrative Engine.  
- Modify Pack architecture folders (except adding this release doc set).  
- Begin Narrative Quality, UI Polish, or Report Engine.

---

## 10. Stop

**Stop after Release A.**

Wait for architecture review and approval before the next epic.

---

END
