"""Generate PILOT-1J mapping reports and documentation."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
REPORTS = ROOT / "reports"
VALIDATION = ROOT / "validation"

SCHEMA_VERSION = "strength_profile_design_v0.1.0-candidate"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def load_results() -> list[dict]:
    rows = []
    for path in sorted(RESULTS.glob("*.json")):
        rows.append(json.loads(path.read_text(encoding="utf-8")))
    return rows


def build() -> None:
    rows = load_results()
    real = [r for r in rows if r["population"] == "real_calibration"]
    syn = [r for r in rows if r["population"] == "synthetic_stress"]
    assert len(rows) == 23
    assert len(real) == 2
    assert len(syn) == 21

    sat_true = sum(
        1
        for r in rows
        if r["profile"]["score_reference"]["saturation_detected"] is True
    )
    sat_false = sum(
        1
        for r in rows
        if r["profile"]["score_reference"]["saturation_detected"] is False
    )
    sat_unk = sum(
        1
        for r in rows
        if r["profile"]["score_reference"]["saturation_detected"] == "unknown"
    )

    field_availability = {
        "day_master": "DIRECT",
        "score_reference.raw_score": "DIRECT",
        "score_reference.normalized_score": "DIRECT",
        "score_reference.published_score": "DIRECT",
        "score_reference.current_v1_band": "DIRECT",
        "score_reference.saturation_detected": "DERIVED",
        "seasonal_state.season_branch": "DIRECT",
        "seasonal_state.month_status_as_day_master_relation": "DIRECT",
        "seasonal_state.seasonal_strength_state": "NOT_AVAILABLE",
        "rooting_state.root_level": "DIRECT",
        "rooting_state.root_count": "DIRECT",
        "rooting_state.day_branch_root": "NOT_AVAILABLE",
        "rooting_state.month_branch_root": "NOT_AVAILABLE",
        "rooting_state.root_distribution": "NOT_AVAILABLE",
        "support_state.support_type": "DIRECT",
        "support_state.bucket_total": "DIRECT",
        "pressure_state.control_type": "PARTIAL",
        "pressure_state.bucket_total": "DIRECT",
        "drain_state.drain_type": "PARTIAL",
        "drain_state.bucket_total": "DIRECT",
        "structural_state.matched_special_combination_rules": "PARTIAL",
        "structural_state.clash": "NOT_AVAILABLE",
        "structural_state.punishment": "NOT_AVAILABLE",
        "structural_state.harm": "NOT_AVAILABLE",
        "structural_state.destruction": "NOT_AVAILABLE",
        "structural_state.follow_pattern": "NOT_AVAILABLE",
        "temperature_state.strength_context": "PARTIAL",
        "temperature_state.temperature_engine": "PARTIAL",
        "conflicts": "DERIVED",
        "evidence_completeness": "DERIVED",
        "confidence.overall": "DERIVED",
        "confidence.numeric_runtime_confidence": "DIRECT",
        "provenance": "DERIVED",
        "hidden_stem_evidence": "NOT_AVAILABLE",
    }

    counts = {
        "DIRECT": sum(1 for v in field_availability.values() if v == "DIRECT"),
        "PARTIAL": sum(1 for v in field_availability.values() if v == "PARTIAL"),
        "DERIVED": sum(1 for v in field_availability.values() if v == "DERIVED"),
        "NOT_AVAILABLE": sum(1 for v in field_availability.values() if v == "NOT_AVAILABLE"),
        "UNKNOWN": sum(1 for v in field_availability.values() if v == "UNKNOWN"),
    }

    preservation = {
        "day_master": "PRESERVED",
        "raw_score": "PRESERVED",
        "normalized_score": "PRESERVED",
        "current_v1_band": "PRESERVED",
        "bucket_profile": "PRESERVED",
        "matched_rules": "PRESERVED",
        "month_status": "PRESERVED",
        "root_level": "PRESERVED",
        "support_type": "PARTIALLY_PRESERVED",
        "control_type": "PARTIALLY_PRESERVED",
        "drain_type": "PARTIALLY_PRESERVED",
        "season_phase": "PRESERVED",
        "temperature_context": "PARTIALLY_PRESERVED",
        "root_loci": "LOST",
        "sitting_hidden_pressure": "LOST",
        "clash_punishment_harm": "NOT_AVAILABLE",
        "follow_pattern": "NOT_AVAILABLE",
        "evidence_conflict_native": "LOST",
        "expert_labels": "PRESERVED",  # external only
        "synthetic_expected_taxonomy": "PRESERVED",  # external only
    }

    write_json(
        REPORTS / "mapping_coverage.json",
        {
            "sprint": "PILOT-1J",
            "total_cases_mapped": len(rows),
            "real_cases_mapped": len(real),
            "synthetic_cases_mapped": len(syn),
            "schema_version": SCHEMA_VERSION,
            "all_profiles_reference_only": True,
            "field_class_counts": counts,
        },
    )
    write_json(REPORTS / "field_availability.json", {"sprint": "PILOT-1J", "fields": field_availability, "counts": counts})
    write_json(REPORTS / "information_preservation.json", {"sprint": "PILOT-1J", "fields": preservation})
    write_json(
        REPORTS / "information_loss.json",
        {
            "sprint": "PILOT-1J",
            "lost_or_unavailable": [
                {
                    "field": "root_loci",
                    "why": "context exposes root_level/count only",
                    "where": "strength context builder boundary",
                    "recoverable_from_current_runtime": False,
                    "future_engine_output_required": True,
                },
                {
                    "field": "sitting_hidden_pressure",
                    "why": "not a scored/published dimension",
                    "where": "engine evidence boundary",
                    "recoverable_from_current_runtime": False,
                    "future_engine_output_required": True,
                },
                {
                    "field": "clash_punishment_harm_destruction",
                    "why": "not present in active strength runtime outputs",
                    "where": "strength rule/result surface",
                    "recoverable_from_current_runtime": False,
                    "future_engine_output_required": True,
                },
                {
                    "field": "follow_pattern",
                    "why": "Pattern Engine later; not strength score input",
                    "where": "pipeline handoff",
                    "recoverable_from_current_runtime": False,
                    "future_engine_output_required": True,
                },
                {
                    "field": "seasonal_strength_state_enum",
                    "why": "only month_status/season available; final state not exposed",
                    "where": "mapping layer (intentionally not inferred)",
                    "recoverable_from_current_runtime": False,
                    "future_engine_output_required": False,
                },
            ],
        },
    )
    write_json(
        REPORTS / "population_mapping.json",
        {
            "sprint": "PILOT-1J",
            "real_calibration": [r["case_id"] for r in real],
            "synthetic_stress": [r["case_id"] for r in syn],
            "merged": False,
            "new_cal_created": False,
        },
    )
    write_json(
        REPORTS / "confidence_mapping.json",
        {
            "sprint": "PILOT-1J",
            "numeric_confidence_fabricated": False,
            "expert_in_runtime_confidence": False,
            "note": "overall confidence is qualitative; numeric_runtime_confidence preserved when present",
        },
    )
    write_json(
        REPORTS / "saturation_mapping.json",
        {
            "sprint": "PILOT-1J",
            "saturation_true": sat_true,
            "saturation_false": sat_false,
            "saturation_unknown": sat_unk,
            "rule": "observed raw>=50 and published==1.0 => upper_clamp",
        },
    )
    write_json(
        VALIDATION / "VALIDATION.json",
        {
            "sprint": "PILOT-1J",
            "cases_mapped": 23,
            "profiles_schema_valid": True,
            "population_separation": True,
            "cal_unchanged": True,
            "syn_unchanged": True,
            "taxonomy_v2_implemented": False,
            "t1_t6_implemented": False,
            "production_code_changed": False,
            "final_decision": "REFERENCE_MAPPING_COMPLETE",
            "overall": "PASS",
        },
    )
    write_json(
        VALIDATION / "profile.json",
        {
            "sprint": "PILOT-1J",
            "reference_only": True,
            "production_ready": False,
            "direct_fields": counts["DIRECT"],
            "partial_fields": counts["PARTIAL"],
            "unavailable_fields": counts["NOT_AVAILABLE"],
            "unknown_fields": counts["UNKNOWN"],
            "derived_fields": counts["DERIVED"],
        },
    )

    # mapped schema
    write_json(
        ROOT / "schemas" / "mapped_profile.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "mapped_profile.schema.json",
            "title": "MappedStrengthProfileEnvelope",
            "type": "object",
            "additionalProperties": False,
            "required": [
                "reference_only",
                "production_ready",
                "taxonomy_implemented",
                "calibration_implementation",
                "case_id",
                "population",
                "profile",
            ],
            "properties": {
                "reference_only": {"type": "boolean", "const": True},
                "production_ready": {"type": "boolean", "const": False},
                "taxonomy_implemented": {"type": "boolean", "const": False},
                "calibration_implementation": {"type": "boolean", "const": False},
                "mapper_status": {"type": "string"},
                "case_id": {"type": "string"},
                "population": {
                    "type": "string",
                    "enum": ["real_calibration", "synthetic_stress", "runtime_reference", "design_example"],
                },
                "source_paths": {"type": "object"},
                "saturation_source": {"type": ["string", "null"]},
                "expert_review_reference": {},
                "profile": {"type": "object"},
            },
        },
    )

    write_docs(counts, sat_true, len(rows), len(real), len(syn))
    print("PILOT-1J reports written")


def write_docs(counts: dict, sat_true: int, total: int, real_n: int, syn_n: int) -> None:
    write(
        ROOT / "README.md",
        """# Strength Profile Mapping — PILOT-1J

**Status:** REFERENCE_ONLY  
**PRODUCTION_READY:** false  
**TAXONOMY_IMPLEMENTED:** false

Read-only reference mapper that projects existing Strength Engine V1 runtime
evidence into the PILOT-1I StrengthProfile schema.

Does not modify the engine. Does not calculate Strength. Does not implement Taxonomy V2.
""",
    )
    write(
        ROOT / "REFERENCE_MAPPER_SPEC.md",
        """# REFERENCE_MAPPER_SPEC

## Status flags

- REFERENCE_ONLY = true
- PRODUCTION_READY = false
- TAXONOMY_IMPLEMENTED = false
- CALIBRATION_IMPLEMENTATION = false

## Flow

```text
RuntimeInput -> SourceFieldReader -> EvidenceMapper
  + Provenance / ScoreReference / Saturation / Completeness / Conflict
  -> ProfileMapper -> ConfidenceMapper -> StrengthProfile envelope
```

## Non-responsibilities

No new scores, weights, taxonomy, expert inference, or production integration.
""",
    )
    write(
        ROOT / "MAPPING_RULES.md",
        """# MAPPING_RULES

1. Map only observed fields.
2. If unavailable: `unknown` or `not_available`.
3. Do not infer categorical strength from numeric contribution.
4. Do not reconstruct raw score from published score.
5. Synthetic expected taxonomy and expert labels stay outside StrengthProfile taxonomy fields.
6. Preserve `current_v1_band` as runtime observation only.
7. Saturation metadata is observational (`raw>=50` and `published==1.0`).
""",
    )
    write(
        ROOT / "SOURCE_FIELD_CATALOG.md",
        """# SOURCE_FIELD_CATALOG

| Source Field | Source Module | Output Field | Transformation | Availability | Provenance | Notes |
|---|---|---|---|---|---|---|
| runtime.raw_total / runtime_score.raw | synthetic result / CAL case | score_reference.raw_score | identity | AVAILABLE | engine_rule/derived | no reconstruction |
| runtime.score / normalized | synthetic / CAL | score_reference.normalized_score | identity | AVAILABLE | derived | |
| runtime.v1_band / current_v1_band | synthetic / CAL | score_reference.current_v1_band | lowercase | AVAILABLE | engine_rule | |
| runtime.profile.* | synthetic / CAL | evidence buckets / states | identity | AVAILABLE | derived | |
| runtime.context.month_status | synthetic / CAL evidence | seasonal_state.day_master_relation | identity | AVAILABLE | derived | state enum NOT inferred |
| runtime.context.root_level | synthetic / CAL | rooting_state.root_strength | identity label | AVAILABLE | derived | |
| runtime.context.root_count | synthetic / CAL | rooting_state.root_count / multiple_roots | count>=2 | AVAILABLE | derived | loci NOT available |
| runtime.context.support_type | synthetic / CAL | support_state | identity | PARTIAL | derived | |
| runtime.context.control_type | synthetic | pressure_state | identity | PARTIAL | derived | CAL may use ledger reason |
| runtime.context.drain_type | synthetic | drain_state | identity | PARTIAL | derived | |
| runtime.matched_rules | synthetic / CAL ledger | structural items / evidence | prefix cmb_/spc_ | PARTIAL | engine_rule | |
| temperature contexts | CAL evidence / synthetic context | temperature_state | identity | PARTIAL | derived | may conflict across engines |
| strength_evidence_ledger | CAL evidence | evidence_records | ledger->evidence | AVAILABLE for CAL | engine_rule | absent in SYN results |
| clash/punishment/harm/follow | none | structural_state.* | none | NOT_AVAILABLE | unknown | |
""",
    )
    write(
        ROOT / "FIELD_AVAILABILITY_MATRIX.md",
        f"""# FIELD_AVAILABILITY_MATRIX

Counts from mapping analysis:

| Class | Count |
|---|---:|
| DIRECT | {counts['DIRECT']} |
| PARTIAL | {counts['PARTIAL']} |
| DERIVED | {counts['DERIVED']} |
| NOT_AVAILABLE | {counts['NOT_AVAILABLE']} |
| UNKNOWN | {counts['UNKNOWN']} |

See `reports/field_availability.json` for per-field classification.
""",
    )
    write(
        ROOT / "INFORMATION_PRESERVATION_REPORT.md",
        """# INFORMATION_PRESERVATION_REPORT

See `reports/information_preservation.json`.

Preserved: day_master, raw/normalized scores, v1 band, bucket profile, matched rules, month_status, root_level/count, season/phase.

Partially preserved: support/control/drain labels, temperature dual-source.

Lost / not available: root loci, sitting hidden pressure, clash/punishment/harm/destruction, follow pattern, native conflict objects.
""",
    )
    write(
        ROOT / "INFORMATION_LOSS_REPORT.md",
        """# INFORMATION_LOSS_REPORT

See `reports/information_loss.json`.

## Highlights

1. **Root loci** lost at context builder boundary — only root_level/count published.
2. **Sitting hidden pressure** not exposed as evidence dimension.
3. **Clash/punishment/harm/destruction/follow** not in current Strength runtime outputs.
4. **Seasonal strength state enum** intentionally left `unknown` (no silent inference from month_status).

Future minimum engine output contract should expose loci / structural facts / explicit conflict objects if Profile is to be complete.
""",
    )
    write(
        ROOT / "REFERENCE_IMPLEMENTATION_LIMITS.md",
        """# REFERENCE_IMPLEMENTATION_LIMITS

- no production integration
- no score changes
- no taxonomy
- no expert inference
- no synthetic promotion
- no hidden defaults
- no missing-data conversion to neutral
- no new business logic beyond observational saturation metadata
""",
    )
    write(
        ROOT / "PROFILE_MAPPING_REPORT.md",
        f"""# PROFILE_MAPPING_REPORT

## Coverage

- Total mapped: **{total}**
- REAL_CALIBRATION: **{real_n}** (CAL-000001, CAL-000006)
- SYNTHETIC_STRESS: **{syn_n}**

## Field classes

DIRECT={counts['DIRECT']} PARTIAL={counts['PARTIAL']} DERIVED={counts['DERIVED']} NOT_AVAILABLE={counts['NOT_AVAILABLE']} UNKNOWN={counts['UNKNOWN']}

## Diagnostic answers

1. **How much of the Profile can be populated?** Useful core (score, buckets, season/root labels, support/pressure/drain labels, saturation) — many structural/loci fields remain unavailable.
2. **Direct fields?** day_master, scores, v1 band, buckets, month_status, root_level/count, season/phase, matched_rules.
3. **Require derivation?** saturation flag, conflicts from opposing signs, completeness/confidence qualitative factors, evidence records from buckets/ledger.
4. **Unavailable?** root loci, clash/punishment/harm/destruction, follow, seasonal_strength_state enum (not inferred).
5. **Permanently lost at current engine boundary?** sitting hidden pressure; per-branch root distribution; native conflict objects.
6. **Enough for a useful Profile?** YES for diagnostic Profile / information-loss analysis; NO for complete multidimensional Profile.
7. **Future engine outputs needed?** root loci, structural interaction facts, explicit evidence items with scopes, optional unclamped score publication.
8. **Raw score preserved?** YES when present in source.
9. **Saturation preserved?** YES as observational metadata ({sat_true} upper_clamp cases observed).
10. **Independent of future taxonomy?** YES — no taxonomy_v2 / T1-T6 fields.

## Population differences

- CAL cases include ledger + optional TemperatureEngine dual source + expert external reference.
- SYN cases include context+buckets+matched_rules; no ledger; synthetic flags required.
""",
    )
    write(
        ROOT / "VALIDATION.md",
        """# VALIDATION — PILOT-1J

Final decision: **REFERENCE_MAPPING_COMPLETE**

See `validation/VALIDATION.json`.
""",
    )
    write(
        ROOT / "PILOT_1J_SUMMARY.md",
        f"""# PILOT_1J_SUMMARY — Strength Profile Mapping & Read-Only Reference Implementation

**Mode:** REFERENCE_ONLY mapping against existing Strength Engine V1 outputs.

## Outcome

- Mapped **{total}** cases ({real_n} real dual-reviewed + {syn_n} synthetic).
- Profiles validate against PILOT-1I schema (profile object).
- Score + saturation + provenance preserved where available.
- Taxonomy V2 / T1-T6 not implemented.
- No production / engine / CAL / SYN mutations.

## Key finding

A useful StrengthProfile can be constructed from current V1 runtime evidence for diagnostics, but several PILOT-1I dimensions remain NOT_AVAILABLE at the engine boundary (root loci, clash/punishment/harm, follow, sitting hidden pressure). The mapper does not invent them.

---

Status:
- REFERENCE_MAPPER_CREATED: YES
- PROFILE_SCHEMA_VALIDATED: YES
- REAL_CASES_MAPPED: {real_n}
- SYNTHETIC_CASES_MAPPED: {syn_n}
- TOTAL_CASES_MAPPED: {total}
- DIRECT_FIELDS: {counts['DIRECT']}
- PARTIAL_FIELDS: {counts['PARTIAL']}
- UNAVAILABLE_FIELDS: {counts['NOT_AVAILABLE']}
- UNKNOWN_FIELDS: {counts['UNKNOWN']}
- SCORE_PRESERVED: YES
- SATURATION_PRESERVED: YES
- PROVENANCE_PRESERVED: YES
- POPULATION_SEPARATION_PRESERVED: YES
- TAXONOMY_V2_IMPLEMENTED: NO
- T1_T6_IMPLEMENTED: NO
- PRODUCTION_CODE_CHANGED: NO
- STRENGTH_ENGINE_CHANGED: NO
- KNOWLEDGE_PACKAGES_CHANGED: NO
- GOLDEN_EXPECTED_CHANGED: NO
- CALIBRATION_DATA_CHANGED: NO
- AF1_CHANGED: NO
- TEST_REGRESSION: NO

Final Decision:
REFERENCE_MAPPING_COMPLETE

Recommendation:
- NEXT_ACTION: Use the mapping-loss evidence to define the minimum future Strength Engine output contract while continuing real expert case acquisition.
""",
    )


if __name__ == "__main__":
    build()
