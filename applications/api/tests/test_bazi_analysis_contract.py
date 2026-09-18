"""Stage 1 Xem lá số contract adapter tests."""

from __future__ import annotations

import inspect
import json

from applications.api.services import bazi_analysis_contract as contract_module
from applications.api.services.bazi_analysis_contract import (
    CONTRACT_VERSION,
    CUSTOMER_SAFE_BLOCKED_KEYS,
    build_bazi_analysis_result,
)


def _sample_payload() -> dict:
    return {
        "analysis_id": "analysis-001",
        "request_id": "analysis-001",
        "chart_id": "chart-001",
        "pipeline": ["calendar", "bazi", "pattern", "score", "interpretation", "report", "narrative"],
        "stage": "analyze",
        "customer": {
            "full_name": "Nguyễn Văn A",
            "gender": "male",
            "gender_label": "Nam",
            "birth_place": "Hà Nội",
            "timezone": "Asia/Ho_Chi_Minh",
        },
        "result_meta": {
            "analysis_id": "analysis-001",
            "created_at": "2026-09-14T08:00:00+00:00",
            "customer_contract": "analysis_result.UsefulGodView@1.5",
        },
        "identity": {
            "person": {
                "full_name": "Nguyễn Văn A",
                "gender": "male",
                "gender_label": "Nam",
                "birth_place": "Hà Nội",
                "timezone": "Asia/Ho_Chi_Minh",
            },
            "four_pillars": {"day": "Canh Ngọ"},
        },
        "calendar": {
            "solar_date": "21/01/1987",
            "lunar_date": "22/12/1986",
            "solar_hour": 3,
            "solar_minute": 30,
            "timezone_name": "Asia/Ho_Chi_Minh",
            "cung_phi": "Khôn",
            "hanh_cung": "Thổ",
            "nhom_trach": "Tây Tứ Trạch",
        },
        "bazi": {
            "day_master": "Canh",
            "day_master_element": "Kim",
            "day_master_yin_yang": "Dương",
            "year_pillar": {"can_chi": "Bính Dần", "nap_am": "Lư Trung Hỏa"},
            "month_pillar": {"can_chi": "Tân Sửu", "ten_god": "Kiếp Tài"},
            "day_pillar": {"can_chi": "Canh Ngọ", "ten_god": "Nhật chủ"},
            "hour_pillar": {"can_chi": "Mậu Dần", "ten_god": "Thiên Ấn"},
            "shensha_matches": [{"name": "Thiên Ất Quý Nhân"}, {"name": "Đào Hoa"}],
        },
        "five_elements": {
            "counts": {"wood": 2, "fire": 2, "earth": 2, "metal": 2, "water": 0},
            "dominant": ["metal"],
            "missing": ["water"],
            "unit_total": 8,
            "method_note": "Tính theo can chi và tàng can.",
        },
        "strength": {"strength_level": "Thân vượng", "matched_rules": ["internal-rule"]},
        "pattern": {
            "cach_cuc": "Chính Ấn cách",
            "than_vuong_nhuoc": "Thân vượng",
            "winning_rule_id": "PAT-001",
        },
        "temperature": {"climate_state_label": "Hàn thấp"},
        "useful_god": {
            "useful_display": "Hỏa",
            "useful_stem": "Đinh",
            "useful_ten_god": "Chính Quan",
            "unfavorable_display": "Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài",
            "customer_reason": {
                "reason_archetype": "INTERNAL",
                "balancing_action": "ôn ấm",
                "target_element": "Hỏa",
                "short_reason": "Nội bộ V1.0 không đưa ra khách.",
            },
            "candidate_list": ["internal-candidate"],
        },
        "ten_gods": {
            "visible": [{"pillar": "hour", "stem": "Mậu", "ten_god": "Thiên Ấn"}],
            "hidden": [{"pillar": "month", "hidden_stem": "Quý", "ten_god": "Thương Quan"}],
        },
        "can_xuong": {"display_weight": "4 lượng 7 chỉ", "classification": "Thượng cách"},
        "luck": {
            "direction": "forward",
            "direction_label": "Thuận vận",
            "start_age": 5,
            "current_cycle": {"gan_zhi": "Giáp Thìn", "age_start": 35, "age_end": 44},
            "cycles": [
                {
                    "index": 1,
                    "gan_zhi": "Giáp Thìn",
                    "stem": "Giáp",
                    "branch": "Thìn",
                    "stem_element": "Mộc",
                    "branch_element": "Thổ",
                    "age_start": 35,
                    "age_end": 44,
                    "year_start": 2022,
                    "year_end": 2031,
                }
            ],
        },
        "detailed_narrative": {
            "executive": {"headline": "Nền mệnh có sức bật tốt."},
            "labels": {"strength": "Thân vượng"},
            "domains": {"health": {"title": "Sức khỏe"}, "career": {"title": "Nghề nghiệp"}},
            "luck": {"current": "Đại vận cần đi chậm mà chắc."},
            "actions": [{"title": "Ưu tiên kỷ luật tài chính."}],
            "schema_version": "internal-v1",
            "metadata": {"traceability": "hidden"},
        },
        "useful_god_source": {"contract": "analysis_result.UsefulGodView@1.5"},
        "pattern_source": {"source": "pattern_engine"},
    }


def test_bazi_analysis_contract_shape_and_core_layers() -> None:
    result = build_bazi_analysis_result(
        _sample_payload(),
        input_payload={"hour": 3, "minute": 30},
        analysis_id="analysis-001",
        request_id="analysis-001",
    )

    assert result["contract"] == CONTRACT_VERSION
    assert result["analysis_id"] == "analysis-001"
    assert result["subject"]["full_name"] == "Nguyễn Văn A"
    assert result["subject"]["birth_time"] == "03:30"

    assert result["technical_data"]["day_master"]["stem"] == "Canh"
    assert result["technical_data"]["four_pillars"]["bazi"]["day"]["can_chi"] == "Canh Ngọ"
    assert result["technical_data"]["five_elements"]["counts"]["metal"] == 2
    assert result["technical_data"]["structure"]["cach_cuc"] == "Chính Ấn cách"
    assert result["technical_data"]["useful_god"]["useful_display"] == "Hỏa"
    assert result["technical_data"]["ten_gods"]["four_layer"]["status"] == "ready"
    assert result["technical_data"]["ten_gods"]["four_layer"]["layers"][3]["primary_ten_god"] == "Thiên Ấn"
    assert result["technical_data"]["shen_sha"]["grouped"]["groups"]["noble_support"]["items"][0]["name"] == "Thiên Ất Quý Nhân"
    assert result["technical_data"]["shen_sha"]["grouped"]["groups"]["relationship"]["items"][0]["name"] == "Đào Hoa"

    assert result["presentation_data"]["hero"]["primary_tags"]
    assert result["presentation_data"]["summary_cards"]
    assert result["presentation_data"]["pillar_table"]
    assert result["presentation_data"]["five_element_chart"]["missing"] == ["Thủy"]
    assert result["presentation_data"]["five_element_chart"]["dominant"] == ["Kim"]

    assert result["customer_narrative"]["provider"] == "detailed_narrative"
    assert result["customer_narrative"]["overview"]["headline"] == "Nền mệnh có sức bật tốt."
    assert result["customer_narrative"]["technical_explanations"]["day_master"]["summary"] == "Nhật chủ Canh, thuộc Kim, tính Dương."
    assert result["customer_narrative"]["technical_explanations"]["useful_god"]["summary"].startswith("Dụng thần trọng tâm: Hỏa.")
    assert "V1.0" not in result["customer_narrative"]["technical_explanations"]["useful_god"]["summary"]
    assert "reason_archetype" not in result["customer_narrative"]["technical_explanations"]["useful_god"]["summary"]
    assert result["customer_narrative"]["technical_explanations"]["ten_gods"]["summary"].startswith("Thập thần theo 4 trụ:")
    assert set(result["customer_narrative"]["life_domains"]) == {
        "health",
        "wealth",
        "career",
        "marriage",
        "children",
        "parents",
        "siblings",
        "ancestry",
        "property",
    }
    assert result["customer_narrative"]["life_domains"]["health"]["status"] == "draft"
    assert len(result["customer_narrative"]["life_domains"]["health"]["paragraphs"]) >= 2
    assert result["customer_narrative"]["life_domains"]["health"]["recommendations"]
    health_paragraphs = result["customer_narrative"]["life_domains"]["health"]["paragraphs"]
    health_text = " ".join(health_paragraphs)
    assert "Bảng Ngũ hành cho thấy" in health_text
    assert "Theo hệ quy chiếu truyền thống" in health_text
    assert "không dùng lá số thay cho chẩn đoán" in health_text
    assert result["customer_narrative"]["life_domains"]["parents"]["status"] == "draft"
    assert result["customer_narrative"]["life_domains"]["parents"]["summary"]
    assert len(result["customer_narrative"]["life_domains"]["marriage"]["paragraphs"]) >= 2
    life_paragraphs = result["customer_narrative"]["life_domains"]["career"]["paragraphs"]
    assert life_paragraphs[0].startswith("Con đường nghề nghiệp hình thành từ trụ tháng")
    assert "Trong đời sống, khí này thường biểu hiện" in " ".join(life_paragraphs)
    assert result["customer_narrative"]["life_domains"]["marriage"]["recommendations"]
    assert result["customer_narrative"]["luck_cycles"]["status"] == "draft"
    assert result["customer_narrative"]["luck_cycles"]["cycles"][0]["summary"] == "Giáp Thìn kích hoạt Mộc / Thổ"
    four_pillar_paragraphs = " ".join(result["customer_narrative"]["report_chapters"][1]["paragraphs"])
    day_master_paragraphs = " ".join(result["customer_narrative"]["report_chapters"][2]["paragraphs"])
    five_element_paragraphs = " ".join(result["customer_narrative"]["report_chapters"][3]["paragraphs"])
    strength_paragraphs = " ".join(result["customer_narrative"]["report_chapters"][4]["paragraphs"])
    ten_gods_paragraphs = " ".join(result["customer_narrative"]["report_chapters"][5]["paragraphs"])
    shen_sha_paragraphs = " ".join(result["customer_narrative"]["report_chapters"][6]["paragraphs"])
    bone_weight_paragraphs = " ".join(result["customer_narrative"]["report_chapters"][7]["paragraphs"])
    palace_paragraphs = " ".join(result["customer_narrative"]["report_chapters"][8]["paragraphs"])
    luck_paragraphs = " ".join(result["customer_narrative"]["report_chapters"][10]["paragraphs"])
    synthesis_paragraphs = " ".join(result["customer_narrative"]["report_chapters"][11]["paragraphs"])
    assert "tàng can/thập thần ẩn Thương Quan" in four_pillar_paragraphs
    assert "Quan hệ Địa chi" in four_pillar_paragraphs
    assert "bán hợp Dần-Ngọ" in four_pillar_paragraphs
    assert "Khi nối bốn trụ thành một hành trình" in four_pillar_paragraphs
    assert "là hình ảnh trung tâm của lá số" in day_master_paragraphs
    assert "Kim sinh Thủy" in day_master_paragraphs
    assert "chịu Hỏa khắc" in day_master_paragraphs
    assert "Ngũ hành tạo nên nhịp chuyển động bên trong lá số" in five_element_paragraphs
    assert "không đơn thuần là bù vào một con số đang thấp" in five_element_paragraphs
    assert "Trục cân bằng của Nhật chủ" in strength_paragraphs
    assert "Dùng Hỏa là tăng ánh sáng" in strength_paragraphs
    assert "Phần khí cần tiết chế là Kim" in strength_paragraphs
    assert "hợp tác chỉ bền khi vai trò" in ten_gods_paragraphs
    assert "Quý nhân/phúc tinh" in shen_sha_paragraphs
    assert "Cân xương ghi nhận 4 lượng 7 chỉ" in bone_weight_paragraphs
    assert "Giá trị của Cân xương nằm ở việc bổ sung sắc thái" in bone_weight_paragraphs
    assert "Cung Phi/Mệnh quái của lá số là Khôn" in palace_paragraphs
    assert "Tây, Tây Bắc, Tây Nam, Đông Bắc" in palace_paragraphs
    assert "Cung Phi đưa phần luận từ con người sang không gian" in palace_paragraphs
    assert "Trục nên dùng khi đọc vận" in luck_paragraphs
    assert "Khí Mộc mở nhu cầu học hỏi" in luck_paragraphs
    assert "Nhìn lại toàn cục, đường dây xuyên suốt của lá số" in synthesis_paragraphs
    assert "Lợi thế đáng quý của lá số" in synthesis_paragraphs
    assert "Con đường cải thiện nên bắt đầu từ nền sức khỏe" in synthesis_paragraphs
    assert [item["id"] for item in result["customer_narrative"]["report_chapters"]] == [
        "overview",
        "four_pillars",
        "day_master",
        "five_elements",
        "strength_structure_useful_god",
        "ten_gods",
        "shen_sha",
        "bone_weight",
        "palace_feng_shui",
        "life_domains",
        "luck_cycles",
        "synthesis",
        "recommendations",
    ]
    life_chapter_paragraphs = result["customer_narrative"]["report_chapters"][9]["paragraphs"]
    assert life_chapter_paragraphs
    assert life_chapter_paragraphs[0].startswith("Sức khỏe - ")
    assert any(paragraph.startswith("Mệnh/Tài vận - ") for paragraph in life_chapter_paragraphs)
    assert any(paragraph.startswith("Nhân duyên/Hôn nhân - ") for paragraph in life_chapter_paragraphs)
    assert any(paragraph.startswith("Điền trạch - ") for paragraph in life_chapter_paragraphs)
    assert all("Dụng thần trọng tâm:" not in paragraph for paragraph in life_chapter_paragraphs)
    report_document = result["customer_narrative"]["report_document"]
    assert report_document["title"] == "Bản luận giải lá số Bát Tự"
    assert report_document["chapter_count"] == 13
    assert "# Bản luận giải lá số Bát Tự" in report_document["markdown"]
    assert "## 9 mục đời sống" in report_document["markdown"]
    assert "## Cân xương đoán mệnh" in report_document["markdown"]
    assert "## Cung Phi và phương vị" in report_document["markdown"]
    assert "## Đại vận" in report_document["markdown"]
    assert "## Kết luận tổng hợp" in report_document["markdown"]
    markdown = report_document["markdown"]
    assert "Dữ liệu dùng để luận" not in markdown
    assert "Ý nghĩa luận giải" not in markdown
    assert "Tầng này chủ về" not in markdown
    assert "Luận theo 4 tầng" in markdown
    assert "Từ nền này, các phần nghề nghiệp, tài vận, hôn nhân" in markdown
    assert "mọi kết luận đều quay lại trục Dụng thần" in markdown
    assert result["module_exports"]["marriage_seed"]["status"] == "draft"
    assert result["module_exports"]["marriage_seed"]["usable_fields"]["day_master"]["stem"] == "Canh"
    assert result["module_exports"]["career_seed"]["usable_fields"]["structure"] == "Chính Ấn cách"
    assert result["module_exports"]["feng_shui_seed"]["usable_fields"]["five_elements"]["missing"] == ["Thủy"]
    assert result["module_exports"]["child_planning_seed"]["usable_fields"]["hour_layer"]["primary_ten_god"] == "Thiên Ấn"
    assert result["meta"]["contract_version"] == CONTRACT_VERSION


def test_health_narrative_uses_element_relations() -> None:
    payload = _sample_payload()
    payload["five_elements"]["counts"] = {"wood": 1, "fire": 5, "earth": 6, "metal": 4, "water": 0}
    payload["five_elements"]["dominant"] = ["earth"]
    payload["five_elements"]["missing"] = ["water"]
    payload["temperature"] = {"climate_state_label": "Hàn"}
    payload["ten_gods"]["visible"].append({"pillar": "month", "stem": "Đinh", "ten_god": "Chính Quan"})

    result = build_bazi_analysis_result(payload)

    health_text = " ".join(result["customer_narrative"]["life_domains"]["health"]["paragraphs"])
    assert "Thổ vượng sinh Kim" in health_text
    assert "hô hấp, phổi, mũi xoang" in health_text
    assert "viêm xoang, dị ứng" in health_text
    assert "Hỏa khắc Kim" in health_text
    assert "xương khớp" in health_text
    assert "áp lực công việc" in health_text


def test_core_life_domains_use_ten_god_reasoning() -> None:
    payload = _sample_payload()
    payload["ten_gods"]["visible"].extend(
        [
            {"pillar": "year", "stem": "Giáp", "ten_god": "Thiên Tài"},
            {"pillar": "month", "stem": "Đinh", "ten_god": "Chính Quan"},
            {"pillar": "day", "stem": "Ất", "ten_god": "Chính Tài"},
        ]
    )

    result = build_bazi_analysis_result(payload)
    domains = result["customer_narrative"]["life_domains"]
    wealth_text = " ".join(domains["wealth"]["paragraphs"])
    career_text = " ".join(domains["career"]["paragraphs"])
    marriage_text = " ".join(domains["marriage"]["paragraphs"])
    partnership_text = " ".join(domains["siblings"]["paragraphs"])
    children_text = " ".join(domains["children"]["paragraphs"])
    parents_text = " ".join(domains["parents"]["paragraphs"])
    ancestry_text = " ".join(domains["ancestry"]["paragraphs"])
    property_text = " ".join(domains["property"]["paragraphs"])

    assert "Tín hiệu Tài tinh đang thấy" in wealth_text
    assert "Luận Tài tinh: Chính Tài" in wealth_text
    assert "Luận nguồn sinh tài" in wealth_text
    assert "Kim nổi bật là tín hiệu tốt cho khả năng quản trị tiền" in wealth_text
    assert "Cung Phi Khôn" in wealth_text
    assert "Tây Tứ Trạch" in wealth_text
    assert "Nhóm tín hiệu nghề nghiệp nổi bật" in career_text
    assert "Luận nghề theo Thập thần: Chính Quan" in career_text
    assert "môi trường có chuẩn mực" in career_text
    assert "Thê tinh được đọc qua Chính Tài, Thiên Tài" in marriage_text
    assert "Chính Tài lộ tại trụ ngày" in marriage_text
    assert "người vợ biết vun vén, giữ lời" in marriage_text
    assert "Với nam mệnh" in marriage_text
    assert "Kết luận thực tế:" in marriage_text
    assert "nền cho tư vấn hợp tác" in partnership_text
    assert "Luận hợp tác: Kiếp Tài" in partnership_text
    assert "hợp đồng, pháp lý, phân quyền" in partnership_text
    assert "Sao tử tức cần quan sát: Chính Quan, Thất Sát" in children_text
    assert "Luận con cái/hậu vận: Thiên Ấn" in children_text
    assert "Đại vận và Lưu niên" in children_text
    assert "Luận nền bố mẹ: Kiếp Tài" in parents_text
    assert "môi trường trưởng thành" in parents_text
    assert "Luận gốc phúc: Thiên Tài" in ancestry_text
    assert "Tín hiệu Thần sát liên quan" in ancestry_text
    assert "Nhóm trạch: Tây Tứ Trạch" in property_text
    assert "Ngũ hành cần nâng trong không gian là Hỏa" in property_text
    assert "Tây, Tây Bắc, Tây Nam, Đông Bắc" in property_text


def test_marriage_narrative_reasons_from_spouse_star_position_and_palace() -> None:
    payload = _sample_payload()
    payload["customer"].update({"gender": "female", "gender_label": "Nữ"})
    payload["identity"]["person"].update({"gender": "female", "gender_label": "Nữ"})
    payload["bazi"]["day_pillar"] = {"can_chi": "Giáp Thìn", "ten_god": "Nhật chủ"}
    payload["bazi"]["hour_pillar"] = {"can_chi": "Tân Mùi", "ten_god": "Chính Quan"}
    payload["ten_gods"] = {
        "visible": [{"pillar": "hour", "stem": "Tân", "ten_god": "Chính Quan"}],
        "hidden": [
            {"pillar": "day", "hidden_stem": "Mậu", "ten_god": "Thiên Tài"},
            {"pillar": "day", "hidden_stem": "Ất", "ten_god": "Kiếp Tài"},
            {"pillar": "day", "hidden_stem": "Quý", "ten_god": "Chính Ấn"},
        ],
    }

    result = build_bazi_analysis_result(payload)
    marriage_text = " ".join(result["customer_narrative"]["life_domains"]["marriage"]["paragraphs"])

    assert "Phu tinh được đọc qua Chính Quan, Thất Sát" in marriage_text
    assert "Chính Quan lộ tại trụ giờ" in marriage_text
    assert "Duyên chính thức thường rõ hơn khi chủ mệnh đã trưởng thành" in marriage_text
    assert "Cung phối ngẫu đặt tại Thìn" in marriage_text
    assert "Thiên Tài, Kiếp Tài, Chính Ấn" in marriage_text
    assert "Phu/Thê tinh không nằm trực tiếp trong cung này" in marriage_text
    assert "hình tượng phù hợp là một người chồng chững chạc" in marriage_text
    assert "Kết luận thực tế:" in marriage_text
    assert "không đủ độ phân giải để chốt chính xác nghề nghiệp" in marriage_text


def test_customer_facing_layers_do_not_leak_technical_tokens() -> None:
    result = build_bazi_analysis_result(_sample_payload())
    customer_blob = json.dumps(
        {
            "presentation_data": result["presentation_data"],
            "customer_narrative": result["customer_narrative"],
        },
        ensure_ascii=False,
        sort_keys=True,
    )

    for token in CUSTOMER_SAFE_BLOCKED_KEYS:
        assert token not in customer_blob

    assert result["technical_data"]["strength"]["matched_rules"] == ["internal-rule"]
    assert result["technical_data"]["structure"]["winning_rule_id"] == "PAT-001"
    assert result["quality"]["customer_safe"] is True
    assert result["quality"]["has_life_domains"] is True
    assert result["quality"]["has_ten_gods_four_layer"] is True
    assert result["quality"]["has_shen_sha_grouped"] is True
    assert result["quality"]["has_technical_explanations"] is True
    assert result["quality"]["has_module_exports"] is True
    assert result["quality"]["has_complete_report_chapters"] is True
    assert result["quality"]["has_report_document"] is True
    assert result["quality"]["missing_sections"] == []
    assert result["quality"]["missing_technical_explanations"] == []
    assert result["quality"]["missing_module_exports"] == []
    assert result["quality"]["missing_report_chapters"] == []


def test_bazi_contract_adapter_does_not_depend_on_number_energy() -> None:
    source = inspect.getsource(contract_module)
    assert "number_energy" not in source
    assert "NumberEnergy" not in source
