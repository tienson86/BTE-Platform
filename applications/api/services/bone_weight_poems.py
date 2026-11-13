"""Sino-Vietnamese readings of the received Xưng Cốt Ca, indexed by chỉ.

Reference: https://www.zhyw.net/a/xuanmendaojiao/2020/12/31/208202.html
For 27 chỉ, use the variant supplied by the project owner.
"""

POEMS = {
    21: "Đoản mệnh phi nghiệp vị đại không|Bình sinh tai nạn sự trùng trùng|Hung họa tần lâm hãm nghịch cảnh|Chung thế khốn khổ sự bất thành",
    22: "Thân hàn cốt lãnh khổ linh đinh|Thử mệnh suy lai hành khất nhân|Lao lao lục lục vô độ nhật|Chung niên đả củng quá bình sinh",
    23: "Thử mệnh suy lai cốt tự khinh|Cầu mưu tác sự sự nan thành|Thê nhi huynh đệ ưng nan hứa|Biệt xứ tha hương tác tản nhân",
    24: "Thử mệnh suy lai phúc lộc vô|Môn đình khốn khổ tổng nan vinh|Lục thân cốt nhục giai vô kháo|Lưu lãng tha hương tác lão ông",
    25: "Thử mệnh suy lai tổ nghiệp vi|Môn đình doanh độ tự hi kỳ|Lục thân cốt nhục như băng thán|Nhất thế cần lao tự bả trì",
    26: "Bình sinh y lộc khổ trung cầu|Độc tự doanh mưu sự bất hưu|Ly tổ xuất môn nghi tảo kế|Vãn lai y lộc tự vô hưu",
    27: "Nhất sinh tác sự thiếu thương lượng|Nan kháo tổ tông tác chủ trương|Độc mã đơn thương không tố khứ|Tảo niên môn hộ tự thê lương",
    28: "Nhất sinh hành sự tự phiêu bồng|Tổ tông sản nghiệp tại mộng trung|Nhược bất quá phòng cải danh tính|Dã đương di đồ nhị tam thông",
    29: "Sơ niên vận hạn vị tằng hanh|Túng hữu công danh tại hậu thành|Tu quá tứ tuần tài khả lập|Di cư cải tính thủy vi lương",
    30: "Lao lao lục lục khổ trung cầu|Đông bôn tây tẩu hà nhật hưu|Nhược sử chung thân cần dữ kiệm|Lão lai sảo khả miễn ưu sầu",
    31: "Mang mang lục lục khổ trung cầu|Hà nhật vân khai kiến nhật đầu|Nan đắc tổ cơ gia khả lập|Trung niên y thực tiệm vô ưu",
    32: "Sơ niên vận kiển sự nan mưu|Tiệm hữu tài nguyên như thủy lưu|Đáo đắc trung niên y thực vượng|Na thời danh lợi nhất tề thu",
    33: "Tảo niên tố sự sự nan thành|Bách niên cần lao uổng phí tâm|Bán thế tự như lưu thủy khứ|Hậu lai vận đáo thủy đắc kim",
    34: "Thử mệnh phúc khí quả như hà|Tăng đạo môn trung y lộc đa|Ly tổ xuất gia phương vi diệu|Triêu vãn bái Phật niệm Di Đà",
    35: "Sinh bình phúc lượng bất chu toàn|Tổ nghiệp căn cơ giác thiểu truyền|Doanh sự sinh nhai nghi thủ cựu|Thời lai y thực thắng tòng tiền",
    36: "Bất tu lao lục quá bình sinh|Độc tự thành gia phúc bất khinh|Tảo hữu phúc tinh thường chiếu mệnh|Nhậm quân hành khứ bách ban thành",
    37: "Thử mệnh ban ban sự bất thành|Đệ huynh thiểu lực tự cô hành|Tuy nhiên tổ nghiệp tu vi hữu|Lai đắc minh thời khứ bất minh",
    38: "Nhất thân cốt nhục tối thanh cao|Tảo nhập Phật môn tính thị tiêu|Đãi đáo niên tương tam thập lục|Lam sam thoát khứ hoán hồng bào",
    39: "Thử mệnh chung thân vận bất thông|Lao lao tác sự tận giai không|Khổ tâm kiệt lực thành gia kế|Đáo đắc na thời tại mộng trung",
    40: "Bình sinh y lộc thị miên trường|Kiện kiện tâm trung tự chủ trương|Tiền diện phong sương đa thụ quá|Hậu lai tất định hưởng an khang",
    41: "Thử mệnh suy lai tự bất đồng|Vi nhân năng cán dị phàm dung|Trung niên hoàn hữu tiêu dao phúc|Bất bỉ tiền thời vận lai thông",
    42: "Đắc khoan hoài xứ thả khoan hoài|Hà dụng song mi trứu bất khai|Nhược sử trung niên mệnh vận tế|Na thời danh lợi nhất tề lai",
    43: "Vi nhân tâm tính tối thông minh|Tác sự hiên ngang cận quý nhân|Y lộc nhất sinh thiên chú định|Bất tu lao lục thị phong hanh",
    44: "Vạn sự do thiên mạc khổ cầu|Tu tri phúc lộc lại nhân tu|Đương niên tài bạch nan như ý|Vãn cảnh hân nhiên tiện bất ưu",
    45: "Danh lợi suy cầu cánh nhược hà|Tiền phiên tân khổ hậu bôn ba|Mệnh trung nan dưỡng nam hòa nữ|Cốt nhục phù trì dã bất đa",
    46: "Đông tây nam bắc tận giai thông|Xuất tính di cư cánh giác long|Y lộc vô cùng vô số định|Trung niên vãn cảnh nhất ban đồng",
    47: "Thử mệnh suy cầu vượng mạt niên|Thê vinh tử quý tự di nhiên|Bình sinh nguyên hữu thao thao phúc|Khả bốc tài nguyên nhược thủy tuyền",
    48: "Ấu niên vận đạo vị tằng hanh|Nhược thị tha đà tái bất dữ|Huynh đệ lục thân giai vô kháo|Nhất thân sự nghiệp vãn niên thành",
    49: "Thử mệnh suy lai phúc bất khinh|Tự thành tự lập hiển môn đình|Tòng lai phú quý nhân khâm kính|Sử tỳ sai nô quá nhất sinh",
    50: "Vi lợi vi danh chung nhật lao|Trung niên phúc lộc dã đa tao|Lão lai tự hữu tài tinh chiếu|Bất bỉ tiền phiên mục hạ cao",
    51: "Nhất thế vinh hoa sự sự thông|Bất tu lao lục tự hanh thông|Huynh đệ thúc điệt giai như ý|Gia nghiệp thành thời phúc lộc hoành",
    52: "Nhất thế hanh thông sự sự năng|Bất tu lao khổ tự nhiên ninh|Tông tộc hữu quang hân hỉ thậm|Gia sản phong doanh tự xứng tâm",
    53: "Thử cách suy lai phúc trạch hoành|Hưng gia lập nghiệp tại kỳ trung|Nhất sinh y thực an bài định|Khước thị nhân gian nhất phúc ông",
    54: "Thử mệnh suy lai hậu thả thanh|Thi thư mãn phúc khán công thành|Phong y túc thực tự nhiên ổn|Chính thị nhân gian hữu phúc nhân",
    55: "Sách mã dương tiên tranh danh lợi|Thiếu niên tác sự phí trù luận|Nhất triêu phúc lộc nguyên nguyên chí|Phú quý vinh hoa hiển lục thân",
    56: "Thử cách suy lai lễ nghĩa thông|Nhất thân phúc lộc dụng vô cùng|Điềm toan khổ lạt giai thường quá|Cổn cổn tài nguyên doanh nhi phong",
    57: "Phúc lộc phong doanh vạn sự toàn|Nhất thân vinh diệu lạc thiên niên|Danh dương uy chấn nhân tranh tiện|Thử thế tiêu dao uyển tự tiên",
    58: "Bình sinh y thực tự nhiên lai|Danh lợi song toàn phú quý giai|Kim bảng đề danh đăng giáp đệ|Tử bào ngọc đái tẩu kim giai",
    59: "Tế suy thử cách tú nhi thanh|Tất định tài cao học nghiệp thành|Giáp đệ chi trung ưng hữu phận|Dương tiên tẩu mã hiển uy vinh",
    60: "Nhất triêu kim bảng khoái đề danh|Hiển tổ vinh tông đại khí thành|Y lộc định nhiên vô khiếm khuyết|Điền viên tài bạch cánh phong doanh",
    61: "Bất tác triều trung kim bảng khách|Định vi thế thượng đại tài ông|Thông minh thiên phó kinh thư thục|Danh hiển cao quải tự thị vinh",
    62: "Thử mệnh sinh lai phúc bất cùng|Độc thư tất định hiển thân tông|Tử y ngọc đái vi khanh tướng|Phú quý vinh hoa thục dữ đồng",
    63: "Mệnh chủ vi quan phúc lộc trường|Đắc lai phú quý thực phi thường|Danh đề nhạn tháp truyền kim bảng|Đại hiển môn đình thiên hạ dương",
    64: "Thử cách uy quyền bất khả đương|Tử bào kim đái tọa cao đường|Vinh hoa phú quý thùy năng cập|Vạn cổ lưu danh tính thị dương",
    65: "Tế suy thử mệnh phúc phi khinh|Phú quý vinh hoa thục dữ tranh|Định quốc an bang nhân cực phẩm|Uy thanh hiển hách chấn hoàn doanh",
    66: "Thử cách nhân gian nhất phúc nhân|Đôi kim tích ngọc mãn đường xuân|Tòng lai phú quý hữu thiên định|Kim bảng đề danh cánh hiển thân",
    67: "Thử mệnh sinh lai phúc tự hoành|Điền viên gia nghiệp tối cao long|Bình sinh y lộc doanh phong túc|Nhất lộ vinh hoa vạn sự thông",
    68: "Phú quý do thiên mạc khổ cầu|Vạn sự gia kế bất tu mưu|Thập niên bất bỉ tiền phiên sự|Tổ nghiệp căn cơ thiên cổ lưu",
    69: "Quân thị nhân gian phúc lộc tinh|Nhất sinh phú quý chúng nhân khâm|Tổng nhiên y lộc do thiên định|An hưởng vinh hoa quá nhất sinh",
    70: "Thử mệnh suy lai phúc bất khinh|Hà tu sầu lự khổ lao tâm|Vinh hoa phú quý dĩ thiên định|Chính hốt thùy thân bái tử thần",
    71: "Thử mệnh sinh thành đại bất đồng|Công hầu khanh tướng tại kỳ trung|Nhất sinh tự hữu tiêu dao phúc|Phú quý vinh hoa cực phẩm long",
}


def poem_for_weight(total: int) -> list[str]:
    poem = POEMS.get(total)
    if poem is None:
        return []
    return [line + punctuation for line, punctuation in zip(poem.split("|"), ",.,.")]
