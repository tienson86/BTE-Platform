# Recommended Changes

No P1/P2/P3 items implemented in PILOT-1B.

---

## P0 — Objective correctness bugs

**None confirmed.**

Investigated and rejected as P0:

| Candidate | Why not P0 |
|---|---|
| CASE-0001 polarity inversion | Rule signs and month_status Tướng are classically consistent |
| Normalization formula | Arithmetic verified on all seven cases |
| CASE-0006 month pillar | Calendar fixture issue (PILOT-1A), not Strength engine |

If a future audit proves a coding defect (wrong operator, inverted map, broken matcher), document file/function/evidence before any patch.

---

## P1 — Model / taxonomy improvements

1. **Versioned taxonomy contract** — 7-level **or** 3-band + tilt/intensity (see `TAXONOMY_PROPOSAL.md`).  
2. **CASE-0001 weight / evidence-coverage review** with expert — season Tướng magnitude, seal stacking (`spc_004`), missing day-branch sitting fire.  
3. **Officer double-count policy** — `ctl_001` + `ctl_006` both fire on same Thất Sát family.  
4. **Align StrengthContext temperature with TemperatureEngine** or document Strength as branch-season-only (currently divergent on CASE-0001).  
5. **Threshold cliff policy** — soft band or hysteresis around 0.65 / 0.35.

---

## P2 — Confidence improvements

1. Reduce confidence near thresholds (`|score−0.65|<0.05`).  
2. Penalize high opposing masses (strengthen vs weaken).  
3. Expose confidence drivers in metadata.  
4. Do not use confidence to silently change band.

---

## P3 — Future research

1. Expand expert-graded set (≥30) before freezing taxonomy edges.  
2. Study follow-pattern vs strength contradictions (CASE-0003 Tòng Nhi / CASE-0007 Tòng Tài).  
3. Hidden-stem ten-god inclusion policy for control/drain.  
4. Whether baseline 50 remains appropriate under expanded taxonomy.

---

## Explicitly forbidden (still)

- Case-specific thresholds / multipliers / labels  
- Rewriting expert labels to match runtime  
- Golden Expected edits to hide gaps  
- Implementing taxonomy in this sprint
