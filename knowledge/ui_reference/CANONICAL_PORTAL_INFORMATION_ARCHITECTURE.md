# BTE Platform V1.0

# Canonical Portal Information Architecture

# Design Review Package

---

## Document Information

| Item | Value |
|------|-------|
| Document | Canonical Portal Information Architecture — Design Review Package |
| Version | **1.0 — PO Review** |
| Status | **AWAITING PRODUCT OWNER DECISION** (PASS / PASS WITH CHANGES / REJECT) |
| Scope | Cách đọc một lá số Bát Tự trên Portal (Result page primary) |
| Owner | Product Owner |
| References | `CANONICAL_PORTAL_UI.md`, `UI_DESIGN_PRINCIPLES.md`, `CANONICAL_PORTAL_UI.png`, `UI_CHANGELOG.md` |
| Code | **NONE** — Không React / CSS / UI / S01 cho đến khi IA được duyệt |

---

## Why This Architecture Exists

Product Owner Round 2 **REJECT** vì team đang thiết kế *card*, trong khi bài toán thật là:

> **Thiết kế cách người dùng đọc một lá số Bát Tự.**

Kiến trúc dưới đây trả lời 5 câu hỏi thương mại trước khi có bất kỳ pixel nào:

1. Tôi là ai?  
2. Lá số mạnh hay yếu?  
3. Điều gì quan trọng nhất?  
4. Tôi cần quan tâm điều gì?  
5. Muốn đọc sâu thì đọc đâu?

**Quy tắc vàng:** Câu 1–4 phải trả lời được trong **First Viewport** (không bắt buộc scroll).

---

# 1. Reading Flow

## 1.1 Timed Reading Map

| Thời gian | Người dùng nhìn gì | Họ hiểu thêm điều gì | Vì sao đúng |
|-----------|--------------------|----------------------|-------------|
| **0–5 giây** | **Nhật Chủ** (tín hiệu lớn nhất) → nhanh đến **Đánh giá tổng quan** + **Thân** | “Tôi là X (Ngũ Hành · Âm Dương). Lá số đang **vượng / trung / nhược**.” | Identity trước bằng chứng — commercial & Principle 02 |
| **5–15 giây** | **Dụng Thần · Hỷ · Kỵ · Cách Cục** + 1 câu khuyến nghị đầu | “Điều quan trọng nhất là …; tôi cần quan tâm …” | Priority signal — quyết định sơ bộ không cần kỹ thuật |
| **15–30 giây** | **Bối cảnh lá số** (tên, mã, ngày sinh) + bắt đầu **Tứ Trụ** | “Đây là lá số của ai / cấu trúc 4 trụ thế nào” | Neo ngữ cảnh rồi mới xem xương sống kỹ thuật |
| **30–60 giây** | Hoàn tất **Tứ Trụ** (Nhật Chủ trùng với S01) | “Ngày là trung tâm; bốn trụ khớp với tóm tắt” | Củng cố niềm tin: tóm tắt không mâu thuẫn cấu trúc |
| **Sau 60 giây** | Kéo xuống / TOC: Ngũ Hành → Thân chi tiết → Thập Thần → Thần Sát → Luận giải → Tri thức | “Vì sao mạnh/yếu; tín hiệu phụ; ý nghĩa đời sống; học thêm” | Progressive Disclosure — sâu chỉ khi sẵn sàng |

## 1.2 Reading Narrative (plain language)

```
0–5s     Nhìn Nhật Chủ → “Tôi là ai?”
5–15s    Nhìn Thân + Dụng/Hỷ/Kỵ → “Mạnh/yếu? Quan trọng nhất là gì?”
15–30s   Nhìn bối cảnh + Tứ Trụ → “Lá số này dựng thế nào?”
30–60s   Khớp Nhật Chủ trên trụ Ngày với S01 → “Tóm tắt đáng tin”
>60s     Chọn sâu: cơ chế / tín hiệu phụ / luận giải / tri thức
```

## 1.3 Direction of Gaze (Desktop)

```
TOP    (Header: đang ở “Kết quả” — định vị sản phẩm)
  ↓
LEFT   (TOC: bản đồ trang — không phải nội dung chính)
  ↓
CENTER (First Viewport = S01 Zones A→C — trả lời Q1–Q4)
  ↓
DOWN   (S02 → S09 — bằng chứng & ý nghĩa)
```

Không bắt người dùng nhảy ngang liên tục giữa các khối không cùng tầng ý nghĩa.

---

# 2. Information Hierarchy (Tree)

```
PORTAL SHELL
├── Primary Nav (Top)     … định vị sản phẩm
├── Page TOC (Left)       … bản đồ đọc trong trang Kết quả
└── MAIN RESULT COLUMN
    │
    ├── S01  Tóm tắt điều hành          ★ FIRST VIEWPORT
    │        Mục tiêu: Trả lời Q1–Q4 trong vài giây
    │        Chính: Nhật Chủ, Thân, Đánh giá, Dụng/Hỷ/Kỵ, Cách Cục, khuyến nghị 1 câu
    │        Phụ: Cân Xương (nếu có), độ tin cậy
    │        Decision: “Tôi hiểu sơ bộ lá số — có cần đọc sâu không?”
    │
    ├── S02  Bối cảnh lá số
    │        Mục tiêu: Neo ngữ cảnh (ai / mã / thao tác)
    │        Chính: Họ tên, ngày giờ sinh, mã lá, trạng thái
    │        Phụ: Engine/version metadata, CTA PDF/In (có thể disabled)
    │        Decision: “Đây đúng lá số của tôi / tôi muốn xuất hoặc phân tích lại?”
    │
    ├── S03  Tứ Trụ
    │        Mục tiêu: Chỉ cấu trúc gốc Năm–Tháng–Ngày–Giờ
    │        Chính: 4 trụ; trụ Ngày = Nhật Chủ
    │        Phụ: Tàng Can, Nạp Âm, Trường Sinh, Thập Thần trên trụ
    │        Decision: “Tôi thấy xương sống lá số; Nhật Chủ khớp S01?”
    │
    ├── S04  Ngũ Hành
    │        Mục tiêu: Cơ chế phân bố năng lượng
    │        Chính: Kim Mộc Thủy Hỏa Thổ (mức / %)
    │        Phụ: Nhãn mạnh/yếu từng hành
    │        Decision: “Vì sao lá số nghiêng theo hướng đó?”
    │
    ├── S05  Thân Vượng / Nhược
    │        Mục tiêu: Chi tiết hóa Q2 đã preview ở S01
    │        Chính: Thang điểm / nhãn vượng–nhược, kết luận
    │        Phụ: Mô tả ngắn, độ tin cậy
    │        Decision: “Kết luận sức mạnh đã đủ rõ để tin?”
    │
    ├── S06  Thập Thần
    │        Mục tiêu: Tín hiệu quan hệ (secondary)
    │        Chính: Có / không của từng thần
    │        Phụ: Điểm số / mô tả ngắn
    │        Decision: “Có tín hiệu quan hệ nào nổi bật không?” (không bắt buộc)
    │
    ├── S07  Thần Sát
    │        Mục tiêu: Tín hiệu phụ cát/hung
    │        Chính: Có / không / chưa xác định
    │        Phụ: Chú thích
    │        Decision: “Có điểm phụ cần lưu ý không?” (không bắt buộc)
    │
    ├── S08  Luận giải
    │        Mục tiêu: Ý nghĩa đời sống + khuyến nghị đầy đủ
    │        Chính: Đoạn luận, khuyến nghị hành động
    │        Phụ: Liên kết lại Dụng/Kỵ
    │        Decision: “Tôi nên làm gì tiếp theo?”
    │
    └── S09  Tri thức
             Mục tiêu: Học thuật ngữ / nền tảng
             Chính: Liên kết khái niệm (Nhật Chủ, Thân, Dụng…)
             Phụ: Tham chiếu Knowledge Pack
             Decision: “Tôi muốn hiểu sâu thuật ngữ nào?”
```

### TOC ↔ Section

| TOC | Jump |
|-----|------|
| Tóm tắt | S01 |
| Bối cảnh | S02 |
| Bát Tự | S03 |
| Phân tích | S04 + S05 |
| Chi tiết | S06 + S07 |
| Luận giải | S08 |
| Tri thức | S09 |

---

# 3. Desktop Wireframe

```
+====================================================================================+
| BTE Portal    Trang chủ  Luận giải  [Kết quả]  Báo cáo  Lịch sử  Tài khoản   🌙 👤 |
+====================================================================================+
| MỤC LỤC     |  KẾT QUẢ BÁT TỰ                                                      |
|             |  subtitle: mã lá · tên  (phụ — không át S01)                         |
| • Tóm tắt ● |----------------------------------------------------------------------|
| • Bối cảnh  |                                                                      |
| • Bát Tự    |  +----------------------------------------------------------------+  |
| • Phân tích |  | S01  TÓM TẮT ĐIỀU HÀNH              << FIRST VIEWPORT >>      |  |
| • Chi tiết  |  |                                                                |  |
| • Luận giải |  |  ZONE A IDENTITY                                                |  |
| • Tri thức  |  |    Nhật Chủ (largest) | Ngũ Hành | Âm Dương | (Cân Xương?)     |  |
|             |  |                                                                |  |
|             |  |  ZONE B CONDITION                                              |  |
|             |  |    Thân Vượng/Nhược | Đánh giá tổng quan                       |  |
|             |  |                                                                |  |
|             |  |  ZONE C PRIORITY                                               |  |
|             |  |    Dụng | Hỷ | Kỵ | Cách Cục                                   |  |
|             |  |    Khuyến nghị đầu tiên  →  sang Luận giải                     |  |
|             |  +----------------------------------------------------------------+  |
|             |                                                                      |
|             |======== typical laptop fold ========================================|
|             |                                                                      |
|             |  +----------------------------------------------------------------+  |
|             |  | S02  BỐI CẢNH LÁ SỐ  (hồ sơ · metadata · thao tác)             |  |
|             |  +----------------------------------------------------------------+  |
|             |                                                                      |
|             |  +----------------------------------------------------------------+  |
|             |  | S03  TỨ TRỤ                                                    |  |
|             |  |   [ Năm ]  [ Tháng ]  [ Ngày* ]  [ Giờ ]                       |  |
|             |  |                    *Nhật Chủ                                   |  |
|             |  +----------------------------------------------------------------+  |
|             |                                                                      |
|             |  +---------------------------+  +--------------------------------+  |
|             |  | S04  NGŨ HÀNH             |  | S05  THÂN VƯỢNG / NHƯỢC        |  |
|             |  +---------------------------+  +--------------------------------+  |
|             |                                                                      |
|             |  +---------------------------+  +--------------------------------+  |
|             |  | S06  THẬP THẦN            |  | S07  THẦN SÁT                  |  |
|             |  +---------------------------+  +--------------------------------+  |
|             |                                                                      |
|             |  +----------------------------------------------------------------+  |
|             |  | S08  LUẬN GIẢI                                                 |  |
|             |  +----------------------------------------------------------------+  |
|             |                                                                      |
|             |  +----------------------------------------------------------------+  |
|             |  | S09  TRI THỨC                                                  |  |
|             |  +----------------------------------------------------------------+  |
| theme / ver |  disclaimer                                                          |
+====================================================================================+
```

---

# 4. Tablet Wireframe

Cùng hierarchy — chỉ đổi xếp chỗ (UI-008).

```
+==============================================================+
| BTE Portal     nav rút gọn / có thể scroll ngang        👤   |
+==============================================================+
| TOC | MAIN                                                   |
| hẹp |  S01  Zone A → B → C (dọc hơn; glance 3×2)             |
| icon|                                                        |
|     |======== fold ==========================================|
|     |  S02                                                   |
|     |  S03  Tứ Trụ  2×2                                      |
|     |  S04                                                   |
|     |  S05                                                   |
|     |  S06                                                   |
|     |  S07                                                   |
|     |  S08 → S09                                             |
+==============================================================+
```

---

# 5. Mobile Wireframe

```
+-----------------------------+
| ☰  BTE Portal          👤   |
+-----------------------------+
| Primary: [Kết quả] …        |
+-----------------------------+
| TOC = drawer (không che S01 |
| khi vừa mở trang)           |
+-----------------------------+
| S01 ZONE A — IDENTITY       |
|   Nhật Chủ (largest)        |
|   Ngũ Hành · Âm Dương       |
+-----------------------------+
| S01 ZONE B — CONDITION      |
|   Thân · Đánh giá           |
+-----------------------------+
| S01 ZONE C — PRIORITY       |
|   Dụng · Hỷ · Kỵ · Cách Cục |
|   Khuyến nghị → Luận giải   |
+-----------------------------+
| —— scroll / TOC jump ——     |
| S02 Bối cảnh                |
| S03 Tứ Trụ (xếp dọc 1 cột)  |
| S04 Ngũ Hành                |
| S05 Thân                    |
| S06 Thập Thần               |
| S07 Thần Sát                |
| S08 Luận giải               |
| S09 Tri thức                |
+-----------------------------+
```

**Mobile:** một cột; không horizontal scroll; cùng thứ tự S01→S09.

---

# 6. First Viewport (quan trọng nhất)

First Viewport = phần nhìn thấy **không scroll** trên Desktop chuẩn.

Chỉ chứa **`S01 — Tóm tắt điều hành`**, chia 3 zone bắt buộc (+ Zone D tùy chọn).

```
+------------------------------------------------------------------+
| S01 — TÓM TẮT ĐIỀU HÀNH                                          |
|                                                                  |
|  ZONE A — IDENTITY                                               |
|  ZONE B — CONDITION                                              |
|  ZONE C — PRIORITY                                               |
|  ZONE D — (optional) CONTEXT STRIP                               |
|                                                                  |
+------------------------------------------------------------------+
        ↑ hết First Viewport — dưới đây mới là S02+
```

## Zone A — Identity

| | |
|--|--|
| **Nội dung** | Nhật Chủ (lớn nhất); Ngũ Hành Nhật Chủ; Âm Dương; (tuỳ chọn) Cân Xương |
| **Mục tiêu** | Trả lời **“Tôi là ai?”** trong 0–5 giây |
| **Lý do tồn tại** | Không có identity → mọi phân tích phía dưới vô nghĩa với người mới. Nhật Chủ phải là tín hiệu thị giác #1 |

## Zone B — Condition

| | |
|--|--|
| **Nội dung** | Thân Vượng / Nhược (nhãn + mức); Đánh giá tổng quan (grade / verdict ngắn) |
| **Mục tiêu** | Trả lời **“Lá số mạnh hay yếu?”** |
| **Lý do tồn tại** | Commercial: khách hàng cần *đánh giá*, không cần *công thức* ngay. Preview kết luận — chi tiết nằm ở S05 |

## Zone C — Priority

| | |
|--|--|
| **Nội dung** | Dụng Thần; Hỷ Thần; Kỵ Thần; Cách Cục (nếu có); **một** câu khuyến nghị đầu + lối vào Luận giải |
| **Mục tiêu** | Trả lời **“Điều gì quan trọng nhất?”** và **“Tôi cần quan tâm gì?”** |
| **Lý do tồn tại** | Biến Portal từ “bảng dữ liệu” thành “sản phẩm ra quyết định”. Không có Zone C → người dùng biết mình là ai nhưng không biết làm gì |

## Zone D — Optional Context Strip (không bắt buộc trong fold)

| | |
|--|--|
| **Nội dung** | Mã lá số · tên ngắn · badge trạng thái (Hoàn tất) |
| **Mục tiêu** | Neo “đúng hồ sơ” mà không chiếm chỗ Zone A–C |
| **Lý do tồn tại** | Giảm nhầm lá số. Nếu làm phình First Viewport → đẩy xuống S02 |

### Những gì **không** được vào First Viewport

- Toàn bộ lưới Thập Thần / Thần Sát  
- Bảng Tứ Trụ đầy đủ chi tiết  
- Luận giải dài / Knowledge Pack  
- Form nhập liệu / Dashboard widgets  

---

# 7. User Journey

**Persona:** Người chưa từng biết Bát Tự. Vừa có kết quả lá số. Mở **Kết quả**.

| Bước | Đọc gì | Hiểu thêm sau bước đó |
|------|--------|------------------------|
| 0 | Header “Kết quả” + TOC | Đây là trang kết quả lá số, có mục lục |
| 1 | Zone A — Nhật Chủ | “Tôi gắn với một ‘Nhật Chủ’ tên X, thuộc hành Y” |
| 2 | Zone B — Thân + Đánh giá | “Lá số này thiên về mạnh/yếu ở mức …” |
| 3 | Zone C — Dụng/Hỷ/Kỵ | “Ưu tiên quan tâm yếu tố …; tránh …” |
| 4 | (Tuỳ chọn) dừng hoặc chia sẻ | Đã có quyết định sơ bộ — không bắt buộc kỹ thuật |
| 5 | S02 Bối cảnh | Xác nhận đúng người / đúng mã lá |
| 6 | S03 Tứ Trụ | Thấy 4 cột thời gian; trụ Ngày = Nhật Chủ đã gặp |
| 7 | S04–S05 Phân tích | Hiểu *vì sao* mạnh/yếu qua Ngũ Hành + thang Thân |
| 8 | S06–S07 (lướt) | Biết có tín hiệu phụ; không bắt buộc hiểu hết |
| 9 | S08 Luận giải | Nhận khuyến nghị đời sống đầy đủ hơn Zone C |
| 10 | S09 Tri thức (tuỳ chọn) | Học thuật ngữ khi muốn |

### Anti-journey (không được xảy ra)

- Phải kéo qua metadata / checklist dài mới thấy Nhật Chủ  
- Thần Sát trước Đánh giá tổng quan  
- TOC thứ tự khác với nội dung  
- Hai “ngôn ngữ tầng thông tin” giữa Dashboard và Result  

---

# 8. Decision Journey

Sau mỗi section, người dùng trả lời được câu hỏi nào?

```
S01  →  “Tôi là ai?”
     →  “Lá số mạnh hay yếu?”
     →  “Điều gì quan trọng nhất / tôi cần quan tâm gì?”
     →  “Có cần đọc sâu hơn không?”

S02  →  “Đây đúng lá số của tôi chứ?”
     →  “Tôi muốn xuất / làm lại không?”

S03  →  “Bốn trụ ra sao? Nhật Chủ nằm ở đâu trong cấu trúc?”

S04  →  “Ngũ Hành phân bố thế nào? Vì sao nghiêng?”

S05  →  “Kết luận Thân có vững không? Chi tiết mức độ ra sao?”

S06  →  “Thập Thần nào nổi bật / vắng?”

S07  →  “Thần Sát nào đáng chú ý?”

S08  →  “Ý nghĩa đời sống là gì? Tôi nên làm gì tiếp?”

S09  →  “Thuật ngữ này nghĩa là gì? Học thêm ở đâu?”
```

---

# 9. Section Rationale

## Vì sao thứ tự này?

| So sánh | Lý do đứng trước | Nếu đảo vị trí thì sao? |
|---------|------------------|-------------------------|
| **S01 trước mọi thứ** | Kết luận thương mại trước bằng chứng (Principle 02, UI-002) | Người mới bị ngợp kỹ thuật → bỏ cuộc / không tin sản phẩm |
| **S02 sau S01, trước S03** | Neo ngữ cảnh sau khi đã có tóm tắt | Metadata/hồ sơ chiếm First Viewport → chậm trả lời “tôi là ai?” |
| **S03 trước S04/S05** | Tứ Trụ là xương sống; cần thấy cấu trúc trước biểu đồ | Ngũ Hành/Thân “lơ lửng” — người mới không biết số liệu gắn vào đâu |
| **S04 trước S05** | Phân bố hành → rồi mới chi tiết kết luận thân | Thân chi tiết trước khi thấy cơ chế → khó tin / khó giải thích |
| **S01 preview Thân/Dụng; S04–S05 chi tiết sau** | Progressive Disclosure | Nhồi hết cơ chế lên đầu → First Viewport thành dashboard kỹ thuật |
| **S06/S07 sau core** | Secondary signals (UI-005) | Checklist dài lên sớm → nhiễu Q1–Q4 |
| **S08 sau phân tích** | Meaning cần bằng chứng | Luận giải sớm = “lời hay” thiếu neo → giảm tin cậy |
| **S09 cuối** | Learning tùy chọn | Tri thức lên sớm = giáo trình, không phải sản phẩm quyết định |

## Nguyên tắc sắp xếp

```
Kết luận (S01)
  → Ngữ cảnh (S02)
  → Cấu trúc (S03)
  → Cơ chế (S04–S05)
  → Tín hiệu phụ (S06–S07)
  → Ý nghĩa (S08)
  → Học thêm (S09)
```

---

# 10. Commercial Review

Kiến trúc này phù hợp sản phẩm thương mại vì:

1. **Time-to-value < 15 giây** — khách hiểu “tôi là ai / mạnh yếu / ưu tiên” trước khi đọc kỹ thuật.  
2. **Quyết định trước bằng chứng** — đúng kỳ vọng mua luận giải, không kỳ vọng phần mềm nghiên cứu.  
3. **Progressive Disclosure** — giảm cognitive load; người mới không bị “đập” Thần Sát trước.  
4. **Một reading language** — dễ bán, dễ demo, dễ đào tạo CS/sales (Principle 12).  
5. **Lối vào upsell tự nhiên** — Zone C → Luận giải / Báo cáo PDF sau khi đã tin tóm tắt.  
6. **Responsive cùng hierarchy** — một câu chuyện trên Desktop/Tablet/Mobile (UI-008).  
7. **Sẵn sàng Integration sau UI Freeze** — IA ổn định thì API chỉ “đổ dữ liệu vào đúng tầng”, không phá bố cục.

Không phù hợp thương mại nếu: Portal trông như tool nội bộ xếp đầy bảng kỹ thuật từ trên xuống.

---

# 11. Screenshot Mapping

Dùng để PO **so sánh ý tưởng IA** với ảnh tham chiếu / ảnh hiện trạng — **không** phải bằng chứng UI đã đạt.

| Wireframe zone | Ảnh tham chiếu / hiện trạng | Ghi chú review |
|----------------|-----------------------------|----------------|
| Shell: Top nav + TOC trái | `CANONICAL_PORTAL_UI.png` | Học **cấu trúc khung đọc**, không copy pixel/màu |
| First Viewport ≈ “Tóm tắt” trên ảnh canonical | `CANONICAL_PORTAL_UI.png` (phần trên) | Đối chiếu Zone A/B/C — thiếu gì / thừa gì |
| Tứ Trụ / Phân tích phía dưới fold | `CANONICAL_PORTAL_UI.png` (phần giữa–dưới) | Khớp S03 → S05 / secondary |
| Baseline trước Canonical | `CURRENT_PORTAL_UI.png` | So “thiếu hierarchy” vs IA đề xuất |
| Round 2 (REJECT — card polish) | `migration_report/screenshots/round2_executive/*` | Minh họa **sai bài toán** (đẹp card ≠ đúng IA) — không dùng làm chuẩn |

```
Wireframe S01 Zones A–C
        ↓  so sánh ý
CANONICAL_PORTAL_UI.png (upper)
        ↓  không copy
Design System BTE (sau khi IA PASS)
```

---

# 12. Known Weaknesses

Tự đánh giá — **không sửa trong gói này**:

1. **Ranh giới S01 vs S04/S05** — Dụng/Hỷ/Kỵ vừa nằm Zone C vừa thuộc “Core Analysis” trong spec cũ; cần PO chốt: preview ở S01, chi tiết ở đâu (S01 only / S04–S05 / cả hai đồng bộ).  
2. **S02 có thể bị bỏ qua** — người mới có thể nhảy TOC thẳng S03; cần quyết định S02 bắt buộc hay compact strip.  
3. **Cân Xương** — hữu ích thương mại nhưng dễ cạnh tranh thị giác với Nhật Chủ nếu đặt Zone A.  
4. **Mobile fold** — màn hình ngắn có thể không chứa trọn Zone C trong first paint; cần chấp nhận Zone C ngay dưới fold.  
5. **Độ dài S08** — chưa giới hạn progressive trong Luận giải (accordion / “đọc thêm”).  
6. **Đồng bộ Dashboard** — IA này tập trung Result; Dashboard mới chỉ nêu principle, chưa tree chi tiết.  
7. **Thuật ngữ** — người mới vẫn gặp chữ Hán-Việt; S09 giúp sau, chưa giải quyết onboarding thuật ngữ trong S01 (tooltip IA vs copy).  

---

# 13. Open Questions (cần Product Owner quyết)

| ID | Câu hỏi | Gợi ý mặc định (nếu PO không chọn) |
|----|---------|-------------------------------------|
| OQ-1 | Zone C có **bắt buộc** Có Cách Cục không khi Engine chưa có? | Hiện “—” / “Chưa có” — không ẩn zone |
| OQ-2 | Cân Xương nằm Zone A hay chỉ S02/phụ? | Phụ trong Zone A, nhỏ hơn Nhật Chủ |
| OQ-3 | S04+S05 Desktop: **cùng hàng** hay xếp dọc? | Cùng hàng (cơ chế); mobile xếp dọc |
| OQ-4 | S06+S07: luôn hiện hay “mở thêm”? | Luôn hiện, dưới fold — secondary nhưng không ẩn |
| OQ-5 | Khuyến nghị đầu (Zone C) lấy từ đâu trước Integration? | Copy mock cố định, ghi rõ mock |
| OQ-6 | Sau IA PASS, Round tiếp theo có đổi tên S01 thành “Product Identity & Decision Panel” không? | Đồng ý đổi tên hiển thị; giữ ID `S01` |
| OQ-7 | TOC label “Phân tích” nhảy tới S04 hay tới anchor chung S04–S05? | Anchor chung `#phan-tich` bao cả hai |

---

# Decision Request

Product Owner chọn một:

- **PASS** — được phép thiết kế UI Section **S01** theo IA này (Design → Screenshot → Review).  
- **PASS WITH CHANGES** — nêu thay đổi hierarchy/flow; cập nhật IA rồi duyệt lại.  
- **REJECT** — nêu phần Reading Flow / Hierarchy / First Viewport cần làm lại.

---

# STOP

```
Design Review Package đã gửi
        ↓
DỪNG
        ↓
Không S01 · Không UI · Không CSS · Không React
        ↓
Chờ Product Owner Review
```
