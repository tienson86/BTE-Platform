"""Frozen V1 narrative catalog copied from the two canonical knowledge files."""

from __future__ import annotations

from typing import Final

PURPOSE_FOCUS_VI: Final[dict[str, str]] = {
    "phone_number": (
        "Với số điện thoại, theo hệ thống này nên đọc thiên về giao tiếp, "
        "quan hệ, tài khí, nhịp sự nghiệp và mức dùng hằng ngày."
    ),
    "car_plate": (
        "Với biển số xe hơi, theo hệ thống này nên đọc thiên về chuyển động, "
        "biểu tượng an toàn, di chuyển công việc, ổn định tài sản và dòng tiền."
    ),
    "motorbike_plate": (
        "Với biển số xe máy, theo hệ thống này nên đọc thiên về di chuyển "
        "hằng ngày, nhịp cá nhân và biểu tượng an toàn thực tế."
    ),
    "id_number": (
        "Với số định danh, theo hệ thống này nên đọc thiên về dấu ấn dài hạn, "
        "chủ đề đời sống và sự tương hợp với chủ số khi có thêm dữ liệu."
    ),
    "bank_account": (
        "Với số tài khoản, theo hệ thống này nên đọc thiên về dòng tiền, "
        "khả năng giữ tài, rủi ro và sự ổn định giao dịch."
    ),
    "house_number": (
        "Với số nhà, theo hệ thống này nên đọc thiên về ổn định gia đình, "
        "nghỉ ngơi, sức khỏe theo nghĩa năng lượng và trường dài hạn."
    ),
    "generic_number": (
        "Với dãy số generic, V1 chỉ đọc năng lượng nội tại của số, "
        "chưa kết luận tương hợp chủ số."
    ),
}

CANONICAL_CUSTOMER_COPY: Final[dict[str, str]] = {
    "103": (
        "Dãy này có nền Thiên Y, thiên về tài khí/phúc khí/tình cảm ổn định, "
        "nhưng biểu hiện không lộ mạnh vì bị âm trường che."
    ),
    "153": (
        "Dãy này kích hoạt Thiên Y mạnh, phù hợp khi cần tăng tài khí, "
        "phúc khí và sự ổn định trong quan hệ."
    ),
    "108": (
        "Dãy này có nền Ngũ Quỷ bị che bởi âm trường. Không nên kết luận là "
        "đã mất hẳn biến động; nên xem thêm các cặp sau đó có Sinh Khí chế ước hay không."
    ),
    "141319": (
        "Đây là chuỗi cát tinh mạnh, đi theo trật tự hỗ trợ: mở cơ hội, "
        "tăng tài khí/phúc khí, rồi đưa về ổn định và trách nhiệm."
    ),
    "1414": (
        "Dãy này nhấn rất mạnh Sinh Khí, hợp để mở quan hệ và cơ hội. "
        "Nếu dùng quá nhiều, nên phối thêm trường tạo kỷ luật và ổn định."
    ),
    "219": (
        "Dãy này có một phần quyết liệt/mạo hiểm rất mạnh, sau đó đi vào "
        "xu hướng ổn định và trách nhiệm. Tuy nhiên, theo V1, cần Thiên Y "
        "để chế Tuyệt Mệnh; Diên Niên chỉ giúp tăng kỷ luật, không thay thế vai trò Thiên Y."
    ),
    "216": (
        "Dãy này có tổ hợp quyết liệt/mạo hiểm đi cùng cảm xúc và quan hệ "
        "dễ biến động. Cần phối thêm cát tinh phù hợp nếu dùng trong ngữ cảnh quan trọng."
    ),
}

ENERGY_CATALOG: Final[dict[str, dict[str, str]]] = {
    "sheng_qi": {
        "customer_summary": (
            "Sinh Khí thiên về quý nhân, cơ hội và khả năng mở đường. "
            "Khi xuất hiện hợp lý, dãy số thường hỗ trợ giao tiếp, kết nối "
            "và khả năng gặp trợ lực đúng lúc."
        ),
        "shadow": "thiếu quyết đoán, thiếu động lực, dễ hài lòng sớm",
        "excessive_effect": (
            "quá tùy duyên, dễ lười, thiếu chủ kiến, dựa vào may mắn"
        ),
        "health": "theo hệ thống này, cần lưu ý dạ dày và vùng tai-mắt-mũi",
        "remedy_relation": "Sinh Khí chế/giáng Ngũ Quỷ",
        "expert_notes": (
            "Không diễn giải Sinh Khí là may mắn tuyệt đối. Nếu lặp quá nhiều, "
            "cần kiểm tra trạng thái REPEATED hoặc AMPLIFIED."
        ),
        "recommended_context": (
            "số cần mở quan hệ, tăng cơ hội, hỗ trợ kinh doanh mềm"
        ),
        "avoid_context": (
            "mục tiêu cần kỷ luật cao, quyết định nhanh, cạnh tranh mạnh "
            "nếu thiếu năng lượng ổn định"
        ),
    },
    "tian_yi": {
        "customer_summary": (
            "Thiên Y thiên về tài vận, tình duyên và phúc khí. Khi đặt đúng vị trí, "
            "đây là trường thuận lợi cho đời sống vật chất và quan hệ."
        ),
        "shadow": (
            "quá thiện lương, dễ bị lợi dụng, tiền vào nhưng quản tiền chưa chắc tốt"
        ),
        "excessive_effect": (
            "mất cân bằng tiền bạc hoặc tình cảm nếu thiếu trường điều tiết"
        ),
        "health": "theo hệ thống này, liên hệ tuần hoàn, huyết áp, tai-mắt-mũi",
        "remedy_relation": "Thiên Y chế Tuyệt Mệnh",
        "expert_notes": (
            "Customer-facing copy phải tránh biến phần sức khỏe thành chẩn đoán y khoa."
        ),
        "recommended_context": (
            "tài vận, hôn nhân, quan hệ ổn định, sức khỏe theo nghĩa năng lượng"
        ),
        "avoid_context": (
            "mục tiêu cần sự sắc bén, ranh giới rõ, cạnh tranh quyết liệt nếu thiếu Diên Niên"
        ),
    },
    "yan_nian": {
        "customer_summary": (
            "Diên Niên là trường của sự nghiệp và sự ổn định. Nó phù hợp với người "
            "cần quyền hạn, khả năng quản lý, trách nhiệm và nền tảng lâu dài."
        ),
        "shadow": "cứng, cố chấp, khó nghe ý kiến",
        "excessive_effect": "lao lực, kiểm soát quá mức, gây áp lực cho người khác",
        "health": "theo hệ thống này, cần lưu ý vai gáy, thần kinh, mất ngủ, stress",
        "remedy_relation": "Diên Niên chế Lục Sát",
        "expert_notes": (
            "Khi lặp quá nhiều, phải cảnh báo áp lực và khuynh hướng kiểm soát."
        ),
        "recommended_context": "công việc, quản trị, người cần ổn định sự nghiệp và giữ tài",
        "avoid_context": (
            "mục tiêu cần mềm dẻo cảm xúc nếu thiếu Sinh Khí hoặc Thiên Y"
        ),
    },
    "fu_wei": {
        "customer_summary": (
            "Phục Vị là năng lượng duy trì. Khi đi sau trường tốt, nó giúp ổn định "
            "và kéo dài lợi thế; khi đi sau trường bất lợi, nó có thể làm trạng thái "
            "đó kéo dài hơn."
        ),
        "shadow": "bảo thủ, chần chừ, dễ bỏ lỡ cơ hội",
        "excessive_effect": "trì trệ, bị động, khó thay đổi, kéo dài trạng thái hiện có",
        "health": "theo hệ thống này, liên hệ tim, não và trạng thái tích tụ",
        "remedy_relation": (
            "Phục Vị được Sinh Khí hoặc Thiên Y hỗ trợ; Phục Vị không tự hóa giải hung tinh mạnh"
        ),
        "expert_notes": (
            "Phục Vị vừa có ý nghĩa riêng, vừa có khả năng kéo dài hoặc khuếch đại "
            "trường khí đứng trước tùy chuỗi."
        ),
        "recommended_context": "công việc tĩnh, nghiên cứu, giữ ổn định, bảo toàn",
        "avoid_context": (
            "giai đoạn cần bứt phá nhanh nếu không có Sinh Khí hoặc Thiên Y hỗ trợ"
        ),
    },
    "huo_hai": {
        "customer_summary": (
            "Họa Hại không chỉ là trường của thị phi mà còn là trường của ngôn ngữ. "
            "Nếu dùng đúng, nó tạo khả năng ăn nói và thuyết phục; nếu quá mạnh, "
            "lời nói dễ trở thành nguồn gây tranh chấp."
        ),
        "shadow": "nóng lời, thích thắng lời, để tâm chuyện vụn vặt, dễ gây tranh chấp",
        "excessive_effect": (
            "mâu thuẫn kéo dài, tổn hại quan hệ, phá tài vì lời nói hoặc kiện tụng"
        ),
        "health": (
            "theo hệ thống này, cần lưu ý khoang miệng, họng, khí quản, "
            "tuyến bạch huyết, vùng ngực và mệt mỏi"
        ),
        "remedy_relation": (
            "Họa Hại cần phối hợp cát tinh; không khóa một cặp hóa giải đơn trong V1"
        ),
        "expert_notes": (
            "Không diễn giải Họa Hại chỉ là xấu. Trong nghề nghiệp dùng ngôn ngữ, "
            "nó có thể trở thành năng lực nếu được cát tinh điều phối."
        ),
        "recommended_context": (
            "nghề cần nói, thương lượng, giảng dạy, bán hàng, truyền thông nếu có cát tinh phối hợp"
        ),
        "avoid_context": (
            "hôn nhân, hợp tác nhạy cảm, môi trường cần hòa khí nếu Họa Hại quá mạnh"
        ),
    },
    "wu_gui": {
        "customer_summary": (
            "Ngũ Quỷ là trường biến động mạnh. Nó có thể tạo tài năng sáng tạo và "
            "khả năng đổi mới, nhưng nếu thiếu cân bằng sẽ khiến công việc, "
            "tài chính và tình cảm khó ổn định."
        ),
        "shadow": "bất ổn, nghi ngờ, thay đổi nhanh, khó duy trì cam kết",
        "excessive_effect": (
            "cuộc sống biến động liên tục, công việc/tài chính/tình cảm khó ổn định"
        ),
        "health": "theo hệ thống này, cần lưu ý tim, tuần hoàn và trạng thái đột phát",
        "remedy_relation": "Sinh Khí chế/giáng Ngũ Quỷ",
        "expert_notes": (
            "Với Ngũ Quỷ, ưu tiên kiểm tra có chuỗi Sinh Khí hỗ trợ hoặc chuỗi "
            "chế ước đã được catalog trong interaction rules hay không."
        ),
        "recommended_context": (
            "sáng tạo, kinh doanh linh hoạt, cải tổ, môi trường cần ý tưởng mới"
        ),
        "avoid_context": (
            "mục tiêu cần ổn định gia đạo, tài chính đều, tâm lý an định nếu thiếu Sinh Khí chế ước"
        ),
    },
    "liu_sha": {
        "customer_summary": (
            "Lục Sát làm mạnh cảm xúc và khả năng kết nối. Nó có thể tạo sức hút "
            "và năng lực giao tiếp tốt, nhưng cũng dễ khiến đời sống tình cảm "
            "trở nên phức tạp nếu xuất hiện quá mạnh."
        ),
        "shadow": "đa nghi, do dự, vướng tình, dễ để quan hệ biến động",
        "excessive_effect": (
            "quan hệ và tâm lý mất ổn định, tình cảm phức tạp, công việc thiếu quyết tâm"
        ),
        "health": "theo hệ thống này, cần lưu ý da, dạ dày và stress cảm xúc",
        "remedy_relation": "Diên Niên chế Lục Sát",
        "expert_notes": (
            "Không nói đơn giản “xấu cho tình duyên”; phải diễn giải là trường "
            "cảm xúc và quan hệ mạnh nhưng thiếu ổn định."
        ),
        "recommended_context": (
            "nghề giao tiếp, dịch vụ, ngoại giao, thẩm mỹ nếu có Diên Niên kiểm soát"
        ),
        "avoid_context": (
            "hôn nhân hoặc hợp tác cần ranh giới rõ nếu Lục Sát quá mạnh và không được chế"
        ),
    },
    "jue_ming": {
        "customer_summary": (
            "Tuyệt Mệnh là trường quyết liệt và mạo hiểm. Nó không hoàn toàn vô dụng; "
            "trong một số môi trường cạnh tranh hoặc đầu tư, đặc tính này có thể tạo "
            "lợi thế, nhưng phải được kiểm soát chặt."
        ),
        "shadow": "xung động, mạo hiểm, tự cho là đúng, dễ đi cực đoan",
        "excessive_effect": (
            "tài chính và quan hệ lên xuống mạnh, hao tổn vì quyết định nhanh"
        ),
        "health": (
            "theo hệ thống này, cần lưu ý gan, thận, hệ tiết niệu và trạng thái quá sức"
        ),
        "remedy_relation": "Thiên Y chế Tuyệt Mệnh",
        "expert_notes": (
            "Không diễn giải Tuyệt Mệnh như tai họa tuyệt đối. Luôn kiểm tra ngữ cảnh, "
            "mục đích sử dụng và cát tinh chế ước."
        ),
        "recommended_context": (
            "cạnh tranh, đầu tư, kinh doanh rủi ro, môi trường cần quyết đoán nếu có Thiên Y chế ước"
        ),
        "avoid_context": (
            "người cần an toàn tài chính, hôn nhân ổn định, sức khỏe cân bằng nếu Tuyệt Mệnh quá mạnh"
        ),
    },
}
