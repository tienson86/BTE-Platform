# 18 — Scenario Knowledge Matrix

Version: 1.0  
Status: **SPRINT D — Knowledge Catalog Blueprint**  
Date: 2026-08-08  
Depends on: `16`, `17`, Sprint B `06`–`07`  

---

## 1. Purpose

Matrix:

```
Scenario
    ↓
Required Knowledge Units
    ↓
Optional Knowledge Units
    ↓
Narrative Components
```

Ids from `16`. Profiles align with `07` cardinality.

---

## 2. Matrix

| Scenario | Required KUs | Optional KUs | Narrative components |
|----------|--------------|--------------|----------------------|
| **CS-ID** | AN-ID-000001…000003,000005…000008; AN-XX-000001; AC-DM-000006 | AN-ID-000004; CN-PE-000001; AN-XX-000003 | Exec, Observation, Reasoning, Conclusion |
| **CS-CA** | CN-CA-000001; AC-CA-000001; AN-ID-000007; AC-DM-000001 | CN-CA-000002/3; OP-CA-000001; OP-LU-000001; AC-CA-000004 | Exec, Impact, Recommendation, Conclusion; Warning if RK |
| **CS-CC** | AC-DM-000002…000005; AC-CA-000002/3; RK/MT-CA-000001; CN-CA-000001; CN-LU-000001 | OP-LU-000001; ST-PG-000001; AC-FI-* if money-driven | Exec, Reasoning, Impact, Recommendation, Warning, Conclusion |
| **CS-PR** | OP-CA-000001; RK/MT-LE-000001; CN-LE-000001; AC-DM-000001/4 | PG-LE-000001; OP-LU-000002 | Exec, Impact, Recommendation, Warning, Conclusion |
| **CS-BU** | CN-BU-000001; AC-BU-000001; RK/MT-BU-000001 | CN-FI-000001; OP-BU-000001; ST-BU-000001 | Exec, Impact, Recommendation, Warning, Conclusion |
| **CS-ST** | OP-BU-000001; RK/MT-BU-000002; AC-BU-000002; CN-LU-000001; AC-DM-* postures | CN-BU-000001; PG-XX-000001 | Full set (Rec + Warning heavy) |
| **CS-LE** | CN-LE-000001; AN-XX-000003; PG-LE-000001 | RK/MT-LE-000001; AC-DM-000001 | Observation, Reasoning, Impact, Recommendation, Warning |
| **CS-IV** | RK/MT-FI-000001; AC-FI-000001/2; AC-DM-000005; CN-FI-000001 | OP-LU-000001; RK/MT-FI-000002 | Exec, Impact, Recommendation, Warning, Conclusion |
| **CS-FI** | CN-FI-000001; PG-FI-000001; AC-FI-000001; RK/MT-FI-000002 | AC-FI-000002; OP-XX-000001 | Impact, Recommendation, Warning, Conclusion |
| **CS-PP** | CN-FI-000002; AC-FI-000003; RK/MT-FI-000003; AC-DM-000002/3 | CN-EN-000001; OP-LU-000001 | Exec, Recommendation, Warning, Conclusion |
| **CS-MA** | CN-MA-000001; RK/MT-MA-000001; AC-MA-000001 | CN-LU-000002; CN-RE-000001 | Impact, Recommendation, Warning, Conclusion; Exec careful |
| **CS-DT** | CN-DT-000001; PG-DT-000001; CN-PE-000001 | CN-RE-000001; RK/MT-MA light if indicated | Observation, Impact, Recommendation, Warning |
| **CS-CH** | CN-CH-000001; PG-CH-000001 | CN-RE-000001 | Impact, Recommendation, Warning (soft) |
| **CS-PA** | CN-PA-000001; AC-PA-000001 | CN-RE-000001 | Impact, Recommendation, Conclusion |
| **CS-HE** | CN-HE-000001; RK/MT-HE-000001; AC-HE-000001; AN-XX-000002 | RK/MT-XX-000003 | Impact, Recommendation, Warning |
| **CS-LS** | PG-LS-000001; PG-XX-000001; AC-LS-000001 | PG-LS-000002/3; AN-XX-000002 | Recommendation, Impact, Conclusion |
| **CS-ED** | CN-ED-000001; AC-ED-000001 | OP-ED-000001; AC-CA-000004; OP-LU-000001 | Impact, Recommendation, Conclusion |
| **CS-PG** | ST-PG-000001; CN-PG-000001; AC-PG-000001; AN-ID-000001/5/6 | OP-XX-000001 | Exec, Reasoning, Recommendation, Conclusion |
| **CS-LT** | CN-LU-000001/2; AC-LU-000001; OP-LU-000001; RK/MT-XX-000001/2 | CN-LU-000003; RK/MT-LU-000001; OP-LU-000002 | Exec, Impact, Recommendation, Warning, Conclusion |
| **CS-MD** | AC-DM-000001…000007; RK/MT-XX-000001/2; CN-XX-000001 | Context-domain Required set (union) | Full set |
| **CS-EN** | CN-EN-000002; PG-EN-000001 | PG-XX-000001 | Impact, Recommendation |
| **CS-TR** | CN-TR-000001; AC-TR-000001; RK/MT-TR-000001 | CN-LU-000002; PG-LS-000001 | Recommendation, Warning, Impact |
| **CS-RL** | CN-EN-000001; AC-EN-000001; RK/MT-EN-000001; AC-DM-*; CN-CA or CN-FI as applicable | OP-LU-000001; ST-PG-000001 | Full decision set |
| **CS-ENP** | ST-BU-000001; CN-BU-000001; AC-BU-000001; RK/MT-BU-000001; OP-BU-000002 | RK/MT-BU-000003; CN-LE-000001; OP-BU-000001 | Exec, Reasoning, Impact, Recommendation, Warning, Conclusion |
| **CS-RT** | ST-PG-000002; CN-FI-000003; PG-LS-000004; AC-FI-000004 | CN-LU-000001; RK/MT-FI-000001 | Impact, Recommendation, Warning, Conclusion |
| **Default Result** | CS-ID Required ∪ CS-LT light (CN-LU-000001, AC-LU-000001) ∪ CS-MD light (AC-DM-000001/6/7) ∪ structural RK/MT-XX if signals | Life CN/AC only if evidence supports | Full Pack 05 grammar |

Short ids in the table omit the `KU-` prefix for readability; full ids are `KU-…` as in `16`.

---

## 3. Completeness rules

| Rule | Detail |
|------|--------|
| Required unmet | Scenario → `partial_insufficient` if selected |
| Optional unmet | Allowed |
| Warning | Required whenever any Required/conditional RK selected |
| Mitigation | Required whenever RK selected (paired MT) |
| Advance posture | Requires OP or explicit strength support + Risk gate |

---

## 4. Cross-scenario reuse hotspots

| KU family | Reused by |
|-----------|-----------|
| AC-DM postures | CS-MD, CS-CC, CS-RL, CS-IV, default |
| RK/MT-XX structural | CS-LT, CS-MD, default |
| AN-ID identity set | CS-ID, CS-PG, default |
| CN/AC luck set | CS-LT, CS-CA, CS-ST, CS-RL |

---

## 5. Stop line

Scenario matrix complete. No population.

---

END
