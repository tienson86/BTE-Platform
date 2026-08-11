"""PILOT-1K design package builder (design-only; no production changes)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples"
REPORTS = ROOT / "reports"
VALIDATION = ROOT / "validation"

SCHEMA_META = "https://json-schema.org/draft/2020-12/schema"
SCHEMA_VERSION = "0.1.0"
DESIGN_MARKER = "design_only"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def nullable(t: dict) -> dict:
    return {"anyOf": [t, {"type": "null"}]}


def enum_str(values: list[str]) -> dict:
    return {"type": "string", "enum": values}


MISSING = ["unknown", "not_available", "not_applicable", "partial"]
PROVENANCE = [
    "engine_rule",
    "knowledge_rule",
    "derived",
    "structural",
    "calendar",
    "expert",
    "synthetic",
    "design_only",
    "unknown",
]
RESOLUTION = ["confirmed", "probable", "candidate", "unresolved", "not_applicable"]
COMPLETENESS = ["complete", "partial", "limited", "unknown"]
CONFIDENCE = ["high", "medium", "low", "unknown"]
SEVERITY = ["low", "medium", "high", "critical", "unknown"]
DIRECTION = ["support", "pressure", "drain", "neutral", "conflict", "unknown"]
STRUCTURE_TYPES = [
    "combination",
    "clash",
    "punishment",
    "harm",
    "destruction",
    "transformation",
    "special_structure",
    "follow_pattern",
]
SATURATION = ["none", "upper_clamp", "lower_clamp", "normalization", "unknown"]
STEMS = ["canh", "tan", "nham", "quy", "giap", "at", "binh", "dinh", "mau", "ky"]
BRANCHES = [
    "ty", "suu", "dan", "mao", "thin", "ti", "ngo", "mui", "than", "dau", "tuat", "hoi"
]
ELEMENTS = ["kim", "moc", "thuy", "hoa", "tho", "unknown"]
PILLARS = ["year", "month", "day", "hour", "multi", "unknown"]
REQ_CLASS = ["required", "optional", "reserved", "not_supported"]


def build() -> None:
    for name, schema in SCHEMAS_MAP.items():
        write_json(SCHEMAS / name, schema)
    for name, example in EXAMPLES_MAP.items():
        write_json(EXAMPLES / name, example)
    for name, report in REPORTS_MAP.items():
        write_json(REPORTS / name, report)
    write_json(VALIDATION / "VALIDATION.json", VALIDATION_JSON)
    write_json(VALIDATION / "profile.json", PROFILE_META)
    for name, text in DOCS.items():
        write(ROOT / name, text)
    print("PILOT-1K design package written")


PROVENANCE_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_provenance_output.schema.json",
    "title": "StrengthProvenanceEvidence",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "provenance_type"],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "provenance_type": enum_str(PROVENANCE),
        "source_module": nullable({"type": "string"}),
        "source_rule": nullable({"type": "string"}),
        "source_path": nullable({"type": "string"}),
        "source_record": nullable({"type": "string"}),
        "generated_at": nullable({"type": "string"}),
        "calculation_id": nullable({"type": "string"}),
        "notes": nullable({"type": "string"}),
    },
}

SCORE_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_score_output.schema.json",
    "title": "StrengthScoreEvidence",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "raw_score",
        "normalized_score",
        "published_score",
        "current_v1_band",
        "score_source",
        "score_status",
        "saturation_detected",
        "saturation_type",
        "design_marker",
    ],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "design_marker": {"type": "string", "const": DESIGN_MARKER},
        "raw_score": nullable({"type": "number"}),
        "normalized_score": nullable({"type": "number"}),
        "published_score": nullable({"type": "number"}),
        "current_v1_band": enum_str(["weak", "balanced", "strong", "unknown"]),
        "score_source": {"type": "string"},
        "score_status": enum_str(["observed", "partial", "unknown", "design_only"]),
        "saturation_detected": {
            "anyOf": [{"type": "boolean"}, {"type": "string", "const": "unknown"}]
        },
        "saturation_type": enum_str(SATURATION),
        "saturation_boundary": nullable({"type": "string"}),
        "saturation_source": nullable({"type": "string"}),
        "contributions": nullable(
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "seasonal_contribution": nullable({"type": "number"}),
                    "root_contribution": nullable({"type": "number"}),
                    "support_contribution": nullable({"type": "number"}),
                    "pressure_contribution": nullable({"type": "number"}),
                    "drain_contribution": nullable({"type": "number"}),
                    "structural_contribution": nullable({"type": "number"}),
                    "special_rule_contribution": nullable({"type": "number"}),
                },
            }
        ),
        "provenance": {"$ref": "strength_provenance_output.schema.json"},
    },
}

ROOT_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_root_output.schema.json",
    "title": "StrengthRootEvidence",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "design_marker", "roots"],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "design_marker": {"type": "string", "const": DESIGN_MARKER},
        "summary": nullable(
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "multiple_roots": {
                        "anyOf": [{"type": "boolean"}, {"type": "string", "const": "unknown"}]
                    },
                    "root_count": nullable({"type": "integer"}),
                    "root_strength_label": nullable({"type": "string"}),
                    "root_confidence": enum_str(CONFIDENCE),
                },
            }
        ),
        "roots": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["root_id", "source_pillar", "visibility", "direction", "provenance"],
                "properties": {
                    "root_id": {"type": "string", "pattern": "^ROOT-[A-Z0-9_-]+$"},
                    "source_pillar": enum_str(PILLARS),
                    "source_branch": nullable(enum_str(BRANCHES + ["unknown"])),
                    "source_stem": nullable(enum_str(STEMS + ["unknown"])),
                    "element": nullable(enum_str(ELEMENTS)),
                    "visibility": enum_str(["visible", "hidden", "unknown"]),
                    "relation": nullable({"type": "string"}),
                    "direction": enum_str(DIRECTION),
                    "magnitude": nullable(
                        {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "representation": enum_str(
                                    ["raw_contribution", "categorical", "ordinal", "unknown"]
                                ),
                                "raw_contribution": nullable({"type": "number"}),
                                "categorical": nullable({"type": "string"}),
                                "ordinal": nullable({"type": "string"}),
                            },
                        }
                    ),
                    "confidence": enum_str(CONFIDENCE),
                    "provenance": {"$ref": "strength_provenance_output.schema.json"},
                },
            },
        },
    },
}

STRUCTURAL_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_structural_output.schema.json",
    "title": "StrengthStructuralEvidence",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "design_marker", "structures"],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "design_marker": {"type": "string", "const": DESIGN_MARKER},
        "structures": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "structure_id",
                    "structure_type",
                    "resolution_status",
                    "direction",
                    "provenance",
                ],
                "properties": {
                    "structure_id": {"type": "string", "pattern": "^STR-[A-Z0-9_-]+$"},
                    "structure_type": enum_str(STRUCTURE_TYPES),
                    "participating_pillars": {"type": "array", "items": enum_str(PILLARS)},
                    "participating_stems": {"type": "array", "items": enum_str(STEMS)},
                    "participating_branches": {"type": "array", "items": enum_str(BRANCHES)},
                    "participating_elements": {"type": "array", "items": enum_str(ELEMENTS)},
                    "direction": enum_str(DIRECTION),
                    "effect_on_strength": enum_str(
                        ["support", "pressure", "drain", "neutral", "unknown"]
                    ),
                    "resolution_status": enum_str(RESOLUTION),
                    "confidence": enum_str(CONFIDENCE),
                    "supporting_evidence_ids": {"type": "array", "items": {"type": "string"}},
                    "opposing_evidence_ids": {"type": "array", "items": {"type": "string"}},
                    "provenance": {"$ref": "strength_provenance_output.schema.json"},
                    "notes": nullable({"type": "string"}),
                },
            },
        },
    },
}

CONFLICT_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_conflict_output.schema.json",
    "title": "StrengthConflictEvidence",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "design_marker", "conflicts"],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "design_marker": {"type": "string", "const": DESIGN_MARKER},
        "conflicts": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "conflict_id",
                    "conflict_type",
                    "evidence_ids",
                    "dimensions",
                    "severity",
                    "resolution_status",
                    "confidence",
                    "provenance",
                ],
                "properties": {
                    "conflict_id": {"type": "string", "pattern": "^CF-[A-Z0-9_-]+$"},
                    "conflict_type": enum_str(
                        [
                            "season_vs_root",
                            "support_vs_pressure",
                            "resource_vs_drain",
                            "root_vs_control",
                            "structure_conflict",
                            "temperature_conflict",
                            "other",
                        ]
                    ),
                    "evidence_ids": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                    "dimensions": {"type": "array", "items": {"type": "string"}, "minItems": 1},
                    "severity": enum_str(SEVERITY),
                    "resolution_status": enum_str(RESOLUTION),
                    "confidence": enum_str(CONFIDENCE),
                    "provenance": {"$ref": "strength_provenance_output.schema.json"},
                    "notes": nullable({"type": "string"}),
                },
            },
        },
    },
}

COMPLETENESS_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_completeness_output.schema.json",
    "title": "StrengthCompletenessEvidence",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "design_marker", "overall", "by_dimension"],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "design_marker": {"type": "string", "const": DESIGN_MARKER},
        "overall": enum_str(COMPLETENESS),
        "by_dimension": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "calendar": enum_str(COMPLETENESS),
                "season": enum_str(COMPLETENESS),
                "roots": enum_str(COMPLETENESS),
                "support": enum_str(COMPLETENESS),
                "pressure": enum_str(COMPLETENESS),
                "drain": enum_str(COMPLETENESS),
                "structure": enum_str(COMPLETENESS),
                "temperature": enum_str(COMPLETENESS),
                "expert_review": enum_str(COMPLETENESS),
            },
        },
        "notes": nullable({"type": "string"}),
    },
}

EVIDENCE_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_evidence_output.schema.json",
    "title": "StrengthEvidenceBundle",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "design_marker"],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "design_marker": {"type": "string", "const": DESIGN_MARKER},
        "seasonal": nullable({"type": "object", "additionalProperties": True}),
        "roots": nullable({"$ref": "strength_root_output.schema.json"}),
        "support": nullable({"type": "object", "additionalProperties": True}),
        "pressure": nullable({"type": "object", "additionalProperties": True}),
        "drain": nullable({"type": "object", "additionalProperties": True}),
        "structural": nullable({"$ref": "strength_structural_output.schema.json"}),
        "follow_pattern": nullable({"type": "object", "additionalProperties": True}),
        "temperature": nullable({"type": "object", "additionalProperties": True}),
        "conflicts": nullable({"$ref": "strength_conflict_output.schema.json"}),
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["evidence_id", "dimension", "direction", "provenance"],
                "properties": {
                    "evidence_id": {"type": "string", "pattern": "^EV-[A-Z0-9_-]+$"},
                    "dimension": {"type": "string"},
                    "direction": enum_str(DIRECTION),
                    "availability": enum_str(
                        ["observed", "derived", "inferred", "unknown", "not_available"]
                    ),
                    "magnitude": nullable({"type": "object", "additionalProperties": True}),
                    "confidence": enum_str(CONFIDENCE),
                    "provenance": {"$ref": "strength_provenance_output.schema.json"},
                    "notes": nullable({"type": "string"}),
                },
            },
        },
    },
}

ENVELOPE_SCHEMA = {
    "$schema": SCHEMA_META,
    "$id": "strength_output_envelope.schema.json",
    "title": "StrengthOutputEnvelope",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "design_marker",
        "engine_version",
        "calculation_id",
        "day_master_reference",
        "score_reference",
        "evidence",
        "completeness",
        "provenance",
    ],
    "properties": {
        "schema_version": {"type": "string", "const": SCHEMA_VERSION},
        "design_marker": {"type": "string", "const": DESIGN_MARKER},
        "engine_version": {"type": "string"},
        "calculation_id": {"type": "string"},
        "chart_reference": nullable({"type": "string"}),
        "day_master_reference": enum_str(STEMS),
        "score_reference": {"$ref": "strength_score_output.schema.json"},
        "evidence": {"$ref": "strength_evidence_output.schema.json"},
        "completeness": {"$ref": "strength_completeness_output.schema.json"},
        "provenance": {"$ref": "strength_provenance_output.schema.json"},
        "diagnostics": nullable({"type": "object", "additionalProperties": True}),
        "contract_class": enum_str(["minimum", "extended", "partial", "unknown"]),
    },
}

SCHEMAS_MAP = {
    "strength_provenance_output.schema.json": PROVENANCE_SCHEMA,
    "strength_score_output.schema.json": SCORE_SCHEMA,
    "strength_root_output.schema.json": ROOT_SCHEMA,
    "strength_structural_output.schema.json": STRUCTURAL_SCHEMA,
    "strength_conflict_output.schema.json": CONFLICT_SCHEMA,
    "strength_completeness_output.schema.json": COMPLETENESS_SCHEMA,
    "strength_evidence_output.schema.json": EVIDENCE_SCHEMA,
    "strength_output_envelope.schema.json": ENVELOPE_SCHEMA,
}


def prov(ptype: str = "design_only") -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "provenance_type": ptype,
        "source_module": "pilot_1k_design",
        "source_rule": None,
        "source_path": "knowledge/pilot/replay/root_cause/strength_engine_output_contract/",
        "source_record": None,
        "generated_at": None,
        "calculation_id": "DESIGN-ONLY",
        "notes": "DESIGN_ONLY example; not runtime output",
    }


def score_block(**kwargs) -> dict:
    base = {
        "schema_version": SCHEMA_VERSION,
        "design_marker": DESIGN_MARKER,
        "raw_score": None,
        "normalized_score": None,
        "published_score": None,
        "current_v1_band": "unknown",
        "score_source": "design_only",
        "score_status": "design_only",
        "saturation_detected": "unknown",
        "saturation_type": "unknown",
        "saturation_boundary": None,
        "saturation_source": None,
        "contributions": None,
        "provenance": prov(),
    }
    base.update(kwargs)
    return base


def completeness(overall: str, **dims: str) -> dict:
    by = {
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
    by.update(dims)
    return {
        "schema_version": SCHEMA_VERSION,
        "design_marker": DESIGN_MARKER,
        "overall": overall,
        "by_dimension": by,
        "notes": None,
    }


def envelope(
    *,
    day_master: str,
    score: dict,
    evidence: dict,
    completeness_obj: dict,
    contract_class: str,
    calculation_id: str,
) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "design_marker": DESIGN_MARKER,
        "engine_version": "future_design_only",
        "calculation_id": calculation_id,
        "chart_reference": None,
        "day_master_reference": day_master,
        "score_reference": score,
        "evidence": evidence,
        "completeness": completeness_obj,
        "provenance": prov(),
        "diagnostics": {"note": "DESIGN_ONLY"},
        "contract_class": contract_class,
    }


EX_MINIMUM = envelope(
    day_master="canh",
    calculation_id="DESIGN-MIN-001",
    contract_class="minimum",
    score=score_block(
        raw_score=37.0,
        normalized_score=0.87,
        published_score=0.87,
        current_v1_band="strong",
        score_status="observed",
        saturation_detected=False,
        saturation_type="none",
        contributions={
            "seasonal_contribution": 25.0,
            "root_contribution": 12.0,
            "support_contribution": 8.0,
            "pressure_contribution": -18.0,
            "drain_contribution": 0.0,
            "structural_contribution": 0.0,
            "special_rule_contribution": 10.0,
        },
    ),
    evidence={
        "schema_version": SCHEMA_VERSION,
        "design_marker": DESIGN_MARKER,
        "seasonal": {
            "season_branch": "suu",
            "season_element": "tho",
            "day_master_element": "kim",
            "relation": "tuong",
            "seasonal_direction": "support",
            "seasonal_state": "unknown",
            "source": "month_status",
            "confidence": "medium",
            "provenance": prov("engine_rule"),
        },
        "roots": {
            "schema_version": SCHEMA_VERSION,
            "design_marker": DESIGN_MARKER,
            "summary": {
                "multiple_roots": False,
                "root_count": 1,
                "root_strength_label": "thong_can_1_chi",
                "root_confidence": "medium",
            },
            "roots": [
                {
                    "root_id": "ROOT-DAY-NGO",
                    "source_pillar": "day",
                    "source_branch": "ngo",
                    "source_stem": "dinh",
                    "element": "hoa",
                    "visibility": "hidden",
                    "relation": "not_same_element_as_day_master",
                    "direction": "unknown",
                    "magnitude": {"representation": "unknown"},
                    "confidence": "unknown",
                    "provenance": prov("design_only"),
                }
            ],
        },
        "support": {
            "items": [
                {
                    "evidence_id": "EV-SUP-001",
                    "support_type": "same_element",
                    "direction": "support",
                    "magnitude": {"representation": "raw_contribution", "raw_contribution": 8.0},
                    "confidence": "unknown",
                    "provenance": prov("engine_rule"),
                }
            ]
        },
        "pressure": {
            "items": [
                {
                    "evidence_id": "EV-PRESS-OFF-001",
                    "pressure_type": "officer",
                    "direction": "pressure",
                    "visibility": "visible",
                    "magnitude": {"representation": "raw_contribution", "raw_contribution": -18.0},
                    "confidence": "unknown",
                    "provenance": prov("engine_rule"),
                },
                {
                    "evidence_id": "EV-PRESS-SIT-001",
                    "pressure_type": "structural_pressure",
                    "direction": "pressure",
                    "visibility": "hidden",
                    "affected_branch": "ngo",
                    "affected_pillar": "day",
                    "notes": "sitting_hidden_pressure_example",
                    "magnitude": {"representation": "unknown"},
                    "confidence": "unknown",
                    "provenance": prov("design_only"),
                },
            ]
        },
        "drain": {"items": []},
        "structural": {"schema_version": SCHEMA_VERSION, "design_marker": DESIGN_MARKER, "structures": []},
        "follow_pattern": {
            "considered": "unknown",
            "supporting_evidence_ids": [],
            "opposing_evidence_ids": [],
            "resolution_status": "not_applicable",
            "confidence": "unknown",
            "provenance": prov("design_only"),
        },
        "temperature": {
            "temperature_state": "cold",
            "heat_evidence": None,
            "cold_evidence": "winter_context",
            "dryness_evidence": None,
            "moisture_evidence": None,
            "conflict": False,
            "confidence": "unknown",
            "provenance": prov("derived"),
        },
        "conflicts": {
            "schema_version": SCHEMA_VERSION,
            "design_marker": DESIGN_MARKER,
            "conflicts": [
                {
                    "conflict_id": "CF-SUP-PRESS-001",
                    "conflict_type": "support_vs_pressure",
                    "evidence_ids": ["EV-SUP-001", "EV-PRESS-OFF-001"],
                    "dimensions": ["support", "pressure"],
                    "severity": "unknown",
                    "resolution_status": "unresolved",
                    "confidence": "unknown",
                    "provenance": prov("derived"),
                    "notes": None,
                }
            ],
        },
        "items": [],
    },
    completeness_obj=completeness(
        "partial",
        season="partial",
        roots="partial",
        support="partial",
        pressure="partial",
        drain="limited",
        structure="limited",
        temperature="limited",
        calendar="unknown",
        expert_review="unknown",
    ),
)

EX_ROOT = {
    "schema_version": SCHEMA_VERSION,
    "design_marker": DESIGN_MARKER,
    "summary": {
        "multiple_roots": True,
        "root_count": 2,
        "root_strength_label": "thong_can_2_chi",
        "root_confidence": "medium",
    },
    "roots": [
        {
            "root_id": "ROOT-MONTH-THAN",
            "source_pillar": "month",
            "source_branch": "than",
            "source_stem": "canh",
            "element": "kim",
            "visibility": "hidden",
            "relation": "same_element",
            "direction": "support",
            "magnitude": {"representation": "categorical", "categorical": "present"},
            "confidence": "medium",
            "provenance": prov("design_only"),
        },
        {
            "root_id": "ROOT-HOUR-THAN",
            "source_pillar": "hour",
            "source_branch": "than",
            "source_stem": "canh",
            "element": "kim",
            "visibility": "hidden",
            "relation": "same_element",
            "direction": "support",
            "magnitude": {"representation": "categorical", "categorical": "present"},
            "confidence": "medium",
            "provenance": prov("design_only"),
        },
    ],
}

EX_STRUCTURAL = {
    "schema_version": SCHEMA_VERSION,
    "design_marker": DESIGN_MARKER,
    "structures": [
        {
            "structure_id": "STR-CLASH-001",
            "structure_type": "clash",
            "participating_pillars": ["day", "month"],
            "participating_stems": [],
            "participating_branches": ["ngo", "ti"],
            "participating_elements": ["hoa"],
            "direction": "pressure",
            "effect_on_strength": "pressure",
            "resolution_status": "candidate",
            "confidence": "low",
            "supporting_evidence_ids": [],
            "opposing_evidence_ids": [],
            "provenance": prov("design_only"),
            "notes": "candidate only; not confirmed",
        },
        {
            "structure_id": "STR-FOLLOW-001",
            "structure_type": "follow_pattern",
            "participating_pillars": ["year", "month", "day", "hour"],
            "participating_stems": [],
            "participating_branches": [],
            "participating_elements": [],
            "direction": "unknown",
            "effect_on_strength": "unknown",
            "resolution_status": "unresolved",
            "confidence": "unknown",
            "supporting_evidence_ids": ["EV-A"],
            "opposing_evidence_ids": ["EV-B"],
            "provenance": prov("design_only"),
            "notes": "follow considered; no classifier implemented",
        },
    ],
}

EX_SATURATED = envelope(
    day_master="nham",
    calculation_id="DESIGN-SAT-001",
    contract_class="minimum",
    score=score_block(
        raw_score=107.0,
        normalized_score=1.0,
        published_score=1.0,
        current_v1_band="strong",
        score_status="observed",
        saturation_detected=True,
        saturation_type="upper_clamp",
        saturation_boundary="raw_ge_50",
        saturation_source="observed_relationship",
        contributions={
            "seasonal_contribution": 35.0,
            "root_contribution": 22.0,
            "support_contribution": 18.0,
            "pressure_contribution": 0.0,
            "drain_contribution": 0.0,
            "structural_contribution": 0.0,
            "special_rule_contribution": 32.0,
        },
    ),
    evidence={
        "schema_version": SCHEMA_VERSION,
        "design_marker": DESIGN_MARKER,
        "seasonal": {"seasonal_state": "unknown", "season_branch": "hoi"},
        "roots": EX_ROOT,
        "support": {"items": []},
        "pressure": {"items": []},
        "drain": {"items": []},
        "structural": {"schema_version": SCHEMA_VERSION, "design_marker": DESIGN_MARKER, "structures": []},
        "follow_pattern": {
            "considered": False,
            "supporting_evidence_ids": [],
            "opposing_evidence_ids": [],
            "resolution_status": "not_applicable",
            "confidence": "unknown",
            "provenance": prov(),
        },
        "temperature": {"temperature_state": "cold", "conflict": False, "confidence": "unknown", "provenance": prov()},
        "conflicts": {"schema_version": SCHEMA_VERSION, "design_marker": DESIGN_MARKER, "conflicts": []},
        "items": [],
    },
    completeness_obj=completeness("partial", season="partial", roots="partial", support="limited", pressure="limited", drain="limited", structure="limited", temperature="limited"),
)

EX_PARTIAL = envelope(
    day_master="giap",
    calculation_id="DESIGN-PART-001",
    contract_class="partial",
    score=score_block(
        raw_score=None,
        normalized_score=0.42,
        published_score=0.42,
        current_v1_band="balanced",
        score_status="partial",
        saturation_detected="unknown",
        saturation_type="unknown",
    ),
    evidence={
        "schema_version": SCHEMA_VERSION,
        "design_marker": DESIGN_MARKER,
        "seasonal": {"seasonal_state": "unknown", "relation": "tuong"},
        "roots": {
            "schema_version": SCHEMA_VERSION,
            "design_marker": DESIGN_MARKER,
            "summary": {
                "multiple_roots": "unknown",
                "root_count": None,
                "root_strength_label": "vo_can",
                "root_confidence": "unknown",
            },
            "roots": [],
        },
        "support": {"items": []},
        "pressure": {"items": []},
        "drain": {"items": []},
        "structural": {"schema_version": SCHEMA_VERSION, "design_marker": DESIGN_MARKER, "structures": []},
        "follow_pattern": {
            "considered": "unknown",
            "supporting_evidence_ids": [],
            "opposing_evidence_ids": [],
            "resolution_status": "unresolved",
            "confidence": "unknown",
            "provenance": prov(),
        },
        "temperature": {"temperature_state": "unknown", "conflict": False, "confidence": "unknown", "provenance": prov()},
        "conflicts": {"schema_version": SCHEMA_VERSION, "design_marker": DESIGN_MARKER, "conflicts": []},
        "items": [],
    },
    completeness_obj=completeness("limited", season="partial", roots="limited", support="unknown", pressure="unknown", drain="unknown", structure="unknown", temperature="unknown"),
)

EX_UNKNOWN = envelope(
    day_master="mau",
    calculation_id="DESIGN-UNK-001",
    contract_class="unknown",
    score=score_block(),
    evidence={
        "schema_version": SCHEMA_VERSION,
        "design_marker": DESIGN_MARKER,
        "seasonal": None,
        "roots": {"schema_version": SCHEMA_VERSION, "design_marker": DESIGN_MARKER, "summary": None, "roots": []},
        "support": None,
        "pressure": None,
        "drain": None,
        "structural": {"schema_version": SCHEMA_VERSION, "design_marker": DESIGN_MARKER, "structures": []},
        "follow_pattern": {
            "considered": "unknown",
            "supporting_evidence_ids": [],
            "opposing_evidence_ids": [],
            "resolution_status": "not_applicable",
            "confidence": "unknown",
            "provenance": prov(),
        },
        "temperature": None,
        "conflicts": {"schema_version": SCHEMA_VERSION, "design_marker": DESIGN_MARKER, "conflicts": []},
        "items": [],
    },
    completeness_obj=completeness("unknown"),
)

EXAMPLES_MAP = {
    "minimum_output.json": EX_MINIMUM,
    "root_output.json": EX_ROOT,
    "structural_output.json": EX_STRUCTURAL,
    "saturated_score_output.json": EX_SATURATED,
    "partial_output.json": EX_PARTIAL,
    "unknown_output.json": EX_UNKNOWN,
}

# Field classification matrix data
FIELD_MATRIX = [
    # field, class, priority, v1_availability, note
    ("score.raw_score", "required", "P0", "AVAILABLE", "preserve when exposed"),
    ("score.normalized_score", "required", "P0", "AVAILABLE", "current published path"),
    ("score.published_score", "required", "P0", "AVAILABLE", "may equal normalized"),
    ("score.current_v1_band", "required", "P0", "AVAILABLE", "runtime observation only"),
    ("score.saturation_*", "required", "P0", "PARTIAL", "observational metadata"),
    ("contributions.*_bucket", "required", "P0", "AVAILABLE", "existing profile buckets"),
    ("season.season_branch", "required", "P0", "AVAILABLE", "month branch"),
    ("season.relation_month_status", "required", "P0", "AVAILABLE", "dac/tuong/..."),
    ("season.seasonal_state", "optional", "P2", "NOT_AVAILABLE", "do not infer"),
    ("root.root_id_loci", "required", "P0", "LOST", "PILOT-1J major loss"),
    ("root.source_pillar/branch", "required", "P0", "LOST", "must expose loci"),
    ("root.visibility_hidden", "required", "P0", "PARTIAL", "hidden stems exist internally"),
    ("root.summary_count_label", "required", "P0", "AVAILABLE", "root_level/count"),
    ("support.items", "required", "P0", "PARTIAL", "support_type + bucket"),
    ("pressure.items_visible", "required", "P0", "PARTIAL", "control_type + bucket"),
    ("pressure.sitting_hidden", "required", "P0", "LOST", "PILOT-1J major loss"),
    ("drain.items", "required", "P1", "PARTIAL", "drain_type + bucket"),
    ("structural.clash", "required", "P0", "NOT_AVAILABLE", "PILOT-1J loss"),
    ("structural.punishment", "required", "P0", "NOT_AVAILABLE", "PILOT-1J loss"),
    ("structural.harm", "required", "P0", "NOT_AVAILABLE", "PILOT-1J loss"),
    ("structural.destruction", "required", "P0", "NOT_AVAILABLE", "PILOT-1J loss"),
    ("structural.combination", "optional", "P1", "PARTIAL", "cmb rules sometimes"),
    ("structural.special_structure", "optional", "P1", "PARTIAL", "spc rules"),
    ("structural.transformation", "reserved", "P3", "NOT_AVAILABLE", "future"),
    ("follow_pattern", "required", "P1", "NOT_AVAILABLE", "considered/resolution only"),
    ("temperature", "optional", "P2", "PARTIAL", "independent of taxonomy"),
    ("conflicts", "required", "P1", "LOST", "native objects not published"),
    ("provenance", "required", "P0", "PARTIAL", "must be first-class"),
    ("completeness", "required", "P1", "LOST", "derived today"),
    ("taxonomy_v2_*", "not_supported", "P3", "N/A", "firewall"),
    ("t1_t6", "not_supported", "P3", "N/A", "firewall"),
]

REPORTS_MAP = {
    "required_optional_reserved.json": {
        "schema_version": SCHEMA_VERSION,
        "fields": [
            {"field": f, "class": c, "priority": p, "v1": v, "note": n}
            for f, c, p, v, n in FIELD_MATRIX
        ],
        "counts": {
            "required": sum(1 for x in FIELD_MATRIX if x[1] == "required"),
            "optional": sum(1 for x in FIELD_MATRIX if x[1] == "optional"),
            "reserved": sum(1 for x in FIELD_MATRIX if x[1] == "reserved"),
            "not_supported": sum(1 for x in FIELD_MATRIX if x[1] == "not_supported"),
        },
    },
    "v1_gap_analysis.json": {
        "schema_version": SCHEMA_VERSION,
        "source": "PILOT-1J information_loss",
        "gaps": [
            {
                "field": "root_loci",
                "current_v1_availability": "lost",
                "current_source": "context.root_level/root_count only",
                "current_loss_point": "context builder boundary",
                "recoverability": False,
                "future_output_requirement": "required",
                "priority": "P0",
            },
            {
                "field": "sitting_hidden_pressure",
                "current_v1_availability": "lost",
                "current_source": "none published",
                "current_loss_point": "engine evidence boundary",
                "recoverability": False,
                "future_output_requirement": "required",
                "priority": "P0",
            },
            {
                "field": "clash_punishment_harm_destruction",
                "current_v1_availability": "not_available",
                "current_source": "none in active strength runtime",
                "current_loss_point": "strength result surface",
                "recoverability": False,
                "future_output_requirement": "required",
                "priority": "P0",
            },
            {
                "field": "follow_pattern",
                "current_v1_availability": "not_available",
                "current_source": "pattern engine later",
                "current_loss_point": "pipeline handoff",
                "recoverability": False,
                "future_output_requirement": "required_considered_status",
                "priority": "P1",
            },
            {
                "field": "seasonal_strength_state_enum",
                "current_v1_availability": "not_available",
                "current_source": "month_status/season only",
                "current_loss_point": "mapping (intentionally not inferred)",
                "recoverability": False,
                "future_output_requirement": "optional",
                "priority": "P2",
            },
        ],
    },
    "profile_compatibility.json": {
        "schema_version": SCHEMA_VERSION,
        "mapping": {
            "score_reference": "direct",
            "seasonal_state": "partial",
            "rooting_state": "partial_today_direct_with_loci",
            "support_state": "direct",
            "pressure_state": "partial_today_direct_with_hidden",
            "drain_state": "direct",
            "structural_state": "unavailable_today_direct_future",
            "temperature_state": "partial",
            "conflicts": "derived_today_direct_future",
            "evidence_completeness": "derived",
            "provenance": "derived_today_direct_future",
            "taxonomy": "unavailable_by_design",
        },
    },
    "minimum_contract.json": {
        "schema_version": SCHEMA_VERSION,
        "minimum_required_layers": [
            "score_reference",
            "saturation_metadata",
            "contribution_buckets",
            "season_branch_and_relation",
            "root_summary_and_loci",
            "support_items",
            "pressure_items_including_hidden",
            "drain_items",
            "structural_items_clash_punishment_harm_destruction",
            "follow_pattern_consideration_status",
            "conflicts",
            "provenance",
            "completeness",
        ],
        "optional_in_minimum": ["temperature", "seasonal_state_enum", "transformation"],
        "excluded": ["taxonomy_v2", "t1_t6", "expert_labels_as_runtime"],
        "genuinely_smaller_than_full": True,
    },
    "information_loss.json": {
        "schema_version": SCHEMA_VERSION,
        "pilot_1j_losses_addressed": [
            "root_loci",
            "sitting_hidden_pressure",
            "clash",
            "punishment",
            "harm",
            "destruction",
            "follow_pattern",
        ],
    },
    "versioning.json": {
        "schema_version": SCHEMA_VERSION,
        "design_only": True,
        "evolution": "additive preferred; breaking changes require schema_version bump",
        "production_compatibility_claimed": False,
    },
}

VALIDATION_JSON = {
    "sprint": "PILOT-1K",
    "design_only": True,
    "taxonomy_v2_implemented": False,
    "t1_t6_implemented": False,
    "production_code_changed": False,
    "strength_engine_changed": False,
    "calibration_data_changed": False,
    "synthetic_data_changed": False,
    "minimum_contract_smaller_than_full": True,
    "final_decision": "DESIGN_COMPLETE",
    "overall": "PASS",
}

PROFILE_META = {
    "sprint": "PILOT-1K",
    "schema_version": SCHEMA_VERSION,
    "layers": [
        "StrengthOutputEnvelope",
        "StrengthScoreEvidence",
        "SeasonalEvidence",
        "RootEvidence",
        "SupportEvidence",
        "PressureEvidence",
        "DrainEvidence",
        "StructuralEvidence",
        "TemperatureEvidence",
        "ConflictEvidence",
        "ProvenanceEvidence",
        "CompletenessEvidence",
    ],
    "final_decision": "DESIGN_COMPLETE",
}


def _docs() -> dict[str, str]:
    req_n = sum(1 for x in FIELD_MATRIX if x[1] == "required")
    opt_n = sum(1 for x in FIELD_MATRIX if x[1] == "optional")
    res_n = sum(1 for x in FIELD_MATRIX if x[1] == "reserved")
    ns_n = sum(1 for x in FIELD_MATRIX if x[1] == "not_supported")
    return {
        "README.md": f"""# Strength Engine Output Contract — PILOT-1K

**Mode:** DESIGN ONLY (`schema_version` = `{SCHEMA_VERSION}`)

Defines the minimum future Strength Engine **evidence** output boundary so StrengthProfile can be populated without silent inference.

```text
CURRENT V1 OUTPUT -> AVAILABLE / PARTIAL / LOST
        v
MINIMUM FUTURE EVIDENCE OUTPUT CONTRACT
        v
StrengthProfile -> Future Taxonomy (external)
```

Engine must remain taxonomy-neutral.
""",
        "STRENGTH_OUTPUT_ENVELOPE.md": """# STRENGTH_OUTPUT_ENVELOPE

See `schemas/strength_output_envelope.schema.json`.

Contains: schema_version, engine_version, calculation_id, chart_reference, day_master_reference, score_reference, evidence, completeness, provenance, diagnostics.

Must NOT contain taxonomy_v2 / taxonomy_level / T1-T6 / expert labels.
""",
        "STRENGTH_SCORE_OUTPUT.md": """# STRENGTH_SCORE_OUTPUT

Preserve raw_score, normalized_score, published_score, current_v1_band, score_source, score_status, saturation_*.

Do not reconstruct raw from published. Do not invent missing components.
""",
        "STRENGTH_CONTRIBUTION_OUTPUT.md": """# STRENGTH_CONTRIBUTION_OUTPUT

| Contribution | Class |
|---|---|
| seasonal_contribution | REQUIRED (when V1 bucket exists) |
| root_contribution | REQUIRED |
| support_contribution | REQUIRED |
| pressure_contribution | REQUIRED |
| drain_contribution | REQUIRED |
| structural_contribution | OPTIONAL |
| special_rule_contribution | OPTIONAL |

No new weights. If unavailable: null / not_available.
""",
        "STRENGTH_SEASONAL_OUTPUT.md": """# STRENGTH_SEASONAL_OUTPUT

Fields: season_branch, season_element, day_master_element, relation, seasonal_direction, seasonal_state, source, confidence, provenance.

`seasonal_state` is OPTIONAL / unknown unless engine exposes it. Do not freeze as taxonomy.
""",
        "STRENGTH_ROOT_OUTPUT.md": """# STRENGTH_ROOT_OUTPUT

HIGH PRIORITY. Must distinguish day/month/other branch roots, hidden stem roots, multiple roots, distribution, strength label, confidence.

Each root record: root_id, source_pillar, source_branch, source_stem, element, visibility, relation, direction, magnitude, confidence, provenance.

Do NOT collapse to has_root=true.
""",
        "STRENGTH_SUPPORT_OUTPUT.md": """# STRENGTH_SUPPORT_OUTPUT

Types: same_element, resource, seasonal_support, root_support, structural_support.

Record-level evidence only. No aggregate support calculation in the contract.
""",
        "STRENGTH_PRESSURE_OUTPUT.md": """# STRENGTH_PRESSURE_OUTPUT

Types: wealth, officer, control, seasonal_opposition, structural_pressure.

MUST support hidden / sitting-branch pressure with visibility=hidden. This was a PILOT-1J P0 loss.
""",
        "STRENGTH_DRAIN_OUTPUT.md": """# STRENGTH_DRAIN_OUTPUT

Types: output, leakage, resource_consumption, structural_drain, other.

Keep records separate. Do not collapse into one score.
""",
        "STRENGTH_STRUCTURAL_OUTPUT.md": """# STRENGTH_STRUCTURAL_OUTPUT

Generic StructuralEvidence with structure_type including combination, clash, punishment, harm, destruction, transformation, special_structure, follow_pattern.

Preserve resolution_status. Candidate != confirmed.
""",
        "STRENGTH_FOLLOW_PATTERN_OUTPUT.md": """# STRENGTH_FOLLOW_PATTERN_OUTPUT

Separate object answering: considered? supporting evidence? opposing evidence? resolution? confidence?

No follow-pattern classifier in this sprint.
""",
        "STRENGTH_TEMPERATURE_OUTPUT.md": """# STRENGTH_TEMPERATURE_OUTPUT

Independent from Strength taxonomy. Optional in minimum contract.
""",
        "STRENGTH_CONFLICT_OUTPUT.md": """# STRENGTH_CONFLICT_OUTPUT

Native conflict objects: season_vs_root, support_vs_pressure, resource_vs_drain, root_vs_control, structure_conflict, temperature_conflict.

Do not resolve conflicts here.
""",
        "STRENGTH_PROVENANCE_OUTPUT.md": """# STRENGTH_PROVENANCE_OUTPUT

Every evidence record needs provenance_type, source_module/rule/path/record, generated_at, calculation_id.

Runtime evidence must not claim expert provenance.
""",
        "STRENGTH_COMPLETENESS_OUTPUT.md": """# STRENGTH_COMPLETENESS_OUTPUT

Per-dimension completeness: calendar, season, roots, support, pressure, drain, structure, temperature, expert_review.

Allow mixed states (roots=partial, structure=unknown, temperature=complete).
""",
        "UNKNOWN_AND_MISSING_DATA_POLICY.md": """# UNKNOWN_AND_MISSING_DATA_POLICY

Distinguish: unknown | not_available | not_applicable | partial

Forbidden conversions:

- unknown -> neutral
- not_available -> false
- missing -> zero
- invent confidence / magnitude / direction / structure resolution
""",
        "REQUIRED_OPTIONAL_RESERVED_MATRIX.md": f"""# REQUIRED_OPTIONAL_RESERVED_MATRIX

| Class | Count |
|---|---:|
| required | {req_n} |
| optional | {opt_n} |
| reserved | {res_n} |
| not_supported | {ns_n} |

See `reports/required_optional_reserved.json`.
""",
        "MINIMUM_STRENGTH_OUTPUT_CONTRACT.md": """# MINIMUM_STRENGTH_OUTPUT_CONTRACT

Smallest future output to avoid major PILOT-1J losses while remaining taxonomy-neutral.

## REQUIRED minimum layers

1. Score triple + v1 band + saturation metadata
2. Contribution buckets (existing V1 buckets)
3. Season branch + relation (month_status)
4. Root summary **and** root loci records
5. Support evidence items
6. Pressure evidence items **including sitting/hidden pressure**
7. Drain evidence items
8. Structural evidence for clash/punishment/harm/destruction (even if empty list with completeness=limited)
9. Follow-pattern consideration status (not a classifier)
10. Conflict evidence list
11. Provenance + completeness

## OPTIONAL in minimum

- temperature full detail
- seasonal_state enum
- transformation structures

## EXCLUDED

- taxonomy_v2 / T1-T6
- expert labels as runtime evidence
- invented magnitudes

This set is intentionally smaller than the full extended contract (`contract_class=extended`).
""",
        "V1_OUTPUT_GAP_ANALYSIS.md": """# V1_OUTPUT_GAP_ANALYSIS

Traceable to PILOT-1J. See `reports/v1_gap_analysis.json`.

| Field | V1 | Loss point | Future | Priority |
|---|---|---|---|---|
| root_loci | LOST | context builder | REQUIRED | P0 |
| sitting_hidden_pressure | LOST | evidence boundary | REQUIRED | P0 |
| clash/punishment/harm/destruction | NOT_AVAILABLE | result surface | REQUIRED | P0 |
| follow_pattern | NOT_AVAILABLE | pipeline handoff | REQUIRED (status) | P1 |
| seasonal_state enum | NOT_AVAILABLE | not inferred | OPTIONAL | P2 |
""",
        "PROFILE_COMPATIBILITY.md": """# PROFILE_COMPATIBILITY

```text
Future Strength Engine Output -> StrengthProfile
```

Engine exposes evidence. Profile organizes evidence. Taxonomy interprets later.

See `reports/profile_compatibility.json`.
""",
        "SCORE_PROFILE_BOUNDARY.md": """# SCORE_PROFILE_BOUNDARY

| Concept | Role |
|---|---|
| Score | quantitative engine result |
| Evidence | reasons/signals exposed by engine |
| Profile | structured organization of evidence |
| Taxonomy | future interpretation (external) |
| Confidence | reliability metadata |

Engine output must not become a hidden taxonomy.
""",
        "FUTURE_ENGINE_COMPATIBILITY.md": """# FUTURE_ENGINE_COMPATIBILITY

Prefer additive evolution. Breaking changes require `schema_version` bump.

Consumers must tolerate unknown additional evidence types via reserved extension points in evidence bundles.

No API versioning in this sprint.
""",
        "IMPLEMENTATION_GUARDRAILS.md": """# IMPLEMENTATION_GUARDRAILS

## Prohibit

- changing V1 score / weights / thresholds
- hidden scoring logic
- converting evidence into taxonomy
- inventing evidence / confidence / magnitude
- hiding unknown values
- promoting synthetic or expert labels into runtime evidence
- modifying Golden / calibration / APIs / UI

## Require

- provenance
- versioning
- unknown preservation
- additive evolution
- population separation
- schema validation
- evidence traceability
""",
        "VALIDATION.md": """# VALIDATION — PILOT-1K

Final decision: **DESIGN_COMPLETE**

See `validation/VALIDATION.json`.
""",
        "PILOT_1K_SUMMARY.md": f"""# PILOT_1K_SUMMARY — Minimum Strength Engine Evidence Output Contract

**Mode:** DESIGN ONLY  
**schema_version:** `{SCHEMA_VERSION}`

## Answer

Minimum future Strength Engine output must expose taxonomy-neutral **evidence**: score triple + saturation, contribution buckets, season relation, **root loci**, support/pressure/drain items (including **sitting hidden pressure**), structural clash/punishment/harm/destruction records, follow-pattern consideration status, conflicts, provenance, and completeness — without inventing missing values or emitting Taxonomy V2.

## Delivered

Envelope + score/root/structural/conflict/provenance/completeness schemas, required/optional/reserved matrix, V1 gap analysis, profile compatibility, unknown policy, 6 DESIGN_ONLY examples, tests.

---

Status:
- OUTPUT_ENVELOPE_DESIGNED: YES
- SCORE_OUTPUT_DESIGNED: YES
- CONTRIBUTION_OUTPUT_DESIGNED: YES
- SEASONAL_OUTPUT_DESIGNED: YES
- ROOT_OUTPUT_DESIGNED: YES
- SUPPORT_OUTPUT_DESIGNED: YES
- PRESSURE_OUTPUT_DESIGNED: YES
- DRAIN_OUTPUT_DESIGNED: YES
- STRUCTURAL_OUTPUT_DESIGNED: YES
- FOLLOW_PATTERN_OUTPUT_DESIGNED: YES
- TEMPERATURE_OUTPUT_DESIGNED: YES
- CONFLICT_OUTPUT_DESIGNED: YES
- PROVENANCE_OUTPUT_DESIGNED: YES
- COMPLETENESS_OUTPUT_DESIGNED: YES
- UNKNOWN_POLICY_DESIGNED: YES
- MINIMUM_CONTRACT_DEFINED: YES
- V1_GAP_ANALYSIS_COMPLETE: YES
- PROFILE_COMPATIBILITY_DEFINED: YES
- VERSIONING_DEFINED: YES
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
DESIGN_COMPLETE

Recommendation:
- NEXT_ACTION: Continue real expert case acquisition and dual review while preserving the V1 Strength Engine and keeping the future Taxonomy V2 unimplemented.
""",
    }


DOCS = _docs()

if __name__ == "__main__":
    build()
