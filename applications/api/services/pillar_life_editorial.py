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

# Each scene is chosen by the role of the actual pillar, not by a sample chart.
_FAMILY = {
    "Tỷ Kiên": "peer", "Kiếp Tài": "peer",
    "Thực Thần": "voice", "Thương Quan": "voice",
    "Chính Tài": "resources", "Thiên Tài": "resources",
    "Chính Quan": "duty", "Thất Sát": "duty",
    "Chính Ấn": "learning", "Thiên Ấn": "learning",
}
_SCENES = {
    "parents": {
        "peer": "Trong nhà, có thể bạn muốn được tự làm một phần việc để người lớn thấy mình đã đủ sức. Khi bất đồng, nói rõ phần nào bạn muốn tự quyết và phần nào vẫn mong bố mẹ góp ý sẽ dễ nghe hơn một lời từ chối chung.",
        "voice": "Bạn có thể nhớ rõ những lúc người lớn chịu nghe mình giải thích vì sao muốn làm khác. Khi có chuyện khó nói với bố mẹ, thử kể một việc cụ thể đã xảy ra rồi mới nói điều mình mong họ hiểu.",
        "resources": "Sự chăm sóc trong nhà có thể được cảm nhận rõ qua những việc rất thực tế: dành thời gian, chuẩn bị cho nhau hoặc góp sức khi ai đó thiếu người. Nếu cần giúp bố mẹ, hãy hỏi việc nào thực sự làm họ nhẹ gánh trong tuần này.",
        "duty": "Khi được giao việc sớm, bạn có thể quen chứng tỏ mình bằng cách lo cho xong. Nếu một trách nhiệm trong nhà đang dồn về phía bạn, hãy nói phần mình nhận được và nhờ người thân nhận một phần cụ thể.",
        "learning": "Điều còn theo bạn từ gia đình đôi khi là cách một người lớn kiên nhẫn chỉ cho bạn làm một việc. Nếu muốn hiểu vì sao bố mẹ hay nhắc một điều, thử hỏi họ đã học điều ấy trong hoàn cảnh nào.",
    },
    "siblings": {
        "peer": "Bạn bè có thể giúp nhau rất nhanh, nhất là khi mỗi người đều muốn tự đứng trên phần việc của mình. Khi việc chung bắt đầu có tiền hoặc khách hàng, chốt trước ai quyết, ai giao việc và chia phần thế nào.",
        "voice": "Trong nhóm, bạn có thể là người nói ra cách làm khác khi cả nhóm đang mắc kẹt. Hãy đưa một ví dụ nhỏ để mọi người cùng thử; người nghe sẽ dễ góp ý hơn khi biết ý tưởng đó giúp việc gì.",
        "resources": "Một người giới thiệu cơ hội, người khác bỏ công theo đến cùng. Trước khi cùng nhận việc, hãy thống nhất phần đóng góp nào là giúp nhau và phần nào được tính vào quyền lợi.",
        "duty": "Khi nhóm có việc gấp, bạn có thể đứng ra giữ tiến độ. Trước lúc nhận thêm việc thay người khác, hãy nói rõ ai làm phần còn lại và khi nào cả nhóm nhìn lại cách chia việc.",
        "learning": "Bạn có thể quý người đồng nghiệp chịu chỉ cho mình một cách làm và giải thích vì sao nó hiệu quả. Khi trao lại kinh nghiệm, hãy dùng một ca cụ thể để cả hai thấy chỗ nào áp dụng được và chỗ nào cần đổi.",
    },
    "children": {
        "peer": "Bạn có thể quý đứa trẻ biết tự chọn, nhưng vẫn sốt ruột khi nó chọn đường bạn thấy khó. Hãy cùng con chốt một giới hạn an toàn rồi để con thử và kể lại điều tự học được.",
        "voice": "Một việc bạn thích có thể trở thành dịp gần con hơn nếu hai người được cùng làm. Hãy hỏi con muốn làm theo cách nào trước khi chỉ cách của mình; về sau, những lần cùng thử dễ thành kỷ niệm hơn những lời dặn dài.",
        "resources": "Muốn truyền cách tự lo, bạn có thể cùng con chọn một khoản nhỏ hoặc một việc vừa sức để tự lên kế hoạch. Khi nhìn lại, hãy hỏi con đã cân nhắc thế nào để thấy cả cách nghĩ đằng sau kết quả.",
        "duty": "Bạn có thể muốn con học cách giữ lời và chịu trách nhiệm. Hãy chọn một việc vừa sức, nói rõ khi nào cần hoàn thành và cùng con xem lại nếu chưa làm được; đó cũng là cách truyền nếp nhà về sau.",
        "learning": "Về sau, điều đáng trao lại có thể là cách bạn đi tìm lời giải khi gặp một việc lạ. Kể cho con hoặc người đi sau một lần bạn từng đổi ý và vì sao; họ sẽ có thêm cách tự cân nhắc khi gặp chuyện tương tự.",
    },
}
_STAGE_STEP = {
    "Trường Sinh": "Hãy bắt đầu bằng một việc nhỏ có người cùng thử.",
    "Mộc Dục": "Khi có nhiều điều mới để thử, chọn một việc để theo đủ lâu rồi hãy đổi.",
    "Quan Đới": "Nói rõ vai trò và việc mỗi người sẽ làm trước khi bắt đầu.",
    "Lâm Quan": "Nhận phần có thể tự quyết và nói rõ khi nào cần người khác góp sức.",
    "Đế Vượng": "Khi đã đủ sức đứng ra lo việc, vẫn dành cho người khác một phần họ được tự quyết.",
    "Suy": "Chọn việc còn đáng giữ sức, rồi bàn cách giảm bớt phần đang ôm.",
    "Bệnh": "Nếu cách cũ làm cả hai mệt, thử đổi nhịp hoặc chia lại phần việc.",
    "Tử": "Xem điều gì đã hết tác dụng để khép lại cho rõ và dành chỗ cho cách mới.",
    "Mộ": "Chọn một điều đã tích lũy có ích và chia sẻ đúng lúc, thay vì giữ mọi thứ cho riêng mình.",
    "Tuyệt": "Khi cách cũ không còn giúp được, thử một cách khác trong phạm vi nhỏ.",
    "Thai": "Giữ ý tưởng mới ở quy mô vừa đủ để quan sát trước khi hứa nhiều hơn.",
    "Dưỡng": "Cho nếp mới thời gian thành thói quen; một việc nhỏ làm đều dễ giữ hơn.",
}
_ACTION = {
    "peer": "Trước lần cộng tác tới, ghi lại phần việc, quyền quyết và cách chia kết quả.",
    "voice": "Chọn một ý tưởng đang bỏ ngỏ và thử thành một kết quả người khác có thể dùng.",
    "resources": "Chọn một việc mang lại giá trị đều và theo dõi công sức bỏ ra trong một tháng.",
    "duty": "Chọn một trách nhiệm quan trọng để làm tới nơi, rồi giao rõ phần còn lại cho người cùng làm.",
    "learning": "Ghi lại một kinh nghiệm đã có kết quả và tìm dịp chỉ lại cho người có thể dùng nó.",
}

def _stage(pillar):
    stage = pillar.get("truong_sinh")
    return "Lâm Quan" if stage in ("Kiến Lộc", "Kiến lộc") else stage

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
    god, stage_name = a.get("ten_god"), _stage(a)
    role, stage = _ROLES.get(god), _STAGES.get(stage_name)
    if not a.get("branch") or not (role or stage):
        return []
    contexts = {
        "parents": ("Bố mẹ và tuổi nhỏ", "Hãy nhìn lại cách người lớn giao việc, góp ý và nâng đỡ bạn khi còn nhỏ. Khi có việc gia đình, nói rõ phần bạn có thể nhận sẽ dễ phối hợp hơn tự đoán điều bố mẹ mong đợi."),
        "ancestry": ("Nếp nhà và gia tiên", "Điều được truyền lại đôi khi là nghề, cách giữ lời hay cách gia đình xử lý lúc khó. Hãy chọn một nếp tốt đã thấy có ích để tiếp nối bằng việc làm cụ thể."),
        "siblings": ("Anh em và bạn bè", "Khi cùng làm, nên nói rõ ai góp công, ai quyết việc và chia phần thế nào. Một lần bàn thẳng lúc bắt đầu có thể giữ được tình thân khi kết quả khác dự tính."),
        "children": ("Con cái và hậu vận", "Nếu muốn truyền kinh nghiệm cho con hoặc người đi sau, hãy cho họ thử một việc nhỏ rồi cùng nhìn lại kết quả. Về sau, giữ một việc mình còn muốn học hoặc chia sẻ cũng giúp đời sống có nhịp riêng."),
    }
    title, action = contexts[key]
    scene = _SCENES.get(key, {}).get(_FAMILY.get(god), action)
    evidence = []
    if role:
        evidence.append(f"{god} ở trụ này gợi {role}.")
    if stage:
        evidence.append(f"Khi đọc thêm {stage_name}, có thể lưu ý {stage}.")
    if stage and key in _SCENES:
        scene = f"{scene} {_STAGE_STEP[stage_name]}"
    return [f"{title}: " + " ".join(evidence), scene]

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
        lines = []
        for position, title in (("month", "Trong công việc và quan hệ ngang vai"), ("hour", "Với con cái và người đi sau"), ("year", "Với gia đình")):
            pillar = _pillar(p, position)
            if not pillar.get("branch"):
                continue
            role = _FAMILY.get(pillar.get("ten_god"))
            stage = _STAGE_STEP.get(_stage(pillar))
            if role or stage:
                detail = _ACTION.get(role, "")
                if position == "year" and role:
                    detail = "Chọn một việc có thể cùng người thân làm trong tháng này, rồi nói rõ mỗi người nhận phần nào."
                if position == "hour" and role:
                    detail = "Dành một buổi làm cùng con hoặc người đi sau, để họ tự thử một phần rồi cùng nhìn lại."
                lines.append(f"{title}: " + " ".join(x for x in (detail, stage) if x))
        return lines
    return []
    return [
        "Trong nghề, hãy giữ một hướng đủ lâu để người khác nhớ đến bạn vì việc bạn làm tốt nhất. Khi thấy chán, hãy xem thứ cần đổi là nghề, vai trò hay chỉ là cách làm. Đôi khi cái mới có ích nhất là tìm ra một cách tốt hơn để làm việc mình đã giỏi, rồi kiên trì đến lúc người khác nhìn thấy kết quả.",
        "Trong tình cảm, sự thủy chung cần đi cùng sự minh bạch. Người bạn đời dễ yên lòng hơn khi những mối quan hệ bên ngoài có giới hạn rõ, và khi những chuyện vui buồn quan trọng vẫn được mang về kể cho nhau. Bạn vốn có thể lo được nhiều việc cho người mình thương. Điều đáng vun thêm là để họ cảm thấy, ngay cả khi bạn chưa lo xong mọi việc, hai người vẫn đang ở cùng một phía.",
    ]
