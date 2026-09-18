"""Customer-safe meanings for zero/five modifiers by position and energy."""

from __future__ import annotations

from engines.number_energy.constants import CHALLENGING_ENERGY_IDS
from engines.number_energy.types import EnergyOccurrence

POSITION_INTERPOSED = "INTERPOSED"
POSITION_INTERPOSED_ZERO_FIVE = "INTERPOSED_ZERO_FIVE"
POSITION_POST = "POST"
POSITION_POST_ZERO_FIVE = "POST_ZERO_FIVE"


def customer_modifier_note(item: EnergyOccurrence) -> str | None:
    """Return a cautious customer narrative for a resolved modifier occurrence."""
    position = modifier_position(item)
    if position is None:
        return None
    if position == POSITION_INTERPOSED_ZERO_FIVE:
        return _interposed_zero_five_note(item.energy_id, item.pair_digits)
    if position == POSITION_POST_ZERO_FIVE:
        return (
            "Cặp số kết bằng 05: trường khí đã hình thành nhưng thành quả sau cùng "
            "dễ bị rút bớt, khó tích tụ trọn vẹn dù quá trình có nhiều nỗ lực."
        )
    if item.via_modifier == 0:
        return _zero_note(item.energy_id, item.pair_digits, position)
    if item.via_modifier == 5:
        return _five_note(item.energy_id, item.pair_digits, position)
    return None


def modifier_position(item: EnergyOccurrence) -> str | None:
    """Infer the preserved modifier position from source and underlying pair."""
    source = item.source_digits
    pair = item.pair_digits
    if source == f"{pair}05":
        return POSITION_POST_ZERO_FIVE
    if len(source) == 4 and source[0] + source[3] == pair and source[1:3] == "05":
        return POSITION_INTERPOSED_ZERO_FIVE
    if len(source) == 3 and source[0] + source[2] == pair:
        return POSITION_INTERPOSED
    if source.startswith(pair) and len(source) > len(pair):
        return POSITION_POST
    return None


def _zero_note(energy_id: str, pair: str, position: str) -> str:
    if position == POSITION_POST:
        return _post_zero_note(energy_id)

    notes = {
        "jue_ming": (
            "Số 0 kẹp giữa Tuyệt Mệnh làm lực đầu tư bị mắc kẹt, khó đạt "
            "kết quả mong muốn và cần thận trọng hơn khi phân bổ nguồn lực."
        ),
        "huo_hai": (
            "Số 0 kẹp giữa Họa Hại cho thấy có khả năng diễn đạt nhưng khó "
            "truyền đạt trọn ý; những vấn đề cần lưu ý cũng dễ ở trạng thái kín."
        ),
        "liu_sha": (
            "Số 0 kẹp giữa Lục Sát làm cảm xúc dễ nặng nề hơn, tăng xu hướng "
            "u buồn và giữ cảm xúc tiêu cực ở bên trong."
        ),
        "wu_gui": (
            "Số 0 kẹp giữa Ngũ Quỷ làm hoạt động suy nghĩ tăng nhưng khó giải "
            "tỏa, dễ suy nghĩ nhiều và nghiêng theo hướng tiêu cực."
        ),
        "tian_yi": _tian_yi_zero_interposed(pair),
        "sheng_qi": (
            "Số 0 kẹp giữa Sinh Khí làm quý nhân và cơ hội ở trạng thái ẩn, "
            "khó nhận ra trợ lực và dễ gặp lực cản trong quá trình thực hiện."
        ),
        "yan_nian": (
            "Số 0 kẹp giữa Diên Niên làm công việc và sự nghiệp dễ bị đình "
            "trệ, năng lực khó phát huy liên tục."
        ),
        "fu_wei": (
            "Số 0 kẹp giữa Phục Vị làm trạng thái đang kéo dài chuyển vào bên "
            "trong, khó biểu hiện và khó tạo kết quả rõ ràng."
        ),
    }
    return notes[energy_id]


def _interposed_zero_five_note(energy_id: str, pair: str) -> str:
    notes = {
        "jue_ming": (
            "Cụm 05 kẹp giữa Tuyệt Mệnh cho thấy việc đầu tư ban đầu dễ bị "
            "kẹt hoặc hao hụt, sau đó xu hướng đầu tư lại lộ rõ và kéo dài; "
            "cần quản lý nguồn lực chặt chẽ."
        ),
        "huo_hai": (
            "Cụm 05 kẹp giữa Họa Hại làm lời nói hoặc vấn đề cần lưu ý ban "
            "đầu khó nhận thấy, sau đó biểu hiện rõ và có thể kéo dài hơn."
        ),
        "liu_sha": (
            "Cụm 05 kẹp giữa Lục Sát làm cảm xúc bị dồn nén ở bên trong rồi "
            "bộc lộ rõ, mạnh và kéo dài hơn."
        ),
        "wu_gui": (
            "Cụm 05 kẹp giữa Ngũ Quỷ làm suy nghĩ nặng và khó giải tỏa ở "
            "giai đoạn đầu, sau đó biến động tư duy biểu hiện rõ và kéo dài hơn."
        ),
        "tian_yi": (
            "Cụm 05 kẹp giữa Thiên Y cho thấy tài nguyên ban đầu dễ bị ẩn, "
            "kẹt hoặc hao tổn, sau đó được làm lộ và tăng cường; quá trình tạo "
            "Tài dễ có nhịp gián đoạn và cần quản lý dòng tiền."
        ),
        "sheng_qi": (
            "Cụm 05 kẹp giữa Sinh Khí cho thấy quý nhân hoặc cơ hội ban đầu "
            "khó nhận ra, sau đó mới xuất hiện rõ và tăng lên."
        ),
        "yan_nian": (
            "Cụm 05 kẹp giữa Diên Niên cho thấy công việc ban đầu dễ đình "
            "trệ, sau đó năng lực và nỗ lực mới được nhìn thấy rõ hơn."
        ),
        "fu_wei": (
            "Cụm 05 kẹp giữa Phục Vị làm trạng thái ban đầu bị ẩn hoặc gián "
            "đoạn, sau đó được biểu hiện và kéo dài rõ hơn."
        ),
    }
    note = notes[energy_id]
    if energy_id == "tian_yi" and pair in {"13", "31"}:
        note += (
            " Với cặp 13/31, chuyện tình cảm từ kín đáo có thể chuyển sang "
            "biểu hiện rõ; cần minh bạch để hạn chế thị phi."
        )
    return note


def _post_zero_note(energy_id: str) -> str:
    specific = {
        "jue_ming": (
            "Với Tuyệt Mệnh, kế hoạch đầu tư và thành quả dễ bị hụt ở chặng "
            "cuối, cần đặc biệt tránh dồn nguồn lực mà thiếu phương án thu hồi."
        ),
        "huo_hai": (
            "Với Họa Hại, lời nói và vấn đề cần lưu ý khó biểu hiện rõ ra ngoài."
        ),
    }.get(energy_id)
    general = (
        "Số 0 đứng sau cặp số làm kết quả bị rút bớt: công việc có thể bận rộn "
        "nhưng thành quả cuối cùng khó tích tụ trọn vẹn."
    )
    return f"{specific} {general}" if specific else general


def _five_note(energy_id: str, pair: str, position: str) -> str:
    if position == POSITION_POST:
        return _post_five_note(energy_id, pair)

    notes = {
        "jue_ming": (
            "Số 5 kẹp giữa Tuyệt Mệnh làm xu hướng đầu tư biểu hiện nổi bật "
            "hơn vào một lĩnh vực cụ thể; cần đi cùng khả năng quản lý rủi ro."
        ),
        "huo_hai": (
            "Số 5 kẹp giữa Họa Hại làm lời nói, hao tổn và vấn đề cần lưu ý "
            "biểu hiện rõ hơn, đồng thời có xu hướng phát sinh liên tiếp."
        ),
        "liu_sha": (
            "Số 5 kẹp giữa Lục Sát làm cảm xúc và quan hệ biểu hiện rõ, mạnh "
            "và kéo dài hơn; cần tránh để cảm xúc dẫn dắt quyết định."
        ),
        "wu_gui": (
            "Số 5 kẹp giữa Ngũ Quỷ làm tư duy và biến động được kích hoạt rõ, "
            "mạnh và kéo dài hơn."
        ),
        "tian_yi": _tian_yi_five_interposed(pair),
        "sheng_qi": (
            "Số 5 kẹp giữa Sinh Khí làm quý nhân và cơ hội nổi bật, giúp nhận "
            "biết rõ ai đang mang lại trợ lực."
        ),
        "yan_nian": (
            "Số 5 kẹp giữa Diên Niên làm nỗ lực và thực lực được nhìn thấy rõ, "
            "nhưng khả năng phát huy vẫn có giới hạn cần vượt qua."
        ),
        "fu_wei": (
            "Số 5 kẹp giữa Phục Vị làm trạng thái trước đó biểu hiện rõ và kéo "
            "dài hơn."
        ),
    }
    return notes[energy_id]


def _post_five_note(energy_id: str, pair: str) -> str:
    notes = {
        "jue_ming": (
            "Số 5 đứng sau Tuyệt Mệnh làm xu hướng đầu tư kéo dài và tăng lên; "
            "nếu quản lý không tốt, nguồn lực dễ bị phân tán."
        ),
        "huo_hai": (
            "Số 5 đứng sau Họa Hại làm hao tổn và vấn đề cần lưu ý ngày càng "
            "rõ, mạnh và kéo dài hơn."
        ),
        "liu_sha": (
            "Số 5 đứng sau Lục Sát làm cảm xúc và các vấn đề quan hệ ngày càng "
            "rõ, mạnh và kéo dài hơn."
        ),
        "wu_gui": (
            "Số 5 đứng sau Ngũ Quỷ làm suy nghĩ và biến động ngày càng mạnh, "
            "dễ kéo dài nếu không được điều tiết."
        ),
        "tian_yi": (
            "Số 5 đứng sau Thiên Y làm tài phú và nguồn lực có xu hướng ngày "
            "càng tăng và biểu hiện rõ hơn."
        ),
        "sheng_qi": (
            "Số 5 đứng sau Sinh Khí làm quý nhân, cơ hội và trợ lực có xu hướng "
            "ngày càng nhiều hơn."
        ),
        "yan_nian": (
            "Số 5 đứng sau Diên Niên làm năng lực, chuyên môn và sức làm việc "
            "có xu hướng ngày càng mạnh hơn."
        ),
        "fu_wei": (
            "Số 5 đứng sau Phục Vị làm trạng thái đang có tiếp tục được tăng "
            "cường và kéo dài."
        ),
    }
    note = notes[energy_id]
    if energy_id == "tian_yi" and pair in {"13", "31"}:
        note += (
            " Với cặp 13/31, chuyện tình cảm cũng dễ lộ rõ và cần minh bạch "
            "để hạn chế thị phi."
        )
    return note


def _tian_yi_zero_interposed(pair: str) -> str:
    note = (
        "Số 0 kẹp giữa Thiên Y làm tài nguyên dễ bị mắc kẹt: mua tài sản có "
        "thể phát sinh nợ, cho mượn khó thu hồi hoặc đầu tư chậm quay vòng."
    )
    if pair in {"13", "31"}:
        note += (
            " Với cặp 13/31, tình cảm có xu hướng kín; cần làm rõ ranh giới "
            "để tránh phát sinh mối quan hệ thứ ba."
        )
    return note


def _tian_yi_five_interposed(pair: str) -> str:
    note = (
        "Số 5 kẹp giữa Thiên Y làm tài phú biểu hiện rõ nhưng quá trình kiếm "
        "tiền thường đòi hỏi nhiều công sức hơn."
    )
    if pair in {"13", "31"}:
        note += (
            " Với cặp 13/31, chuyện tình cảm dễ lộ ra và cần minh bạch để "
            "hạn chế thị phi."
        )
    return note


def is_zero_modified_challenging(item: EnergyOccurrence) -> bool:
    """Score signal: zero does not erase a challenging underlying energy."""
    return item.via_modifier == 0 and item.energy_id in CHALLENGING_ENERGY_IDS
