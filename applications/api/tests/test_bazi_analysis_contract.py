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
    assert life_paragraphs[0].startswith("Dữ liệu dùng để luận nghề nghiệp")
    assert "Ý nghĩa luận giải" in " ".join(life_paragraphs)
    assert result["customer_narrative"]["life_domains"]["marriage"]["recommendations"]
    assert result["customer_narrative"]["luck_cycles"]["status"] == "draft"
    assert result["customer_narrative"]["luck_cycles"]["cycles"][0]["summary"] == "Giáp Thìn kích hoạt Mộc / Thổ"
    assert [item["id"] for item in result["customer_narrative"]["report_chapters"]] == [
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
    ]
    assert result["customer_narrative"]["report_chapters"][7]["paragraphs"]
    report_document = result["customer_narrative"]["report_document"]
    assert report_document["title"] == "Bản luận giải lá số Bát Tự"
    assert report_document["chapter_count"] == 10
    assert "# Bản luận giải lá số Bát Tự" in report_document["markdown"]
    assert "## 9 mục đời sống" in report_document["markdown"]
    assert "## Đại vận" in report_document["markdown"]
    markdown = report_document["markdown"]
    assert "Dữ liệu dùng để luận" in markdown
    assert "Ý nghĩa luận giải" in markdown
    assert "Luận theo 4 tầng" in markdown
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

    assert "Tín hiệu Tài tinh đang thấy" in wealth_text
    assert "Luận Tài tinh: Chính Tài" in wealth_text
    assert "Luận nguồn sinh tài" in wealth_text
    assert "Kim nổi bật là tín hiệu tốt cho khả năng quản trị tiền" in wealth_text
    assert "Cung Phi Khôn" in wealth_text
    assert "Tây Tứ Trạch" in wealth_text
    assert "Nhóm tín hiệu nghề nghiệp nổi bật" in career_text
    assert "Luận nghề theo Thập thần: Chính Quan" in career_text
    assert "môi trường có chuẩn mực" in career_text
    assert "Sao phối ngẫu cần quan sát: Chính Tài, Thiên Tài" in marriage_text
    assert "Luận sao phối ngẫu: Chính Tài" in marriage_text
    assert "với nam mệnh" in marriage_text


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
