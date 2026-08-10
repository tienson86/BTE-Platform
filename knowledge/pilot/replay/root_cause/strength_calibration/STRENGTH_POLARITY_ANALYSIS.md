# Strength Polarity Analysis

**Priority case:** CASE-0001  
**Question:** Is there an objective polarity (sign) defect?

---

## CASE-0001 polarity ledger

Day Master: **Canh Kim**  
Month: **Tân Sửu** (month branch element Thổ; month_branch_ten_god = Chính Ấn)

| Evidence | Source | Expected polarity (classical) | Runtime polarity | Weight (raw) | Contribution (norm) | Correct/Incorrect | Notes |
|---|---|---|---|---:|---:|---|---|
| month_status = Tướng | `_compute_month_status` Thổ→Kim | strengthen (相) | strengthen | — | — | **Correct** | Thổ sinh Kim |
| sea_002 Tướng | `01_season_rules.csv` | strengthen | strengthen | +25 | +0.25 | **Correct sign** | Weight magnitude debatable |
| root 1 chi | hidden same-element | strengthen | strengthen | +12 | +0.12 | **Correct sign** | |
| Đồng hành (Tân = Kiếp Tài) | visible month stem | strengthen | strengthen | +8 | +0.08 | **Correct sign** | |
| Thất Sát (Bính) | year stem | weaken | weaken | −10 / −8 | −0.18 | **Correct sign** | ctl_001 + ctl_006 double-count same officer family |
| spc_004 Ấn mùa lạnh | Chính Ấn + winter | strengthen (seal support) | strengthen | +10 | +0.10 | **Correct sign** | Stacks with season Tướng |
| Day sits Ngọ (Hỏa) | day branch | weaken (坐杀/伤) | **NOT fully scored as drain/control** | — | — | **Coverage gap** | Ten-god list uses visible stems; day-branch fire not in officer/output lists |

### Totals

| Side | Raw |
|---|---:|
| Strengthening | +25+12+8+10 = **+55** |
| Weakening | −10−8 = **−18** |
| Net raw | **+37** → normalized **0.87** |

---

## Polarity investigation answers (CASE-0001)

| Question | Answer |
|---|---|
| Wrong polarity on an element? | **No proven inversion** |
| Polarity rule itself wrong? | Month-status map matches classical 旺相休囚死 skeleton |
| Input mapping wrong? | Pillars match expert; not upstream chart error |
| Ten Gods involved? | Yes — support/control/special keyed off ten gods / month_branch_ten_god |
| Season support incorrect? | Classification Tướng is consistent; **weight +25** may be high for expert mid/weak charts |
| Hidden-stem support incorrect? | Root count uses hidden same-element; sign OK |
| Rooting incorrect? | 1-chi root present; sign OK |

---

## What is *not* an implementation polarity bug

1. Expert says “slightly weak” while score is strong — **disagreement / model calibration**, not `+`/`−` flip.  
2. Missing day-branch sitting fire as explicit weakener — **evidence coverage / modeling gap**, recommend research (P1), not silent patch.  
3. Double counting officer (`ctl_001` + `ctl_006`) — **weighting design**, still correct polarity (both negative).  
4. StrengthContext `cold` vs TemperatureEngine `hot` — temperature scorer **not in Strength path** (`NOT_EXPOSED`); inconsistency for product UX, not Strength polarity math.

---

## Cross-case polarity spot check

| Case | Notable | Polarity signs OK? |
|---|---|---|
| 0002 | season+/root+/control− | Yes |
| 0003 | season+/root+/drain− | Yes |
| 0005 | season− (Tù)/root+ | Yes (season is bipolar) |
| 0006 | season− (Tù)/root+/control− | Yes |
| 0007 | season+ (Đắc lệnh)/control− | Yes |

Season rules are **bipolar** by design (`sea_001…003` positive, `sea_004…005` negative). Treat season expected polarity as context-dependent, not always “strengthen”.

---

## Verdict

**POLARITY_ISSUE: NO** (no objective sign defect proven)  

CASE-0001 primary classification for agreement matrix: **EXPERT_DISAGREEMENT** (with secondary modeling: weighting / evidence coverage).  
Do **not** implement a polarity fix in PILOT-1B.
