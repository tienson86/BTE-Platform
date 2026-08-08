# 05 — Wave 1.1 Update Plan

Version: 1.0  
Status: **OFFICIAL — Wave 1.1 Update Plan (awaiting Product approval)**  
Date: 2026-08-08  
Depends on: `01`–`04` · `database/20_knowledge/21_knowledge_units.csv` (Wave 1.1 only)  
Scope: Identify exact revisions — **do not edit CSV in this sprint**  

---

## 1. Purpose

State **exactly which** Wave 1.1 Knowledge Units require revision to close P0 gaps.

| Constraint | Rule |
|------------|------|
| Units in scope | Only the five allow-listed ids |
| New units | **None** |
| Wave 1.2 | **Forbidden** |
| Content edit now | **Forbidden** until Product approval |

---

## 2. Unit revision matrix

| Knowledge Unit | Revise? | Actions | P0 actions |
|----------------|:-------:|---------|------------|
| **KU-ID-001** | **Yes** | Commercial band phrasing per `02`; shorten so Strength can differ (`04` R1–R3) | IA-P0-01 |
| **KU-ST-001** | **Yes** | Remove dependence on raw band tokens; **do not** restate full identity; strength-only beat (`02`, `04`) | IA-P0-01 |
| **KU-WK-001** | **Yes** | Frame A vs Frame B; full Weakness→Risk→Mitigation→Opportunity mini-arc; assume unique `{weakness_signal_label}` (`03`) | IA-P0-02, IA-P0-03, IA-P0-04 |
| **KU-UG-001** | **Light yes** | Keep reason clarity; avoid advance tone that fights mitigation-first when paired with WK; no new claims | IA-P0-04 (light) |
| **KU-RC-001** | **Yes** | Mitigation-first order when structural caution applies; clearer Action/Reason/Next without requiring new unit (`03`, `04`) | IA-P0-04 |

No other rows in `21_knowledge_units.csv` may be added for P0.

---

## 3. Per-unit change intents (authoring brief)

### 3.1 KU-ID-001 — Identity Core

| Field | Intent |
|-------|--------|
| **Cause addressed** | Technical band labels in identity |
| **Solution** | Use commercial thân phrases (`02`); keep one identity beat |
| **Expected improvement** | Cleaner Exec open; no `vuong`/`can`/`nhuoc` leakage |
| **Version after edit** | `1.0.1` (proposed) |

### 3.2 KU-ST-001 — Strength Core

| Field | Intent |
|-------|--------|
| **Cause addressed** | Band tokens + identity repetition |
| **Solution** | Strength-only consultant prose; commercial labels; no “Bạn là người mang Nhật chủ…” reopen |
| **Expected improvement** | Distinct strengths slot; better rhythm |
| **Version after edit** | `1.0.1` (proposed) |

### 3.3 KU-WK-001 — Weakness Core

| Field | Intent |
|-------|--------|
| **Cause addressed** | Duplication amplification, mixed false “mỏng”, arc stops at weakness |
| **Solution** | Dual frames A/B; mandatory Risk+Mitigation+Opportunity close; single-label assumption |
| **Expected improvement** | Accurate Mixed/Weak presentation; never stop at weakness |
| **Version after edit** | `1.0.1` (proposed) |

### 3.4 KU-UG-001 — Useful God Core

| Field | Intent |
|-------|--------|
| **Cause addressed** | Possible over-push vs mitigation-first |
| **Solution** | Preserve explanation; optional caution-aware closing clause when paired (still one unit) |
| **Expected improvement** | Consistent story with WK+RC |
| **Version after edit** | `1.0.1` (proposed) only if prose changes |

### 3.5 KU-RC-001 — Core Recommendation

| Field | Intent |
|-------|--------|
| **Cause addressed** | Expand-first on weak/caution charts |
| **Solution** | Explicit mitigation-first branch in commercial text when caution present; then Dụng thần action; distinct next-step sentence |
| **Expected improvement** | Empathy + Decision Support on Weak/Mixed |
| **Version after edit** | `1.0.1` (proposed) |

---

## 4. Fields likely touched (when approved)

| Field | Touch? |
|-------|:------:|
| `modern_interpretation` | Yes (primary) |
| `summary` / `purpose` | Maybe (align wording) |
| `author_notes` | Yes (Frame A/B; label contract) |
| `classical_text` | Prefer unchanged |
| `condition` | Only if needed to distinguish Frame A/B **without** new unit — prefer notes + bind phrases first |
| `knowledge_unit_id` | **Never change** |
| `wave_id` | Remain `W-P0-1.1-CORE` |
| New rows | **Never** |

---

## 5. Publish / allow-list policy (IA-P0-05)

Product must choose **one**:

| Option | Description | Recommendation |
|--------|-------------|----------------|
| **A — Formal Publish** | After P0 content revision + Golden re-review, set `review_status` to `approved` then `published` per EPIC 3 lifecycle | **Preferred** for commercial release |
| **B — Explicit allow-list exception** | Keep `awaiting_review` but document signed exception: owner, expiry, five ids only | Temporary only |

Until Product chooses, production eligibility remains ambiguous (KG-018).

---

## 6. Companion dependencies (named, not implemented)

These are **not** Knowledge Unit creations and **not** done in this documentation sprint:

| Dependency | Why |
|------------|-----|
| Projection: commercial `strength_band_label` map | Guarantees `02` even if KU keeps placeholders |
| Projection: unique `weakness_signal_label` | Guarantees `03` signal contract |
| Later Narrative P1: strengths≠identity aggregation | BL-P1-02 |

Product may authorize a separate implementation sprint; Architecture remains frozen for redesign — only minimal projection/bind fixes if approved.

---

## 7. Validation after future content edit

Re-run EPIC 6 structural/control cases:

- GC-STRONG-FOLLOW  
- GC-WEAK-ENEMY  
- GC-MIXED  
- GC-SPECIAL-PATTERN (labels only; no new special KU)  
- GC-NO-USEFUL-GOD  

Pass intents:

- No technical band tokens  
- No duplicated weakness labels/paragraphs  
- Mixed uses Frame B  
- Weak/Mixed RC mitigation-first  
- Still exactly five units  

---

## 8. Approval checklist (Product)

- [ ] IA-P0-01…05 accepted  
- [ ] Standards `02`–`04` accepted  
- [ ] Unit matrix §2 accepted (no new units)  
- [ ] Publish option A or B chosen  
- [ ] Authorization to open **content revision sprint** (edit Wave 1.1 only)

---

## 9. Stop line

Update plan complete.  
**Wait for Product approval before modifying any Knowledge Unit.**

---

END
