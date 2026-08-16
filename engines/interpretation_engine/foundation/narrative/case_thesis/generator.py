"""Deterministic Case Thesis Generator.

Reads already-validated bundles and ChartFocus. Does not calculate astrology,
select Useful God, or invent long-form customer prose.
"""

from __future__ import annotations

import re
from dataclasses import replace

from engines.interpretation_engine.foundation.interpreters.useful_god.templates import (
    STEM_ELEMENT,
)
from engines.interpretation_engine.foundation.narrative.case_thesis.functions import (
    CORRECTIVE_ID,
    EXPANDED_THESIS_WORD_LIMIT,
    GOVERNING_DOMAINS,
    SHORT_THESIS_SENTENCE_MAX,
    SHORT_THESIS_SENTENCE_MIN,
    TITLE_WORD_LIMIT,
    dominant_element,
    function_of,
    majority_function,
    strength_function,
    useful_function,
)
from engines.interpretation_engine.foundation.narrative.case_thesis.models import (
    INCOMPLETE_THESIS,
    CaseThesisResult,
)
from engines.interpretation_engine.foundation.narrative.input import (
    ChartFocus,
    NarrativeComposerInput,
)
from engines.interpretation_engine.foundation.narrative.models import EvidenceGraph
from engines.interpretation_engine.foundation.narrative.text import normalize_text

_OVERCLAIM = re.compile(
    r"bạn là người chắc chắn|bạn sẽ\b|bạn sinh ra để",
    re.IGNORECASE,
)
_WORD = re.compile(r"\S+")
_SENTENCE = re.compile(r"(?<=[.!?])\s+")

_TITLE_BY_COMBO: dict[tuple[str, str, str, str], str] = {
    ("surplus", "support", "output", "peer"): "Người tự gánh",
    ("balance", "support", "discipline", "growth"): "Người chỉnh trục",
    ("balance", "support", "resource", "growth"): "Người chỉnh trục",
    ("balance", "support", "discipline", "support"): "Người chỉnh trục",
    ("balance", "support", "resource", "support"): "Người chỉnh trục",
    ("surplus", "resource", "visibility", "discipline"): "Người kiến tạo",
    ("surplus", "resource", "peer", "discipline"): "Người kiến tạo",
    ("surplus", "resource", "output", "discipline"): "Người kiến tạo",
    ("surplus", "resource", "peer", "resource"): "Người kiến tạo",
    ("deficit", "support", "output", "peer"): "Người xây nền",
    ("balance", "authority", "circulation", "growth"): "Người điều phối",
}

_TITLE_FROM_USEFUL: dict[str, str] = {
    "output": "Người xuất thành",
    "discipline": "Người chỉnh trục",
    "resource": "Người gìn nguồn",
    "visibility": "Người tinh luyện",
    "peer": "Người đứng vững",
    "authority": "Người định khung",
    "support": "Người xây nền",
    "growth": "Người mở đường",
    "circulation": "Người điều phối",
    "stability": "Người giữ nền",
}

_TENSION_TEXT: dict[str, str] = {
    "capacity_vs_overload": (
        "sức gánh được việc lớn nhưng dễ chất thêm tải vì vẫn còn sức"
    ),
    "growth_vs_containment": (
        "nền có hệ nhưng dễ bị mọc thêm khung thay vì được chỉnh cho vừa"
    ),
    "accumulation_vs_cutting": (
        "nguồn vận hành được nhưng dễ bị cắt lạnh thay vì được luyện thành giá trị"
    ),
    "structure_vs_expression": (
        "có khung ổn định nhưng kênh ra việc chưa thành sản phẩm thấy được"
    ),
    "responsibility_vs_competition": (
        "giữ được trách nhiệm nhưng dễ bị kéo vào tranh ngang vai"
    ),
    "flexibility_vs_direction": (
        "cân bằng được nhịp nhưng dễ mất trục khi mở quá nhiều hướng"
    ),
}

_CORRECTIVE_TEXT: dict[str, str] = {
    "release_output": "đưa sức dư ra thành việc hoàn thành, thấy được",
    "introduce_discipline": "cắt phần thừa và lập kỷ luật dùng được",
    "improve_circulation": "khơi dòng lưu thông, bớt ứ đọng",
    "circulate_resource": "xoay nguồn có hạn mức, không ôm mọi nghĩa vụ",
    "refine_visibility": "giữ nhiệt điểm, tinh luyện đúng chỗ",
    "strengthen_support": "dựng nền có cửa ra, không ủ mãi",
    "introduce_structure": "đặt khung trách nhiệm rõ trước khi mở rộng",
    "open_growth": "mở một trục tăng trưởng, không đâm mọi hướng",
    "stabilize_base": "giữ nền ổn rồi mới chuyển nhịp",
    "stand_independently": "đứng vững trên việc của mình, bớt tranh ngang",
}

_CAPACITY_TEXT: dict[str, str] = {
    "surplus": "sức gánh và chịu tải cao",
    "balance": "khả năng chỉnh nhịp cho vừa, không thiên dư hay kiệt",
    "deficit": "cần nền đỡ trước khi ra tải lớn",
    "support": "làm việc có hệ, có chỗ dựa cấu trúc",
    "output": "biến sức thành sản phẩm và kỹ năng thấy được",
    "resource": "vận hành nguồn có sổ",
    "discipline": "cắt và chuẩn hóa được phần thừa",
    "visibility": "tinh luyện đúng điểm",
    "peer": "tự lực và chịu trách nhiệm phần mình",
}

_RISK_TEXT: dict[str, str] = {
    "peer": "thêm tải hoặc tranh ngang vai vì vẫn còn sức",
    "growth": "mở thêm khung, khởi sự chồng lên chỗ đã chật",
    "discipline": "cắt lạnh quá sớm phần đang cần luyện",
    "support": "ủ mãi không ra việc, bọc kín hệ thống",
    "output": "làm nhiều mà mất nền, thoát khí không phép",
    "resource": "ôm thêm nghĩa vụ nguồn quá sức nền",
    "authority": "siết quyền kiểm soát đến mức nghẽn",
    "visibility": "hun đốt nội nhiệt, tinh chỉnh không điểm dừng",
}


def generate_case_thesis(
    source: NarrativeComposerInput,
    *,
    evidence: EvidenceGraph | None = None,
    case_id: str = "",
) -> CaseThesisResult:
    """Build one case thesis from current bundles. No LLM. No engine rewrite."""
    focus = source.chart_focus
    if focus is None:
        return INCOMPLETE_THESIS
    pattern_fn = function_of(focus.pattern_label, stem_roles=focus.stem_roles)
    strength_fn = strength_function(focus)
    useful_fn = useful_function(focus)
    ky_fn = majority_function(focus.unfavorable, stem_roles=focus.stem_roles)
    ky_element = majority_function(
        tuple(STEM_ELEMENT.get(name, "") for name in focus.unfavorable),
        stem_roles=(),
    )
    if ky_fn == pattern_fn and ky_element and ky_element != ky_fn:
        ky_fn = ky_element
    diagnostics: list[str] = []
    if not focus.pattern_label or not pattern_fn:
        diagnostics.append("missing_pattern")
    if not strength_fn:
        diagnostics.append("missing_strength")
    if not focus.selected or not useful_fn:
        diagnostics.append("missing_useful_god")
    if diagnostics:
        return replace(
            INCOMPLETE_THESIS,
            case_id=case_id,
            diagnostics=tuple(diagnostics),
            core_pattern=focus.pattern_label,
            core_strength=focus.strength_label or focus.strength_state,
        )
    tension_id = _tension_id(
        strength_fn,
        pattern_fn,
        useful_fn,
        ky_fn,
        dominant_element(focus),
    )
    corrective_id = CORRECTIVE_ID.get(useful_fn, "release_output")
    title = _title(strength_fn, pattern_fn, useful_fn, ky_fn)
    core_tension = _TENSION_TEXT.get(tension_id, "")
    if not core_tension:
        core_tension = (
            f"nền {focus.pattern_label} dễ lệch nếu không theo hướng {focus.selected}"
        )
    corrective = _CORRECTIVE_TEXT.get(corrective_id, "theo hướng Dụng thần đã chọn")
    evidence_ids, refs, confidence = _trace(source, evidence)
    unsupported = 0 if evidence_ids and refs else 1
    if unsupported:
        diagnostics.append("unsupported_thesis_claims")
    short_thesis = _short_thesis(
        strength_fn=strength_fn,
        pattern_label=focus.pattern_label,
        useful_name=focus.selected,
        ky_fn=ky_fn,
        tension=core_tension,
        corrective=corrective,
        wood_heavy=_wood_heavy(focus),
    )
    expanded = _expanded_thesis(
        title=title,
        short_thesis=short_thesis,
        pattern_label=focus.pattern_label,
        strength_label=focus.strength_label or focus.strength_state,
        selected=focus.selected,
        unfavorable=focus.unfavorable,
        corrective=corrective,
        dayun=focus.current_dayun,
    )
    claims = (
        title,
        short_thesis,
        expanded,
        core_tension,
        corrective,
    )
    if any(_OVERCLAIM.search(item or "") for item in claims):
        diagnostics.append("overclaim_language")
    capacities = _capacities(strength_fn, pattern_fn, useful_fn)
    risks = _risks(ky_fn, tension_id)
    career, finance, relationship, health = _implications(
        useful_fn, ky_fn, tension_id, corrective
    )
    domains = _domains(source)
    coverage = 1.0 if evidence_ids else 0.0
    domain_coverage = _domain_coverage(domains)
    specificity = _specificity(
        focus.pattern_label,
        strength_fn,
        focus.selected,
        ky_fn,
        tension_id,
        corrective_id,
    )
    thesis_key = "|".join(
        (
            focus.pattern_label,
            strength_fn,
            focus.selected,
            ",".join(sorted(focus.unfavorable)),
            useful_fn,
            ky_fn,
            tension_id,
            corrective_id,
        )
    )
    return CaseThesisResult(
        case_id=case_id,
        status="complete",
        thesis_key=thesis_key,
        title=_limit_title(title),
        short_thesis=short_thesis,
        expanded_thesis=_limit_words(expanded, EXPANDED_THESIS_WORD_LIMIT),
        core_pattern=focus.pattern_label,
        core_strength=focus.strength_label or focus.strength_state,
        core_tension=core_tension,
        corrective_direction=corrective,
        supporting_facts=_supporting_facts(focus),
        supporting_domains=domains,
        primary_risks=risks,
        primary_capacities=capacities,
        career_implication=career,
        finance_implication=finance,
        relationship_implication=relationship,
        health_implication=health,
        evidence_ids=evidence_ids,
        engine_truth_refs=refs,
        confidence=confidence,
        alternatives=(),
        diagnostics=tuple(diagnostics),
        pattern_function=pattern_fn,
        strength_function=strength_fn,
        useful_function=useful_fn,
        ky_function=ky_fn,
        tension_id=tension_id,
        corrective_id=corrective_id,
        thesis_evidence_coverage=coverage,
        thesis_domain_coverage=domain_coverage,
        thesis_specificity=specificity,
        unsupported_thesis_claims=unsupported,
        core_tension_present=1.0 if core_tension else 0.0,
        corrective_direction_present=1.0 if corrective else 0.0,
    )


def _tension_id(
    strength_fn: str,
    pattern_fn: str,
    useful_fn: str,
    ky_fn: str,
    dominant: str,
) -> str:
    """Derive one tension id from the combination, not from a single label."""
    if (
        strength_fn == "surplus"
        and pattern_fn == "support"
        and useful_fn == "output"
        and ky_fn == "peer"
    ):
        return "capacity_vs_overload"
    if ky_fn == "growth" and useful_fn in {"discipline", "resource", "authority"}:
        return "growth_vs_containment"
    if (
        strength_fn == "balance"
        and pattern_fn == "support"
        and ky_fn == "support"
        and useful_fn in {"discipline", "resource", "authority"}
    ):
        return "growth_vs_containment"
    if pattern_fn == "resource" and ky_fn == "discipline":
        return "accumulation_vs_cutting"
    if pattern_fn == "support" and useful_fn == "output":
        return "structure_vs_expression"
    if ky_fn == "peer":
        return "responsibility_vs_competition"
    if strength_fn == "balance" and dominant == "Mộc":
        return "growth_vs_containment"
    if strength_fn == "balance":
        return "flexibility_vs_direction"
    return f"{ky_fn}_vs_{useful_fn}"


def _title(
    strength_fn: str,
    pattern_fn: str,
    useful_fn: str,
    ky_fn: str,
) -> str:
    """Human title from the combination. Not a Pattern lookup."""
    combo = (strength_fn, pattern_fn, useful_fn, ky_fn)
    if combo in _TITLE_BY_COMBO:
        return _TITLE_BY_COMBO[combo]
    return _TITLE_FROM_USEFUL.get(useful_fn, "Người điều phối")


def _short_thesis(
    *,
    strength_fn: str,
    pattern_label: str,
    useful_name: str,
    ky_fn: str,
    tension: str,
    corrective: str,
    wood_heavy: bool,
) -> str:
    """Two to four structural sentences. No fortune-telling."""
    strength_clause = {
        "surplus": "Lá số cho thấy xu hướng sức gánh cao",
        "balance": "Lá số cho thấy xu hướng trung hòa, cần chỉnh cho vừa",
        "deficit": "Lá số cho thấy xu hướng cần nền đỡ trước khi ra tải",
    }.get(strength_fn, "Lá số cho thấy một cấu trúc vận hành rõ")
    wood = " trong bối cảnh Mộc dày" if wood_heavy else ""
    first = f"{strength_clause} trên nền {pattern_label}{wood}."
    second = f"Cấu trúc này phù hợp hơn khi {corrective}."
    third = f"Rủi ro tăng khi {tension}."
    fourth = ""
    if ky_fn:
        fourth = f"Áp lực chính đi cùng hướng {useful_name} cần được giữ, không đảo ngược."
    text = " ".join(part for part in (first, second, third, fourth) if part)
    return _limit_sentences(text, SHORT_THESIS_SENTENCE_MAX, SHORT_THESIS_SENTENCE_MIN)


def _expanded_thesis(
    *,
    title: str,
    short_thesis: str,
    pattern_label: str,
    strength_label: str,
    selected: str,
    unfavorable: tuple[str, ...],
    corrective: str,
    dayun: str,
) -> str:
    """Concise synthesis. Not a knowledge dump."""
    ky = ", ".join(unfavorable[:2]) if unfavorable else "áp lực hiện tại"
    frame = f" Khung thời gian đọc là {dayun}." if dayun else ""
    extra = (
        f"{title} là hình dung ngắn của cách lá số này vận hành. "
        f"Nền {pattern_label} và trạng thái {strength_label} giải thích sức chứa. "
        f"Hướng chỉnh là {selected}; điều không nên khuếch đại là {ky}. "
        f"Cấu trúc này phù hợp hơn khi {corrective}.{frame}"
    )
    return _limit_words(f"{short_thesis} {extra}", EXPANDED_THESIS_WORD_LIMIT)


def _implications(
    useful_fn: str,
    ky_fn: str,
    tension_id: str,
    corrective: str,
) -> tuple[str, str, str, str]:
    """One short implication per life area. Not a profession catalogue."""
    career = (
        f"Sự nghiệp phù hợp hơn khi {corrective}; "
        f"rủi ro tăng khi biến chỗ làm thành chỗ { _RISK_TEXT.get(ky_fn, 'thêm tải') }."
    )
    finance = {
        "output": "Tài chính nên đi cùng việc hoàn thành có nhịp, không ôm thêm nghĩa vụ vì còn sức.",
        "discipline": "Tài chính nên cắt phần lỗ và giữ hạn mức, không mở vốn theo đà mọc.",
        "resource": "Tài chính nên vận hành một dòng có sổ, không ôm mọi cam kết nguồn.",
        "visibility": "Tài chính nên chọn lọc chất, không cắt lạnh vòng vốn đang luyện.",
    }.get(useful_fn, "Tài chính nên theo hướng chỉnh đã chọn, không hứa hiệu quả.")
    relationship = {
        "capacity_vs_overload": (
            "Quan hệ dễ thành kho chứa việc; cấu trúc này phù hợp hơn khi có biên tải."
        ),
        "growth_vs_containment": (
            "Quan hệ dễ thành chỗ mở thêm khung; cần biên để không đâm thẳng mọi hướng."
        ),
        "accumulation_vs_cutting": (
            "Quan hệ dễ thành chỗ tính-cắt; cần giữ nhiệt luyện, bớt nhát cắt lạnh."
        ),
    }.get(tension_id, "Quan hệ nên theo cùng hướng chỉnh, không biến thành kho chứa.")
    health = {
        "surplus": (
            "Sức khỏe: giữ nhịp nghỉ sau pha gánh; không hiểu còn sức là không cần phục hồi."
        ),
        "balance": (
            "Sức khỏe: chỉnh nóng-lạnh và căng-giãn cho vừa, không kích một phía."
        ),
        "deficit": (
            "Sức khỏe: dưỡng nền trước tải; không lấy thiếu sức làm lý do siết thêm."
        ),
    }.get(
        "balance" if "growth" in tension_id or "flex" in tension_id else (
            "deficit" if "containment" in tension_id and useful_fn == "support" else "surplus"
        ),
        "Sức khỏe: giữ nhịp cân; không chẩn đoán.",
    )
    return career, finance, relationship, health


def _capacities(strength_fn: str, pattern_fn: str, useful_fn: str) -> tuple[str, ...]:
    """Primary capacities from the combination."""
    items = [
        _CAPACITY_TEXT.get(strength_fn, ""),
        _CAPACITY_TEXT.get(pattern_fn, ""),
        _CAPACITY_TEXT.get(useful_fn, ""),
    ]
    return tuple(dict.fromkeys(item for item in items if item))


def _risks(ky_fn: str, tension_id: str) -> tuple[str, ...]:
    """Primary risks from Kỵ pressure and tension."""
    items = [
        _RISK_TEXT.get(ky_fn, ""),
        _TENSION_TEXT.get(tension_id, ""),
    ]
    return tuple(dict.fromkeys(item for item in items if item))[:3]


def _supporting_facts(focus: ChartFocus) -> tuple[str, ...]:
    """Current-chart facts that the thesis stands on. Shen Sha is not primary."""
    facts = [
        focus.day_master,
        focus.pattern_label,
        focus.strength_label or focus.strength_state,
        focus.selected,
        *focus.favorable[:2],
        *focus.unfavorable[:2],
        focus.current_dayun,
    ]
    if _wood_heavy(focus):
        facts.append("Mộc")
    return tuple(item for item in dict.fromkeys(facts) if item)


def _wood_heavy(focus: ChartFocus) -> bool:
    """True when copied five-element counts show wood as the thickest."""
    if dominant_element(focus) == "Mộc":
        return True
    for name, count in focus.five_elements:
        if name == "Mộc" and count >= 5:
            return True
    return False


def _trace(
    source: NarrativeComposerInput,
    evidence: EvidenceGraph | None,
) -> tuple[tuple[str, ...], tuple[str, ...], float]:
    """Bind thesis language to existing evidence and engine truth refs."""
    refs: list[str] = []
    ids: list[str] = []
    confidences: list[float] = []
    focus = source.chart_focus
    tokens = focus.active_names() if focus else frozenset()
    if evidence is not None:
        for node in evidence.nodes:
            if node.domain in GOVERNING_DOMAINS or (
                tokens and any(token in node.statement for token in tokens)
            ):
                ids.append(node.evidence_id)
                if node.engine_truth_ref:
                    refs.append(node.engine_truth_ref)
                confidences.append(node.confidence)
    if not refs:
        for bundle in source.all_bundles():
            if bundle.domain not in GOVERNING_DOMAINS:
                continue
            refs.extend(bundle.engine_truth_refs)
            confidences.append(bundle.confidence)
            if evidence is None:
                ids.extend(bundle.engine_truth_refs)
    unique_ids = tuple(dict.fromkeys(item for item in ids if item))
    unique_refs = tuple(dict.fromkeys(item for item in refs if item))
    confidence = max(confidences) if confidences else 0.0
    return unique_ids[:16], unique_refs[:16], confidence


def _domains(source: NarrativeComposerInput) -> tuple[str, ...]:
    """Domains that actually contributed statements."""
    names = [bundle.domain for bundle in source.all_bundles() if bundle.statements]
    return tuple(dict.fromkeys(names))


def _domain_coverage(domains: tuple[str, ...]) -> float:
    """Share of governing domains present on the thesis."""
    if not GOVERNING_DOMAINS:
        return 1.0
    found = sum(1 for name in GOVERNING_DOMAINS if name in domains)
    return found / len(GOVERNING_DOMAINS)


def _specificity(*parts: str) -> float:
    """How many structural axes are actually filled."""
    filled = sum(1 for part in parts if part)
    return filled / max(len(parts), 1)


def _limit_title(title: str) -> str:
    """Keep the human title short."""
    words = _WORD.findall(normalize_text(title))
    return " ".join(words[:TITLE_WORD_LIMIT])


def _limit_words(text: str, limit: int) -> str:
    """Clip expanded thesis to the editorial word cap."""
    words = _WORD.findall(normalize_text(text))
    if len(words) <= limit:
        return normalize_text(text)
    return " ".join(words[:limit]).rstrip(" ,;") + "."


def _limit_sentences(text: str, maximum: int, minimum: int) -> str:
    """Keep short thesis in the 2–4 sentence band."""
    parts = [part.strip() for part in _SENTENCE.split(normalize_text(text)) if part.strip()]
    if len(parts) > maximum:
        parts = parts[:maximum]
    while len(parts) < minimum and parts:
        parts.append(parts[-1])
        break
    return " ".join(parts)
