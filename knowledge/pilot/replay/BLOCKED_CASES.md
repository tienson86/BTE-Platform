# Blocked Cases

## CASE-0008 — REFERENCE_ONLY / blocked runtime

**block_reason:** `MISSING_BIRTH_DATETIME`

Provided:

- Pillars only: Quý Dậu / Giáp Tý / Mậu Tý / Nhâm Tý
- Day master: Mậu Thổ
- External classification: Follow Wealth / Tòng Tài (REFERENCE ONLY)

Blocked because:

- Canonical harness `OrchestratorService.analyze` requires solar birth datetime
- No birth datetime was supplied
- Inventing a datetime to force pillars would violate Pilot Replay rules

External expected is retained as `external_expected` only. Not treated as absolute ground truth.
Cannot evaluate strength / follow / transform / decision / luck / interpretation / report for this case without input completion.

## CASE-0009 — BLOCKED

**block_reason:** `BLOCKED_REFERENCE_DATA`

Intent: compare Combination detected vs Transformation detected.

Blocked because:

- No reliable birth/pillar reference transformation case was found in:
  - `knowledge/pilot/cases/`
  - Pilot fixtures created for this run
  - QC2 scenario catalog (slug `transformation` only; no birth chart payload)
  - repo search for a named transformation reference chart
- Fabricating CASE-0009 input is forbidden

Systemic note (even after data arrives):

- Production public orchestrator payload does not currently produce `transformation_*`
- Combination packages explicitly state they do not determine transformation

## Systemic blocks (all runnable cases)

| Layer | Status | Reason |
|---|---|---|
| Decision | BLOCKED | `DecisionEngine` not imported/called by `OrchestratorService` |
| Luck (public) | INTERNAL_ONLY | LuckEngine runs in Stage 7; `luck` stripped by `_INTERNAL_PAYLOAD_KEYS` |
| Transformation | NOT_PRODUCED | No transformation producer on public analyze payload |
| Portal DOM | BLOCKED | Live portal/API browser replay not started in this run |

## Needs data / needs contract

| Item | Need |
|---|---|
| CASE-0008 | Birth datetime (and gender if luck direction depends on it) |
| CASE-0009 | Verified reference chart + explicit combination vs transformation expectations |
| Decision column | Product decision to wire DecisionEngine into orchestrator or accept out-of-band harness |
| Luck column PASS | Public contract change or dedicated internal snapshot channel |
