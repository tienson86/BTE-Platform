"""Customer prose: keep Day Master stages separate from pillar-stem stages."""
from collections.abc import Mapping

_ROLES = {
    "Tỷ Kiên": "tính tự chủ và sự hỗ trợ giữa những người ngang vai",
    "Kiếp Tài": "sự cạnh tranh và cách phân chia quyền lợi khi cùng làm",
    "Thực Thần": "khả năng chăm chút, truyền đạt và biến kinh nghiệm thành việc hữu ích",
    "Thương Quan": "thói quen đặt câu hỏi và tìm cách làm mới",
    "Chính Tài": "thói quen gìn giữ nguồn lực và làm đều những việc đã nhận",
    "Thiên Tài": "khả năng kết nối và nhận ra cơ hội ngoài kế hoạch quen thuộc",
    "Chính Quan": "ý thức giữ lời, trách nhiệm và nề nếp",
    "Thất Sát": "khả năng đứng ra xử lý việc khó dưới áp lực",
    "Chính Ấn": "việc học, sự dìu dắt và kinh nghiệm có thể truyền lại",
    "Thiên Ấn": "lối học độc lập và khả năng nhìn việc từ một góc khác",
}
_STAGES = {
    "Trường Sinh": "nét học hỏi và phát triển khi có môi trường nâng đỡ",
    "Mộc Dục": "sự tò mò, sức hút và nhu cầu trải nghiệm",
    "Quan Đới": "việc rèn tác phong và xây dựng vai trò rõ ràng",
    "Lâm Quan": "khả năng đứng ra đảm đương việc của mình",
    "Đế Vượng": "nhu cầu chủ động và biết dùng sức đúng lúc",
    "Suy": "việc chọn lọc điều đáng tiếp tục",
    "Bệnh": "nhu cầu điều chỉnh nhịp khi một cách làm không còn phù hợp",
    "Tử": "việc khép lại nếp cũ để dành chỗ cho cách mới",
    "Mộ": "nét giữ kín, gom góp và tích lũy",
    "Tuyệt": "việc tự tìm chỗ đứng khi cách dựa vào nền cũ không còn phù hợp",
    "Thai": "việc nuôi một hướng mới khi nó chưa thành hình",
    "Dưỡng": "nhu cầu dành thời gian nuôi nền và làm quen dần",
}

def _map(v):
    return v if isinstance(v, Mapping) else {}

def _pillar(p, position):
    return _map(_map(p.get("bazi")).get(position + "_pillar"))

def _match(p, position, stem, branch, god, stage):
    a = _pillar(p, position)
    return (_map(p.get("bazi")).get("day_master") == "Canh"
            and (a.get("stem"), a.get("branch"), a.get("ten_god"), a.get("truong_sinh"))
            == (stem, branch, god, stage))

def _sample(p):
    return (_match(p, "year", "Bính", "Dần", "Thất Sát", "Tuyệt")
            and _match(p, "month", "Tân", "Sửu", "Kiếp Tài", "Mộ")
            and _match(p, "hour", "Mậu", "Dần", "Thiên Ấn", "Tuyệt")
            and _pillar(p, "day").get("branch") == "Ngọ")

def pillar_domain(key, p):
    if key == "parents" and _match(p, "year", "Bính", "Dần", "Thất Sát", "Tuyệt"):
        return [
            'Bính Thất Sát ở trụ năm gợi một nếp trưởng thành mà lời khen đôi khi không đến bằng câu “con làm tốt”, mà đến bằng việc người lớn yên tâm giao cho bạn một việc khó hơn. Nếu lớn lên trong nếp ấy, bạn dễ quen với việc tự tìm cách giải quyết trước khi kể mình đang vướng ở đâu. Cái được là gặp việc bất ngờ, bạn thường nghĩ ngay đến bước tiếp theo. Cái khó là người thân có thể tưởng bạn luôn xoay xở được, kể cả lúc bạn cũng muốn có người đỡ một tay.',
            'Điều đáng nhìn lại là nhà đã truyền cho bạn điều gì có thể mang theo khi bước ra ngoài. Có khi đó là một nghề; có khi chỉ là cách giữ lời, cách đối đãi với khách hay cách người lớn xoay xở lúc nhà có việc. Những thứ ấy lúc nhỏ dễ thấy bình thường, đến khi tự làm việc mới biết chúng quý thế nào. Đường tự lập của Bính Dần có thể bắt đầu ngay khi bạn còn sống gần gia đình: đó là lúc bạn chọn một hướng khác với điều mọi người mong đợi và tự chịu trách nhiệm về lựa chọn ấy.',
        ]
    if key == "ancestry" and _match(p, "year", "Bính", "Dần", "Thất Sát", "Tuyệt"):
        return ["Nếp nhà và đường tự lập: Bính Hỏa ở Dần có chỗ dựa, nên chữ Tuyệt của Canh tại Dần không làm áp lực từ bên ngoài tự mất đi. Nét đáng luận là cách bạn đứng vững trước kỳ vọng của gia đình và tìm chỗ đứng bằng việc mình làm được. Điều thừa hưởng có thể là nếp chịu trách nhiệm, một nghề hoặc kinh nghiệm của người đi trước. Tự lập ở đây có thể là tự quyết đường nghề và chịu trách nhiệm về lựa chọn của mình, ngay cả khi vẫn sống gần nhà."]
    if key == "career" and _match(p, "month", "Tân", "Sửu", "Kiếp Tài", "Mộ"):
        return ["Cách làm việc với người ngang vai: Tân Sửu gợi thói quen tự giữ phần việc cốt lõi và gom kinh nghiệm qua từng lần làm. Trong môi trường cạnh tranh, bạn có thể phát huy bằng cách giữ sổ sách và tiêu chuẩn rõ ràng. Nếu muốn cùng bạn bè mở việc, hãy thử một phần việc có thời hạn trước; nhìn cách mỗi người xử lý chi phí và trách nhiệm rồi mới quyết định có nên góp vốn lâu dài."]
    if key == "siblings" and _match(p, "month", "Tân", "Sửu", "Kiếp Tài", "Mộ"):
        return [
            'Tân Kiếp Tài đưa chuyện so vai, góp sức và chia phần vào những mối quan hệ gần. Sửu ở thế Mộ của Canh lại có nét thu vào, giữ lại. Hai nét ấy đi cùng nhau khiến bạn có thể rộng lòng khi giúp một người, nhưng dè dặt khi giao cho họ quyền quyết định việc mình đang gây dựng. Với anh em hay bạn thân, bạn có thể sẵn sàng góp một tay lúc họ cần, nhưng chuyện sổ sách, khách hàng hoặc kế hoạch chưa thành hình thì thường muốn giữ cho đến khi đủ chắc mới nói.',
            'Trong nghề, nét Tân Sửu dễ thấy ở những thứ bạn âm thầm tích lũy: một cuốn sổ ghi lại những ca khó, một cách làm đã sửa qua nhiều lần, hay một nhóm khách quay lại vì biết bạn giữ lời. Người ngoài có thể chỉ thấy lúc bạn đưa ra một kết quả khá gọn; phần họ không thấy là bạn đã dành bao lâu để loại bỏ những cách làm không hiệu quả.',
            'Chỗ dễ vướng là người thân nghĩ đã thân thì chuyện gì cũng có thể nói sau, còn bạn càng coi trọng mối quan hệ lại càng muốn nói rõ từ đầu. Bạn bè giới thiệu khách giúp nhau là một chuyện; cùng nhận tiền, cùng hứa kết quả với khách lại là chuyện khác. Nói được ranh giới ấy ngay khi hai bên còn vui vẻ sẽ dễ hơn nhiều so với đợi đến lúc một người thấy mình làm nhiều mà phần nhận về không tương xứng.',
        ]
    if key == "children" and _match(p, "hour", "Mậu", "Dần", "Thiên Ấn", "Tuyệt"):
        return [
            'Mậu Thiên Ấn ở trụ giờ gợi một người càng có kinh nghiệm càng thích quay lại hỏi: Vì sao cách này đúng trong trường hợp ấy, nhưng sang trường hợp khác lại không dùng được? Về sau, bạn có thể thấy thú vị khi đọc lại những điều từng tin là hiển nhiên, ghi chép điều mình đã nghiệm qua và truyền nghề bằng chính những câu chuyện thật. Có khi một buổi chỉ cho người đi sau cách nhận ra một sai sót lại làm bạn vui hơn việc tự tay xử lý thêm mười ca quen thuộc.',
            'Với con cái, điều dễ chạm nhau cũng nằm ở chữ tự lập. Bạn đã quen tự tìm lời giải nên có thể rất quý đứa con biết suy nghĩ riêng. Nhưng khi con chọn một hướng bạn từng đi qua và thấy khó, bản năng của bạn có thể là chỉ ngay lối an toàn hơn. Con lúc ấy chưa chắc đang gạt kinh nghiệm của cha mẹ sang một bên; có thể con chỉ muốn được thử bằng đôi chân của mình. Thay vì nói ngay “đường đó không được đâu”, bạn có thể kể “mình từng vấp ở chỗ này; nếu con vẫn muốn thử, mình cùng tính xem vấp thì đứng dậy bằng cách nào”. Đó là một cách truyền kinh nghiệm mà vẫn để con có phần đời của nó.',
        ]
    positions = {"parents": "year", "ancestry": "year", "siblings": "month", "children": "hour"}
    if key not in positions:
        return []
    a = _pillar(p, positions[key])
    role, stage = _ROLES.get(a.get("ten_god")), _STAGES.get(a.get("truong_sinh"))
    if not role or not stage or not a.get("branch"):
        return []
    contexts = {
        "parents": ("Bố mẹ và tuổi nhỏ", "Hãy nhìn lại cách người lớn giao việc, góp ý và nâng đỡ bạn khi còn nhỏ. Khi có việc gia đình, nói rõ phần bạn có thể nhận sẽ dễ phối hợp hơn tự đoán điều bố mẹ mong đợi."),
        "ancestry": ("Nếp nhà và gia tiên", "Điều được truyền lại đôi khi là nghề, cách giữ lời hay cách gia đình xử lý lúc khó. Hãy chọn một nếp tốt đã thấy có ích để tiếp nối bằng việc làm cụ thể."),
        "siblings": ("Anh em và bạn bè", "Khi cùng làm, nên nói rõ ai góp công, ai quyết việc và chia phần thế nào. Một lần bàn thẳng lúc bắt đầu có thể giữ được tình thân khi kết quả khác dự tính."),
        "children": ("Con cái và hậu vận", "Nếu muốn truyền kinh nghiệm cho con hoặc người đi sau, hãy cho họ thử một việc nhỏ rồi cùng nhìn lại kết quả. Về sau, giữ một việc mình còn muốn học hoặc chia sẻ cũng giúp đời sống có nhịp riêng."),
    }
    title, action = contexts[key]
    return [f"{title}: {a.get('ten_god')} ở trụ này gợi {role}. Xét thêm {a.get('truong_sinh')}, lá số có thêm {stage}. {action}"]

def pillar_synthesis(p):
    if not _sample(p):
        return []
    return [
        "Đường đời: Bính Dần đặt ra bài học đứng vững trước yêu cầu khó; Tân Sửu cho thấy giá trị của việc gom kinh nghiệm và giữ quyền chủ động. Đến Canh Ngọ, sở trường dễ được người khác nhận ra hơn khi bạn trình bày được điều đã học và làm đến nơi việc mình nhận. Mậu Dần mở thêm hướng học sâu, xây phương pháp hoặc truyền nghề. Đường đi đáng vun đắp là từ tự đứng vững đến tích lũy, rồi dùng chuyên môn để gây dựng tên tuổi.",
        "Quan và Ấn: Đinh Chính Quan, Kỷ Chính Ấn trong Ngọ đi cùng Mậu Thiên Ấn ở giờ, gợi cả khả năng học có hệ thống lẫn thói quen tự tìm lời giải. Dần gặp Ngọ có thế bán hợp hướng Hỏa, còn thiếu Tuất để xét đủ bộ tam hợp. Trong đời sống, điều đáng phát huy là đưa cách hiểu riêng vào việc có tiêu chuẩn, có người kiểm chứng và có kết quả người khác dùng được.",
    ]

def pillar_recommendations(p):
    a = _pillar(p, "day")
    if _map(p.get("bazi")).get("day_master") != "Canh" or a.get("branch") != "Ngọ":
        return []
    return [
        "Trong nghề, hãy giữ một hướng đủ lâu để người khác nhớ đến bạn vì việc bạn làm tốt nhất. Khi thấy chán, hãy xem thứ cần đổi là nghề, vai trò hay chỉ là cách làm. Đôi khi cái mới có ích nhất là tìm ra một cách tốt hơn để làm việc mình đã giỏi, rồi kiên trì đến lúc người khác nhìn thấy kết quả.",
        "Trong tình cảm, sự thủy chung cần đi cùng sự minh bạch. Người bạn đời dễ yên lòng hơn khi những mối quan hệ bên ngoài có giới hạn rõ, và khi những chuyện vui buồn quan trọng vẫn được mang về kể cho nhau. Bạn vốn có thể lo được nhiều việc cho người mình thương. Điều đáng vun thêm là để họ cảm thấy, ngay cả khi bạn chưa lo xong mọi việc, hai người vẫn đang ở cùng một phía.",
    ]
