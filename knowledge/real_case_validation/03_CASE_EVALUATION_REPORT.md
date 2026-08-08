# 03 — Case Evaluation Report

Version: 1.0  
Status: **EPIC 6 · SPRINT A — Product Quality Evaluation**  
Date: 2026-08-08  
Depends on: Wave 1.1 integration · Golden Case set `01` · EPIC 5 framework  
Scope: Evaluation only — no Knowledge / runtime changes  

---

## 1. Summary verdict

Wave 1.1 integration **materially improves** default consulting voice for identity, strength, useful-god reason, and core recommendation when signals are present.

Consulting quality is **not yet commercially complete**:

- Domain intents (business / career / marriage / health / wealth) have **no dedicated Knowledge** — output stays structural-core only.  
- Several **composition defects** remain (duplication, band-token leakage, priority≈next copy).  
- Weak/mixed charts show **strength–weakness tension** and weak “reduce load first” elevation.  
- Without useful god, recommendation correctly thins out — but commercial usefulness drops hard.

**Overall (Sprint A set, synthetic bags):** **Needs Improvement** for commercial release; **Good** for core structural framing on strong+UG cases only.

---

## 2. Evaluation method

| Item | Detail |
|------|--------|
| Pipeline | `build_narrative_result_dict` + Wave 1.1 Adapter (read-only evaluation) |
| Knowledge | Wave 1.1 five units only |
| Cases run | GC-STRONG-FOLLOW, GC-WEAK-ENEMY, GC-NO-USEFUL-GOD (as GC-NO-UG), GC-SPECIAL-PATTERN, GC-MIXED |
| Intent cases | Coverage assessment only (no domain KU to evaluate) |
| Instruments | Surfaces in `02`; dimensions from EPIC 5 |

No engines, Narrative architecture, Foundation, or KU content were modified.

---

## 3. Good outputs

| Observation | Case evidence | Why it matters |
|-------------|---------------|----------------|
| Consultant identity framing | Strong / Special / Mixed / No-UG | Replaces “Quan sát từ dữ liệu phân tích…” calculator dump |
| Strength commercial lift | Strong, Special, Mixed, No-UG | KU-ST-001 when thân favorable |
| Actionable Rec + reason | Strong, Weak, Special, Mixed | KU-RC-001 action + KU-UG-001 reason |
| Correct UG/RC omission | No useful god | Bundle partial; no invented Dụng thần advice |
| Weakness Core fires | Weak, Mixed | KU-WK-001 selected when enemy/weak signals exist |
| Provenance | All enriched cases | `knowledge:KU-*` / bundle selected_units present |

---

## 4. Weak outputs

| Observation | Case evidence | Impact |
|-------------|---------------|--------|
| Strengths slot often repeats identity | Strong, Special, Mixed | Readability / duplication |
| Priority recommendation == next_action same string | Strong, Weak, Special, Mixed | Decision Support feels incomplete |
| Band tokens in customer text (`vuong`, `nhuoc`, `can`) | Strong, Weak, Special, Mixed | Naturalness / professionalism |
| Weak chart strengths = identity only | Weak | Exec hierarchy thin |
| Weak chart still “expand via UG” without elevating reduce-load | Weak | Empathy / Decision Support |
| Special pattern name passed through; no special-pattern counsel | Special | Generic relative to profile claim |
| Mixed: ST + WK both fire; weakness text says “mỏng” while thân vuong | Mixed | Consistency tension |
| Status often `partial_insufficient` even when Rec good | Strong/Special | Trust messaging vs commercial feel |

---

## 5. Missing advice

| Missing | Profiles | Notes |
|---------|----------|-------|
| Business expansion / venture posture | GC-BUSINESS | No CS-BU knowledge |
| Career role / environment fit | GC-CAREER | No CS-CA knowledge |
| Marriage / relationship counsel | GC-MARRIAGE | No CS-RL/MA knowledge |
| Health lifestyle (non-medical) | GC-HEALTH | No CS-HE knowledge |
| Wealth / money posture | GC-WEALTH | No CS-FI/IV knowledge |
| Special-pattern interpretation | GC-SPECIAL-PATTERN | Pattern label only |
| Follow-pattern specific guidance | GC-FOLLOW-PATTERN | Not distinct from strong/follow bag |
| Distinct next step vs priority | All UG cases | Same prose reused |
| Warning surface depth | Weak/Mixed | Weakness appears in summary; Warning body fill still thin in Pack 05 sections |

---

## 6. Generic advice

| Symptom | Example | Risk |
|---------|---------|------|
| Same 2–4 week UG action template | All UG cases differ only by god label | Feels templated across customers |
| Strength “chịu trách nhiệm / nhịp dài” | Strong & Special alike | Under-differentiates special/follow |
| Identity formula | All cases | Acceptable core; needs domain overlays later |

Generic is **acceptable for Wave 1.1 core**, but blocks “Excellent” commercial rating on intent cases.

---

## 7. Technical wording

| Symptom | Where | Class |
|---------|-------|-------|
| `thân vuong` / `nhuoc` / `can` romanized tokens | Exec identity/strength/weakness | Weak Narrative + Weak Knowledge bind labels |
| Historical calculator phrasing (pre-CK) | Documented in EPIC 4 before/after | Mitigated when CK on |
| Analysis reasoning with `matched rules` / `kích hoạt` | Soft-enriched behind commercial text | Filtered from KU bind; may still linger in side channels |

No raw `{placeholder}` leaks observed in evaluated bags.

---

## 8. Repeated wording

| Pattern | Cases |
|---------|-------|
| Identity text reused as strengths | Strong, Special, Mixed, No-UG |
| Weakness sentence duplicated in slot (`Hỏa; Hỏa`, repeated paragraph) | Weak, Mixed |
| Priority = next = rec action identical | All complete UG bundles |
| Enemy label duplicated in weakness_signal_label | Weak (`Hỏa; Hỏa`), Mixed (`Thủy; Thủy`) |

---

## 9. Per-case scorecard (indicative)

Indicative human scores for Sprint A (not Product sign-off):

| Case | Avg (est.) | Overall | Headline |
|------|-----------:|---------|----------|
| GC-STRONG-FOLLOW | 7.4 | Acceptable→Good | Best path; duplication & token polish remain |
| GC-WEAK-ENEMY | 6.6 | Needs Improvement | WK works; reduce-load & duplication issues |
| GC-NO-USEFUL-GOD | 6.2 | Needs Improvement | Honest thin Rec; low commercial value |
| GC-SPECIAL-PATTERN | 6.8 | Needs Improvement | Core OK; no special-pattern depth |
| GC-MIXED | 6.5 | Needs Improvement | ST+WK tension; duplicate weakness |
| Intent cases (×5) | n/a | Needs Improvement | **Missing Knowledge** for domain advice |

---

## 10. Relation to EPIC 5 acceptance

Against `05_ACCEPTANCE_CRITERIA.md`:

| Gate | Sprint A finding |
|------|------------------|
| Strong+UG structural | Near Acceptable on several dimensions; polish required |
| Full Golden Case set | **Not ready** for commercial release |
| Domain intents | Fail Commercial Value / Decision Support by design (no KU) |
| Hard fails (invention / ethics) | **Not observed** on evaluated bags |

---

## 11. Stop line

Evaluation recorded. Gaps → `04`. Backlog → `05`.  
**Do not author Knowledge Units in this sprint.**

---

END
