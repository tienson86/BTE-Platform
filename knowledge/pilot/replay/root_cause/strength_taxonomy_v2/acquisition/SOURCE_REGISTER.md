# Source Register

**Sprint:** PILOT-1E  
**Privacy:** No full names, phones, addresses, national IDs, or emails in calibration artifacts.

## Allowed provenance classes

| Class | Counts toward calibration coverage? | Notes |
|---|---|---|
| EXISTING_PILOT | Yes (provisional until dual) | CAL-000001…007 |
| EXISTING_GOLDEN | Only after new expert labels | Do not mutate Expected |
| EXPERT_SUPPLIED | Yes if verified + dual | Preferred for gaps |
| VERIFIED_REFERENCE | Yes if license/provenance clear | Document license |
| SYNTHETIC | **No** | Engineering only |
| UNKNOWN | **No** | Reject from verified pool |

## Registered sources

| source_id | class | description | license/access | cases | status |
|---|---|---|---|---|---|
| SRC-PILOT-001 | EXISTING_PILOT | Pilot replay CASE-0001…0007 | Internal pilot | CAL-000001…007 | ACTIVE |
| SRC-EXPERT-PENDING | EXPERT_SUPPLIED | Authorized expert chart intake | Pending human supply | — | WAITING (PILOT-1F) |
| SRC-USER-PENDING | EXPERT_SUPPLIED / user | Authorized user charts (anonymized) | Pending consent + intake | — | WAITING (PILOT-1F) |

## Reviewer IDs (anonymized)

| reviewer_id | role | availability |
|---|---|---|
| EXPERT-A | Primary Strength reviewer | Available for new intake; historical refs for CAL-000001…007 |
| EXPERT-B | Independent second reviewer | Completed CAL-000001 / CAL-000006; available for new intake |
| ADJUDICATOR-1 | Disagreement adjudicator | Standby |

## Rejected / not registered

| Candidate | Reason |
|---|---|
| Fabricated charts | Forbidden |
| Unlicensed public celebrity lists | Provenance/privacy unclear |
| Synthetic generators as ground truth | Forbidden for coverage counts |
