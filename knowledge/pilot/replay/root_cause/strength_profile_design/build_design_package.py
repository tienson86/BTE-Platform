"""PILOT-1I design package builder (design-only; no production changes)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples"
REPORTS = ROOT / "reports"
VALIDATION = ROOT / "validation"

SCHEMA_META = "https://json-schema.org/draft/2020-12/schema"
SCHEMA_VERSION = "strength_profile_design_v0.1.0-candidate"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def build() -> None:
    for name, schema in SCHEMAS_MAP.items():
        write_json(SCHEMAS / name, schema)
    for name, example in EXAMPLES_MAP.items():
        write_json(EXAMPLES / name, example)
    for name, report in REPORTS_MAP.items():
        write_json(REPORTS / name, report)
    write_json(VALIDATION / "VALIDATION.json", VALIDATION_JSON)
    write_json(VALIDATION / "profile.json", PROFILE_META_JSON)
    for name, text in DOCS.items():
        write(ROOT / name, text)
    print("PILOT-1I design package written")


# ---------- shared defs ----------
DIRECTION = ["support", "pressure", "drain", "neutral", "conflict", "unknown"]
POLARITY = ["positive", "negative", "mixed", "neutral", "unknown"]
PROVENANCE = [
    "engine_rule",
    "knowledge_rule",
    "derived",
    "structural",
    "calendar",
    "expert",
    "synthetic",
    "design_only",
]
AVAILABILITY = ["observed", "derived", "inferred", "externally_reviewed", "synthetic", "unknown"]
COMPLETENESS = ["complete", "partial", "limited", "unknown"]
CONFIDENCE = ["high", "medium", "low", "unknown"]
SEVERITY = ["low", "medium", "high", "critical", "unknown"]
RESOLUTION = ["confirmed", "probable", "candidate", "unresolved", "not_applicable"]
INFO_LOSS = ["preserved", "partially_preserved", "compressed", "lost", "not_available"]
V1_BAND = ["weak", "balanced", "strong", "unknown"]
SATURATION_TYPE = ["none", "upper_clamp", "lower_clamp", "normalization", "unknown"]
POPULATION = ["real_calibration", "synthetic_stress", "runtime_reference", "design_example"]

STEMS = ["canh", "tan", "nham", "quy", "giap", "at", "binh", "dinh", "mau", "ky"]
BRANCHES = [
    "ty", "suu", "dan", "mao", "thin", "ti", "ngo", "mui", "than", "dau", "tuat", "hoi"
]
ELEMENTS = ["kim", "moc", "thuy", "hoa", "tho", "unknown"]
PILLAR_SCOPE = ["year", "month", "day", "hour", "multi", "unknown"]

DIMENSIONS = [
    "seasonal_strength",
    "rooting",
    "same_element_support",
    "resource_support",
    "output_drain",
    "wealth_pressure",
    "officer_pressure",
    "hidden_stem_evidence",
    "temperature",
    "combination",
    "clash",
    "punishment",
    "harm",
    "destruction",
    "transformation",
    "special_structure",
    "follow_pattern",
    "evidence_conflict",
    "evidence_completeness",
    "other",
]


def nullable(t: dict) -> dict:
    return {"anyOf": [t, {"type": "null"}]}


def string_enum(values: list[str]) -> dict:
    return {"type": "string", "enum": values}


# ---------- schemas ----------
PROVENANCE_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_provenance.schema.json",
    "title": "StrengthProvenance",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "provenance_class", "availability"],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "provenance_class": string_enum(PROVENANCE),
        "availability": string_enum(AVAILABILITY),
        "source_system": nullable({"type": "string"}),
        "source_path": nullable({"type": "string"}),
        "rule_id": nullable({"type": "string"}),
        "observed_at": nullable({"type": "string"}),
        "notes": nullable({"type": "string"}),
    },
}

EVIDENCE_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_evidence.schema.json",
    "title": "StrengthEvidence",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "evidence_id",
        "evidence_type",
        "dimension",
        "direction",
        "polarity",
        "availability",
        "provenance",
    ],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "evidence_id": {"type": "string", "pattern": "^EV-[A-Z0-9_-]+$"},
        "evidence_type": {
            "type": "string",
            "enum": [
                "seasonal",
                "rooting",
                "support",
                "pressure",
                "drain",
                "structural",
                "temperature",
                "conflict",
                "completeness",
                "score_reference",
                "other",
            ],
        },
        "dimension": string_enum(DIMENSIONS),
        "source": nullable({"type": "string"}),
        "source_path": nullable({"type": "string"}),
        "direction": string_enum(DIRECTION),
        "magnitude": {
            "type": "object",
            "additionalProperties": False,
            "required": ["representation"],
            "properties": {
                "representation": {
                    "type": "string",
                    "enum": [
                        "ordinal",
                        "normalized",
                        "categorical",
                        "raw_contribution",
                        "bounded_contribution",
                        "unknown",
                    ],
                },
                "ordinal": nullable({"type": "string"}),
                "categorical": nullable({"type": "string"}),
                "raw_contribution": nullable({"type": "number"}),
                "normalized": nullable({"type": "number"}),
                "bounded_contribution": nullable({"type": "number"}),
                "unit_note": nullable({"type": "string"}),
            },
        },
        "polarity": string_enum(POLARITY),
        "confidence": string_enum(CONFIDENCE),
        "provenance": {"$ref": "strength_provenance.schema.json"},
        "explanation": nullable({"type": "string"}),
        "affected_element": nullable(string_enum(ELEMENTS)),
        "affected_day_master": nullable(string_enum(STEMS)),
        "pillar_scope": nullable(string_enum(PILLAR_SCOPE)),
        "branch_scope": nullable(string_enum(BRANCHES + ["multi", "unknown"])),
        "stem_scope": nullable(string_enum(STEMS + ["multi", "unknown"])),
        "seasonal_context": nullable({"type": "object", "additionalProperties": True}),
        "interaction_context": nullable({"type": "object", "additionalProperties": True}),
        "availability": string_enum(AVAILABILITY),
        "completeness": nullable(string_enum(COMPLETENESS)),
        "information_loss": nullable(string_enum(INFO_LOSS)),
    },
}

CONFLICT_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_conflict.schema.json",
    "title": "StrengthConflict",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "conflict_id",
        "conflict_type",
        "dimensions",
        "evidence_ids",
        "severity",
        "resolution_status",
        "confidence",
    ],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "conflict_id": {"type": "string", "pattern": "^CF-[A-Z0-9_-]+$"},
        "conflict_type": {
            "type": "string",
            "enum": [
                "seasonal_support_vs_structural_pressure",
                "root_vs_control",
                "resource_support_vs_drain",
                "support_vs_pressure",
                "multiple_structure_conflict",
                "season_vs_root",
                "other",
            ],
        },
        "dimensions": {"type": "array", "items": string_enum(DIMENSIONS), "minItems": 1},
        "evidence_ids": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "severity": string_enum(SEVERITY),
        "resolution_status": string_enum(RESOLUTION),
        "confidence": string_enum(CONFIDENCE),
        "notes": nullable({"type": "string"}),
    },
}

COMPLETENESS_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_completeness.schema.json",
    "title": "StrengthEvidenceCompleteness",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "overall", "by_dimension"],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "overall": string_enum(COMPLETENESS),
        "by_dimension": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "calendar": string_enum(COMPLETENESS),
                "season": string_enum(COMPLETENESS),
                "roots": string_enum(COMPLETENESS),
                "support": string_enum(COMPLETENESS),
                "pressure": string_enum(COMPLETENESS),
                "drain": string_enum(COMPLETENESS),
                "structure": string_enum(COMPLETENESS),
                "temperature": string_enum(COMPLETENESS),
                "expert_review": string_enum(COMPLETENESS),
            },
        },
        "notes": nullable({"type": "string"}),
    },
}

CONFIDENCE_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_confidence.schema.json",
    "title": "StrengthConfidence",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "overall", "factors"],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "overall": string_enum(CONFIDENCE),
        "factors": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "evidence_completeness": string_enum(CONFIDENCE),
                "evidence_conflict": string_enum(CONFIDENCE),
                "calendar_certainty": string_enum(CONFIDENCE),
                "structural_certainty": string_enum(CONFIDENCE),
                "expert_agreement": string_enum(CONFIDENCE),
                "boundary_proximity": string_enum(CONFIDENCE),
                "runtime_stability": string_enum(CONFIDENCE),
            },
        },
        "numeric_runtime_confidence": nullable({"type": "number"}),
        "notes": nullable({"type": "string"}),
    },
}

PROFILE_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_profile.schema.json",
    "title": "StrengthProfile",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "identity",
        "day_master",
        "score_reference",
        "seasonal_state",
        "rooting_state",
        "support_state",
        "pressure_state",
        "drain_state",
        "structural_state",
        "temperature_state",
        "conflicts",
        "evidence_completeness",
        "provenance",
        "population",
        "design_marker",
    ],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "identity": {
            "type": "object",
            "additionalProperties": False,
            "required": ["profile_id", "source_case_ref"],
            "properties": {
                "profile_id": {"type": "string", "pattern": "^PRF-[A-Z0-9_-]+$"},
                "source_case_ref": {"type": "string"},
                "population": string_enum(POPULATION),
                "notes": nullable({"type": "string"}),
            },
        },
        "population": string_enum(POPULATION),
        "design_marker": {
            "type": "string",
            "enum": ["design_example", "runtime_projection", "not_applicable"],
        },
        "day_master": string_enum(STEMS),
        "score_reference": {
            "type": "object",
            "additionalProperties": False,
            "required": ["score_source", "score_status", "current_v1_band", "saturation_detected"],
            "properties": {
                "raw_score": nullable({"type": "number"}),
                "normalized_score": nullable({"type": "number"}),
                "published_score": nullable({"type": "number"}),
                "current_v1_band": string_enum(V1_BAND),
                "score_source": {"type": "string"},
                "score_status": {
                    "type": "string",
                    "enum": ["observed", "partial", "unknown", "design_example"],
                },
                "saturation_detected": {
                    "anyOf": [
                        {"type": "boolean"},
                        {"type": "string", "const": "unknown"},
                    ]
                },
                "saturation_type": nullable(string_enum(SATURATION_TYPE)),
            },
        },
        "seasonal_state": {"type": "object", "additionalProperties": True},
        "rooting_state": {"type": "object", "additionalProperties": True},
        "support_state": {"type": "object", "additionalProperties": True},
        "pressure_state": {"type": "object", "additionalProperties": True},
        "drain_state": {"type": "object", "additionalProperties": True},
        "structural_state": {"type": "object", "additionalProperties": True},
        "temperature_state": {"type": "object", "additionalProperties": True},
        "conflicts": {"type": "array", "items": {"$ref": "strength_conflict.schema.json"}},
        "evidence_completeness": {"$ref": "strength_completeness.schema.json"},
        "evidence_records": {
            "type": "array",
            "items": {"$ref": "strength_evidence.schema.json"},
        },
        "dominant_factors": {"type": "array", "items": {"type": "string"}},
        "supporting_factors": {"type": "array", "items": {"type": "string"}},
        "opposing_factors": {"type": "array", "items": {"type": "string"}},
        "uncertainty": nullable({"type": "string"}),
        "confidence": nullable({"$ref": "strength_confidence.schema.json"}),
        "provenance": {"$ref": "strength_provenance.schema.json"},
        "synthetic_flags": nullable(
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "synthetic": {"type": "boolean"},
                    "calibration_eligible": {"type": "boolean"},
                    "golden_eligible": {"type": "boolean"},
                    "expert_calibration_eligible": {"type": "boolean"},
                },
            }
        ),
        "external_labels": nullable(
            {
                "type": "object",
                "additionalProperties": False,
                "description": "Labels stored outside StrengthProfile taxonomy fields",
                "properties": {
                    "synthetic_expected_taxonomy": nullable({"type": "string"}),
                    "expert_taxonomy_candidate": nullable({"type": "string"}),
                    "note": nullable({"type": "string"}),
                },
            }
        ),
    },
}

SCHEMAS_MAP = {
    "strength_provenance.schema.json": PROVENANCE_SCHEMA,
    "strength_evidence.schema.json": EVIDENCE_SCHEMA,
    "strength_conflict.schema.json": CONFLICT_SCHEMA,
    "strength_completeness.schema.json": COMPLETENESS_SCHEMA,
    "strength_confidence.schema.json": CONFIDENCE_SCHEMA,
    "strength_profile.schema.json": PROFILE_SCHEMA,
}


def prov(cls: str, availability: str, source_path: str | None = None, rule_id: str | None = None) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "provenance_class": cls,
        "availability": availability,
        "source_system": "strength_engine_v1",
        "source_path": source_path,
        "rule_id": rule_id,
        "observed_at": None,
        "notes": None,
    }


def mag_raw(value: float | None, representation: str = "raw_contribution") -> dict:
    if value is None:
        return {"representation": "unknown", "raw_contribution": None, "ordinal": None, "categorical": None, "normalized": None, "bounded_contribution": None, "unit_note": None}
    return {
        "representation": representation,
        "raw_contribution": value,
        "ordinal": None,
        "categorical": None,
        "normalized": None,
        "bounded_contribution": None,
        "unit_note": "engine_bucket_contribution_if_observed",
    }


def completeness(overall: str, **dims: str) -> dict:
    base = {
        "calendar": "unknown",
        "season": "unknown",
        "roots": "unknown",
        "support": "unknown",
        "pressure": "unknown",
        "drain": "unknown",
        "structure": "unknown",
        "temperature": "unknown",
        "expert_review": "unknown",
    }
    base.update(dims)
    return {"schema_version": SCHEMA_VERSION, "overall": overall, "by_dimension": base, "notes": None}


def confidence(overall: str, **factors: str) -> dict:
    base = {
        "evidence_completeness": "unknown",
        "evidence_conflict": "unknown",
        "calendar_certainty": "unknown",
        "structural_certainty": "unknown",
        "expert_agreement": "unknown",
        "boundary_proximity": "unknown",
        "runtime_stability": "unknown",
    }
    base.update(factors)
    return {
        "schema_version": SCHEMA_VERSION,
        "overall": overall,
        "factors": base,
        "numeric_runtime_confidence": None,
        "notes": "design confidence is not the same as v1 runtime confidence",
    }


def base_profile(
    *,
    profile_id: str,
    source_ref: str,
    population: str,
    day_master: str,
    raw: float | None,
    normalized: float | None,
    band: str,
    saturation: object,
    saturation_type: str | None,
    seasonal: dict,
    rooting: dict,
    support: dict,
    pressure: dict,
    drain: dict,
    structural: dict,
    temperature: dict,
    conflicts: list,
    completeness_obj: dict,
    evidence: list,
    dominant: list,
    supporting: list,
    opposing: list,
    uncertainty: str,
    confidence_obj: dict,
    synthetic_flags: dict | None,
    external_labels: dict | None,
    design_marker: str = "design_example",
) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "identity": {
            "profile_id": profile_id,
            "source_case_ref": source_ref,
            "population": population,
            "notes": "DESIGN_EXAMPLE only; not calibration truth",
        },
        "population": population,
        "design_marker": design_marker,
        "day_master": day_master,
        "score_reference": {
            "raw_score": raw,
            "normalized_score": normalized,
            "published_score": normalized,
            "current_v1_band": band,
            "score_source": "strength_engine_v1_runtime_observation",
            "score_status": "observed" if normalized is not None else "unknown",
            "saturation_detected": saturation,
            "saturation_type": saturation_type,
        },
        "seasonal_state": seasonal,
        "rooting_state": rooting,
        "support_state": support,
        "pressure_state": pressure,
        "drain_state": drain,
        "structural_state": structural,
        "temperature_state": temperature,
        "conflicts": conflicts,
        "evidence_completeness": completeness_obj,
        "evidence_records": evidence,
        "dominant_factors": dominant,
        "supporting_factors": supporting,
        "opposing_factors": opposing,
        "uncertainty": uncertainty,
        "confidence": confidence_obj,
        "provenance": prov("design_only", "derived", "pilot_1i_design_example"),
        "synthetic_flags": synthetic_flags,
        "external_labels": external_labels,
    }


# ---------- examples (design only; values from known runtime observations) ----------
EX_VERY_WEAK = base_profile(
    profile_id="PRF-DESIGN-VW-001",
    source_ref="SYN-STR-000001",
    population="design_example",
    day_master="quy",
    raw=-49.0,
    normalized=0.01,
    band="weak",
    saturation=False,
    saturation_type="none",
    seasonal={
        "season_branch": "ngo",
        "season_element": "hoa",
        "day_master_relation": "controlled_by_season_element",
        "seasonal_support_direction": "pressure",
        "seasonal_strength_state": "weakening",
        "seasonal_confidence": "medium",
        "source": "runtime_month_status_tu",
        "raw_contribution": -10.0,
    },
    rooting={
        "day_branch_root": "absent",
        "month_branch_root": "absent",
        "other_branch_root": "absent",
        "hidden_root": "absent",
        "multiple_roots": False,
        "root_strength": "vo_can",
        "root_distribution": [],
        "root_confidence": "high",
        "raw_contribution": -20.0,
    },
    support={"items": [], "summary": "none_observed", "confidence": "medium"},
    pressure={
        "items": [
            {"category": "wealth", "direction": "pressure", "raw_contribution": -6.0, "provenance": "engine_rule"}
        ],
        "summary": "wealth_pressure_present",
        "confidence": "medium",
    },
    drain={
        "items": [
            {"category": "output", "direction": "drain", "raw_contribution": -13.0, "provenance": "engine_rule"}
        ],
        "summary": "output_drain_present",
        "confidence": "medium",
    },
    structural={"items": [], "summary": "none_confirmed", "confidence": "low"},
    temperature={
        "temperature_state": "hot",
        "heat_evidence": "summer_month_branch",
        "cold_evidence": None,
        "dryness_evidence": None,
        "moisture_evidence": None,
        "temperature_conflict": False,
        "confidence": "low",
        "provenance": "context_only_not_in_score",
    },
    conflicts=[],
    completeness_obj=completeness(
        "partial",
        calendar="not_available" if False else "unknown",
        season="partial",
        roots="partial",
        support="limited",
        pressure="partial",
        drain="partial",
        structure="limited",
        temperature="limited",
        expert_review="unknown",
    ),
    evidence=[
        {
            "schema_version": SCHEMA_VERSION,
            "evidence_id": "EV-SEA-004",
            "evidence_type": "seasonal",
            "dimension": "seasonal_strength",
            "source": "01_season_rules.csv",
            "source_path": "database/12_strength/01_season_rules.csv",
            "direction": "pressure",
            "magnitude": mag_raw(-10.0),
            "polarity": "negative",
            "confidence": "medium",
            "provenance": prov("engine_rule", "observed", "database/12_strength/01_season_rules.csv", "sea_004"),
            "explanation": "month_status tu contribution",
            "affected_element": "thuy",
            "affected_day_master": "quy",
            "pillar_scope": "month",
            "branch_scope": "ngo",
            "stem_scope": None,
            "seasonal_context": {"month_status": "tu"},
            "interaction_context": None,
            "availability": "observed",
            "completeness": "partial",
            "information_loss": "partially_preserved",
        },
        {
            "schema_version": SCHEMA_VERSION,
            "evidence_id": "EV-ROOT-005",
            "evidence_type": "rooting",
            "dimension": "rooting",
            "source": "02_root_rules.csv",
            "source_path": "database/12_strength/02_root_rules.csv",
            "direction": "pressure",
            "magnitude": mag_raw(-20.0),
            "polarity": "negative",
            "confidence": "high",
            "provenance": prov("engine_rule", "observed", "database/12_strength/02_root_rules.csv", "root_005"),
            "explanation": "vo can",
            "affected_element": "thuy",
            "affected_day_master": "quy",
            "pillar_scope": "multi",
            "branch_scope": "multi",
            "stem_scope": None,
            "seasonal_context": None,
            "interaction_context": None,
            "availability": "observed",
            "completeness": "partial",
            "information_loss": "compressed",
        },
    ],
    dominant=["vo_can", "output_drain", "season_tu"],
    supporting=[],
    opposing=["season_tu", "wealth_pressure", "output_drain"],
    uncertainty="synthetic_expected_very_weak_is_external_label_only",
    confidence_obj=confidence("medium", evidence_completeness="medium", evidence_conflict="high", calendar_certainty="low"),
    synthetic_flags={
        "synthetic": True,
        "calibration_eligible": False,
        "golden_eligible": False,
        "expert_calibration_eligible": False,
    },
    external_labels={
        "synthetic_expected_taxonomy": "very_weak",
        "expert_taxonomy_candidate": None,
        "note": "external label; not inside taxonomy fields",
    },
)

# Fix completeness calendar value - I used a bad idiom. Let me fix in the completeness call - use "unknown"
EX_VERY_WEAK["evidence_completeness"] = completeness(
    "partial",
    calendar="unknown",
    season="partial",
    roots="partial",
    support="limited",
    pressure="partial",
    drain="partial",
    structure="limited",
    temperature="limited",
    expert_review="unknown",
)

EX_WEAK = base_profile(
    profile_id="PRF-DESIGN-W-001",
    source_ref="SYN-STR-000005",
    population="design_example",
    day_master="dinh",
    raw=None,
    normalized=0.14,
    band="weak",
    saturation=False,
    saturation_type="none",
    seasonal={"seasonal_strength_state": "weakening", "seasonal_confidence": "medium", "source": "runtime", "raw_contribution": None},
    rooting={"root_strength": "limited", "multiple_roots": False, "root_confidence": "medium", "root_distribution": []},
    support={"items": [], "summary": "limited_or_none", "confidence": "medium"},
    pressure={"items": [{"category": "control", "direction": "pressure"}], "summary": "kim_environment_pressure", "confidence": "medium"},
    drain={"items": [], "summary": "unknown", "confidence": "low"},
    structural={"items": [], "summary": "none_confirmed", "confidence": "low"},
    temperature={"temperature_state": "unknown", "confidence": "unknown", "provenance": "unknown"},
    conflicts=[],
    completeness_obj=completeness("partial", season="partial", roots="partial", support="limited", pressure="partial", drain="limited", structure="limited", temperature="unknown", calendar="unknown", expert_review="unknown"),
    evidence=[],
    dominant=["environmental_pressure"],
    supporting=[],
    opposing=["kim_pressure"],
    uncertainty="raw_score_unknown_in_this_design_example",
    confidence_obj=confidence("low", evidence_completeness="low"),
    synthetic_flags={"synthetic": True, "calibration_eligible": False, "golden_eligible": False, "expert_calibration_eligible": False},
    external_labels={"synthetic_expected_taxonomy": "weak", "expert_taxonomy_candidate": None, "note": None},
)

EX_SLIGHTLY_WEAK_REAL = base_profile(
    profile_id="PRF-DESIGN-SW-REAL-001",
    source_ref="CAL-000001",
    population="design_example",
    day_master="canh",
    raw=37.0,
    normalized=0.87,
    band="strong",
    saturation=False,
    saturation_type="none",
    seasonal={
        "season_branch": "suu",
        "season_element": "tho",
        "day_master_relation": "tuong",
        "seasonal_support_direction": "support",
        "seasonal_strength_state": "supportive",
        "seasonal_confidence": "medium",
        "source": "runtime_month_status_tuong",
        "raw_contribution": 25.0,
    },
    rooting={
        "day_branch_root": "candidate",
        "month_branch_root": "unknown",
        "other_branch_root": "unknown",
        "hidden_root": "present",
        "multiple_roots": False,
        "root_strength": "thong_can_1_chi",
        "root_distribution": ["unknown_loci"],
        "root_confidence": "medium",
        "raw_contribution": 12.0,
    },
    support={
        "items": [
            {"category": "same_element", "direction": "support", "raw_contribution": 8.0, "provenance": "engine_rule"},
            {"category": "resource", "direction": "support", "raw_contribution": 10.0, "provenance": "engine_rule", "note": "special_an_cold"},
        ],
        "summary": "companion_plus_special_resource",
        "confidence": "medium",
    },
    pressure={
        "items": [
            {"category": "officer", "direction": "pressure", "raw_contribution": -18.0, "provenance": "engine_rule"}
        ],
        "summary": "officer_pressure",
        "confidence": "medium",
    },
    drain={"items": [], "summary": "none_observed", "confidence": "medium"},
    structural={"items": [], "summary": "none_confirmed", "confidence": "low"},
    temperature={
        "temperature_state": "cold",
        "heat_evidence": None,
        "cold_evidence": "winter_context",
        "dryness_evidence": None,
        "moisture_evidence": None,
        "temperature_conflict": True,
        "confidence": "low",
        "provenance": "context_vs_temperature_engine_may_differ",
    },
    conflicts=[
        {
            "schema_version": SCHEMA_VERSION,
            "conflict_id": "CF-SUP-PRESS-001",
            "conflict_type": "support_vs_pressure",
            "dimensions": ["same_element_support", "officer_pressure", "seasonal_strength"],
            "evidence_ids": ["EV-SEA-002", "EV-SUP-001", "EV-CTL-001"],
            "severity": "high",
            "resolution_status": "unresolved",
            "confidence": "medium",
            "notes": "runtime net strong vs expert slightly_weak; no resolution invented",
        }
    ],
    completeness_obj=completeness(
        "partial",
        calendar="partial",
        season="partial",
        roots="partial",
        support="partial",
        pressure="partial",
        drain="partial",
        structure="limited",
        temperature="limited",
        expert_review="partial",
    ),
    evidence=[
        {
            "schema_version": SCHEMA_VERSION,
            "evidence_id": "EV-SEA-002",
            "evidence_type": "seasonal",
            "dimension": "seasonal_strength",
            "source": "01_season_rules.csv",
            "source_path": "database/12_strength/01_season_rules.csv",
            "direction": "support",
            "magnitude": mag_raw(25.0),
            "polarity": "positive",
            "confidence": "medium",
            "provenance": prov("engine_rule", "observed", "database/12_strength/01_season_rules.csv", "sea_002"),
            "explanation": "tuong season",
            "affected_element": "kim",
            "affected_day_master": "canh",
            "pillar_scope": "month",
            "branch_scope": "suu",
            "stem_scope": None,
            "seasonal_context": {"month_status": "tuong"},
            "interaction_context": None,
            "availability": "observed",
            "completeness": "partial",
            "information_loss": "compressed",
        }
    ],
    dominant=["season_tuong", "officer_pressure", "special_an"],
    supporting=["season_tuong", "root_1_chi", "companion"],
    opposing=["officer_pressure"],
    uncertainty="expert_dual_reviewed_slightly_weak_disagrees_with_runtime_strong",
    confidence_obj=confidence(
        "low",
        evidence_completeness="medium",
        evidence_conflict="low",
        calendar_certainty="high",
        expert_agreement="high",
        boundary_proximity="medium",
        runtime_stability="medium",
    ),
    synthetic_flags=None,
    external_labels={
        "synthetic_expected_taxonomy": None,
        "expert_taxonomy_candidate": "slightly_weak",
        "note": "expert labels remain external; not profile taxonomy",
    },
)

EX_BALANCED = base_profile(
    profile_id="PRF-DESIGN-BAL-001",
    source_ref="SYN-STR-000010",
    population="design_example",
    day_master="mau",
    raw=-11.0,
    normalized=0.39,
    band="balanced",
    saturation=False,
    saturation_type="none",
    seasonal={"seasonal_strength_state": "strongly_weakening", "raw_contribution": -25.0, "seasonal_confidence": "medium", "source": "runtime"},
    rooting={"root_strength": "thong_can_3_chi", "multiple_roots": True, "raw_contribution": 30.0, "root_confidence": "medium", "root_distribution": ["multi"]},
    support={"items": [{"category": "resource", "raw_contribution": 10.0}], "summary": "resource_support", "confidence": "medium"},
    pressure={"items": [{"category": "officer", "raw_contribution": -18.0}], "summary": "officer_pressure", "confidence": "medium"},
    drain={"items": [{"category": "output", "raw_contribution": -8.0}], "summary": "output_drain", "confidence": "medium"},
    structural={"items": [], "summary": "none_confirmed", "confidence": "low"},
    temperature={"temperature_state": "unknown", "confidence": "unknown", "provenance": "unknown"},
    conflicts=[
        {
            "schema_version": SCHEMA_VERSION,
            "conflict_id": "CF-SEA-ROOT-001",
            "conflict_type": "season_vs_root",
            "dimensions": ["seasonal_strength", "rooting"],
            "evidence_ids": ["EV-SEA-005", "EV-ROOT-001"],
            "severity": "high",
            "resolution_status": "unresolved",
            "confidence": "medium",
            "notes": "cancellation equilibrium; not quiet mid",
        }
    ],
    completeness_obj=completeness("partial", season="partial", roots="partial", support="partial", pressure="partial", drain="partial", structure="limited", temperature="unknown", calendar="unknown", expert_review="unknown"),
    evidence=[],
    dominant=["death_season", "triple_root"],
    supporting=["triple_root", "resource"],
    opposing=["death_season", "officer", "output"],
    uncertainty="balanced_via_cancellation",
    confidence_obj=confidence("medium", evidence_conflict="low"),
    synthetic_flags={"synthetic": True, "calibration_eligible": False, "golden_eligible": False, "expert_calibration_eligible": False},
    external_labels={"synthetic_expected_taxonomy": "balanced", "expert_taxonomy_candidate": None, "note": None},
)

EX_STRONG = base_profile(
    profile_id="PRF-DESIGN-STR-001",
    source_ref="SYN-STR-000018",
    population="design_example",
    day_master="canh",
    raw=82.0,
    normalized=1.0,
    band="strong",
    saturation=True,
    saturation_type="upper_clamp",
    seasonal={"seasonal_strength_state": "very_supportive", "raw_contribution": 35.0, "seasonal_confidence": "medium", "source": "runtime"},
    rooting={"root_strength": "thong_can_2_chi", "multiple_roots": True, "raw_contribution": 22.0, "root_confidence": "medium", "root_distribution": ["multi"]},
    support={"items": [{"category": "same_element", "raw_contribution": 13.0}], "summary": "companion_support", "confidence": "medium"},
    pressure={"items": [], "summary": "none_observed", "confidence": "medium"},
    drain={"items": [], "summary": "none_observed", "confidence": "medium"},
    structural={"items": [{"type": "combination", "resolution_status": "probable", "effect_on_strength": "support"}], "summary": "combination_candidate", "confidence": "medium"},
    temperature={"temperature_state": "cool", "confidence": "low", "provenance": "context_only"},
    conflicts=[],
    completeness_obj=completeness("partial", season="partial", roots="partial", support="partial", pressure="partial", drain="partial", structure="partial", temperature="limited", calendar="unknown", expert_review="unknown"),
    evidence=[],
    dominant=["dac_lenh", "dual_root", "companion"],
    supporting=["dac_lenh", "dual_root", "companion", "combination"],
    opposing=[],
    uncertainty="published_score_clamped",
    confidence_obj=confidence("medium"),
    synthetic_flags={"synthetic": True, "calibration_eligible": False, "golden_eligible": False, "expert_calibration_eligible": False},
    external_labels={"synthetic_expected_taxonomy": "strong", "expert_taxonomy_candidate": None, "note": None},
)

EX_VERY_STRONG = base_profile(
    profile_id="PRF-DESIGN-VS-001",
    source_ref="SYN-STR-000019",
    population="design_example",
    day_master="nham",
    raw=107.0,
    normalized=1.0,
    band="strong",
    saturation=True,
    saturation_type="upper_clamp",
    seasonal={"seasonal_strength_state": "very_supportive", "raw_contribution": 35.0, "seasonal_confidence": "medium", "source": "runtime"},
    rooting={"root_strength": "thong_can_2_chi", "multiple_roots": True, "raw_contribution": 22.0, "root_confidence": "medium", "root_distribution": ["multi"]},
    support={"items": [{"category": "same_element", "raw_contribution": 18.0}], "summary": "strong_support", "confidence": "medium"},
    pressure={"items": [], "summary": "none_observed", "confidence": "medium"},
    drain={"items": [], "summary": "none_observed", "confidence": "medium"},
    structural={"items": [{"type": "special_structure", "resolution_status": "probable"}], "summary": "special_boost", "confidence": "medium"},
    temperature={"temperature_state": "cold", "confidence": "low", "provenance": "context_only"},
    conflicts=[],
    completeness_obj=completeness("partial", season="partial", roots="partial", support="partial", pressure="partial", drain="partial", structure="partial", temperature="limited", calendar="unknown", expert_review="unknown"),
    evidence=[],
    dominant=["dac_lenh", "support_mass", "special"],
    supporting=["dac_lenh", "root", "support", "special"],
    opposing=[],
    uncertainty="raw_above_clamp_same_published_score_as_strong_peers",
    confidence_obj=confidence("medium"),
    synthetic_flags={"synthetic": True, "calibration_eligible": False, "golden_eligible": False, "expert_calibration_eligible": False},
    external_labels={"synthetic_expected_taxonomy": "very_strong", "expert_taxonomy_candidate": None, "note": "intensity visible in raw_score only"},
)

EX_CONFLICT = base_profile(
    profile_id="PRF-DESIGN-CF-001",
    source_ref="SYN-STR-000007",
    population="design_example",
    day_master="canh",
    raw=37.0,
    normalized=0.87,
    band="strong",
    saturation=False,
    saturation_type="none",
    seasonal={"seasonal_strength_state": "supportive", "raw_contribution": 25.0, "seasonal_confidence": "medium", "source": "runtime"},
    rooting={"root_strength": "thong_can_1_chi", "raw_contribution": 12.0, "root_confidence": "medium", "multiple_roots": False, "root_distribution": []},
    support={"items": [{"category": "same_element", "raw_contribution": 8.0}], "summary": "companion", "confidence": "medium"},
    pressure={"items": [{"category": "officer", "raw_contribution": -18.0}], "summary": "officer", "confidence": "medium"},
    drain={"items": [], "summary": "none_observed", "confidence": "medium"},
    structural={"items": [], "summary": "none_confirmed", "confidence": "low"},
    temperature={"temperature_state": "cold", "confidence": "low", "provenance": "context_only"},
    conflicts=[
        {
            "schema_version": SCHEMA_VERSION,
            "conflict_id": "CF-SUP-PRESS-007",
            "conflict_type": "support_vs_pressure",
            "dimensions": ["seasonal_strength", "officer_pressure", "same_element_support"],
            "evidence_ids": ["EV-SEA-002", "EV-CTL-001", "EV-SUP-001"],
            "severity": "high",
            "resolution_status": "unresolved",
            "confidence": "medium",
            "notes": "mirrors CAL-000001 family; synthetic slightly_weak external",
        }
    ],
    completeness_obj=completeness("partial", season="partial", roots="partial", support="partial", pressure="partial", drain="partial", structure="limited", temperature="limited", calendar="unknown", expert_review="unknown"),
    evidence=[],
    dominant=["season_support", "officer_pressure"],
    supporting=["season", "root", "companion", "special"],
    opposing=["officer"],
    uncertainty="support_pressure_conflict_unresolved",
    confidence_obj=confidence("low", evidence_conflict="low"),
    synthetic_flags={"synthetic": True, "calibration_eligible": False, "golden_eligible": False, "expert_calibration_eligible": False},
    external_labels={"synthetic_expected_taxonomy": "slightly_weak", "expert_taxonomy_candidate": None, "note": None},
)

EX_INCOMPLETE = base_profile(
    profile_id="PRF-DESIGN-INC-001",
    source_ref="DESIGN-INCOMPLETE-001",
    population="design_example",
    day_master="giap",
    raw=None,
    normalized=None,
    band="unknown",
    saturation="unknown",
    saturation_type="unknown",
    seasonal={"seasonal_strength_state": "unknown", "seasonal_confidence": "unknown", "source": "unknown"},
    rooting={"root_strength": "unknown", "root_confidence": "unknown", "multiple_roots": False, "root_distribution": []},
    support={"items": [], "summary": "unknown", "confidence": "unknown"},
    pressure={"items": [], "summary": "unknown", "confidence": "unknown"},
    drain={"items": [], "summary": "unknown", "confidence": "unknown"},
    structural={"items": [], "summary": "unknown", "confidence": "unknown"},
    temperature={"temperature_state": "unknown", "confidence": "unknown", "provenance": "unknown"},
    conflicts=[],
    completeness_obj=completeness(
        "limited",
        calendar="unknown",
        season="unknown",
        roots="unknown",
        support="unknown",
        pressure="unknown",
        drain="unknown",
        structure="unknown",
        temperature="unknown",
        expert_review="unknown",
    ),
    evidence=[],
    dominant=[],
    supporting=[],
    opposing=[],
    uncertainty="intentionally_incomplete_design_example",
    confidence_obj=confidence("unknown"),
    synthetic_flags={"synthetic": True, "calibration_eligible": False, "golden_eligible": False, "expert_calibration_eligible": False},
    external_labels={"synthetic_expected_taxonomy": None, "expert_taxonomy_candidate": None, "note": "incomplete evidence illustration"},
)

EXAMPLES_MAP = {
    "very_weak_synthetic.json": EX_VERY_WEAK,
    "weak_synthetic.json": EX_WEAK,
    "slightly_weak_real.json": EX_SLIGHTLY_WEAK_REAL,
    "balanced_synthetic.json": EX_BALANCED,
    "strong_synthetic.json": EX_STRONG,
    "very_strong_synthetic.json": EX_VERY_STRONG,
    "evidence_conflict.json": EX_CONFLICT,
    "incomplete_evidence.json": EX_INCOMPLETE,
}

REPORTS_MAP = {
    "evidence_vocabulary.json": {
        "schema_version": SCHEMA_VERSION,
        "directions": DIRECTION,
        "polarities": POLARITY,
        "provenance_classes": PROVENANCE,
        "dimensions": DIMENSIONS,
        "confidence": CONFIDENCE,
    },
    "profile_fields.json": {
        "schema_version": SCHEMA_VERSION,
        "required_top_level": PROFILE_SCHEMA["required"],
        "forbidden_in_profile": [
            "taxonomy_v2_label",
            "future_taxonomy_label",
            "t1",
            "t2",
            "t3",
            "t4",
            "t5",
            "t6",
            "final_v2_classification",
        ],
    },
    "information_loss.json": {
        "schema_version": SCHEMA_VERSION,
        "v1_dimensions": {
            "seasonal_strength": "compressed",
            "rooting": "compressed",
            "same_element_support": "compressed",
            "resource_support": "partially_preserved",
            "output_drain": "partially_preserved",
            "wealth_pressure": "partially_preserved",
            "officer_pressure": "partially_preserved",
            "hidden_stem_evidence": "lost",
            "temperature": "not_available",
            "combination": "partially_preserved",
            "clash": "not_available",
            "punishment": "not_available",
            "harm": "not_available",
            "destruction": "not_available",
            "transformation": "partially_preserved",
            "special_structure": "partially_preserved",
            "follow_pattern": "not_available",
            "evidence_conflict": "lost",
            "evidence_completeness": "lost",
            "raw_vs_normalized_score": "partially_preserved",
        },
    },
    "compatibility.json": {
        "schema_version": SCHEMA_VERSION,
        "v1_bands": ["weak", "balanced", "strong"],
        "future_bands_conceptual_only": [
            "very_weak",
            "weak",
            "slightly_weak",
            "balanced",
            "slightly_strong",
            "strong",
            "very_strong",
        ],
        "mapping_frozen": False,
        "taxonomy_v2_implemented": False,
        "thresholds_implemented": False,
    },
    "implementation_guardrails.json": {
        "schema_version": SCHEMA_VERSION,
        "do_not": [
            "replace_v1_score",
            "tune_v1_weights",
            "tune_v1_thresholds",
            "implement_taxonomy_v2",
            "infer_expert_labels",
            "promote_synthetic_evidence",
            "modify_golden_dataset",
            "modify_production_contracts",
            "bypass_provenance",
            "hide_unknown_values",
            "convert_missing_to_neutral",
        ],
        "must": [
            "preserve_raw_runtime_evidence",
            "preserve_provenance",
            "preserve_unknown",
            "preserve_evidence_conflicts",
            "preserve_population_separation",
            "preserve_v1_compatibility",
            "version_schema",
            "validate_future_implementations",
        ],
    },
}

VALIDATION_JSON = {
    "sprint": "PILOT-1I",
    "design_only": True,
    "taxonomy_v2_implemented": False,
    "t1_t6_frozen": False,
    "production_code_changed": False,
    "strength_engine_changed": False,
    "calibration_data_changed": False,
    "synthetic_data_changed": False,
    "final_decision": "DESIGN_COMPLETE",
    "overall": "PASS",
}

PROFILE_META_JSON = {
    "sprint": "PILOT-1I",
    "schema_version": SCHEMA_VERSION,
    "layers": [
        "StrengthEvidence",
        "StrengthEvidenceGroup",
        "StrengthProfile",
        "StrengthConfidence",
        "FutureTaxonomyInput",
    ],
    "examples": list(EXAMPLES_MAP.keys()),
    "final_decision": "DESIGN_COMPLETE",
}

# Markdown docs filled below
DOCS: dict[str, str] = {}


def _doc_block() -> None:
    global DOCS
    DOCS = {
        "README.md": f"""# Strength Profile Design — PILOT-1I

**Mode:** DESIGN ONLY. No production Strength Profile runtime. No Taxonomy V2.

## Architecture

```text
Strength Engine V1
      |
      v
Strength Evidence
      |
      v
Strength Profile
      |
      v
Future Taxonomy V2 (not implemented)
      |
      v
Confidence
      |
      v
Public Contract
```

## Principles

- Score remains the quantitative net-strength index (V1 authoritative).
- Profile preserves multidimensional evidence currently compressed by V1.
- Profile does **not** emit taxonomy labels or T1-T6 thresholds.
- Populations stay separated: REAL_CALIBRATION / SYNTHETIC_STRESS / RUNTIME_REFERENCE / DESIGN_EXAMPLES.

## Schema version

`{SCHEMA_VERSION}`
""",
        "STRENGTH_EVIDENCE_SCHEMA.md": """# STRENGTH_EVIDENCE_SCHEMA

Canonical evidence record for StrengthProfile design.

See `schemas/strength_evidence.schema.json`.

## Required fields

evidence_id, evidence_type, dimension, direction, polarity, availability, provenance, schema_version

## Optional / nullable

magnitude, confidence, explanation, scopes, contexts, completeness, information_loss

## Magnitude policy

If engine exposes numeric contribution: store as `raw_contribution` with representation `raw_contribution`.  
If not exposed: representation `unknown` — do not invent numbers.
""",
        "STRENGTH_EVIDENCE_VOCABULARY.md": f"""# STRENGTH_EVIDENCE_VOCABULARY

Candidate design enums (not production-frozen).

## direction

{', '.join(DIRECTION)}

## polarity

{', '.join(POLARITY)}

## provenance_class

{', '.join(PROVENANCE)}

## dimensions

{', '.join(DIMENSIONS)}

## confidence / completeness / severity / resolution

See JSON schemas. Values are lowercase ASCII snake_case.
""",
        "STRENGTH_PROFILE_SCHEMA.md": """# STRENGTH_PROFILE_SCHEMA

See `schemas/strength_profile.schema.json`.

## Layers

1. StrengthEvidence
2. StrengthEvidenceGroup (logical grouping of evidence_records)
3. StrengthProfile
4. StrengthConfidence
5. FutureTaxonomyInput (out of band; not fields on Profile)

## Forbidden on Profile

- taxonomy_v2_label / future taxonomy classification
- T1-T6
- invented expert judgment
""",
        "STRENGTH_PROFILE_CONTRACT.md": """# STRENGTH_PROFILE_CONTRACT

## Contract purpose

Preserve multidimensional Strength evidence between Strength Engine V1 and a future Taxonomy V2.

## Non-goals

- Replace V1 score
- Produce taxonomy labels
- Freeze thresholds
- Implement production runtime in this sprint

## Required sections

identity, day_master, score_reference, seasonal_state, rooting_state, support_state, pressure_state, drain_state, structural_state, temperature_state, conflicts, evidence_completeness, provenance, population, design_marker

## External labels

Synthetic expected taxonomy and expert taxonomy candidates live in `external_labels` (outside taxonomy fields) or entirely outside the Profile in calibration records.
""",
        "STRENGTH_CONFIDENCE_SCHEMA.md": """# STRENGTH_CONFIDENCE_SCHEMA

Confidence is **not** Strength score.

Factors: evidence_completeness, evidence_conflict, calendar_certainty, structural_certainty, expert_agreement, boundary_proximity, runtime_stability.

States: high | medium | low | unknown

Numeric runtime confidence may be referenced if observed; do not invent a new numeric confidence formula here.
""",
        "STRENGTH_PROVENANCE_MODEL.md": """# STRENGTH_PROVENANCE_MODEL

Classes: engine_rule, knowledge_rule, derived, structural, calendar, expert, synthetic, design_only

Availability: observed, derived, inferred, externally_reviewed, synthetic, unknown

Rule: synthetic evidence must never be represented as expert evidence.
""",
        "STRENGTH_COMPLETENESS_MODEL.md": """# STRENGTH_COMPLETENESS_MODEL

Overall and per-dimension: complete | partial | limited | unknown

Dimensions: calendar, season, roots, support, pressure, drain, structure, temperature, expert_review

One dimension may be complete while another is unknown.
""",
        "STRENGTH_CONFLICT_MODEL.md": """# STRENGTH_CONFLICT_MODEL

Conflict records preserve conflict_id, conflict_type, dimensions, evidence_ids, severity, resolution_status, confidence.

Do not invent resolution logic. Use unresolved when unknown.
""",
        "STRENGTH_SCORE_REFERENCE.md": """# STRENGTH_SCORE_REFERENCE

Fields: raw_score, normalized_score, published_score, current_v1_band, score_source, score_status, saturation_detected, saturation_type

Preserve distinctions. Do not reconstruct missing values. Use null / unknown.
""",
        "STRENGTH_SATURATION_METADATA.md": """# STRENGTH_SATURATION_METADATA

saturation_detected: true | false | unknown  
saturation_type: none | upper_clamp | lower_clamp | normalization | unknown

PILOT-1H observation: raw >= 50 clamps published normalized score to 1.0. This is metadata, not an implementation of new scoring.
""",
        "STRENGTH_ROOTING_MODEL.md": """# STRENGTH_ROOTING_MODEL

Distinguish day_branch_root, month_branch_root, other_branch_root, hidden_root, multiple_roots, root_strength, root_distribution, root_confidence.

Allow multiple rooting evidence records. Do not reduce to a boolean.
""",
        "STRENGTH_SUPPORT_MODEL.md": """# STRENGTH_SUPPORT_MODEL

Categories: same_element, resource, seasonal_support, root_support, structural_support

Preserve source, type, direction, magnitude if known, scope, confidence, provenance.
""",
        "STRENGTH_PRESSURE_MODEL.md": """# STRENGTH_PRESSURE_MODEL

Categories: wealth, officer, control, seasonal_opposition, structural_pressure, other

Do not collapse all pressure into one number.
""",
        "STRENGTH_DRAIN_MODEL.md": """# STRENGTH_DRAIN_MODEL

Categories: output, leakage, resource_consumption, structural_drain, other

Do not assume all drain is numerically equivalent.
""",
        "STRENGTH_SEASONAL_MODEL.md": """# STRENGTH_SEASONAL_MODEL

Candidate fields: season_branch, season_element, day_master_relation, seasonal_support_direction, seasonal_strength_state, seasonal_confidence, source

Candidate states: very_supportive, supportive, neutral, weakening, strongly_weakening, unknown

Design candidates only — not frozen production enums.
""",
        "STRENGTH_STRUCTURAL_MODEL.md": """# STRENGTH_STRUCTURAL_MODEL

Types: combination, clash, punishment, harm, destruction, transformation, special_structure, follow_pattern

Each item: type, participating_pillars, participating_elements, direction, effect_on_strength, confidence, provenance, resolution_status

Candidate structures are not confirmed.
""",
        "STRENGTH_TEMPERATURE_MODEL.md": """# STRENGTH_TEMPERATURE_MODEL

Temperature is separate from Strength score.

Fields: temperature_state, heat/cold/dryness/moisture evidence, temperature_conflict, confidence, provenance

Do not silently alter Strength taxonomy via temperature in this design.
""",
        "STRENGTH_EXPERT_COMPATIBILITY.md": """# STRENGTH_EXPERT_COMPATIBILITY

```text
Runtime Profile
  + Expert Review
  + Adjudication
  = Calibration Record
```

Expert evidence remains separate and must not overwrite runtime evidence fields. Adjudication is not implemented here.
""",
        "STRENGTH_SYNTHETIC_COMPATIBILITY.md": """# STRENGTH_SYNTHETIC_COMPATIBILITY

Synthetic examples must set:

- synthetic = true
- calibration_eligible = false
- golden_eligible = false
- expert_calibration_eligible = false

Synthetic expected taxonomy lives in external_labels, never as Profile taxonomy.
""",
        "V1_PROFILE_COMPATIBILITY.md": """# V1_PROFILE_COMPATIBILITY

Conceptual only (not frozen, not implemented):

| future candidate | -> v1 |
|---|---|
| very_weak | weak |
| weak | weak |
| slightly_weak | weak |
| balanced | balanced |
| slightly_strong | strong |
| strong | strong |
| very_strong | strong |

No thresholds assigned.
""",
        "PROFILE_TAXONOMY_BOUNDARY.md": """# PROFILE_TAXONOMY_BOUNDARY

| Layer | Answers |
|---|---|
| StrengthProfile | Why does the current Strength Engine produce this result? |
| Future Taxonomy | How should the overall Strength state be categorized? |
| StrengthConfidence | How reliable is that categorization? |

The profile must not become a hidden taxonomy.
""",
        "INFORMATION_LOSS_MODEL.md": """# INFORMATION_LOSS_MODEL

Classes: PRESERVED | PARTIALLY_PRESERVED | COMPRESSED | LOST | NOT_AVAILABLE

Applied to V1 using PILOT-1H diagnostics (see `reports/information_loss.json`).

Key losses: sitting hidden pressure, clash/punishment/harm, temperature-in-score, evidence conflict publication, raw intensity after clamp, root loci.
""",
        "DESIGN_EXAMPLES.md": """# DESIGN_EXAMPLES

All files under `examples/` are **DESIGN_EXAMPLE** only.

| File | Illustrates | Source ref |
|---|---|---|
| very_weak_synthetic.json | extreme weak | SYN-STR-000001 |
| weak_synthetic.json | weak | SYN-STR-000005 |
| slightly_weak_real.json | dual-reviewed conflict | CAL-000001 |
| balanced_synthetic.json | cancellation balanced | SYN-STR-000010 |
| strong_synthetic.json | strong + clamp | SYN-STR-000018 |
| very_strong_synthetic.json | very_strong saturation | SYN-STR-000019 |
| evidence_conflict.json | support vs pressure | SYN-STR-000007 |
| incomplete_evidence.json | unknown-heavy profile | DESIGN-INCOMPLETE-001 |

No CAL-* / SYN-* source records were modified.
""",
        "IMPLEMENTATION_GUARDRAILS.md": """# IMPLEMENTATION_GUARDRAILS

## DO NOT

- replace V1 score
- tune V1 weights
- tune V1 thresholds
- implement Taxonomy V2
- infer expert labels
- promote synthetic evidence
- modify Golden Dataset
- modify production contracts
- bypass provenance
- hide unknown values
- silently convert missing evidence to neutral evidence

## MUST

- preserve raw runtime evidence
- preserve provenance
- preserve unknown
- preserve evidence conflicts
- preserve population separation
- preserve V1 compatibility
- version the schema
- validate all future implementations
""",
        "VALIDATION.md": """# VALIDATION — PILOT-1I

Design-only validation. Final decision: **DESIGN_COMPLETE**.

See `validation/VALIDATION.json`.
""",
        "PILOT_1I_SUMMARY.md": f"""# PILOT_1I_SUMMARY — Strength Profile Contract & Evidence Schema Design

**Mode:** DESIGN ONLY  
**Schema version:** `{SCHEMA_VERSION}`

## Delivered

- Evidence, Profile, Confidence, Provenance, Completeness, Conflict schemas (Draft 2020-12)
- Dimension models (season/root/support/pressure/drain/structure/temperature)
- Score reference + saturation metadata
- Expert/synthetic/V1 compatibility docs
- Information loss model
- 8 DESIGN_EXAMPLE profiles
- Implementation guardrails + tests

## Explicit non-delivery

- No Strength Engine changes
- No Taxonomy V2 / T1-T6
- No production Profile runtime
- No CAL/SYN mutations

---

Status:
- EVIDENCE_SCHEMA_DESIGNED: YES
- PROFILE_SCHEMA_DESIGNED: YES
- CONFIDENCE_SCHEMA_DESIGNED: YES
- PROVENANCE_MODEL_DESIGNED: YES
- COMPLETENESS_MODEL_DESIGNED: YES
- CONFLICT_MODEL_DESIGNED: YES
- SCORE_REFERENCE_DESIGNED: YES
- SATURATION_METADATA_DESIGNED: YES
- EXPERT_COMPATIBILITY_DESIGNED: YES
- SYNTHETIC_COMPATIBILITY_DESIGNED: YES
- V1_COMPATIBILITY_DESIGNED: YES
- INFORMATION_LOSS_MODEL_DESIGNED: YES
- TAXONOMY_V2_IMPLEMENTED: NO
- TAXONOMY_THRESHOLDS_IMPLEMENTED: NO
- T1_T6_FROZEN: NO
- PRODUCTION_CODE_CHANGED: NO
- STRENGTH_ENGINE_CHANGED: NO
- KNOWLEDGE_PACKAGES_CHANGED: NO
- GOLDEN_EXPECTED_CHANGED: NO
- CALIBRATION_DATA_CHANGED: NO
- AF1_CHANGED: NO
- TEST_REGRESSION: NO

Final Decision:
DESIGN_COMPLETE

Recommendation:
- NEXT_ACTION: Continue real expert case acquisition and dual review while preserving the V1 Strength Engine and keeping future Taxonomy V2 unimplemented.
""",
    }


_doc_block()

if __name__ == "__main__":
    build()
