"""Deterministic paragraph realization from CommercialLanguageInput."""

from __future__ import annotations

from applications.production.language.models import (
    CommercialLanguageInput,
    ConsultingParagraph,
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


def _observation(data: CommercialLanguageInput) -> ConsultingParagraph:
    theme = pl.plain_theme(data.primary_theme)
    style = pl.plain_style(data.operating_style)
    capacity = pl.plain_capacity(data.capacity_cue)
    structure = pl.structure_to_plain(data.structure_cue)
    meaning_bits = [b for b in (theme, style) if b]
    meaning = ""
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
    recognition = ""
    if style:
        recognition = (
            f"Trong môi trường cần ra quyết định nhanh và có sản phẩm nhìn thấy được, "
            f"bạn thường ổn hơn khi đi đúng {style}."
        )
        if data.primary_theme == "OPERATING_SELF_CARRY":
            recognition = (
                "Trong môi trường nhiều việc dồn về một người, "
                "bạn thường là người tự nhận và tự đẩy trước khi kịp phân vai."
            )
    meaning = ""
    if capacity:
        meaning = f"Nền của bạn: {capacity}."
    return ConsultingParagraph(
        intent=data.intent,
        recognition=recognition,
        meaning=meaning,
        status=ParagraphStatus.READY if recognition else ParagraphStatus.PARTIAL,
    )


def _work_style(data: CommercialLanguageInput) -> ConsultingParagraph:
    style = pl.plain_style(data.operating_style) or pl.plain_theme(data.primary_theme)
    meaning = (
        f"Cách bạn làm việc hiệu quả nhất nghiêng về {style}."
        if style
        else "Cách bạn làm việc được nêu khi có tín hiệu vận hành đã công bố."
    )
    implication = (
        "Khi đúng kênh này, nhịp làm việc rõ và bền hơn; "
        "khi bị ép sang khung trái, dễ mệt hoặc lệch ưu tiên."
    )
    return ConsultingParagraph(
        intent=data.intent,
        meaning=meaning,
        implication=implication if style else "",
        status=ParagraphStatus.READY if style else ParagraphStatus.PARTIAL,
    )


def _support(data: CommercialLanguageInput) -> ConsultingParagraph:
    balance = pl.plain_balance(data.balance_cue)
    capacity = pl.plain_capacity(data.capacity_cue)
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
    limitation = texts[0] if texts else (
        "Giới hạn được nêu khi có tín hiệu bất lợi hoặc căng liên miền đã công bố."
    )
    meaning = "Giới hạn không phải ‘yếu hơn người khác’, mà là biên cần nhìn thẳng."
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
    return ConsultingParagraph(
        intent=data.intent,
        meaning="Trước khi chốt một nhãn duy nhất về bản thân, giữ đọc có điều kiện:",
        limitation=limitation,
        status=ParagraphStatus.READY,
    )


def _pressure(data: CommercialLanguageInput) -> ConsultingParagraph:
    theme = data.primary_theme
    if theme == "OPERATING_OUTPUT":
        recognition = (
            "Khi áp lực tăng, bạn dễ tìm cách ‘làm ra được cái gì đó’ để lấy lại cảm giác kiểm soát."
        )
        action = (
            "Hãy chọn một đầu ra nhỏ nhưng rõ trong ngày, thay vì nhận thêm việc để chứng minh."
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
    lim = ""
    if data.limitations:
        lim = pl.plain_constraint(data.limitations[0]) or ""
    return ConsultingParagraph(
        intent=data.intent,
        recognition=recognition,
        action=action,
        limitation=lim,
        status=ParagraphStatus.READY,
    )


def _environment(data: CommercialLanguageInput) -> ConsultingParagraph:
    theme = data.primary_theme
    if theme == "OPERATING_OUTPUT":
        meaning = (
            "Môi trường hợp bạn hơn khi có không gian tạo ra sản phẩm, ý tưởng hoặc kết quả "
            "nhìn thấy được — và có phản hồi rõ."
        )
    elif theme == "OPERATING_SELF_CARRY":
        meaning = (
            "Môi trường hợp bạn hơn khi vai trò tự chủ được định nghĩa rõ biên tải — "
            "không phải chỗ việc tràn về một người theo mặc định."
        )
    elif theme == "FOLLOW_STRUCTURE":
        meaning = (
            "Môi trường hợp bạn hơn khi tôn trọng khung dài hạn riêng của bạn, "
            "không ép theo checklist ‘chuẩn mực chung’ trái nhịp."
        )
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
