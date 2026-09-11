# 13_PHONE_WEALTH_FLOW_RULES.md

# BTE NUMBER ENERGY
## PHONE WEALTH FLOW RULES
### Quy tắc luận Tài vận – Nguồn Tài – Dòng Tài – Hậu vận của số điện thoại

Status: CANONICAL KNOWLEDGE
Version: 1.0
Scope: Number Energy / Phone Number
Depends on:
- 01_BAGUA_DIGIT_MAPPING.md
- 02_EIGHT_ENERGY_CATALOG.md
- 03_PAIR_STRENGTH_MATRIX.md
- 04_DIRECTED_INTERACTION_MATRIX.md
- 05_ZERO_FIVE_MODIFIERS.md
- 06_POSITION_AND_TAIL_RULES.md
- 08_CHAIN_INTERPRETATION_RULES.md
- 12_TRIPLE_COMBINATION_CATALOG.md

---

# 1. PURPOSE

Tài liệu này định nghĩa quy tắc chuẩn để hệ thống BTE đọc dòng
Tài vận trong một số điện thoại.

Mục tiêu không chỉ trả lời:

    "Dãy số có Thiên Y hay không?"

mà phải lần lượt trả lời:

    1. Có Tài hay không?
    2. Tài khí mạnh hay yếu?
    3. Tài đến từ đâu?
    4. Tài được tạo ra bằng cách nào?
    5. Sau khi có Tài, Tài đi về đâu?
    6. Tài có xu hướng giữ, dùng, đầu tư hay biến động?
    7. Năng lượng cuối dãy nói gì về hậu vận?
    8. Toàn chuỗi có hỗ trợ hay làm suy giảm dòng Tài?

Đây là logic chuyên biệt cho:

    purpose_context = phone_number

Không áp dụng máy móc cho biển số xe hoặc các loại mã số khác.

---

# 2. CORE PRINCIPLE

Trong hệ thống Number Energy:

    THIÊN Y = TRƯỜNG KHÍ TÀI PHÚ TRỌNG TÂM

Do đó khi luận Tài vận của số điện thoại, hệ thống phải tìm
các occurrence Thiên Y trước.

Nhưng:

    Có Thiên Y ≠ tự động kết luận giàu.
    Không có Thiên Y ≠ tự động kết luận nghèo.

Thiên Y là tín hiệu trung tâm để đọc dòng Tài.

Kết luận cuối cùng phải xét:

    Thiên Y
    + strength
    + position
    + source energy
    + target energy
    + modifiers 0/5
    + repeated patterns
    + tail energy
    + whole-chain context

---

# 3. WEALTH READING MODEL

Canonical flow:

    PHONE NUMBER
        ↓
    NORMALIZE
        ↓
    PAIR SEGMENTATION
        ↓
    ENERGY DETECTION
        ↓
    FIND THIEN_Y
        ↓
    MEASURE THIEN_Y STRENGTH
        ↓
    READ LEFT CONTEXT
        ↓
    SOURCE OF WEALTH
        ↓
    READ RIGHT CONTEXT
        ↓
    DESTINATION OF WEALTH
        ↓
    READ TAIL
        ↓
    LATER OUTCOME / HẬU VẬN
        ↓
    WHOLE-CHAIN SYNTHESIS

Customer-facing model:

    TÀI VẬN
        ↓
    NGUỒN TÀI
        ↓
    DÒNG TÀI
        ↓
    HẬU VẬN

---

# 4. PHONE PREFIX RULE

Đối với số điện thoại Việt Nam:

Ví dụ:

    0328278786

Số `0` đầu dãy là tiền tố số điện thoại.

Canonical rule:

    leading_phone_zero = PREFIX

Không đưa số 0 tiền tố vào phép ghép Du Niên.

Do đó:

    Input:
    0328278786

    Analysis body:
    328278786

Không được tạo:

    03

thành một cặp Du Niên.

Số 0 xuất hiện ở giữa hoặc cuối thân số phải xử lý theo:

    05_ZERO_FIVE_MODIFIERS.md

---

# 5. STEP 1 — DETECT WEALTH ENERGY

Hệ thống phải tìm tất cả occurrence thuộc:

    THIEN_Y

Canonical Thiên Y pairs:

    13
    31
    68
    86
    49
    94
    27
    72

Mỗi occurrence phải giữ:

    pair
    start_index
    end_index
    strength_level
    previous_energy
    next_energy
    modifier_context
    tail_distance

Không được chỉ đếm tổng số Thiên Y.

---

# 6. STEP 2 — THIEN Y STRENGTH

Cường độ Thiên Y giảm dần:

    Level 1:
    13 / 31

    Level 2:
    68 / 86

    Level 3:
    49 / 94

    Level 4:
    27 / 72

Canonical order:

    13/31 > 68/86 > 49/94 > 27/72

Customer UI không bắt buộc hiện:

    rank = 1
    rank = 2
    ...

Có thể chuyển thành:

    Rất mạnh
    Mạnh
    Vừa
    Nhẹ

hoặc thanh lực trực quan.

Không dùng percentage nếu knowledge không định nghĩa percentage.

---

# 7. STEP 3 — IS THERE WEALTH?

## 7.1 Có Thiên Y

Nếu có ít nhất một Thiên Y hợp lệ:

    wealth_signal = PRESENT

Nhưng phải tiếp tục xét context.

Không được dừng ở kết luận:

    "Dãy số có tài vận tốt."

---

## 7.2 Nhiều Thiên Y

Nhiều Thiên Y làm tín hiệu tài vận nổi bật hơn.

Nhưng:

    MORE_THIEN_Y != ALWAYS_BETTER

Phải xét:

- strength;
- vị trí;
- trường đứng trước;
- trường đứng sau;
- 0/5;
- các hung tinh liên tiếp;
- năng lượng kết.

Không được cộng Thiên Y cơ học thành điểm tài vận.

---

## 7.3 Không có Thiên Y

Nếu không có Thiên Y:

    wealth_signal = NO_DIRECT_THIEN_Y

Customer wording:

    "Dãy số không xuất hiện trường Thiên Y trực tiếp,
    vì vậy tín hiệu tài vận theo trục Thiên Y không nổi bật."

Không được viết:

    "Không có tài."
    "Không kiếm được tiền."
    "Số nghèo."
    "Không thể phát tài."

Sau đó vẫn phải xét:

    Sinh Khí
    Diên Niên
    chain context
    tail

để mô tả khả năng hỗ trợ công việc, cơ hội và nguồn lực.

---

# 8. STEP 4 — SOURCE OF WEALTH

Để xác định:

    "Tài từ đâu đến?"

đọc trường khí NGAY TRƯỚC Thiên Y.

Pattern:

    SOURCE_ENERGY → THIEN_Y

Truth phải lấy từ:

    12_TRIPLE_COMBINATION_CATALOG.md

Không được tự diễn giải.

---

# 9. SOURCE OF WEALTH MATRIX

## 9.1 Sinh Khí → Thiên Y

Canonical meaning:

    Thông qua quý nhân mà mang đến tài phú.

wealth_source:

    QUY_NHAN

Customer label:

    Quý nhân & cơ hội

Customer wording:

    "Tài vận có xu hướng đến thông qua quý nhân,
    quan hệ hoặc những cơ hội thuận lợi."

---

## 9.2 Thiên Y → Thiên Y

Canonical meaning:

    Tụ tập tăng cường năng lượng tài phú,
    còn có hiện tượng hôn nhân.

wealth_source:

    REINFORCED_WEALTH

Customer label:

    Tài khí tăng cường

Customer wording:

    "Trường Thiên Y được tiếp nối,
    làm tín hiệu tài vận trở nên nổi bật hơn."

---

## 9.3 Diên Niên → Thiên Y

Canonical meaning:

    Dựa vào năng lực kiếm tiền.

wealth_source:

    CAREER_ABILITY

Customer label:

    Năng lực nghề nghiệp

Customer wording:

    "Tài vận chủ yếu đến từ năng lực làm việc,
    chuyên môn và sự nghiệp."

Special rule:

    Diên Niên lớn + Thiên Y nhỏ
    → làm nhiều, thu hoạch tương đối ít hơn.

    Diên Niên nhỏ + Thiên Y lớn
    → hiệu quả tạo tài thuận hơn.

Phải dùng strength matrix để xác định.

---

## 9.4 Phục Vị → Thiên Y

Canonical meaning:

    Thông qua kiên nhẫn, kiên trì, chờ đợi
    mà tạo ra tài phú lớn.

wealth_source:

    PATIENCE_ACCUMULATION

Customer label:

    Kiên trì & tích lũy

Customer wording:

    "Tài vận thiên về tích lũy theo thời gian,
    cần sự kiên trì và ổn định."

---

## 9.5 Lục Sát → Thiên Y

Canonical meaning:

    Thông qua ngành dịch vụ mà kiếm tiền.
    Cần công việc tỉ mỉ.

wealth_source:

    SERVICE

Customer label:

    Dịch vụ & quan hệ

Customer wording:

    "Nguồn tài phù hợp với dịch vụ, giao tiếp,
    chăm sóc khách hàng hoặc công việc cần sự tinh tế."

---

## 9.6 Họa Hại → Thiên Y

Canonical meaning:

    Thông qua khẩu tài mà kiếm tiền.
    Các loại công việc như bán hàng, diễn thuyết.

wealth_source:

    COMMUNICATION

Customer label:

    Khẩu tài

Customer wording:

    "Khả năng nói, bán hàng, tư vấn hoặc thuyết phục
    có thể trở thành công cụ tạo thu nhập."

---

## 9.7 Ngũ Quỷ → Thiên Y

Canonical meaning:

    Thông qua ý tưởng, tài hoa mà kiếm tiền.
    Công việc cần cường độ linh hoạt hoạt động não.

wealth_source:

    INTELLECT_CREATIVITY

Customer label:

    Trí tuệ & sáng tạo

Customer wording:

    "Tài vận gắn với trí tuệ, ý tưởng,
    khả năng phân tích, sáng tạo hoặc công việc dùng nhiều chất xám."

Possible domains:

    công nghệ
    IT
    thiết kế
    lập kế hoạch
    nghệ thuật
    chuyên môn trí óc

Không được khẳng định người dùng chắc chắn làm các nghề này.

---

## 9.8 Tuyệt Mệnh → Thiên Y

Canonical meaning:

    Thông qua cố gắng phấn đấu mà kiếm tiền.
    Hoặc làm đầu tư, quản lý tài sản.

wealth_source:

    ACTION_INVESTMENT

Customer label:

    Hành động & đầu tư

Customer wording:

    "Tài vận gắn với hành động, nỗ lực,
    kinh doanh, đầu tư hoặc quản lý tài sản."

Không được biến thành khuyến nghị đầu tư tài chính.

---

# 10. STEP 5 — WHERE DOES WEALTH GO?

Để trả lời:

    "Tài đi về đâu?"

đọc trường khí NGAY SAU Thiên Y.

Pattern:

    THIEN_Y → TARGET_ENERGY

Truth phải tham chiếu:

    12_TRIPLE_COMBINATION_CATALOG.md
    04_DIRECTED_INTERACTION_MATRIX.md

Đây là DÒNG RA của tài.

Không được lấy nghĩa SOURCE_OF_WEALTH để dùng ngược chiều.

---

# 11. WEALTH DESTINATION RULES

## 11.1 Thiên Y → Sinh Khí

Canonical basis:

    Thiên Y + Sinh Khí:
    hiếu bằng hữu, đối với bằng hữu hào phóng,
    nhân duyên tốt, tốn không ít tiền cho bằng hữu.

wealth_destination:

    RELATIONSHIP_NETWORK

Customer label:

    Quan hệ & bằng hữu

Customer wording:

    "Sau khi có tài, nguồn lực có xu hướng được sử dụng
    cho quan hệ, bạn bè hoặc việc mở rộng nhân duyên."

Positive side:

    quan hệ tốt
    hào phóng
    mở rộng kết nối

Caution:

    dễ chi nhiều cho bạn bè hoặc quan hệ.

---

## 11.2 Thiên Y → Thiên Y

wealth_destination:

    REINFORCED_WEALTH

Customer label:

    Tài khí tiếp nối

Customer wording:

    "Tài khí được tiếp tục tăng cường,
    làm chủ đề tài vận nổi bật trong dãy số."

---

## 11.3 Thiên Y → Diên Niên

Canonical basis:

    Thiên Y + Diên Niên:
    có ý tự mình làm chủ,
    giỏi về đầu tư lập nghiệp.

wealth_destination:

    CAREER_BUSINESS

Customer label:

    Sự nghiệp & lập nghiệp

Customer wording:

    "Nguồn lực tài chính có xu hướng được đưa vào
    công việc, kinh doanh, lập nghiệp hoặc phát triển sự nghiệp."

---

## 11.4 Thiên Y → Phục Vị

Canonical basis:

    Thiên Y + Phục Vị:
    từ trường Thiên Y được kéo dài.

wealth_destination:

    EXTENDED_WEALTH

Customer label:

    Tài khí kéo dài

Customer wording:

    "Thiên Y được Phục Vị kéo dài,
    vì vậy ảnh hưởng của tài khí có xu hướng tiếp tục
    sang đoạn sau của dãy số."

Không tự diễn thành:

    "giữ được tiền"

trừ khi chain context khác có rule xác nhận.

Đây là điểm bắt buộc.

---

## 11.5 Thiên Y → Lục Sát

Canonical basis:

    Thiên Y + Lục Sát:
    tiêu cho Lục Sát.

Theo knowledge:

    tiền dùng tại:
    - nữ nhân;
    - gia đình;
    - cửa hàng;
    - đồ trang điểm;
    - quần áo;
    - việc nhà;
    - các lĩnh vực mang tính dịch vụ / quan hệ.

wealth_destination:

    SERVICE_RELATIONSHIP_EXPENSE

Customer label:

    Quan hệ & tiêu dùng

Customer wording:

    "Tài khí phía trước dễ chuyển thành chi tiêu
    cho quan hệ, gia đình, dịch vụ hoặc nhu cầu đời sống."

Không được mặc định gán giới tính cho khách hàng.

---

## 11.6 Thiên Y → Họa Hại

Canonical basis:

    Thiên Y + Họa Hại:
    dùng cho Họa Hại.

Knowledge examples:

    chi tiêu lớn
    xã giao
    xa xỉ phẩm
    xem bệnh

wealth_destination:

    COMMUNICATION_SOCIAL_EXPENSE

Customer label:

    Xã giao & chi tiêu

Customer wording:

    "Dòng tài dễ chuyển sang các khoản chi cho giao tiếp,
    xã giao hoặc những nhu cầu phát sinh."

Không dùng nội dung sức khỏe như chẩn đoán.

---

## 11.7 Thiên Y → Ngũ Quỷ

Canonical basis:

    Thiên Y + Ngũ Quỷ:
    tiêu cho Ngũ Quỷ.

Knowledge:

    tiền vào ra không ổn định
    lên xuống lớn
    tài chính không an toàn
    lưu động lớn
    lưu không được

wealth_destination:

    VOLATILE_FLOW

Customer label:

    Dòng tiền biến động

Customer wording:

    "Tài khí có nhưng dòng tiền dễ biến động,
    vào ra nhanh và khó duy trì trạng thái ổn định."

Không được kết luận:

    phá sản
    mất sạch
    chắc chắn thất bại

nếu không có rule riêng xác nhận.

---

## 11.8 Thiên Y → Tuyệt Mệnh

Canonical basis:

    Thiên Y + Tuyệt Mệnh:
    dùng tài Tuyệt Mệnh.

Knowledge:

    xung động tiêu phí
    đầu tư
    tiêu hao
    phá tài

wealth_destination:

    INVESTMENT_ACTION_OUTFLOW

Customer label:

    Đầu tư & hành động

Customer wording:

    "Nguồn tài có xu hướng được đưa vào đầu tư,
    hành động hoặc những quyết định tài chính mạnh."

Caution:

    cần tránh quyết định tài chính quá nóng vội.

Không được đưa ra tư vấn đầu tư cụ thể.

---

# 12. SOURCE VS DESTINATION MUST NOT BE CONFUSED

Ví dụ:

    HỌA HẠI → THIÊN Y

nghĩa:

    khẩu tài tạo tài.

Nhưng:

    THIÊN Y → HỌA HẠI

nghĩa:

    tài đi vào xã giao / chi tiêu / nhu cầu Họa Hại.

Hai tổ hợp KHÔNG đồng nghĩa.

Tương tự:

    NGŨ QUỶ → THIÊN Y
    = trí tuệ / ý tưởng tạo tài.

    THIÊN Y → NGŨ QUỶ
    = tài khí đi vào dòng biến động.

Và:

    TUYỆT MỆNH → THIÊN Y
    = hành động / đầu tư tạo tài.

    THIÊN Y → TUYỆT MỆNH
    = tài được đưa vào đầu tư / hành động / tiêu hao.

Runtime phải giữ direction tuyệt đối.

---

# 13. STEP 6 — MULTIPLE THIEN Y

Nếu dãy có nhiều Thiên Y:

    TY_1
    TY_2
    TY_3
    ...

phải phân tích từng occurrence.

Không được chỉ chọn Thiên Y mạnh nhất rồi bỏ các occurrence khác.

Mỗi occurrence tạo một:

    Wealth Node

Structure:

    WealthNode {
        pair
        strength
        position
        source_energy
        source_meaning
        target_energy
        destination_meaning
        modifier_context
    }

Sau đó mới tổng hợp.

---

# 14. PRIMARY WEALTH NODE

Nếu có nhiều Wealth Node, xác định:

    primary_wealth_node

theo thứ tự:

    1. validity
    2. modifier state
    3. strength
    4. position relevance
    5. tail relevance

Không được chỉ dựa vào pair strength.

Ví dụ:

Một `13` mạnh ở đầu dãy và một `86` ở cuối dãy:

    13 có strength cao hơn

nhưng:

    86 có thể quan trọng hơn đối với hậu vận
    vì nằm ở năng lượng kết.

Do đó:

    strongest_wealth_node

và:

    terminal_wealth_node

là hai khái niệm khác nhau.