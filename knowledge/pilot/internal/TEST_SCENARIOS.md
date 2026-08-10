# Test Scenarios

Version: 1.0.0  
Sprint: Beta-5

Scripted companions to journeys. Each row: ID, journey, data, expected.

| ID | Journey | Setup | Expected |
|----|---------|-------|----------|
| S-L01 | J1 Landing | Cold browser | Home/landing usable |
| S-A01 | J2 Create | Valid solar datetime + timezone | Accepted |
| S-A02 | J2 Create | Month 13 | Validation error, no crash |
| S-A03 | J2 Create | Unknown hour if UI allows | Accepted with caution or explicit unknown |
| S-A04 | J2 Create | Double-click submit | One analysis or clear duplicate handling |
| S-W01 | J3 Waiting | Valid create | Terminal success or terminal error |
| S-W02 | J3 Waiting | Refresh once mid-wait | No duplicate chaos **or** documented behavior |
| S-R01 | J4 Report | Completed analysis | Overview present |
| S-R02 | J4 Report | Header name/date | Matches input |
| S-K01 | J5 Knowledge | Known term in report | Article or graceful missing state |
| S-P01 | J6 PDF | If control exists | File opens |
| S-H01 | J7 Share | If control exists | Confirm audience |
| S-Y01 | J8 History | ≥1 completed case | Reopen works |
| S-U01 | J9 Return | New session next day | Resume possible |

Mark N/A with reason. Do not invent UI to make a scenario pass.

---

END
