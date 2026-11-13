"""Customer narrative standard: fact-specific prose, not a copied sample chart.

No calculation result is changed here. Age-aware guidance only scopes the
application of published ten-god roles; it does not predict life events.
"""
from __future__ import annotations
from typing import Any, Mapping

ROLE_READINGS = {
    "Thực Thần": ("học hỏi, diễn đạt và tạo ra điều hữu ích", "Thực Thần gắn với việc chuyển điều đã hiểu thành cách làm dễ tiếp nhận. Bạn có thể phát huy sự kiên nhẫn bằng cách làm một việc đến nơi đến chốn, rồi chia sẻ kinh nghiệm theo cách người khác hiểu được."),
    "Thương Quan": ("tư duy độc lập và thay đổi cách làm", "Thương Quan nhấn mạnh khả năng nhận ra điều chưa hợp lý và tìm lời giải khác. Điều cần giữ là nói rõ vấn đề cùng đề xuất của mình, để sự thẳng thắn giúp tháo gỡ thay vì tạo thêm khoảng cách."),
    "Thiên Tài": ("nhận ra cơ hội và kết nối nguồn lực", "Thiên Tài gợi khả năng nhìn thấy giá trị trong những nhu cầu hoặc mối liên hệ mới. Cơ hội chỉ đáng theo đuổi khi bạn hiểu rõ phần đóng góp, chi phí và giới hạn của mình; sự xuất hiện của Tài không bảo đảm lợi nhuận."),
    "Chính Tài": ("công sức, thu nhập và khả năng tích lũy", "Chính Tài đặt trọng tâm vào giá trị được tạo ra bằng công sức đều đặn. Điều đáng chú ý không chỉ là khoản thu, mà còn là phần thời gian và nguồn lực phải bỏ ra để giữ được thành quả lâu dài."),
    "Thất Sát": ("áp lực, thử thách và khả năng tự chủ", "Thất Sát gợi những tình huống đòi hỏi sự quyết đoán và sức chịu trách nhiệm. Bạn nên phân biệt một thử thách giúp mình trưởng thành với một gánh nặng vượt quá khả năng, thay vì xem mọi sức ép đều cần đối đầu."),
    "Chính Quan": ("trách nhiệm, sự tin cậy và nguyên tắc", "Chính Quan nhấn mạnh sự rõ ràng trong vai trò và lời cam kết. Bạn có thể xây dựng sự tin cậy bằng cách làm đúng phần đã nhận, đồng thời trao đổi sớm khi điều kiện thay đổi để tránh biến trách nhiệm thành gánh nặng âm thầm."),
    "Thiên Ấn": ("tìm hiểu sâu và phát triển cách nhìn riêng", "Thiên Ấn gợi nhu cầu tìm tới nguyên nhân và học bằng trải nghiệm riêng. Điều hữu ích là kiểm tra lại điều mình hiểu, lắng nghe góc nhìn khác và diễn đạt bằng ví dụ cụ thể, để kiến thức không chỉ dừng ở suy nghĩ."),
    "Chính Ấn": ("nền tảng, học hỏi và sự nâng đỡ", "Chính Ấn hướng sự chú ý tới điều giúp bạn có điểm tựa: kiến thức, kinh nghiệm và những quan hệ tin cậy. Giữ lại điều có ích không đồng nghĩa phải giữ nguyên mọi nếp cũ; một nền vững vẫn cần chỗ cho sự thích nghi."),
    "Tỷ Kiên": ("sự độc lập và quan hệ bình đẳng", "Tỷ Kiên làm nổi bật nhu cầu tự quyết và giữ cách nhìn của mình. Sự độc lập phát huy tốt hơn khi đi cùng khả năng trao đổi, để bạn vừa giữ được nguyên tắc vừa không phải một mình gánh mọi việc."),
    "Kiếp Tài": ("chia sẻ nguồn lực và ranh giới trong quan hệ", "Kiếp Tài gợi việc cân bằng giữa mong muốn cùng người khác góp sức và nhu cầu bảo vệ phần của mình. Cần nói rõ trách nhiệm, phần đóng góp và điều có thể hỗ trợ; không suy từ tên sao rằng người thân hay cộng sự sẽ gây thiệt hại."),
}

def _age(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        result = float(value)
        return result if result >= 0 else None
    except (ValueError, TypeError):
        return None

def age_application(god: str, age: Any) -> str:
    """Keep applications suitable for the start of a published age interval."""
    age = _age(age)
    if age is None:
        return "Khi vận dụng, hãy đặt chủ đề này vào hoàn cảnh học tập, công việc và gia đình thực tế của bạn."
    if age < 18:
        if god in ("Chính Tài", "Thiên Tài", "Kiếp Tài", "Tỷ Kiên"):
            return "Ở tuổi đi học, chủ đề này nên được hiểu qua việc tự lập, chia sẻ với bạn bè và học cách quý trọng công sức, chứ chưa phải yêu cầu kiếm tiền hay gánh trách nhiệm tài chính. Gia đình có thể giúp bằng những việc nhỏ vừa sức và nguyên tắc rõ ràng."
        if god in ("Thất Sát", "Chính Quan"):
            return "Ở tuổi đi học, cần đặt việc rèn nề nếp cạnh nhu cầu được giải thích và nâng đỡ. Mục tiêu vừa sức cùng sự ghi nhận tiến bộ sẽ có ích hơn việc dùng áp lực để đòi hỏi thành tích."
        return "Trong giai đoạn học tập, bạn cần cơ hội tìm hiểu, đặt câu hỏi và thử điều mới trong môi trường có người hướng dẫn. Chưa nên dùng thành tích nhất thời để kết luận khả năng của cả cuộc đời."
    if age >= 65:
        if god in ("Chính Tài", "Thiên Tài", "Kiếp Tài"):
            return "Ở giai đoạn cao tuổi, trọng tâm thích hợp là sự chủ động trong chi tiêu và các thỏa thuận hỗ trợ trong gia đình. Những quyết định chia sẻ tiền bạc cần rõ ràng và phù hợp nhu cầu sống, không mặc định phải tiếp tục mở rộng công việc."
        if god in ("Thất Sát", "Chính Quan", "Tỷ Kiên"):
            return "Ở giai đoạn cao tuổi, điều đáng ưu tiên là quyền tự chủ và phần trách nhiệm bạn thực sự muốn giữ. Chia sẻ việc nặng với người đáng tin giúp đời sống nhẹ nhàng hơn mà vẫn tôn trọng lựa chọn của bạn."
        return "Ở giai đoạn cao tuổi, việc học và chia sẻ kinh nghiệm nên đem lại niềm vui, không trở thành một nghĩa vụ mới. Giữ những quan hệ gần gũi, nhịp sinh hoạt phù hợp và sự hỗ trợ khi cần quan trọng hơn yêu cầu tạo thêm thành tích."
    if age >= 55:
        return "Trong chặng này, bạn có thể cân nhắc điều muốn tiếp tục và điều nên trao bớt cho người khác. Việc duy trì công việc hay thay đổi nhịp sống nên phù hợp mong muốn, nguồn lực và trách nhiệm gia đình, không chỉ theo kỳ vọng bên ngoài."
    if god == "Chính Tài":
        return "Nếu gắn với công việc tạo thu nhập, hãy làm rõ giá bán, chi phí hoặc mức thanh toán và phần tiền giữ lại. Chọn quy mô có thể theo lâu thường thiết thực hơn nhận thêm việc chỉ vì khoản thu trước mắt."
    if god == "Thất Sát":
        return "Khi nhận việc khó, hãy làm rõ quyền quyết định, thời hạn và sự hỗ trợ có thể nhận. Bạn không cần chứng tỏ năng lực bằng việc nhận mọi trách nhiệm, nhất là khi phải đánh đổi thời gian nghỉ và quan hệ quan trọng."
    if age < 30:
        return "Khi mới xây dựng hướng đi, hãy thử một lựa chọn ở phạm vi vừa sức, tích lũy kinh nghiệm rồi đánh giá lại. Sự phù hợp cần được kiểm chứng bằng trải nghiệm, không chỉ bởi kỳ vọng của mình hoặc người khác."
    return "Trong công việc và gia đình, hãy chọn một việc cần ưu tiên, nói rõ điều mong muốn với người liên quan và dành thời gian kiểm tra kết quả. Cách làm phù hợp sẽ rõ dần qua trải nghiệm, thay vì quyết định vội chỉ từ một dấu hiệu của vận."

CLASHES = {frozenset(p) for p in (("Tý", "Ngọ"), ("Sửu", "Mùi"), ("Dần", "Thân"), ("Mão", "Dậu"), ("Thìn", "Tuất"), ("Tỵ", "Hợi"))}
COMBINES = {frozenset(p) for p in (("Tý", "Sửu"), ("Dần", "Hợi"), ("Mão", "Tuất"), ("Thìn", "Dậu"), ("Tỵ", "Thân"), ("Ngọ", "Mùi"))}

def cycle_branch_context(branch: str, bazi: Mapping[str, Any]) -> str:
    facts = []
    for position, label in (("year", "năm"), ("month", "tháng"), ("day", "ngày"), ("hour", "giờ")):
        pillar = bazi.get(position + "_pillar")
        if not isinstance(pillar, Mapping):
            continue
        natal = str(pillar.get("branch") or "")
        pair = frozenset((branch, natal))
        relation = "xung" if pair in CLASHES else "hợp" if pair in COMBINES else "lặp" if branch == natal else ""
        if relation:
            facts.append(f"{branch} {relation} {natal} ở trụ {label}")
    if not facts:
        return ""
    return "Đối chiếu nguyên cục, " + "; ".join(facts) + ". Các quan hệ này là điểm cần xét cùng toàn cục và lưu niên, không tự xác định một sự kiện tốt hay xấu. "

def current_age(payload: Mapping[str, Any]) -> float | None:
    """Use the engine's published age; do not infer it from a sample or the clock."""
    luck = payload.get("luck")
    return _age(luck.get("current_age_for_luck")) if isinstance(luck, Mapping) else None


def age_scoped_domain(key: str, payload: Mapping[str, Any]) -> list[str]:
    """Apply natal evidence at a suitable life stage, before sample-specific prose."""
    age = current_age(payload)
    if age is None or 18 <= age < 65:
        return []
    bazi = payload.get("bazi") or {}
    stem = str(bazi.get("day_master") or "")
    if not stem:
        return []
    pattern = str((payload.get("pattern") or {}).get("cach_cuc") or "")
    def pillar(position: str) -> str:
        value = bazi.get(position + "_pillar") or {}
        return " ".join(str(value.get(k) or "") for k in ("stem", "branch")).strip()
    if key == "career":
        basis = f"Mệnh cục {pattern}" if pattern else f"Nhật chủ {stem}"
        if age < 18:
            return [f"Học tập và khả năng riêng: {basis} là một điểm tham khảo khi tìm cách học phù hợp, không ấn định nghề nghiệp của bạn. Ở tuổi này, nên quan sát điều khiến bạn tò mò, cách bạn tiếp nhận hướng dẫn và những việc bạn muốn thử lại.",
                    "Từng bước khám phá: Chọn hoạt động vừa sức để được làm, hỏi và nhận góp ý. Gia đình nên tạo cơ hội tiếp xúc nhiều lĩnh vực, thay vì chốt sớm một nghề từ lá số hoặc một kết quả học tập."]
        return [f"Công việc và trải nghiệm: {basis} vẫn có thể gợi cách bạn sử dụng kinh nghiệm. Việc tiếp tục làm nghề, hướng dẫn người khác hay dành thêm thời gian riêng nên do mong muốn và điều kiện thực tế của bạn quyết định.",
                "Phần muốn giữ lại: Chọn công việc đem lại ý nghĩa và nhịp sống phù hợp. Nếu nhận thêm trách nhiệm, hãy thống nhất thời gian và sự hỗ trợ; không mặc định giai đoạn này phải mở rộng hoặc phải dừng công việc."]
    if key == "marriage" and age < 18:
        return [f"Quan hệ gần gũi: Trụ ngày {pillar('day') or stem} là dữ kiện được dùng trong cách luận quan hệ truyền thống. Với người chưa trưởng thành, chưa nên suy từ đó về người phối ngẫu, thời điểm kết hôn hay một kết cục tình cảm.",
                "Điều cần học lúc này: Tập lắng nghe, nói rõ điều mình muốn và tôn trọng ranh giới của người khác. Các quan hệ an toàn, được gia đình hỗ trợ sẽ có ích hơn một dự đoán hôn nhân quá sớm."]
    if key == "children":
        evidence = f"Trụ giờ {pillar('hour')}" if pillar('hour') else "Chưa có đủ dữ kiện trụ giờ; phần này"
        if age < 18:
            return [f"Trụ giờ và điều về sau: {evidence} không phải căn cứ để đặt trách nhiệm sinh con hoặc chăm lo thế hệ sau lên bạn lúc này. Lá số không xác định số con, giới tính hay khả năng sinh sản.",
                    "Ưu tiên hiện tại: Dành chỗ cho học tập, vui chơi và trưởng thành trong môi trường có người hỗ trợ. Những lựa chọn về gia đình thuộc về tương lai và cần dựa trên nguyện vọng, điều kiện thực tế khi đã trưởng thành."]
        return [f"Điều muốn trao lại: {evidence} gợi một góc nhìn về hậu vận và sự tiếp nối, không xác nhận bạn đã có con cháu. Nếu có người muốn hướng dẫn hoặc nâng đỡ, hãy trao đổi điều họ thật sự cần thay vì quyết định thay.",
                "Giữ sự gần gũi: Chia sẻ kinh nghiệm khi được đón nhận, nói rõ mức hỗ trợ phù hợp và giữ không gian riêng cho mỗi người. Sự gắn bó không đòi hỏi bạn phải gánh mọi việc của thế hệ sau."]
    if key == "siblings" and age < 18:
        return [f"Bạn bè và anh chị em: Trụ tháng {pillar('month') or 'chưa đủ dữ kiện'} là một phần để tham khảo quan hệ ngang vai, không chỉ định ai sẽ giúp hay gây hại cho bạn.",
                "Cách cùng nhau lớn lên: Tập chia lượt, giữ lời hứa nhỏ và nói rõ khi thấy không công bằng. Khi bất đồng khó giải quyết, hãy nhờ người lớn đáng tin hỗ trợ; không cần tự chịu mọi sức ép trong nhóm."]
    if key == "wealth":
        if age < 18:
            return ["Hiểu Tài ở tuổi đi học: Những dấu Tài mô tả quan hệ trong lá số, không phải yêu cầu bạn kiếm tiền hoặc gánh tài chính gia đình. Điều phù hợp là học quý trọng công sức, phân biệt điều cần với điều muốn và biết nhờ người lớn hỗ trợ.",
                    "Thực hành vừa sức: Nếu được giao một khoản chi nhỏ, có thể tập ghi lại và để dành cho mục tiêu đơn giản. Không suy từ Tài tinh thành lời hứa giàu có hoặc lựa chọn đầu tư."]
        return ["Nguồn lực trong chặng hiện tại: Nếu có thu nhập hoặc khoản hỗ trợ, hãy đặt chúng cạnh nhu cầu sinh hoạt và các cam kết thực tế. Lá số không xác nhận mức tài sản, lương hưu hay nghĩa vụ tài chính của bạn.",
                "Quyền chủ động: Việc giúp đỡ người thân hay tiếp tục tạo thu nhập nên phù hợp mong muốn và khả năng của bạn. Nói rõ giới hạn và điều kiện trước khi nhận trách nhiệm; không xem tên sao là lý do phải mở rộng hay mạo hiểm."]
    return []
