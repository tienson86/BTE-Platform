"""Stage 1 Bazi analysis result contract.

This adapter is presentation/data-contract glue only. It does not recalculate
the chart and does not call any engine.
"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

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
    "bone_weight",
    "palace_feng_shui",
    "life_domains",
    "luck_cycles",
    "synthesis",
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

BRANCH_THREE_COMBINATIONS = (
    (("Thân", "Tý", "Thìn"), "Thủy"),
    (("Hợi", "Mão", "Mùi"), "Mộc"),
    (("Dần", "Ngọ", "Tuất"), "Hỏa"),
    (("Tỵ", "Dậu", "Sửu"), "Kim"),
)

BRANCH_SIX_CLASHES = (
    ("Tý", "Ngọ"),
    ("Sửu", "Mùi"),
    ("Dần", "Thân"),
    ("Mão", "Dậu"),
    ("Thìn", "Tuất"),
    ("Tỵ", "Hợi"),
)

ELEMENT_LABELS = {
    "wood": "Mộc",
    "fire": "Hỏa",
    "earth": "Thổ",
    "metal": "Kim",
    "water": "Thủy",
}

HEAVENLY_STEM_ELEMENTS = {
    "Giáp": "Mộc",
    "Ất": "Mộc",
    "Bính": "Hỏa",
    "Đinh": "Hỏa",
    "Mậu": "Thổ",
    "Kỷ": "Thổ",
    "Canh": "Kim",
    "Tân": "Kim",
    "Nhâm": "Thủy",
    "Quý": "Thủy",
}

STRENGTH_LABELS = {
    "weak": "Thân nhược",
    "balanced": "Thân trung hòa",
    "strong": "Thân vượng",
    "too_weak": "Thân quá nhược",
    "too_strong": "Thân quá vượng",
}

STRENGTH_PUBLIC_GUIDANCE = {
    "Thân vượng": "Nhật chủ có lực tự thân khá rõ, vì vậy khi luận nên ưu tiên cách tiết chế, điều hòa và đưa năng lượng vào việc có khuôn khổ.",
    "Thân quá vượng": "Nhật chủ quá nhiều lực cùng phe, dễ mạnh ở ý chí nhưng cũng dễ cứng; trọng tâm luận giải là mở dòng tiết, dùng kỷ luật và môi trường phù hợp để giảm cực đoan.",
    "Thân trung hòa": "Nhật chủ có nền lực vừa phải, không nên đọc theo hướng thiếu hay thừa tuyệt đối; trọng tâm là giữ nhịp cân bằng và chọn đúng điểm kích hoạt.",
    "Thân nhược": "Nhật chủ cần thêm điểm tựa và nguồn sinh trợ; khi luận nên ưu tiên nền tảng, người hỗ trợ, môi trường ổn định và cách đi từng bước.",
    "Thân quá nhược": "Nhật chủ thiếu lực nâng đỡ rõ, nên tránh gánh việc quá sức; trọng tâm là bồi nền, giảm áp lực và chọn đường đi có người, có hệ thống hỗ trợ.",
}

TEN_GOD_PUBLIC_MEANINGS = {
    "Nhật Chủ": "lõi bản thân, khí chất gốc và cách người này tự đứng trong đời sống",
    "Nhật chủ": "lõi bản thân, khí chất gốc và cách người này tự đứng trong đời sống",
    "Tỷ Kiên": "tính tự chủ, sức cạnh tranh ngang vai và nhu cầu giữ lập trường riêng",
    "Kiếp Tài": "sự chia sẻ hoặc tranh đoạt nguồn lực, bạn đồng hành, đối thủ và áp lực phân vai",
    "Thực Thần": "khả năng tạo sản phẩm, nuôi dưỡng thành quả, hưởng thụ lành mạnh và độ bền sáng tạo",
    "Thương Quan": "khả năng biểu đạt, phá khuôn, phản biện và nhu cầu được làm theo cách riêng",
    "Chính Tài": "nguồn tiền ổn định, năng lực quản lý tài sản, trách nhiệm vật chất và kết quả cụ thể",
    "Thiên Tài": "cơ hội linh hoạt, tài lộc ngoài khuôn cố định, quan hệ xã hội và khả năng xoay chuyển nguồn lực",
    "Chính Quan": "kỷ luật, danh phận, trách nhiệm, luật lệ và con đường phát triển qua chuẩn mực rõ ràng",
    "Thất Sát": "áp lực cạnh tranh, thử thách mạnh, quyền lực, rủi ro và khả năng bứt phá khi có kiểm soát",
    "Chính Ấn": "nền học hỏi, bảo hộ, uy tín, bằng cấp, người nâng đỡ và khả năng đi đường dài bằng nền tảng",
    "Thiên Ấn": "trực giác, tư duy khác biệt, khả năng nghiên cứu sâu và cách tiếp cận không theo lối thông thường",
}

DOMAIN_LOGIC_LEADS = {
    "health": "Sức khỏe của lá số được nhìn như một trạng thái cân bằng: Ngũ hành cho thấy nơi dễ quá tải hoặc suy yếu, khí hậu cho biết cơ thể hợp ấm hay mát, còn thế Thân phản ánh cách chủ mệnh tiêu hao và hồi phục năng lượng.",
    "wealth": "Tài vận không chỉ nằm ở việc có Tài tinh hay không. Mệnh cục cho biết cách tổ chức nguồn lực, Thực Thần và Thương Quan cho thấy năng lực tạo giá trị, còn Đại vận quyết định thời điểm dòng tiền dễ mở hay cần giữ.",
    "career": "Con đường nghề nghiệp hình thành từ trụ tháng và Mệnh cục: một bên phản ánh môi trường làm việc phù hợp, một bên cho thấy vai trò mà chủ mệnh dễ phát huy. Quan, Sát, Ấn và Thực Thương giúp làm rõ nên đi bằng chuyên môn, quản trị hay năng lực tạo sản phẩm.",
    "marriage": "Hôn nhân được đọc từ trụ ngày, nơi bản thân và cung phối ngẫu cùng hiện diện. Dụng thần cho biết kiểu quan hệ giúp hai người cân bằng, còn sao phối ngẫu và duyên tinh cho thấy cách cơ hội tình cảm thường tìm đến.",
    "children": "Trụ giờ mở câu chuyện về con cái, hậu vận và những thành quả được để lại về sau. Thập thần tại đây mô tả cách nuôi dưỡng, còn Đại vận và Lưu niên giúp nhận ra giai đoạn nào nền gia đình thuận hơn cho kế hoạch dài hạn.",
    "parents": "Trụ tháng lưu dấu khá rõ ảnh hưởng của cha mẹ và môi trường trưởng thành. Qua đó có thể thấy chủ mệnh đã nhận được kiểu nâng đỡ nào, chịu kỳ vọng gì và mang theo bài học gia đình ra sao khi bước vào đời.",
    "siblings": "Quan hệ anh em và người đồng hành được soi qua các sao ngang vai, cạnh tranh và chia sẻ nguồn lực. Điểm quan trọng không phải nhiều hay ít người hỗ trợ, mà là cách phân vai, giữ ranh giới và cùng nhau đi đến kết quả.",
    "ancestry": "Trụ năm là lớp nền xa nhất, phản ánh khí chất gia tộc, môi trường ban đầu và những giá trị được truyền lại. Phần này giúp chủ mệnh hiểu mình đến từ đâu, nhưng không biến nguồn gốc thành một định mệnh cố định.",
    "property": "Điền trạch là câu chuyện về một nơi chốn đủ sức nâng đỡ đời sống lâu dài. Cung Phi và nhóm trạch gợi phương vị, Ngũ hành và Dụng thần cho biết không gian nên được tổ chức thế nào để vừa hợp khí vừa thuận công năng.",
}

ELEMENT_HEALTH_AREAS = {
    "Mộc": "gan mật, gân cơ, mắt và khả năng điều tiết căng thẳng",
    "Hỏa": "tim mạch, huyết áp, thần kinh, giấc ngủ và độ hưng phấn tinh thần",
    "Thổ": "tỳ vị, tiêu hóa, chuyển hóa, cơ bắp và khả năng hấp thu",
    "Kim": "hô hấp, da, đại tràng và sức đề kháng bề mặt",
    "Thủy": "thận, tiết niệu, xương khớp, tai và sức bền nền",
}

ELEMENT_HEALTH_EXCESS = {
    "Mộc": "Mộc nổi bật thường làm khí vươn lên mạnh; khi mất cân bằng dễ biểu hiện thành căng gân cơ, nóng trong do uất, hoặc khó thả lỏng đầu óc.",
    "Hỏa": "Hỏa nổi bật làm tinh thần nhanh, phản ứng mạnh; khi quá đà cần giữ nhịp ngủ, huyết áp, tim mạch và trạng thái hồi hộp/nóng vội.",
    "Thổ": "Thổ nổi bật cho thấy tỳ vị và hệ tiêu hóa là điểm cần giữ; khi Thổ bí hoặc nặng dễ sinh cảm giác trì trệ, đầy nặng, tích lũy và khó chuyển hóa.",
    "Kim": "Kim nổi bật liên quan hô hấp, da và đại tràng; khi Kim căng dễ biểu hiện thành khô, cứng, nhạy với không khí lạnh/khô hoặc khó thả lỏng cơ thể.",
    "Thủy": "Thủy nổi bật làm khí lạnh, sâu và hướng vào bên trong; khi quá mạnh cần chú ý lạnh ẩm, thận khí, xương khớp và sức bền tinh thần.",
}

ELEMENT_HEALTH_WEAK = {
    "Mộc": "Mộc yếu thì khả năng sơ tiết và độ mềm của gân cơ cần được bồi dưỡng; nên tránh để stress dồn nén quá lâu.",
    "Hỏa": "Hỏa yếu thì dương khí, sự ấm áp và nhịp hưng phấn tinh thần cần được nâng đỡ; nên giữ vận động đều và tránh lạnh kéo dài.",
    "Thổ": "Thổ yếu thì tiêu hóa, hấp thu và nhịp ăn ngủ cần được ổn định trước; tránh ăn uống thất thường hoặc làm việc quá sức sau bữa ăn.",
    "Kim": "Kim yếu thì hô hấp, da và khả năng tạo ranh giới cơ thể cần được chăm; nên chú ý môi trường sống sạch, thoáng và nhịp thở.",
    "Thủy": "Thủy yếu thì thận khí, xương khớp, giấc ngủ sâu và sức bền nền cần được giữ; tránh thức khuya, hao sức kéo dài hoặc dùng quá nhiều kích thích.",
}

ELEMENT_GENERATES = {
    "Mộc": "Hỏa",
    "Hỏa": "Thổ",
    "Thổ": "Kim",
    "Kim": "Thủy",
    "Thủy": "Mộc",
}

ELEMENT_CONTROLS = {
    "Mộc": "Thổ",
    "Thổ": "Thủy",
    "Thủy": "Hỏa",
    "Hỏa": "Kim",
    "Kim": "Mộc",
}

CLIMATE_HEALTH_GUIDANCE = {
    "Hàn": "Khí Hàn làm bài toán sức khỏe nghiêng về giữ ấm, tránh lạnh ẩm và duy trì vận động để khí huyết lưu thông.",
    "Hàn thấp": "Khí Hàn thấp làm cơ thể dễ nặng, chậm và giữ ẩm; nên ưu tiên ấm, khô, vận động nhẹ đều và nếp ăn dễ tiêu.",
    "Ôn": "Khí Ôn tương đối dễ điều hòa, nhưng vẫn cần giữ nhịp ngủ nghỉ đều để không đẩy Hỏa hoặc Thổ lên quá mức.",
    "Táo": "Khí Táo cần chú ý phần khô: da, hô hấp, đại tràng và nhuận dưỡng cơ thể.",
    "Nhiệt": "Khí Nhiệt cần tiết chế nóng vội, rượu bia, thức khuya và các yếu tố làm tim mạch/thần kinh căng quá mức.",
}

WEALTH_TEN_GOD_READINGS = {
    "Chính Tài": "Chính Tài thiên về nguồn tiền ổn định, thu nhập có kế hoạch, khả năng giữ tài sản và trách nhiệm vật chất rõ.",
    "Thiên Tài": "Thiên Tài thiên về cơ hội linh hoạt, kinh doanh, quan hệ thị trường và khả năng xoay chuyển nguồn lực ngoài khuôn cố định.",
    "Thực Thần": "Thực Thần là năng lực tạo sản phẩm bền, nuôi nguồn thu bằng tay nghề, dịch vụ, chất lượng và uy tín lâu dài.",
    "Thương Quan": "Thương Quan giúp tiền đến qua biểu đạt, truyền thông, sáng tạo, bán ý tưởng hoặc cách làm khác biệt, nhưng cần kỷ luật để tránh phá khuôn quá mức.",
}

CAREER_TEN_GOD_READINGS = {
    "Chính Quan": "Chính Quan hợp môi trường có chuẩn mực, chức danh, quy trình, luật lệ hoặc vai trò quản trị trách nhiệm.",
    "Thất Sát": "Thất Sát hợp môi trường cạnh tranh, áp lực, xử lý rủi ro, mục tiêu cao và những việc cần bản lĩnh quyết đoán.",
    "Chính Ấn": "Chính Ấn hợp con đường học thuật, bằng cấp, chuyên môn, bảo trợ, hệ thống lớn và công việc cần uy tín nền tảng.",
    "Thiên Ấn": "Thiên Ấn hợp nghiên cứu sâu, tư duy khác biệt, tư vấn, huyền học/kỹ thuật chuyên biệt hoặc công việc cần trực giác phân tích.",
    "Thực Thần": "Thực Thần hợp tạo sản phẩm, vận hành dịch vụ, đào tạo, chăm sóc khách hàng và xây chất lượng bền.",
    "Thương Quan": "Thương Quan hợp truyền thông, sáng tạo, phản biện, cải tiến, bán hàng bằng nội dung hoặc những việc cần tiếng nói riêng.",
    "Chính Tài": "Chính Tài đưa nghề nghiệp về quản trị tiền, tài sản, vận hành, thương mại ổn định và kết quả đo được.",
    "Thiên Tài": "Thiên Tài đưa nghề nghiệp về kinh doanh linh hoạt, thị trường, môi giới, đầu tư hoặc kết nối nguồn lực.",
}

MARRIAGE_TEN_GOD_READINGS = {
    "Chính Tài": "với nam mệnh, Chính Tài thường đưa duyên hôn nhân về sự ổn định, trách nhiệm và khả năng cùng nhau vun vén đời sống thực tế. Người phù hợp không nhất thiết quá lãng mạn, nhưng biết giữ lời, coi trọng gia đình và có thể đồng hành trong những kế hoạch dài hạn",
    "Thiên Tài": "với nam mệnh, Thiên Tài làm duyên gặp gỡ linh hoạt hơn, thường mở qua giao tiếp, công việc, quan hệ xã hội hoặc môi trường có nhiều cơ hội. Sức hút đến khá tự nhiên, nhưng muốn đi đường dài thì cảm xúc cần được chuyển thành cam kết và một nhịp sống chung rõ ràng",
    "Chính Quan": "với nữ mệnh, Chính Quan thường hướng hình ảnh người bạn đời về sự chính danh, trách nhiệm, chuẩn mực và thái độ nghiêm túc với cam kết. Quan hệ dễ bền khi hai người tôn trọng vai trò của nhau, cùng thống nhất nguyên tắc sống mà không biến khuôn phép thành sự kiểm soát",
    "Thất Sát": "với nữ mệnh, Thất Sát làm tình cảm có sức hút mạnh, dễ gặp người quyết đoán hoặc mối quan hệ tạo nhiều chuyển động. Mặt tích cực là cùng nhau trưởng thành nhanh; mặt cần lưu ý là áp lực và cảm xúc mạnh phải được đặt trong ranh giới rõ để tình yêu không trở thành cuộc giằng co quyền lực",
}

PARTNERSHIP_TEN_GOD_READINGS = {
    "Tỷ Kiên": "Tỷ Kiên là người ngang vai, cùng chí hướng hoặc cùng năng lực; hợp để đồng hành khi mục tiêu rõ, nhưng dễ va cái tôi nếu quyền quyết định không minh bạch.",
    "Kiếp Tài": "Kiếp Tài là tín hiệu chia sẻ hoặc tranh nguồn lực; trong hợp tác làm ăn cần đặc biệt rõ vốn, lợi nhuận, quyền ký, trách nhiệm và đường lui.",
    "Chính Tài": "Chính Tài giúp hợp tác đi vào tiền thật, tài sản thật, kế hoạch thật; phù hợp quan hệ có sổ sách, cam kết và dòng tiền rõ.",
    "Thiên Tài": "Thiên Tài mở cơ hội qua quan hệ, thị trường, môi giới, đầu tư hoặc kinh doanh linh hoạt; hợp tác kiểu này cần kiểm soát rủi ro và kỳ vọng lợi nhuận.",
    "Chính Quan": "Chính Quan giúp hợp tác có hợp đồng, vai trò, chuẩn mực và kỷ luật vận hành; phù hợp mô hình cần pháp lý hoặc quy trình rõ.",
    "Thất Sát": "Thất Sát đưa vào áp lực cạnh tranh, tốc độ và rủi ro; hợp tác được khi có người kiểm soát rủi ro tốt, nhưng không nên mơ hồ về quyền lực.",
    "Chính Ấn": "Chính Ấn giúp hợp tác dựa trên uy tín, kiến thức, bằng cấp, hệ thống hoặc người bảo trợ; phù hợp làm dài hạn và cần niềm tin nền.",
    "Thiên Ấn": "Thiên Ấn hợp cộng sự có chuyên môn sâu, tư duy khác biệt hoặc năng lực nghiên cứu; cần thống nhất cách giao tiếp để tránh mỗi người đi một hướng.",
}

CHILDREN_TEN_GOD_READINGS = {
    "Thực Thần": "Thực Thần ở phần con cái cho thấy bản năng nuôi dưỡng khá tự nhiên: dễ quan tâm đến sự đủ đầy, sức khỏe và môi trường để con phát triển. Hậu vận cũng thuận hơn khi chủ mệnh biết bồi đắp từng bước, để thành quả lớn lên bằng sự đều đặn thay vì thúc ép kết quả sớm.",
    "Thương Quan": "Thương Quan làm phần con cái và hậu vận mang màu tự do, biểu đạt mạnh và không thích khuôn mẫu cứng. Con trẻ hoặc những dự án để đời có thể bộc lộ cá tính riêng rất sớm; cách đồng hành phù hợp là tôn trọng khác biệt nhưng vẫn thống nhất giới hạn, trách nhiệm và nề nếp căn bản.",
    "Chính Quan": "Chính Quan trong tín hiệu con cái/hậu vận cho thấy sự coi trọng kỷ luật, trách nhiệm và một con đường phát triển rõ ràng. Đây là nền tốt để dạy con biết tự quản, nhưng kỳ vọng nên vừa sức để nguyên tắc trở thành điểm tựa chứ không biến thành áp lực phải luôn hoàn hảo.",
    "Thất Sát": "Thất Sát khiến phần con cái/hậu vận có nhiều động lực cạnh tranh hoặc những giai đoạn thử thách buộc cả gia đình trưởng thành. Khi được dẫn bằng nguyên tắc bình tĩnh, khí này tạo bản lĩnh; nếu phản ứng bằng nóng giận hay áp đặt, nó lại dễ làm khoảng cách giữa cha mẹ và con cái lớn hơn.",
    "Chính Ấn": "Chính Ấn ở trụ giờ gợi một hậu vận đặt nặng học hỏi, sự bảo hộ và nền nếp. Con cái thường cần được nâng đỡ bằng tri thức và sự tin cậy; về lâu dài, chủ mệnh cũng dễ nhận lại niềm vui từ việc truyền kinh nghiệm, xây nền giáo dục hoặc để lại giá trị có tính kế thừa.",
    "Thiên Ấn": "Thiên Ấn ở trụ giờ cho thấy con cái, hậu vận hoặc dự án dài hạn có chiều sâu riêng, thiên về nghiên cứu, trực giác và lối đi khác số đông. Điều quan trọng là tạo không gian để năng lực đặc biệt ấy phát triển, đồng thời giữ kết nối thực tế để sự khác biệt không trở thành khép kín.",
}

PARENTS_TEN_GOD_READINGS = {
    "Chính Ấn": "Chính Ấn là nền bảo hộ, học hành, uy tín và sự nâng đỡ chính thống; khi hiện ở trụ tháng thường cho thấy gia đình hoặc môi trường trưởng thành coi trọng nền tảng.",
    "Thiên Ấn": "Thiên Ấn là nền nâng đỡ theo kiểu khác biệt, nghiên cứu, trực giác hoặc không theo khuôn thông thường; quan hệ gia đình có thể sâu nhưng khó nói bằng lời đơn giản.",
    "Chính Tài": "Chính Tài ở tầng bố mẹ/môi trường sớm nhấn mạnh trách nhiệm vật chất, nề nếp tài chính và bài học về sự thực tế.",
    "Thiên Tài": "Thiên Tài ở tầng bố mẹ/môi trường sớm nhấn mạnh quan hệ xã hội, xoay chuyển nguồn lực, cơ hội bên ngoài và tính linh hoạt của gia đình.",
    "Chính Quan": "Chính Quan ở tầng này làm nền gia đình nghiêng về quy củ, danh phận, kỷ luật và kỳ vọng rõ.",
    "Thất Sát": "Thất Sát ở tầng này cho thấy môi trường trưởng thành có áp lực, cạnh tranh hoặc yêu cầu bản lĩnh sớm; cần đọc như bài học rèn lực, không vội quy thành xấu.",
    "Tỷ Kiên": "Tỷ Kiên làm nền gia đình có yếu tố tự lập, ngang vai, anh em/bạn đồng trang lứa hoặc bài học giữ lập trường.",
    "Kiếp Tài": "Kiếp Tài làm nền gia đình có bài học về chia sẻ nguồn lực, cạnh tranh, phân vai và ranh giới vật chất.",
}

ANCESTRY_TEN_GOD_READINGS = {
    "Chính Ấn": "Chính Ấn ở trụ năm cho thấy gốc phúc thiên về học hành, uy tín, đạo lý hoặc nền nếp gia tộc.",
    "Thiên Ấn": "Thiên Ấn ở trụ năm làm gốc phúc có màu khác biệt, tâm linh, nghiên cứu, nghề đặc thù hoặc dòng suy nghĩ không theo số đông.",
    "Chính Quan": "Chính Quan ở trụ năm cho thấy nền gia tộc coi trọng danh phận, quy củ, phép tắc và trách nhiệm.",
    "Thất Sát": "Thất Sát ở trụ năm cho thấy nền sớm có khí cạnh tranh, áp lực hoặc thử thách; đời sau cần biến áp lực thành bản lĩnh thay vì mang thành nỗi sợ.",
    "Chính Tài": "Chính Tài ở trụ năm nói về nền thực tế, tài sản, trách nhiệm vật chất và bài học giữ gìn nguồn lực gia đình.",
    "Thiên Tài": "Thiên Tài ở trụ năm nói về quan hệ xã hội, cơ hội bên ngoài, khả năng xoay chuyển và dòng phúc đến qua kết nối.",
    "Thực Thần": "Thực Thần ở trụ năm cho thấy gốc phúc có mạch nuôi dưỡng, tay nghề, tạo thành quả và biết hưởng thụ lành mạnh.",
    "Thương Quan": "Thương Quan ở trụ năm cho thấy gốc phúc có khí biểu đạt, phá khuôn, khác biệt hoặc bài học về cách dùng tiếng nói riêng.",
    "Tỷ Kiên": "Tỷ Kiên ở trụ năm cho thấy khí tự lập, cạnh tranh ngang vai và truyền thống tự đứng bằng sức mình.",
    "Kiếp Tài": "Kiếp Tài ở trụ năm cho thấy gốc phúc có bài học về chia sẻ, tranh đoạt hoặc phân nguồn lực; đời sau cần minh bạch ranh giới.",
}

ELEMENT_SPACE_GUIDANCE = {
    "Mộc": "Mộc cần không gian có cây xanh vừa phải, sự thông thoáng, chất liệu tự nhiên và hướng phát triển mềm; tránh bừa bộn làm khí Mộc rối.",
    "Hỏa": "Hỏa cần ánh sáng, độ ấm, sinh khí, màu sắc có điểm nhấn và khu vực làm việc đủ sáng; tránh lạnh tối kéo dài làm giảm lực hành động.",
    "Thổ": "Thổ cần sự ổn định, vuông vức, sạch sẽ, điểm tựa chắc và nhịp sinh hoạt đều; tránh ẩm thấp, tù đọng hoặc chất quá nhiều đồ nặng.",
    "Kim": "Kim cần gọn, sạch, sáng, có trật tự, bề mặt rõ và ít nhiễu; tránh quá lạnh, quá sắc hoặc không gian làm người dùng thêm căng cứng.",
    "Thủy": "Thủy cần dòng lưu thông, sự mềm mại, thông tin luân chuyển và yếu tố nước dùng tiết chế; tránh ẩm lạnh, tối thấp hoặc để nước tù.",
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
    "marriage": "Hôn nhân bền khi hai người không chỉ có cảm xúc, mà còn cùng xây được cách trò chuyện, phân chia trách nhiệm và một nhịp sống khiến cả hai đều cảm thấy được tôn trọng.",
    "children": "Kế hoạch sinh con và nuôi dạy con nên được chuẩn bị trên cả ba nền sức khỏe, tài chính và nhịp sống gia đình; thời điểm thuận cần xét thêm Đại vận, Lưu niên thay vì chỉ dựa vào một tín hiệu đơn lẻ.",
    "parents": "Quan hệ với cha mẹ nên được nhìn như nền nâng đỡ và bài học gốc, tránh diễn giải một chiều thành tốt hoặc xấu tuyệt đối.",
    "siblings": "Quan hệ anh em/bạn đồng hành nên chú trọng ranh giới, vai trò và cách chia sẻ nguồn lực.",
    "ancestry": "Phần tổ tiên/gốc phúc nên được dùng như nền văn hóa gia đình để hiểu mình, không nên quy hết thành định mệnh.",
    "property": "Điền trạch tốt là nơi giúp người ở phục hồi, làm việc hiệu quả và giữ được nhịp sống lâu dài; hướng, bố cục và ngũ hành nên cùng phục vụ mục tiêu ấy thay vì chạy theo từng mẹo phong thủy rời rạc.",
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
            "dominant": _element_label_list(five_elements.get("dominant")),
            "missing": _element_label_list(five_elements.get("missing")),
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
                    "dominant": _element_label_list(five_elements.get("dominant")),
                    "missing": _element_label_list(five_elements.get("missing")),
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
            {"group": key, "title": value["title"], "count": len(_unique_texts([item.get("name") for item in value["items"] if isinstance(item, Mapping)]))}
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
    useful_god = _mapping(payload.get("useful_god"))
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
        "balance_axis": {
            "useful_elements": _useful_element_labels(useful_god),
            "unfavorable_elements": _unfavorable_element_labels(useful_god),
        },
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
        _chapter("day_master", "Nhật chủ", _day_master_chapter_paragraphs(payload, technical), ["bazi.day_master"]),
        _chapter("five_elements", "Ngũ hành", _five_elements_chapter_paragraphs(payload, technical), ["five_elements"]),
        _chapter(
            "strength_structure_useful_god",
            "Thân vượng, Mệnh cục và Dụng thần",
            _strength_structure_useful_god_paragraphs(payload, technical),
            ["strength", "pattern", "useful_god"],
        ),
        _chapter("ten_gods", "Thập thần", _ten_gods_chapter_paragraphs(payload, technical), ["ten_gods.four_layer"]),
        _chapter("shen_sha", "Thần sát", _shen_sha_chapter_paragraphs(payload, technical), ["shen_sha.grouped"]),
        _chapter("bone_weight", "Cân xương đoán mệnh", _bone_weight_paragraphs(payload), ["can_xuong"]),
        _chapter("palace_feng_shui", "Cung Phi và phương vị", _palace_feng_shui_paragraphs(payload), ["calendar.cung_phi", "calendar.nhom_trach", "five_elements", "useful_god"]),
        _chapter("life_domains", "9 mục đời sống", _life_domain_paragraphs(life_domains), ["customer_narrative.life_domains"]),
        _chapter(
            "luck_cycles",
            "Đại vận và lộ trình 5 năm",
            _luck_cycle_paragraphs(luck_cycles) + _annual_roadmap_paragraphs(payload),
            ["luck.current_cycle", "luck.cycles", "luck.annual_identity", "bazi", "useful_god"],
        ),
        _chapter("synthesis", "Kết luận tổng hợp", _synthesis_paragraphs(payload, narrative), ["bazi", "five_elements", "ten_gods", "shen_sha", "luck", "useful_god"]),
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
            _strength_summary(strength, pattern),
            ["strength"],
            existing.get("strength"),
        ),
        "structure": _technical_section(
            "Mệnh cục",
            _structure_summary(pattern),
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


def _strength_structure_useful_god_paragraphs(payload: Mapping[str, Any], technical: Mapping[str, Any]) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    five_elements = _mapping(payload.get("five_elements"))
    pattern = _mapping(payload.get("pattern"))
    useful = _mapping(payload.get("useful_god"))
    strength = _mapping(payload.get("strength"))
    strength_line = _section_summary(technical, "strength")
    structure_line = _section_summary(technical, "structure")
    useful_line = _section_summary(technical, "useful_god")
    paragraphs = _non_empty([strength_line, structure_line, useful_line])
    useful_display = _first_text(useful.get("useful_display"), useful.get("useful_stem"), useful.get("useful_element"))
    structure = _first_text(pattern.get("cach_cuc"), pattern.get("pattern"))
    strength_label = _strength_label(_first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")))
    day_element = _text(bazi.get("day_master_element"))
    counts = _mapping(five_elements.get("counts"))
    distribution = _element_distribution(counts)
    useful_elements = _useful_element_labels(useful)
    unfavorable = _unfavorable_element_labels(useful)

    if day_element or distribution:
        paragraphs.append(
            _fallback_join(
                f"Nhật chủ {day_element} đang đứng trong thế {strength_label or 'cân bằng riêng của lá số'}; sức của Nhật chủ chỉ hiện rõ khi đặt cạnh toàn bộ dòng khí xung quanh." if day_element else "",
                f"Bức tranh hiện có {distribution}." if distribution else "",
                _day_master_balance_axis(day_element),
                "Vì vậy, vượng hay nhược không đồng nghĩa với mạnh hay yếu trong tính cách; đó là cách nguồn lực bên trong được nâng đỡ, tiêu hao hoặc chịu áp lực trong hoàn cảnh thực tế.",
            )
        )
    if structure:
        paragraphs.append(
            _fallback_join(
                f"Mệnh cục {structure} giống như lối vận hành quen thuộc của lá số: cách chủ mệnh tiếp nhận hoàn cảnh, tạo giá trị và xử lý áp lực.",
                "Trụ tháng và nguyệt lệnh giữ vai trò lớn vì chúng phản ánh mùa khí, môi trường trưởng thành và nhịp nghề nghiệp đã định hình con người từ sớm.",
                "Từ nền này, nghề nghiệp, tài vận, hôn nhân và hợp tác mới được nối thành một câu chuyện thống nhất thay vì những nhận định rời nhau.",
            )
        )
    if useful_elements:
        paragraphs.append(
            "Dụng thần có thể hình dung như phần khí giúp toàn cục trở nên dễ vận hành hơn. Với lá số này, điểm cân bằng nằm ở "
            + ", ".join(useful_elements)
            + ". "
            + " ".join(_useful_element_application(element) for element in useful_elements if _useful_element_application(element))
        )
    if unfavorable:
        paragraphs.append(
            "Phần khí cần tiết chế là "
            + ", ".join(unfavorable)
            + ". "
            + " ".join(_unfavorable_element_caution(element) for element in unfavorable if _unfavorable_element_caution(element))
            + " Nếu công việc, quan hệ hoặc môi trường sống liên tục làm phần này mạnh thêm, chủ mệnh dễ hao sức hoặc phản ứng cực đoan; lúc đó điều cần thiết là giảm tải và lấy lại độ cân bằng, không phải lo sợ một nhãn tốt hay xấu."
        )
    if structure and useful_display:
        paragraphs.append(
            f"Nói ngắn gọn, Mệnh cục {structure} là cách chủ mệnh vận hành nguồn lực, còn {useful_display} là hướng giúp nguồn lực ấy đi đúng đường. Trước một lựa chọn lớn, câu hỏi hữu ích nhất là: quyết định này làm mình sáng rõ và cân bằng hơn, hay đang khuếch đại đúng điểm vốn dễ mất kiểm soát?"
        )
    return _unique_texts(paragraphs)


def _day_master_chapter_paragraphs(payload: Mapping[str, Any], technical: Mapping[str, Any]) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    strength = _mapping(payload.get("strength"))
    pattern = _mapping(payload.get("pattern"))
    useful = _mapping(payload.get("useful_god"))
    stem = _text(bazi.get("day_master"))
    element = _text(bazi.get("day_master_element"))
    yin_yang = _text(bazi.get("day_master_yin_yang"))
    strength_label = _strength_label(_first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")))
    useful_elements = _useful_element_labels(useful)
    paragraphs = _non_empty([_section_summary(technical, "day_master")])
    if stem or element:
        paragraphs.append(
            _fallback_join(
                f"Nhật chủ {stem}" if stem else "Nhật chủ",
                f"thuộc hành {element}" if element else "",
                f"tính {yin_yang}" if yin_yang else "",
                "là hình ảnh trung tâm của lá số, phản ánh cách một người cảm nhận bản thân và sử dụng năng lượng của mình. Các trụ còn lại cho biết nguồn lực nào đang nâng đỡ, nơi nào làm họ tiêu hao và hoàn cảnh nào buộc họ phải trưởng thành.",
            )
        )
    if element in ELEMENT_GENERATES:
        generated = ELEMENT_GENERATES[element]
        controls = ELEMENT_CONTROLS.get(element, "")
        controlled_by = _element_controlling(element)
        paragraphs.append(
            _fallback_join(
                "Theo quan hệ Ngũ hành, "
                + "; ".join(
                    part
                    for part in (
                        f"{element} sinh {generated}" if generated else "",
                        f"{element} khắc {controls}" if controls else "",
                        f"{element} chịu {controlled_by} khắc" if controlled_by else "",
                    )
                    if part
                )
                + ".",
                "Dòng sinh cho thấy cách năng lực được chuyển thành thành quả; dòng khắc nói về khả năng kiểm soát và áp lực. Khi ba chiều này cân nhau, chủ mệnh dễ quyết đoán mà không cứng, linh hoạt mà không mất phương hướng.",
            )
        )
    if strength_label:
        paragraphs.append(
            f"Ở thế {strength_label}, bài toán không nằm ở việc cố trở nên mạnh hơn, mà ở cách dùng lực cho đúng. Người có nền vượng cần một khuôn đủ tốt để sức mạnh thành kết quả; người có nền nhược lại phát triển bền hơn khi có chuyên môn, người đồng hành và môi trường đáng tin làm điểm tựa."
        )
    if useful_elements:
        paragraphs.append(
            "Dụng thần vì thế không phải một nhãn phong thủy, mà là lời chỉ dẫn về cách sống và lựa chọn môi trường. Lá số này thuận hơn khi ưu tiên "
            + ", ".join(useful_elements)
            + "."
        )
    return _unique_texts(paragraphs)


def _day_master_balance_axis(day_element: str) -> str:
    element = _element_label(day_element)
    if element not in ELEMENT_GENERATES:
        return ""
    resource = _element_generating(element)
    generated = ELEMENT_GENERATES.get(element, "")
    controls = ELEMENT_CONTROLS.get(element, "")
    controlled_by = _element_controlling(element)
    parts = _non_empty(
        [
            f"{resource} sinh {element} làm nguồn nâng Nhật chủ" if resource else "",
            f"{element} sinh {generated} là đường tiết khí/tạo sản phẩm" if generated else "",
            f"{element} khắc {controls} là đường kiểm soát/tài tinh" if controls else "",
            f"{controlled_by} khắc {element} là áp lực/kỷ luật tác động lên Nhật chủ" if controlled_by else "",
        ]
    )
    if not parts:
        return ""
    return "Trục cân bằng của Nhật chủ: " + "; ".join(parts) + "."


def _useful_element_application(element: str) -> str:
    label = _element_label(element)
    notes = {
        "Mộc": "Dùng Mộc là tăng học hỏi, kế hoạch dài hạn, khả năng phát triển và môi trường có sinh khí.",
        "Hỏa": "Dùng Hỏa là tăng ánh sáng, kỷ luật biểu hiện, thương hiệu, sự ấm áp và khả năng đưa năng lực ra ngoài.",
        "Thổ": "Dùng Thổ là tăng nền tảng, tính ổn định, tích lũy, đất đai, hệ thống và trách nhiệm đều đặn.",
        "Kim": "Dùng Kim là tăng trật tự, tài chính, quy trình, ranh giới, định giá và năng lực kiểm soát rủi ro.",
        "Thủy": "Dùng Thủy là tăng dòng chảy, giao tiếp, thị trường, thông tin, di chuyển và khả năng hồi phục.",
    }
    return notes.get(label, "")


def _unfavorable_element_caution(element: str) -> str:
    label = _element_label(element)
    notes = {
        "Mộc": "Mộc quá đà dễ thành phân tán, nóng phát triển, quyết định theo kỳ vọng hơn là nền lực thật.",
        "Hỏa": "Hỏa quá đà dễ thành vội, căng, háo thắng, đốt sức và làm quyết định lớn thiếu độ lùi.",
        "Thổ": "Thổ quá đà dễ thành nặng, ì, lo nhiều, tích áp lực và ôm trách nhiệm quá mức.",
        "Kim": "Kim quá đà dễ thành cứng, khô, quá kiểm soát, khó mềm trong quan hệ và dễ căng ở tài chính/quy trình.",
        "Thủy": "Thủy quá đà dễ thành trôi, do dự, nhiễu thông tin, thiếu điểm neo và khó giữ nhịp ổn định.",
    }
    return notes.get(label, "")


def _five_elements_chapter_paragraphs(payload: Mapping[str, Any], technical: Mapping[str, Any]) -> list[str]:
    five_elements = _mapping(payload.get("five_elements"))
    useful = _mapping(payload.get("useful_god"))
    counts = _mapping(five_elements.get("counts"))
    dominant = _element_label_list(five_elements.get("dominant")) or _element_extremes(counts, strongest=True)
    weak = _element_label_list(five_elements.get("missing")) or _element_extremes(counts, strongest=False)
    distribution = _element_distribution(counts)
    useful_elements = _useful_element_labels(useful)
    paragraphs = _non_empty([_section_summary(technical, "five_elements")])
    if distribution:
        paragraphs.append(
            "Ngũ hành tạo nên nhịp chuyển động bên trong lá số. Phân bố hiện tại là "
            + distribution
            + ". Hành nổi bật thường trở thành phản xạ tự nhiên, còn hành yếu là nơi con người dễ thiếu độ linh hoạt hoặc sức bền. Tuy nhiên, ý nghĩa cuối cùng vẫn phụ thuộc vào mùa sinh, thế Thân và vai trò điều tiết của Dụng thần."
        )
    if dominant:
        paragraphs.append(_element_group_meaning("Hành nổi bật", dominant, excess=True))
    if weak:
        paragraphs.append(_element_group_meaning("Hành yếu/thiếu", weak, excess=False))
    paragraphs.extend(_five_element_relation_paragraphs(counts, dominant, weak))
    if useful_elements:
        paragraphs.append(
            "Không nên thấy thiếu hành nào rồi bổ hành ấy một cách máy móc. Điều lá số thực sự cần ưu tiên là "
            + ", ".join(useful_elements)
            + ", bởi đây là phần giúp toàn cục chuyển động hài hòa hơn, chứ không đơn thuần là bù vào một con số đang thấp."
        )
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


def _element_group_meaning(prefix: str, elements: Sequence[str], *, excess: bool) -> str:
    notes = []
    for element in elements:
        notes.append(_element_character_note(element, excess=excess))
    return prefix + ": " + ", ".join(elements) + ". " + " ".join(note for note in notes if note)


def _element_character_note(element: str, *, excess: bool) -> str:
    element = _element_label(element)
    if element == "Mộc":
        return "Mộc nổi thì khí phát triển, học hỏi và mở rộng mạnh; Mộc yếu thì cần bồi khả năng linh hoạt, định hướng và sức vươn."
    if element == "Hỏa":
        return "Hỏa nổi thì biểu hiện, tốc độ và sự hiện diện mạnh; Hỏa yếu thì cần bồi động lực, ánh sáng, niềm vui và khả năng đưa mình ra ngoài."
    if element == "Thổ":
        return "Thổ nổi thì tính ổn định, tích lũy và trách nhiệm mạnh; Thổ yếu thì cần bồi nền tảng, nhịp sinh hoạt và khả năng giữ trung tâm."
    if element == "Kim":
        return "Kim nổi thì kỷ luật, định giá, trật tự và khả năng cắt lọc mạnh; Kim yếu thì cần bồi nguyên tắc, ranh giới và năng lực ra quyết định rõ."
    if element == "Thủy":
        return "Thủy nổi thì dòng chảy, giao tiếp, thị trường và khả năng thích nghi mạnh; Thủy yếu thì cần bồi sự mềm mại, hồi phục, thông tin và khả năng luân chuyển."
    return ""


def _five_element_relation_paragraphs(
    counts: Mapping[str, Any],
    dominant: Sequence[str],
    weak: Sequence[str],
) -> list[str]:
    paragraphs: list[str] = []
    dominant_set = {_element_label(element) for element in dominant}
    weak_set = {_element_label(element) for element in weak}
    count_values = {_element_label(label): _element_count(counts, label) for label in ELEMENT_HEALTH_AREAS}
    for source, target in ELEMENT_GENERATES.items():
        if source in dominant_set and count_values.get(target, 0) >= 2:
            paragraphs.append(
                f"Quan hệ sinh đáng chú ý: {source} vượng sinh {target}. Điều này cho thấy khí {target} không chỉ nhìn ở số lượng riêng, mà còn được {source} đẩy thêm; khi luận nghề nghiệp, tài vận, sức khỏe hay phong thủy cần tính cả dòng sinh này."
            )
    for source, target in ELEMENT_CONTROLS.items():
        if count_values.get(source, 0) >= 3 and (target in weak_set or count_values.get(target, 0) <= 1):
            paragraphs.append(
                f"Quan hệ khắc cần lưu ý: {source} mạnh khắc {target}. Khi {target} đã yếu, phần này dễ thành điểm mất cân bằng; các quyết định lớn nên tránh làm {source} quá nặng hoặc tiếp tục rút lực của {target}."
            )
    return paragraphs


def _ten_gods_chapter_paragraphs(payload: Mapping[str, Any], technical: Mapping[str, Any]) -> list[str]:
    ten_layers = build_ten_gods_four_layer_view(payload)
    paragraphs = _non_empty([_section_summary(technical, "ten_gods")])
    for layer in _list(ten_layers.get("layers")):
        if not isinstance(layer, Mapping):
            continue
        label = _first_text(layer.get("label"), layer.get("pillar"))
        god = _text(layer.get("primary_ten_god"))
        can_chi = _text(layer.get("can_chi"))
        meaning = _ten_god_meaning(god)
        life_hint = _text(layer.get("life_hint")).rstrip(".")
        if god:
            paragraphs.append(
                _fallback_join(
                    f"Ở trụ {label} {can_chi}, khí {god} hiện khá rõ." if can_chi else f"Ở trụ {label}, khí {god} hiện khá rõ.",
                    f"Vị trí này gắn với {life_hint.lower()}." if life_hint else "",
                    f"Trong đời sống, nó thường biểu hiện qua {meaning}." if meaning else "",
                )
            )
    paragraphs.extend(_ten_god_pattern_synthesis(ten_layers))
    return _unique_texts(paragraphs)


def _ten_god_pattern_synthesis(ten_layers: Mapping[str, Any]) -> list[str]:
    paragraphs: list[str] = []
    officer = _ten_god_signal_labels(ten_layers, ("Chính Quan", "Thất Sát"))
    resource = _ten_god_signal_labels(ten_layers, ("Chính Ấn", "Thiên Ấn"))
    output = _ten_god_signal_labels(ten_layers, ("Thực Thần", "Thương Quan"))
    wealth = _ten_god_signal_labels(ten_layers, ("Chính Tài", "Thiên Tài"))
    peers = _ten_god_signal_labels(ten_layers, ("Tỷ Kiên", "Kiếp Tài"))
    if officer:
        paragraphs.append(
            "Quan/Sát đưa trách nhiệm, chuẩn mực và áp lực thành một chủ đề lớn. Khi được nâng bằng chuyên môn và kỷ luật, áp lực trở thành động lực để có vị trí; khi thiếu nền, cùng nguồn lực ấy lại dễ biến thành căng thẳng và cảm giác luôn phải chứng minh mình."
        )
    if resource:
        paragraphs.append(
            "Ấn tinh tạo nền học hỏi, uy tín và khả năng nhận sự nâng đỡ đúng lúc. Khi đi cùng Quan/Sát, con đường phát triển thường bền hơn nếu dựa trên chuyên môn, bằng cấp, quy chuẩn hoặc một hệ thống đủ tin cậy thay vì chỉ dùng ý chí cá nhân."
        )
    if output:
        paragraphs.append(
            "Thực Thần và Thương Quan là con đường đưa năng lực bên trong thành sản phẩm, lời nói và giá trị người khác có thể cảm nhận. Khi dòng này thông, tài vận và nghề nghiệp có đầu ra; khi bị nghẽn, nhiều ý tưởng vẫn có thể nằm lại ở tiềm năng."
        )
    if wealth:
        paragraphs.append(
            "Tài tinh phản ánh quan hệ với tiền bạc, tài sản và trách nhiệm vật chất. Có người giỏi tạo tiền nhưng khó giữ, có người tích lũy tốt nhưng chậm mở cơ hội; vì vậy kiếm tiền, giữ tiền và dùng tiền cần được nhìn như ba năng lực khác nhau."
        )
    if peers:
        paragraphs.append(
            "Tỷ Kiên và Kiếp Tài làm nổi bật tính tự chủ, quan hệ ngang vai và bài học chia sẻ nguồn lực. Chủ mệnh có thể thu hút người cùng chí hướng, nhưng hợp tác chỉ bền khi vai trò, quyền quyết định và lợi ích được nói rõ ngay từ đầu."
        )
    return paragraphs


def _shen_sha_chapter_paragraphs(payload: Mapping[str, Any], technical: Mapping[str, Any]) -> list[str]:
    grouped = build_shen_sha_grouped_view(payload)
    paragraphs = _non_empty([_section_summary(technical, "shen_sha")])
    groups = _mapping(grouped.get("groups"))
    group_guidance = {
        "noble_support": "Quý nhân không làm thay phần việc của chủ mệnh, nhưng thường mở ra một người chỉ đường, một cơ hội hóa giải hoặc một lối đi xuất hiện đúng lúc. Sự trợ lực này rõ nhất khi bản thân đã chuẩn bị đủ năng lực để đón nhận.",
        "relationship": "Duyên tinh làm tăng sức hút và cơ hội gặp gỡ, đồng thời đem đến bài học về cảm xúc và ranh giới. Muốn hiểu duyên có đi được đường dài hay không vẫn phải trở về trụ ngày và cách hai người xây đời sống chung.",
        "authority": "Quyền tinh và tài danh mở khả năng được nhìn nhận qua học hành, uy tín hoặc vị trí. Danh chỉ bền khi đi cùng năng lực thật, nên càng có tín hiệu này càng cần giữ kỷ luật và chất lượng công việc.",
        "caution": "Nhóm cảnh báo nhắc chủ mệnh chuẩn bị trước cho những điểm dễ va chạm về an toàn, sức khỏe, gia đạo hoặc cảm xúc. Biết trước không phải để lo sợ, mà để có ranh giới và phương án xử lý bình tĩnh hơn.",
        "later_life": "Nhóm hậu vận và dịch chuyển gợi những lần đổi môi trường, đi xa hoặc thay đổi chiều sâu tinh thần. Đại vận sẽ cho biết khi nào nhu cầu chuyển mình ấy trở nên rõ và nên được biến thành hành động.",
    }
    for key, guidance in group_guidance.items():
        group = _mapping(groups.get(key))
        items = [item for item in _list(group.get("items")) if isinstance(item, Mapping)]
        if not items:
            continue
        names = _unique_texts([item.get("name") for item in items if _text(item.get("name"))])
        title = _first_text(group.get("title"), key)
        paragraphs.append(f"{title}: {', '.join(names)}. {guidance}")
    if len(paragraphs) == 1:
        paragraphs.append("Thần sát trong lá số này không tạo thành một chủ đề đủ mạnh để dẫn dắt toàn bộ câu chuyện. Đây là tín hiệu nền, chỉ phát huy ý nghĩa khi đặt cạnh Tứ trụ, Ngũ hành, Mệnh cục và đúng thời điểm Đại vận.")
    else:
        paragraphs.append("Thần sát nên được xem như những dấu nhấn nhỏ: sao thuận chỉ nơi dễ nhận trợ lực, sao cảnh báo nhắc nơi cần chuẩn bị. Không một sao đơn lẻ nào đủ quyền quyết định toàn bộ vận mệnh của một người.")
    return _unique_texts(paragraphs)


def _bone_weight_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    can_xuong = _mapping(payload.get("can_xuong"))
    weight = _first_text(can_xuong.get("display_weight"), can_xuong.get("weight"), can_xuong.get("weight_label"))
    classification = _first_text(can_xuong.get("classification"), can_xuong.get("grade"), can_xuong.get("category"))
    summary = _first_text(can_xuong.get("summary"), can_xuong.get("interpretation"), can_xuong.get("description"))
    paragraphs: list[str] = []
    if weight or classification:
        paragraphs.append(
            _fallback_join(
                f"Cân xương ghi nhận {weight}." if weight else "",
                f"Xếp loại {classification}." if classification else "",
                "Chỉ số này gợi nhịp tích lũy của cuộc đời: có người thuận nền sớm, có người phải gây dựng từng bước rồi mới vững. Đây là lớp tham khảo bổ trợ, không phải chiếc khuôn đóng cứng số phận.",
            )
        )
    if summary:
        paragraphs.append(summary)
    if classification:
        paragraphs.append(_bone_weight_guidance(classification))
    if paragraphs:
        paragraphs.append(
            "Giá trị của Cân xương nằm ở việc bổ sung sắc thái cho toàn cục. Nền thuận vẫn cần kỷ luật mới thành thành quả; nền phải gây dựng nhiều hơn vẫn có thể chuyển biến rõ khi chủ mệnh chọn đúng nghề, đúng môi trường và biết tận dụng những chặng vận nâng mình."
        )
    return _unique_texts(paragraphs)


def _bone_weight_guidance(classification: str) -> str:
    text = _text(classification)
    if "Thượng" in text:
        return "Nhóm Thượng cách nên được hiểu là nền có khả năng tích lũy và mở vận tốt khi biết đi đúng thời. Điểm cần giữ là không chủ quan, vì phúc khí chỉ phát huy khi hành động có phương pháp."
    if "Trung" in text:
        return "Nhóm Trung cách thiên về tích lũy theo thời gian: không nên kỳ vọng đột biến quá sớm, nhưng nếu chọn đúng nghề, đúng người và đúng nhịp vận thì vẫn có đường bền."
    if "Hạ" in text:
        return "Nhóm Hạ cách cần nhấn mạnh chiến lược bồi nền: giữ sức, giữ tiền, học kỹ một nghề, chọn môi trường ít hao tổn và tránh quyết định lớn khi vận chưa nâng."
    return "Xếp loại Cân xương nên được đọc cùng bối cảnh toàn lá số để tránh biến một chỉ số phụ thành kết luận cứng."


def _palace_feng_shui_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    calendar = _mapping(payload.get("calendar"))
    five_elements = _mapping(payload.get("five_elements"))
    useful = _mapping(payload.get("useful_god"))
    counts = _mapping(five_elements.get("counts"))
    cung_phi = _first_text(calendar.get("cung_phi"), calendar.get("menh_quai"), calendar.get("gua_name"))
    house_group = _first_text(calendar.get("nhom_trach"), calendar.get("house_group"))
    palace_element = _first_text(calendar.get("hanh_cung"), calendar.get("cung_phi_element"), calendar.get("gua_element"))
    directions = _house_group_directions(house_group)
    useful_elements = _useful_element_labels(useful)
    unfavorable = _unfavorable_element_labels(useful)
    dominant = _element_label_list(five_elements.get("dominant")) or _element_extremes(counts, strongest=True)
    weak = _element_label_list(five_elements.get("missing")) or _element_extremes(counts, strongest=False)
    paragraphs: list[str] = []

    paragraphs.append(
        _fallback_join(
            f"Cung Phi/Mệnh quái của lá số là {cung_phi}." if cung_phi else "",
            f"Hành cung: {palace_element}." if palace_element else "",
            f"Nhóm trạch: {house_group}." if house_group else "",
            "Cung Phi đưa phần luận từ con người sang không gian: nơi ở, nơi làm việc, bếp, cửa và cách tổ chức mặt bằng. Nó không thay thế Tứ trụ, nhưng giúp những kết luận về khí mệnh trở thành lựa chọn có thể áp dụng trong đời sống hằng ngày.",
        )
    )
    if directions:
        paragraphs.append(
            f"Với {house_group}, nhóm phương vị nên ưu tiên tham khảo là {directions}. Khi tư vấn thực tế cần đọc theo mục tiêu sử dụng: nhà ở cần ổn định sức khỏe và gia đạo, văn phòng cần nâng hiệu suất và quan hệ, cửa hàng/kho bãi cần hỗ trợ dòng khách, dòng tiền và khả năng kiểm soát rủi ro."
        )
    if useful_elements or unfavorable:
        paragraphs.append(
            _fallback_join(
                f"Trục Dụng thần nên nâng trong không gian: {', '.join(useful_elements)}." if useful_elements else "",
                f"Nhóm Kỵ thần cần tiết chế khi bố trí: {', '.join(unfavorable)}." if unfavorable else "",
                "Phong thủy phù hợp vì thế không nằm ở một hướng tốt hay xấu duy nhất. Hướng, ánh sáng, vật liệu, màu sắc, độ thoáng và thói quen sử dụng cần cùng tạo ra một không gian khiến người ở khỏe hơn, sáng hơn và làm việc ổn định hơn.",
            )
        )
    if palace_element:
        paragraphs.append(
            _fallback_join(
                f"Hành cung {palace_element} cho biết khí không gian hợp mệnh quái nghiêng về {palace_element}.",
                ELEMENT_SPACE_GUIDANCE.get(_element_label(palace_element), ""),
                "Nếu hành cung trùng với hành đang quá vượng trong lá số thì không nên kích thêm quá mạnh; nếu hành cung nâng được Dụng thần thì có thể dùng làm điểm tựa khi chọn nơi ở và nơi làm việc.",
            )
        )
    if dominant or weak:
        paragraphs.append(
            _fallback_join(
                f"Ngũ hành nổi bật của lá số: {', '.join(dominant)}." if dominant else "",
                f"Ngũ hành yếu/thiếu: {', '.join(weak)}." if weak else "",
                "Khi bố trí không gian, hành nổi bật là khí sẵn có cần tiết chế đúng mức, còn hành yếu/thiếu chỉ nên bồi vừa phải và bền, không dùng đồ vật hay màu sắc cực đoan để ép mệnh.",
            )
        )
    paragraphs.append(
        "Những phương vị trên là nền tham khảo cho bước tư vấn phong thủy sâu hơn. Với một ngôi nhà cụ thể, vẫn cần nhìn hiện trạng cửa, bếp, phòng ngủ, bàn làm việc, dòng di chuyển và mục tiêu của gia chủ để phương án vừa hợp khí vừa thực sự sống được."
    )
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


def _overview_paragraphs(payload: Mapping[str, Any], narrative: Mapping[str, Any]) -> list[str]:
    overview = _mapping(narrative.get("overview"))
    headline = _first_text(overview.get("headline"), overview.get("summary"), overview.get("title"))
    bazi = _mapping(payload.get("bazi"))
    strength = _mapping(payload.get("strength"))
    pattern = _mapping(payload.get("pattern"))
    useful = _mapping(payload.get("useful_god"))
    day_master = _day_master_summary(bazi).rstrip(".")
    strength_label = _strength_label(_first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")))
    structure = _first_text(pattern.get("cach_cuc"), pattern.get("pattern"))
    useful_display = _first_text(useful.get("useful_display"), useful.get("useful_stem"), useful.get("useful_element"))
    summary = _fallback_join(
        "Bức tranh chính của lá số bắt đầu từ Nhật chủ, được định hình bởi thế Thân và Mệnh cục, rồi tìm điểm cân bằng qua Dụng thần.",
        f"Cốt khí là {day_master}." if day_master else "",
        f"Nguồn lực đang ở thế {strength_label}." if strength_label else "",
        f"Lối vận hành nổi bật mang Mệnh cục {structure}." if structure else "",
        f"Điểm mở để điều hòa toàn cục là {useful_display}." if useful_display else "",
    )
    method_note = (
        "Bốn trụ kể câu chuyện từ gốc gia đình đến hậu vận; Ngũ hành cho thấy dòng khí mạnh yếu; Thập thần chuyển dòng khí ấy thành vai trò đời sống; còn Đại vận đặt tất cả vào từng chặng thời gian cụ thể."
    )
    module_note = (
        "Từ nền này, các phần nghề nghiệp, tài vận, hôn nhân, hợp tác, phong thủy và sinh con được nối với nhau. Mỗi kết luận vì thế không đứng riêng lẻ, mà cùng phản ánh một con người trong nhiều hoàn cảnh khác nhau."
    )
    return _non_empty([headline, summary, method_note, module_note])


def _four_pillars_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    ten_layers = build_ten_gods_four_layer_view(payload)
    paragraphs: list[str] = _non_empty([_month_calendar_note(payload)])
    for key, label in PILLAR_LABELS.items():
        pillar = _mapping(bazi.get(f"{key}_pillar"))
        can_chi = _pillar_can_chi(pillar)
        if not can_chi:
            continue
        ten_god = _text(pillar.get("ten_god"))
        nap_am = _text(pillar.get("nap_am"))
        truong_sinh = _text(pillar.get("truong_sinh"))
        layer = _pillar_layer(ten_layers, key)
        hidden_gods = _hidden_ten_god_labels(layer)
        data_parts = _non_empty(
            [
                f"Can chi {can_chi}",
                f"thập thần {ten_god}" if ten_god else "",
                f"nạp âm {nap_am}" if nap_am else "",
                f"vòng trường sinh {truong_sinh}" if truong_sinh else "",
                f"tàng can/thập thần ẩn {', '.join(hidden_gods)}" if hidden_gods else "",
            ]
        )
        meaning = _ten_god_meaning(ten_god)
        life_hint = PILLAR_LIFE_HINTS[key].rstrip(".")
        paragraphs.append(
            f"Trụ {label}: "
            + "; ".join(data_parts)
            + f". Trong đời sống, vị trí này gắn với {life_hint.lower()}."
            + (f" Sự hiện diện của {ten_god} thường biểu lộ qua {meaning}." if ten_god and meaning else "")
            + _pillar_extra_guidance(key, ten_god, hidden_gods)
        )
    paragraphs.extend(_branch_relationship_paragraphs(payload))
    paragraphs.append(_four_pillar_synthesis(payload, ten_layers))
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


def _pillar_branch(pillar: Mapping[str, Any]) -> str:
    branch = _text(pillar.get("branch"))
    if branch:
        return branch
    can_chi = _pillar_can_chi(pillar)
    parts = can_chi.split()
    return parts[-1] if len(parts) >= 2 else ""


def _branch_relationship_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    branches: dict[str, str] = {}
    for key, label in PILLAR_LABELS.items():
        branch = _pillar_branch(_mapping(bazi.get(f"{key}_pillar")))
        if branch:
            branches[label] = branch
    if len(branches) < 2:
        return []
    present = set(branches.values())
    combination_notes: list[str] = []
    for group, element in BRANCH_THREE_COMBINATIONS:
        hits = [branch for branch in group if branch in present]
        if len(hits) == 3:
            combination_notes.append(f"tam hợp {'-'.join(group)} hóa khí {element}")
        elif len(hits) == 2:
            combination_notes.append(f"bán hợp {'-'.join(hits)} nghiêng khí {element}")
    clash_notes: list[str] = []
    for left, right in BRANCH_SIX_CLASHES:
        if left in present and right in present:
            left_places = [label for label, branch in branches.items() if branch == left]
            right_places = [label for label, branch in branches.items() if branch == right]
            place = " / ".join(_non_empty([", ".join(left_places), ", ".join(right_places)]))
            clash_notes.append(f"{left}-{right} xung" + (f" tại {place}" if place else ""))
    if not combination_notes and not clash_notes:
        return []
    paragraphs: list[str] = []
    if combination_notes:
        paragraphs.append(
            "Quan hệ Địa chi có tín hiệu hợp: "
            + "; ".join(combination_notes)
            + ". Hợp khí cho biết các trụ có xu hướng kéo về cùng một dòng năng lượng; khi gặp vận kích hoạt đúng chi còn thiếu, dòng khí này thường biểu hiện rõ hơn trong nghề nghiệp, quan hệ hoặc sức khỏe."
        )
    if clash_notes:
        paragraphs.append(
            "Quan hệ Địa chi có tín hiệu xung: "
            + "; ".join(clash_notes)
            + ". Xung không mặc định là xấu, nhưng cho biết nơi dễ có va chạm, thay đổi, di chuyển hoặc áp lực cần xử lý; khi luận hôn nhân, sức khỏe và vận hạn phải đọc kỹ vị trí trụ bị xung."
        )
    return paragraphs


def _hidden_ten_god_labels(layer: Mapping[str, Any]) -> list[str]:
    labels: list[str] = []
    for item in _list(layer.get("hidden")):
        if isinstance(item, Mapping):
            labels.append(_text(item.get("ten_god")))
    return _unique_texts(labels)


def _pillar_extra_guidance(key: str, ten_god: str, hidden_gods: Sequence[str]) -> str:
    parts: list[str] = []
    if hidden_gods:
        parts.append(
            " Tàng can cho biết phần khí nằm dưới bề mặt: "
            + ", ".join(hidden_gods)
            + ". Khi luận thực tế, phần ẩn này thường biểu hiện thành động cơ bên trong hoặc điều kiện chỉ lộ rõ khi gặp vận kích hoạt."
        )
    if key == "month":
        parts.append(" Vì trụ tháng giữ nhịp nghề nghiệp và môi trường trưởng thành, đây là trụ cần đọc kỹ khi chọn nghề, chọn tổ chức hoặc đánh giá nền gia đình.")
    elif key == "day":
        parts.append(" Vì trụ ngày là bản thân và phối ngẫu, mọi luận hôn nhân/quan hệ gần phải quay lại cách trụ này đứng trong toàn cục.")
    elif key == "hour":
        parts.append(" Vì trụ giờ là con cái, hậu vận và dự án dài hạn, tín hiệu ở đây thường cần Đại vận hỗ trợ mới phát rõ.")
    elif key == "year":
        parts.append(" Vì trụ năm là gốc phúc và môi trường sớm, nó cho biết khí nền ban đầu hơn là kết luận cố định về cả đời.")
    return "".join(parts)


def _four_pillar_synthesis(payload: Mapping[str, Any], ten_layers: Mapping[str, Any]) -> str:
    bazi = _mapping(payload.get("bazi"))
    year = _pillar_can_chi(_mapping(bazi.get("year_pillar")))
    month = _pillar_can_chi(_mapping(bazi.get("month_pillar")))
    day = _pillar_can_chi(_mapping(bazi.get("day_pillar")))
    hour = _pillar_can_chi(_mapping(bazi.get("hour_pillar")))
    month_god = _text(_pillar_layer(ten_layers, "month").get("primary_ten_god"))
    day_god = _text(_pillar_layer(ten_layers, "day").get("primary_ten_god"))
    hour_god = _text(_pillar_layer(ten_layers, "hour").get("primary_ten_god"))
    parts = _non_empty(
        [
            f"trụ năm {year} là gốc nền" if year else "",
            f"trụ tháng {month}" + (f" với {month_god}" if month_god else "") + " là nhịp nghề nghiệp/môi trường chính" if month else "",
            f"trụ ngày {day}" + (f" với {day_god}" if day_god else "") + " là lõi bản thân và quan hệ gần" if day else "",
            f"trụ giờ {hour}" + (f" với {hour_god}" if hour_god else "") + " là hậu vận, con cái và thành quả dài hạn" if hour else "",
        ]
    )
    return "Khi nối bốn trụ thành một hành trình, " + "; ".join(parts) + ". Mỗi trụ giữ một vai trò, nhưng chỉ khi đặt cạnh nhau mới thấy được cách quá khứ, hiện tại và hậu vận ảnh hưởng qua lại."


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
            paragraphs.extend(
                f"{title} - {_life_domain_subtitle(item, index)}: {item}"
                for index, item in enumerate(detailed)
            )
            continue
        summary = _text(section.get("summary"))
        if summary:
            paragraphs.append(f"{title}: {summary}")
    return paragraphs


def _luck_cycle_paragraphs(luck_cycles: Mapping[str, Any]) -> list[str]:
    paragraphs: list[str] = []
    direction = _first_text(luck_cycles.get("direction_label"), luck_cycles.get("direction"))
    start_age = luck_cycles.get("start_age")
    axis = _mapping(luck_cycles.get("balance_axis"))
    useful_elements = _text_list(axis.get("useful_elements"))
    unfavorable_elements = _text_list(axis.get("unfavorable_elements"))
    if direction or start_age is not None:
        paragraphs.append(
            "Mệnh cục giống như nền năng lực và khí chất đi theo một người, còn Đại vận cho biết nền ấy gặp thời tiết nào trong từng chặng đời. Có giai đoạn sở trường được nâng đỡ nên làm việc thuận tay hơn; cũng có giai đoạn buộc phải đổi cách đi, thu hẹp để tích lực hoặc trưởng thành qua áp lực. "
            + "Lá số này đi theo "
            + _first_text(direction, "chiều vận đã tính")
            + (f", khởi vận khoảng {start_age} tuổi." if start_age is not None else ".")
        )
    if useful_elements or unfavorable_elements:
        paragraphs.append(
            _fallback_join(
                f"Trục nên dùng khi đọc vận: {', '.join(useful_elements)}." if useful_elements else "",
                f"Nhóm cần tiết chế khi vào vận: {', '.join(unfavorable_elements)}." if unfavorable_elements else "",
                "Bởi vậy, một Đại vận thuận không đơn giản là can chi nghe đẹp, mà là giai đoạn giúp Dụng thần có đất phát huy, đồng thời không đẩy điểm mất cân bằng của lá số lên quá mức.",
            )
        )
    current = _mapping(luck_cycles.get("current_cycle"))
    current_summary = _text(current.get("summary"))
    if current_summary:
        current_age = _age_range(current)
        current_years = _year_range(current)
        context = _fallback_join(current_age, current_years)
        guidance = _luck_cycle_guidance(current, useful_elements, unfavorable_elements)
        paragraphs.append(
            "Vận hiện tại "
            + (f"({context}) " if context else "")
            + current_summary
            + ". "
            + guidance
        )
    cycles = [item for item in _list(luck_cycles.get("cycles")) if isinstance(item, Mapping)]
    for item in cycles[:6]:
        age = _age_range(item)
        years = _year_range(item)
        summary = _text(item.get("summary"))
        if summary:
            prefix = " · ".join(part for part in (age, years) if part)
            guidance = _luck_cycle_guidance(item, useful_elements, unfavorable_elements)
            paragraphs.append((prefix + ": " if prefix else "") + summary + ". " + guidance)
    return paragraphs


def _life_domain_subtitle(paragraph: str, index: int) -> str:
    text = _text(paragraph)
    lowered = text.lower()
    explicit = text.split(":", 1)[0].strip() if ":" in text else ""
    if explicit and len(explicit) <= 48:
        return explicit
    if lowered.startswith("trục điều tiết của lá số"):
        return "Dụng thần ứng dụng"
    rules = (
        (("đại vận", "lưu niên", "thời điểm"), "Thời điểm và vận khí"),
        (("cung phi", "mệnh quái", "nhóm trạch", "hướng "), "Phương vị và không gian"),
        (("ngũ hành", "hành nổi bật", "hành còn yếu", "hành còn thiếu"), "Cân bằng Ngũ hành"),
        (("tài tinh", "dòng tiền", "thanh khoản", "tài vận"), "Tài khí và dòng tiền"),
        (("trụ tháng", "nghề nghiệp", "chuyên môn"), "Nền nghề nghiệp"),
        (("trụ ngày", "phối ngẫu", "hôn nhân"), "Nền hôn nhân"),
        (("trụ giờ", "tử tức", "con cái", "hậu vận"), "Nền con cái và hậu vận"),
        (("trụ năm", "gia tộc", "gốc phúc"), "Nền gia tộc"),
        (("thập thần", "chính quan", "thất sát", "ấn tinh", "thực thần", "thương quan"), "Tín hiệu Thập thần"),
        (("điểm cần", "nên ", "ưu tiên", "không nên"), "Định hướng ứng dụng"),
    )
    for keywords, subtitle in rules:
        if any(keyword in lowered for keyword in keywords):
            return subtitle
    return "Luận điểm chính" if index == 0 else f"Góc nhìn bổ sung {index}"


def _luck_cycle_guidance(
    cycle: Mapping[str, Any],
    useful_elements: Sequence[str],
    unfavorable_elements: Sequence[str],
) -> str:
    elements = _unique_texts(
        [
            _extract_element_label(cycle.get("stem_element")),
            _extract_element_label(cycle.get("branch_element")),
        ]
    )
    useful_hits = [element for element in elements if element in useful_elements]
    unfavorable_hits = [element for element in elements if element in unfavorable_elements]
    action = _luck_element_action(elements)
    if useful_hits and unfavorable_hits:
        return (
            f"Đây là chặng vận có cả cơ hội lẫn phép thử: {', '.join(useful_hits)} nâng phần nên dùng, trong khi {', '.join(unfavorable_hits)} đồng thời làm điểm cần tiết chế rõ hơn. Chủ mệnh vẫn có thể mở việc và tiến lên, nhưng thành quả bền hay không phụ thuộc vào kế hoạch, khả năng kiểm soát rủi ro và việc giữ nhịp sống không bị cuốn theo tham vọng ngắn hạn. "
            + action
        )
    if useful_hits:
        return (
            f"Vận này đưa {', '.join(useful_hits)} vào đúng trục cần dùng, nên chủ mệnh thường cảm thấy năng lực có nơi để phát huy và quyết định dễ đi vào kết quả hơn. Cơ hội sẽ rõ nhất khi chủ động chọn đúng công việc, cộng sự và môi trường, thay vì chỉ chờ vận may tự đến. "
            + action
        )
    if unfavorable_hits:
        return (
            f"Vận này làm {', '.join(unfavorable_hits)} nổi lên, nên những thói quen vốn dễ gây mất cân bằng cũng bộc lộ rõ hơn. Đây không hẳn là giai đoạn xấu, nhưng phù hợp với việc củng cố nền tảng, chọn lọc cơ hội và giữ dư địa an toàn hơn là quyết định nóng hoặc mở rộng quá sức. "
            + action
        )
    if elements:
        return "Khí nổi lên trong giai đoạn này là " + ", ".join(elements) + ". Tác động thuận hay nghịch còn tùy nó nâng Dụng thần hay làm điểm kỵ mạnh thêm, vì vậy các quyết định lớn cần đối chiếu với sức của Nhật chủ và lĩnh vực đời sống đang được kích hoạt. " + action
    return "Giai đoạn này cần được đặt cạnh Dụng thần và Kỵ thần mới thấy rõ ý nghĩa: khi trục điều tiết được nâng, chủ mệnh có thể mở việc; khi điểm mất cân bằng bị kích mạnh, ưu tiên nên là giữ nền, đi có bước và bảo toàn sức bền."


def _luck_element_action(elements: Sequence[str]) -> str:
    notes = {
        "Mộc": "Khí Mộc mở nhu cầu học hỏi, phát triển quan hệ và xây kế hoạch dài hơi; phù hợp gieo nền cho điều có thể lớn dần theo thời gian.",
        "Hỏa": "Khí Hỏa làm nổi bật thương hiệu, tốc độ, sự hiện diện và danh tiếng; cơ hội đi cùng yêu cầu quyết đoán nhưng cần tránh nóng vội.",
        "Thổ": "Khí Thổ kéo trọng tâm về nền tảng, tài sản, đất đai, tổ chức và trách nhiệm; thành quả đến từ tích lũy chắc hơn là đổi hướng liên tục.",
        "Kim": "Khí Kim nhấn mạnh tài chính, kỷ luật, luật lệ, quy trình và định giá; đây là lúc năng lực sàng lọc và kiểm soát rủi ro trở nên quan trọng.",
        "Thủy": "Khí Thủy mở dòng tiền, giao tiếp, thông tin, thị trường và sự dịch chuyển; độ linh hoạt sẽ quyết định cơ hội có thực sự lưu thông hay không.",
    }
    return " ".join(notes[element] for element in elements if element in notes)


_ANNUAL_TEN_GOD_GUIDANCE: dict[str, tuple[str, str, str]] = {
    "Thực Thần": (
        "biến năng lực thành sản phẩm và doanh thu",
        "chuẩn hóa một sản phẩm/dịch vụ chủ lực, đo phản hồi khách hàng rồi mới mở rộng",
        "làm nhiều, chi nhiều hoặc mở quá nhiều hướng cùng lúc",
    ),
    "Thương Quan": (
        "tái cấu trúc cách làm và tạo khác biệt",
        "thử nhỏ, đo kết quả, bỏ phần không hiệu quả và giữ mô hình thắng",
        "phá bỏ hệ thống cũ khi phương án mới chưa được kiểm chứng",
    ),
    "Thiên Tài": (
        "mở cơ hội thị trường và nguồn thu linh hoạt",
        "mở thêm kênh bán hoặc dự án có giới hạn vốn và tiêu chí dừng rõ",
        "dùng đòn bẩy cao hoặc chạy theo cơ hội chưa kiểm chứng",
    ),
    "Chính Tài": (
        "ổn định doanh thu và tích lũy tài sản",
        "siết biên lợi nhuận, dòng tiền và chuyển thu nhập thành phần tích lũy đều",
        "đánh đổi nền thu nhập ổn định để lấy tăng trưởng nóng",
    ),
    "Thất Sát": (
        "nhận trách nhiệm lớn hơn trong môi trường cạnh tranh",
        "chọn một mục tiêu khó nhưng có quyền hạn, nguồn lực và tiêu chuẩn thành công rõ",
        "ôm áp lực hoặc cam kết vượt quá năng lực thực thi",
    ),
    "Chính Quan": (
        "củng cố vị trí, uy tín và tính chính danh",
        "hoàn thiện quy trình, hợp đồng, chức danh hoặc chuẩn nghề nghiệp",
        "đi đường tắt làm suy giảm uy tín dài hạn",
    ),
    "Thiên Ấn": (
        "đổi góc nhìn và nâng chiều sâu chuyên môn",
        "học một năng lực mới có thể áp dụng trực tiếp vào công việc",
        "học lan man nhưng không chuyển thành đầu ra",
    ),
    "Chính Ấn": (
        "xây nền chuyên môn và hệ thống bảo chứng",
        "chuẩn hóa kiến thức, chứng chỉ, quy trình hoặc đội ngũ hỗ trợ",
        "chờ đủ hoàn hảo mới bắt đầu hành động",
    ),
    "Tỷ Kiên": (
        "tăng quyền tự chủ và năng lực tự quyết",
        "xác lập một mảng mình chịu trách nhiệm cuối cùng và đo được kết quả",
        "cố tự làm mọi việc hoặc từ chối hỗ trợ cần thiết",
    ),
    "Kiếp Tài": (
        "mở mạng lưới, đội nhóm và cạnh tranh ngang vai",
        "quy định rõ vai trò, quyền quyết định, tỷ lệ lợi ích và điều kiện rút lui",
        "hợp tác bằng niềm tin miệng hoặc chia nguồn lực không có ranh giới",
    ),
}

_BRANCH_CLASHES = {
    frozenset(pair)
    for pair in (("Tý", "Ngọ"), ("Sửu", "Mùi"), ("Dần", "Thân"), ("Mão", "Dậu"), ("Thìn", "Tuất"), ("Tỵ", "Hợi"))
}
_BRANCH_COMBINES = {
    frozenset(pair)
    for pair in (("Tý", "Sửu"), ("Dần", "Hợi"), ("Mão", "Tuất"), ("Thìn", "Dậu"), ("Tỵ", "Thân"), ("Ngọ", "Mùi"))
}


def _annual_branch_evidence(branch: str, natal_branches: Sequence[str]) -> str:
    clashes = [item for item in natal_branches if frozenset((branch, item)) in _BRANCH_CLASHES]
    combines = [item for item in natal_branches if frozenset((branch, item)) in _BRANCH_COMBINES]
    repeats = [item for item in natal_branches if item == branch]
    notes: list[str] = []
    if clashes:
        notes.append(f"{branch}-{clashes[0]} xung, báo hiệu nhu cầu thay đổi hoặc tái cấu trúc rõ hơn")
    if combines:
        notes.append(f"{branch}-{combines[0]} hợp, thuận cho việc nối nguồn lực và hình thành liên kết")
    if repeats:
        notes.append(f"chi {branch} lặp lại nguyên cục, làm chủ đề sẵn có nổi bật hơn")
    return "; ".join(notes)


def _cycle_for_year(cycles: Sequence[Any], year: int) -> Mapping[str, Any]:
    for raw in cycles:
        item = _mapping(raw)
        start = _integer(item.get("year_start"))
        end = _integer(item.get("year_end"))
        if start is not None and end is not None and start <= year <= end:
            return item
    return {}


def _integer(value: Any) -> int | None:
    try:
        return int(value) if value is not None and str(value).strip() else None
    except (TypeError, ValueError):
        return None


def _annual_roadmap_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    """Build decisive near-term guidance from published Lưu niên identities."""
    luck = _mapping(payload.get("luck"))
    annual = _mapping(luck.get("annual_identity"))
    nearby = [_mapping(item) for item in _list(annual.get("nearby_years"))]
    current_year = _integer(annual.get("civil_year")) or _integer(annual.get("year"))
    if current_year is None:
        return []
    selected = sorted(
        (item for item in nearby if current_year <= (_integer(item.get("year")) or 0) <= current_year + 4),
        key=lambda item: _integer(item.get("year")) or 0,
    )
    if not selected:
        return []

    bazi = _mapping(payload.get("bazi"))
    natal_branches = _non_empty(
        [_text(_mapping(bazi.get(f"{pillar}_pillar")).get("branch")) for pillar in ("year", "month", "day", "hour")]
    )
    cycles = _list(luck.get("cycles"))
    useful = _mapping(payload.get("useful_god"))
    useful_elements = set(_useful_element_labels(useful))
    unfavorable_elements = set(_unfavorable_element_labels(useful))
    paragraphs = [
        "Năm năm tới nên được đọc như một lộ trình hành động, không phải bảng dự báo may rủi. Mỗi năm dưới đây nêu rõ tín hiệu được kích hoạt, việc nên ưu tiên và giới hạn cần giữ."
    ]
    previous_cycle = ""
    for item in selected:
        year = _integer(item.get("year")) or current_year
        ganzhi = _first_text(item.get("gan_zhi"), item.get("ganzhi"))
        ten_god = _text(item.get("ten_god"))
        branch = _text(item.get("branch"))
        stem_element = _element_label(item.get("stem_element"))
        focus, do_this, avoid = _ANNUAL_TEN_GOD_GUIDANCE.get(
            ten_god,
            ("củng cố nền lực và chọn việc có kết quả đo được", "giữ một mục tiêu chính và theo dõi kết quả theo quý", "mở rộng chỉ vì cảm giác thuận lợi"),
        )
        evidence = [f"thiên can hiện {ten_god}" if ten_god else ""]
        branch_note = _annual_branch_evidence(branch, natal_branches)
        if branch_note:
            evidence.append(branch_note)
        cycle = _cycle_for_year(cycles, year)
        cycle_ganzhi = _first_text(cycle.get("gan_zhi"), cycle.get("ganzhi"))
        if cycle_ganzhi and cycle_ganzhi != previous_cycle:
            start = _integer(cycle.get("year_start"))
            evidence.append(
                f"bắt đầu Đại vận {cycle_ganzhi}" if start == year else f"đang trong Đại vận {cycle_ganzhi}"
            )
        previous_cycle = cycle_ganzhi or previous_cycle
        balance_note = ""
        if stem_element in unfavorable_elements:
            balance_note = f" Hành {stem_element} đồng thời chạm nhóm cần tiết chế, nên thành quả phụ thuộc vào khả năng giữ giới hạn."
        elif stem_element in useful_elements:
            balance_note = f" Hành {stem_element} đi cùng trục nên dùng, có thể chủ động hơn khi nền thực thi đã sẵn sàng."
        title = f"{year} - {ganzhi}: trọng tâm là {focus}." if ganzhi else f"{year}: trọng tâm là {focus}."
        paragraphs.append(
            title
            + (" Căn cứ: " + "; ".join(part for part in evidence if part) + "." if any(evidence) else "")
            + balance_note
            + f" Nên làm: {do_this}. Không nên: {avoid}."
        )
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
    useful = _mapping(payload.get("useful_god"))
    pattern = _mapping(payload.get("pattern"))
    strength = _mapping(payload.get("strength"))
    useful_line = _useful_god_summary(useful)
    strength_label = _strength_label(_first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")))
    if useful_line:
        paragraphs.append(
            "Ưu tiên đầu tiên là đưa Dụng thần vào những lựa chọn có thể thực hiện mỗi ngày, bởi đây là hướng giúp chủ mệnh bớt hao lực và phát huy sở trường một cách tự nhiên hơn. "
            + useful_line
        )
    structure = _first_text(pattern.get("cach_cuc"), pattern.get("pattern"))
    if structure:
        paragraphs.append(
            f"Với nền {structure}, chủ mệnh phát triển tốt trong môi trường có nguyên tắc rõ, đầu ra đo được và thành quả có thể tích lũy. Trước một cơ hội lớn, thế {strength_label or 'thân'} sẽ cho biết nên tăng tốc hay dành thêm thời gian củng cố nền lực."
        )
    luck = _mapping(payload.get("luck"))
    current = _mapping(luck.get("current_cycle"))
    current_ganzhi = _first_text(current.get("gan_zhi"), current.get("ganzhi"))
    if current_ganzhi:
        paragraphs.append(
            f"Đại vận {current_ganzhi} là bối cảnh chủ mệnh đang thực sự sống trong đó. Khi vận nâng Dụng thần, có thể chủ động mở việc; khi điểm kỵ nổi lên, sự khôn ngoan nằm ở việc giữ tiền, giữ sức và giữ những quan hệ quan trọng thay vì cố thắng bằng tốc độ."
        )
    paragraphs.append(_module_bridge_recommendation(payload))
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


def _module_bridge_recommendation(payload: Mapping[str, Any]) -> str:
    bazi = _mapping(payload.get("bazi"))
    calendar = _mapping(payload.get("calendar"))
    pattern = _mapping(payload.get("pattern"))
    useful = _mapping(payload.get("useful_god"))
    structure = _first_text(pattern.get("cach_cuc"), pattern.get("pattern"))
    day_pillar = _pillar_can_chi(_mapping(bazi.get("day_pillar")))
    month_pillar = _pillar_can_chi(_mapping(bazi.get("month_pillar")))
    hour_pillar = _pillar_can_chi(_mapping(bazi.get("hour_pillar")))
    cung_phi = _first_text(calendar.get("cung_phi"), calendar.get("menh_quai"))
    house_group = _first_text(calendar.get("nhom_trach"), calendar.get("house_group"))
    useful_elements = _useful_element_labels(useful)
    anchors = _non_empty(
        [
            f"hôn nhân lấy trụ ngày {day_pillar}" if day_pillar else "",
            f"nghề nghiệp lấy trụ tháng {month_pillar}" + (f" và Mệnh cục {structure}" if structure else "") if month_pillar or structure else "",
            "hợp tác lấy Tỷ/Kiếp, Tài tinh, Quan/Sát và Ấn tinh",
            f"phong thủy lấy Cung Phi {cung_phi}" + (f" thuộc {house_group}" if house_group else "") if cung_phi or house_group else "",
            f"sinh con lấy trụ giờ {hour_pillar} và Đại vận" if hour_pillar else "",
            f"mọi kết luận đều quay lại trục Dụng thần {', '.join(useful_elements)}" if useful_elements else "",
        ]
    )
    if not anchors:
        return ""
    return "Những bước tư vấn chuyên sâu về sau đều có điểm tựa rõ trong lá số: " + "; ".join(anchors) + ". Nhờ vậy, mỗi lời khuyên vẫn mang tính riêng của chủ mệnh thay vì trở thành một công thức chung cho mọi người."


def _synthesis_paragraphs(payload: Mapping[str, Any], narrative: Mapping[str, Any]) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    pattern = _mapping(payload.get("pattern"))
    strength = _mapping(payload.get("strength"))
    useful = _mapping(payload.get("useful_god"))
    five_elements = _mapping(payload.get("five_elements"))
    luck = _mapping(payload.get("luck"))
    ten_layers = build_ten_gods_four_layer_view(payload)
    shen_groups = build_shen_sha_grouped_view(payload)

    day_master = _day_master_summary(bazi).rstrip(".")
    strength_label = _strength_label(_first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")))
    structure = _first_text(pattern.get("cach_cuc"), pattern.get("pattern"))
    useful_elements = _useful_element_labels(useful)
    counts = _mapping(five_elements.get("counts"))
    dominant = _element_label_list(five_elements.get("dominant")) or _element_extremes(counts, strongest=True)
    weak = _element_label_list(five_elements.get("missing")) or _element_extremes(counts, strongest=False)
    current = _mapping(luck.get("current_cycle"))
    current_ganzhi = _first_text(current.get("gan_zhi"), current.get("ganzhi"))

    paragraphs = [
        _fallback_join(
            "Nhìn lại toàn cục, đường dây xuyên suốt của lá số là",
            day_master + "," if day_master else "",
            f"thế {strength_label}," if strength_label else "",
            f"Mệnh cục {structure}," if structure else "",
            f"và Dụng thần {', '.join(useful_elements)}." if useful_elements else "",
            "Khi giữ đúng đường dây này, các mặt tưởng như riêng biệt của đời sống sẽ trở về cùng một logic.",
        )
    ]

    favorable_signals = _synthesis_favorable_signals(ten_layers, shen_groups, dominant)
    if favorable_signals:
        paragraphs.append(
            "Lợi thế đáng quý của lá số nằm ở "
            + "; ".join(favorable_signals)
            + ". Đây là phần nên được chủ động đưa vào nghề nghiệp, cách tạo thu nhập, lựa chọn người đồng hành và môi trường sống để tiềm năng trở thành kết quả nhìn thấy được."
        )

    caution_signals = _synthesis_caution_signals(ten_layers, weak, useful)
    if caution_signals:
        paragraphs.append(
            "Mặt cần được chăm sóc và tiết chế là "
            + "; ".join(caution_signals)
            + ". Khi có nếp sống đều, kỷ luật tài chính, ranh giới quan hệ rõ và biết chọn thời điểm, những điểm này trở thành bài học trưởng thành thay vì lực cản kéo dài."
        )

    if current_ganzhi:
        paragraphs.append(
            f"Trong Đại vận {current_ganzhi}, điều quan trọng không phải gắn nhãn tốt hay xấu, mà là nhận ra phần năng lực nào đang được mở và thói quen nào dễ bị đẩy quá xa. Chủ động theo phần thuận và giữ giới hạn ở phần kỵ sẽ tạo khác biệt lớn cho cùng một chặng vận."
        )

    paragraphs.append(
        "Con đường cải thiện nên bắt đầu từ nền sức khỏe và nhịp sống, rồi mới mở sang nghề nghiệp, tài vận, hôn nhân, hợp tác, phong thủy và con cái. Khi nền bên trong ổn, các lựa chọn bên ngoài thường sáng rõ hơn và ít phải trả giá vì quyết định trong lúc mất cân bằng."
    )
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


def _synthesis_favorable_signals(
    ten_layers: Mapping[str, Any],
    shen_groups: Mapping[str, Any],
    dominant: Sequence[str],
) -> list[str]:
    signals: list[str] = []
    output = _ten_god_signal_labels(ten_layers, ("Thực Thần", "Thương Quan"))
    resource = _ten_god_signal_labels(ten_layers, ("Chính Ấn", "Thiên Ấn"))
    wealth = _ten_god_signal_labels(ten_layers, ("Chính Tài", "Thiên Tài"))
    noble_items = _list(_mapping(_mapping(shen_groups.get("groups")).get("noble_support")).get("items"))
    authority_items = _list(_mapping(_mapping(shen_groups.get("groups")).get("authority")).get("items"))
    if output:
        signals.append("khả năng tạo sản phẩm/giá trị qua " + ", ".join(output))
    if resource:
        signals.append("nền học hỏi, chuyên môn và người nâng đỡ qua " + ", ".join(resource))
    if wealth:
        signals.append("ý thức tài sản và dòng tiền qua " + ", ".join(wealth))
    if dominant:
        signals.append("khí nổi bật " + ", ".join(dominant))
    if noble_items:
        signals.append("tín hiệu Quý nhân/phúc tinh hỗ trợ khi đi đúng thời")
    if authority_items:
        signals.append("tín hiệu tài danh/uy tín có thể dùng khi có năng lực thật")
    return _unique_texts(signals)


def _synthesis_caution_signals(
    ten_layers: Mapping[str, Any],
    weak: Sequence[str],
    useful: Mapping[str, Any],
) -> list[str]:
    signals: list[str] = []
    peers = _ten_god_signal_labels(ten_layers, ("Tỷ Kiên", "Kiếp Tài"))
    officer = _ten_god_signal_labels(ten_layers, ("Chính Quan", "Thất Sát"))
    unfavorable = _unfavorable_element_labels(useful)
    if weak:
        signals.append("hành yếu/thiếu " + ", ".join(weak))
    if unfavorable:
        signals.append("nhóm Kỵ thần cần tiết chế " + ", ".join(unfavorable))
    if peers:
        signals.append("Tỷ/Kiếp cần ranh giới rõ khi chia nguồn lực")
    if officer:
        signals.append("Quan/Sát tạo áp lực trách nhiệm nên phải quản trị stress và pháp lý/kỷ luật")
    return _unique_texts(signals)


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
    paragraphs: list[str] = []
    strength_label = _strength_label(_first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")))
    structure = _first_text(pattern.get("cach_cuc"), pattern.get("pattern"))
    useful_line = _useful_god_domain_lead(useful)
    logic_lead = DOMAIN_LOGIC_LEADS.get(key, "")
    if logic_lead:
        paragraphs.append(logic_lead)
    if summary and not _is_low_value_domain_summary(summary) and "Dụng thần trọng tâm:" not in summary:
        paragraphs.append(summary)

    if key == "health":
        paragraphs.extend(_health_domain_paragraphs(payload, five_elements, strength_label))
    elif key == "wealth":
        paragraphs.extend(_wealth_domain_paragraphs(payload, ten_layers, structure, strength_label, useful_line))
    elif key == "career":
        paragraphs.extend(_career_domain_paragraphs(payload, ten_layers, structure, strength_label, useful_line))
    elif key == "marriage":
        paragraphs.extend(_marriage_domain_paragraphs(payload, ten_layers, shen_groups, strength_label, useful_line))
    elif key == "children":
        paragraphs.extend(_children_domain_paragraphs(payload, ten_layers, useful_line))
    elif key == "parents":
        paragraphs.extend(_parents_domain_paragraphs(payload, ten_layers, useful_line))
    elif key == "siblings":
        paragraphs.extend(_partnership_domain_paragraphs(ten_layers, useful_line))
    elif key == "ancestry":
        paragraphs.extend(_ancestry_domain_paragraphs(payload, ten_layers, shen_groups))
    elif key == "property":
        paragraphs.extend(_property_domain_paragraphs(payload, useful_line))

    advice = _DOMAIN_RECOMMENDATIONS.get(key, "")
    if advice:
        paragraphs.append(advice)
    return _unique_texts(paragraphs)


def _health_domain_paragraphs(
    payload: Mapping[str, Any],
    five_elements: Mapping[str, Any],
    strength_label: str,
) -> list[str]:
    temperature = _mapping(payload.get("temperature"))
    climate = _first_text(temperature.get("climate_state_label"), temperature.get("temperature_level"))
    counts = _mapping(five_elements.get("counts"))
    dominant = _element_label_list(five_elements.get("dominant")) or _element_extremes(counts, strongest=True)
    weak = _element_label_list(five_elements.get("missing")) or _element_extremes(counts, strongest=False)
    distribution = _element_distribution(counts)
    paragraphs: list[str] = []
    if distribution:
        paragraphs.append(
            "Bảng Ngũ hành cho thấy "
            + distribution
            + ". Khi luận sức khỏe, đây là bản đồ khí chất: hành nào nổi bật thì vùng cơ thể/tập tính của hành đó dễ thành điểm cần giữ; hành nào yếu thì cần được bồi nền đều đặn."
        )
    if dominant:
        dominant_notes = [_element_health_note(element, excess=True) for element in dominant]
        paragraphs.append(
            "Hành nổi bật: "
            + ", ".join(dominant)
            + ". "
            + " ".join(note for note in dominant_notes if note)
        )
    if weak:
        weak_notes = [_element_health_note(element, excess=False) for element in weak]
        paragraphs.append(
            "Hành còn thiếu hoặc yếu: "
            + ", ".join(weak)
            + ". "
            + " ".join(note for note in weak_notes if note)
        )
    paragraphs.extend(_health_relation_paragraphs(payload, counts, dominant, weak))
    climate_note = CLIMATE_HEALTH_GUIDANCE.get(climate, "")
    if climate_note or strength_label:
        paragraphs.append(
            _fallback_join(
                climate_note,
                f"Thế {strength_label} cho biết cách dùng sức cũng quan trọng: không chỉ xem cơ quan nào yếu, mà còn xem người này nên tiêu hao, hồi phục và giữ nhịp sinh hoạt ra sao." if strength_label else "",
            )
        )
    paragraphs.append(
        "Kết luận sức khỏe nên dùng như định hướng phòng ngừa: giữ nhịp ngủ, ăn, vận động và môi trường sống hợp khí; nếu có triệu chứng cụ thể thì vẫn cần kiểm tra y khoa, không dùng lá số thay cho chẩn đoán."
    )
    return _unique_texts(paragraphs)


def _wealth_domain_paragraphs(
    payload: Mapping[str, Any],
    ten_layers: Mapping[str, Any],
    structure: str,
    strength_label: str,
    useful_line: str,
) -> list[str]:
    paragraphs: list[str] = []
    wealth_signals = _ten_god_signal_labels(ten_layers, ("Chính Tài", "Thiên Tài"))
    output_signals = _ten_god_signal_labels(ten_layers, ("Thực Thần", "Thương Quan"))
    paragraphs.append(
        _fallback_join(
            f"Mệnh cục {structure} cho biết cách lá số tổ chức nguồn lực và tạo kết quả." if structure else "",
            f"Tín hiệu Tài tinh đang thấy: {', '.join(wealth_signals)}." if wealth_signals else "Chưa thấy Tài tinh lộ rõ trong 4 tầng đang xét; điều này không có nghĩa là không có tiền, mà cho thấy tài vận cần đọc qua năng lực tạo giá trị, nghề nghiệp và Đại vận kích hoạt.",
            f"Tín hiệu sinh tài qua sản phẩm/kỹ năng: {', '.join(output_signals)}." if output_signals else "",
        )
    )
    paragraphs.extend(_ten_god_reading_paragraphs("Luận Tài tinh", wealth_signals, WEALTH_TEN_GOD_READINGS))
    paragraphs.extend(_ten_god_reading_paragraphs("Luận nguồn sinh tài", output_signals, WEALTH_TEN_GOD_READINGS))
    if output_signals and wealth_signals:
        paragraphs.append(
            "Khi Thực/Thương đi cùng Tài tinh, mạch kiếm tiền sáng hơn: trước hết phải có năng lực tạo sản phẩm, dịch vụ hoặc giá trị cụ thể, sau đó mới chuyển hóa thành dòng tiền. Đây là kiểu tài vận cần làm thật, tích lũy uy tín và đo bằng kết quả, không nên chỉ trông vào may mắn."
        )
    elif output_signals and not wealth_signals:
        paragraphs.append(
            "Có Thực/Thương mà Tài tinh chưa lộ rõ thì trọng tâm không phải săn cơ hội tiền ngay, mà là làm mạnh sản phẩm, tay nghề, nội dung, năng lực phục vụ. Khi Đại vận hoặc lưu niên kích Tài, phần đã tích lũy này mới dễ đổi thành tiền."
        )
    elif wealth_signals and not output_signals:
        paragraphs.append(
            "Có Tài tinh nhưng thiếu tín hiệu sinh tài rõ thì người này vẫn có ý thức về tiền và trách nhiệm vật chất, nhưng cần xây hệ thống tạo giá trị đều hơn để tiền không chỉ đến theo cơ hội rời rạc."
        )
    paragraphs.extend(_wealth_business_environment_paragraphs(payload))
    if strength_label:
        paragraphs.append(_wealth_strength_guidance(strength_label))
    if useful_line:
        paragraphs.append(
            useful_line
            + " Trong tài vận, Dụng thần là bộ lọc để biết nên mở rộng theo kiểu nào: cơ hội nào làm lá số cân bằng hơn thì nên ưu tiên, cơ hội nào kích hoạt điểm kỵ thì dù hấp dẫn cũng cần đi chậm."
        )
    return _unique_texts(paragraphs)


def _wealth_business_environment_paragraphs(payload: Mapping[str, Any]) -> list[str]:
    five_elements = _mapping(payload.get("five_elements"))
    counts = _mapping(five_elements.get("counts"))
    dominant = _element_label_list(five_elements.get("dominant")) or _element_extremes(counts, strongest=True)
    metal_count = _element_count(counts, "Kim")
    water_count = _element_count(counts, "Thủy")
    fire_count = _element_count(counts, "Hỏa")
    calendar = _mapping(payload.get("calendar"))
    cung_phi = _first_text(calendar.get("cung_phi"), calendar.get("menh_quai"))
    house_group = _first_text(calendar.get("nhom_trach"), calendar.get("house_group"))
    paragraphs: list[str] = []

    if metal_count >= 3 or "Kim" in dominant:
        paragraphs.append(
            "Xét riêng về kinh doanh và tài vận, Kim nổi bật là tín hiệu tốt cho khả năng quản trị tiền, tài sản, quy trình, luật lệ, định giá và kiểm soát rủi ro. Người có Kim mạnh thường hợp các việc cần sự sắc bén, kỷ luật, tính toán rõ và biết biến nguồn lực thành tài sản; tuy vậy Kim quá căng thì dễ cứng, khô hoặc quá thận trọng, nên vẫn cần dòng lưu thông và cơ hội phù hợp để tiền không bị đứng."
        )
    if metal_count >= 3 and water_count >= 2:
        paragraphs.append(
            "Kim có Thủy đi kèm thì tài khí dễ có dòng chảy hơn: năng lực quản trị, định giá và hệ thống của Kim được Thủy làm mềm bằng giao tiếp, thị trường, luân chuyển thông tin và khả năng xoay dòng tiền. Đây là thế kinh doanh nên chú trọng kênh phân phối, dữ liệu khách hàng và nhịp thu chi linh hoạt."
        )
    elif metal_count >= 3 and water_count <= 1:
        paragraphs.append(
            "Kim mạnh nhưng Thủy yếu thì tiền/tài sản dễ nghiêng về tích lũy, kiểm soát và phòng thủ hơn là dòng chảy. Khi làm kinh doanh cần đặc biệt chú ý thanh khoản, kênh bán, giao tiếp thị trường và cách làm cho sản phẩm/dịch vụ lưu thông đều, tránh giữ nguồn lực quá chặt."
        )
    if metal_count >= 3 and fire_count >= 3:
        paragraphs.append(
            "Kim gặp Hỏa đủ lực tạo thành thế vừa có tài sản/quy trình vừa có áp lực cạnh tranh, thương hiệu, tốc độ và mục tiêu doanh số. Đây có thể là lực tốt cho kinh doanh nếu có kỷ luật vận hành; ngược lại dễ thành căng thẳng, quyết định nóng hoặc xung đột giữa kiểm soát và mở rộng."
        )
    if cung_phi or house_group:
        paragraphs.append(
            _fallback_join(
                f"Cung Phi {cung_phi}" if cung_phi else "",
                f"thuộc {house_group}" if house_group else "",
                "là dữ liệu nên dùng khi nối phần tài vận sang phong thủy kinh doanh. Đông/Tây Tứ Trạch không thay thế Tài tinh hay Đại vận, nhưng giúp chọn hướng nhà, hướng bàn làm việc, cửa hàng, kho bãi hoặc môi trường giao dịch sao cho không gian hỗ trợ khí mệnh và cách kiếm tiền của người đó.",
            )
        )
    return paragraphs


def _career_domain_paragraphs(
    payload: Mapping[str, Any],
    ten_layers: Mapping[str, Any],
    structure: str,
    strength_label: str,
    useful_line: str,
) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    month_layer = _pillar_layer(ten_layers, "month")
    career_signals = _ten_god_signal_labels(
        ten_layers,
        ("Chính Quan", "Thất Sát", "Chính Ấn", "Thiên Ấn", "Thực Thần", "Thương Quan", "Chính Tài", "Thiên Tài"),
    )
    paragraphs: list[str] = [
        _fallback_join(
            _pillar_brief("Trụ tháng", _mapping(bazi.get("month_pillar"))),
            _layer_brief(month_layer),
            f"Mệnh cục {structure} là khung tổ chức nghề nghiệp của lá số." if structure else "",
            f"Nhóm tín hiệu nghề nghiệp nổi bật: {', '.join(career_signals)}." if career_signals else "",
        )
    ]
    paragraphs.extend(_ten_god_reading_paragraphs("Luận nghề theo Thập thần", career_signals, CAREER_TEN_GOD_READINGS))
    if _has_any(career_signals, ("Chính Quan", "Thất Sát")) and _has_any(career_signals, ("Chính Ấn", "Thiên Ấn")):
        paragraphs.append(
            "Quan/Sát đi cùng Ấn là thế nghề cần trách nhiệm nhưng cũng cần nền chuyên môn. Người có mạch này thường thuyết phục hơn khi làm trong vai trò có chuẩn mực, kiến thức, uy tín hoặc quyền hạn được trao rõ, thay vì chỉ dựa vào cảm hứng nhất thời."
        )
    elif _has_any(career_signals, ("Thực Thần", "Thương Quan")) and _has_any(career_signals, ("Chính Tài", "Thiên Tài")):
        paragraphs.append(
            "Thực/Thương đi cùng Tài khiến nghề nghiệp nên gắn với sản phẩm, dịch vụ, kinh doanh hoặc khả năng biến ý tưởng thành doanh thu. Điểm cần giữ là kỷ luật vận hành, vì sáng tạo mạnh mà thiếu khuôn thì dễ phân tán."
        )
    if strength_label:
        paragraphs.append(_career_strength_guidance(strength_label))
    if useful_line:
        paragraphs.append(
            useful_line
            + " Khi chọn nghề hoặc vai trò, nên ưu tiên môi trường làm mạnh trục Dụng thần, vì đó là nơi năng lực tự nhiên được dùng mà không làm mệnh cục mất cân bằng quá mức."
        )
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


def _marriage_domain_paragraphs(
    payload: Mapping[str, Any],
    ten_layers: Mapping[str, Any],
    shen_groups: Mapping[str, Any],
    strength_label: str,
    useful_line: str,
) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    day_layer = _pillar_layer(ten_layers, "day")
    spouse_labels = _spouse_star_labels(payload)
    spouse_signals = _ten_god_signal_labels(ten_layers, tuple(spouse_labels))
    relationship_group = _mapping(_mapping(shen_groups.get("groups")).get("relationship"))
    paragraphs: list[str] = []
    paragraphs.extend(_spouse_star_reasoning(payload, ten_layers, spouse_labels))
    paragraphs.extend(_spouse_palace_reasoning(bazi, day_layer, spouse_labels))
    if spouse_labels:
        paragraphs.extend(_ten_god_reading_paragraphs("Luận sao phối ngẫu", spouse_signals, MARRIAGE_TEN_GOD_READINGS))
    relationship_brief = _group_brief(relationship_group)
    if relationship_brief:
        paragraphs.append(
            relationship_brief
            + " Đây là dấu hiệu cho thấy duyên gặp gỡ và sức hút có thể đến khá tự nhiên. Tuy vậy, duyên tinh chỉ mở cánh cửa; chất lượng hôn nhân vẫn được quyết định bởi sự rõ ràng trong cam kết, khả năng giữ ranh giới và cách hai người xử lý những lúc cảm xúc lên cao."
        )
    if strength_label:
        paragraphs.append(_marriage_strength_guidance(strength_label))
    if useful_line:
        paragraphs.append(
            useful_line
            + " Trong hôn nhân, Dụng thần không thay thế Phu/Thê tinh và cung phối ngẫu; nó được dùng như bộ lọc để phân biệt người chỉ tạo sức hút với người thực sự giúp đời sống chung ổn định hơn."
        )
    conclusion = _spouse_conclusion(payload, ten_layers, spouse_labels)
    if conclusion:
        paragraphs.append(conclusion)
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


_PILLAR_MARRIAGE_CONTEXT = {
    "year": "ở trụ năm, duyên thường mở qua môi trường xã hội rộng, nền gia đình hoặc các mối quan hệ từ giai đoạn sớm",
    "month": "ở trụ tháng, hình tượng phối ngẫu dễ gắn với công việc, môi trường nghề nghiệp và nhịp sống trưởng thành",
    "day": "ngay tại trụ ngày, chủ đề bạn đời đi sát đời sống riêng và thường được cảm nhận trực tiếp hơn",
    "hour": "ở trụ giờ, duyên chính thức thường rõ hơn khi chủ mệnh đã trưởng thành về nghề nghiệp, tài chính và cách tổ chức cuộc sống",
}


def _spouse_occurrences(ten_layers: Mapping[str, Any], labels: Sequence[str]) -> list[dict[str, str]]:
    occurrences: list[dict[str, str]] = []
    for layer in _list(ten_layers.get("layers")):
        if not isinstance(layer, Mapping):
            continue
        pillar = _text(layer.get("pillar"))
        primary = _text(layer.get("primary_ten_god"))
        if primary in labels and primary != "Nhật chủ":
            occurrences.append({"god": primary, "pillar": pillar, "visibility": "lộ"})
        for field, visibility in (("visible", "lộ"), ("hidden", "ẩn")):
            for item in _list(layer.get(field)):
                if not isinstance(item, Mapping):
                    continue
                god = _text(item.get("ten_god"))
                if god in labels:
                    occurrences.append({"god": god, "pillar": pillar, "visibility": visibility})
    unique: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for item in occurrences:
        key = (item["god"], item["pillar"], item["visibility"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def _spouse_star_reasoning(
    payload: Mapping[str, Any],
    ten_layers: Mapping[str, Any],
    spouse_labels: Sequence[str],
) -> list[str]:
    if not spouse_labels:
        return []
    gender = _first_text(
        _mapping(payload.get("customer")).get("gender_label"),
        _mapping(payload.get("customer")).get("gender"),
    ).lower()
    role = "Phu tinh" if gender in {"female", "nữ", "nu", "f"} else "Thê tinh"
    occurrences = _spouse_occurrences(ten_layers, spouse_labels)
    visible = [item for item in occurrences if item["visibility"] == "lộ"]
    hidden = [item for item in occurrences if item["visibility"] == "ẩn"]
    paragraphs = [f"{role} được đọc qua {', '.join(spouse_labels)}. Đây là trục dùng để nhận diện hình tượng người bạn đời và cách duyên hôn nhân đi vào đời sống, không phải căn cứ để chốt một nghề hay một con người cụ thể."]
    if visible:
        details = ", ".join(
            f"{item['god']} lộ tại trụ {PILLAR_LABELS.get(item['pillar'], item['pillar']).lower()}"
            for item in visible
        )
        paragraphs.append(f"Điểm nổi bật là {details}. Vì sao này hiện ra ở thiên can, phẩm chất của người phối ngẫu và thái độ đối với cam kết thường biểu hiện khá rõ, thay vì chỉ tồn tại như một nhu cầu kín bên trong.")
        contexts = _unique_texts(_PILLAR_MARRIAGE_CONTEXT.get(item["pillar"], "") for item in visible)
        if contexts:
            paragraphs.append("Xét vị trí, " + "; ".join(contexts) + ".")
    elif hidden:
        details = ", ".join(f"{item['god']} ẩn tại trụ {PILLAR_LABELS.get(item['pillar'], item['pillar']).lower()}" for item in hidden)
        paragraphs.append(f"Trong nguyên cục, {details}. Phối ngẫu tinh có mặt nhưng chưa lộ rõ, nên duyên thường cần đúng môi trường hoặc đúng vận mới thành hình rõ; không nên diễn giải thành không có duyên hôn nhân.")
    else:
        paragraphs.append("Nguyên cục chưa thấy Phu/Thê tinh lộ hoặc tàng rõ trong dữ liệu đang xét. Điều này không đồng nghĩa không kết hôn; kết luận cần dựa nhiều hơn vào cung phối ngẫu và vận kích hoạt, thay vì dựng một chân dung quá cụ thể.")
    gods = {item["god"] for item in occurrences}
    if "Chính Quan" in gods and "Thất Sát" not in gods:
        paragraphs.append("Cấu trúc nghiêng về Chính Quan hơn Thất Sát: người phù hợp để đi đường dài thường chững chạc, có nghề nghiệp và nguyên tắc rõ, coi trọng trách nhiệm và danh dự. Sức hút ban đầu có thể không quá ồn ào, nhưng giá trị nằm ở khả năng làm cho cuộc sống chung có trật tự và ổn định hơn.")
    elif "Thất Sát" in gods and "Chính Quan" not in gods:
        paragraphs.append("Cấu trúc nghiêng về Thất Sát: dễ bị thu hút bởi người quyết đoán, mạnh và có khả năng xử lý áp lực. Mặt cần kiểm chứng trước hôn nhân là cách người đó dùng quyền lực và quản trị cảm xúc, bởi bản lĩnh là điểm mạnh nhưng kiểm soát quá mức sẽ trở thành áp lực lâu dài.")
    elif "Chính Quan" in gods and "Thất Sát" in gods:
        paragraphs.append("Chính Quan và Thất Sát cùng xuất hiện, nên tiêu chuẩn tình cảm có hai lớp: vừa cần sự ổn định, chính danh, vừa dễ bị hấp dẫn bởi người mạnh và nhiều chuyển động. Điều cần phân biệt là người tạo cảm xúc mạnh chưa chắc là người có cấu trúc phù hợp để sống lâu dài.")
    return paragraphs


def _spouse_palace_reasoning(
    bazi: Mapping[str, Any],
    day_layer: Mapping[str, Any],
    spouse_labels: Sequence[str],
) -> list[str]:
    day_pillar = _mapping(bazi.get("day_pillar"))
    can_chi = _pillar_can_chi(day_pillar)
    branch = _pillar_branch(day_pillar)
    hidden = [item for item in _list(day_layer.get("hidden")) if isinstance(item, Mapping)]
    hidden_gods = _unique_texts(_text(item.get("ten_god")) for item in hidden)
    hidden_stems = _unique_texts(_text(item.get("stem")) for item in hidden)
    paragraphs = [f"Cung phối ngẫu nằm tại nhật chi {branch or can_chi}. Đây là tầng mô tả đời sống bên trong của hôn nhân: hai người phải cùng xử lý điều gì sau khi sức hút ban đầu đã qua."]
    if hidden_gods:
        stem_text = f" ({', '.join(hidden_stems)})" if hidden_stems else ""
        paragraphs.append(f"Cung này chứa {', '.join(hidden_gods)}{stem_text}. Vì vậy, đời sống hôn nhân cần được đọc qua chính những chủ đề này, thay vì chỉ lấy một sao phối ngẫu rồi kết luận toàn bộ quan hệ.")
        if not any(god in spouse_labels for god in hidden_gods):
            paragraphs.append("Phu/Thê tinh không nằm trực tiếp trong cung phối ngẫu. Điều này thường cho thấy hôn nhân không tự nhiên trở thành trung tâm duy nhất của tuổi trẻ; người phù hợp còn phải cùng chủ mệnh giải được các bài toán thực tế của đời sống chung như công việc, tiền bạc, gia đình hoặc sự nâng đỡ tinh thần.")
    return paragraphs


def _spouse_conclusion(
    payload: Mapping[str, Any],
    ten_layers: Mapping[str, Any],
    spouse_labels: Sequence[str],
) -> str:
    occurrences = _spouse_occurrences(ten_layers, spouse_labels)
    gods = {item["god"] for item in occurrences}
    if "Chính Quan" in gods:
        portrait = "điềm tĩnh, có nghề nghiệp rõ, giữ lời, có kỷ luật tài chính và tôn trọng cam kết"
        warning = "sống tùy hứng, nóng nảy, thiếu trách nhiệm hoặc dùng nguyên tắc để kiểm soát người khác"
    elif "Thất Sát" in gods:
        portrait = "quyết đoán, có năng lực gánh việc, chịu áp lực tốt nhưng biết tôn trọng ranh giới"
        warning = "mạnh nhưng độc đoán, đẩy rủi ro và áp lực sang người bạn đời"
    elif set(spouse_labels) & gods:
        portrait = "có khả năng cùng xây đời sống thực tế và minh bạch trách nhiệm"
        warning = "hấp dẫn lúc đầu nhưng thiếu ổn định và không rõ cam kết"
    else:
        return "Kết luận hiện tại nên dừng ở tiêu chí chọn người và cách vận hành quan hệ; chưa đủ căn cứ để khẳng định nghề nghiệp, ngoại hình, tuổi hay số lần đổ vỡ của người phối ngẫu."
    return f"Kết luận thực tế: người phù hợp hơn là người {portrait}. Kiểu người cần thận trọng là người {warning}. Đây là tiêu chí có giá trị hơn việc chỉ chọn tuổi hợp hoặc chọn một người mang đúng hành của Dụng thần."


def _partnership_domain_paragraphs(ten_layers: Mapping[str, Any], useful_line: str) -> list[str]:
    peer_signals = _ten_god_signal_labels(ten_layers, ("Tỷ Kiên", "Kiếp Tài"))
    business_signals = _ten_god_signal_labels(
        ten_layers,
        ("Chính Tài", "Thiên Tài", "Chính Quan", "Thất Sát", "Chính Ấn", "Thiên Ấn"),
    )
    paragraphs: list[str] = [
        _fallback_join(
            f"Tín hiệu đồng hành/cạnh tranh: {', '.join(peer_signals)}." if peer_signals else "Chưa thấy Tỷ Kiên/Kiếp Tài lộ rõ; phần hợp tác nên đọc thêm qua Tài tinh, Quan/Sát, Ấn và Đại vận.",
            f"Tín hiệu hợp tác làm ăn liên quan: {', '.join(business_signals)}." if business_signals else "",
            "Mục này là nền cho tư vấn hợp tác: không chỉ xem có người hỗ trợ hay không, mà còn xem hợp tác dễ sinh tiền, sinh áp lực, sinh tranh chấp hay sinh uy tín ở điểm nào.",
        )
    ]
    paragraphs.extend(_ten_god_reading_paragraphs("Luận hợp tác", peer_signals, PARTNERSHIP_TEN_GOD_READINGS))
    paragraphs.extend(_ten_god_reading_paragraphs("Luận hợp tác", business_signals, PARTNERSHIP_TEN_GOD_READINGS))
    if _has_any(peer_signals, ("Kiếp Tài",)) and _has_any(business_signals, ("Chính Tài", "Thiên Tài")):
        paragraphs.append(
            "Kiếp Tài gặp Tài tinh là cấu trúc rất cần minh bạch tiền bạc: có cơ hội cùng kiếm tiền, nhưng cũng dễ phát sinh tranh phần, ứng trước, chia lợi nhuận hoặc mâu thuẫn vì quyền kiểm soát dòng tiền."
        )
    if _has_any(business_signals, ("Chính Quan", "Thất Sát")):
        paragraphs.append(
            "Khi Quan/Sát xuất hiện trong hợp tác, hợp đồng, pháp lý, phân quyền và tiêu chuẩn vận hành phải đặt trước cảm tính. Càng làm việc lớn càng cần giấy tờ rõ, trách nhiệm rõ và cơ chế xử lý rủi ro rõ."
        )
    if _has_any(business_signals, ("Chính Ấn", "Thiên Ấn")):
        paragraphs.append(
            "Ấn tinh trong hợp tác cho thấy niềm tin, tri thức, uy tín hoặc người nâng đỡ là tài sản quan trọng. Nên chọn cộng sự có nền chuyên môn và đạo đức làm việc ổn, vì đây là kiểu hợp tác thắng bằng độ bền hơn là đánh nhanh."
        )
    if useful_line:
        paragraphs.append(
            useful_line
            + " Khi xét cộng sự, người phù hợp là người giúp trục Dụng thần được mạnh lên; người liên tục kích hoạt điểm kỵ thì dù có lợi trước mắt cũng nên thận trọng."
        )
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


def _children_domain_paragraphs(
    payload: Mapping[str, Any],
    ten_layers: Mapping[str, Any],
    useful_line: str,
) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    hour_layer = _pillar_layer(ten_layers, "hour")
    child_labels = _child_star_labels(payload)
    child_signals = _ten_god_signal_labels(ten_layers, tuple(child_labels))
    hour_god = _text(hour_layer.get("primary_ten_god"))
    hour_signals = _unique_texts([hour_god, *child_signals])
    paragraphs: list[str] = [
        _fallback_join(
            _pillar_brief("Trụ giờ", _mapping(bazi.get("hour_pillar"))),
            _layer_brief(hour_layer),
            "Trụ giờ chủ về con cái, hậu vận và những thành quả được bồi đắp trong thời gian dài. Vì vậy, phần này vừa cho thấy cách chủ mệnh nuôi dưỡng thế hệ sau, vừa phản ánh điều họ muốn để lại: một gia đình có nền nếp, một giá trị nghề nghiệp hay một công trình đủ sức đi xa hơn chính mình.",
        )
    ]
    if child_labels:
        paragraphs.append(
            "Sao tử tức cần quan sát: "
            + ", ".join(child_labels)
            + ". "
            + (
                "Trong lá số, các tín hiệu đang hiện rõ là " + ", ".join(child_signals) + ". Chúng mô tả khí chất của mối quan hệ cha mẹ - con cái và cách thành quả hậu vận hình thành, không dùng để kết luận máy móc về số lượng hay giới tính con."
                if child_signals
                else "Trong dữ liệu hiện tại chưa thấy sao tử tức lộ rõ, nên cần đọc kỹ trụ giờ và Đại vận thay vì kết luận vội."
            )
        )
    paragraphs.extend(_ten_god_reading_paragraphs("Luận con cái/hậu vận", hour_signals, CHILDREN_TEN_GOD_READINGS))
    luck_note = _luck_activation_note(payload)
    if luck_note:
        paragraphs.append(
            "Lá số gốc cho biết nền, còn thời điểm sinh con cần soi thêm Đại vận và Lưu niên. "
            + luck_note
        )
    if useful_line:
        paragraphs.append(
            useful_line
            + " Với kế hoạch sinh con, nên ưu tiên giai đoạn mà sức khỏe, tài chính và đời sống gia đình cùng có độ ổn định, đồng thời môi trường sống nâng được trục Dụng thần. Một ngày đẹp chỉ hỗ trợ điểm khởi đầu; nền khí bền của cha mẹ mới là điều nuôi dưỡng hành trình lâu dài."
        )
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


def _parents_domain_paragraphs(
    payload: Mapping[str, Any],
    ten_layers: Mapping[str, Any],
    useful_line: str,
) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    month_layer = _pillar_layer(ten_layers, "month")
    parent_signals = _ten_god_signal_labels(
        ten_layers,
        ("Chính Ấn", "Thiên Ấn", "Chính Tài", "Thiên Tài", "Chính Quan", "Thất Sát", "Tỷ Kiên", "Kiếp Tài"),
    )
    month_god = _text(month_layer.get("primary_ten_god"))
    focus_signals = _unique_texts([month_god, *parent_signals])
    paragraphs: list[str] = [
        _fallback_join(
            _pillar_brief("Trụ tháng", _mapping(bazi.get("month_pillar"))),
            _layer_brief(month_layer),
            "Trụ tháng là môi trường trưởng thành, cha mẹ, nghề nghiệp gốc và nhịp vận hành chính của mệnh. Vì vậy quan hệ với bố mẹ nên đọc như nền hình thành tính cách, kỷ luật, cách nhận hỗ trợ và cách bước vào xã hội.",
        )
    ]
    paragraphs.extend(_ten_god_reading_paragraphs("Luận nền bố mẹ", focus_signals, PARENTS_TEN_GOD_READINGS))
    if _has_any(focus_signals, ("Chính Ấn", "Thiên Ấn")):
        paragraphs.append(
            "Ấn tinh hiện rõ làm phần bố mẹ/nền nâng đỡ nghiêng về học hành, bảo hộ, uy tín hoặc niềm tin. Điểm tốt là có nền để đi đường dài; điểm cần chú ý là không nên sống mãi trong sự bảo hộ mà thiếu tự quyết."
        )
    if _has_any(focus_signals, ("Chính Tài", "Thiên Tài")):
        paragraphs.append(
            "Tài tinh ở tầng này cho thấy bài học gia đình gắn với tiền bạc, trách nhiệm, tài sản hoặc khả năng xoay xở vật chất. Khi luận cho khách, nên nói đây là bài học thực tế chứ không phán cha mẹ tốt/xấu một chiều."
        )
    if useful_line:
        paragraphs.append(
            useful_line
            + " Khi hòa giải hoặc tư vấn quan hệ gia đình, nên chọn cách giao tiếp làm mạnh trục Dụng thần: đúng khí thì dễ nói chuyện, sai khí thì cùng một việc cũng dễ thành áp lực."
        )
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


def _ancestry_domain_paragraphs(
    payload: Mapping[str, Any],
    ten_layers: Mapping[str, Any],
    shen_groups: Mapping[str, Any],
) -> list[str]:
    bazi = _mapping(payload.get("bazi"))
    year_layer = _pillar_layer(ten_layers, "year")
    year_god = _text(year_layer.get("primary_ten_god"))
    noble_group = _mapping(_mapping(shen_groups.get("groups")).get("noble_support"))
    relationship_group = _mapping(_mapping(shen_groups.get("groups")).get("relationship"))
    paragraphs: list[str] = [
        _fallback_join(
            _pillar_brief("Trụ năm", _mapping(bazi.get("year_pillar"))),
            _layer_brief(year_layer),
            "Trụ năm là tầng xa nhất: gốc phúc, nền gia tộc, môi trường sớm và khí hậu tinh thần ban đầu. Phần này nên giúp khách hiểu gốc nền của mình, không nên biến thành lời phán tuyệt đối về dòng họ.",
        )
    ]
    paragraphs.extend(_ten_god_reading_paragraphs("Luận gốc phúc", [year_god], ANCESTRY_TEN_GOD_READINGS))
    noble_brief = _group_brief(noble_group)
    if noble_brief:
        paragraphs.append(
            noble_brief
            + " Nhóm này có thể xem như tín hiệu nâng đỡ: gặp người hỗ trợ, dễ có cơ hội hóa giải hoặc trong khó khăn vẫn có đường học hỏi và xoay chuyển."
        )
    relationship_brief = _group_brief(relationship_group)
    if relationship_brief:
        paragraphs.append(
            relationship_brief
            + " Khi xuất hiện ở bản nền, các tín hiệu duyên quan hệ cho thấy đời sống gia tộc/môi trường sớm cũng để lại bài học về kết nối, sức hút và ranh giới cảm xúc."
        )
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


def _property_domain_paragraphs(payload: Mapping[str, Any], useful_line: str) -> list[str]:
    calendar = _mapping(payload.get("calendar"))
    five_elements = _mapping(payload.get("five_elements"))
    useful = _mapping(payload.get("useful_god"))
    counts = _mapping(five_elements.get("counts"))
    dominant = _element_label_list(five_elements.get("dominant")) or _element_extremes(counts, strongest=True)
    weak = _element_label_list(five_elements.get("missing")) or _element_extremes(counts, strongest=False)
    useful_element = _first_text(
        _extract_element_label(useful.get("useful_display")),
        _stem_element_label(_text(useful.get("useful_stem"))),
        _extract_element_label(useful.get("useful_element")),
    )
    cung_phi = _first_text(calendar.get("cung_phi"), calendar.get("menh_quai"))
    house_group = _first_text(calendar.get("nhom_trach"), calendar.get("house_group"))
    paragraphs: list[str] = [
        _fallback_join(
            f"Cung Phi/Mệnh quái: {cung_phi}." if cung_phi else "",
            f"Nhóm trạch: {house_group}." if house_group else "",
            "Điền trạch không chỉ nói về việc có nhà đất hay chọn một hướng đẹp. Quan trọng hơn, đó là khả năng tạo ra nơi ở và nơi làm việc giúp chủ mệnh hồi phục, tập trung, giữ tài sản và duy trì được nhịp sống ổn định qua nhiều năm.",
        )
    ]
    directions = _house_group_directions(house_group)
    if directions:
        paragraphs.append(
            f"Với {house_group}, các hướng {directions} là nhóm nên ưu tiên khi có đủ điều kiện lựa chọn. Tuy nhiên, hướng tốt chỉ phát huy khi đi cùng mặt bằng hợp lý, cửa đón khí thông thoáng, bếp và nơi nghỉ không xung đột, còn bàn làm việc phù hợp với mục tiêu sử dụng. Vì vậy không nên vì theo một hướng mà bỏ qua công năng và chất lượng sống thực tế."
        )
    if useful_element and useful_element in ELEMENT_SPACE_GUIDANCE:
        paragraphs.append(
            f"Ngũ hành cần nâng trong không gian là {useful_element}. {ELEMENT_SPACE_GUIDANCE[useful_element]} Khi được bổ trợ vừa đủ, ngôi nhà không chỉ đẹp về hình thức mà còn giúp chủ mệnh dễ trở về trạng thái cân bằng và dùng đúng sở trường của mình."
        )
    if dominant:
        paragraphs.append(
            "Hành nổi bật trong lá số là "
            + ", ".join(dominant)
            + ". Đây là khí đã có sẵn khá nhiều, nên bố trí nhà cửa không cần tiếp tục nhấn quá mạnh. Cách tốt hơn là giữ ưu điểm của hành này làm nền, sau đó dùng ánh sáng, vật liệu, màu sắc và độ thông thoáng để tiết chế, tránh khiến không gian làm tính khí vốn có trở nên cực đoan hơn."
        )
    if weak:
        weak_notes = [ELEMENT_SPACE_GUIDANCE[element] for element in weak if element in ELEMENT_SPACE_GUIDANCE]
        if weak_notes:
            paragraphs.append(
                "Hành còn yếu/thiếu là "
                + ", ".join(weak)
                + ". Phần yếu không đồng nghĩa cứ thêm thật nhiều là tốt; nên bồi có chủ đích, bắt đầu từ công năng và cảm nhận sống: "
                + " ".join(weak_notes)
            )
    if useful_line:
        paragraphs.append(
            useful_line
            + " Vì vậy, phong thủy phù hợp nhất là phong thủy có thể sống cùng mỗi ngày: hỗ trợ Dụng thần, thuận công năng, vừa khả năng tài chính và tạo cảm giác an định lâu dài."
        )
    return _unique_texts([paragraph for paragraph in paragraphs if paragraph])


def _ten_god_reading_paragraphs(prefix: str, signals: Sequence[str], readings: Mapping[str, str]) -> list[str]:
    paragraphs: list[str] = []
    for signal in signals:
        reading = readings.get(signal)
        if reading:
            paragraphs.append(f"{prefix}: {signal}. {reading}")
    return paragraphs


def _wealth_strength_guidance(strength_label: str) -> str:
    if strength_label in {"Thân vượng", "Thân quá vượng"}:
        return (
            f"Với thế {strength_label}, tài vận nên đi qua năng lực chủ động, sản phẩm rõ và kỷ luật giữ tiền. "
            "Người này có thể gánh cơ hội lớn hơn khi có hệ thống kiểm soát, nhưng nếu mở rộng bằng cảm xúc thì dễ tán tài hoặc ôm quá nhiều việc."
        )
    if strength_label in {"Thân nhược", "Thân quá nhược"}:
        return (
            f"Với thế {strength_label}, tài vận cần đi từng bước và mượn nền hệ thống, chuyên môn hoặc người hỗ trợ. "
            "Không nên dùng đòn bẩy quá sớm, vì cơ hội tiền lớn nhưng lực thân chưa đủ dễ biến thành áp lực."
        )
    return (
        f"Với thế {strength_label}, tài vận hợp cách cân bằng: vừa tạo giá trị đều, vừa giữ biên an toàn dòng tiền, "
        "không quá co cụm nhưng cũng không mở rộng khi dữ liệu vận chưa ủng hộ."
    )


def _career_strength_guidance(strength_label: str) -> str:
    if strength_label in {"Thân vượng", "Thân quá vượng"}:
        return (
            f"Với thế {strength_label}, nghề nghiệp cần có sân để dùng lực: vai trò tự chủ, điều phối, chịu trách nhiệm hoặc dẫn dắt sẽ dễ phát huy. "
            "Điểm cần tiết chế là sự cứng, ôm việc và phản ứng quá mạnh khi bị bó khuôn."
        )
    if strength_label in {"Thân nhược", "Thân quá nhược"}:
        return (
            f"Với thế {strength_label}, nghề nghiệp nên chọn nơi có quy trình, người nâng đỡ và lộ trình học rõ. "
            "Khi nền lực chưa đủ, việc nhảy vào môi trường quá cạnh tranh hoặc áp lực cao dễ làm mất nhịp phát triển."
        )
    return (
        f"Với thế {strength_label}, nghề nghiệp hợp nhịp vừa phải: có tự chủ nhưng vẫn có khuôn, có thử thách nhưng không để áp lực lấn át sức bền."
    )


def _marriage_strength_guidance(strength_label: str) -> str:
    if strength_label in {"Thân vượng", "Thân quá vượng"}:
        return (
            f"Với thế {strength_label}, trong quan hệ gần người này thường có lập trường mạnh và nhu cầu tự quyết cao. "
            "Hôn nhân bền hơn khi hai bên có ranh giới rõ, biết nhường nhịp và không biến cái tôi thành cuộc hơn thua."
        )
    if strength_label in {"Thân nhược", "Thân quá nhược"}:
        return (
            f"Với thế {strength_label}, hôn nhân cần cảm giác an toàn, sự nâng đỡ và nhịp sống ổn định. "
            "Người này không nên bước vào quan hệ chỉ vì áp lực bên ngoài, vì dễ tự mất tiếng nói khi nền lực chưa vững."
        )
    return (
        f"Với thế {strength_label}, quan hệ cần sự cân bằng giữa độc lập và nương tựa. "
        "Điểm tốt là dễ thương lượng nếu cả hai giữ được nhịp giao tiếp đều và không dồn cảm xúc quá lâu."
    )


def _spouse_star_labels(payload: Mapping[str, Any]) -> list[str]:
    customer = _mapping(payload.get("customer"))
    identity = _mapping(payload.get("identity"))
    person = _mapping(identity.get("person"))
    gender = _first_text(customer.get("gender"), person.get("gender"), customer.get("gender_label"), person.get("gender_label")).lower()
    if gender in {"male", "nam", "m"}:
        return ["Chính Tài", "Thiên Tài"]
    if gender in {"female", "nữ", "nu", "f"}:
        return ["Chính Quan", "Thất Sát"]
    return []


def _child_star_labels(payload: Mapping[str, Any]) -> list[str]:
    customer = _mapping(payload.get("customer"))
    identity = _mapping(payload.get("identity"))
    person = _mapping(identity.get("person"))
    gender = _first_text(customer.get("gender"), person.get("gender"), customer.get("gender_label"), person.get("gender_label")).lower()
    if gender in {"male", "nam", "m"}:
        return ["Chính Quan", "Thất Sát"]
    if gender in {"female", "nữ", "nu", "f"}:
        return ["Thực Thần", "Thương Quan"]
    return []


def _luck_activation_note(payload: Mapping[str, Any]) -> str:
    luck = _mapping(payload.get("luck"))
    current = _mapping(luck.get("current_cycle"))
    cycles = [item for item in _list(luck.get("cycles")) if isinstance(item, Mapping)]
    current_text = _fallback_join(_text(current.get("gan_zhi")), _age_range(current), _year_range(current))
    first_cycle = _mapping(cycles[0]) if cycles else {}
    first_text = _fallback_join(_text(first_cycle.get("gan_zhi")), _age_range(first_cycle), _year_range(first_cycle))
    if current_text:
        return f"Vận hiện tại {current_text} cho biết bối cảnh đang kích hoạt; nếu vận này hợp Dụng thần thì kế hoạch con cái/hậu vận dễ thuận hơn, còn nếu kích điểm kỵ thì nên chuẩn bị nền sức khỏe, tài chính và nhịp sống kỹ hơn."
    if first_text:
        return f"Các Đại vận như {first_text} cần được dùng để chọn giai đoạn, vì trụ giờ chỉ cho nền, còn vận mới cho biết thời điểm nào phần con cái/hậu vận mở rõ."
    return ""


def _house_group_directions(house_group: str) -> str:
    text = _text(house_group)
    if "Đông" in text or "Dong" in text:
        return "Đông, Đông Nam, Nam, Bắc"
    if "Tây" in text or "Tay" in text:
        return "Tây, Tây Bắc, Tây Nam, Đông Bắc"
    return ""


def _has_any(values: Sequence[str], expected: Sequence[str]) -> bool:
    value_set = set(values)
    return any(item in value_set for item in expected)


def _element_health_note(element: str, *, excess: bool) -> str:
    element = _element_label(element)
    area = ELEMENT_HEALTH_AREAS.get(element, "")
    note = (ELEMENT_HEALTH_EXCESS if excess else ELEMENT_HEALTH_WEAK).get(element, "")
    if area and note:
        return f"Theo hệ quy chiếu truyền thống, {element} liên quan {area}. {note}"
    return note


def _health_relation_paragraphs(
    payload: Mapping[str, Any],
    counts: Mapping[str, Any],
    dominant: Sequence[str],
    weak: Sequence[str],
) -> list[str]:
    paragraphs: list[str] = []
    count_values = {_element_label(label): _element_count(counts, label) for label in ELEMENT_HEALTH_AREAS}
    dominant_set = {_element_label(element) for element in dominant}
    weak_set = {_element_label(element) for element in weak}

    for source, target in ELEMENT_GENERATES.items():
        source_score = count_values.get(source, 0.0)
        target_score = count_values.get(target, 0.0)
        if source in dominant_set and target_score >= 3:
            if source == "Thổ" and target == "Kim":
                paragraphs.append(
                    "Luận theo quan hệ sinh: Thổ vượng sinh Kim, nên khí Kim không chỉ được tính riêng ở bảng Ngũ hành mà còn được Thổ đẩy thêm. Vì Kim liên hệ hô hấp, phổi, mũi xoang, da và đại tràng, người có thế này nên chủ động giữ môi trường sống sạch, đủ ẩm, tránh lạnh/khô kéo dài; các biểu hiện như viêm xoang, dị ứng hoặc nhạy đường hô hấp cần được xem là điểm phòng ngừa sớm."
                )
            else:
                target_area = ELEMENT_HEALTH_AREAS.get(target, "")
                paragraphs.append(
                    f"Luận theo quan hệ sinh: {source} vượng sinh {target}, làm vùng {target} được kích hoạt thêm. Theo hệ quy chiếu truyền thống, {target} liên quan {target_area}; vì vậy khi {source} quá nổi, phần {target} cũng cần được điều hòa chứ không chỉ nhìn số lượng riêng của {target}."
                )

    for source, target in ELEMENT_CONTROLS.items():
        source_score = count_values.get(source, 0.0)
        target_score = count_values.get(target, 0.0)
        if source_score >= 3 and target_score > 0:
            if source == "Hỏa" and target == "Kim":
                paragraphs.append(
                    "Luận theo quan hệ khắc: Hỏa khắc Kim. Khi Hỏa đủ lực ép vào Kim, vùng Kim dễ bị căng, khô hoặc phản ứng mạnh hơn; vì vậy cần lưu ý nhịp thở, phổi, mũi xoang, da, đại tràng và cả trạng thái căng thẳng do áp lực công việc. Nếu Thủy cũng yếu, phần xương khớp, giấc ngủ sâu và sức bền nền càng cần được giữ bằng nghỉ ngơi đúng giờ, vận động đều và giảm hao sức kéo dài."
                )
            elif source == "Thổ" and target == "Thủy" and ("Thủy" in weak_set or count_values.get("Thủy", 0.0) <= 1):
                paragraphs.append(
                    "Luận theo quan hệ khắc: Thổ mạnh khắc Thủy. Khi Thủy đã yếu, dấu hiệu này làm phần thận khí, tiết niệu, xương khớp, giấc ngủ sâu và sức bền nền càng cần được bồi dưỡng đều, tránh để công việc hoặc sinh hoạt thất thường rút cạn nền hồi phục."
                )

    pressure_signals = _health_pressure_signals(payload)
    if pressure_signals:
        paragraphs.append(
            "Về mặt tinh thần - công việc, lá số có tín hiệu "
            + ", ".join(pressure_signals)
            + ". Đây là nhóm sao/hành dễ tạo trách nhiệm, khuôn phép hoặc sức ép phải gánh việc; khi đi cùng Hỏa-Kim căng, sức khỏe nên được quản trị bằng cách giảm dồn deadline, giữ lịch ngủ ổn định và có nhịp xả áp đều."
        )

    return paragraphs


def _health_pressure_signals(payload: Mapping[str, Any]) -> list[str]:
    signals: list[str] = []
    ten_layers = build_ten_gods_four_layer_view(payload)
    ten_god_signals = _ten_god_signal_labels(ten_layers, ("Chính Quan", "Thất Sát"))
    if ten_god_signals:
        signals.extend(ten_god_signals)
    useful_god = _mapping(payload.get("useful_god"))
    useful_display = _text(useful_god.get("useful_display"))
    useful_stem = _text(useful_god.get("useful_stem"))
    if "Hỏa" in {useful_display, _stem_element_label(useful_stem)}:
        signals.append("Hỏa được kích hoạt")
    return _unique_texts(signals)


def _element_count(counts: Mapping[str, Any], label: str) -> float:
    normalized = _element_label(label)
    for key, element_label in ELEMENT_LABELS.items():
        if element_label != normalized:
            continue
        try:
            return float(counts.get(key, 0) or 0)
        except (TypeError, ValueError):
            return 0.0
    try:
        return float(counts.get(normalized, 0) or 0)
    except (TypeError, ValueError):
        return 0.0


def _stem_element_label(stem: str) -> str:
    return HEAVENLY_STEM_ELEMENTS.get(_text(stem), "")


def _extract_element_label(value: Any) -> str:
    text = _text(value)
    normalized = _element_label(text)
    if normalized in ELEMENT_HEALTH_AREAS:
        return normalized
    for label in ELEMENT_HEALTH_AREAS:
        if label in text:
            return label
    return ""


def _useful_element_labels(useful_god: Mapping[str, Any]) -> list[str]:
    """Return only customer-published Dụng/Hỷ elements.

    ``canonical_favorable_display`` is an internal candidate trace. It may
    contain a lower-ranked balancing or climate candidate even when the Hỷ
    thần gate deliberately publishes no separate Hỷ thần. Mixing that field
    into customer prose incorrectly promotes those candidates to the same
    level as the selected Dụng thần.
    """
    labels: list[str] = []
    labels.append(_extract_element_label(useful_god.get("useful_display")))
    labels.append(_extract_element_label(useful_god.get("useful_element")))
    labels.append(_stem_element_label(_text(useful_god.get("useful_stem"))))
    labels.extend(_element_labels_from_text(useful_god.get("favorable_display")))
    return _unique_texts(labels)


def _unfavorable_element_labels(useful_god: Mapping[str, Any]) -> list[str]:
    labels: list[str] = []
    labels.append(_extract_element_label(useful_god.get("unfavorable_display")))
    labels.extend(_element_labels_from_text(useful_god.get("unfavorable_display")))
    return _unique_texts(labels)


def _element_labels_from_text(value: Any) -> list[str]:
    text = _text(value)
    return [label for label in ELEMENT_HEALTH_AREAS if label in text]


def _element_controlling(element: str) -> str:
    normalized = _element_label(element)
    for source, target in ELEMENT_CONTROLS.items():
        if target == normalized:
            return source
    return ""


def _element_generating(element: str) -> str:
    normalized = _element_label(element)
    for source, target in ELEMENT_GENERATES.items():
        if target == normalized:
            return source
    return ""


def _element_extremes(counts: Mapping[str, Any], *, strongest: bool) -> list[str]:
    values: list[tuple[str, float]] = []
    for key in ("wood", "fire", "earth", "metal", "water"):
        try:
            values.append((ELEMENT_LABELS[key], float(counts.get(key))))
        except (TypeError, ValueError):
            continue
    if not values:
        return []
    target = max(score for _, score in values) if strongest else min(score for _, score in values)
    if target <= 0 and strongest:
        return []
    return [label for label, score in values if score == target]


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
    meaning = _ten_god_meaning(god)
    return _fallback_join(
        f"Khí chính tại vị trí này là {god}." if god else "",
        f"Trong đời sống, khí này thường biểu hiện qua {meaning}." if meaning else "",
        f"Phạm vi ảnh hưởng gắn với {hint.rstrip('.').lower()}." if hint else "",
    )


def _ten_god_meaning(god: str) -> str:
    return TEN_GOD_PUBLIC_MEANINGS.get(_text(god), "")


def _group_brief(group: Mapping[str, Any]) -> str:
    items = [item for item in _list(group.get("items")) if isinstance(item, Mapping)]
    names = _unique_texts([item.get("name") for item in items if _text(item.get("name"))])
    if not names:
        return ""
    return "Tín hiệu Thần sát liên quan: " + ", ".join(names) + "."


def _is_low_value_domain_summary(summary: str) -> bool:
    text = _text(summary).lower()
    low_value_fragments = (
        "nên đọc từ",
        "nên đọc cùng",
        "lấy trụ",
        "đọc từ",
        "đọc nhiều ở trụ",
        "đọc qua",
        "đọc cùng cung phi",
        "nên đặt trên",
    )
    return any(fragment in text for fragment in low_value_fragments)


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
    canonical_favorable = _text(useful_god.get("canonical_favorable_display"))
    if favorable and not favorable.startswith("Chưa đủ căn cứ"):
        parts.append(f"Hỷ thần/bổ trợ: {favorable}.")
    elif canonical_favorable and canonical_favorable != display:
        parts.append(f"Nhóm bổ trợ có thể đi cùng: {canonical_favorable}.")
    unfavorable = _text(useful_god.get("unfavorable_display"))
    if unfavorable:
        parts.append(f"Kỵ thần cần tiết chế: {unfavorable}.")
    reason = _useful_god_reason(useful_god, display)
    if reason:
        parts.append(reason)
    return " ".join(parts)


def _useful_god_domain_lead(useful_god: Mapping[str, Any]) -> str:
    display = _first_text(
        useful_god.get("useful_display"),
        useful_god.get("useful_stem"),
        useful_god.get("useful_element"),
    )
    return f"Trục điều tiết của lá số là {display}." if display else ""


def _five_elements_summary(five_elements: Mapping[str, Any]) -> str:
    dominant = _element_label_list(five_elements.get("dominant"))
    missing = _element_label_list(five_elements.get("missing"))
    counts = _mapping(five_elements.get("counts"))
    distribution = _element_distribution(counts)
    parts: list[str] = []
    if distribution:
        parts.append("Phân bố Ngũ hành: " + distribution + ".")
    if dominant:
        parts.append("Hành nổi bật: " + ", ".join(dominant) + ".")
    if missing:
        parts.append("Hành còn thiếu hoặc yếu: " + ", ".join(missing) + ".")
    if dominant or missing:
        parts.append("Phần này cho biết khí nào dễ lộ ra trong tính cách, sức bền và cách xử lý việc, nhưng vẫn phải đọc cùng mùa sinh, Thân vượng/nhược và Dụng thần.")
    return " ".join(parts)


def _strength_summary(strength: Mapping[str, Any], pattern: Mapping[str, Any]) -> str:
    label = _strength_label(_first_text(strength.get("strength_level"), pattern.get("than_vuong_nhuoc")))
    reasoning = _first_text(strength.get("reasoning"), pattern.get("than_vuong_nhuoc"))
    guidance = STRENGTH_PUBLIC_GUIDANCE.get(label, "")
    parts = _non_empty(
        [
            f"Thế thân được đánh giá là {label}." if label else "",
            "Căn cứ được tổng hợp từ mùa sinh, căn khí, lực sinh trợ, lực tiết khí và lực khắc chế trong toàn bộ Tứ trụ." if label else "",
            f"Lý do chính: {reasoning}." if reasoning and reasoning != label else "",
            guidance,
        ]
    )
    return " ".join(parts)


def _structure_summary(pattern: Mapping[str, Any]) -> str:
    structure = _first_text(pattern.get("cach_cuc"), pattern.get("pattern"))
    if not structure:
        return ""
    month_branch = _text(pattern.get("month_branch"))
    main_qi = _text(pattern.get("month_main_qi"))
    main_god = _text(pattern.get("month_main_qi_ten_god"))
    grade = _text(pattern.get("structural_grade"))
    purity = _text(pattern.get("structural_purity"))
    force = _text(pattern.get("structural_strength"))
    integrity = _text(pattern.get("structural_integrity"))
    basis = _fallback_join(
        f"nguyệt lệnh {month_branch}" if month_branch else "",
        f"khí chính {main_qi}" if main_qi else "",
        f"ứng với {main_god}" if main_god else "",
    )
    quality = ", ".join(
        _non_empty(
            [
                f"độ thuần {purity}" if purity else "",
                f"lực cách {force}" if force else "",
                f"mức toàn vẹn {integrity}" if integrity else "",
                f"hạng {grade}" if grade else "",
            ]
        )
    )
    parts = [f"Mệnh cục nghiêng về {structure}."]
    if basis:
        parts.append(f"Căn cứ chính nằm ở {basis}; đây là lý do phần Mệnh cục không chỉ lấy tên gọi mà phải đối chiếu từ trụ tháng và khí chủ đạo.")
    if quality:
        parts.append(f"Chất lượng cấu trúc: {quality}.")
    return " ".join(parts)


def _useful_god_reason(useful_god: Mapping[str, Any], display: str) -> str:
    customer_reason = _mapping(useful_god.get("customer_reason"))
    action = _text(customer_reason.get("balancing_action"))
    target = _text(customer_reason.get("target_element"))
    source = _text(customer_reason.get("source_element"))
    role = _text(customer_reason.get("candidate_ten_god"))
    if action and target:
        bridge = _fallback_join(
            f"Nhật chủ thuộc hành {source}" if source else "",
            f"nên cần {action} về hành {target}" if target else "",
            f"thông qua vai trò {role}" if role else "",
        )
        return f"{bridge if bridge else 'Lá số cần điều tiết khí mệnh'}, vì vậy {display} được dùng làm trục điều tiết chính. Đây là câu trả lời cho phần 'dựa vào đâu': Dụng thần được chọn để xử lý điểm lệch của toàn cục, không phải chỉ vì một hành đang thiếu hay đang nhiều trên bảng Ngũ hành."
    public_reason = _public_reason_text(useful_god)
    if public_reason:
        return public_reason
    return "Dụng thần nên được hiểu là hướng điều tiết giúp lá số vận hành thuận hơn; khi ứng dụng vào nghề nghiệp, tài vận, hôn nhân hay phong thủy, cần ưu tiên các lựa chọn làm mạnh thêm trục này."


def _public_reason_text(useful_god: Mapping[str, Any]) -> str:
    reason = _first_text(useful_god.get("reasoning"), useful_god.get("short_reason"))
    blocked_fragments = ("V1.0", "rule", "Rule", "candidate", "matched")
    if any(fragment in reason for fragment in blocked_fragments):
        return ""
    return reason


def _strength_label(value: Any) -> str:
    text = _text(value)
    return STRENGTH_LABELS.get(text, text)


def _element_distribution(counts: Mapping[str, Any]) -> str:
    labels: list[str] = []
    for key in ("wood", "fire", "earth", "metal", "water"):
        value = counts.get(key)
        if value is None:
            continue
        labels.append(f"{ELEMENT_LABELS[key]} {value}")
    return ", ".join(labels)


def _year_range(item: Mapping[str, Any]) -> str:
    start = item.get("year_start")
    end = item.get("year_end")
    if start is not None and end is not None:
        return f"{start}-{end}"
    if start is not None:
        return f"từ {start}"
    return ""


def _element_label(value: Any) -> str:
    text = _text(value)
    return ELEMENT_LABELS.get(text, text)


def _element_label_list(value: Any) -> list[str]:
    return _unique_texts([_element_label(item) for item in _text_list(value)])


def _ten_gods_summary(four_layer: Mapping[str, Any]) -> str:
    layers = [item for item in _list(four_layer.get("layers")) if isinstance(item, Mapping)]
    labels = []
    meanings = []
    for item in layers:
        label = _first_text(item.get("label"), item.get("pillar"))
        god = _text(item.get("primary_ten_god"))
        if label and god:
            labels.append(f"{label}: {god}")
            meaning = _ten_god_meaning(god)
            if meaning:
                meanings.append(f"{label} hiện {god}, chủ về {meaning}")
    if not labels:
        return ""
    summary = "Thập thần theo 4 trụ: " + "; ".join(labels) + "."
    if meanings:
        summary += " Luận theo 4 tầng: " + "; ".join(meanings) + "."
    return summary


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
    if isinstance(value, Mapping | list | tuple):
        return ""
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
