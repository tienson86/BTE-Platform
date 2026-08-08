# 06 — Wave 1.1 Revision Report

Version: 1.0  
Status: **EPIC 7 · SPRINT B COMPLETE — awaiting Product Review**  
Date: 2026-08-08  
Depends on: Sprint A `01`–`05` · Wave 1.1 CSV · EPIC 6 Golden Cases  
Scope: Content revision of five existing units only  

---

## 1. Summary

Sprint B completed the first Knowledge Evolution cycle: **revise quality, not quantity**.

| Item | Result |
|------|--------|
| Units revised | KU-ID-001, KU-ST-001, KU-WK-001, KU-UG-001, KU-RC-001 |
| New units | **0** |
| Wave 1.2 | **Not started** |
| Version | `1.0.0` → **`1.0.1`** |
| Content status | **`approved`** (Publish still Product-owned) |
| Golden Baseline | **V1 candidate** (five-unit core) |
| Module tests | `tests/commercial_knowledge` → **16 passed** |
| Golden Cases re-run | **12 / 12** (see `07`) |

---

## 2. P0 actions applied

| Action | Applied how |
|--------|-------------|
| IA-P0-01 Commercial band labels | KU prose + projection maps `vuong`/`nhuoc`/`can` → thương mại |
| IA-P0-02 Weakness signal uniqueness | Projection dedupe; WK assumes clean label |
| IA-P0-03 Mixed Frame B | Projected `weakness_statement` (opposed ≠ mỏng) |
| IA-P0-04 Mitigation-first RC | KU-RC-001 leads with giữ mực → then Dụng thần |
| IA-P0-05 Status clarity | `review_status=approved`; Publish still Product |

---

## 3. Per-unit changes

| Unit | What changed | Unchanged |
|------|--------------|-----------|
| KU-ID-001 | Shorter identity beat; commercial `{strength_band_label}` | id, schema, scenarios, targets, usage |
| KU-ST-001 | Strength-only beat (no identity reopen) | same |
| KU-WK-001 | Arc via `{weakness_statement}` / risk / mitigation + Opportunity close | same |
| KU-UG-001 | Caution-aware closing clause | same |
| KU-RC-001 | Mitigation-first Action; clearer next step | same |

Classical text kept. Narrative targets / primary·secondary usage / ids untouched.

---

## 4. Companion bind fix (minimal)

To make commercial labels and Frame A/B bind correctly without new units:

| File | Change |
|------|--------|
| `engines/commercial_knowledge/signal_projection.py` | Commercial `strength_band_label`; unique weakness labels; `weakness_statement` / `risk` / `mitigation` |

Not a Narrative Engine redesign. Not Foundation/UI. Adapter retrieval contract unchanged.

---

## 5. Database notes

- Target file: `database/20_knowledge/21_knowledge_units.csv`  
- Changelog: `0.2.1` entry added  
- Still exactly **five** rows  

---

## 6. Stop line

Revision complete. Comparisons: `07`. Remaining gaps: `08`.  
**No Wave 1.2. No new units. Wait for Product Review (including Publish).**

---

END
