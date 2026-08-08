# 06 — Release Blockers · Commercial V1

Version: 1.0.0  
Status: **OFFICIAL BLOCKER LIST**  
Date: 2026-08-08  
Epic: Commercial V1 Polish · Sprint A (Audit only)  
Depends on: `01`–`05`  

---

## 1. Purpose

This is the official **Commercial V1 release blocker list**.

No new Capability development in this Epic.  
Fixes are **out of scope for Sprint A** — Product Review decides priority and next polish sprint.

---

## 2. Readiness call

**NO-GO for Commercial V1 Beta** while any **P0** remains open (unless Product issues a written waiver).

---

## 3. P0 — Must fix before Beta

| ID | Blocker | Area | Why it blocks Beta | Evidence |
|----|---------|------|--------------------|----------|
| **P0-01** | Default production path prefers **Promotion** Rec whenever both capabilities fire | Actionability / Journey | Career-intent customers may receive the wrong primary next action | `narrative_merge` Promotion-first; Portal action preference |
| **P0-02** | Career Selection and Promotion Readiness are **not discoverable as named products** on the Result journey | CX / Trust | Customers cannot answer “did I get Career Selection? Promotion?” | No dedicated framing; projections only into S01/S08-style slots |
| **P0-03** | Dual-capability merge creates **dense / concatenated** Exec-facing prose | Narrative / Density | Feels assembled / rule-engine rather than senior consultant | Soft-enrich concatenates career + promotion into reasoning |
| **P0-04** | First-time comprehension risk from **BaZi vocabulary** without journey framing | CX / Understanding | Trust→Understanding pyramid breaks for non-experts | Dụng thần / pattern labels in primary slots; glossary late |
| **P0-05** | Primary Recommendation does not consistently answer **What / Why / How / When / Expected outcome** as a structured consulting answer | Actionability | Commercial Acceptance actionability bar | 90-day prose present; structure incomplete |
| **P0-06** | **Consulting Quality human acceptance** on live merged Result for Strong / Weak / Mixed / Career / Promotion not closed | Process gate | EPIC 5 / Acceptance Criteria require human case gate | Module tests ≠ consulting acceptance |

### P0 notes

- Fixes may be content orchestration, scenario/intent policy, presentation framing, or review process — **not** new Capabilities.  
- Do **not** interpret P0 as permission to redesign Foundation / Design System / Narrative Engine without Product approval.

---

## 4. P1 — Should fix

| ID | Issue | Area | Impact |
|----|-------|------|--------|
| **P1-01** | Both SEL and PRO units include `default` scenario → always co-fire when UG present | Intent routing | Worsens P0-01/03 |
| **P1-02** | Repeated motifs (giữ mực / nuôi Dụng thần / 2–4 tuần / 90 ngày) across caps | Redundancy | Fatigue |
| **P1-03** | Weak-chart Exec not sharp enough on “prepare first” as the lead message | Consulting | Weak scenario quality |
| **P1-04** | Summary → Analysis transition feels calculator after commercial Exec | Flow | Brand inconsistency |
| **P1-05** | Promotion risks under-shown when Career risks win warning slots | Completeness | Asymmetric capability visibility |
| **P1-06** | Career 90-day plan rarely customer-visible on full production path | Commercial value | SEL value under-delivered |
| **P1-07** | Loading / empty copy is utility-grade, not consultant-grade | CX polish | Weak first impression |
| **P1-08** | End-of-report lacks strong “revisit / next conversation” close | Journey | Weak reflection stage |

---

## 5. P2 — Future improvement

| ID | Idea | Notes |
|----|------|-------|
| **P2-01** | Intent selector (Career vs Promotion vs General) before/inside Result | Product feature — later |
| **P2-02** | Dedicated capability summary cards (if architecture allows) | Requires Product + Foundation compliance check |
| **P2-03** | Per-capability progressive disclosure | Density control |
| **P2-04** | Scenario-specific Narrative ordering templates | Without Engine redesign if possible |
| **P2-05** | Mobile density pass for long KU paragraphs | Presentation |
| **P2-06** | Stronger differentiation vs Leadership Assessment vocabulary | Avoid capability confusion pre-Release 3 |

---

## 6. Explicit non-blockers (do not treat as Beta P0)

| Item | Reason |
|------|--------|
| Absence of Leadership / other roadmap capabilities | Out of Commercial V1 scope |
| Frozen Foundation / Design System not redesigned | Correct freeze |
| Analytical engines unchanged | Correct |
| Module Golden Cases for SEL/PRO content | Already PASS — not a content-authoring blocker |
| Wave 1.1 still present | Required dependency |

---

## 7. Suggested Product Review agenda (no fixes yet)

1. Confirm P0-01 policy: intent routing vs single primary capability per run.  
2. Confirm P0-02 minimum framing (copy-only vs structural).  
3. Confirm whether P0-04 is P0 or P1 for Beta audience definition.  
4. Schedule consulting scorecard sessions for five scenarios (P0-06).  
5. Authorize Polish Sprint B scope strictly against this list.

---

## 7. Stop line

**Official blocker list published.**  

Sprint B engineering resolved P0-01…P0-05; P0-06 human package ready (`10`).  

**Wait for Product Review / human consulting sign-off. Do not start a new Capability.**

---

END
