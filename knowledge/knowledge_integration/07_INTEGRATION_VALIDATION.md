# 07 — Integration Validation

Version: 1.0  
Status: **EPIC 4 · SPRINT A**  
Date: 2026-08-08  
Depends on: `01`–`06`  
Scope: Validation specification — no test code required this sprint  

---

## 1. Purpose

Define how to verify Commercial Knowledge integration once Phase B implements the Adapter.

Validation must prove:

1. Knowledge retrieved  
2. Correct Narrative usage  
3. Traceability  
4. No duplicated advice  
5. No unsupported statements  
6. No technical wording  

---

## 2. Validation layers

| Layer | When | Focus |
|-------|------|-------|
| V1 Contract | Unit tests of Adapter (Phase B) | Filters, ranking, bind, fallback |
| V2 Mapping | Fixture charts | Exec/Rec slot fill per `05`/`06` |
| V3 Narrative | Module tests Narrative path | Status, insufficient honesty |
| V4 Content quality | Spot review | Natural VI, no jargon |
| V5 Regression | Portal smoke | Prefer narrative_result; no UI change |

---

## 3. Verify: Knowledge retrieved

| Check | Pass criteria |
|-------|---------------|
| Allow-list | `awaiting_review` units **not** retrieved until allowed |
| Condition | ST omitted when strength unfavorable |
| Condition | UG/RC omitted when no useful_god |
| ID | Retrieved when day master + pattern/strength band present |
| Bundle | `selected_units` lists expected ids |
| Dropped | Reasons recorded |

---

## 4. Verify: Correct Narrative usage

| Check | Pass criteria |
|-------|---------------|
| Exec identity | Uses KU-ID-001 text when selected |
| Exec strengths | Uses KU-ST-001 only when eligible |
| Exec weaknesses | Uses KU-WK-001 only when eligible |
| Recommendation | Uses KU-RC-001 action evidence |
| Reason | UG explanation available to Rec/Reasoning |
| No new sections | Still 7 Pack 05 components |

---

## 5. Verify: Traceability

| Check | Pass criteria |
|-------|---------------|
| Paragraph/slot trace | Contains `knowledge_unit_id` + version |
| Bundle id | Present on run |
| Signal refs | Match bind keys used |
| Audit | Can answer “why this sentence?” with KU id |

---

## 6. Verify: No duplicated advice

| Check | Pass criteria |
|-------|---------------|
| Single id | Each KU at most once |
| Single action | One primary Rec action from CK Wave 1.1 |
| Dedupe | Near-duplicate texts collapsed |

---

## 7. Verify: No unsupported statements

| Check | Pass criteria |
|-------|---------------|
| No invent | No commercial claim without KU or allowed Analysis substrate |
| Condition honor | No ST language under weak band |
| Placeholder | No raw `{useful_god_label}` in output |
| Posture | No Advance from Wave 1.1 RC |

---

## 8. Verify: No technical wording

| Check | Pass criteria |
|-------|---------------|
| Filter | No “kích hoạt khi”, matched rules, mock/placeholder engine phrases |
| Voice | Consultant VI |
| Classical | Paraphrase acceptable; no fake scholarly dump |

---

## 9. Wave 1.1 acceptance fixtures (logical)

| Fixture | Expect CK selection |
|---------|---------------------|
| Strong chart + useful god | ID, ST, UG, RC |
| Weak chart + useful god | ID, WK, UG, RC |
| Strong chart + no useful god | ID, ST (no UG/RC) |
| Minimal missing identity signals | empty or partial; insufficient honesty |
| Units still awaiting_review only | empty bundle |

---

## 10. Exit criteria for Phase B implementation

- [ ] All V1–V3 automated checks green for Wave 1.1 fixtures  
- [ ] V4 spot review Pass on Exec + Rec samples  
- [ ] No Interpretation Engine / Narrative redesign diffs  
- [ ] No Foundation / Portal UI diffs  
- [ ] Traceability demo recorded  

---

## 11. Stop line

Validation defined. Not executed (no runtime this sprint).

---

END
