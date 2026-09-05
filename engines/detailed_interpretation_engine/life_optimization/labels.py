"""Deterministic Vietnamese labels for Life Optimization. No narrative prose."""

from __future__ import annotations

TITLE = "KẾ HOẠCH TỐI ƯU"

GROUP_LABELS: dict[str, str] = {
    "develop": "NÊN PHÁT HUY",
    "improve": "CẦN CẢI THIỆN",
    "control": "CẦN KIỂM SOÁT",
    "avoid": "NÊN TRÁNH / HẠN CHẾ",
    "temporal": "THEO VẬN HIỆN TẠI",
}

SCOPE_LABELS: dict[str, str] = {
    "natal_long_term": "Dài hạn",
    "current_luck_cycle": "Vận hiện tại",
    "current_annual": "Năm hiện tại",
}

DOMAIN_TITLES: dict[str, str] = {
    "authority": "Quyền lực",
    "career": "Sự nghiệp",
    "wealth": "Tài",
    "relationship": "Quan hệ",
    "legacy": "Di sản",
    "vitality": "Sinh lực",
}

ACTION_TYPE_LABELS: dict[str, str] = {
    "strengthen": "Tăng cường",
    "reduce": "Giảm tải",
    "protect": "Bảo vệ",
    "stabilize": "Ổn định",
    "release": "Giải tỏa",
    "support": "Hỗ trợ",
    "convert": "Chuyển hóa",
    "retain": "Giữ vốn",
    "recover": "Phục hồi",
    "develop": "Phát triển",
    "avoid": "Hạn chế",
    "monitor": "Theo dõi",
}

ACTION_LABELS: dict[str, str] = {
    "opt.wealth.retain_capital_discipline": "Giữ kỷ luật vốn",
    "opt.wealth.convert_commercialization": "Chuyển hóa thành giá trị",
    "opt.wealth.avoid_expansion": "Hạn chế mở rộng",
    "opt.career.protect_workload": "Kiểm soát khối lượng việc",
    "opt.career.support_management": "Hỗ trợ năng lực quản lý",
    "opt.career.convert_skill_to_role": "Chuyển kỹ năng thành vai trò",
    "opt.career.avoid_expansion": "Không tăng khối lượng việc",
    "opt.authority.protect_pressure": "Kiểm soát áp lực quyền",
    "opt.authority.avoid_exposure": "Không tăng thêm quyền/trách nhiệm",
    "opt.relationship.develop_communication": "Tăng chất lượng giao tiếp",
    "opt.legacy.develop_transmission": "Phát triển truyền thừa",
    "opt.vitality.protect_recovery": "Bảo vệ phục hồi",
    "opt.vitality.recover_capacity": "Phục hồi năng lực bền",
    "opt.element.support_function": "Hỗ trợ chức năng hành",
}

REASON_LABELS: dict[str, str] = {
    "wealth.volatility_high": "Tài biến động cao, cần bảo vệ giữ vốn",
    "wealth.commercialization_gap": "Sản xuất chưa chuyển thành giá trị",
    "wealth.creation_not_driver": "Không tăng thêm sản xuất khi nút thắt nằm ở thương mại hóa",
    "career.overloaded": "Sự nghiệp đang quá tải, cần kiểm soát trước khi mở rộng",
    "career.management_gap": "Nút thắt quản lý cần được hỗ trợ",
    "career.skill_role_gap": "Kỹ năng cao chưa thành vai trò hữu dụng",
    "authority.overloaded": "Quyền lực đang quá tải, không tăng thêm trách nhiệm",
    "relationship.communication": "Nút thắt giao tiếp cần được cải thiện",
    "legacy.transmission": "Truyền thừa cần được phát triển",
    "vitality.recovery": "Phục hồi yếu, cần bảo vệ năng lực",
    "vitality.stress_from_career": "Sự nghiệp đang chuyển áp lực sang sinh lực",
    "useful_god.function": "Dụng thần cần được dùng theo chức năng cấu trúc",
    "element.function_support": "Hỗ trợ chức năng hành, không thêm hành theo số đếm",
    "ky.not_ban": "Kỵ thần là ngữ cảnh tránh khuếch đại, không cấm tuyệt đối",
}

EFFECT_LABELS: dict[str, str] = {
    "reduce_leakage": "Giảm rò rỉ",
    "protect_recovery": "Bảo vệ phục hồi",
    "improve_commercialization": "Cải thiện thương mại hóa",
    "increase_communication_quality": "Tăng chất lượng giao tiếp",
    "stabilize_capital": "Ổn định vốn",
    "support_transmission": "Hỗ trợ truyền thừa",
    "control_workload": "Kiểm soát khối lượng việc",
    "control_authority_pressure": "Kiểm soát áp lực quyền",
    "support_management": "Hỗ trợ quản lý",
    "convert_skill_to_role": "Chuyển kỹ năng thành vai trò",
    "support_element_function": "Hỗ trợ chức năng hành",
}

FUNCTION_LABELS: dict[str, str] = {
    "growth": "tăng trưởng",
    "planning": "kế hoạch",
    "development": "phát triển",
    "learning": "học hỏi",
    "flexibility": "linh hoạt",
    "activation": "kích hoạt",
    "warmth": "sức ấm",
    "visibility": "hiển lộ",
    "communication": "giao tiếp",
    "leadership_expression": "thể hiện lãnh đạo",
    "stability": "ổn định",
    "systems": "hệ thống",
    "retention": "giữ vốn",
    "continuity": "liên tục",
    "discipline": "kỷ luật",
    "precision": "chính xác",
    "rules": "quy tắc",
    "execution": "thực thi",
    "quality_control": "kiểm soát chất lượng",
    "adaptation": "thích ứng",
    "recovery": "phục hồi",
    "information": "thông tin",
    "flow": "lưu thông",
    "reflection": "soi chiếu",
}

ELEMENT_DIRECTION_LABELS: dict[str, str] = {
    "support": "cần tăng chức năng",
    "protect": "cần giữ chức năng",
    "reduce": "cần giảm khuếch đại",
    "monitor": "theo dõi",
}

CONFLICT_LABELS: dict[str, str] = {
    "career_vitality_stress": "Sự nghiệp cần đầu ra, sinh lực cần phục hồi",
    "career_wealth_conflict": "Sự nghiệp và Tài đang kéo theo hướng khác nhau",
    "authority_career_overload": "Quyền lực và sự nghiệp cùng quá tải",
}

CAUTION_LABELS: dict[str, str] = {
    "expansion_when_retention_weak": "Mở rộng không phù hợp khi giữ vốn yếu",
    "expansion_when_volatility_high": "Mở rộng không phù hợp khi biến động cao",
    "expansion_when_management_weak": "Mở rộng không phù hợp khi quản lý yếu",
    "more_workload_when_overloaded": "Không tăng khối lượng việc khi đang quá tải",
    "more_authority_when_overloaded": "Không tăng thêm quyền khi đang quá tải",
    "no_medical": "Không phải lời khuyên y khoa",
    "no_investment_picks": "Không phải khuyến nghị giao dịch cụ thể",
}

PRIORITY_RANK_LABELS: dict[int, str] = {
    1: "Ưu tiên 1",
    2: "Ưu tiên 2",
    3: "Ưu tiên 3",
}
