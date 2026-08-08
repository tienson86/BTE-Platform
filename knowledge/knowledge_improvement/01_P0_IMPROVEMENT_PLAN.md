# 01 — P0 Improvement Plan

Version: 1.0  
Status: **OFFICIAL — P0 Improvement Plan**  
Date: 2026-08-08  
Depends on: EPIC 6 `05_IMPROVEMENT_BACKLOG.md`, `04_KNOWLEDGE_GAP_LOG.md`  
Scope: One improvement action per P0 gap — documentation only  

---

## 1. Purpose

Convert every approved **P0** gap into exactly **one** improvement action with:

- Cause  
- Solution  
- Affected Knowledge Unit(s)  
- Expected improvement  

---

## 2. Action map

### IA-P0-01 — Commercial strength-band labels

| Field | Content |
|-------|---------|
| **Backlog / gaps** | BL-P0-01 · KG-008 |
| **Cause** | `{strength_band_label}` binds raw Analysis tokens (`vuong`, `nhuoc`, `can`) into customer prose in Identity / Strength / Weakness paths |
| **Solution** | Adopt Label Language Standard (`02`): official commercial band phrases; Wave 1.1 units must use only commercial labels (or placeholders that resolve to them). Document required projection mapping for implementation sprint |
| **Affected Knowledge Units** | **KU-ID-001**, **KU-ST-001**, **KU-WK-001** (placeholders / surrounding wording). KU-UG-001 / KU-RC-001 unchanged for this action |
| **Expected improvement** | No romanized technical band tokens in Exec; professionalism / naturalness scores rise on all enriched cases |

---

### IA-P0-02 — Weakness signal uniqueness

| Field | Content |
|-------|---------|
| **Backlog / gaps** | BL-P0-02 · KG-009, KG-010 |
| **Cause** | `{weakness_signal_label}` concatenates overlapping enemy sources without dedupe; summary may repeat the same weakness paragraph |
| **Solution** | Weakness Presentation Standard (`03`) § signal contract: one unique caution phrase per case; KU-WK-001 prose assumes a single clean label and must not self-repeat. Document dedupe rules for projection/composition (companion, not this sprint’s runtime edit) |
| **Affected Knowledge Units** | **KU-WK-001** (primary). Pair awareness: **KU-RC-001** |
| **Expected improvement** | Weakness / Warning read once, clearly; trustworthiness recovered on Weak / Mixed cases |

---

### IA-P0-03 — Mixed strong + enemy wording

| Field | Content |
|-------|---------|
| **Backlog / gaps** | BL-P0-03 · KG-014 |
| **Cause** | KU-WK-001 template assumes “lực cấu trúc đang mỏng” even when thân is favorable and caution is enemy/clash-driven |
| **Solution** | Split commercial weakness frames inside **existing** KU-WK-001 via conditional wording patterns (or mutually exclusive bind phrases) defined in `03`: (A) thân suy / overloaded, (B) strong-but-opposed. No new unit id |
| **Affected Knowledge Units** | **KU-WK-001** only (revision). Conditions must stay within Wave 1.1 allow-list unit |
| **Expected improvement** | Mixed charts stay consistent with Strength Core; Accuracy / Consistency defects close |

---

### IA-P0-04 — Reduce-load posture before expand

| Field | Content |
|-------|---------|
| **Backlog / gaps** | BL-P0-04 · KG-013 |
| **Cause** | When WK + RC both select, KU-RC-001 still leads with “nuôi Dụng thần / mở hướng” while reduce-load is a trailing clause — weak charts sound like uncritical expansion |
| **Solution** | Revise **KU-RC-001** commercial shape: when structural caution is in play, **Mitigation-first** order (reduce load → then align to useful god). Align KU-WK-001 closing line with same arc (`03` Weakness→Risk→Mitigation→Opportunity) |
| **Affected Knowledge Units** | **KU-RC-001** (primary), **KU-WK-001** (closing posture), **KU-UG-001** (light touch: keep reason, do not over-push advance) |
| **Expected improvement** | Weak / Mixed Golden Cases gain Empathy + Decision Support; no ethics overclaim |

---

### IA-P0-05 — Wave 1.1 publish / allow-list policy

| Field | Content |
|-------|---------|
| **Backlog / gaps** | BL-P0-05 · KG-018 |
| **Cause** | Units remain `awaiting_review` while production retrieves by id allow-list — policy ambiguity for commercial release |
| **Solution** | Product decision recorded in `05_WAVE_1_1_UPDATE_PLAN.md` § Publish policy: choose (A) formal Approve/Publish after P0 content revision, or (B) explicit time-boxed allow-list exception with owner + expiry. Not a prose edit by itself |
| **Affected Knowledge Units** | All five Wave 1.1 units (**status field / review metadata only** — no new ids) |
| **Expected improvement** | Clear production eligibility; Trustworthiness / release gate unblocked |

---

## 3. Coverage check

| P0 backlog | Improvement action | Status |
|------------|--------------------|--------|
| BL-P0-01 | IA-P0-01 | Planned |
| BL-P0-02 | IA-P0-02 | Planned |
| BL-P0-03 | IA-P0-03 | Planned |
| BL-P0-04 | IA-P0-04 | Planned |
| BL-P0-05 | IA-P0-05 | Planned |

Every P0 has exactly one action. No P1/P2 actions included.

---

## 4. Dependency order (after Product approval)

```
IA-P0-05 (policy decision)     ← can run in parallel with design freeze
        ↓
IA-P0-01 (labels) + IA-P0-02 (signal contract)
        ↓
IA-P0-03 (WK frames) + IA-P0-04 (RC posture)
        ↓
Content revision sprint (edit Wave 1.1 CSV only)
        ↓
Re-run EPIC 6 structural Golden Cases
```

---

## 5. Out of scope reminders

| Do not | Why |
|--------|-----|
| Create units for career/business/etc. | Quantity expansion = Wave 1.2+ |
| Split priority/next (BL-P1-01) | P1 |
| Fix strengths≡identity slot clone alone | P1 / Narrative — noted in `04` as Exec guidance for later |
| Change Narrative Engine / Adapter code now | Documentation-only sprint |

---

## 6. Stop line

P0 actions defined. Standards in `02`–`04`. Unit-level plan in `05`.

---

END
