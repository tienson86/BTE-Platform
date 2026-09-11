# 14_PHONE_SCORE_MODEL.md

# BTE NUMBER ENERGY
## PHONE SCORE MODEL
### Mô hình chấm điểm tổng hợp số điện thoại

Status: CANONICAL KNOWLEDGE
Version: 1.0
Scope: Number Energy / Phone Number
Purpose Context: phone_number

Depends on:
- 02_EIGHT_ENERGY_CATALOG.md
- 03_PAIR_STRENGTH_MATRIX.md
- 04_DIRECTED_INTERACTION_MATRIX.md
- 05_ZERO_FIVE_MODIFIERS.md
- 06_POSITION_AND_TAIL_RULES.md
- 07_CONTROL_REMEDY_RULES.md
- 08_CHAIN_INTERPRETATION_RULES.md
- 09_DOMAIN_INTERPRETATION.md
- 12_TRIPLE_COMBINATION_CATALOG.md
- 13_PHONE_WEALTH_FLOW_RULES.md

---

# 1. PURPOSE

Tài liệu này định nghĩa mô hình chấm điểm tổng hợp cho một
số điện thoại sau khi toàn bộ knowledge engine đã hoàn thành
việc nhận diện và luận giải.

Score dùng để trả lời nhanh:

    Dãy số này tổng thể đang ở mức nào?

Score KHÔNG dùng để thay thế luận giải.

Canonical order:

    Normalize
        ↓
    Pair Detection
        ↓
    Pair Strength
        ↓
    Directed Triple Interpretation
        ↓
    0 / 5 Modifier
        ↓
    Chain Interpretation
        ↓
    Wealth Flow
        ↓
    Position & Tail
        ↓
    Domain Interpretation
        ↓
    SCORE
        ↓
    Customer Presentation

Nguyên tắc bắt buộc:

    INTERPRET FIRST.
    SCORE SECOND.

---

# 2. SCORE IS NOT TRUTH

Score là Presentation Summary.

Không được dùng Score để tạo knowledge.

Sai:

    Score cao
    → suy ra người này chắc chắn giàu.

Sai:

    Hung pair nhiều
    → tự động kết luận số xấu.

Sai:

    Thiên Y nhiều
    → tự động cộng điểm cao.

Đúng:

    Knowledge xác định ý nghĩa
        ↓
    Context xác định tác dụng
        ↓
    Score tóm tắt kết quả đó.

---

# 3. SCORE RANGE

Canonical customer score:

    0 – 100

Display:

    XX / 100

Score phải được clamp:

    min = 0
    max = 100

Không được xuất:

    -4 / 100
    107 / 100

---

# 4. SCORE DIMENSIONS

Phone Score gồm 5 trục:

    A. Energy Structure      25
    B. Wealth Flow           25
    C. Career & Support      20
    D. Stability & Risk      15
    E. Tail / Later Outcome  15

Total:

    25 + 25 + 20 + 15 + 15 = 100

Canonical formula:

    final_score =
        energy_structure_score
      + wealth_flow_score
      + career_support_score
      + stability_risk_score
      + tail_score

---

# 5. WHY SCORE BY DOMAIN

Không dùng mô hình:

    +10 Sinh Khí
    -10 Ngũ Quỷ
    +10 Thiên Y
    -10 Tuyệt Mệnh

vì phương pháp này làm mất:

- strength;
- direction;
- position;
- tam số thành tượng;
- tác dụng của Phục Vị;
- tác dụng 0/5;
- chế ước;
- nguồn tài;
- dòng tài;
- năng lượng kết.

Ví dụ:

    NGŨ QUỶ → THIÊN Y

không thể bị tính đơn giản:

    Ngũ Quỷ = âm điểm
    Thiên Y = dương điểm

vì canonical truth là:

    trí tuệ / ý tưởng / tài hoa → tạo tài.

Do đó score phải nhận kết quả từ Interpretation Engine.

---

# 6. DIMENSION A
# ENERGY STRUCTURE — 25 POINTS

Mục đích:

Đánh giá cấu trúc trường khí toàn dãy.

Không chỉ đếm cát/hung.

Inputs:

    pair_occurrences
    pair_strength
    positive_interactions
    negative_interactions
    modifiers
    repeated_energy
    chain_balance

Internal components:

    A1. Pair Quality          0–10
    A2. Interaction Quality   0–10
    A3. Structural Balance    0–5

Total:

    0–25

---

# 7. A1 — PAIR QUALITY

Pair Quality đánh giá nền trường khí.

Bốn cát tinh:

    Sinh Khí
    Thiên Y
    Diên Niên
    Phục Vị

Bốn hung tinh:

    Họa Hại
    Ngũ Quỷ
    Lục Sát
    Tuyệt Mệnh

NHƯNG:

Không được:

    good_count - bad_count

một cách cơ học.

Pair phải được weighted theo:

    strength
    position
    modifier state

Recommended normalized internal value:

    pair_quality_raw ∈ [-1, +1]

Mapping:

    -1.00 → 0
     0.00 → 5
    +1.00 → 10

Không hiển thị raw value cho khách hàng.

---

# 8. A2 — INTERACTION QUALITY

Nguồn:

    12_TRIPLE_COMBINATION_CATALOG.md

Mỗi triple interaction đã match phải mang:

    effect_type

Ví dụ:

    WEALTH_GENERATION
    WEALTH_FROM_CAREER
    COMMUNICATION_POSITIVE
    CAREER_FROM_SUPPORT
    AMPLIFY_POSITIVE
    EXTEND_SOURCE
    VOLATILE_FLOW
    NEGATIVE_EXTENSION
    ...

Score Engine không tự đọc tên energy để quyết định.

Nó chỉ đọc classification đã được knowledge layer xuất ra.

Pseudo:

    interaction_score =
        aggregate(
            canonical_effect_weight,
            strength_context,
            position_context
        )

Normalize:

    0–10

---

# 9. A3 — STRUCTURAL BALANCE

Maximum:

    5

Mục tiêu:

Đánh giá dãy số có:

- quá lệch một loại trường khí;
- quá nhiều hung tinh liên tiếp;
- quá nhiều Phục Vị kéo dài;
- nhiều 0 làm ẩn/rút năng lượng;
- chuỗi có khả năng vận động và chuyển hóa;
- cát/hung có quan hệ hợp lý.

Canonical principle:

    Số điện thoại không nên toàn cát,
    càng không nên toàn hung.

Theo knowledge:

    "Cát tinh làm chủ, hung tinh là trái."

và:

    "Cát bên trong có hung,
    mới có thể thành dụng cụ."

Do đó:

    ALL_GOOD != PERFECT_SCORE

và:

    ALL_BAD != BALANCED_STRUCTURE

Score không được khuyến khích việc nhồi càng nhiều cát tinh
càng tốt.

---

# 10. DIMENSION B
# WEALTH FLOW — 25 POINTS

Đây là dimension trọng yếu của phone_number.

Nguồn canonical:

    13_PHONE_WEALTH_FLOW_RULES.md

Components:

    B1. Wealth Presence       0–7
    B2. Wealth Source         0–6
    B3. Wealth Flow           0–6
    B4. Wealth Continuity     0–6

Total:

    25

---

# 11. B1 — WEALTH PRESENCE

Dựa trên:

    Thiên Y occurrence
    strength
    position
    modifier context

Không chỉ đếm số lượng.

Conceptual scale:

    0
    → không có Thiên Y trực tiếp

    low
    → Thiên Y yếu / context bất lợi

    medium
    → Thiên Y hiện diện rõ

    high
    → Thiên Y mạnh, context tốt

Maximum:

    7

Không được dùng rule:

    mỗi Thiên Y + 2 điểm

vì Thiên Y lặp nhiều không mặc định càng tốt.

---

# 12. B2 — WEALTH SOURCE

Dựa vào:

    SOURCE → THIEN_Y

Canonical sources:

    Sinh Khí → Thiên Y
        quý nhân / cơ hội tạo tài

    Diên Niên → Thiên Y
        năng lực nghề nghiệp tạo tài

    Phục Vị → Thiên Y
        kiên trì / tích lũy tạo tài

    Lục Sát → Thiên Y
        dịch vụ / quan hệ tạo tài

    Họa Hại → Thiên Y
        khẩu tài tạo tài

    Ngũ Quỷ → Thiên Y
        trí tuệ / sáng tạo tạo tài

    Tuyệt Mệnh → Thiên Y
        hành động / đầu tư tạo tài

    Thiên Y → Thiên Y
        tài khí được tăng cường

Score không xếp hạng:

    nghề này tốt hơn nghề kia.

Ví dụ:

    Họa Hại → Thiên Y

không được điểm thấp chỉ vì Họa Hại là hung tinh.

Nếu interaction canonical tạo tài hợp lệ:

    source_quality = POSITIVE

Maximum:

    6

---

# 13. B3 — WEALTH FLOW

Đọc:

    THIEN_Y → TARGET

Mục tiêu:

Tài sau khi hình thành vận động thế nào?

Các trạng thái canonical:

    PRODUCTIVE
    REINVESTED
    EXTENDED
    RELATIONSHIP_SPENDING
    SOCIAL_SPENDING
    VOLATILE
    INVESTMENT_OUTFLOW
    UNKNOWN

Ví dụ:

    Thiên Y → Diên Niên
        tài đi vào sự nghiệp / lập nghiệp.

    Thiên Y → Phục Vị
        Thiên Y được kéo dài.

    Thiên Y → Ngũ Quỷ
        dòng tài biến động.

    Thiên Y → Tuyệt Mệnh
        tài đi vào đầu tư / hành động.

Không được tự coi:

    "tiền đi ra" = hoàn toàn xấu.

Đầu tư và sử dụng nguồn lực khác với phá tài.

Maximum:

    6

---

# 14. B4 — WEALTH CONTINUITY

Đánh giá khả năng dòng Tài tiếp tục tới phần sau của dãy.

Inputs:

    multiple WealthNodes
    terminal WealthNode
    Phục Vị extension
    0 modifier
    5 modifier
    tail energy
    adverse chain interruption

Maximum:

    6

Ví dụ:

    Thiên Y → Phục Vị

có thể hỗ trợ continuity vì Thiên Y được kéo dài.

Nhưng:

    Thiên Y → Ngũ Quỷ

phải đánh dấu:

    wealth_volatility = true

Không tự động cho 0 điểm.

---

# 15. DIMENSION C
# CAREER & SUPPORT — 20 POINTS

Components:

    C1. Career Energy     0–8
    C2. Noble Support     0–6
    C3. Productive Skill  0–6

Total:

    20

---

# 16. C1 — CAREER ENERGY

Trọng tâm:

    DIEN_NIEN

Nhưng phải xét interaction.

Ví dụ:

    Sinh Khí → Diên Niên
        quý nhân mang đến công việc.

    Thiên Y → Diên Niên
        xu hướng lập nghiệp.

    Họa Hại → Diên Niên
        khẩu tài thành nghề.

    Ngũ Quỷ → Diên Niên
        trí óc thành nghề.

    Lục Sát → Diên Niên
        dịch vụ / giao tế thành nghề.

    Tuyệt Mệnh → Diên Niên
        hành động / kinh doanh / đầu tư thành nghề.

Maximum:

    8

---

# 17. C2 — NOBLE SUPPORT

Trọng tâm:

    SINH_KHI

Đánh giá:

    presence
    strength
    interaction
    position
    modifier

Sinh Khí không chỉ là "có/không".

Ví dụ:

    Họa Hại → Sinh Khí
        khẩu tài được phát huy tích cực.

    Ngũ Quỷ → Sinh Khí
        ý tưởng chuyển thành phương án hữu ích.

    Phục Vị → Sinh Khí
        Sinh Khí được tăng cường.

Maximum:

    6

---

# 18. C3 — PRODUCTIVE SKILL

Đánh giá dãy có biến năng lượng thành năng lực hữu dụng hay không.

Ví dụ:

    Họa Hại → Diên Niên
        communication → career

    Ngũ Quỷ → Diên Niên
        intellect → career

    Lục Sát → Diên Niên
        social/service → career

    Tuyệt Mệnh → Diên Niên
        action → career

Maximum:

    6

---

# 19. DIMENSION D
# STABILITY & RISK — 15 POINTS

Khác với các dimension khác:

    15 = ổn định tốt
    0  = rủi ro cấu trúc cao

Components:

    D1. Negative Chain Risk    0–6
    D2. Modifier Risk          0–4
    D3. Flow Stability         0–5

Total:

    15

---

# 20. D1 — NEGATIVE CHAIN RISK

Đánh giá:

    consecutive_negative_energy
    amplified_negative_energy
    dangerous tail structure
    unresolved negative chain

Không được chỉ đếm hung tinh.

Ví dụ:

    Họa Hại → Sinh Khí

đã có canonical positive interaction.

Không được vẫn phạt toàn bộ Họa Hại như một hung pair độc lập
mà bỏ qua interaction.

Nguyên tắc:

    interaction truth > isolated pair label

khi đang đánh giá chính interaction đó.

Maximum:

    6

---

# 21. D2 — MODIFIER RISK

Nguồn:

    05_ZERO_FIVE_MODIFIERS.md

Canonical:

    0 = âm / ẩn / rút bớt / che giấu năng lượng
    5 = dương / hiển / tăng cường / kéo dài

Nhưng:

    0 != always bad
    5 != always good

Tác dụng phụ thuộc trường khí nó modifier.

Ví dụ:

    0 + positive energy
        có thể làm năng lượng khó biểu hiện.

    5 + negative energy
        có thể làm hung tính mạnh và kéo dài.

Score Engine phải nhận:

    modifier_effect

từ Modifier Engine.

Không tự quyết định.

Maximum:

    4

---

# 22. D3 — FLOW STABILITY

Đánh giá:

- dòng năng lượng có đứt đoạn;
- tài khí có biến động;
- hung khí có bị kéo dài;
- cát khí có được tiếp nối;
- cấu trúc có quá nhiều chuyển động mạnh.

Maximum:

    5

Ví dụ:

    Thiên Y → Ngũ Quỷ

không phủ nhận có tài.

Nhưng:

    financial_flow_stability

sẽ thấp hơn vì dòng tiền biến động.

---

# 23. DIMENSION E
# TAIL / LATER OUTCOME — 15 POINTS

Phần cuối dãy là vùng trọng yếu.

Nguồn:

    06_POSITION_AND_TAIL_RULES.md

Canonical principle:

    Số đuôi tất cát,
    mới có thể thành quả.

Không được hiểu thành:

    chỉ cần cặp cuối cát là toàn bộ số tốt.

Tail chỉ là một dimension.

Components:

    E1. Terminal Energy       0–8
    E2. Tail Continuity       0–4
    E3. Tail Modifier State   0–3

Total:

    15

---

# 24. E1 — TERMINAL ENERGY

Occurrence cuối cùng:

    terminal_energy

Customer label:

    Năng lượng kết

Ví dụ:

    ...86
       ↓
    THIEN_Y

Có thể diễn đạt:

    "Dãy số kết tại Thiên Y."

Không viết:

    "Hậu vận chắc chắn giàu."

Tail score phải xét:

    energy
    strength
    preceding interaction

Maximum:

    8

---

# 25. E2 — TAIL CONTINUITY

Đọc triple cuối.

Ví dụ:

    786

gồm:

    78 = Diên Niên
    86 = Thiên Y

Do đó:

    Diên Niên → Thiên Y

Canonical:

    năng lực nghề nghiệp → tạo tài.

Nếu triple cuối có canonical positive directed interaction:

    tail_continuity = SUPPORTIVE

Nếu negative:

    tail_continuity = CAUTION

Maximum:

    4

---

# 26. E3 — TAIL MODIFIER

Đặc biệt kiểm tra:

    ending 0
    ending 5
    0/5 gần terminal energy

Theo canonical knowledge:

Không khuyến nghị số điện thoại kết:

    0
    05

Nhưng UI phải diễn đạt theo ngôn ngữ tư vấn,
không dùng kết luận định mệnh tuyệt đối.

Maximum:

    3

---

# 27. SCORE AGGREGATION

Canonical:

    final_score =
        A + B + C + D + E

Where:

    A ∈ [0,25]
    B ∈ [0,25]
    C ∈ [0,20]
    D ∈ [0,15]
    E ∈ [0,15]

Then:

    final_score = clamp(final_score, 0, 100)

Round:

    display_score = round(final_score)

Không cần decimal trên UI customer.

---

# 28. SCORE BANDS

Canonical presentation bands:

    85–100
    RẤT TỐT

    70–84
    TỐT

    55–69
    KHÁ

    40–54
    TRUNG BÌNH

    25–39
    CẦN CÂN NHẮC

    0–24
    NHIỀU ĐIỂM CẦN LƯU Ý

Internal keys:

    EXCELLENT
    GOOD
    FAIR
    AVERAGE
    CONSIDER
    CAUTION

Không dùng:

    Đại Cát
    Đại Hung
    Số tử
    Số phá sản
    Số tuyệt đối tốt
    Số tuyệt đối xấu

trong score summary.

---

# 29. CUSTOMER SCORE CARD

Customer UI nên hiển thị:

    ĐÁNH GIÁ TỔNG THỂ

              78