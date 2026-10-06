"""Project business wording from stored structural evidence, without recalculation."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

from consulting.business.models import BusinessProfile
from consulting.business.score import project_business_score
from consulting.marriage.dto.history import MarriageStoredResult
from consulting.marriage.models.matrix import MarriageMatrixRow
from consulting.marriage.models.report import MarriageReportModel, ReportBlock, ReportSection

BUSINESS_SCOPE = "Dẫn chứng hiện phản ánh tương tác giữa hai lá số. Mức phù hợp với ngành/nghề đã chọn cần được đánh giá thêm theo chuyên môn và điều kiện kinh doanh."
GROUPS = (
    ("useful_god", "Dụng thần và Ngũ Hành", "Xem người này có bổ sung đúng hành người kia cần, hay đồng thời kích hoạt hành bất lợi.", "Đối chiếu phần bổ trợ với năng lực thực tế để phân công công việc; nếu có áp lực hai chiều, thống nhất giới hạn trách nhiệm."),
    ("cung_phi", "Cung Phi", "Đối chiếu cung bản mệnh và cung từng trụ theo Du Niên; đây là chỉ báo phụ khi xem khả năng phối hợp.", "Đọc cùng Dụng thần và Can Chi khi cân nhắc cách phối hợp, không dùng riêng Cung Phi để quyết định góp vốn."),
    ("stem_branch", "Can Chi", "Các quan hệ hợp, xung, hình, hại và yếu tố cứu giải giúp lý giải phần đồng thuận hoặc ma sát giữa hai lá số.", "Thống nhất người quyết định cuối cùng, cách phản biện và quy trình giải quyết bất đồng trong công việc."),
    ("pattern", "Mệnh Cục", "Mệnh Cục cung cấp bối cảnh của từng lá số; giống hoặc khác mệnh cục chưa đủ để kết luận hợp hay khắc.", "Dùng bối cảnh này để trao đổi về cách làm việc, rồi kiểm chứng bằng kinh nghiệm và hiệu quả công việc thực tế."),
    ("day_master", "Nhật Chủ", "Quan hệ sinh–khắc và âm dương của Nhật Chủ được đọc cùng Dụng thần và các quan hệ Can Chi.", "Thỏa thuận mức tự chủ của mỗi người và cơ chế kiểm soát chéo khi ra quyết định chung."),
)


def business_context(stored: MarriageStoredResult) -> dict[str, str] | None:
    client = stored.request.request_meta.client if stored.request.request_meta else None
    if not client or client.split(";", 1)[0] != "business_consulting":
        return None
    fields = dict(part.split("=", 1) for part in client.split(";")[1:] if "=" in part)
    return {"occupation": fields.get("occupation", ""), "occupation_label": fields.get("occupation_label", "Chưa ghi nhận ngành/nghề")}


def _verdict(rows: list[MarriageMatrixRow]) -> str:
    statuses = {row.status for row in rows if row.available and row.status != "unavailable"}
    if not statuses:
        return "Chưa đủ dữ liệu để đối chiếu"
    if "mixed" in statuses or {"supportive", "pressured"} <= statuses:
        return "Có cả bổ trợ và điểm cần thỏa thuận"
    if "pressured" in statuses:
        return "Có áp lực cần quản lý khi phối hợp"
    if "supportive" in statuses:
        return "Có yếu tố hỗ trợ trong đối chiếu"
    if statuses == {"reference"}:
        return "Căn cứ tham khảo về bối cảnh hai lá số"
    return "Chưa có xu hướng bổ trợ hoặc áp lực nổi trội"


def build_business_profile(stored: MarriageStoredResult) -> BusinessProfile:
    context = business_context(stored)
    if context is None or stored.report_model is None:
        raise ValueError("business_report_missing")
    name_a = stored.result.person_a.display_name or "Đối tác A"
    name_b = stored.result.person_b.display_name or "Đối tác B"
    labels = {"a_to_b": f"{name_a} bổ trợ {name_b}", "b_to_a": f"{name_b} bổ trợ {name_a}", "ten_gods_a_to_b": f"Vai trò {name_a} → {name_b}", "ten_gods_b_to_a": f"Vai trò {name_b} → {name_a}"}
    matrix = stored.result.compatibility_matrix
    sections = matrix.sections if matrix else []
    by_section = {section.key: [replace(row, label=labels.get(row.key, row.label)) for row in section.rows] for section in sections}

    def rows_for(key: str) -> list[MarriageMatrixRow]:
        if key in {"useful_god", "cung_phi"}:
            return by_section.get(key, [])
        return [row for row in by_section.get("structure", []) if (row.key.startswith("stem_branch") if key == "stem_branch" else row.key == key)]

    cards = []
    assessment_blocks = []
    action_blocks = []
    for key, title, meaning, guidance in GROUPS:
        rows = rows_for(key)
        available = any(row.available and row.status != "unavailable" for row in rows)
        facts = [f"{row.label}: {name_a} - {row.value_a}; {name_b} - {row.value_b}. {row.relationship} Cơ sở: {row.basis}" for row in rows]
        card = {"question_id": key, "question": title, "answer": _verdict(rows), "meaning": meaning, "supporting_facts": facts, "quick_guidance": guidance if available else "Bổ sung dữ liệu lá số trước khi luận phần này.", "confidence": "", "limitations": []}
        cards.append(card)
        assessment_blocks.extend([
            ReportBlock(block_id=f"{key}-answer", kind="answer", title=title, body=card["answer"]),
            ReportBlock(block_id=f"{key}-meaning", kind="paragraph", body=meaning),
            ReportBlock(block_id=f"{key}-guidance", kind="paragraph", body=card["quick_guidance"]),
        ])
        if available and key != "cung_phi":
            action_blocks.append(ReportBlock(block_id=key, kind="recommendation", title=f"Phối hợp theo {title}", body=f"Ưu tiên vừa. {guidance}"))

    core_rows = [row for key in ("useful_god", "stem_branch", "day_master") for row in rows_for(key)]
    supportive = next((row for row in core_rows if row.available and row.status == "supportive"), None)
    pressured = next((row for row in core_rows if row.available and row.status in {"pressured", "mixed"}), None)
    score = project_business_score(matrix)
    score_text = f"{score.score:g}/100" if score.score is not None else "Chưa đủ dữ liệu để chấm điểm"
    overall = f"{score.recommendation}. Điểm tương hợp Bát Tự: {score_text}{' (tạm tính)' if score.provisional and score.score is not None else ''}."
    conclusion = [
        ReportBlock(block_id="conclusion-opinion", kind="paragraph", title="Nhận định chung", body=overall),
        ReportBlock(block_id="conclusion-strength", kind="paragraph", title="Điểm bổ trợ nổi bật", body=f"{supportive.label}: {supportive.relationship}" if supportive else "Chưa có yếu tố hỗ trợ nổi trội đủ dữ liệu để kết luận."),
        ReportBlock(block_id="conclusion-attention", kind="paragraph", title="Điều cần lưu ý", body=f"{pressured.label}: {pressured.relationship}" if pressured else "Cần đọc đầy đủ các hàng đối chiếu và phần thiếu dữ liệu trước khi quyết định hợp tác."),
        ReportBlock(block_id="conclusion-recommendation", kind="paragraph", title="Khuyến nghị", body=f"Đối với lĩnh vực {context['occupation_label']}: {score.advice}"),
    ]
    score_blocks = [ReportBlock(block_id="business-score", kind="paragraph", title="Điểm hợp tác trên thang 100", body=overall), ReportBlock(block_id="business-score-coverage", kind="paragraph", body=f"Độ phủ dữ liệu: {score.coverage:g}%. Độ tin cậy dữ liệu: {score.confidence * 100:g}%.")]
    for group in score.groups:
        detail = f"{group.score:g}/100; trọng số quy ước {group.configured_weight:g}%; trọng số thực tính {group.effective_weight:g}%; đóng góp {group.contribution:g} điểm." if group.score is not None else "Không chấm điểm."
        score_blocks.append(ReportBlock(block_id=f"business-score-{group.key}", kind="paragraph", title=group.title, body=f"{detail} {group.explanation}"))
    score_blocks.extend([
        ReportBlock(block_id="business-score-method", kind="paragraph", title="Cách tính điểm", body=score.methodology),
        ReportBlock(block_id="business-score-bands", kind="paragraph", body="Từ 75 điểm: có thể hợp tác; từ 60 đến dưới 75: hợp tác có điều kiện; từ 45 đến dưới 60: chỉ thử quy mô nhỏ; dưới 45: chưa nên hợp tác dài hạn. Thiếu dữ liệu hoặc áp lực lõi có thể làm khuyến nghị thận trọng hơn mức điểm."),
        ReportBlock(block_id="business-score-guards", kind="paragraph", body="Chỉ đưa ra khuyến nghị khi có đủ ba nhóm lõi, độ phủ ít nhất 80% và độ tin cậy dữ liệu ít nhất 50%. Nhóm lõi dưới 40 điểm giới hạn khuyến nghị ở mức thử quy mô nhỏ; độ tin cậy dưới 70% không cho khuyến nghị thuận lợi nhất."),
        *[ReportBlock(block_id=f"business-score-reason-{index}", kind="paragraph", body=reason) for index, reason in enumerate(score.reasons)],
        ReportBlock(block_id="business-score-disclaimer", kind="paragraph", body=score.disclaimer),
    ])
    conclusion.extend([ReportBlock(block_id=f"conclusion-reason-{index}", kind="paragraph", body=reason) for index, reason in enumerate(score.reasons)])
    conclusion.append(ReportBlock(block_id="conclusion-disclaimer", kind="paragraph", body=score.disclaimer))
    report_sections = [ReportSection(section_id="business_score", title="Điểm và khuyến nghị hợp tác", blocks=score_blocks), ReportSection(section_id="executive_summary", title="Đánh giá hợp tác", summary=overall, blocks=assessment_blocks)]
    for section in sections:
        if section.key not in {"useful_god", "cung_phi", "structure"}:
            continue
        blocks = []
        for row in by_section[section.key]:
            confidence = round(row.confidence * 100)
            status = "Thiếu dữ liệu" if not row.available else {"supportive": "Hỗ trợ", "pressured": "Áp lực", "mixed": "Hai chiều", "balanced": "Cân bằng", "reference": "Tham khảo", "unavailable": "Thiếu dữ liệu"}.get(row.status, row.status)
            blocks.extend([
                ReportBlock(block_id=f"{section.key}-{row.key}", kind="paragraph", title=row.label, body=f"{name_a}: {row.value_a}\n{name_b}: {row.value_b}\nKết quả đối chiếu ({status}): {row.relationship}"),
                ReportBlock(block_id=f"{section.key}-{row.key}-basis", kind="paragraph", body=f"Cơ sở: {row.basis}\nĐộ tin cậy dữ liệu: {confidence}%"),
            ])
        report_sections.append(ReportSection(section_id=f"evidence-{section.key}", title=section.title, summary=section.description, blocks=blocks))
    report_sections.extend([
        ReportSection(section_id="action_plan", title="Gợi ý phối hợp", blocks=action_blocks),
        ReportSection(section_id="conclusion", title="Kết luận hợp tác", blocks=conclusion),
    ])
    return BusinessProfile(saved_at=datetime.now(timezone.utc).isoformat(), report_model=MarriageReportModel(metadata=stored.report_model.metadata, sections=report_sections), assessment_cards=cards, business_score=score)


def resolve_business_profile(stored: MarriageStoredResult) -> BusinessProfile:
    """Old snapshots gain the rubric from stored evidence, never rerun birth analysis."""
    profile = stored.business_profile
    if profile is not None and profile.business_score is not None:
        return profile
    upgraded = build_business_profile(stored)
    return replace(upgraded, saved_at=profile.saved_at) if profile is not None else upgraded
