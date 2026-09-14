"""Stage 1 Bazi analysis result contract.

This adapter is presentation/data-contract glue only. It does not recalculate
the chart and does not call any engine.
"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Mapping

CONTRACT_VERSION = "bazi_analysis_result.v1"

CUSTOMER_SAFE_BLOCKED_KEYS = {
    "candidate_list",
    "catalog_id",
    "climate_candidate_list",
    "contract",
    "evidence_refs",
    "generator",
    "matched_rules",
    "metadata",
    "overall_candidate_list",
    "runtime_ms",
    "schema_version",
    "source_path",
    "traceability",
    "validation_issues",
    "winning_rule_group",
    "winning_rule_id",
}

LIFE_DOMAIN_KEYS = (
    "health",
    "wealth",
    "career",
    "marriage",
    "children",
    "parents",
    "siblings",
    "ancestry",
    "property",
)

TECHNICAL_EXPLANATION_KEYS = (
    "day_master",
    "strength",
    "structure",
    "useful_god",
    "five_elements",
    "ten_gods",
    "shen_sha",
)

MODULE_EXPORT_KEYS = (
    "marriage_seed",
    "career_seed",
    "partnership_seed",
    "feng_shui_seed",
    "child_planning_seed",
)

REPORT_CHAPTER_KEYS = (
    "overview",
    "four_pillars",
    "day_master",
    "five_elements",
    "strength_structure_useful_god",
    "ten_gods",
    "shen_sha",
    "life_domains",
    "luck_cycles",
    "recommendations",
)

PILLAR_LABELS = {
    "year": "Năm",
    "month": "Tháng",
    "day": "Ngày",
    "hour": "Giờ",
}

PILLAR_LIFE_HINTS = {
    "year": "Gốc gia tộc, môi trường sớm, nền phúc khí.",
    "month": "Cha mẹ, nghề nghiệp, nhịp vận hành chính của mệnh.",
    "day": "Bản thân, phối ngẫu, cách đi vào quan hệ gần.",
    "hour": "Con cái, hậu vận, dự án dài hạn.",
}

LIFE_DOMAIN_TITLES = {
    "health": "Sức khỏe",
    "wealth": "Mệnh/Tài vận",
    "career": "Quan vận/Nghề nghiệp",
    "marriage": "Nhân duyên/Hôn nhân",
    "children": "Con cái",
    "parents": "Bố mẹ",
    "siblings": "Anh em",
    "ancestry": "Tổ tiên",
    "property": "Điền trạch",
}

_DOMAIN_RECOMMENDATIONS = {
    "health": "Ưu tiên nếp sống điều độ, ngủ nghỉ ổn định và quan sát các thời điểm ngũ hành mất cân bằng rõ.",
    "wealth": "Tài vận nên đi cùng kỷ luật dòng tiền, tránh quyết định lớn khi cảm xúc hoặc áp lực vận hạn đang chi phối.",
    "career": "Nghề nghiệp nên chọn môi trường giúp điểm mạnh của Mệnh cục được dùng đúng chỗ, đồng thời có khuôn khổ để tránh phân tán.",
    "marriage": "Quan hệ thân mật cần được đọc chậm, ưu tiên cách giao tiếp ổn định và khả năng cùng xây nhịp sống thực tế.",
    "children": "Việc sinh con hoặc nuôi dạy con nên xét thêm vận hạn từng giai đoạn, không chỉ nhìn một tín hiệu riêng lẻ trong lá số gốc.",
    "parents": "Quan hệ với cha mẹ nên được nhìn như nền nâng đỡ và bài học gốc, tránh diễn giải một chiều thành tốt hoặc xấu tuyệt đối.",
    "siblings": "Quan hệ anh em/bạn đồng hành nên chú trọng ranh giới, vai trò và cách chia sẻ nguồn lực.",
    "ancestry": "Phần tổ tiên/gốc phúc nên được dùng như nền văn hóa gia đình để hiểu mình, không nên quy hết thành định mệnh.",
    "property": "Điền trạch/phong thủy nên ưu tiên sự ổn định, sạch thoáng và các yếu tố bổ trợ đúng Dụng thần thay vì chạy theo mẹo rời rạc.",
}

_DOMAIN_SOURCE_REFS = {
    "health": ["five_elements", "temperature"],
    "wealth": ["useful_god", "wealth_profile"],
    "career": ["pattern", "career_profile"],
    "marriage": ["bazi.day_pillar", "ten_gods.four_layer.day", "shen_sha.relationship"],
    "children": ["bazi.hour_pillar", "ten_gods.four_layer.hour", "luck"],
    "parents": ["bazi.month_pillar", "ten_gods.four_layer.month"],
    "siblings": ["bazi.month_pillar", "ten_gods.four_layer.month"],
    "ancestry": ["bazi.year_pillar", "ten_gods.four_layer.year"],
    "property": ["calendar.cung_phi", "five_elements", "useful_god"],
}

_DOMAIN_ALIASES = {
    "health": ("health", "sức khỏe", "suc khoe"),
    "wealth": ("wealth", "tài", "tài vận", "tai van", "money", "finance"),
    "career": ("career", "nghề", "quan vận", "nghe nghiep", "sự nghiệp", "su nghiep"),
    "marriage": ("marriage", "hôn nhân", "hon nhan", "nhân duyên", "nhan duyen", "spouse"),
    "children": ("children", "con cái", "con cai", "tử tức", "tu tuc"),
    "parents": ("parents", "bố mẹ", "bo me", "cha mẹ", "cha me"),
    "siblings": ("siblings", "anh em", "huynh đệ", "huynh de"),
    "ancestry": ("ancestry", "tổ tiên", "to tien", "phúc đức", "phuc duc"),
    "property": ("property", "điền trạch", "dien trach", "nhà đất", "nha dat"),
}

_SHEN_SHA_GROUPS = {
    "noble_support": {
        "title": "Quý nhân/phúc tinh",
        "keywords": ("Quý Nhân", "Thiên Ất", "Thiên Đức", "Nguyệt Đức", "Phúc", "Giải Thần"),
    },
    "relationship": {
        "title": "Đào hoa/nhân duyên",
        "keywords": ("Đào Hoa", "Hồng Loan", "Thiên Hỷ", "Hàm Trì"),
    },
    "authority": {
        "title": "Quyền tinh/tài danh",
        "keywords": ("Tướng Tinh", "Lộc Thần", "Quốc Ấn", "Văn Xương", "Kim Dư"),
    },
    "caution": {
        "title": "Cảnh báo/gia đạo",
        "keywords": ("Dương Nhận", "Kiếp Sát", "Tai Sát", "Cô Thần", "Quả Tú", "Tang Môn", "Bạch Hổ"),
    },
    "later_life": {
        "title": "Hậu vận/dịch chuyển",
        "keywords": ("Dịch Mã", "Hoa Cái", "Thiên La", "Địa Võng"),
    },
}


def build_bazi_analysis_result(
    payload: dict[str, Any],
    *,
    input_payload: dict[str, Any] | None = None,
    analysis_id: str | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Build ``bazi_analysis_result.v1`` from the legacy Analyze payload."""
    envelope: dict[str, Any] = {
        "contract": CONTRACT_VERSION,
        "analysis_id": _text(analysis_id) or _text(payload.get("analysis_id")),
        "subject": build_subject(payload, input_payload),
        "technical_data": build_technical_data(payload),
        "presentation_data": build_presentation_data(payload),
        "customer_narrative": build_customer_narrative(payload),
        "module_exports": build_module_exports(payload),
        "meta": build_meta(payload, analysis_id=analysis_id, request_id=request_id),
    }
    envelope["quality"] = build_quality(payload, envelope)
    return envelope


def build_subject(payload: Mapping[str, Any], input_payload: Mapping[str, Any] | None) -> dict[str, Any]:
    """Build customer/chart identity without feeding it back into engines."""
    identity = _mapping(payload.get("identity"))
    person = _mapping(identity.get("person"))
    customer = _mapping(payload.get("customer"))
    calendar = _mapping(payload.get("calendar"))
    input_data = _mapping(input_payload)
    birth_time = _first_text(
        person.get("birth_time"),
        _format_birth_time(input_data.get("hour"), input_data.get("minute")),
        _format_birth_time(calendar.get("solar_hour"), calendar.get("solar_minute")),
    )
    return {
        "full_name": _first_text(person.get("full_name"), customer.get("full_name"), input_data.get("full_name")),
        "gender": _first_text(person.get("gender"), customer.get("gender"), input_data.get("gender")),
        "gender_label": _first_text(person.get("gender_label"), customer.get("gender_label")),
        "birth_place": _first_text(person.get("birth_place"), customer.get("birth_place"), input_data.get("birth_place")),
        "timezone": _first_text(
            person.get("timezone"),
            customer.get("timezone"),
            input_data.get("timezone"),
            calendar.get("timezone_name"),
            calendar.get("timezone"),
        ),
        "solar_birth": _first_text(person.get("solar_birth"), calendar.get("solar_date")),
        "lunar_birth": _first_text(person.get("lunar_birth"), calendar.get("lunar_date")),
        "birth_time": birth_time,
        "customer_id": _first_text(person.get("customer_id"), customer.get("customer_id"), input_data.get("customer_id")),
    }


def build_technical_data(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Keep technical analysis rich, but grouped by topic."""
    bazi = _mapping(payload.get("bazi"))
    identity = _mapping(payload.get("identity"))
    ten_gods = _copy_mapping(payload.get("ten_gods"))
    ten_gods["four_layer"] = build_ten_gods_four_layer_view(payload)
    return {
        "calendar": _copy_mapping(payload.get("calendar")),
        "four_pillars": {
            "bazi": {
                "year": _copy_mapping_or_value(bazi.get("year_pillar")),
                "month": _copy_mapping_or_value(bazi.get("month_pillar")),
                "day": _copy_mapping_or_value(bazi.get("day_pillar")),
                "hour": _copy_mapping_or_value(bazi.get("hour_pillar")),
            },
            "identity": _copy_mapping_or_value(identity.get("four_pillars")),
            "hidden_stems": deepcopy(bazi.get("hidden_stems")),
        },
        "day_master": {
            "stem": _text(bazi.get("day_master")),
            "element": _text(bazi.get("day_master_element")),
            "yin_yang": _text(bazi.get("day_master_yin_yang")),
        },
        "five_elements": _copy_mapping(payload.get("five_elements")),
        "strength": _copy_mapping(payload.get("strength")),
        "structure": _copy_mapping(payload.get("pattern")),
        "temperature": _copy_mapping(payload.get("temperature")),
        "useful_god": _copy_mapping(payload.get("useful_god")),
        "ten_gods": ten_gods,
        "shen_sha": {
            "shen_sha": deepcopy(bazi.get("shen_sha")),
            "shensha": deepcopy(bazi.get("shensha")),
            "matches": deepcopy(bazi.get("shensha_matches")),
            "grouped": build_shen_sha_grouped_view(payload),
        },
        "bone_weight": _copy_mapping(payload.get("can_xuong")),
        "luck": _copy_mapping(payload.get("luck")),
        "mingju": {
            "achievement": _copy_mapping_or_value(payload.get("achievement")),
            "wealth_profile": _copy_mapping_or_value(payload.get("wealth_profile")),
            "career_profile": _copy_mapping_or_value(payload.get("career_profile")),
            "integrity": _copy_mapping_or_value(payload.get("integrity")),
            "damage_ids": deepcopy(payload.get("damage_ids")),
            "rescue_ids": deepcopy(payload.get("rescue_ids")),
        },
    }


def build_presentation_data(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Build a small customer-safe projection for future UI/PDF surfaces."""
    bazi = _mapping(payload.get("bazi"))
    strength = _mapping(payload.get("strength"))
    pattern = _mapping(payload.get("pattern"))
    useful_god = _mapping(payload.get("useful_god"))
    five_elements = _mapping(payload.get("five_elements"))
    primary_tags = _non_empty(
        [
            _join_label_value(_text(bazi.get("day_master")), _text(bazi.get("day_master_element"))),
            _first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")),
            _first_text(pattern.get("cach_cuc"), pattern.get("pattern")),
            _first_text(useful_god.get("useful_display"), useful_god.get("useful_element"), useful_god.get("useful_stem")),
        ]
    )
    summary_cards = _non_empty_cards(
        [
            {"label": "Nhật chủ", "value": primary_tags[0] if primary_tags else ""},
            {"label": "Thân", "value": _first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc"))},
            {"label": "Mệnh cục", "value": _first_text(pattern.get("cach_cuc"), pattern.get("pattern"))},
            {"label": "Dụng thần", "value": _first_text(useful_god.get("useful_display"), useful_god.get("useful_stem"))},
        ]
    )
    projection = {
        "hero": {
            "title": "Kết quả luận giải Bát Tự",
            "subtitle": "Bức tranh nền mệnh và định hướng đời sống",
            "primary_tags": primary_tags,
        },
        "summary_cards": summary_cards,
        "pillar_table": _build_pillar_table(bazi),
        "five_element_chart": {
            "counts": deepcopy(five_elements.get("counts")),
            "dominant": deepcopy(five_elements.get("dominant")),
            "missing": deepcopy(five_elements.get("missing")),
            "unit_total": five_elements.get("unit_total"),
            "method_note": _text(five_elements.get("method_note")),
        },
        "section_index": [
            {"id": "four_pillars", "title": "Tứ trụ"},
            {"id": "five_elements", "title": "Ngũ hành"},
            {"id": "strength", "title": "Thân vượng/nhược"},
            {"id": "structure", "title": "Mệnh cục và Dụng thần"},
            {"id": "ten_gods", "title": "Thập thần"},
            {"id": "shen_sha", "title": "Thần sát"},
            {"id": "life_domains", "title": "9 mục đời sống"},
            {"id": "luck", "title": "Đại vận"},
        ],
    }
    return _customer_safe(projection)


def build_customer_narrative(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Publish the safest available narrative source under one stable shape."""
    v2 = _mapping(payload.get("narrative_v2_shadow"))
    presentation = _mapping(v2.get("presentation"))
    if v2.get("status") == "ok" and presentation:
        return _customer_safe(
            _normalize_customer_narrative(
                {
                    "provider": "narrative_v2_shadow",
                    "version": "stage_2",
                    "overview": _first_mapping(presentation.get("summary"), presentation.get("overview"), presentation),
                    "technical_explanations": _mapping(presentation.get("technical_explanations")),
                    "life_domains": _first_mapping(presentation.get("life_domains"), presentation.get("domains")),
                    "luck_cycles": _first_mapping(presentation.get("luck_cycles"), presentation.get("luck")),
                    "recommendations": _list(presentation.get("recommendations")),
                },
                payload,
            )
        )

    detailed = _mapping(payload.get("detailed_narrative"))
    if detailed:
        return _customer_safe(
            _normalize_customer_narrative(
                {
                    "provider": "detailed_narrative",
                    "version": "stage_2",
                    "overview": _first_mapping(detailed.get("executive"), detailed.get("summary")),
                    "technical_explanations": _mapping(detailed.get("labels")),
                    "life_domains": _mapping(detailed.get("domains")),
                    "luck_cycles": _mapping(detailed.get("luck")),
                    "recommendations": _list(detailed.get("actions")),
                },
                payload,
            )
        )

    integrated = _mapping(payload.get("integrated_narrative"))
    if integrated:
        return _customer_safe(
            _normalize_customer_narrative(
                {
                    "provider": "integrated_narrative",
                    "version": "stage_2",
                    "overview": {
                        "summary": integrated.get("summary"),
                        "observation": integrated.get("observation"),
                        "impact": integrated.get("impact"),
                    },
                    "technical_explanations": _mapping(integrated.get("reasoning")),
                    "life_domains": {},
                    "luck_cycles": {},
                    "recommendations": _list_or_single(integrated.get("recommendation")),
                },
                payload,
            )
        )

    narrative_result = _mapping(payload.get("narrative_result"))
    if narrative_result:
        return _customer_safe(
            _normalize_customer_narrative(
                {
                    "provider": "narrative_result",
                    "version": "stage_2",
                    "overview": _first_mapping(
                        narrative_result.get("commercial_executive_summary"),
                        narrative_result.get("summary"),
                    ),
                    "technical_explanations": {},
                    "life_domains": _mapping(narrative_result.get("sections")),
                    "luck_cycles": {},
                    "recommendations": _list(narrative_result.get("recommendations")),
                },
                payload,
            )
        )

    commercial = _mapping(payload.get("commercial_consulting"))
    return _customer_safe(
        _normalize_customer_narrative(
            {
                "provider": "commercial_consulting" if commercial else "none",
                "version": "stage_2",
                "overview": {},
                "technical_explanations": {},
                "life_domains": _mapping(commercial.get("sections")),
                "luck_cycles": {},
                "recommendations": [],
            },
            payload,
        )
    )


def build_module_exports(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Provide draft seeds so future modules do not read raw payload ad hoc."""
    bazi = _mapping(payload.get("bazi"))
    calendar = _mapping(payload.get("calendar"))
    five_elements = _mapping(payload.get("five_elements"))
    pattern = _mapping(payload.get("pattern"))
    strength = _mapping(payload.get("strength"))
    useful_god = _mapping(payload.get("useful_god"))
    luck = _mapping(payload.get("luck"))
    ten_gods_four_layer = build_ten_gods_four_layer_view(payload)
    shen_sha_grouped = build_shen_sha_grouped_view(payload)
    return {
        "marriage_seed": _module_seed(
            ["technical_data.day_master", "technical_data.ten_gods.four_layer", "technical_data.shen_sha.grouped"],
            {
                "day_master": _day_master_identity(bazi),
                "spouse_pillar": _mapping(bazi.get("day_pillar")),
                "ten_gods_four_layer": ten_gods_four_layer,
                "relationship_shen_sha": _mapping(_mapping(shen_sha_grouped.get("groups")).get("relationship")),
            },
            ["day_master.stem", "spouse_pillar", "ten_gods_four_layer"],
        ),
        "career_seed": _module_seed(
            ["technical_data.structure", "technical_data.useful_god", "technical_data.strength", "technical_data.mingju.career_profile"],
            {
                "day_master": _day_master_identity(bazi),
                "strength_level": _first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")),
                "structure": _first_text(pattern.get("cach_cuc"), pattern.get("pattern")),
                "useful_god": _useful_god_identity(useful_god),
                "career_profile": _copy_mapping_or_value(payload.get("career_profile")),
            },
            ["day_master.stem", "structure", "useful_god"],
        ),
        "partnership_seed": _module_seed(
            ["technical_data.day_master", "technical_data.ten_gods.four_layer", "technical_data.useful_god"],
            {
                "day_master": _day_master_identity(bazi),
                "ten_gods_four_layer": ten_gods_four_layer,
                "useful_god": _useful_god_identity(useful_god),
                "authority_or_resource_signals": _ten_god_signal_labels(
                    ten_gods_four_layer,
                    ("Chính Quan", "Thất Sát", "Chính Ấn", "Thiên Ấn"),
                ),
            },
            ["day_master.stem", "ten_gods_four_layer", "useful_god"],
        ),
        "feng_shui_seed": _module_seed(
            ["technical_data.calendar", "technical_data.five_elements", "technical_data.useful_god"],
            {
                "cung_phi": _first_text(calendar.get("cung_phi"), calendar.get("menh_quai")),
                "house_group": _first_text(calendar.get("nhom_trach"), calendar.get("house_group")),
                "five_elements": {
                    "dominant": deepcopy(five_elements.get("dominant")),
                    "missing": deepcopy(five_elements.get("missing")),
                },
                "useful_god": _useful_god_identity(useful_god),
            },
            ["cung_phi", "five_elements", "useful_god"],
        ),
        "child_planning_seed": _module_seed(
            ["technical_data.four_pillars.bazi.hour", "technical_data.luck", "technical_data.ten_gods.four_layer"],
            {
                "hour_pillar": _mapping(bazi.get("hour_pillar")),
                "hour_layer": _pillar_layer(ten_gods_four_layer, "hour"),
                "luck_current_cycle": _mapping(luck.get("current_cycle")),
                "luck_cycles": _list(luck.get("cycles")),
            },
            ["hour_pillar", "hour_layer", "luck_cycles"],
        ),
    }


def build_quality(payload: Mapping[str, Any], envelope: Mapping[str, Any]) -> dict[str, Any]:
    """Compute readiness flags for the contract without blocking legacy output."""
    technical = _mapping(envelope.get("technical_data"))
    narrative = _mapping(envelope.get("customer_narrative"))
    presentation = _mapping(envelope.get("presentation_data"))
    module_exports = _mapping(envelope.get("module_exports"))
    day_master = _mapping(technical.get("day_master"))
    life_domains = _mapping(narrative.get("life_domains"))
    missing_sections = [
        key
        for key in LIFE_DOMAIN_KEYS
        if key not in life_domains or _mapping(life_domains.get(key)).get("status") == "missing"
    ]
    technical_explanations = _mapping(narrative.get("technical_explanations"))
    missing_technical_explanations = [
        key
        for key in TECHNICAL_EXPLANATION_KEYS
        if key not in technical_explanations or _mapping(technical_explanations.get(key)).get("status") == "missing"
    ]
    missing_module_exports = [
        key
        for key in MODULE_EXPORT_KEYS
        if key not in module_exports or _mapping(module_exports.get(key)).get("missing_fields")
    ]
    report_chapters = _list(narrative.get("report_chapters"))
    report_chapter_ids = {
        _text(item.get("id"))
        for item in report_chapters
        if isinstance(item, Mapping)
    }
    missing_report_chapters = [
        key
        for key in REPORT_CHAPTER_KEYS
        if key not in report_chapter_ids
    ]
    report_document = _mapping(narrative.get("report_document"))
    report_markdown = _text(report_document.get("markdown"))
    customer_safe = _is_customer_safe(
        {
            "presentation_data": presentation,
            "customer_narrative": narrative,
            "module_exports": module_exports,
        }
    )
    flags = {
        "has_day_master": bool(day_master.get("stem")),
        "has_four_pillars": bool(_mapping(technical.get("four_pillars")).get("bazi")),
        "has_five_elements": bool(technical.get("five_elements")),
        "has_strength": bool(technical.get("strength")),
        "has_structure": bool(technical.get("structure")),
        "has_useful_god": bool(technical.get("useful_god")),
        "has_luck": bool(technical.get("luck")),
        "has_customer_narrative": bool(narrative.get("provider") and narrative.get("provider") != "none"),
        "has_life_domains": not missing_sections,
        "has_ten_gods_four_layer": bool(_mapping(technical.get("ten_gods")).get("four_layer")),
        "has_shen_sha_grouped": bool(_mapping(_mapping(technical.get("shen_sha")).get("grouped")).get("groups")),
        "has_technical_explanations": not missing_technical_explanations,
        "has_module_exports": not missing_module_exports,
        "has_complete_report_chapters": not missing_report_chapters,
        "has_report_document": bool(report_markdown and not missing_report_chapters),
    }
    required_complete = all(
        flags[key]
        for key in (
            "has_day_master",
            "has_four_pillars",
            "has_five_elements",
            "has_strength",
            "has_structure",
            "has_useful_god",
        )
    )
    warnings: list[str] = []
    if not flags["has_customer_narrative"]:
        warnings.append("customer_narrative_missing")
    if missing_sections:
        warnings.append("life_domains_incomplete")
    if missing_technical_explanations:
        warnings.append("technical_explanations_incomplete")
    if missing_module_exports:
        warnings.append("module_exports_incomplete")
    if missing_report_chapters:
        warnings.append("report_chapters_incomplete")
    if not flags["has_report_document"]:
        warnings.append("report_document_missing")
    return {
        "data_complete": bool(required_complete and customer_safe),
        "customer_safe": customer_safe,
        **flags,
        "missing_sections": missing_sections,
        "missing_technical_explanations": missing_technical_explanations,
        "missing_module_exports": missing_module_exports,
        "missing_report_chapters": missing_report_chapters,
        "warnings": warnings,
    }


def build_meta(
    payload: Mapping[str, Any],
    *,
    analysis_id: str | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Collect provenance and runtime metadata away from customer prose."""
    result_meta = _mapping(payload.get("result_meta"))
    source_keys = [key for key in payload.keys() if key.endswith("_source")]
    return {
        "analysis_id": _first_text(analysis_id, payload.get("analysis_id"), result_meta.get("analysis_id")),
        "request_id": _first_text(request_id, payload.get("request_id")),
        "chart_id": _text(payload.get("chart_id")),
        "contract_version": CONTRACT_VERSION,
        "created_at": _first_text(result_meta.get("created_at"), datetime.now(timezone.utc).isoformat()),
        "provenance": {key: _copy_mapping_or_value(payload.get(key)) for key in sorted(source_keys)},
        "runtime": {
            "pipeline": deepcopy(payload.get("pipeline")),
            "stage": payload.get("stage"),
            "legacy_customer_contract": result_meta.get("customer_contract"),
        },
    }


def build_ten_gods_four_layer_view(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Project Ten Gods into year/month/day/hour layers for later commentary."""
    bazi = _mapping(payload.get("bazi"))
    ten_gods = _mapping(payload.get("ten_gods"))
    visible = [item for item in _list(ten_gods.get("visible")) if isinstance(item, Mapping)]
    hidden = [item for item in _list(ten_gods.get("hidden")) if isinstance(item, Mapping)]
    layers: list[dict[str, Any]] = []
    for key, label in PILLAR_LABELS.items():
        pillar = _mapping(bazi.get(f"{key}_pillar"))
        visible_items = [_ten_god_occurrence(item) for item in visible if _text(item.get("pillar")) == key]
        hidden_items = [_ten_god_occurrence(item) for item in hidden if _text(item.get("pillar")) == key]
        primary = _first_text(
            pillar.get("ten_god"),
            *(item.get("ten_god") for item in visible_items if isinstance(item, Mapping)),
        )
        layers.append(
            {
                "pillar": key,
                "label": label,
                "can_chi": _first_text(pillar.get("can_chi"), pillar.get("name")),
                "stem": _text(pillar.get("stem")),
                "branch": _text(pillar.get("branch")),
                "primary_ten_god": primary,
                "visible": visible_items,
                "hidden": hidden_items,
                "life_hint": PILLAR_LIFE_HINTS[key],
            }
        )
    return {
        "status": "ready" if any(layer["primary_ten_god"] or layer["visible"] or layer["hidden"] for layer in layers) else "missing",
        "layers": layers,
        "note": _text(ten_gods.get("note")),
    }


def build_shen_sha_grouped_view(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Group ShenSha for customer-facing chapters without adding new astrology facts."""
    items = _collect_shen_sha_items(payload)
    groups = {
        key: {"title": spec["title"], "items": []}
        for key, spec in _SHEN_SHA_GROUPS.items()
    }
    groups["other"] = {"title": "Khác", "items": []}
    for item in items:
        name = _first_text(item.get("name"), item.get("canonical_name"))
        group_key = _shen_sha_group_key(name)
        groups[group_key]["items"].append(item)
    return {
        "status": "ready" if items else "missing",
        "groups": groups,
        "summary": [
            {"group": key, "title": value["title"], "count": len(value["items"])}
            for key, value in groups.items()
            if value["items"]
        ],
    }


def build_life_domain_sections(
    payload: Mapping[str, Any],
    existing_domains: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize the nine DOCX life domains into a stable customer shape."""
    sections = {
        key: {
            "title": LIFE_DOMAIN_TITLES[key],
            "status": "missing",
            "summary": "",
            "source_refs": [],
        }
        for key in LIFE_DOMAIN_KEYS
    }
    _merge_life_domain_source(sections, existing_domains, "customer_narrative.life_domains")
    detailed = _mapping(payload.get("detailed_narrative"))
    _merge_life_domain_source(sections, _mapping(detailed.get("domains")), "detailed_narrative.domains")
    _merge_life_domain_source(sections, payload.get("domains"), "domains")
    commercial = _mapping(payload.get("commercial_consulting"))
    _merge_life_domain_source(sections, commercial.get("sections"), "commercial_consulting.sections")
    for key, section in sections.items():
        if section["status"] == "missing":
            fallback = _fallback_life_domain_summary(key, payload)
            if fallback:
                section["status"] = "draft"
                section["summary"] = fallback
                section["source_refs"] = _DOMAIN_SOURCE_REFS.get(key, [])
        _enrich_life_domain_section(key, section, payload)
    return sections


def build_luck_cycle_narrative(
    payload: Mapping[str, Any],
    existing_luck: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Create factual luck-cycle narrative seeds from the existing luck payload."""
    luck = _mapping(payload.get("luck"))
    cycles = [item for item in _list(luck.get("cycles")) if isinstance(item, Mapping)]
    projected_cycles = [_project_luck_cycle(item) for item in cycles]
    current = _mapping(luck.get("current_cycle"))
    return {
        "status": "draft" if projected_cycles or current else "missing",
        "source_refs": ["luck.current_cycle", "luck.cycles"],
        "direction": _text(luck.get("direction")),
        "direction_label": _text(luck.get("direction_label")),
        "start_age": luck.get("start_age"),
        "current_cycle": _project_luck_cycle(current) if current else _mapping(existing_luck),
        "cycles": projected_cycles,
        "method_note": _text(luck.get("method_note")),
        "precision": _text(luck.get("precision")),
    }


def _normalize_customer_narrative(base: dict[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    base = dict(base)
    base["technical_explanations"] = build_technical_explanation_sections(
        payload,
        _mapping(base.get("technical_explanations")),
    )
    base["life_domains"] = build_life_domain_sections(payload, _mapping(base.get("life_domains")))
    base["luck_cycles"] = build_luck_cycle_narrative(payload, _mapping(base.get("luck_cycles")))
    base["report_chapters"] = build_report_chapters(payload, base)
    base["report_document"] = build_report_document(payload, base)
    return base


def build_report_document(payload: Mapping[str, Any], narrative: Mapping[str, Any]) -> dict[str, Any]:
    """Render report chapters into a customer-readable markdown document."""
    subject = build_subject(payload, None)
    chapters = [item for item in _list(narrative.get("report_chapters")) if isinstance(item, Mapping)]
    title = "Bản luận giải lá số Bát Tự"
    subject_name = _text(subject.get("full_name"))
    subtitle_parts = _non_empty(
        [
            subject_name,
            _text(subject.get("gender_label")),
            _text(subject.get("solar_birth")),
            _text(subject.get("birth_time")),
            _text(subject.get("birth_place")),
        ]
    )
    subtitle = " · ".join(subtitle_parts)
    markdown = _render_report_markdown(title, subtitle, chapters)
    return {
        "format": "markdown",
        "title": title,
        "subtitle": subtitle,
        "status": "draft" if markdown else "missing",
        "chapter_count": len(chapters),
        "markdown": markdown,
    }


def build_report_chapters(payload: Mapping[str, Any], narrative: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Build ordered customer-safe chapters for a complete Bazi reading draft."""
    technical = _mapping(narrative.get("technical_explanations"))
    life_domains = _mapping(narrative.get("life_domains"))
    luck_cycles = _mapping(narrative.get("luck_cycles"))
    recommendations = _list(narrative.get("recommendations"))
    return [
        _chapter("overview", "Tổng quan lá số", _overview_paragraphs(payload, narrative), ["overview", "bazi", "pattern", "useful_god"]),
        _chapter("four_pillars", "Tứ trụ", _four_pillars_paragraphs(payload), ["bazi.year_pillar", "bazi.month_pillar", "bazi.day_pillar", "bazi.hour_pillar"]),
        _chapter("day_master", "Nhật chủ", [_section_summary(technical, "day_master")], ["bazi.day_master"]),
        _chapter("five_elements", "Ngũ hành", [_section_summary(technical, "five_elements")], ["five_elements"]),
        _chapter(
            "strength_structure_useful_god",
            "Thân vượng, Mệnh cục và Dụng thần",
            [
                _section_summary(technical, "strength"),
                _section_summary(technical, "structure"),
                _section_summary(technical, "useful_god"),
            ],
            ["strength", "pattern", "useful_god"],
        ),
        _chapter("ten_gods", "Thập thần", [_section_summary(technical, "ten_gods")], ["ten_gods.four_layer"]),
        _chapter("shen_sha", "Thần sát", [_section_summary(technical, "shen_sha")], ["shen_sha.grouped"]),
        _chapter("life_domains", "9 mục đời sống", _life_domain_paragraphs(life_domains), ["customer_narrative.life_domains"]),
        _chapter("luck_cycles", "Đại vận", _luck_cycle_paragraphs(luck_cycles), ["luck.current_cycle", "luck.cycles"]),
        _chapter("recommendations", "Khuyến nghị", _recommendation_paragraphs(recommendations, payload), ["recommendations", "useful_god", "optimization"]),
    ]


def build_technical_explanation_sections(
    payload: Mapping[str, Any],
    existing_sections: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build customer-safe chapter seeds for the technical explanation block."""
    bazi = _mapping(payload.get("bazi"))
    five_elements = _mapping(payload.get("five_elements"))
    strength = _mapping(payload.get("strength"))
    pattern = _mapping(payload.get("pattern"))
    useful_god = _mapping(payload.get("useful_god"))
    ten_gods_four_layer = build_ten_gods_four_layer_view(payload)
    shen_sha_grouped = build_shen_sha_grouped_view(payload)
    existing = _mapping(existing_sections)
    sections = {
        "day_master": _technical_section(
            "Nhật chủ",
            _day_master_summary(bazi),
            ["bazi.day_master", "bazi.day_master_element"],
            existing.get("day_master"),
        ),
        "strength": _technical_section(
            "Thân vượng/nhược",
            _first_text(strength.get("customer_summary"), strength.get("evidence_compact"), strength.get("strength_level")),
            ["strength"],
            existing.get("strength"),
        ),
        "structure": _technical_section(
            "Mệnh cục",
            _first_text(pattern.get("customer_summary"), pattern.get("cach_cuc"), pattern.get("pattern")),
            ["pattern"],
            existing.get("structure"),
        ),
        "useful_god": _technical_section(
            "Dụng thần",
            _useful_god_summary(useful_god),
            ["useful_god"],
            existing.get("useful_god"),
        ),
        "five_elements": _technical_section(
            "Ngũ hành",
            _five_elements_summary(five_elements),
            ["five_elements"],
            existing.get("five_elements"),
        ),
        "ten_gods": _technical_section(
            "Thập thần",
            _ten_gods_summary(ten_gods_four_layer),
            ["ten_gods.four_layer"],
            existing.get("ten_gods"),
        ),
        "shen_sha": _technical_section(
            "Thần sát",
            _shen_sha_summary(shen_sha_grouped),
            ["bazi.shensha_matches", "bazi.shen_sha"],
            existing.get("shen_sha"),
        ),
    }
    return sections


def _ten_god_occurrence(item: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "pillar": _text(item.get("pillar")),
        "stem": _first_text(item.get("stem"), item.get("hidden_stem")),
        "branch": _text(item.get("branch")),
        "element": _text(item.get("element")),
        "ten_god": _first_text(item.get("ten_god"), item.get("label")),
        "visibility": _text(item.get("visibility")),
        "display": _text(item.get("display")),
    }


def _collect_shen_sha_items(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    bazi = _mapping(payload.get("bazi"))
    raw_items: list[Any] = []
    matches = bazi.get("shensha_matches")
    if isinstance(matches, list):
        raw_items.extend(matches)
    shen_sha = bazi.get("shen_sha")
    if isinstance(shen_sha, Mapping):
        individual = shen_sha.get("individual")
        if isinstance(individual, list):
            raw_items.extend(individual)
    names = bazi.get("shensha") or bazi.get("shensha_names")
    if isinstance(names, list):
        raw_items.extend(names)

    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_items):
        if isinstance(raw, Mapping):
            name = _first_text(raw.get("canonical_name"), raw.get("name"), raw.get("title"))
            if not name:
                continue
            item = {
                "id": _first_text(raw.get("id"), f"shen_sha_{index + 1}"),
                "name": name,
                "evidence": _first_text(raw.get("evidence_text"), raw.get("evidence")),
                "pillar": _text(raw.get("pillar")),
                "location": _text(raw.get("location")),
                "presence_label": _text(raw.get("presence_label")),
            }
        else:
            name = _text(raw)
            if not name:
                continue
            item = {"id": f"shen_sha_{index + 1}", "name": name}
        identity = f"{item.get('id')}::{item.get('name')}"
        if identity in seen:
            continue
        seen.add(identity)
        items.append(item)
    return items


def _chapter(
    chapter_id: str,
    title: str,
    paragraphs: list[str],
    source_refs: list[str],
) -> dict[str, Any]:
    clean_paragraphs = [paragraph for paragraph in (_text(item) for item in paragraphs) if paragraph]
    return {
        "id": chapter_id,
        "title": title,
        "status": "draft" if clean_paragraphs else "missing",
        "paragraphs": clean_paragraphs,
        "source_refs": source_refs,
    }


def _render_report_markdown(
    title: str,
    subtitle: str,
    chapters: list[Mapping[str, Any]],
) -> str:
    if not chapters:
        return ""
    lines = [f"# {title}"]
    if subtitle:
        lines.extend(["", subtitle])
    for chapter in chapters:
        chapter_title = _text(chapter.get("title"))
        paragraphs = _text_list(chapter.get("paragraphs"))
        if not chapter_title or not paragraphs:
            continue
        lines.extend(["", f"## {chapter_title}"])
        for paragraph in paragraphs:
            lines.extend(["", paragraph])
    return "\n".join(lines).strip()


def _overview_paragraphs(payload: Mapping[str, Any], narrative: Mapping[str, Any]) -> list[str]:
    overview = _mapping(narrative.get("overview"))
    headline = _first_text(overview.get("headline"), overview.get("summary"), overview.get("title"))
    bazi = _mapping(payload.get("bazi"))
    strength = _mapping(payload.get("strength"))
    pattern = _mapping(payload.get("pattern"))
    useful = _mapping(payload.get("useful_god"))
    tags = _non_empty(
        [
            _day_master_summary(bazi).rstrip("."),
            _first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")),
            _first_text(pattern.get("cach_cuc"), pattern.get("pattern")),
            _first_text(useful.get("useful_display"), useful.get("useful_stem"), useful.get("useful_element")),
        ]
    )
    summary = "Tổng thể lá số được đọc trên nền " + "; ".join(tags) + "." if tags else ""
    return _non_empty([headline, summary])


def _four_pillars_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    paragraphs: list[str] = _non_empty([_month_calendar_note(payload)])
    for key, label in PILLAR_LABELS.items():
        pillar = _mapping(bazi.get(f"{key}_pillar"))
        can_chi = _pillar_can_chi(pillar)
        if not can_chi:
            continue
        parts = [f"Trụ {label}: {can_chi}"]
        ten_god = _text(pillar.get("ten_god"))
        nap_am = _text(pillar.get("nap_am"))
        truong_sinh = _text(pillar.get("truong_sinh"))
        if ten_god:
            parts.append(f"thập thần {ten_god}")
        if nap_am:
            parts.append(f"nạp âm {nap_am}")
        if truong_sinh:
            parts.append(f"vòng trường sinh {truong_sinh}")
        parts.append(PILLAR_LIFE_HINTS[key].rstrip("."))
        paragraphs.append("; ".join(parts) + ".")
    return paragraphs


def _pillar_can_chi(pillar: Mapping[str, Any]) -> str:
    stem = _text(pillar.get("stem"))
    branch = _text(pillar.get("branch"))
    return _first_text(
        pillar.get("can_chi"),
        pillar.get("ganzhi"),
        pillar.get("name"),
        f"{stem} {branch}".strip(),
    )


def _month_calendar_note(payload: Mapping[str, Any]) -> str:
    calendar = _mapping(payload.get("calendar"))
    bazi = _mapping(payload.get("bazi"))
    lunar = _mapping(calendar.get("lunar"))
    lunar_can_chi = _mapping(calendar.get("lunar_can_chi"))
    bazi_can_chi = _mapping(calendar.get("bazi_can_chi"))
    month_pillar = _mapping(bazi.get("month_pillar"))
    lunar_month = _first_text(
        calendar.get("lunar_month_can_chi"),
        lunar.get("month_can_chi"),
        lunar_can_chi.get("month"),
    )
    bazi_month = _first_text(
        month_pillar.get("can_chi"),
        month_pillar.get("ganzhi"),
        bazi_can_chi.get("month"),
    )
    if not lunar_month or not bazi_month or lunar_month == bazi_month:
        return ""
    solar_term = _mapping(calendar.get("solar_term"))
    term_name = _first_text(solar_term.get("name"), calendar.get("solar_term"))
    lunar_date = _text(calendar.get("lunar_date"))
    lunar_text = f"Âm lịch {lunar_date}" if lunar_date else "Tháng âm lịch"
    term_text = f" theo tiết khí {term_name}" if term_name else " theo tiết khí"
    return (
        f"{lunar_text} thuộc tháng {lunar_month}; "
        f"trụ tháng Bát Tự đang hiển thị{term_text} là {bazi_month}. "
        "BTE ưu tiên tháng âm cho trụ tháng; tiết khí chỉ dùng làm bối cảnh luận giải."
    )


def _section_summary(sections: Mapping[str, Any], key: str) -> str:
    section = _mapping(sections.get(key))
    return _text(section.get("summary"))


def _life_domain_paragraphs(life_domains: Mapping[str, Any]) -> list[str]:
    paragraphs: list[str] = []
    for key in LIFE_DOMAIN_KEYS:
        section = _mapping(life_domains.get(key))
        title = _first_text(section.get("title"), LIFE_DOMAIN_TITLES[key])
        detailed = _text_list(section.get("paragraphs"))
        if detailed:
            paragraphs.extend(f"{title}: {item}" if index == 0 else item for index, item in enumerate(detailed))
            continue
        summary = _text(section.get("summary"))
        if summary:
            paragraphs.append(f"{title}: {summary}")
    return paragraphs


def _luck_cycle_paragraphs(luck_cycles: Mapping[str, Any]) -> list[str]:
    paragraphs: list[str] = []
    direction = _first_text(luck_cycles.get("direction_label"), luck_cycles.get("direction"))
    start_age = luck_cycles.get("start_age")
    if direction or start_age is not None:
        paragraphs.append(
            "Đại vận được đọc theo "
            + _first_text(direction, "chiều vận đã tính")
            + (f", khởi vận khoảng {start_age} tuổi." if start_age is not None else ".")
        )
    current = _mapping(luck_cycles.get("current_cycle"))
    current_summary = _text(current.get("summary"))
    if current_summary:
        paragraphs.append("Vận hiện tại: " + current_summary + ".")
    cycles = [item for item in _list(luck_cycles.get("cycles")) if isinstance(item, Mapping)]
    for item in cycles[:6]:
        age = _age_range(item)
        summary = _text(item.get("summary"))
        if summary:
            paragraphs.append((age + ": " if age else "") + summary + ".")
    return paragraphs


def _recommendation_paragraphs(recommendations: list[Any], payload: Mapping[str, Any]) -> list[str]:
    paragraphs: list[str] = []
    for item in recommendations:
        if isinstance(item, Mapping):
            text = _first_text(item.get("title"), item.get("summary"), item.get("body"), item.get("content"))
        else:
            text = _text(item)
        if text:
            paragraphs.append(text)
    if paragraphs:
        return paragraphs
    useful = _mapping(payload.get("useful_god"))
    useful_line = _useful_god_summary(useful)
    if useful_line:
        paragraphs.append("Ưu tiên hành động nên xoay quanh trục Dụng thần/Hỷ thần: " + useful_line)
    return paragraphs


def _fallback_life_domain_summary(key: str, payload: Mapping[str, Any]) -> str:
    bazi = _mapping(payload.get("bazi"))
    five_elements = _mapping(payload.get("five_elements"))
    pattern = _mapping(payload.get("pattern"))
    useful = _mapping(payload.get("useful_god"))
    calendar = _mapping(payload.get("calendar"))
    ten_layers = build_ten_gods_four_layer_view(payload)
    shen_groups = build_shen_sha_grouped_view(payload)
    if key == "health":
        return _fallback_join(
            "Sức khỏe nên đọc từ độ cân bằng ngũ hành và khí hậu lá số.",
            _five_elements_summary(five_elements),
        )
    if key == "wealth":
        return _fallback_join(
            "Tài vận nên đọc cùng Mệnh cục, Dụng thần và nhịp Đại vận.",
            _useful_god_summary(useful),
        )
    if key == "career":
        structure = _first_text(pattern.get("cach_cuc"), pattern.get("pattern"))
        return _fallback_join("Nghề nghiệp nên đặt trên trục Mệnh cục và năng lực điều phối của Nhật chủ.", structure)
    if key == "marriage":
        day = _mapping(bazi.get("day_pillar"))
        rel = _mapping(_mapping(shen_groups.get("groups")).get("relationship"))
        return _fallback_join(
            "Hôn nhân/nhân duyên lấy trụ ngày làm điểm đọc chính.",
            _pillar_brief("Trụ ngày", day),
            _group_brief(rel),
        )
    if key == "children":
        hour = _mapping(bazi.get("hour_pillar"))
        hour_layer = _pillar_layer(ten_layers, "hour")
        return _fallback_join("Con cái và hậu vận lấy trụ giờ làm điểm đọc chính.", _pillar_brief("Trụ giờ", hour), _layer_brief(hour_layer))
    if key == "parents":
        month = _mapping(bazi.get("month_pillar"))
        month_layer = _pillar_layer(ten_layers, "month")
        return _fallback_join("Bố mẹ và nền nâng đỡ đọc nhiều ở trụ tháng.", _pillar_brief("Trụ tháng", month), _layer_brief(month_layer))
    if key == "siblings":
        month_layer = _pillar_layer(ten_layers, "month")
        return _fallback_join("Anh em/bạn đồng hành đọc qua trụ tháng và các tín hiệu đồng hành trong Thập thần.", _layer_brief(month_layer))
    if key == "ancestry":
        year = _mapping(bazi.get("year_pillar"))
        year_layer = _pillar_layer(ten_layers, "year")
        return _fallback_join("Tổ tiên/gốc phúc đọc từ trụ năm và nền khí ban đầu.", _pillar_brief("Trụ năm", year), _layer_brief(year_layer))
    if key == "property":
        return _fallback_join(
            "Điền trạch/phong thủy nền đọc cùng Cung Phi, nhóm trạch và ngũ hành cần bổ trợ.",
            _first_text(calendar.get("cung_phi"), calendar.get("menh_quai")),
            _first_text(calendar.get("nhom_trach"), calendar.get("house_group")),
            _useful_god_summary(useful),
        )
    return ""


def _enrich_life_domain_section(
    key: str,
    section: dict[str, Any],
    payload: Mapping[str, Any],
) -> None:
    summary = _text(section.get("summary"))
    paragraphs = _life_domain_detail_paragraphs(key, payload, summary)
    if paragraphs:
        section["paragraphs"] = paragraphs
    recommendation = _DOMAIN_RECOMMENDATIONS.get(key, "")
    if recommendation:
        section["recommendations"] = [recommendation]
    if section.get("status") != "missing" and not section.get("source_refs"):
        section["source_refs"] = _DOMAIN_SOURCE_REFS.get(key, [])


def _life_domain_detail_paragraphs(
    key: str,
    payload: Mapping[str, Any],
    summary: str,
) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    useful = _mapping(payload.get("useful_god"))
    pattern = _mapping(payload.get("pattern"))
    strength = _mapping(payload.get("strength"))
    five_elements = _mapping(payload.get("five_elements"))
    calendar = _mapping(payload.get("calendar"))
    ten_layers = build_ten_gods_four_layer_view(payload)
    shen_groups = build_shen_sha_grouped_view(payload)
    paragraphs = _non_empty([summary])

    if key == "health":
        paragraphs.append(
            _fallback_join(
                "Khi đọc sức khỏe, trọng tâm là sự điều hòa khí chất hơn là dự đoán bệnh tật.",
                _five_elements_summary(five_elements),
                _first_text(_mapping(payload.get("temperature")).get("climate_state_label"), _mapping(payload.get("temperature")).get("temperature_level")),
            )
        )
    elif key == "wealth":
        paragraphs.append(
            _fallback_join(
                "Tài vận của lá số nên được xét cùng Dụng thần và khả năng giữ nhịp ổn định qua từng đại vận.",
                _useful_god_summary(useful),
            )
        )
    elif key == "career":
        paragraphs.append(
            _fallback_join(
                "Nghề nghiệp được đọc từ Mệnh cục, mức thân vượng/nhược và cách Nhật chủ sử dụng nguồn lực.",
                _first_text(pattern.get("cach_cuc"), pattern.get("pattern")),
                _first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")),
            )
        )
    elif key == "marriage":
        paragraphs.append(
            _fallback_join(
                "Hôn nhân lấy trụ ngày và các tín hiệu nhân duyên làm điểm đọc chính.",
                _pillar_brief("Trụ ngày", _mapping(bazi.get("day_pillar"))),
                _group_brief(_mapping(_mapping(shen_groups.get("groups")).get("relationship"))),
            )
        )
    elif key == "children":
        paragraphs.append(
            _fallback_join(
                "Con cái và hậu vận đi nhiều qua trụ giờ, đồng thời cần xem vận nào kích hoạt mạnh phần này.",
                _pillar_brief("Trụ giờ", _mapping(bazi.get("hour_pillar"))),
                _layer_brief(_pillar_layer(ten_layers, "hour")),
            )
        )
    elif key == "parents":
        paragraphs.append(
            _fallback_join(
                "Bố mẹ và nền nâng đỡ ban đầu thường đọc ở trụ tháng.",
                _pillar_brief("Trụ tháng", _mapping(bazi.get("month_pillar"))),
                _layer_brief(_pillar_layer(ten_layers, "month")),
            )
        )
    elif key == "siblings":
        paragraphs.append(
            _fallback_join(
                "Anh em và người đồng hành gần được đọc qua các tín hiệu cùng vai/vai trò trong trụ tháng.",
                _layer_brief(_pillar_layer(ten_layers, "month")),
            )
        )
    elif key == "ancestry":
        paragraphs.append(
            _fallback_join(
                "Tổ tiên và gốc phúc là tầng nền của lá số, thường nhìn từ trụ năm.",
                _pillar_brief("Trụ năm", _mapping(bazi.get("year_pillar"))),
                _layer_brief(_pillar_layer(ten_layers, "year")),
            )
        )
    elif key == "property":
        paragraphs.append(
            _fallback_join(
                "Điền trạch cần đọc cùng Cung Phi, nhóm trạch và hành bổ trợ.",
                _first_text(calendar.get("cung_phi"), calendar.get("menh_quai")),
                _first_text(calendar.get("nhom_trach"), calendar.get("house_group")),
                _useful_god_summary(useful),
            )
        )

    advice = _DOMAIN_RECOMMENDATIONS.get(key, "")
    if advice:
        paragraphs.append(advice)
    return _unique_texts(paragraphs)


def _fallback_join(*parts: str) -> str:
    return " ".join(part for part in (_text(item).strip() for item in parts) if part)


def _pillar_brief(label: str, pillar: Mapping[str, Any]) -> str:
    can_chi = _pillar_can_chi(pillar)
    ten_god = _text(pillar.get("ten_god"))
    if can_chi and ten_god:
        return f"{label} {can_chi} có thập thần {ten_god}."
    if can_chi:
        return f"{label} {can_chi}."
    return ""


def _layer_brief(layer: Mapping[str, Any]) -> str:
    god = _text(layer.get("primary_ten_god"))
    hint = _text(layer.get("life_hint"))
    return _fallback_join(f"Thập thần chính: {god}." if god else "", hint)


def _group_brief(group: Mapping[str, Any]) -> str:
    items = [item for item in _list(group.get("items")) if isinstance(item, Mapping)]
    names = [_text(item.get("name")) for item in items if _text(item.get("name"))]
    if not names:
        return ""
    return "Tín hiệu Thần sát liên quan: " + ", ".join(names) + "."


def _age_range(item: Mapping[str, Any]) -> str:
    start = item.get("age_start")
    end = item.get("age_end")
    if start is not None and end is not None:
        return f"{start}-{end} tuổi"
    if start is not None:
        return f"từ {start} tuổi"
    return ""


def _shen_sha_group_key(name: str) -> str:
    for key, spec in _SHEN_SHA_GROUPS.items():
        if any(keyword in name for keyword in spec["keywords"]):
            return key
    return "other"


def _merge_life_domain_source(
    sections: dict[str, dict[str, Any]],
    source: Any,
    source_ref: str,
) -> None:
    if isinstance(source, Mapping):
        iterable = source.items()
    elif isinstance(source, list):
        iterable = ((str(index), item) for index, item in enumerate(source))
    else:
        return
    for raw_key, raw_value in iterable:
        value = raw_value if isinstance(raw_value, Mapping) else {"summary": raw_value}
        key = _life_domain_key(str(raw_key), value)
        if not key:
            continue
        section = sections[key]
        section["status"] = "draft"
        section["summary"] = _first_text(
            value.get("summary"),
            value.get("body"),
            value.get("content"),
            value.get("description"),
            section.get("summary"),
        )
        section["source_refs"] = _unique_texts([*section["source_refs"], source_ref])
        title = _first_text(value.get("title"), value.get("label"))
        if title:
            section["title"] = title


def _life_domain_key(raw_key: str, value: Mapping[str, Any]) -> str:
    haystack = " ".join(
        [
            raw_key,
            _text(value.get("id")),
            _text(value.get("domain")),
            _text(value.get("key")),
            _text(value.get("title")),
            _text(value.get("label")),
        ]
    ).lower()
    for key, aliases in _DOMAIN_ALIASES.items():
        if any(alias.lower() in haystack for alias in aliases):
            return key
    return ""


def _project_luck_cycle(item: Mapping[str, Any]) -> dict[str, Any]:
    gan_zhi = _first_text(item.get("gan_zhi"), item.get("ganzhi"), item.get("summary"))
    stem_element = _text(item.get("stem_element"))
    branch_element = _text(item.get("branch_element"))
    elements = " / ".join(part for part in (stem_element, branch_element) if part)
    summary = gan_zhi
    if elements:
        summary = f"{gan_zhi} kích hoạt {elements}" if gan_zhi else f"Kích hoạt {elements}"
    return {
        "index": item.get("index"),
        "gan_zhi": gan_zhi,
        "stem": _first_text(item.get("stem"), item.get("heavenly_stem")),
        "branch": _first_text(item.get("branch"), item.get("earthly_branch")),
        "stem_element": stem_element,
        "branch_element": branch_element,
        "age_start": item.get("age_start") if item.get("age_start") is not None else item.get("start_age"),
        "age_end": item.get("age_end") if item.get("age_end") is not None else item.get("end_age"),
        "year_start": item.get("year_start") if item.get("year_start") is not None else item.get("start_year"),
        "year_end": item.get("year_end") if item.get("year_end") is not None else item.get("end_year"),
        "summary": summary,
        "status": "draft",
    }


def _technical_section(
    title: str,
    summary: str,
    source_refs: list[str],
    existing: Any = None,
) -> dict[str, Any]:
    existing_map = _mapping(existing)
    text = _first_text(
        existing_map.get("summary"),
        existing_map.get("body"),
        existing_map.get("content"),
        summary,
    )
    return {
        "title": _first_text(existing_map.get("title"), title),
        "status": "draft" if text else "missing",
        "summary": text,
        "source_refs": _unique_texts([*_list(existing_map.get("source_refs")), *source_refs]),
    }


def _day_master_identity(bazi: Mapping[str, Any]) -> dict[str, str]:
    return {
        "stem": _text(bazi.get("day_master")),
        "element": _text(bazi.get("day_master_element")),
        "yin_yang": _text(bazi.get("day_master_yin_yang")),
    }


def _useful_god_identity(useful_god: Mapping[str, Any]) -> dict[str, str]:
    return {
        "display": _first_text(useful_god.get("useful_display"), useful_god.get("useful_stem"), useful_god.get("useful_element")),
        "stem": _text(useful_god.get("useful_stem")),
        "element": _text(useful_god.get("useful_element")),
        "ten_god": _text(useful_god.get("useful_ten_god")),
        "favorable_display": _text(useful_god.get("favorable_display")),
        "unfavorable_display": _text(useful_god.get("unfavorable_display")),
    }


def _day_master_summary(bazi: Mapping[str, Any]) -> str:
    stem = _text(bazi.get("day_master"))
    element = _text(bazi.get("day_master_element"))
    yin_yang = _text(bazi.get("day_master_yin_yang"))
    if not stem:
        return ""
    parts = [stem]
    if element:
        parts.append(f"thuộc {element}")
    if yin_yang:
        parts.append(f"tính {yin_yang}")
    return "Nhật chủ " + ", ".join(parts) + "."


def _useful_god_summary(useful_god: Mapping[str, Any]) -> str:
    display = _first_text(useful_god.get("useful_display"), useful_god.get("useful_stem"), useful_god.get("useful_element"))
    if not display:
        return ""
    parts = [f"Dụng thần trọng tâm: {display}."]
    favorable = _text(useful_god.get("favorable_display"))
    if favorable:
        parts.append(f"Hỷ thần/bổ trợ: {favorable}.")
    unfavorable = _text(useful_god.get("unfavorable_display"))
    if unfavorable:
        parts.append(f"Kỵ thần cần tiết chế: {unfavorable}.")
    reason = _first_text(useful_god.get("customer_reason"), useful_god.get("short_reason"))
    if reason:
        parts.append(reason)
    return " ".join(parts)


def _five_elements_summary(five_elements: Mapping[str, Any]) -> str:
    dominant = _text_list(five_elements.get("dominant"))
    missing = _text_list(five_elements.get("missing"))
    parts: list[str] = []
    if dominant:
        parts.append("Hành nổi bật: " + ", ".join(dominant) + ".")
    if missing:
        parts.append("Hành còn thiếu hoặc yếu: " + ", ".join(missing) + ".")
    return " ".join(parts)


def _ten_gods_summary(four_layer: Mapping[str, Any]) -> str:
    layers = [item for item in _list(four_layer.get("layers")) if isinstance(item, Mapping)]
    labels = []
    for item in layers:
        label = _first_text(item.get("label"), item.get("pillar"))
        god = _text(item.get("primary_ten_god"))
        if label and god:
            labels.append(f"{label}: {god}")
    if not labels:
        return ""
    return "Thập thần theo 4 trụ: " + "; ".join(labels) + "."


def _shen_sha_summary(grouped: Mapping[str, Any]) -> str:
    summary = [item for item in _list(grouped.get("summary")) if isinstance(item, Mapping)]
    labels = [
        f"{_text(item.get('title'))} ({item.get('count')})"
        for item in summary
        if _text(item.get("title")) and item.get("count")
    ]
    if not labels:
        return ""
    return "Các nhóm Thần sát hiện diện: " + "; ".join(labels) + "."


def _pillar_layer(four_layer: Mapping[str, Any], pillar: str) -> dict[str, Any]:
    for item in _list(four_layer.get("layers")):
        if isinstance(item, Mapping) and _text(item.get("pillar")) == pillar:
            return dict(item)
    return {}


def _ten_god_signal_labels(four_layer: Mapping[str, Any], labels: tuple[str, ...]) -> list[str]:
    found: list[str] = []
    for item in _list(four_layer.get("layers")):
        if not isinstance(item, Mapping):
            continue
        candidates = [_text(item.get("primary_ten_god"))]
        for field in ("visible", "hidden"):
            for occurrence in _list(item.get(field)):
                if isinstance(occurrence, Mapping):
                    candidates.append(_text(occurrence.get("ten_god")))
        for candidate in candidates:
            if candidate in labels:
                found.append(candidate)
    return _unique_texts(found)


def _module_seed(
    source_refs: list[str],
    usable_fields: Mapping[str, Any] | None = None,
    required_fields: list[str] | None = None,
) -> dict[str, Any]:
    fields = _customer_safe(_copy_mapping(usable_fields))
    missing = [
        field
        for field in (required_fields or [])
        if not _has_path(fields, field)
    ]
    return {
        "status": "draft",
        "source_refs": source_refs,
        "usable_fields": fields,
        "missing_fields": missing,
    }


def _build_pillar_table(bazi: Mapping[str, Any]) -> list[dict[str, Any]]:
    labels = (("year", "Năm"), ("month", "Tháng"), ("day", "Ngày"), ("hour", "Giờ"))
    rows: list[dict[str, Any]] = []
    for key, label in labels:
        pillar = bazi.get(f"{key}_pillar")
        if isinstance(pillar, Mapping):
            rows.append(
                _customer_safe(
                    {
                        "key": key,
                        "label": label,
                        "can_chi": _first_text(pillar.get("can_chi"), pillar.get("name")),
                        "stem": _text(pillar.get("stem")),
                        "branch": _text(pillar.get("branch")),
                        "ten_god": _text(pillar.get("ten_god")),
                        "nap_am": _text(pillar.get("nap_am")),
                        "truong_sinh": _text(pillar.get("truong_sinh")),
                    }
                )
            )
        elif pillar:
            rows.append({"key": key, "label": label, "can_chi": _text(pillar)})
    return rows


def _customer_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        safe: dict[str, Any] = {}
        for key, item in value.items():
            if str(key) in CUSTOMER_SAFE_BLOCKED_KEYS:
                continue
            if str(key).startswith("_"):
                continue
            safe[str(key)] = _customer_safe(item)
        return safe
    if isinstance(value, list):
        return [_customer_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_customer_safe(item) for item in value]
    return deepcopy(value)


def _is_customer_safe(value: Any) -> bool:
    blob = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return not any(token in blob for token in CUSTOMER_SAFE_BLOCKED_KEYS)


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _copy_mapping(value: Any) -> dict[str, Any]:
    return deepcopy(_mapping(value))


def _copy_mapping_or_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return deepcopy(dict(value))
    return deepcopy(value)


def _list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _list_or_single(value: Any) -> list[Any]:
    if isinstance(value, list):
        return list(value)
    if value:
        return [value]
    return []


def _text_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [_text(item) for item in value if _text(item)]
    text = _text(value)
    return [text] if text else []


def _first_mapping(*values: Any) -> dict[str, Any]:
    for value in values:
        if isinstance(value, Mapping) and value:
            return dict(value)
    return {}


def _text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _first_text(*values: Any) -> str:
    for value in values:
        text = _text(value)
        if text:
            return text
    return ""


def _non_empty(values: list[str]) -> list[str]:
    return [value for value in values if value]


def _non_empty_cards(cards: list[dict[str, str]]) -> list[dict[str, str]]:
    return [card for card in cards if _text(card.get("value"))]


def _unique_texts(values: list[Any]) -> list[str]:
    return list(dict.fromkeys(_text(value) for value in values if _text(value)))


def _has_path(data: Mapping[str, Any], path: str) -> bool:
    current: Any = data
    for part in path.split("."):
        if isinstance(current, Mapping):
            current = current.get(part)
        else:
            return False
    if isinstance(current, Mapping) or isinstance(current, list):
        return bool(current)
    return bool(_text(current))


def _join_label_value(label: str, value: str) -> str:
    if label and value:
        return f"{label} - {value}"
    return label or value


def _format_birth_time(hour: Any, minute: Any) -> str:
    if hour is None:
        return ""
    try:
        hour_int = int(hour)
        minute_int = int(minute or 0)
    except (TypeError, ValueError):
        return ""
    return f"{hour_int:02d}:{minute_int:02d}"
