"""Deterministic snapshot fixtures for TV1-B03 decision tests."""

from __future__ import annotations

from consulting.marriage.constants import MODULE_VERSION
from consulting.marriage.models.enums import CanonicalGender, FiveElement, PersonSide, YinYang
from consulting.marriage.models.options import ResolvedMarriageOptions
from consulting.marriage.models.person import (
    BirthDataQuality,
    CanonicalVersionReference,
    MarriagePersonReference,
)
from consulting.marriage.models.snapshot import (
    DayMasterSnapshot,
    ElementOrStemReference,
    FengShuiSnapshot,
    FiveElementSnapshot,
    LuckCycleSnapshot,
    LuckSnapshot,
    MarriageCanonicalSnapshot,
    PatternSnapshot,
    PillarSnapshot,
    PillarValue,
    ShenShaItem,
    ShenShaSnapshot,
    StrengthSnapshot,
    TenGodItem,
    TenGodSnapshot,
    UsefulGodSnapshot,
)
from consulting.marriage.models.versioning import MarriageVersionBundle
from consulting.marriage.policy.context import MarriagePolicyContext
from consulting.marriage.policy.versions import (
    EVIDENCE_CATALOG_VERSION,
    SCORE_MODEL_VERSION,
    policy_version_token,
)


def pillar(stem: str, branch: str, *, na_yin: str | None = None) -> PillarValue:
    """Build one pillar value."""
    return PillarValue(
        stem=stem,
        branch=branch,
        can_chi=f"{stem} {branch}",
        na_yin=na_yin,
    )


def person_ref(
    *,
    analysis_id: str,
    gender: CanonicalGender = CanonicalGender.MALE,
    hour_known: bool = True,
) -> MarriagePersonReference:
    """Build a person reference with explicit data-quality flags."""
    limitations = [] if hour_known else ["birth_time_unknown"]
    flags = (True, hour_known, False, True)
    return MarriagePersonReference(
        analysis_id=analysis_id,
        gender=gender,
        birth_data_quality=BirthDataQuality(
            birth_date_known=True,
            birth_time_known=hour_known,
            birth_place_known=False,
            timezone_resolved=True,
            completeness_score=sum(1 for flag in flags if flag) / 4.0,
            limitations=limitations,
        ),
        canonical_version=CanonicalVersionReference(
            bazi_version="li_chun_jdn_v1",
            strength_version="analysis_result.StrengthView@1.0",
            useful_god_version="analysis_result.UsefulGodView@1.5",
        ),
    )


def make_snapshot(
    *,
    analysis_id: str,
    side: PersonSide,
    gender: CanonicalGender,
    day_stem: str,
    day_branch: str,
    day_element: FiveElement,
    useful: FiveElement,
    unfavorable: FiveElement | None = FiveElement.WATER,
    useful_role: str = "Chính Quan",
    unfavorable_role: str = "Thiên Ấn",
    year_stem: str = "Bính",
    year_branch: str = "Dần",
    month_stem: str = "Tân",
    month_branch: str = "Sửu",
    hour_stem: str | None = "Mậu",
    hour_branch: str | None = "Dần",
    hour_known: bool = True,
    distribution: dict[FiveElement, float] | None = None,
    ten_god_visible: str = "Thất Sát",
    luck_stem: str = "Giáp",
    luck_branch: str = "Tý",
    shen_sha: list[ShenShaItem] | None = None,
    cung_phi: str | None = "Khảm",
    na_yin: str | None = None,
) -> MarriageCanonicalSnapshot:
    """Build a Canonical snapshot for decision tests. No engine calls."""
    counts = distribution or {
        FiveElement.WOOD: 2.0,
        FiveElement.FIRE: 3.0,
        FiveElement.EARTH: 2.0,
        FiveElement.METAL: 2.0,
        FiveElement.WATER: 1.0,
    }
    hour = None
    if hour_known and hour_stem and hour_branch:
        hour = pillar(hour_stem, hour_branch, na_yin=na_yin)
    unfavorable_refs = None
    if unfavorable is not None:
        unfavorable_refs = [
            ElementOrStemReference(element=unfavorable, role=unfavorable_role)
        ]
    return MarriageCanonicalSnapshot(
        person=person_ref(analysis_id=analysis_id, gender=gender, hour_known=hour_known),
        pillars=PillarSnapshot(
            year=pillar(year_stem, year_branch, na_yin=na_yin),
            month=pillar(month_stem, month_branch, na_yin=na_yin),
            day=pillar(day_stem, day_branch, na_yin=na_yin),
            hour=hour,
        ),
        day_master=DayMasterSnapshot(
            stem=day_stem,
            element=day_element,
            yin_yang=YinYang.YANG,
        ),
        five_elements=FiveElementSnapshot(distribution=counts),
        strength=StrengthSnapshot(classification="strong", score=0.8, confidence=0.9),
        pattern=PatternSnapshot(pattern_id="chinh_an"),
        useful_god=UsefulGodSnapshot(
            useful=[ElementOrStemReference(element=useful, role=useful_role)],
            favorable=[ElementOrStemReference(element=useful, role=useful_role)],
            unfavorable=unfavorable_refs,
            confidence=0.8,
        ),
        ten_gods=TenGodSnapshot(
            visible=[TenGodItem(name=ten_god_visible, source_pillar="year", source_stem=year_stem)],
            hidden=[TenGodItem(name=unfavorable_role, source_pillar="month")],
        ),
        source_analysis_id=analysis_id,
        luck=LuckSnapshot(
            cycles=[
                LuckCycleSnapshot(
                    index=0,
                    start_year=2020,
                    end_year=2029,
                    can_chi=f"{luck_stem} {luck_branch}",
                    stem=luck_stem,
                    branch=luck_branch,
                )
            ],
            current_cycle=LuckCycleSnapshot(
                index=0,
                start_year=2020,
                end_year=2029,
                can_chi=f"{luck_stem} {luck_branch}",
                stem=luck_stem,
                branch=luck_branch,
            ),
        ),
        shen_sha=ShenShaSnapshot(items=shen_sha or [ShenShaItem(name="Đào Hoa")]),
        feng_shui=FengShuiSnapshot(cung_phi=cung_phi) if cung_phi else None,
    )


def golden_pair() -> tuple[MarriageCanonicalSnapshot, MarriageCanonicalSnapshot]:
    """A/B pair used by golden decision assertions."""
    snapshot_a = make_snapshot(
        analysis_id="MC-GOLDEN-A",
        side=PersonSide.A,
        gender=CanonicalGender.MALE,
        day_stem="Canh",
        day_branch="Tý",
        day_element=FiveElement.METAL,
        useful=FiveElement.FIRE,
        unfavorable=FiveElement.WATER,
        luck_stem="Quý",
        luck_branch="Hợi",
    )
    snapshot_b = make_snapshot(
        analysis_id="MC-GOLDEN-B",
        side=PersonSide.B,
        gender=CanonicalGender.FEMALE,
        day_stem="Bính",
        day_branch="Ngọ",
        day_element=FiveElement.FIRE,
        useful=FiveElement.WOOD,
        unfavorable=FiveElement.WATER,
        year_stem="Giáp",
        year_branch="Dần",
        ten_god_visible="Chính Quan",
        luck_stem="Giáp",
        luck_branch="Dần",
        distribution={
            FiveElement.WOOD: 3.0,
            FiveElement.FIRE: 4.0,
            FiveElement.EARTH: 1.0,
            FiveElement.METAL: 1.0,
            FiveElement.WATER: 1.0,
        },
    )
    return snapshot_a, snapshot_b


def policy_context_for(
    snapshot_a: MarriageCanonicalSnapshot,
    snapshot_b: MarriageCanonicalSnapshot,
    *,
    include_luck: bool | None = True,
    include_shen_sha: bool | None = True,
    include_feng_shui_reference: bool | None = True,
) -> MarriagePolicyContext:
    """Build a frozen policy context from two snapshots."""
    limitations = tuple(
        dict.fromkeys(
            [
                *snapshot_a.person.birth_data_quality.limitations,
                *snapshot_b.person.birth_data_quality.limitations,
            ]
        )
    )
    return MarriagePolicyContext(
        consultation_id="MC-TEST",
        snapshot_a=snapshot_a,
        snapshot_b=snapshot_b,
        options=ResolvedMarriageOptions(
            include_luck=include_luck,
            include_shen_sha=include_shen_sha,
            include_feng_shui_reference=include_feng_shui_reference,
        ),
        versions=MarriageVersionBundle(
            module_version=MODULE_VERSION,
            decision_profile_version=policy_version_token(),
            score_model_version=SCORE_MODEL_VERSION,
            rule_catalog_version=EVIDENCE_CATALOG_VERSION,
            canonical_versions=snapshot_a.person.canonical_version,
        ),
        available_domains=(),
        limitations=limitations,
        source_analysis_id_a=snapshot_a.source_analysis_id,
        source_analysis_id_b=snapshot_b.source_analysis_id,
    )


def build_test_decision(
    snapshot_a: MarriageCanonicalSnapshot | None = None,
    snapshot_b: MarriageCanonicalSnapshot | None = None,
    **policy_kwargs: object,
) -> MarriageDecisionResult:
    """Build a B03 Decision Result from snapshots. Does not generate recommendations."""
    from consulting.marriage.decision.comparison import build_marriage_comparison
    from consulting.marriage.decision.context import MarriageDecisionContext
    from consulting.marriage.decision.resolver import MarriageDecisionResolverV1, build_confidence
    from consulting.marriage.evidence.extractor import CanonicalEvidenceBuilder
    from consulting.marriage.evidence.resolver import MarriageEvidenceResolver
    from consulting.marriage.finding.resolver import CanonicalFindingBuilder
    from consulting.marriage.models.context import MarriageRelationshipContext
    from consulting.marriage.models.result import MarriageDecisionResult

    if snapshot_a is None or snapshot_b is None:
        snapshot_a, snapshot_b = golden_pair()
    context = policy_context_for(snapshot_a, snapshot_b, **policy_kwargs)  # type: ignore[arg-type]
    evidence = CanonicalEvidenceBuilder().build_from_policy_context(context)
    resolved = MarriageEvidenceResolver().resolve(evidence)
    findings = CanonicalFindingBuilder().build_from_resolved(evidence, resolved)
    decision_context = MarriageDecisionContext(
        consultation_id=context.consultation_id,
        relationship=MarriageRelationshipContext(
            person_a=snapshot_a,
            person_b=snapshot_b,
            options=context.options,
            available_domains=list(context.available_domains),
            limitations=list(context.limitations),
        ),
        versions=context.versions,
        evidence=evidence,
        findings=findings,
    )
    resolver = MarriageDecisionResolverV1()
    domains = resolver.resolve_domains(decision_context)
    overall = resolver.resolve_overall(decision_context)
    coverage = sum(
        1
        for item in (
            domains.five_elements,
            domains.stem_branch,
            domains.ten_gods,
            domains.interaction,
            domains.finance,
            domains.family,
            domains.children,
            domains.luck,
        )
        if item.availability.available
    ) / 8.0
    result = MarriageDecisionResult(
        consultation_id=context.consultation_id,
        person_a=snapshot_a.person,
        person_b=snapshot_b.person,
        canonical_a=snapshot_a,
        canonical_b=snapshot_b,
        evidence=evidence,
        domains=domains,
        overall=overall,
        recommendations=[],
        confidence=build_confidence(
            data_quality=(
                snapshot_a.person.birth_data_quality.completeness_score
                + snapshot_b.person.birth_data_quality.completeness_score
            )
            / 2.0,
            evidence=evidence,
            limitations=list(context.limitations),
            engine_coverage=coverage,
        ),
        versions=context.versions,
        created_at="2026-01-01T00:00:00+00:00",
        resolved_evidence=resolved,
        findings=findings,
        limitations=list(context.limitations),
    )
    result.comparison = build_marriage_comparison(result)
    return result
