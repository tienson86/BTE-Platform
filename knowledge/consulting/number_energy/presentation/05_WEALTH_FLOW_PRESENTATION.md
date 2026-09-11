# 05_WEALTH_FLOW_PRESENTATION.md

# BTE NUMBER ENERGY
## WEALTH FLOW PRESENTATION STANDARD
### Chuẩn hiển thị Dòng Tài Vận — Số điện thoại

**Status:** CANONICAL PRESENTATION STANDARD
**Version:** 1.0
**Module:** Number Energy Consulting
**Method:** Bát Cực Linh Số / Năng lượng số
**Purpose Context:** `phone_number`
**Scope:** Customer Wealth Presentation

**Parent:**
- `00_NUMBER_ENERGY_PRESENTATION_MASTER.md`
- `01_INFORMATION_ARCHITECTURE.md`
- `03_PHONE_RESULT_LAYOUT.md`
- `04_PAIR_TRIPLE_VISUALIZATION.md`

**Knowledge dependencies:**
- `number_energy/knowledge/03_PAIR_STRENGTH_MATRIX.md`
- `number_energy/knowledge/06_POSITION_AND_TAIL_RULES.md`
- `number_energy/knowledge/10_CUSTOMER_NARRATIVE_CATALOG.md`
- `number_energy/knowledge/12_TRIPLE_COMBINATION_CATALOG.md`
- `number_energy/knowledge/13_PHONE_WEALTH_FLOW_RULES.md`
- `number_energy/knowledge/14_PHONE_SCORE_MODEL.md`
- `number_energy/knowledge/15_RUNTIME_BINDING_CONTRACT.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa cách hiển thị
phần Dòng Tài Vận của số điện thoại.

Đây là một Signature Feature
của Number Energy Phone Result.

Customer must be able to answer:

    1. CÓ TÀI KHÔNG?
    2. TÀI MẠNH HAY YẾU?
    3. TÀI TỪ ĐÂU?
    4. TÀI ĐƯỢC TẠO BẰNG CÁCH NÀO?
    5. TÀI ĐI VỀ ĐÂU?
    6. DÒNG TÀI ỔN ĐỊNH HAY BIẾN ĐỘNG?
    7. PHẦN CUỐI DÃY QUY VỀ ĐÂU?
    8. HẬU VẬN CỦA DÃY SỐ THẾ NÀO?

Customer should understand
the primary wealth story
within approximately 10–20 seconds.

---

# 2. MASTER CUSTOMER MODEL

Canonical customer flow:

    CÓ TÀI?
        ↓
    NGUỒN TÀI
        ↓
    DÒNG TÀI
        ↓
    HẬU VẬN

Internal truth may be more complex.

Customer presentation must simplify
without changing meaning.

---

# 3. WEALTH IS A FLOW, NOT A BADGE

Forbidden presentation:

    TÀI VẬN
    ★★★★★
    Rất giàu

Forbidden:

    Có Thiên Y = số phát tài

Canonical presentation:

    THIÊN Y
        ↓
    SOURCE
        ↓
    DESTINATION
        ↓
    TERMINAL CONTEXT

Wealth is presented
as a structured flow.

---

# 4. SOURCE OF TRUTH

All wealth semantics MUST come from:

    13_PHONE_WEALTH_FLOW_RULES.md

Triple evidence MUST come from:

    12_TRIPLE_COMBINATION_CATALOG.md

Score MUST come from:

    14_PHONE_SCORE_MODEL.md

Presentation MUST NOT create
its own wealth interpretation.

---

# 5. SECTION PLACEMENT

Canonical section:

    P-S03 — WEALTH FLOW

Position:

    AFTER
    Number Energy Map
    + Quick Structure

    BEFORE
    long Triple Interpretation
    + generic Domain Insights

Reason:

Wealth is one of the first
questions phone-number customers care about.

---

# 6. SECTION HEADER

Canonical title:

    DÒNG TÀI VẬN

Canonical subtitle:

    Có Tài không · Tài từ đâu · Tài đi đâu · Hậu vận

Optional supporting copy:

    Thiên Y là trường khí trọng tâm
    để hệ thống đọc dòng Tài trong số điện thoại.

Keep supporting copy short.

Do not explain the whole method here.

---

# 7. FOUR-STAGE HERO

Canonical stages:

    WF-01  TÀI VẬN
    WF-02  NGUỒN TÀI
    WF-03  TÀI ĐI ĐÂU
    WF-04  HẬU VẬN

These four stages MUST remain
visually distinguishable.

---

# 8. DESKTOP LAYOUT

Recommended:

    ┌─────────────────┐
    │ 01 · TÀI VẬN   │
    │                 │
    │ Có Thiên Y     │
    │ 27 · 86        │
    └────────┬────────┘
             →
    ┌─────────────────┐
    │ 02 · NGUỒN TÀI │
    │                 │
    │ Quý nhân       │
    │ SK → TY        │
    └────────┬────────┘
             →
    ┌─────────────────┐
    │ 03 · TÀI ĐI ĐÂU│
    │                 │
    │ Sự nghiệp      │
    │ TY → DN        │
    └────────┬────────┘
             →
    ┌─────────────────┐
    │ 04 · HẬU VẬN   │
    │                 │
    │ Thiên Y        │
    │ DN → TY        │
    └─────────────────┘

Production Customer Mode uses
full Vietnamese energy labels,
not SK/TY/DN abbreviations.

---

# 9. MOBILE LAYOUT

Mobile must become:

    TÀI VẬN
       ↓
    NGUỒN TÀI
       ↓
    TÀI ĐI ĐÂU
       ↓
    HẬU VẬN

Each stage:

    full width

Do not shrink four cards
into four tiny columns.

---

# 10. FLOW DIRECTION

Directional connector:

    →

desktop.

Directional connector:

    ↓

mobile.

Purpose:

Show:

    WEALTH STORY HAS ORDER

Connector does NOT mean
deterministic causal prediction.

---

# 11. WF-01 — TÀI VẬN

Purpose:

Answer:

    "Dãy này có tín hiệu Tài không?"

Primary value options:

    Có Thiên Y
    Có nhiều điểm Thiên Y
    Thiên Y nổi bật
    Không có Thiên Y trực tiếp

Exact state should come
from Wealth Flow runtime.

---

# 12. WF-01 WITH THIEN Y

Example:

    TÀI VẬN

    Có Thiên Y

    27 · 86

Supporting:

    Dãy có hai điểm Thiên Y,
    vì vậy trục tài vận được hình thành rõ.

Do not say:

    Có 2 Thiên Y nên rất giàu.

---

# 13. WF-01 WITHOUT THIEN Y

Display:

    TÀI VẬN

    Không có Thiên Y trực tiếp

Supporting:

    Tín hiệu tài vận theo trục Thiên Y
    không phải điểm nổi bật của dãy.

Do not display:

    Không có Tài
    Số nghèo
    Không kiếm được tiền

---

# 14. WEALTH STRENGTH

If runtime provides canonical
Thiên Y strength:

Customer may see:

    Lực Tài

    ● ● ● ○

or:

    Mạnh

Do not display:

    T1
    rank 1
    78%

unless separately approved.

---

# 15. MULTIPLE THIEN Y

If multiple Thiên Y occur:

Show compact evidence:

    Thiên Y xuất hiện:
    27 · 86

Optional:

    2 vị trí

Do not show:

    2 tài tinh = 2 lần tài vận.

Every occurrence retains
its own context.

---

# 16. STRONGEST VS PRIMARY WEALTH NODE

Presentation must distinguish internally:

    strongest_wealth_node

from:

    primary_wealth_node

and:

    terminal_wealth_node

Customer usually sees:

    primary wealth story

not all three technical concepts.

Expert Mode may expose them.

---

# 17. WF-02 — NGUỒN TÀI

Purpose:

Answer:

    "Tài từ đâu đến?"

Canonical logic:

    SOURCE ENERGY
          ↓
       THIÊN Y

Source label comes from:

    13_PHONE_WEALTH_FLOW_RULES.md

---

# 18. SOURCE — SINH KHÍ → THIÊN Y

Customer headline:

    QUÝ NHÂN & CƠ HỘI

Supporting evidence:

    Sinh Khí → Thiên Y

Customer copy:

    Quý nhân, quan hệ hoặc cơ hội
    có khả năng dẫn tới tài vận.

Optional triple:

    827

---

# 19. SOURCE — DIÊN NIÊN → THIÊN Y

Headline:

    NĂNG LỰC NGHỀ NGHIỆP

Evidence:

    Diên Niên → Thiên Y

Copy:

    Tài vận chủ yếu đến từ năng lực làm việc,
    chuyên môn và sự nghiệp.

---

# 20. SOURCE — PHỤC VỊ → THIÊN Y

Headline:

    KIÊN TRÌ & TÍCH LŨY

Evidence:

    Phục Vị → Thiên Y

Copy:

    Tài vận thiên về tích lũy theo thời gian,
    cần sự kiên trì và ổn định.

---

# 21. SOURCE — LỤC SÁT → THIÊN Y

Headline:

    DỊCH VỤ & QUAN HỆ

Evidence:

    Lục Sát → Thiên Y

Copy:

    Nguồn tài phù hợp với dịch vụ,
    giao tiếp, khách hàng
    hoặc công việc cần sự tinh tế.

---

# 22. SOURCE — HỌA HẠI → THIÊN Y

Headline:

    KHẨU TÀI

Evidence:

    Họa Hại → Thiên Y

Copy:

    Khả năng nói, bán hàng,
    tư vấn hoặc thuyết phục
    có thể trở thành công cụ tạo thu nhập.

---

# 23. SOURCE — NGŨ QUỶ → THIÊN Y

Headline:

    TRÍ TUỆ & SÁNG TẠO

Evidence:

    Ngũ Quỷ → Thiên Y

Copy:

    Tài vận gắn với trí tuệ,
    ý tưởng, phân tích, sáng tạo
    hoặc công việc dùng nhiều chất xám.

---

# 24. SOURCE — TUYỆT MỆNH → THIÊN Y

Headline:

    HÀNH ĐỘNG & ĐẦU TƯ

Evidence:

    Tuyệt Mệnh → Thiên Y

Copy:

    Tài vận gắn với hành động,
    nỗ lực, kinh doanh,
    đầu tư hoặc quản lý tài sản.

Do not turn this into
financial investment advice.

---

# 25. SOURCE — THIÊN Y → THIÊN Y

Headline:

    TÀI KHÍ TĂNG CƯỜNG

Evidence:

    Thiên Y → Thiên Y

Copy:

    Thiên Y được tiếp nối,
    làm tín hiệu tài vận
    trở nên nổi bật hơn.

---

# 26. MULTIPLE WEALTH SOURCES

If multiple Thiên Y nodes
have different sources:

Do not show several equal headlines
inside WF-02.

Choose:

    PRIMARY SOURCE

Then below:

    Nguồn Tài bổ sung

Example:

    Nguồn chính:
    Quý nhân & cơ hội

    Nguồn bổ sung:
    Năng lực nghề nghiệp

Selection must come from runtime,
not frontend judgment.

---

# 27. WF-03 — TÀI ĐI ĐÂU

Purpose:

Answer:

    "Sau khi hình thành,
    dòng Tài có xu hướng đi về đâu?"

Canonical:

    THIÊN Y
        ↓
    TARGET ENERGY

This is not the same
as Source of Wealth.

---

# 28. DESTINATION — THIÊN Y → SINH KHÍ

Headline:

    QUAN HỆ & BẰNG HỮU

Copy:

    Nguồn lực có xu hướng được sử dụng
    cho quan hệ, bạn bè
    hoặc mở rộng nhân duyên.

Caution:

    Có thể chi nhiều cho các mối quan hệ.

---

# 29. DESTINATION — THIÊN Y → THIÊN Y

Headline:

    TÀI KHÍ TIẾP NỐI

Copy:

    Trường Thiên Y tiếp tục được duy trì,
    làm chủ đề tài vận nổi bật hơn.

---

# 30. DESTINATION — THIÊN Y → DIÊN NIÊN

Headline:

    SỰ NGHIỆP & LẬP NGHIỆP

Copy:

    Nguồn lực có xu hướng được đưa vào
    công việc, kinh doanh
    hoặc phát triển sự nghiệp.

---

# 31. DESTINATION — THIÊN Y → PHỤC VỊ

Headline:

    TÀI KHÍ KÉO DÀI

Copy:

    Thiên Y được Phục Vị kéo dài,
    vì vậy ảnh hưởng của tài khí
    tiếp tục sang đoạn sau của dãy.

Critical:

Do not rewrite as:

    Giữ được tiền.
    Tích tiền rất tốt.

unless another canonical rule
explicitly supports that conclusion.

---

# 32. DESTINATION — THIÊN Y → LỤC SÁT

Headline:

    QUAN HỆ & TIÊU DÙNG

Copy:

    Dòng tài dễ chuyển sang
    gia đình, quan hệ,
    dịch vụ hoặc nhu cầu đời sống.

Do not use gender-specific claims
unless product context supports them.

---

# 33. DESTINATION — THIÊN Y → HỌA HẠI

Headline:

    XÃ GIAO & CHI TIÊU

Copy:

    Dòng tài có xu hướng chuyển sang
    giao tiếp, xã giao
    hoặc các khoản chi phát sinh.

Do not surface medical claims
from historical source material.

---

# 34. DESTINATION — THIÊN Y → NGŨ QUỶ

Headline:

    DÒNG TIỀN BIẾN ĐỘNG

Copy:

    Tài khí có,
    nhưng dòng tiền dễ vào ra nhanh
    và khó duy trì trạng thái ổn định.

Caution presentation:

    Biến động dòng tiền

Not:

    Phá sản
    Mất tiền chắc chắn

---

# 35. DESTINATION — THIÊN Y → TUYỆT MỆNH

Headline:

    ĐẦU TƯ & HÀNH ĐỘNG

Copy:

    Nguồn tài có xu hướng được đưa vào
    đầu tư, hành động
    hoặc những quyết định tài chính mạnh.

Caution:

    Cần tránh quyết định quá nóng vội.

No financial recommendation.

---

# 36. SOURCE AND DESTINATION VISUAL DIFFERENCE

To prevent confusion:

WF-02 label:

    TÀI TỪ ĐÂU?

WF-03 label:

    TÀI ĐI ĐÂU?

Do not label both:

    TÀI VẬN

Evidence direction must remain visible.

Example:

    Họa Hại → Thiên Y
    = nguồn Tài

versus:

    Thiên Y → Họa Hại
    = dòng Tài ra

---

# 37. WF-04 — HẬU VẬN

Purpose:

Answer:

    "Phần cuối dãy
    đang đưa năng lượng về đâu?"

"Hậu vận" means:

    later section / terminal structure
    of the phone-number sequence

Not:

    end-of-life destiny

---

# 38. HẬU VẬN DATA

WF-04 consumes:

    terminal_pair
    terminal_energy
    terminal_triple
    terminal_interaction
    terminal_modifier
    terminal_strength

Customer display should prioritize:

    terminal_energy
    +
    terminal_triple meaning

---

# 39. HẬU VẬN — GOLDEN CASE

Golden:

    786

Pairs:

    78 Diên Niên
    86 Thiên Y

Interaction:

    Diên Niên → Thiên Y

Display:

    HẬU VẬN

    THIÊN Y

    Năng lực nghề nghiệp tạo Tài

Supporting:

    Phần cuối dãy quy về Thiên Y.
    Diên Niên đứng trước cho thấy
    năng lực và công việc tiếp tục
    là nguồn dẫn tới tài vận.

---

# 40. HẬU VẬN WITH CHALLENGING TERMINAL

If terminal energy
is challenging:

Do not display:

    HẬU VẬN XẤU

Preferred:

    HẬU VẬN
    Ngũ Quỷ

    Phần cuối có tính biến động

Then explain canonical context.

If control exists:

show it.

---

# 41. HẬU VẬN WITH ZERO

If terminal modifier
creates hidden/reduced state:

Display:

    Năng lượng kết
    Thiên Y · trạng thái ẩn

Supporting:

    Tiềm năng vẫn tồn tại
    nhưng khả năng biểu hiện
    không thật sự rõ.

Do not display:

    hậu vận mất Tài

unless canonical knowledge says so.

---

# 42. HẬU VẬN WITH FIVE

If terminal energy is amplified:

Display:

    Năng lượng kết
    {Energy}

    Trường khí được tăng cường

Meaning depends on
which Energy is amplified.

---

# 43. WEALTH STORY SYNTHESIS

After the four stages,
show one synthesis block.

Title:

    CÂU CHUYỆN TÀI VẬN

Golden example:

    Quý nhân & cơ hội
            ↓
          Tài
            ↓
    Sự nghiệp & lập nghiệp
            ↓
    Năng lực nghề nghiệp tạo Tài

Narrative:

    Dòng tài vận của dãy đi theo hướng:
    quý nhân và cơ hội mở đường,
    nguồn lực được đưa vào sự nghiệp,
    và phần cuối lại quy về khả năng
    tạo tài từ chính năng lực nghề