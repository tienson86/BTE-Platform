# MC01-IMP-01 RUNTIME REPORT

## Status
PASS

## Canonical MC-01 runtime owner
`engines.mingju.engine.MingJuDecisionEngine`

Public API:

- `engines.mingju.analyze_mingju`
- `engines.mingju.build_mingju_context`
- `engines.mingju.compose_mingju_decision`
- `engines.mingju.MingJuDecisionResult`

Live pipeline owner: `OrchestratorService._attach_mingju_decision` in `applications/api/services/orchestrator.py`, after Pattern / Strength / Temperature / Useful God / Ten Gods facts and before Pack 07 `attach_mc01_reference()`.

## Upstream inputs
Consumed, not recalculated:

- Pattern Engine (`data.pattern`)
- Strength Engine Day Master Strength (`data.strength`) — input only, never used as Pattern Strength
- Temperature Engine (`data.temperature`)
- Useful God Engine (`data.useful_god`)
- Ten Gods Engine facts (`data.ten_gods` visible/hidden)
- Five Elements (`data.five_elements`)
- BaZi identity / four pillars (`data.bazi`, hour completeness)

ScoreEngine is **not** an MC-01 input for Grade.

## MingJuDecisionResult
Root metadata published:

- `analysis_id` / `chart_id`
- `schema_version` = `bte.mingju.decision.v1`
- `ruleset_version` = `bte.mingju.rules.v1`
- `result_id` = `mc01:{analysis_id}` when present
- `content_hash`
- `status` = `complete` on CASE-0001
- `confidence`
- `trace_ids`

Customer JSON does **not** leak `mc01`, `mingju`, hashes, or Pack 07 context. Structural labels are stamped onto `data.pattern` (`structural_purity`, `structural_strength`, `structural_integrity`, `structural_grade`, `customer_summary`). Canonical IDs `damage_ids` / `rescue_ids` are published for Pack 07 re-resolution.

## Pattern
CASE-0001 live:

- `pattern_id` = `zheng_yin`
- `label` = Chính Ấn
- `family` = `standard`
- `source` = `canonical_pattern_engine`

## Purity
CASE-0001 live:

- classification = `mixed` (Độ thuần: Pha tạp)
- score = `54.0`
- confidence = `0.88`

Mixing is scored independently of Damage and Grade.

## Pattern Strength
CASE-0001 live:

- classification = `moderate` (Lực cách: Vừa)
- score = `57.28`

This is **not** Day Master Strength. Day Master Strength on this chart remains the Strength Engine value used by ScoreEngine; Pattern Strength is computed from pattern-deity season / root / exposure / generation / continuity / position.

## Damage
CASE-0001 live confirmed finding:

- `damage_id` = `DMG-MC-001`
- type = `resource_overload`
- source = `resource`
- target = `output`
- severity = `moderate`
- confidence = `0.76`
- evidence_ids and trace_ids present

Co-presence alone does not confirm Damage. Tests cover residual hidden Thương/Quan co-presence without confirmation.

## Rescue
CASE-0001 live:

- `rescue_id` = `RSC-MC-001`
- type = `output_releases_excess`
- `target_damage_ids` = `DMG-MC-001`
- strength = `minor`

No Rescue without a registered Damage. Validator fails closed on orphan Rescue.

## Integrity
CASE-0001 live:

- state = `mixed` (Toàn vẹn: Hỗn hợp)
- score = `64.1`
- residual_damage = `moderate`

Integrity consumes Purity, Pattern Strength, Support, Damage, Rescue, Useful God compatibility, and climate compatibility. It does not duplicate Grade.

## Grade
CASE-0001 live:

- MC-01 Grade = **B**
- score = `64.1`
- basis = `structural_integrity`
- enum = SS / S / A / B / C / D / UNRESOLVED

ScoreEngine customer grade on the same chart = **D+**.

## Score Grade semantic audit
**DIFFERENT**

ScoreEngine grade (`data.score.grade`) is a customer composite letter from weighted module scores (`S+` … `D+` … `E` via `database/15_score_engine/09_final_score/01_grade.csv`). CASE-0001 `D+` means total score in 50–59.

MC-01 Grade is natal **structural integrity quality** of the pattern (SS/S/A/B/C/D). It is downstream of Integrity only. It must not mean giàu/nghèo/quan.

Therefore ScoreEngine `D+` is **not** bound as MC-01 Grade. Fresh analyze publishes `pattern.structural_grade = B`.

## Achievement
CASE-0001 live dominant capabilities: academic, entrepreneurship, management.

Dimension classifications (usable potential, not biography / status prediction):

- academic = high (76.92)
- entrepreneurship = high (74.61)
- management = high (73.07)
- authority / institutional_career / leadership = above_average
- independence / stability / technical = moderate
- creative / public_visibility = below_average

## Wealth Profile
Frozen dimensions preserved. Not “Tài nhiều = giàu”.

- wealth_creation = below_average (higher_is_better)
- wealth_accumulation = above_average
- wealth_retention = above_average
- business_expansion = moderate
- financial_volatility = above_average (**higher_is_riskier**)

## Career Profile
Work-style fit, not exact professions.

Dominant styles: academic_research, managerial, leadership_command.

- academic_fit = high
- management_fit = high
- leadership_fit / institutional_fit / entrepreneurial_fit = above_average
- specialist/technical = moderate
- creative / public_facing = below_average

## Pack 07 binding
Before (P7-IMP-07 surrogate): Pattern + ScoreEngine grade `D+`. Purity / Damage / Rescue / Integrity / Achievement / Wealth / Career unpublished.

After: `attach_mc01_reference()` prefers `_mingju` / stamped MC-01 identifiers. Fresh analyze uses MC-01 Grade `B`, purity, integrity, `DMG-MC-001`, `RSC-MC-001`. Pattern+Score path remains only as a **labeled legacy surrogate** when no MC-01 stamp exists (keeps existing Pack 07 unit fixtures).

## Pack 07 re-resolution
Fresh CASE-0001 diagnostics after true MC-01:

- Ten Gods: **PASS**
- Combination: **PASS** (was PARTIAL under the surrogate with empty damage/rescue IDs)
- Ten Gods Ecosystem: **PASS**
- Shen Sha: **PASS**
- Shen Sha Ecosystem: **PARTIAL** (legitimate; individual matches still need more MC-01 structural conditions than this ticket owns)

No `NOT_BOUND` on fresh Analyze. `evidence_priority` / `domains` / Pack 07 narrative remain NOT_IMPLEMENTED / NOT_EVALUATED as required.

## Build
PASS — `python tools/build.py`

## Type Check
PASS — scoped mypy:

`python -m mypy --explicit-package-bases --follow-imports=skip engines/mingju`

29 files, no issues.

Portal `tsc --noEmit` still has pre-existing errors outside this ticket (luck DTO, unused locals, ResultStore types). Not repaired.

## Tests
MC-01: **29 passed** (`tests/mingju`)

Pack 07 + Pattern + Useful God + Analyze + History + PDF + DOCX + Portal python: **215 passed**

Strength module: **40 passed, 1 failed** — `tests/strength/test_g1_02r_strength_correctness.py::test_weak_fixture_ex002_profile` (`Tử` vs expected `Tướng`). Unrelated to MC-01. Not repaired.

Portal UI-08 Pattern card: **22 passed**, 1 pre-existing ResultStore boot failure (`resultSource` empty vs current). Not repaired.

## Runtime
- `POST /api/v1/analyze`
- `POST /api/v1/dev/pack07/diagnostics`
- Portal `/result` (existing MỆNH CỤC card)

CASE-0001: Nguyễn Tiến Sơn, male, 21/01/1987 04:30, Hà Nội. Analyze 200. History portal 200.

## Screenshots
- `implementation/pack_06/screenshots/mc01_imp_01_result_overview.png`
- `implementation/pack_06/screenshots/mc01_imp_01_mingju.png`
- `implementation/pack_06/screenshots/mc01_imp_01_grade_integrity.png`
- `implementation/pack_06/screenshots/mc01_imp_01_ten_gods.png`
- `implementation/pack_06/screenshots/mc01_imp_01_ten_gods_ecosystem.png`
- `implementation/pack_06/screenshots/mc01_imp_01_shen_sha.png`
- `implementation/pack_06/screenshots/mc01_imp_01_shen_sha_ecosystem.png`
- `implementation/pack_06/screenshots/mc01_imp_01_diagnostics.png`

Live dump: `implementation/pack_06/MC01-IMP-01_live_proof.json`

## Regression
PASS for in-scope modules, with two remaining unrelated failures documented above (Strength season label; Portal ResultStore boot).

## Files changed
Engine (new):

- `engines/mingju/__init__.py`
- `engines/mingju/api.py`
- `engines/mingju/engine.py`
- `engines/mingju/service.py`
- `engines/mingju/models.py`
- `engines/mingju/adapters.py`
- `engines/mingju/context.py`
- `engines/mingju/pattern.py`
- `engines/mingju/purity.py`
- `engines/mingju/pattern_strength.py`
- `engines/mingju/support.py`
- `engines/mingju/damage.py`
- `engines/mingju/rescue.py`
- `engines/mingju/compatibility.py`
- `engines/mingju/integrity.py`
- `engines/mingju/grade.py`
- `engines/mingju/achievement.py`
- `engines/mingju/wealth.py`
- `engines/mingju/career.py`
- `engines/mingju/composer.py`
- `engines/mingju/validators.py`
- `engines/mingju/views.py`
- `engines/mingju/facts.py`
- `engines/mingju/evidence.py`
- `engines/mingju/serialization.py`
- `engines/mingju/constants.py`
- `engines/mingju/enums.py`
- `engines/mingju/exceptions.py`
- `engines/mingju/versions.py`

Runtime / Pack 07 bridge:

- `applications/api/services/orchestrator.py`
- `applications/api/models/analysis_result.py`
- `engines/detailed_interpretation_engine/mc01.py`

UI bind (existing MỆNH CỤC card, no redesign):

- `applications/customer_portal/src/screens/commercial_dashboard/patternAdapter.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/PatternCard.tsx`
- `applications/customer_portal/src/screens/commercial_dashboard/types.ts`
- `applications/customer_portal/src/screens/commercial_dashboard/patternFixture.ts`
- `applications/customer_portal/src/models/dto.ts`

Tests:

- `tests/mingju/*`

Capture:

- `applications/customer_portal/scripts/capture_mc01_imp_01_live.py`

## Known limitations
- Numeric MC-01 weights are documented V1 provisional ruleset values, not Golden Dataset-calibrated.
- `damage_offset` stays null until calibration.
- Public customer JSON omits traces/hashes; Pack 07 re-binds from stamped structural fields + damage/rescue IDs.
- Shen Sha Ecosystem remains PARTIAL; individual Shen Sha customer states may still show “Chưa đủ dữ liệu” where Pack 07 rules require additional MC-01 conditions.
- Composer summary captured in screenshots still showed English `mixed` once; source now maps integrity to Vietnamese `hỗn hợp`.
- Unrelated Strength fixture `Tử`/`Tướng` and ResultStore boot failures remain.

## Next
STOP.

Wait for Product Owner approval before resuming P7 implementation.

Do not implement Pack 07 Evidence Priority.
Do not implement Domains.
