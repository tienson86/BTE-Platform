"""Customer-facing readings selected by the published day pillar."""
from typing import Mapping

_STEMS = {
    "Giáp": ("Dương Mộc", "Bạn dễ phát huy khi có một hướng đi rõ và đủ thời gian để gây dựng. Khi đã chọn được hướng, bạn thường muốn tiến thẳng; góp ý có ví dụ cụ thể sẽ dễ giúp bạn đổi cách làm hơn lời phản đối chung chung."),
    "Ất": ("Âm Mộc", "Bạn thường tìm đường tiến bằng cách quan sát người và hoàn cảnh. Khi cách làm ban đầu gặp trở ngại, bạn có thể đổi nhịp hoặc tìm người cùng làm mà vẫn giữ mục tiêu. Điểm cần để ý là có lúc thích nghi quá lâu khiến nhu cầu của mình không được nói rõ."),
    "Bính": ("Dương Hỏa", "Bạn dễ nhập cuộc khi thấy mục đích rõ và có người hưởng ứng. Bạn có thể giúp cả nhóm hiểu vì sao một việc đáng làm; lúc quá hào hứng, hãy để ý những cam kết cần nhiều thời gian hơn dự tính."),
    "Đinh": ("Âm Hỏa", "Bạn dễ để ý những chi tiết nhỏ làm thay đổi cảm nhận của người khác: một lời nói đúng lúc hoặc một phần việc được chăm chút. Khi có quá nhiều việc cùng cần sự tập trung, bạn có thể mất nhịp; chọn một việc để làm đến nơi thường hợp hơn."),
    "Mậu": ("Dương Thổ", "Bạn thường muốn biết nền tảng đã đủ chắc chưa trước khi nhận một việc lâu dài. Người khác có thể tin bạn ở chỗ đã nhận thì theo đến cùng. Khi hoàn cảnh đổi, điều đáng xem lại là cách giữ lời, vì cách làm cũ có thể không còn phù hợp."),
    "Kỷ": ("Âm Thổ", "Bạn có xu hướng để ý những việc nhỏ giúp cả nhà hoặc cả nhóm vận hành đều. Bạn có thể thấy trước người khác cần gì, nhưng nếu cứ âm thầm làm thay, họ khó biết bạn đang cần được chia sẻ phần nào."),
    "Canh": ("Dương Kim", "Bạn thường muốn nhìn rõ điều gì đúng, việc gì đáng giữ và ai chịu trách nhiệm. Sự dứt khoát có ích khi một việc bị kéo dài vì thiếu quyết định; khi làm cùng người khác, nói rõ lý do sẽ giúp họ hiểu tiêu chuẩn của bạn."),
    "Tân": ("Âm Kim", "Bạn dễ nhận ra sự khác biệt giữa một việc làm cho xong và một việc được hoàn thiện cẩn thận. Mắt nhìn chi tiết giúp bạn nâng chất lượng; khi thời gian có hạn, hãy chọn những điểm thực sự ảnh hưởng đến người nhận."),
    "Nhâm": ("Dương Thủy", "Bạn thường nhìn thấy nhiều lối đi khi một việc bị bế tắc. Bạn dễ kết nối những nguồn thông tin hoặc những người trước đó chưa làm việc cùng nhau. Chỗ cần giữ là chọn một hướng đủ rõ để những cơ hội ấy thành kết quả."),
    "Quý": ("Âm Thủy", "Bạn có thể nắm được điều người khác chưa nói hết qua cách họ hỏi hoặc phản ứng. Bạn thường cần thời gian quan sát trước khi quyết; nếu đã hiểu đủ, nói rõ lựa chọn của mình sẽ giúp người khác theo kịp."),
}

def _map(value):
    return value if isinstance(value, Mapping) else {}

def _day(payload):
    bazi = _map(payload.get("bazi"))
    return bazi.get("day_master"), _map(bazi.get("day_pillar"))

def _canh_ngo(payload):
    stem, day = _day(payload)
    return stem == "Canh" and day.get("branch") == "Ngọ" and day.get("stem", stem) == stem

def _quan_an(payload):
    hidden = _map(payload.get("ten_gods")).get("hidden") or []
    gods = {(row.get("stem") or row.get("hidden_stem"), row.get("ten_god"))
            for row in hidden if isinstance(row, Mapping)
            and row.get("pillar") == "day" and row.get("branch", "Ngọ") == "Ngọ"}
    return {("Đinh", "Chính Quan"), ("Kỷ", "Chính Ấn")} <= gods

def day_personality(payload):
    stem, _ = _day(payload)
    if _canh_ngo(payload):
        return [
            "Canh thuộc Dương Kim, ví như sắt thép có độ cứng và đường nét rõ ràng. Canh gặp Ngọ Hỏa gợi hình ảnh kim qua lửa rèn: vẫn giữ được sự cứng cỏi bên trong, nhưng cách nói năng và cư xử bên ngoài có phần mềm mại hơn. Khi bất đồng, bạn có thể lựa lời để người đối diện không mất mặt. Nếu câu chuyện chạm đến uy tín, lời hứa hoặc điều bạn cho là đúng, bạn khó nhượng bộ chỉ để giữ hòa khí.",
            "Nét Mộc Dục ở Canh Ngọ thể hiện qua sự chỉn chu và sức hút tự nhiên. Bạn có thể ăn mặc đơn giản mà vẫn tạo ấn tượng, vì biết chọn thứ hợp với mình và hợp hoàn cảnh. Cái duyên còn nằm ở cách nói chuyện: biết lúc nào nên nghiêm túc, lúc nào có thể đùa một câu để không khí nhẹ đi.",
            "Cùng một lời góp ý, nếu được nói riêng và có lý lẽ, bạn có thể tiếp thu nhanh; nếu nói trước mặt người khác với giọng coi nhẹ, bạn dễ nhớ lâu. Bạn cũng tò mò, thích thử điều mới. Điểm dễ vướng là khi việc cũ bước vào giai đoạn chậm và lặp lại, còn hướng mới chỉ vừa xuất hiện và chưa bộc lộ khó khăn. Khi ấy, hãy thử đổi cách làm trước khi đổi cả mục tiêu.",
        ]
    if stem in _STEMS:
        nature, prose = _STEMS[stem]
        return [f"{stem} thuộc {nature}. {prose}"]
    return []

def day_domain(key, payload):
    if not (_canh_ngo(payload) and _quan_an(payload)):
        return []
    if key == "career":
        return [
            "Công danh và uy tín: Trong Ngọ có Đinh Hỏa và Kỷ Thổ, ứng với Chính Quan và Chính Ấn. Đinh sinh Kỷ, Kỷ nâng đỡ Canh. Vào công việc, trách nhiệm khiến bạn muốn học cho chắc; kiến thức tích lũy lại giúp bạn đảm đương việc lớn hơn. Bạn coi trọng danh dự nghề nghiệp và muốn việc mình đứng tên có căn cứ để giải thích khi người khác hỏi lại.",
            "Vai trò dễ phát huy: Bạn có thể hợp với việc thẩm định, hướng dẫn hoặc giữ chất lượng. Khi một nhóm làm việc mỗi người một cách, bạn có thể nhìn ra khâu nào dễ sai, đặt lại tiêu chuẩn và giải thích vì sao cần làm như vậy. Khả năng dẫn dắt thường bắt đầu từ việc đồng nghiệp tin vào cách bạn xử lý việc khó.",
            "Khi muốn đổi hướng: Mộc Dục gợi nhu cầu thử môi trường hoặc vai trò mới. Bạn có thể đổi nhóm khách, đổi cách cung cấp dịch vụ hoặc chuyển từ làm chuyên môn sang đào tạo, quản lý. Điểm cần giữ là sự bền bỉ khi dự án bước vào đoạn sửa lỗi nhỏ và hoàn thiện. Mỗi lần chuyển hướng có giá trị nhất khi chuyên môn cũ được mang theo và dùng ở vai trò tốt hơn. Muốn xác định giai đoạn dễ chuyển nghề, cần xét thêm Đại vận.",
        ]
    if key == "marriage":
        return [
            "Hình tượng người bạn đời: Ở trụ ngày Canh Ngọ, Mộc Dục gợi nét có duyên, biết chăm chút diện mạo và dễ tạo thiện cảm. Chính Ấn thêm nét ham học, có hiểu biết và biết nâng đỡ người thân lúc khó khăn. Chính Quan thêm nét có trách nhiệm với công việc, coi trọng uy tín và có ý thức làm tròn việc đã nhận.",
            "Khi mới quen và khi sống chung: Hai người dễ có nhiều điều để thích ở nhau, từ cách trò chuyện, sự chỉn chu đến những cử chỉ cho thấy mình được để ý. Khi sống chung lâu hơn, sự tin cậy được gây dựng qua những việc thực tế: lúc một người gặp khó trong công việc, người kia biết an ủi và cũng có thể ngồi xuống bàn cách tháo gỡ.",
            "Chỗ dễ nảy sinh hiểu lầm: Một người vẫn có thể chu toàn tiền bạc và việc gia đình, nhưng dành những cuộc trò chuyện vui vẻ hay tâm sự riêng cho người ngoài. Người bạn đời khi ấy có thể cảm thấy mình vẫn được lo liệu nhưng dần không còn là người được chia sẻ. Ghen tuông đôi khi bắt đầu từ cảm giác ấy, trước cả khi có chuyện vượt giới hạn. Nét duyên của Mộc Dục khiến tình huống này đáng lưu ý; riêng dấu hiệu đó chưa đủ để nói sẽ có người thứ ba.",
            "Cách giữ tình cảm: Hai người có thể nói rõ giới hạn trong những mối quan hệ bên ngoài và tiếp tục dành thời gian riêng cho nhau. Lo liệu chu đáo là một cách thương; hỏi han và ghi nhận giúp người kia cảm nhận được tình cảm ấy trong đời sống hằng ngày.",
        ]
    return []
