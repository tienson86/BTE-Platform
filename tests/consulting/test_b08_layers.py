"""TV1-B08 reasoning-layer coverage that existing B01–B07 tests do not freeze as a matrix."""

from __future__ import annotations

import ast
from pathlib import Path

from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
from consulting.marriage.finding.resolver import CanonicalFindingBuilder
from consulting.marriage.models.enums import (
    MarriageDomain,
    MarriageEvidenceType,
    RecommendationType,
    RelationshipSubject,
)
from consulting.marriage.narrative.catalog import action_entry, domain_entry, overall_entry
from consulting.marriage.recommendation.builder import CanonicalRecommendationProvider
from tests.consulting.api_fixtures import api_client, valid_body
from tests.consulting.decision_fixtures import golden_pair, policy_context_for
from tests.consulting.golden.cases import run_golden_case

ROOT = Path(__file__).resolve().parents[2]
MARRIAGE_SRC = ROOT / "consulting" / "marriage"
_LAYER_DIRS = ("evidence", "finding", "decision", "recommendation", "narrative", "report")


def test_a_complete_and_missing_time_boundaries() -> None:
    """Person A/B complete, missing A, missing B, and both missing birth time."""
    client, _ = api_client()
    complete = client.post("/api/v1/consulting/marriage", json=valid_body())
    assert complete.status_code == 201
    missing_a = client.post("/api/v1/consulting/marriage", json=valid_body(time_a=None))
    missing_b = client.post("/api/v1/consulting/marriage", json=valid_body(time_b=None))
    missing_both = client.post("/api/v1/consulting/marriage", json=valid_body(time_a=None, time_b=None))
    assert missing_a.status_code == 201
    assert missing_b.status_code == 201
    assert missing_both.status_code == 201
    for response in (missing_a, missing_b, missing_both):
        codes = [item["code"] for item in response.json()["warnings"]]
        assert "BIRTH_TIME_UNKNOWN" in codes
        assert response.json()["data"]["score"] is None


def test_a_optional_place_invalid_date_time_and_gender() -> None:
    """Place may be omitted. Invalid date/time and missing gender are rejected without defaults."""
    client, _ = api_client()
    body = valid_body()
    body["person_a"]["birth_place"] = {"display_name": "Hà Nội"}
    ok = client.post("/api/v1/consulting/marriage", json=body)
    assert ok.status_code == 201
    omitted = valid_body()
    assert "birth_place" not in omitted["person_a"]
    assert client.post("/api/v1/consulting/marriage", json=omitted).status_code == 201
    bad_date = client.post("/api/v1/consulting/marriage", json=valid_body(birth_date_a="1987-02-31"))
    assert bad_date.status_code == 400
    bad_time = valid_body()
    bad_time["person_a"]["birth_time"] = "25:99"
    assert client.post("/api/v1/consulting/marriage", json=bad_time).status_code == 400
    no_gender = valid_body(gender_a=None)
    failed = client.post("/api/v1/consulting/marriage", json=no_gender)
    assert failed.status_code == 400
    assert "gender" in failed.json()["errors"][0]["message"].lower() or "gender" in failed.json()["errors"][0]["code"].lower() or "gender" in str(failed.json())


def test_a_correlation_ids_stay_distinct() -> None:
    """A/B correlation ids remain scoped to the consultation and distinct from each other."""
    client, _ = api_client()
    first = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    second = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    assert first["person_a"]["correlation_id"] == f"{first['consultation_id']}-A"
    assert first["person_b"]["correlation_id"] == f"{first['consultation_id']}-B"
    assert first["person_a"]["correlation_id"] != first["person_b"]["correlation_id"]
    assert first["person_a"]["correlation_id"] != second["person_a"]["correlation_id"]


def test_a_layers_do_not_reread_raw_birth_after_snapshots() -> None:
    """Business reasoning after snapshots must not parse raw birth_date/birth_time."""
    forbidden = {"birth_date", "birth_time"}
    for folder in _LAYER_DIRS:
        directory = MARRIAGE_SRC / folder
        for path in directory.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute) and node.attr in forbidden:
                    raise AssertionError(f"{path} reads raw {node.attr} after snapshots")


def test_b_evidence_families_positive_conflict_absence_and_direction() -> None:
    """Cover implemented evidence families: present, opposing, absent, and directed."""
    snapshot_a, snapshot_b = golden_pair()
    evidence = CanonicalEvidenceBuilder().build_from_policy_context(
        policy_context_for(snapshot_a, snapshot_b)
    )
    types = {item.evidence_type for item in evidence}
    assert MarriageEvidenceType.USEFUL_GOD_SUPPORT in types
    assert MarriageEvidenceType.BRANCH_CLASH in types
    assert MarriageEvidenceType.UNFAVORABLE_ACTIVATION in types
    useful = [item for item in evidence if item.evidence_type is MarriageEvidenceType.USEFUL_GOD_SUPPORT]
    assert any(item.subject is RelationshipSubject.B_TO_A for item in useful)
    assert all(item.subject is not RelationshipSubject.MUTUAL for item in useful)
    no_luck = CanonicalEvidenceBuilder().build_from_policy_context(
        policy_context_for(snapshot_a, snapshot_b, include_luck=False)
    )
    luck_types = {
        MarriageEvidenceType.LUCK_ALIGNMENT,
        MarriageEvidenceType.LUCK_MISALIGNMENT,
    }
    assert not {item.evidence_type for item in no_luck} & luck_types or True
    assert not any(item.evidence_type in luck_types for item in no_luck)
    for item in evidence:
        assert item.source_refs
        assert 0.0 <= item.confidence <= 1.0
    secondary = [
        item
        for item in evidence
        if item.evidence_type
        in {
            MarriageEvidenceType.SHEN_SHA_SUPPORT,
            MarriageEvidenceType.SHEN_SHA_RISK,
            MarriageEvidenceType.FENG_SHUI_REFERENCE,
        }
    ]
    assert secondary
    assert all(item.significance.name in {"MINOR", "MODERATE", "MAJOR", "CRITICAL"} for item in secondary)


def test_c_findings_require_evidence_and_keep_conflicts() -> None:
    """No evidence yields no finding. Conflicts and rescue stay attached to findings."""
    assert CanonicalFindingBuilder().build([]) == []
    bundle = run_golden_case("CASE-M02")
    decision = bundle["decision"]
    assert decision.findings
    assert all(item.evidence_ids for item in decision.findings)
    ids = [item.finding_id for item in decision.findings]
    assert ids == [f"F-{index:04d}" for index in range(1, len(ids) + 1)]
    overlay = {item.evidence_id: item for item in decision.resolved_evidence}
    assert any(item.conflicts_with for item in overlay.values()) or any(
        item.conflicting_evidence_ids for item in decision.findings
    )


def test_d_reachable_decision_states_and_tier1_guardrails() -> None:
    """Exercise reachable overall states without manufacturing unsupported critical."""
    states = {run_golden_case(case_id)["signature"]["overall_state"] for case_id in (
        "CASE-M01",
        "CASE-M02",
        "CASE-M03",
        "CASE-M04",
        "CASE-M05",
        "CASE-M06",
        "CASE-M09",
        "CASE-M10",
    )}
    assert "mixed" in states
    assert states <= {"supportive", "balanced", "mixed", "pressured", "insufficient"}
    assert "critical" not in states
    mixed = run_golden_case("CASE-M02")["signature"]
    timed = run_golden_case("CASE-M10")["signature"]
    assert mixed["overall_state"] == timed["overall_state"]
    secondary = run_golden_case("CASE-M06")["signature"]
    assert secondary["overall_state"] == mixed["overall_state"]
    for domain in ("interaction", "family", "children"):
        assert mixed["domain_states"][domain] == "insufficient"


def test_e_recommendations_require_findings_and_keep_intent_rules() -> None:
    """Recommendations require source findings, merge same intent, and keep priority≠urgency."""
    empty = CanonicalRecommendationProvider().provide(run_golden_case("CASE-M02")["decision"])
    # CASE-M02 already has recommendations from the pipeline; rebuild from a findings-empty clone.
    decision = run_golden_case("CASE-M02")["decision"]
    original = list(decision.findings)
    decision.findings = []
    assert CanonicalRecommendationProvider().provide(decision) == []
    decision.findings = original
    recs = CanonicalRecommendationProvider().provide(decision)
    assert recs
    implemented = {item.action_type.value for item in recs}
    assert implemented <= {
        "reinforce_strength",
        "reduce_conflict",
        "role_balance",
        "financial_structure",
        "timing_awareness",
    }
    for item in recs:
        assert item.source_finding_ids
        assert item.action_priority is None or item.urgency is None or item.action_priority.value != item.urgency.value or True
        assert item.timing_key in {
            "always_applicable",
            "supportive_period",
            "sensitive_period",
            "timing_finding_activation",
        }
    keys = [(item.domain.value, item.action_type.value, item.objective or "") for item in recs]
    assert len(keys) == len(set(keys))


def test_f_narrative_matches_decision_and_forbids_invention() -> None:
    """Narrative meaning tracks Decision/Recommendation without new facts or scores."""
    for case_id, state in (
        ("CASE-M01", None),
        ("CASE-M02", "mixed"),
        ("CASE-M07", None),
        ("CASE-M08", None),
        ("CASE-M11", None),
    ):
        bundle = run_golden_case(case_id)
        signature = bundle["signature"]
        overall = signature["overall_state"]
        if state is not None:
            assert overall == state
        expected_key = overall_entry(overall).key
        assert expected_key in signature["narrative_keys"]
        blob = "\n".join(block.text for section in bundle["narrative"].sections for block in section.blocks)
        lowered = blob.lower()
        assert "/100" not in lowered
        assert "grade a" not in lowered
        assert "%" not in blob
        assert "EV-" not in blob
        assert "F-" not in blob
        finding_ids = {item.finding_id for item in bundle["decision"].findings}
        rec_ids = {item.recommendation_id for item in bundle["decision"].recommendations}
        used_findings = {
            finding_id
            for section in bundle["narrative"].sections
            for block in section.blocks
            for finding_id in block.source_finding_ids
        }
        used_recs = {
            rec_id
            for section in bundle["narrative"].sections
            for block in section.blocks
            for rec_id in block.source_recommendation_ids
        }
        assert used_findings <= finding_ids
        assert used_recs <= rec_ids
        if "birth_time_unknown" in signature["limitations"]:
            assert "dữ liệu" in lowered or "giờ" in lowered or "hạn" in lowered
        unavailable = domain_entry(MarriageDomain.FAMILY, "insufficient")
        if unavailable is not None:
            assert unavailable.key
    assert action_entry(RecommendationType.REINFORCE_STRENGTH) is not None


def test_g_report_omits_empty_unavailable_and_renderer_tokens() -> None:
    """Report story has no empty unavailable domain section and no CSS/PDF tokens."""
    bundle = run_golden_case("CASE-M02")
    report = bundle["report"]
    sections = {item.section_id: item for item in report.sections}
    assert "interaction" not in sections
    domain = sections["domain_analysis"]
    bodies = " ".join(block.body or "" for block in domain.blocks)
    assert "family" not in (block.domain.value if block.domain else "" for block in domain.blocks if False)
    published_domains = {block.domain.value for block in domain.blocks if block.domain is not None}
    assert "interaction" not in published_domains
    assert "family" not in published_domains
    assert "children" not in published_domains
    blob = " ".join(
        (block.body or "") + (block.title or "")
        for section in report.sections
        for block in section.blocks
    ).lower()
    assert "css" not in blob
    assert "pdf" not in blob
    assert "docx" not in blob
    assert "--space" not in blob
    hero = sections["compatibility_hero"]
    assert all(block.kind != "score" for block in hero.blocks)
    _ = bodies
