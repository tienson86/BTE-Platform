# -*- coding: utf-8 -*-
"""Generate Wave 1.1 Knowledge Units CSV with correct quoting."""
from __future__ import annotations

import csv
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "database" / "20_knowledge" / "21_knowledge_units.csv"

FIELDNAMES = [
    "knowledge_unit_id",
    "title",
    "summary",
    "purpose",
    "kind",
    "domain",
    "scenarios",
    "primary_intent",
    "secondary_intent",
    "condition",
    "evidence_kind",
    "required_evidence",
    "required_interpretation",
    "narrative_targets",
    "consultation_goals",
    "decision_posture",
    "action_category",
    "risk_category",
    "opportunity_category",
    "primary_usage",
    "secondary_usage",
    "priority",
    "confidence",
    "confidence_requirement",
    "commercial_value",
    "ethics_flags",
    "signal_refs",
    "ref_ids",
    "paired_unit_ids",
    "classical_text",
    "modern_interpretation",
    "version",
    "review_status",
    "author",
    "author_notes",
    "reviewers",
    "wave_id",
]

ROWS = [
    {
        "knowledge_unit_id": "KU-ID-001",
        "title": "Identity Core",
        "summary": "Đặt tên cấu trúc lá số bằng ngôn ngữ tư vấn: Nhật chủ + cách cục + mức thân.",
        "purpose": "Giúp khách hiểu họ là ai trong lá số này trước khi bàn quyết định.",
        "kind": "Analytical",
        "domain": "CK-ID",
        "scenarios": "CS-ID;default",
        "primary_intent": "Làm rõ danh tính tư vấn của lá số",
        "secondary_intent": "Khung mở cho mọi kịch bản Result mặc định",
        "condition": "analysis.has_day_master AND analysis.has_pattern_or_strength_band",
        "evidence_kind": "identity",
        "required_evidence": "grade",
        "required_interpretation": "overview;strength;pattern;summary",
        "narrative_targets": "executive_summary;observation;conclusion",
        "consultation_goals": "clarify_identity",
        "decision_posture": "",
        "action_category": "",
        "risk_category": "",
        "opportunity_category": "",
        "primary_usage": "Executive Summary;Interpretation",
        "secondary_usage": "Portal;Report;AI Assistant;Search;Mobile;Future APIs",
        "priority": "100",
        "confidence": "0.92",
        "confidence_requirement": "0.60",
        "commercial_value": "C",
        "ethics_flags": "none",
        "signal_refs": "day_master;pattern_label;strength_band",
        "ref_ids": "REF-000003;REF-000006",
        "paired_unit_ids": "",
        "classical_text": (
            "Nhật chủ là gốc; xem cách cục và khí thế ngày để định hình nhân dạng mệnh lý "
            "(diễn giải hiện đại theo tinh thần Tử Bình)."
        ),
        "modern_interpretation": (
            "Bạn là người mang Nhật chủ {day_master_label} trong cấu trúc {pattern_label}. "
            "Ở mức thân {strength_band_label}, đây là danh tính cốt lõi cần dùng xuyên suốt buổi tư vấn: "
            "mọi nhận xét sau này phải bám vào khung này thay vì liệt kê kỹ thuật rời."
        ),
        "version": "1.0.0",
        "review_status": "awaiting_review",
        "author": "BTE Knowledge Author",
        "author_notes": "Wave 1.1 core pack. Placeholders bind from Analysis only — never invent.",
        "reviewers": "",
        "wave_id": "W-P0-1.1-CORE",
    },
    {
        "knowledge_unit_id": "KU-ST-001",
        "title": "Strength Core",
        "summary": "Giải thích thế mạnh cấu trúc khi thân được nâng đỡ — dùng cho ô strengths của Tóm tắt điều hành.",
        "purpose": "Cho khách thấy điểm tựa thật của lá số bằng ngôn ngữ chuyên gia không kỹ thuật.",
        "kind": "Analytical",
        "domain": "CK-ID",
        "scenarios": "CS-ID;CS-PG;default",
        "primary_intent": "Làm rõ điểm mạnh cốt lõi",
        "secondary_intent": "Hỗ trợ đọc cơ hội khi có tín hiệu thuận",
        "condition": "analysis.strength_band IN (vuong;can;strong_support) OR analysis.strength_score_favorable = true",
        "evidence_kind": "strength",
        "required_evidence": "identity",
        "required_interpretation": "strength;summary",
        "narrative_targets": "executive_summary;observation;reasoning;conclusion",
        "consultation_goals": "name_core_strengths",
        "decision_posture": "",
        "action_category": "",
        "risk_category": "",
        "opportunity_category": "role_fit",
        "primary_usage": "Executive Summary;Interpretation",
        "secondary_usage": "Portal;Report;AI Assistant;Search;Mobile;Future APIs",
        "priority": "95",
        "confidence": "0.90",
        "confidence_requirement": "0.60",
        "commercial_value": "C",
        "ethics_flags": "none",
        "signal_refs": "strength_band;strength_score;support_signals",
        "ref_ids": "REF-000003;REF-000005",
        "paired_unit_ids": "",
        "classical_text": (
            "Thân được sinh phù thì khí đứng vững; luận dụng phải thuận thế mà không khoe khoang "
            "(diễn giải hiện đại)."
        ),
        "modern_interpretation": (
            "Điểm tựa chính của bạn nằm ở chỗ cấu trúc đang được nâng đỡ: thân {strength_band_label} "
            "cho thấy bạn có nền để chịu trách nhiệm và duy trì nhịp dài. Trong tư vấn thương mại hãy nêu "
            "1–2 thế mạnh cụ thể gắn tín hiệu đã có (sinh phù / cách cục thuận) — không phóng đại thành "
            "bảo chứng thành công."
        ),
        "version": "1.0.0",
        "review_status": "awaiting_review",
        "author": "BTE Knowledge Author",
        "author_notes": "Emits only when strength signals are favorable; drop_if_analysis_conflicts.",
        "reviewers": "",
        "wave_id": "W-P0-1.1-CORE",
    },
    {
        "knowledge_unit_id": "KU-WK-001",
        "title": "Weakness Core",
        "summary": "Đặt tên điểm hạn chế cấu trúc một cách điềm tĩnh — không xấu hổ hóa khách.",
        "purpose": "Giúp Tóm tắt điều hành có ô weaknesses/risks trung thực và có thể gắn khuyến nghị.",
        "kind": "Analytical",
        "domain": "CK-ID",
        "scenarios": "CS-ID;CS-MD;default",
        "primary_intent": "Làm rõ điểm cần giữ nhịp / giới hạn lực",
        "secondary_intent": "Gợi mở Warning khi có xung khắc hoặc thân suy",
        "condition": "analysis.strength_band IN (nhuoc;weak;overtaxed) OR analysis.has_enemy_or_clash_caution = true",
        "evidence_kind": "weakness",
        "required_evidence": "identity",
        "required_interpretation": "strength;summary;useful_god",
        "narrative_targets": "executive_summary;warning;conclusion",
        "consultation_goals": "name_core_cautions",
        "decision_posture": "",
        "action_category": "",
        "risk_category": "timing_hostility;lifestyle_imbalance",
        "opportunity_category": "",
        "primary_usage": "Executive Summary;Warning",
        "secondary_usage": "Portal;Report;AI Assistant;Search;Mobile;Future APIs",
        "priority": "95",
        "confidence": "0.88",
        "confidence_requirement": "0.60",
        "commercial_value": "C",
        "ethics_flags": "none",
        "signal_refs": "strength_band;enemy_god;clash_flags",
        "ref_ids": "REF-000005;REF-000006",
        "paired_unit_ids": "KU-RC-001",
        "classical_text": (
            "Chỗ thân suy hoặc bị khắc chế cần giữ mực; luận sát phải ôn hòa "
            "(diễn giải hiện đại theo tinh thần Địch Thiên Tủy / Tử Bình)."
        ),
        "modern_interpretation": (
            "Điểm cần giữ của bạn là chỗ lực cấu trúc đang mỏng hoặc dễ bị kéo quá mức: "
            "{weakness_signal_label}. Hãy nói thẳng nhưng điềm tĩnh — đây là giới hạn cần thiết kế "
            "nhịp sống và quyết định chứ không phải nhãn tính cách tiêu cực. Ưu tiên giảm tải trước "
            "khi mở rộng."
        ),
        "version": "1.0.0",
        "review_status": "awaiting_review",
        "author": "BTE Knowledge Author",
        "author_notes": "Pairs commercially with KU-RC-001. Placeholder {weakness_signal_label} from Analysis.",
        "reviewers": "",
        "wave_id": "W-P0-1.1-CORE",
    },
    {
        "knowledge_unit_id": "KU-UG-001",
        "title": "Useful God Core",
        "summary": "Giải thích Dụng thần như kim chỉ nam ưu tiên — nền cho khuyến nghị cốt lõi.",
        "purpose": "Biến tín hiệu useful god thành ngôn ngữ định hướng đời sống khách hiểu được.",
        "kind": "Analytical",
        "domain": "CK-DM",
        "scenarios": "CS-ID;CS-CA;CS-MD;CS-LT;default",
        "primary_intent": "Hiểu ưu tiên điều chỉnh theo Dụng thần",
        "secondary_intent": "Khung lý giải cho Career/Luck nhẹ",
        "condition": "analysis.has_useful_god = true",
        "evidence_kind": "explanation",
        "required_evidence": "identity",
        "required_interpretation": "useful_god;summary;strength",
        "narrative_targets": "executive_summary;reasoning;impact;recommendation",
        "consultation_goals": "explain_priority_direction",
        "decision_posture": "",
        "action_category": "useful_god_alignment",
        "risk_category": "",
        "opportunity_category": "",
        "primary_usage": "Executive Summary;Interpretation;Recommendation",
        "secondary_usage": "Portal;Report;AI Assistant;Search;Mobile;Future APIs",
        "priority": "98",
        "confidence": "0.91",
        "confidence_requirement": "0.65",
        "commercial_value": "C",
        "ethics_flags": "none",
        "signal_refs": "useful_god;favorable_gods;unfavorable_gods",
        "ref_ids": "REF-000003;REF-000006;REF-000007",
        "paired_unit_ids": "KU-RC-001",
        "classical_text": (
            "Dụng thần là chỗ nên thuận; nghịch dụng thì dễ lệch nhịp "
            "(diễn giải hiện đại theo tinh thần Tử Bình)."
        ),
        "modern_interpretation": (
            "Ưu tiên then chốt của lá số này là thuận theo Dụng thần {useful_god_label}. "
            "Mọi lựa chọn lớn (việc làm, nhịp sống, thời điểm) nên được kiểm bằng câu hỏi: "
            "điều này có nuôi đúng hướng Dụng thần hay đang nuôi phần kỵ? Phần giải thích này "
            "phải rõ ràng, không dùng thuật ngữ kích hoạt luật."
        ),
        "version": "1.0.0",
        "review_status": "awaiting_review",
        "author": "BTE Knowledge Author",
        "author_notes": "Requires useful_god present; binds {useful_god_label} from Analysis/Interpretation.",
        "reviewers": "",
        "wave_id": "W-P0-1.1-CORE",
    },
    {
        "knowledge_unit_id": "KU-RC-001",
        "title": "Core Recommendation",
        "summary": "Khuyến nghị cốt lõi: một ưu tiên và một hành động tiếp theo bám Dụng thần.",
        "purpose": "Tạo Recommendation và ô priority/next_action đủ cụ thể cho Result mặc định.",
        "kind": "Action",
        "domain": "CK-DM",
        "scenarios": "CS-MD;CS-CA;CS-LT;default",
        "primary_intent": "Chọn việc cần làm ngay theo Dụng thần",
        "secondary_intent": "Hỗ trợ kết luận và giảm tải khi có weakness",
        "condition": "analysis.has_useful_god = true",
        "evidence_kind": "action",
        "required_evidence": "identity;explanation",
        "required_interpretation": "useful_god;summary",
        "narrative_targets": "recommendation;executive_summary;conclusion",
        "consultation_goals": "set_priority_and_next_action",
        "decision_posture": "prepare",
        "action_category": "useful_god_priority",
        "risk_category": "",
        "opportunity_category": "",
        "primary_usage": "Recommendation;Executive Summary",
        "secondary_usage": "Portal;Report;AI Assistant;Search;Mobile;Future APIs",
        "priority": "100",
        "confidence": "0.90",
        "confidence_requirement": "0.65",
        "commercial_value": "C",
        "ethics_flags": "no_guaranteed_returns",
        "signal_refs": "useful_god;priority_counsel",
        "ref_ids": "REF-000006;REF-000007",
        "paired_unit_ids": "KU-UG-001",
        "classical_text": "Thuận dụng thần mà hành; trước hết giữ mực rồi mới mở (diễn giải hiện đại).",
        "modern_interpretation": (
            "Hành động: Ưu tiên các việc nuôi Dụng thần {useful_god_label} trong 2–4 tuần tới; "
            "tạm xếp sau những việc làm lệch hướng này. Lý do: đây là trục ưu tiên đã xác lập từ "
            "phân tích Dụng thần — làm đúng trục sẽ giữ nhịp bền hơn là chạy nhiều hướng. "
            "Bước tiếp theo: chọn một việc cụ thể trong tuần này gắn trực tiếp với {useful_god_label} "
            "và một việc cần trì hoãn. Nếu lá số đang có điểm yếu cấu trúc, hãy bắt đầu bằng giảm tải "
            "trước khi mở rộng."
        ),
        "version": "1.0.0",
        "review_status": "awaiting_review",
        "author": "BTE Knowledge Author",
        "author_notes": (
            "Commercial shape: Action / Reason / Next step. Posture prepare is safe default; "
            "Advance only when Opportunity evidence exists in later waves."
        ),
        "reviewers": "",
        "wave_id": "W-P0-1.1-CORE",
    },
]


def main() -> None:
    """Write exactly five Wave 1.1 Knowledge Units."""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        assert len(ROWS) == 5
        for row in ROWS:
            writer.writerow(row)
    print(f"wrote {OUT} rows={len(ROWS)}")


if __name__ == "__main__":
    main()
