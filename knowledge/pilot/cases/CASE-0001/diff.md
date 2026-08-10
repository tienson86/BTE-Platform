# CASE-0001 Diff

## Verdict

Status: **WARNING**

The real orchestration pipeline ran from input through calendar, BaZi, pattern, score, interpretation, report, and narrative. Calendar and BaZi match the user-confirmed input. Later interpretive stages are not accepted as golden yet because they need expert review and show internal inconsistencies.

## Expected vs Actual

| Area | Expected | Actual | Result |
|---|---|---|---|
| Solar birth | 1987-01-21 04:30, Asia/Ho_Chi_Minh, Hà Nội | 21/01/1987 04:30 | PASS |
| Lunar date | 22/12/1986, Bính Dần year | 22/12/Bính Dần, lunar_year 1986 | PASS |
| Year pillar | Bính Dần | Bính Dần | PASS |
| Month pillar | Tân Sửu | Tân Sửu | PASS |
| Day pillar | Canh Ngọ | Canh Ngọ | PASS |
| Hour pillar | Mậu Dần | Mậu Dần | PASS |
| Day master | Canh Kim, Dương | Canh Kim, Dương | PASS |
| Hidden stems | Standard Dần/Sửu/Ngọ hidden stems | Matches expected tables | PASS |
| Visible-stem Ten Gods | Bính=Thất Sát, Tân=Kiếp Tài, Canh=Nhật Chủ, Mậu=Thiên Ấn | Matches expected tables | PASS |
| Strength | Requires expert validation | `strong`, score `0.87`, reasoning `Thân vượng` | REVIEW |
| Pattern strength label | Must be consistent with accepted strength result | `Trung hòa` while Strength stage is `strong` | WARNING |
| Interpretation strength label | Must be consistent with accepted strength result | text says `balanced` while Strength stage is `strong` | WARNING |
| Temperature | Requires expert validation | `hot`, but cold_score `0.58` and mixed warming/cooling recommendations | REVIEW |
| Useful God | Requires expert validation | `Thực Thần`; text also says `(Không có Dụng thần)` | WARNING |
| Score | Requires scoring rubric acceptance | total `51.25`, grade `D+` | REVIEW |
| Report | Should render once interpretation is available | markdown/html present, 10 sections | PASS_WITH_REVIEW |
| Portal DOM replay | Should be verified through live portal | Not run; live server was not started | BLOCKED |

## Findings

### CASE-0001-F01: Strength label mismatch

Severity: P1  
Type: interpretation / pipeline consistency  
Status: Open

The Strength stage returns `strength_level=strong` and `reasoning=Thân vượng`, but Pattern returns `than_vuong_nhuoc=Trung hòa`, and Interpretation text says `balanced`. This should be investigated before promoting this case to golden.

### CASE-0001-F02: Useful God copy contradiction

Severity: P1  
Type: interpretation text  
Status: Open

The useful-god actual output is `Thực Thần`, but the report sentence says `Dụng thần: Thực Thần (Không có Dụng thần)`. This is internally contradictory and should not be accepted as final report copy.

### CASE-0001-F03: Temperature semantics need review

Severity: P2  
Type: engine semantics / wording  
Status: Open

Temperature returns `temperature_level=hot` while the score components include `cold_score=0.58` and recommendations mix cooling and warming actions. This may be valid according to package semantics, but it needs explicit expert confirmation.

### CASE-0001-F04: Portal replay blocked

Severity: P2  
Type: test infrastructure  
Status: Blocked

The repository has `validation/live_e2e_trace.py` for portal replay, but the live portal/API server was not started in this run. No DOM-level portal pass is claimed.

## Architecture Freeze

No engine, Knowledge, API, UI, deployment, or portal files were changed to make expected match actual.
