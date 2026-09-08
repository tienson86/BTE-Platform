"""Customer-facing Vietnamese narrative with V1 safety bounds."""

from __future__ import annotations

from engines.number_energy.catalog import (
    CANONICAL_CUSTOMER_COPY,
    ENERGY_CATALOG,
    PURPOSE_FOCUS_VI,
)
from engines.number_energy.constants import (
    CHALLENGING_CUSTOMER_LABEL,
    COMPATIBILITY_NOTE,
    CONTROL_RELATIONS,
    ENERGY_DISPLAY_NAMES,
    FORBIDDEN_CUSTOMER_PHRASES,
    HEALTH_DISCLAIMER,
    SYSTEM_NAME,
    SYSTEM_SHORT_NAME,
)
from engines.number_energy.exceptions import NumberEnergyEngineError
from engines.number_energy.types import (
    CustomerNarrative,
    EnergyOccurrence,
    NumberEnergyResult,
    SequenceSummary,
    UndefinedSegment,
)


def compose_narrative(
    *,
    input_raw: str,
    occurrences: tuple[EnergyOccurrence, ...],
    undefined: tuple[UndefinedSegment, ...],
    summary: SequenceSummary,
    purpose_context: str,
    approved_patterns: tuple[str, ...],
) -> CustomerNarrative:
    """Compose Vietnamese customer copy from frozen catalog fields only."""
    unknown_notice = _unknown_notice(undefined)
    summary_text = _summary_text(
        input_raw=input_raw,
        occurrences=occurrences,
        undefined=undefined,
        summary=summary,
        approved_patterns=approved_patterns,
    )
    paragraphs = _paragraphs(
        occurrences=occurrences,
        summary=summary,
        purpose_context=purpose_context,
        approved_patterns=approved_patterns,
    )
    strengths, watchouts = _strengths_and_watchouts(occurrences)
    health_needed = bool(occurrences)
    narrative = CustomerNarrative(
        language="vi",
        system_name=SYSTEM_NAME,
        system_short_name=SYSTEM_SHORT_NAME,
        summary=summary_text,
        paragraphs=paragraphs,
        strengths=strengths,
        watchouts=watchouts,
        purpose_focus=PURPOSE_FOCUS_VI.get(
            purpose_context, PURPOSE_FOCUS_VI["generic_number"]
        ),
        health_disclaimer=HEALTH_DISCLAIMER if health_needed else None,
        compatibility_note=COMPATIBILITY_NOTE,
        unknown_notice=unknown_notice,
    )
    _assert_safe(narrative)
    return narrative


def collect_expert_notes(
    occurrences: tuple[EnergyOccurrence, ...],
) -> tuple[str, ...]:
    """Return frozen expert notes for detected energies."""
    notes: list[str] = []
    seen: set[str] = set()
    for item in occurrences:
        if item.energy_id in seen:
            continue
        seen.add(item.energy_id)
        catalog = ENERGY_CATALOG.get(item.energy_id)
        if catalog:
            notes.append(f"{item.display_name}: {catalog['expert_notes']}")
    return tuple(notes)


def _summary_text(
    *,
    input_raw: str,
    occurrences: tuple[EnergyOccurrence, ...],
    undefined: tuple[UndefinedSegment, ...],
    summary: SequenceSummary,
    approved_patterns: tuple[str, ...],
) -> str:
    """Prefer frozen canonical copy when the whole sequence is a catalog example."""
    if input_raw in CANONICAL_CUSTOMER_COPY and not undefined:
        prefix = (
            f"Theo hệ thống {SYSTEM_NAME} ({SYSTEM_SHORT_NAME}). "
        )
        return prefix + CANONICAL_CUSTOMER_COPY[input_raw]
    if undefined and not occurrences:
        return (
            f"Theo hệ thống {SYSTEM_NAME} ({SYSTEM_SHORT_NAME}), "
            "một phần hoặc toàn bộ dãy số này chưa được định nghĩa trong V1. "
            "Engine trả về trạng thái UNKNOWN_OR_NOT_DEFINED, không suy diễn thêm quy tắc."
        )
    names = _unique_names(occurrences)
    text = (
        f"Theo hệ thống {SYSTEM_NAME} ({SYSTEM_SHORT_NAME}), "
        f"dãy {input_raw} xuất hiện các trường khí: {names}."
    )
    if summary.approved_supportive_chain or "approved_supportive_chain" in approved_patterns:
        text += (
            " Chuỗi đi theo trật tự đã khóa Sinh Khí -> Thiên Y -> Diên Niên."
        )
    if undefined:
        text += (
            " Một số đoạn chưa được khóa trong V1 nên được đánh dấu "
            "UNKNOWN_OR_NOT_DEFINED."
        )
    return text


def _paragraphs(
    *,
    occurrences: tuple[EnergyOccurrence, ...],
    summary: SequenceSummary,
    purpose_context: str,
    approved_patterns: tuple[str, ...],
) -> tuple[str, ...]:
    """Explain visible pairs, both sides, and frozen control relations."""
    lines: list[str] = []
    for item in occurrences:
        catalog = ENERGY_CATALOG[item.energy_id]
        why = (
            f"Cặp {item.pair_digits} (span {item.source_span[0]}-{item.source_span[1]}"
            f", nguồn {item.source_digits}) tạo {item.display_name}"
        )
        if item.strength_rank is not None:
            why += f" rank {item.strength_rank}"
        why += f", trạng thái {item.state}."
        if item.via_modifier == 0:
            why += " Số 0 là âm trường, che hoặc giảm biểu hiện chứ không xóa hẳn."
        elif item.via_modifier == 5:
            why += " Số 5 là dương trường, kích hoạt hoặc khuếch đại năng lượng gốc."
        class_label = (
            CHALLENGING_CUSTOMER_LABEL
            if item.classification == "challenging"
            else item.classification
        )
        why += f" Đây là {class_label}."
        why += f" {catalog['customer_summary']}"
        why += (
            f" Mặt cần kiểm soát: {catalog['shadow']}; {catalog['excessive_effect']}."
        )
        lines.append(why)
        lines.append(
            "Theo hệ thống Bát Cực Linh Số, trường khí này gợi ý nên lưu ý: "
            f"{catalog['health']}"
        )
    if summary.approved_supportive_chain or "approved_supportive_chain" in approved_patterns:
        lines.append(
            "Đây là chuỗi cát tinh mạnh đã khóa, đi theo trật tự hỗ trợ: "
            "mở cơ hội, tăng tài khí/phúc khí, rồi đưa về ổn định và trách nhiệm. "
            "Không đảo ngược chuỗi này trong V1."
        )
    lines.extend(_control_paragraphs(occurrences, summary))
    lines.append(PURPOSE_FOCUS_VI.get(purpose_context, PURPOSE_FOCUS_VI["generic_number"]))
    return tuple(lines)


def _control_paragraphs(
    occurrences: tuple[EnergyOccurrence, ...],
    summary: SequenceSummary,
) -> list[str]:
    """Describe frozen control / support relations actually present."""
    lines: list[str] = []
    present = {item.energy_id for item in occurrences}
    if "jue_ming" in present and "tian_yi" not in present:
        lines.append(
            "Theo V1, Tuyệt Mệnh cần Thiên Y để chế ước. "
            "Diên Niên không thay thế vai trò Thiên Y."
        )
    if "wu_gui" in present and "sheng_qi" not in present:
        lines.append("Theo V1, Ngũ Quỷ cần Sinh Khí để chế/giáng.")
    if "liu_sha" in present and "yan_nian" not in present:
        lines.append("Theo V1, Lục Sát cần Diên Niên để chế ước.")
    if "huo_hai" in present:
        lines.append(
            "Họa Hại cần phối hợp cát tinh; V1 không khóa một cặp chế trực tiếp. "
            "Cần phân biệt khẩu tài có thể dùng được với thị phi cần kiểm soát."
        )
    if summary.fu_wei_supported:
        lines.append(
            "Phục Vị được Sinh Khí hoặc Thiên Y hỗ trợ; "
            "Phục Vị không tự hóa giải hung tinh mạnh."
        )
    if summary.controlled_energy_ids:
        names = ", ".join(
            ENERGY_DISPLAY_NAMES[energy_id] for energy_id in summary.controlled_energy_ids
        )
        lines.append(
            f"Các trường {names} được đánh dấu CONTROLLED vì cát tinh chế ước "
            "tương ứng xuất hiện trong dãy. V1 không đánh dấu NEUTRALIZED "
            "trừ khi có cấu trúc hóa giải đã khóa."
        )
    for energy_id, controller in CONTROL_RELATIONS.items():
        if energy_id in present and controller in present:
            lines.append(
                f"{ENERGY_DISPLAY_NAMES[controller]} chế/giảm "
                f"{ENERGY_DISPLAY_NAMES[energy_id]} theo quan hệ đã khóa."
            )
    return lines


def _strengths_and_watchouts(
    occurrences: tuple[EnergyOccurrence, ...],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Always expose both useful and risky sides from frozen catalog fields."""
    strengths: list[str] = []
    watchouts: list[str] = []
    seen: set[str] = set()
    for item in occurrences:
        if item.energy_id in seen:
            continue
        seen.add(item.energy_id)
        catalog = ENERGY_CATALOG[item.energy_id]
        strengths.append(f"{item.display_name}: {catalog['customer_summary']}")
        watchouts.append(
            f"{item.display_name}: {catalog['shadow']}; {catalog['excessive_effect']}"
        )
    if not occurrences:
        watchouts.append(
            "Chưa có trường khí Du Niên được định nghĩa cho toàn bộ dãy này trong V1."
        )
    return tuple(strengths), tuple(watchouts)


def _unknown_notice(undefined: tuple[UndefinedSegment, ...]) -> str | None:
    """Explain undefined spans without inventing a rule."""
    if not undefined:
        return None
    reasons = "; ".join(
        f"{item.source_digits} ({item.reason})" for item in undefined
    )
    return (
        "Trạng thái UNKNOWN_OR_NOT_DEFINED: "
        f"{reasons}."
    )


def _unique_names(occurrences: tuple[EnergyOccurrence, ...]) -> str:
    """Join unique display names in first-seen order."""
    names: list[str] = []
    for item in occurrences:
        if item.display_name not in names:
            names.append(item.display_name)
    return ", ".join(names) if names else "không có cặp đã khóa"


def _assert_safe(narrative: CustomerNarrative) -> None:
    """Refuse forbidden fatalistic or medical-certainty wording."""
    blob = " ".join(
        [
            narrative.summary,
            *narrative.paragraphs,
            *narrative.strengths,
            *narrative.watchouts,
            narrative.purpose_focus,
            narrative.compatibility_note,
            narrative.health_disclaimer or "",
            narrative.unknown_notice or "",
        ]
    ).lower()
    for phrase in FORBIDDEN_CUSTOMER_PHRASES:
        if phrase.lower() in blob:
            raise NumberEnergyEngineError(f"forbidden customer phrase: {phrase}")


def narrative_from_result(result: NumberEnergyResult) -> CustomerNarrative:
    """Re-compose narrative from an existing result (test helper)."""
    return compose_narrative(
        input_raw=result.input_raw,
        occurrences=result.occurrences,
        undefined=result.undefined_segments,
        summary=result.summary,
        purpose_context=result.purpose_context,
        approved_patterns=result.approved_patterns,
    )
