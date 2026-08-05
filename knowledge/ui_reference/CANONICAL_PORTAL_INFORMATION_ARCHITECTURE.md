# BTE Platform V1.0

# Canonical Portal Information Architecture

# Revision v1.1

---

## Document Information

| Item | Value |
|------|-------|
| Document | Canonical Portal Information Architecture |
| Version | **1.1 — PASS WITH CHANGES applied** |
| Status | **AWAITING PO APPROVAL FOR ARCHITECTURE FREEZE** |
| Previous | v1.0 Design Review Package → **PASS WITH CHANGES** |
| Scope | Reading architecture for BaZi Result (Portal) |
| Owner | Product Owner |
| Code | **NONE** until IA v1.1 APPROVED |

---

## Revision Summary (v1.0 → v1.1)

| ID | Change |
|----|--------|
| CH-01 | S01 rename → **Identity & Decision Panel** |
| CH-02 | Zone A: **no Cân Xương**; only Nhật Chủ · Ngũ Hành · Âm Dương (+ Avatar optional) |
| CH-03 | Zone C → **Decision Support** (What / Why / Next) — not a single recommendation line |
| CH-04 | S04 rename → **Element Balance** (balance focus, not element checklist) |
| CH-05 | Knowledge → **Learning Panel** (expandable) — not a large trailing section |
| CH-NEW | **S00 Context Header** before S01 (context only — not Nav, not Hero) |

---

# 1. Updated Reading Flow

## Timed map

| Time | User looks at | Understands |
|------|---------------|-------------|
| **0–3s** | **S00 Context Header** | “Đúng hồ sơ / đúng mã lá / trạng thái phân tích” |
| **3–8s** | **S01 Zone A — Identity** | “Tôi là Nhật Chủ X · hành Y · Âm/Dương” |
| **8–15s** | **S01 Zone B — Condition** | “Lá số mạnh / trung / nhược ở mức …” |
| **15–25s** | **S01 Zone C — Decision Support** | “Quan trọng nhất là gì → vì sao → tôi nên làm gì tiếp” |
| **25–45s** | **S02** (nếu còn) / bắt đầu **S03 Tứ Trụ** | Cấu trúc 4 trụ; Nhật Chủ khớp Zone A |
| **45–90s** | **S04 Element Balance** + **S05 Strength** | Vì sao cân/lệch; thân chi tiết |
| **Sau đó** | **S06 / S07** (secondary) → **S08 Interpretation** | Tín hiệu phụ → ý nghĩa đời sống |
| **Tuỳ chọn** | **Learning Panel** (mở khi cần) | Thuật ngữ / kiến thức nền — không chặn hành trình chính |

## Gaze direction (Desktop)

```
TOP     Primary Nav (sản phẩm)
  ↓
LEFT    TOC (bản đồ đọc)
  ↓
CENTER  S00 Context (xác nhận hồ sơ)
  ↓
CENTER  S01 Identity & Decision Panel  ★ First Viewport decision core
  ↓
DOWN    S02 → S03 → S04 → S05 → S06 → S07 → S08
  ↓
ON DEMAND   Learning Panel (drawer / accordion)
```

### Why this timing

- **S00 trước Identity:** tránh đọc “tôi là ai” trên nhầm hồ sơ.  
- **Identity trước Condition trước Decision:** nhận diện → đánh giá → hành động (thương mại).  
- **Learning on demand:** Progressive Disclosure — kiến thức không cạnh tranh quyết định.

---

# 2. Updated Section Hierarchy

```
PORTAL SHELL
├── Primary Nav (Top)
├── Page TOC (Left)
└── MAIN
    │
    ├── S00  Context Header
    │        Mục tiêu: Xác nhận đúng hồ sơ / phiên bản phân tích
    │        Chính: Hồ sơ đang xem, mã lá, ngày lập, trạng thái,
    │               phiên bản phân tích, thời điểm phân tích
    │        Phụ: Link thao tác nhẹ (nếu có) — không CTA lớn
    │        Decision: “Đây đúng lá số tôi đang xem chứ?”
    │        NOT: Navigation · NOT: Hero · NOT: Identity
    │
    ├── S01  Identity & Decision Panel     ★ FIRST VIEWPORT CORE
    │        (formerly “Executive Summary” / “Tóm tắt điều hành”)
    │        Mục tiêu: Giúp người dùng ĐƯA RA QUYẾT ĐỊNH sơ bộ
    │        Không phải “báo cáo tóm tắt kỹ thuật”
    │        Decision: “Tôi hiểu mình là ai / mạnh yếu / cần làm gì?”
    │
    ├── S02  Chart Overview (Bối cảnh mở rộng — nếu cần tách khỏi S00)
    │        Mục tiêu: Chi tiết hồ sơ & thao tác (PDF/In…) khi S00 chỉ strip
    │        Decision: “Xuất / phân tích lại / xem metadata?”
    │        Note: Nếu S00 đủ context tối thiểu, S02 có thể compact hoặc gộp thao tác
    │
    ├── S03  Four Pillars (Tứ Trụ)
    │        Mục tiêu: Xương sống cấu trúc Năm–Tháng–Ngày–Giờ
    │        Decision: “Bốn trụ ra sao? Nhật Chủ khớp S01?”
    │
    ├── S04  Element Balance          (formerly Five Elements)
    │        Mục tiêu: Mức độ cân bằng ngũ hành — không checklist 5 hàng
    │        Decision: “Lá số cân hay lệch? Lệch về đâu?”
    │
    ├── S05  Strength (Thân Vượng / Nhược)
    │        Mục tiêu: Chi tiết hóa Condition đã preview ở S01-B
    │        Decision: “Kết luận thân có vững không?”
    │
    ├── S06  Ten Gods (Thập Thần)
    │        Mục tiêu: Secondary — tín hiệu quan hệ
    │        Decision: “Có tín hiệu quan hệ nổi bật?” (không bắt buộc)
    │
    ├── S07  ShenSha (Thần Sát)
    │        Mục tiêu: Secondary — tín hiệu phụ
    │        Decision: “Có điểm phụ cần lưu ý?” (không bắt buộc)
    │
    ├── S08  Interpretation (Luận giải)
    │        Mục tiêu: Ý nghĩa đời sống đầy đủ hơn Zone C
    │        Decision: “Tôi nên làm gì — bản đầy đủ?”
    │
    └── LEARNING PANEL (Knowledge) — NOT a blocking end-section
             Pattern: Expandable Drawer | Accordion | Side Learning Panel
             Mục tiêu: Giải thích thuật ngữ khi người dùng chủ động mở
             Decision: “Thuật ngữ này nghĩa là gì?”
```

### TOC mapping (v1.1)

| TOC | Target |
|-----|--------|
| Ngữ cảnh | S00 (+ S02 nếu tách) |
| Tóm tắt / Quyết định | S01 |
| Bát Tự | S03 |
| Cân bằng / Phân tích | S04 + S05 |
| Chi tiết | S06 + S07 |
| Luận giải | S08 |
| Học thêm | Learning Panel (open) |

### CH-01 — Why rename S01

**Cũ:** Executive Summary / Tóm tắt điều hành → nghe như *báo cáo tóm tắt*.  

**Mới:** **Identity & Decision Panel** (alias ngắn: **Identity Summary**).  

**Vì sao:** Section đầu không tồn tại để “tóm tắt dữ liệu engine”. Nó tồn tại để người dùng:

1. Nhận diện bản thân trong lá số (Identity)  
2. Đưa ra quyết định sơ bộ (Decision)  

Đổi tên buộc mọi thiết kế sau này (kể cả S01 UI) bám *quyết định*, không bám *card báo cáo*.

---

# 3. Updated First Viewport

First Viewport = **S00 (compact strip) + S01 (Zones A–C)**.

S00 chiếm **một dải ngữ cảnh thấp** — không Hero.  
S01 chiếm **phần quyết định chính** — không scroll để hoàn tất A→B→C trên Desktop chuẩn.

```
+------------------------------------------------------------------+
| S00 CONTEXT HEADER (strip)                                       |
|  Hồ sơ · Mã lá · Ngày lập · Trạng thái · Version · Thời điểm     |
+------------------------------------------------------------------+
| S01 IDENTITY & DECISION PANEL                                    |
|                                                                  |
|  ZONE A — IDENTITY                                               |
|    [Avatar?]  Nhật Chủ (largest)                                 |
|               Ngũ Hành Nhật Chủ                                  |
|               Âm Dương                                           |
|    (KHÔNG Cân Xương)                                             |
|                                                                  |
|  ZONE B — CONDITION                                              |
|    Thân Vượng / Nhược                                            |
|    Đánh giá tổng quan                                            |
|                                                                  |
|  ZONE C — DECISION SUPPORT                                       |
|    1. Điều gì quan trọng nhất?                                   |
|    2. Vì sao?                                                    |
|    3. Tôi nên làm gì tiếp?                                       |
|    (Dụng / Hỷ / Kỵ / Cách Cục là đầu vào của 1–3 — không thay 1–3)|
|                                                                  |
+------------------------------------------------------------------+
        ↑ hết First Viewport decision core
```

## Zone A — Identity (CH-02)

| | |
|--|--|
| **Allowed** | Nhật Chủ · Ngũ Hành · Âm Dương · Avatar (optional) |
| **Forbidden** | Cân Xương Đoán Mệnh (và mọi metric “phụ / đo lường” cạnh tranh Nhật Chủ) |
| **Goal** | “Tôi là ai?” — tín hiệu thuần nhận diện |
| **Why no Cân Xương** | Cân Xương là *đánh giá phụ / folklore metric*, không phải identity cốt lõi. Đưa vào Zone A làm loãng Nhật Chủ và khiến Identity thành “dashboard chỉ số”. Đưa sang S02 hoặc Learning nếu cần sau |

## Zone B — Condition

Không đổi ý: mạnh/yếu + đánh giá tổng quan. Preview — chi tiết ở S05.

## Zone C — Decision Support (CH-03)

| | |
|--|--|
| **Not** | Một câu “Khuyến nghị đầu tiên” đơn lẻ |
| **Must answer** | (1) Điều gì quan trọng nhất? (2) Vì sao? (3) Tôi nên làm gì tiếp? |
| **Inputs** | Dụng Thần · Hỷ · Kỵ · Cách Cục (nếu có) — phục vụ trả lời 1–2–3 |
| **Exit** | Lối rõ sang S08 Interpretation / hành động tiếp theo |
| **Why** | Commercial product cần *decision support*, không cần *slogan khuyến nghị* |

---

# 4. Updated Decision Journey

```
S00  →  “Đây đúng hồ sơ / đúng lần phân tích của tôi chứ?”

S01-A →  “Tôi là ai?” (Nhật Chủ · Hành · Âm Dương)

S01-B →  “Lá số mạnh hay yếu?”

S01-C →  “Điều gì quan trọng nhất?”
      →  “Vì sao?”
      →  “Tôi nên làm gì tiếp?”

S02  →  “Tôi cần thao tác / xem thêm metadata không?”

S03  →  “Bốn trụ ra sao? Nhật Chủ khớp Identity?”

S04  →  “Ngũ hành cân hay lệch? Lệch về đâu?”   ← Element Balance

S05  →  “Kết luận Thân chi tiết có vững?”

S06  →  “Thập Thần nào nổi?” (optional)

S07  →  “Thần Sát nào đáng chú ý?” (optional)

S08  →  “Ý nghĩa đầy đủ & kế hoạch tiếp theo?”

Learning Panel →  “Thuật ngữ này nghĩa là gì?” (on demand)
```

---

# 5. Updated Wireframes

## Desktop

```
+==============================================================================+
| Primary Nav                                                         theme user|
+==============================================================================+
| TOC        |  RESULT                                                         |
| Ngữ cảnh   |  +------------------------------------------------------------+ |
| Quyết định●|  | S00 CONTEXT HEADER (strip — not hero)                      | |
| Bát Tự     |  | Hồ sơ · Mã · Ngày lập · Status · Version · Timestamp       | |
| Cân bằng   |  +------------------------------------------------------------+ |
| Chi tiết   |  | S01 IDENTITY & DECISION PANEL                              | |
| Luận giải  |  |  A Identity: Avatar? | Nhật Chủ | Ngũ Hành | Âm Dương      | |
| Học thêm※  |  |  B Condition: Thân | Đánh giá                              | |
|            |  |  C Decision Support: What? Why? Next?                      | |
|            |  +------------------------------------------------------------+ |
|            |======== fold ===================================================|
|            |  S02 (optional expand) · S03 Four Pillars                       |
|            |  S04 Element Balance  |  S05 Strength                           |
|            |  S06 Ten Gods         |  S07 ShenSha                            |
|            |  S08 Interpretation                                             |
|            |  ※ Learning Panel = drawer/accordion (not full-page end block)  |
+==============================================================================+
```

※ TOC “Học thêm” **mở Learning Panel**, không scroll tới “section Knowledge khổng lồ”.

## Tablet

Cùng hierarchy. S00 strip full width. S01 A→B→C stack gọn. S03 = 2×2. S04/S05 xếp dọc nếu hẹp. Learning = bottom sheet / accordion.

## Mobile

```
+---------------------------+
| Nav / ☰                   |
+---------------------------+
| S00 CONTEXT (compact)     |
| tên · mã · status         |
+---------------------------+
| S01-A Identity            |
|   Nhật Chủ (largest)      |
|   Ngũ Hành · Âm Dương     |
+---------------------------+
| S01-B Condition           |
+---------------------------+
| S01-C Decision Support    |
|   What? Why? Next?        |
+---------------------------+
| S02…S08 (scroll)          |
| Learning = accordion/drawer|
+---------------------------+
```

---

# 6. Design Rationale (Changes)

### CH-04 — Element Balance (not Five Elements list)

**Cũ:** “Five Elements” dễ thành *danh sách 5 hàng* (Kim/Mộc/Thủy/Hỏa/Thổ).  

**Mới:** **Element Balance** — câu hỏi là *cân hay lệch, lệch hướng nào*.  

**Vì sao:** Khớp Decision Journey (“vì sao mạnh/yếu?”) và Progressive Disclosure; tránh UI checklist kỹ thuật trước khi người dùng hiểu *ý nghĩa cân bằng*.

### CH-05 — Knowledge as Learning Panel

**Cũ:** S09 section lớn cuối trang → buộc scroll hết mới “học”; cạnh tranh với Interpretation.  

**Mới:** **Expandable Drawer / Accordion / Side Learning Panel** — mở khi cần.  

**Vì sao:** Progressive Disclosure (Principle 03). Kiến thức là *hỗ trợ nhận thức*, không phải *bước bắt buộc* trong hành trình quyết định. Commercial flow kết thúc quyết định ở S01-C / S08 — không kết thúc bằng giáo trình.

### CH-NEW — S00 Context Header

**Vì sao trước S01:** Identity chỉ có ý nghĩa khi người dùng chắc đang xem đúng hồ sơ.  

**Vì sao không phải Nav:** Nav định vị *sản phẩm*; S00 định vị *đối tượng dữ liệu*.  

**Vì sao không phải Hero:** Hero/Identity thuộc S01; S00 chỉ strip xác nhận.

---

# 7. IA Freeze Recommendation

## Stable order for BTE Platform V1.0 (proposed freeze)

```
S00 Context Header
  ↓
S01 Identity & Decision Panel
  ↓
S02 Chart Overview (compact / actions — if kept separate)
  ↓
S03 Four Pillars
  ↓
S04 Element Balance
  ↓
S05 Strength
  ↓
S06 Ten Gods
  ↓
S07 ShenSha
  ↓
S08 Interpretation
  ↓
Learning Panel (on demand — not ordered as a blocking S09 page section)
```

## After Freeze — có cần đổi thứ tự nữa không?

**Không — nếu PO APPROVE v1.1.**

Thứ tự trên được coi là **Information Architecture ổn định cho BTE Platform V1.0**, vì:

1. Context → Identity → Decision → Structure → Balance → Strength → Secondary → Meaning → Learning-on-demand đã khép kín 5 câu hỏi thương mại.  
2. Các thay đổi v1.1 đã xử lý đúng các lỗi đặt tên / nhiễu Zone A / Decision nông / Knowledge sai tầng.  
3. Thay đổi sau Freeze chỉ nên là **nội dung trong section** hoặc **pattern Learning Panel**, không đảo thứ tự S00→S08.

**Ngoại lệ duy nhất (không đảo hierarchy):** gộp/tách nhẹ **S00 ↔ S02** (strip vs panel thao tác) nếu PO muốn giảm số section — vẫn giữ *Context trước Identity*.

---

# 8. Open Items Resolved vs Remaining

| Item | Status in v1.1 |
|------|----------------|
| S01 naming | Resolved → Identity & Decision Panel |
| Zone A Cân Xương | Resolved → removed from Identity |
| Zone C depth | Resolved → Decision Support What/Why/Next |
| Five Elements naming | Resolved → Element Balance |
| Knowledge placement | Resolved → Learning Panel on demand |
| S00 Context | Added |
| S02 vs S00 boundary | **Optional PO note:** keep S02 for actions/PDF or fold into S00+toolbar |

---

# STOP

IA Revision **v1.1** sẵn sàng cho Product Owner.

```
Không thiết kế S00/S01 UI
Không React · CSS · Component
Chờ APPROVED (Architecture Freeze)
Chỉ sau APPROVED mới được thiết kế S00 rồi S01
```
Architecture Status

APPROVED

Architecture Freeze

Version 1.1
