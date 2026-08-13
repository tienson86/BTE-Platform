"""Deterministic paragraph realization from CommercialLanguageInput."""

from __future__ import annotations

from applications.production.language.models import (
    CommercialLanguageInput,
    ConsultingParagraph,
    FeatureKind,
    ParagraphIntent,
    ParagraphStatus,
)
from applications.production.language import plain_language as pl


def realize_paragraph(data: CommercialLanguageInput) -> ConsultingParagraph:
    """Build one ConsultingParagraph — no randomness, no invented facts."""
    claims = list(data.claims) + list(data.supporting_claims)
    if not any(
        [
            data.claims,
            data.supporting_claims,
            data.actionability,
            data.limitations,
            data.memory_candidate,
            data.primary_theme,
            data.operating_style,
            data.capacity_cue,
            data.structure_cue,
            data.balance_cue,
        ]
    ):
        return ConsultingParagraph(
            intent=data.intent,
            status=ParagraphStatus.INSUFFICIENT,
            prose="Chưa đủ dữ liệu đã công bố để viết đoạn này.",
            source_claim_ids=[],
        )

    handlers = {
        ParagraphIntent.OBSERVATION: _observation,
        ParagraphIntent.RECOGNITION: _recognition,
        ParagraphIntent.WORK_STYLE: _work_style,
        ParagraphIntent.SUPPORT: _support,
        ParagraphIntent.LIMITATION: _limitation,
        ParagraphIntent.CONDITION: _condition,
        ParagraphIntent.PRESSURE_RESPONSE: _pressure,
        ParagraphIntent.ENVIRONMENT: _environment,
        ParagraphIntent.INSIGHT: _insight,
        ParagraphIntent.ACTION: _action,
        ParagraphIntent.CLOSING: _closing,
        ParagraphIntent.CONTRAST: _contrast,
    }
    handler = handlers.get(data.intent, _observation)
    paragraph = handler(data)
    paragraph.source_claim_ids = claims[:8]
    paragraph.prose = _join_prose(paragraph)
    if not paragraph.prose.strip():
        paragraph.status = ParagraphStatus.INSUFFICIENT
        paragraph.prose = "Chưa đủ dữ liệu đã công bố để viết đoạn này."
    return paragraph


def _join_prose(paragraph: ConsultingParagraph) -> str:
    parts = [
        paragraph.recognition,
        paragraph.meaning,
        paragraph.implication,
        paragraph.action,
        paragraph.limitation,
        paragraph.memory_line,
    ]
    return " ".join(p.strip() for p in parts if p and p.strip())


def _is_follow(structure: str) -> bool:
    low = (structure or "").lower()
    return "tòng" in low or "tong" in low


def _is_output(data: CommercialLanguageInput) -> bool:
    style = data.operating_style or ""
    return data.primary_theme == "OPERATING_OUTPUT" or "Thương Quan" in style or "Thực Thần" in style


def _observation(data: CommercialLanguageInput) -> ConsultingParagraph:
    theme = pl.plain_theme(data.primary_theme)
    style = pl.plain_style(data.operating_style)
    capacity = pl.plain_capacity(data.capacity_cue)
    structure = pl.structure_to_plain(data.structure_cue)
    follow = _is_follow(data.structure_cue)

    if data.primary_theme == "OPERATING_SELF_CARRY":
        meaning = "Điểm nhận diện chính: bạn dễ tự gánh và tự đẩy tiến độ."
        if style:
            meaning += f" Điều này gắn với {style}."
        implication = (
            "Người khác thường nhận ra bạn khi việc khó: bạn vẫn còn mặt để xử lý. "
            "Bên trong, bạn hay tự định nghĩa mình qua việc đã nhận — làm được thì ôm, ôm rồi thì làm tròn."
        )
        if capacity:
            implication += f" Về nền năng lượng, {capacity}."
        if structure:
            implication += f" Về khung dài hạn, {structure}."
        implication += (
            " Điều quan trọng: sức mạnh ở đây là chịu tải có chủ đích — không phải ôm vô hạn."
        )
        return ConsultingParagraph(
            intent=data.intent,
            meaning=meaning,
            implication=implication,
            status=ParagraphStatus.READY,
        )

    if _is_output(data):
        meaning = "Điểm nhận diện chính: bạn cần nhìn thấy đầu ra và kết quả rõ ràng."
        if style:
            meaning += f" Điều này gắn với {style}."
        implication = (
            "Người khác thường nhận ra bạn ở chỗ việc 'ra được cái gì đó' — "
            "một sản phẩm, một ý, một kết quả nhìn thấy — hơn là ở chỗ ôm hết việc hộ mọi người."
        )
        if capacity:
            implication += (
                f" Về nền năng lượng, {capacity}. "
                "Nghĩa là bạn không phải kiểu chịu tải vô hạn; bạn mạnh khi nhịp ra–nghỉ rõ."
            )
        if follow and structure:
            implication += (
                f" Về khung dài hạn, {structure}. "
                "Lấy khuôn 'làm việc như mọi người' để tự đo dễ đánh giá thấp đúng chỗ mạnh."
            )
        elif structure:
            implication += f" Về khung dài hạn, {structure}."
        return ConsultingParagraph(
            intent=data.intent,
            meaning=meaning,
            implication=implication,
            status=ParagraphStatus.READY,
        )

    meaning = ""
    meaning_bits = [b for b in (theme, style) if b]
    if meaning_bits:
        meaning = f"Điểm nhận diện chính: bạn {meaning_bits[0]}."
        if len(meaning_bits) > 1:
            meaning += f" Điều này gắn với {meaning_bits[1]}."
    elif data.claims:
        meaning = f"Điểm nhận diện chính gắn với {data.claims[0]}."
    implication = ""
    if capacity:
        implication = f"Về nền năng lượng, {capacity}."
    if structure:
        implication = (
            f"{implication} Về khung dài hạn, {structure}."
            if implication
            else f"Về khung dài hạn, {structure}."
        ).strip()
    return ConsultingParagraph(
        intent=data.intent,
        meaning=meaning,
        implication=implication,
        status=ParagraphStatus.READY if meaning or implication else ParagraphStatus.PARTIAL,
    )


def _recognition(data: CommercialLanguageInput) -> ConsultingParagraph:
    style = pl.plain_style(data.operating_style) or pl.plain_theme(data.primary_theme)
    capacity = pl.plain_capacity(data.capacity_cue)
    follow = _is_follow(data.structure_cue)
    recognition = ""
    if data.primary_theme == "OPERATING_SELF_CARRY":
        recognition = (
            "Trong môi trường nhiều việc dồn về một người, "
            "bạn thường là người tự nhận và tự đẩy trước khi kịp phân vai."
        )
    elif _is_output(data) and style:
        recognition = (
            "Trong môi trường cần có sản phẩm nhìn thấy được, "
            f"bạn thường ổn và rõ hơn khi được {style} — "
            "không phải khi bị xếp vào việc 'giữ cho đúng quy trình' mà không ra kết quả."
        )
        if follow:
            recognition += (
                " Khung dài hạn của bạn là kiểu riêng: hợp khi được tôn trọng nhịp đó, "
                "không hợp khi bị ép giống checklist chung."
            )
    elif style:
        recognition = (
            f"Trong môi trường cần ra quyết định nhanh và có sản phẩm nhìn thấy được, "
            f"bạn thường ổn hơn khi đi đúng {style}."
        )
    meaning = f"Nền của bạn: {capacity}." if capacity else ""
    return ConsultingParagraph(
        intent=data.intent,
        recognition=recognition,
        meaning=meaning,
        status=ParagraphStatus.READY if recognition else ParagraphStatus.PARTIAL,
    )


def _work_style(data: CommercialLanguageInput) -> ConsultingParagraph:
    style = pl.plain_style(data.operating_style) or pl.plain_theme(data.primary_theme)
    career = data.feature == FeatureKind.CAREER
    if not style:
        return ConsultingParagraph(
            intent=data.intent,
            meaning="Cách bạn làm việc được nêu khi có tín hiệu vận hành đã công bố.",
            status=ParagraphStatus.PARTIAL,
        )
    if data.primary_theme == "OPERATING_SELF_CARRY":
        meaning = (
            f"Cách bạn làm việc hiệu quả nhất nghiêng về {style}: "
            "có việc → đặt mình vào chỗ phải xử lý → tự nâng chuẩn → làm đến khi xong."
        )
        implication = (
            "Quyết định thường đi theo câu hỏi 'ai chịu trách nhiệm?' hơn 'ai thích nhất?'. "
            "Khi đúng kênh này, bạn bền; khi bị ép sang khung trái, dễ mệt vì ôm hộ."
        )
        return ConsultingParagraph(
            intent=data.intent,
            meaning=meaning,
            implication=implication,
            status=ParagraphStatus.READY,
        )
    if career and _is_output(data):
        meaning = (
            f"Bạn làm việc tốt nhất khi tuần được tổ chức quanh {style}: "
            "có đầu ra cụ thể, có phản hồi, có quyền chỉnh chất lượng sản phẩm."
        )
        implication = (
            "Việc 'bận nhưng không ra cái gì nhìn thấy được' làm bạn mòn nhanh hơn việc bận đúng kênh. "
            "Lấy chu kỳ ra kết quả làm thước — không lấy danh xưng hay thời gian gắn bó."
        )
        return ConsultingParagraph(
            intent=data.intent,
            meaning=meaning,
            implication=implication,
            status=ParagraphStatus.READY,
        )
    meaning = f"Cách bạn làm việc hiệu quả nhất nghiêng về {style}."
    implication = (
        "Khi đúng kênh này, nhịp làm việc rõ và bền hơn; "
        "khi bị ép sang khung trái, dễ mệt hoặc lệch ưu tiên."
    )
    if _is_output(data):
        implication = (
            "Nhịp tự nhiên: nghĩ → làm ra → nhìn kết quả → chỉnh. "
            "Khi bị nhốt vào việc không có đầu ra, dễ mất phương hướng dù vẫn đang 'chăm chỉ'."
        )
    return ConsultingParagraph(
        intent=data.intent,
        meaning=meaning,
        implication=implication,
        status=ParagraphStatus.READY,
    )


def _support(data: CommercialLanguageInput) -> ConsultingParagraph:
    section = (data.section or "").upper()
    balance = pl.plain_balance(data.balance_cue)
    capacity = pl.plain_capacity(data.capacity_cue)
    style = pl.plain_style(data.operating_style)
    career = data.feature == FeatureKind.CAREER

    if section == "STRENGTHS" and (style or capacity):
        if data.primary_theme == "OPERATING_SELF_CARRY":
            meaning = (
                "Điểm mạnh lớn nhất là chịu tải có uy tín: khi đã nhận, bạn ít biến mất giữa áp lực."
            )
            implication = (
                "Điểm tựa đi kèm: biết chuyển việc đang mang thành đầu ra có định nghĩa — "
                "đó là van xả, không phải 'gánh thêm cho đủ'."
            )
            if balance:
                implication += f" Hướng điều tiết: {balance}."
        elif _is_output(data):
            meaning = (
                f"Điểm mạnh lớn nhất là tạo ra thứ nhìn thấy được"
                + (f" qua {style}" if style else "")
                + " — người khác tin bạn khi có sản phẩm, không chỉ khi có lời hứa."
            )
            implication = (
                "Điểm tựa thứ hai là biết giữ nhịp: nền trung hòa mạnh khi ra–nghỉ rõ, "
                "yếu khi lấy khối lượng việc làm thước tự chứng minh."
            )
            if balance:
                implication += (
                    f" Van xả tuần: {balance} — xếp giữa các chu kỳ ra kết quả, không chờ kiệt."
                )
        else:
            meaning = (
                f"Điểm tựa chính: {style}." if style else f"Điểm tựa đến từ nền năng lượng: {capacity}."
            )
            implication = "Giữ điểm tựa này như đòn bẩy tuần — không phải lời khuyên chung chung."
        return ConsultingParagraph(
            intent=data.intent,
            meaning=meaning,
            implication=implication,
            status=ParagraphStatus.READY,
        )

    if section in {"BALANCE", "DIRECTION"} or (career and balance):
        if balance:
            if career:
                meaning = (
                    f"Hướng cân bằng trong công việc: {balance}. "
                    "Trong tuần, nghĩa là chèn nhịp làm dịu giữa các vòng ra kết quả — "
                    "họp ngắn hơn, đóng một đầu ra rồi mới mở đầu ra mới."
                )
            else:
                meaning = (
                    f"Hướng điều tiết hiện tại: {balance}. "
                    "Trong đời sống, nghĩa là ưu tiên làm dịu cường độ và giữ dòng chảy ổn định "
                    "thay vì tăng ga khi vẫn còn làm được."
                )
            implication = "Đây là thói quen tuần, không phải mẹo một lần khi đã kiệt."
            return ConsultingParagraph(
                intent=data.intent,
                meaning=meaning,
                implication=implication,
                status=ParagraphStatus.READY,
            )

    meaning = ""
    if balance:
        meaning = f"Điểm tựa điều tiết: {balance}."
    elif capacity:
        meaning = f"Điểm tựa đến từ nền năng lượng: {capacity}."
    elif data.claims:
        meaning = f"Điểm tựa được nêu từ tín hiệu đã công bố: {data.claims[0]}."
    implication = (
        "Giữ điểm tựa này như đòn bẩy tuần — không phải lời khuyên chung chung."
        if meaning
        else ""
    )
    return ConsultingParagraph(
        intent=data.intent,
        meaning=meaning,
        implication=implication,
        status=ParagraphStatus.READY if meaning else ParagraphStatus.PARTIAL,
    )


def _limitation(data: CommercialLanguageInput) -> ConsultingParagraph:
    texts = [pl.plain_constraint(x) for x in data.limitations]
    texts = [t for t in texts if t]
    if not texts and data.limitations:
        texts = [data.limitations[0]] if " " in data.limitations[0] else []
    career = data.feature == FeatureKind.CAREER
    section = (data.section or "").upper()

    if career and section == "RISK":
        if data.primary_theme == "OPERATING_SELF_CARRY":
            meaning = (
                "Rủi ro nghề nghiệp chính là trở thành người giải quyết được việc rồi bị đổ thêm việc — "
                "thành công biến thành biên tải vô hạn."
            )
        elif _is_output(data):
            meaning = (
                "Rủi ro nghề nghiệp chính là bị xếp vào khuôn 'làm như mọi người' "
                "hoặc bị cắt kênh tạo ra kết quả — rồi tự kết luận mình không hợp nghề."
            )
        else:
            meaning = "Rủi ro nghề nghiệp chính là làm việc trái kênh vận hành đã rõ quá lâu."
        limitation = (
            "Nền trung hòa càng dễ kiệt nếu lấy 'chứng minh bằng khối lượng' làm thước. "
            "Giới hạn này không phải yếu hơn người khác — là biên cần nhìn thẳng."
        )
        if texts:
            limitation += f" {texts[0]}"
        return ConsultingParagraph(
            intent=data.intent,
            meaning=meaning,
            limitation=limitation,
            status=ParagraphStatus.READY,
        )

    limitation = texts[0] if texts else (
        "Giới hạn được nêu khi có tín hiệu bất lợi hoặc căng liên miền đã công bố."
    )
    meaning = "Giới hạn không phải ‘yếu hơn người khác’, mà là biên cần nhìn thẳng."
    if _is_output(data) and _is_follow(data.structure_cue):
        meaning = (
            "Giới hạn không phải ‘yếu hơn người khác’, mà là dễ tự đo bằng khuôn chung "
            "rồi bỏ qua đúng chỗ mạnh: ra kết quả trong khung riêng."
        )
    elif data.primary_theme == "OPERATING_SELF_CARRY":
        meaning = (
            "Giới hạn không phải ‘yếu hơn người khác’, mà là ôm thêm khi vẫn còn làm được — "
            "sức mạnh dễ thành gánh quá."
        )
    return ConsultingParagraph(
        intent=data.intent,
        meaning=meaning,
        limitation=limitation,
        status=ParagraphStatus.READY,
    )


def _condition(data: CommercialLanguageInput) -> ConsultingParagraph:
    texts = [pl.plain_constraint(x) for x in data.limitations]
    texts += [t for t in data.limitations if " " in t and not pl.plain_constraint(t)]
    texts = [t for t in texts if t]
    limitation = texts[0] if texts else (
        "Có điểm cần đọc có điều kiện từ các lớp phân tích khác nhau."
    )
    meaning = (
        "Trước khi chốt một nhãn duy nhất về bản thân, giữ đọc có điều kiện:"
    )
    if _is_output(data) and _is_follow(data.structure_cue):
        meaning = (
            "Trước khi chốt một nhãn duy nhất — 'mạnh' hay 'yếu', 'giống mọi người' hay không — "
            "giữ đọc có điều kiện:"
        )
    return ConsultingParagraph(
        intent=data.intent,
        meaning=meaning,
        limitation=limitation,
        status=ParagraphStatus.READY,
    )


def _pressure(data: CommercialLanguageInput) -> ConsultingParagraph:
    theme = data.primary_theme
    career = data.feature == FeatureKind.CAREER
    if theme == "OPERATING_OUTPUT":
        recognition = (
            "Khi áp lực tăng, bạn dễ tìm cách ‘làm ra được cái gì đó’ để lấy lại cảm giác kiểm soát."
        )
        action = (
            "Hãy chọn một đầu ra nhỏ nhưng rõ trong ngày, thay vì nhận thêm việc để chứng minh."
        )
        if career:
            action = (
                "Chốt một đầu ra có người nhận trong ngày — gửi, trình, đóng — "
                "thay vì nhận thêm ticket để cảm thấy mình đang 'gồng'."
            )
    elif theme == "OPERATING_SELF_CARRY":
        recognition = (
            "Khi áp lực tăng, phản xạ thường gặp là tự gánh thêm trước khi kịp phân vai."
        )
        action = (
            "Trước khi nhận thêm một đầu việc, xác định rõ việc nào tự quyết và việc nào giao lại."
        )
    else:
        recognition = (
            "Khi áp lực tăng, hãy trở lại kênh vận hành đã rõ thay vì đổi khung liên tục."
        )
        action = "Giữ một ưu tiên chính trong tuần; đừng mở quá nhiều mặt trận cùng lúc."
    return ConsultingParagraph(
        intent=data.intent,
        recognition=recognition,
        action=action,
        status=ParagraphStatus.READY,
    )


def _environment(data: CommercialLanguageInput) -> ConsultingParagraph:
    theme = data.primary_theme
    career = data.feature == FeatureKind.CAREER
    follow = _is_follow(data.structure_cue)
    if theme == "OPERATING_SELF_CARRY":
        meaning = (
            "Môi trường hợp bạn hơn khi vai trò tự chủ được định nghĩa rõ biên tải — "
            "không phải chỗ việc tràn về một người theo mặc định."
        )
        implication = (
            "Nếu môi trường trái kênh này kéo dài, dễ hiểu nhầm bản thân là 'thiếu năng lực' "
            "trong khi thực ra đang ôm quá biên."
        )
    elif _is_output(data):
        if career:
            meaning = (
                "Môi trường nghề nghiệp hợp bạn hơn khi có không gian tạo sản phẩm, ý tưởng "
                "hoặc kết quả nhìn thấy được — và có phản hồi rõ trong tuần. "
                "Ví dụ khung vai (minh họa, không phải lời tiên nghề): "
                "người tạo sản phẩm, người thiết kế đầu ra, người truyền đạt kết quả."
            )
            if follow:
                meaning += (
                    " Tổ chức tôn trọng nhịp riêng của bạn tốt hơn chỗ ép 'làm việc như mọi người'."
                )
            implication = (
                "Nơi chỉ đo bằng hiện diện, im lặng quy trình, hoặc việc không bao giờ 'ra cái gì' "
                "sẽ làm bạn tưởng mình sai nghề."
            )
        else:
            meaning = (
                "Môi trường hợp bạn hơn khi có không gian tạo ra sản phẩm, ý tưởng hoặc kết quả "
                "nhìn thấy được — và có phản hồi rõ."
            )
            implication = (
                "Nếu môi trường trái kênh này kéo dài, dễ hiểu nhầm bản thân là ‘thiếu năng lực’."
            )
    elif theme == "FOLLOW_STRUCTURE":
        meaning = (
            "Môi trường hợp bạn hơn khi tôn trọng khung dài hạn riêng của bạn, "
            "không ép theo checklist ‘chuẩn mực chung’ trái nhịp."
        )
        implication = "Nếu môi trường trái kênh này kéo dài, dễ hiểu nhầm bản thân là ‘thiếu năng lực’."
    else:
        meaning = (
            "Môi trường hợp bạn hơn khi khớp với kênh vận hành và nền năng lượng đã công bố."
        )
        implication = "Nếu môi trường trái kênh này kéo dài, dễ hiểu nhầm bản thân là ‘thiếu năng lực’."
    return ConsultingParagraph(
        intent=data.intent,
        meaning=meaning,
        implication=implication,
        status=ParagraphStatus.READY,
    )


def _insight(data: CommercialLanguageInput) -> ConsultingParagraph:
    if data.primary_theme == "OPERATING_SELF_CARRY":
        meaning = (
            "Điểm then chốt: sức bền thật sự nằm ở khả năng chuyển tải thành đầu ra có chu kỳ — "
            "không phải gánh thêm cho đủ tư cách."
        )
        implication = (
            "Nếu bỏ qua điều này, dễ lấy 'còn làm được' làm giấy phép ôm thêm, rồi mệt mà vẫn trông ổn."
        )
        return ConsultingParagraph(
            intent=data.intent,
            meaning=meaning,
            implication=implication,
            status=ParagraphStatus.READY,
        )
    if _is_output(data) and _is_follow(data.structure_cue):
        meaning = (
            "Điểm then chốt: bạn không kém vì không giống khuôn chung — "
            "bạn rõ khi tạo ra đầu ra trong đúng khung riêng của mình."
        )
        implication = (
            "Nếu lấy 'làm việc như mọi người' hoặc 'ôm thêm cho đủ' để tự đo, "
            "dễ đánh giá thấp đúng chỗ mạnh dù từng miền riêng lẻ vẫn 'đúng'."
        )
        return ConsultingParagraph(
            intent=data.intent,
            meaning=meaning,
            implication=implication,
            status=ParagraphStatus.READY,
        )
    theme = pl.plain_theme(data.primary_theme)
    structure = pl.structure_to_plain(data.structure_cue)
    style = pl.plain_style(data.operating_style)
    bits = [b for b in (structure, theme or style) if b]
    if len(bits) >= 2:
        meaning = f"Điểm then chốt: vừa {bits[0]}, vừa {bits[1]}."
    elif bits:
        meaning = f"Điểm then chốt: {bits[0]}."
    elif data.claims:
        meaning = f"Điểm then chốt: {data.claims[0]}."
    else:
        meaning = "Điểm then chốt chỉ được nêu khi đủ dữ liệu."
    implication = (
        "Nếu bỏ qua điều này, dễ hiểu sai bản thân dù từng miền riêng lẻ vẫn ‘đúng’."
    )
    return ConsultingParagraph(
        intent=data.intent,
        meaning=meaning,
        implication=implication,
        status=ParagraphStatus.READY,
    )


def _action(data: CommercialLanguageInput) -> ConsultingParagraph:
    action = pl.plain_priority(data.actionability) or pl.plain_avoid(data.actionability)
    if not action and data.claims:
        action = data.claims[0] if " " in data.claims[0] else ""
    if action and data.feature == FeatureKind.CAREER:
        key = (data.actionability or "").split(":", 1)[0]
        if key == "align_operating_role":
            action += " Trong công việc: xếp lịch quanh vòng ra kết quả, không quanh việc 'có mặt'."
        elif key == "apply_balance":
            action += " Trong công việc: đóng một đầu ra rồi mới mở vòng sau."
    meaning = "Việc nên làm gần đây:" if action else ""
    return ConsultingParagraph(
        intent=data.intent,
        meaning=meaning,
        action=action,
        status=ParagraphStatus.READY if action else ParagraphStatus.PARTIAL,
    )


def _closing(data: CommercialLanguageInput) -> ConsultingParagraph:
    memory = (data.memory_candidate or "").strip()
    if not memory:
        theme = pl.plain_theme(data.primary_theme)
        style = pl.plain_style(data.operating_style)
        if theme and style:
            memory = f"Bạn mạnh hơn khi được {style} — và giữ đúng biên năng lượng của mình."
        elif theme:
            memory = f"Nhớ điều này: bạn {theme}."
        elif style:
            memory = f"Bạn rõ hơn khi được {style}."
        else:
            memory = "Giữ quyết định bám những gì đã được công bố — đủ để đi tiếp."
    return ConsultingParagraph(
        intent=data.intent,
        memory_line=memory,
        status=ParagraphStatus.READY,
    )


def _contrast(data: CommercialLanguageInput) -> ConsultingParagraph:
    return _condition(data)
