# N-IMP-02 EVIDENCE BUILDER REPORT

Sprint: N-IMP-02
Module: engines/narrative_v2/evidence
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

Evidence Builder extracts published CanonicalAnalysis facts into
NarrativeEvidenceContext. It does not interpret, calculate, or write
customer narrative.

---

## 2. Canonical schema audit

Source of truth: orchestrator public payload
(`applications/api/services/orchestrator.py` + AnalysisResult views).

Audited published slices used for extraction:

| Domain | Canonical path | Notes |
|--------|----------------|-------|
| identity | `identity.person.*` | name/place empty on orchestrator payload |
| calendar | `calendar.solar_date`, `lunar_date`, `solar_term.name`, timezone wrapper `.name` |
| bazi | `bazi.day_master`, four `*_pillar` (stem/branch/nap_am/truong_sinh/hidden_stems/ten_god) |
| strength | `strength.strength_level`, `strength.strength_score` |
| temperature | `temperature.climate_state`, `temperature.balancing_need` |
| pattern | `pattern.pattern`, `pattern.cach_cuc`, `pattern.than_vuong_nhuoc` |
| useful_god | `useful_god.useful_god`, stem/element/ten_god, favorable/unfavorable |
| five_elements | `five_elements.{wood,fire,earth,metal,water}.count`, `dominant` |
| ten_gods | `ten_gods.visible_labels`, `hidden_labels`, `visible.{pillar}.ten_god` |
| shensha | `bazi.shensha`, `bazi.shensha_matches.{id}` |
| luck | `luck.direction`, `start_age`, `current_cycle.gan_zhi`, `cycles.{n}.gan_zhi` |
| analysis_id | `analysis_id` / `request_id` | only stamped by API layer |

Ignored (not evidence):

`interpretation`, `narrative`, `narrative_result`, `report`,
`commercial_consulting`, `integrated_narrative`, `customer`,
`reasoning`, `recommendations`, `customer_reason`, `luck_summary`.

---

## 3. Evidence architecture

```
CanonicalAnalysis (published mapping)
        ↓
EvidenceBuilder
        ↓
NarrativeEvidenceContext
        ↓
Runtime stage build_evidence
```

Logic lives in `engines/narrative_v2/evidence/`.
Runtime only calls the builder at the `build_evidence` boundary.

---

## 4. Files created

```
engines/narrative_v2/evidence/__init__.py
engines/narrative_v2/evidence/evidence_builder.py
engines/narrative_v2/evidence/evidence_context.py
engines/narrative_v2/evidence/evidence_item.py
engines/narrative_v2/evidence/evidence_reference.py
engines/narrative_v2/evidence/evidence_registry.py
engines/narrative_v2/evidence/evidence_validator.py
engines/narrative_v2/evidence/evidence_errors.py
tests/narrative_v2/conftest.py
tests/narrative_v2/test_evidence_builder.py
tests/narrative_v2/test_evidence_context.py
tests/narrative_v2/test_evidence_validator.py
tests/narrative_v2/test_evidence_runtime_integration.py
implementation/narrative_v2/n_imp_02/case0001_evidence_trace.json
implementation/narrative_v2/N_IMP_02_REPORT.md
```

---

## 5. Files modified

```
engines/narrative_v2/runtime/runtime_pipeline.py
engines/narrative_v2/runtime/runtime_context.py
tests/narrative_v2/test_runtime_skeleton.py
```

Pack05, Portal, API production path, astrology engines, and
`knowledge/narrative_v2/` were not modified.

`test_runtime_skeleton.py` was updated only so `build_evidence` is no
longer asserted as NotImplemented, matching this sprint contract.

---

## 6. Supported domains

identity, calendar, bazi, strength, temperature, pattern,
useful_god, five_elements, ten_gods, shensha, luck

---

## 7. Evidence item contract

```
EvidenceItem
  evidence_id
  domain
  key
  label
  value
  source_path
  status
  references
  metadata
```

Value is scalar or tuple of scalars only.
No dict dump. No customer prose. No UUID.

---

## 8. Evidence id strategy

Deterministic ids, no random UUIDs.

Examples:

- `evidence.identity.gender`
- `evidence.bazi.day_master`
- `evidence.strength.level`
- `evidence.pattern.primary`
- `evidence.useful_god.primary`
- `evidence.ten_gods.visible.year`
- `evidence.shensha.hong_luan.month`
- `evidence.luck.current_cycle`
- `evidence.luck.cycle.{index}`

---

## 9. Source traceability

Every available item has a real CanonicalAnalysis path, e.g.:

- `bazi.day_master`
- `strength.strength_level`
- `pattern.pattern`
- `ten_gods.visible.year.ten_god`
- `luck.current_cycle.gan_zhi`

Paths are not invented. Published name wrappers (`timezone.name`,
`solar_term.name`) are unwrapped to a scalar.

---

## 10. Missing-field policy

If a catalog field is absent or empty:

status = `missing`
value = `None`

No inference. No local calculation. No fill-in.

---

## 11. Evidence validation

`EvidenceValidator` checks:

- allowed domains
- deterministic `evidence.*` ids
- no duplicate ids
- source paths not from narrative/report/portal slices
- no customer-prose markers
- no raw debug/runtime objects

Validator does not interpret astrology.

---

## 12. Runtime integration

`build_evidence` is implemented.

payload = `NarrativeEvidenceContext`

Later stages remain `NotImplemented`:

```
initialize
↓
build_evidence = IMPLEMENTED
↓
build_reasoning = NotImplemented
↓
resolve_knowledge = NotImplemented
↓
commercial_rewrite = NotImplemented
↓
build_summary = NotImplemented
↓
build_interpretation = NotImplemented
↓
build_action = NotImplemented
↓
build_commercial = NotImplemented
↓
validate
↓
publish
```

`NarrativeRuntimeResult.presentation` remains `None`.
Shadow mode unchanged.

---

## 13. CASE-0001 evidence summary

Real CASE-0001 via `OrchestratorService.run_stage("luck")`.
Not hardcoded.

| Fact | Extracted value | Source path |
|------|-----------------|-------------|
| Day master | Canh | bazi.day_master |
| Year / month / day / hour | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | bazi.*_pillar |
| Strength | strong (0.87) | strength.strength_level / strength_score |
| Pattern code | chinh_an | pattern.pattern |
| Cách cục | Chính Ấn | pattern.cach_cuc |
| Useful god | Chính Quan (stem Đinh / Hỏa) | useful_god.useful_god |
| Five elements wood count | 4 | five_elements.wood.count |
| Visible ten gods | Thất Sát · Kiếp Tài · Nhật Chủ · Thiên Ấn | ten_gods.visible_labels |
| ShenSha names | Thiên Ất Quý Nhân, Hồng Loan, Thiên Đức, Nguyệt Đức | bazi.shensha |
| Current luck | Ất Tỵ | luck.current_cycle.gan_zhi |
| Next luck | Bính Ngọ | luck.cycles.4.gan_zhi |
| Direction / start age | forward / 5 | luck.direction / luck.start_age |

Trace: `implementation/narrative_v2/n_imp_02/case0001_evidence_trace.json`

83 items, 80 available, 3 missing (contract gaps).

---

## 14. Contract gaps

EVIDENCE CONTRACT GAP — not repaired in this sprint:

| Requested field | Canonical path | Status |
|-----------------|----------------|--------|
| name | identity.person.full_name | not published by OrchestratorService |
| birth place | identity.person.birth_place | not published by OrchestratorService |
| analysis id | analysis_id | stamped only by API `result_identity`, not by orchestrator payload |

Do not fill locally. Do not modify engines.

---

## 15. Tests

```
py -m pytest tests/narrative_v2 -q
52 passed
```

Coverage: E1–E15 and negative meaning tests.

---

## 16. Determinism verification

Same CASE-0001 CanonicalAnalysis produces identical EvidenceItem tuples
on two builds. Ids are stable. No timestamps in evidence values.

---

## 17. Shadow mode verification

- SHADOW_MODE = True
- replaces_pack05 = False
- portal_connected = False
- presentation = None
- Evidence package does not import Pack05 or Portal
- Production still reads Pack05

---

## 18. Out-of-scope confirmation

| Item | Confirmed |
|------|-----------|
| No Reasoning Builder implemented | YES |
| No Knowledge Resolver implemented | YES |
| No Rewrite implemented | YES |
| No Summary implemented | YES |
| No Interpretation implemented | YES |
| No Action implemented | YES |
| No Portal integration | YES |
| No Pack05 replacement | YES |
| No customer narrative generation | YES |
| No astrology engine modified | YES |

---

## 19. Verdict

READY FOR PRODUCT OWNER REVIEW

STOP.

Do not start N-IMP-03.
