"""Compose the semantic Marriage Report Model from Narrative + Decision."""

from __future__ import annotations

from consulting.marriage.models.narrative import MarriageNarrativeResult, MarriageNarrativeSection
from consulting.marriage.models.report import MarriageReportModel, ReportBlock, ReportMetadata, ReportSection
from consulting.marriage.narrative.catalog import action_entry, domain_title, overall_entry
from consulting.marriage.narrative.input import NarrativeInput, RecommendationNarrativeInput
from consulting.marriage.narrative.versions import NARRATIVE_VERSION
from consulting.marriage.policy.versions import DECISION_ENGINE_VERSION, DECISION_MATHEMATICS_VERSION
from consulting.marriage.recommendation.versions import RECOMMENDATION_CATALOG_VERSION
from consulting.marriage.report.labels import GENDER_LABEL, PRIORITY_LABEL, TIMING_WHEN, URGENCY_LABEL
from consulting.marriage.report.versions import (
    CUSTOMER_STORY_ORDER,
    REPORT_MODEL_VERSION,
    report_profile_token,
)


def compose_report(
    payload: NarrativeInput,
    narrative: MarriageNarrativeResult,
) -> MarriageReportModel:
    """Assemble the customer story. Does not recompute Decision or invent actions."""
    by_id = {item.section_id: item for item in narrative.sections}
    sections = [
        _identity(payload),
        _executive_summary(payload, narrative),
        _hero(payload, narrative),
        _highlight_section("strengths", "Điểm hỗ trợ then chốt", "strength", narrative),
        _highlight_section("risks", "Điểm cần điều chỉnh", "risk", narrative),
    ]
    if "timing" in by_id:
        sections.append(_from_narrative("timing", "Nhịp thời điểm", by_id["timing"], "timeline"))
    sections.append(_domains(payload, by_id.get("domains")))
    sections.append(_actions(payload, by_id.get("actions")))
    sections.append(_from_narrative("confidence_limitations", "Độ tin cậy và giới hạn", by_id["confidence"], "confidence"))
    sections.append(_conclusion(payload, narrative))
    sections.append(_appendix(payload, narrative))
    ordered = [item for item in sections if item is not None]
    _assert_story_order([item.section_id for item in ordered])
    return MarriageReportModel(metadata=_metadata(payload, narrative), sections=ordered)


def _identity(payload: NarrativeInput) -> ReportSection:
    """Couple header from presentation-safe labels."""
    gender_a = GENDER_LABEL[payload.person_a_gender]
    gender_b = GENDER_LABEL[payload.person_b_gender]
    return ReportSection(
        section_id="identity",
        title="Hồ sơ cặp đôi",
        summary=f"{payload.person_a_label} và {payload.person_b_label}",
        blocks=[
            ReportBlock(
                block_id="identity-header",
                kind="headline",
                title="Hồ sơ tư vấn hôn nhân",
                body=(
                    f"{payload.person_a_label} ({gender_a}) và "
                    f"{payload.person_b_label} ({gender_b})"
                ),
                semantic_key="marriage.identity.couple",
            )
        ],
    )


def _executive_summary(
    payload: NarrativeInput,
    narrative: MarriageNarrativeResult,
) -> ReportSection:
    """Short overall conclusion, supports, risks, and action themes."""
    overall = overall_entry(payload.overall_state.value)
    strengths = [item.text for item in narrative.highlights if item.kind == "strength"][:3]
    risks = [item.text for item in narrative.highlights if item.kind == "risk"][:3]
    actions = _action_themes(payload.recommendations)
    parts = [overall.observation]
    if strengths:
        parts.append("Điểm hỗ trợ: " + "; ".join(strengths) + ".")
    if risks:
        parts.append("Điểm cần lưu ý: " + "; ".join(risks) + ".")
    if actions:
        parts.append("Hướng hành động: " + "; ".join(actions) + ".")
    if payload.confidence_level.value != "high":
        parts.append("Nên đọc kèm phần giới hạn dữ liệu.")
    blocks = [
        ReportBlock(
            block_id="exec-conclusion",
            kind="summary",
            title=overall.headline,
            body=" ".join(parts),
            semantic_key=overall.key,
            state=payload.overall_state.value,
            source_finding_ids=list(payload.headline_finding_ids),
        )
    ]
    return ReportSection(
        section_id="executive_summary",
        title="Tóm tắt tư vấn",
        summary=overall.headline,
        blocks=blocks,
    )


def _hero(payload: NarrativeInput, narrative: MarriageNarrativeResult) -> ReportSection:
    """Semantic-only compatibility hero. No score or grade."""
    overall = overall_entry(payload.overall_state.value)
    strengths = [item for item in narrative.highlights if item.kind == "strength"][:3]
    risks = [item for item in narrative.highlights if item.kind == "risk"][:3]
    blocks = [
        ReportBlock(
            block_id="hero-state",
            kind="decision_state",
            title=overall.headline,
            body=overall.observation,
            semantic_key=overall.key,
            state=payload.overall_state.value,
            source_finding_ids=list(payload.headline_finding_ids),
        ),
        ReportBlock(
            block_id="hero-headline",
            kind="headline",
            title=overall.headline,
            semantic_key=overall.key,
            state=payload.overall_state.value,
        ),
        ReportBlock(
            block_id="hero-conclusion",
            kind="summary",
            body=overall.observation,
            semantic_key=overall.key,
        ),
        ReportBlock(
            block_id="hero-confidence",
            kind="confidence",
            body=f"Mức tin cậy: {payload.confidence_level.value}",
            semantic_key=f"marriage.confidence.{payload.confidence_level.value}",
        ),
    ]
    for item in strengths:
        blocks.append(
            ReportBlock(
                block_id=f"hero-{item.highlight_id}",
                kind="highlight",
                title="Điểm hỗ trợ",
                body=item.text,
                semantic_key=item.catalog_key,
                source_finding_ids=list(item.source_finding_ids),
            )
        )
    for item in risks:
        blocks.append(
            ReportBlock(
                block_id=f"hero-{item.highlight_id}",
                kind="highlight",
                title="Điểm cần lưu ý",
                body=item.text,
                semantic_key=item.catalog_key,
                source_finding_ids=list(item.source_finding_ids),
            )
        )
    return ReportSection(
        section_id="compatibility_hero",
        title="Tương hợp tổng thể",
        summary=overall.headline,
        blocks=blocks,
    )


def _highlight_section(
    section_id: str,
    title: str,
    kind: str,
    narrative: MarriageNarrativeResult,
) -> ReportSection:
    """Strength or risk list from narrative highlights."""
    items = [item for item in narrative.highlights if item.kind == kind]
    if not items:
        body = (
            "Không có điểm hỗ trợ then chốt được tách riêng; xem nhận định tổng thể."
            if kind == "strength"
            else "Không có điểm áp lực then chốt được công bố riêng ở hồ sơ này."
        )
        blocks = [
            ReportBlock(
                block_id=f"{section_id}-empty",
                kind="paragraph",
                body=body,
                semantic_key=f"marriage.{section_id}.none",
            )
        ]
    else:
        blocks = [
            ReportBlock(
                block_id=item.highlight_id,
                kind="highlight",
                title=item.text,
                body=item.text,
                semantic_key=item.catalog_key,
                source_finding_ids=list(item.source_finding_ids),
            )
            for item in items
        ]
    return ReportSection(section_id=section_id, title=title, blocks=blocks)


def _domains(
    payload: NarrativeInput,
    narrative_section: MarriageNarrativeSection | None,
) -> ReportSection:
    """Available domain analysis. Omit empty optional domains."""
    blocks: list[ReportBlock] = []
    if narrative_section is not None:
        for item in narrative_section.blocks:
            kind = "domain_summary" if item.stage == "observation" else "paragraph"
            if item.stage == "action_bridge":
                kind = "recommendation"
            blocks.append(
                ReportBlock(
                    block_id=item.block_id,
                    kind=kind,
                    title=domain_title(item.domain) if item.domain else None,
                    body=item.text,
                    semantic_key=item.catalog_key,
                    domain=item.domain,
                    source_finding_ids=list(item.source_finding_ids),
                    source_recommendation_ids=list(item.source_recommendation_ids),
                    visibility=item.visibility,
                )
            )
    if not blocks:
        blocks.append(
            ReportBlock(
                block_id="domains-none",
                kind="paragraph",
                body="Không có miền then chốt đủ dữ liệu để giải thích riêng.",
                semantic_key="marriage.domain.none",
            )
        )
    expert_blocks = [
        ReportBlock(
            block_id=f"expert-domain-{domain.domain.value}",
            kind="methodology",
            title=domain_title(domain.domain),
            body=(
                f"state={domain.state.value if domain.state else 'none'}; "
                f"available={domain.available}"
            ),
            semantic_key="marriage.expert.domain",
            domain=domain.domain,
            visibility="expert",
            source_finding_ids=list(domain.finding_ids),
        )
        for domain in payload.domains
        if domain.available
    ]
    return ReportSection(
        section_id="domain_analysis",
        title="Hiểu vì sao",
        blocks=blocks + expert_blocks,
    )


def _actions(
    payload: NarrativeInput,
    narrative_section: MarriageNarrativeSection | None,
) -> ReportSection:
    """Structured action plan from B04 recommendations. Identical intents render once."""
    blocks: list[ReportBlock] = []
    if narrative_section is not None:
        for item in narrative_section.blocks:
            recs = [
                rec
                for rec in payload.recommendations
                if rec.recommendation_id in item.source_recommendation_ids
            ]
            catalog = action_entry(recs[0].action_type) if recs else None
            when_keys = list(dict.fromkeys(rec.timing_key or "" for rec in recs))
            when = TIMING_WHEN.get(when_keys[0], "Áp dụng theo điều kiện đã nêu") if when_keys else "Áp dụng theo điều kiện đã nêu"
            priority = None
            urgency = None
            if recs and recs[0].action_priority:
                priority = PRIORITY_LABEL.get(recs[0].action_priority)
            if recs and recs[0].urgency:
                urgency = URGENCY_LABEL.get(recs[0].urgency)
            what = item.text
            why = catalog.reason if catalog is not None else ""
            outcome = catalog.impact if catalog is not None else ""
            body = f"{what} {why} Khi nào: {when}. {outcome}".strip()
            if priority:
                body = f"{priority}. {body}"
            if urgency:
                body = f"{body} Mức thời điểm: {urgency}."
            title = catalog.headline if catalog is not None else item.catalog_key
            blocks.append(
                ReportBlock(
                    block_id=item.block_id,
                    kind="recommendation",
                    title=title,
                    body=body,
                    semantic_key=item.catalog_key,
                    domain=item.domain,
                    source_finding_ids=list(item.source_finding_ids),
                    source_recommendation_ids=list(item.source_recommendation_ids),
                )
            )
    if not blocks:
        blocks.append(
            ReportBlock(
                block_id="action-none",
                kind="recommendation",
                body="Không có hành động độc lập được công bố.",
                semantic_key="marriage.action.none",
            )
        )
    return ReportSection(section_id="action_plan", title="Kế hoạch hành động", blocks=blocks)


def _from_narrative(
    section_id: str,
    title: str,
    section: MarriageNarrativeSection,
    kind: str,
) -> ReportSection:
    """Copy a narrative section into the report story."""
    blocks = [
        ReportBlock(
            block_id=item.block_id,
            kind=kind,
            body=item.text,
            semantic_key=item.catalog_key,
            domain=item.domain,
            source_finding_ids=list(item.source_finding_ids),
            source_recommendation_ids=list(item.source_recommendation_ids),
        )
        for item in section.blocks
    ]
    return ReportSection(section_id=section_id, title=title, blocks=blocks)


def _conclusion(
    payload: NarrativeInput,
    narrative: MarriageNarrativeResult,
) -> ReportSection:
    """Close the consultation journey without a new decision."""
    overall = overall_entry(payload.overall_state.value)
    body = f"{overall.headline}. {overall.action_bridge}"
    return ReportSection(
        section_id="conclusion",
        title="Kết luận",
        summary=overall.headline,
        blocks=[
            ReportBlock(
                block_id="conclusion-main",
                kind="paragraph",
                title=overall.headline,
                body=body,
                semantic_key=overall.key,
                state=payload.overall_state.value,
                source_finding_ids=list(payload.headline_finding_ids),
            )
        ],
    )


def _appendix(
    payload: NarrativeInput,
    narrative: MarriageNarrativeResult,
) -> ReportSection:
    """Methodology reference. Customer text has no internal IDs."""
    customer = ReportBlock(
        block_id="appendix-method",
        kind="methodology",
        title="Cách đọc hồ sơ",
        body=(
            "Báo cáo này truyền đạt kết luận cấu trúc đã được chốt ở tầng quyết định "
            "và kế hoạch hành động đã được kết từ khuyến nghị. "
            "Không dùng điểm số tương hợp vì mô hình điểm hiện chưa khả dụng."
        ),
        semantic_key="marriage.appendix.method",
        visibility="customer",
    )
    expert = ReportBlock(
        block_id="appendix-trace",
        kind="methodology",
        title="Đối chiếu chuyên gia",
        body=(
            f"policy={payload.policy_version}; narrative={narrative.version}; "
            f"catalog={narrative.catalog_version}; composer={narrative.composer_version}; "
            f"report={report_profile_token()}; decision_engine={DECISION_ENGINE_VERSION}; "
            f"mathematics={DECISION_MATHEMATICS_VERSION}; "
            f"recommendation={RECOMMENDATION_CATALOG_VERSION}; "
            f"score_model={payload.score_model_version}; "
            f"findings={','.join(item.finding_id for item in payload.findings)}; "
            f"correlation_a={payload.person_a_correlation_id}; "
            f"correlation_b={payload.person_b_correlation_id}"
        ),
        semantic_key="marriage.appendix.trace",
        visibility="expert",
        source_finding_ids=[item.finding_id for item in payload.findings],
        source_recommendation_ids=[item.recommendation_id for item in payload.recommendations],
    )
    return ReportSection(
        section_id="appendix",
        title="Phụ lục phương pháp",
        blocks=[customer, expert],
        visibility="customer",
    )


def _metadata(payload: NarrativeInput, narrative: MarriageNarrativeResult) -> ReportMetadata:
    """Capture report identity. Correlation ids are not Canonical-native engine ids."""
    return ReportMetadata(
        consultation_id=payload.consultation_id,
        module_version=payload.module_version,
        policy_version=payload.policy_version,
        recommendation_version=RECOMMENDATION_CATALOG_VERSION,
        narrative_version=narrative.version or NARRATIVE_VERSION,
        report_profile_version=report_profile_token(),
        report_model_version=REPORT_MODEL_VERSION,
        language=narrative.language,
        audience=narrative.audience,
        created_at=payload.created_at,
        person_a_correlation_id=payload.person_a_correlation_id,
        person_b_correlation_id=payload.person_b_correlation_id,
    )


def _action_themes(recommendations: list[RecommendationNarrativeInput]) -> list[str]:
    """Unique action-type headlines for the executive summary."""
    seen: list[str] = []
    labels = {
        "reinforce_strength": "củng cố điểm hỗ trợ",
        "reduce_conflict": "giảm ma sát",
        "role_balance": "chốt vai trò",
        "financial_structure": "quy ước tài chính",
        "timing_awareness": "theo dõi nhịp thời điểm",
    }
    for item in recommendations:
        label = labels.get(item.action_type.value)
        if label and label not in seen:
            seen.append(label)
        if len(seen) >= 3:
            break
    return seen


def _assert_story_order(section_ids: list[str]) -> None:
    """Require present sections to follow the frozen customer story order."""
    allowed = list(CUSTOMER_STORY_ORDER)
    last = -1
    for section_id in section_ids:
        index = allowed.index(section_id)
        if index < last:
            raise ValueError(f"invalid_story_order:{section_id}")
        last = index
