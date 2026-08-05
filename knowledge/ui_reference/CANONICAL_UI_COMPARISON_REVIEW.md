# BTE Platform V1.0

# Canonical UI Comparison Review

---

## Document Information

| Item | Value |
|------|-------|
| Document | Canonical UI Comparison Review |
| Version | 1.0 |
| Status | **ANALYSIS ONLY — NO IMPLEMENTATION** |
| Trigger | Product Owner **REJECT** — S00 Context Header |
| Owner | Product Owner |
| Scope | So sánh triết lý thiết kế: Canonical vs UI hiện tại (sau S00) |

---

## Purpose

Tài liệu này **không thiết kế lại UI**.

Mục tiêu:

1. Chỉ rõ Agent đã hiểu sai Canonical Portal ở đâu.
2. So sánh cụ thể Canonical UI với UI hiện tại (đặc biệt sau S00).
3. Khóa tư duy: **Reading Experience / Decision Support** — không phải Component / CRM / Admin Dashboard.

**Chỉ được mở lại thiết kế S00 sau khi PO xác nhận Agent đã hiểu đúng.**

---

## References Used

| Reference | Path | Role |
|-----------|------|------|
| Canonical (ẢNH 2) | `knowledge/ui_reference/CANONICAL_PORTAL_UI.png` | Target reading / decision layout philosophy |
| Current baseline (ẢNH 1) | `knowledge/ui_reference/CURRENT_PORTAL_UI.png` | Baseline trước migration |
| Spec | `CANONICAL_PORTAL_UI.md`, `UI_DESIGN_PRINCIPLES.md`, IA v1.1, Screen Spec | Luật đọc thông tin |
| S00 Desktop Full | `migration_report/screenshots/s00_context/01_desktop_full.png` | UI hiện tại — First Viewport |
| S00 Desktop Zoom | `.../02_desktop_zoom_s00.png` | UI hiện tại — S00 tách riêng |
| S00 Tablet | `.../03_tablet.png` | Responsive hiện tại |
| S00 Mobile | `.../04_mobile.png` | Mobile hiện tại |

---

## Verdict (one line)

**Canonical tối ưu hành trình quyết định của người đọc lá số. UI hiện tại (S00) tối ưu hiển thị record metadata như CRM — vì vậy bị REJECT dù component/CSS có thể “đúng kỹ thuật”.**

---

# GROUP 1 — Information Hierarchy

| # | Điểm khác | Canonical | UI hiện tại (S00 / Result) |
|---|-----------|-----------|----------------------------|
| 1 | **Tầng thông tin mở đầu** | Kết luận / nhận diện lá số trước (Nhật Chủ, đánh giá, tín hiệu quyết định). | Metadata hồ sơ trước (tên, mã, version, timestamp, status). |
| 2 | **Vai trò khối đầu trang** | Hero / Executive Summary = “Tôi là ai? Lá số thế nào?” | Context strip = “Record nào đang mở?” — câu hỏi của admin, không phải của người xem mệnh. |
| 3 | **Thứ tự giá trị thương mại** | Identity → Condition → Decision → cấu trúc → phân tích phụ → luận giải. | Page title kỹ thuật → CRM strip → mới đến Executive (đã đẩy xuống dưới fold cảm nhận). |
| 4 | **Độ ưu tiên “Mã lá số / Version”** | Metadata kỹ thuật là phụ — không chiếm tầng 1. | `BZ-…`, `1.0.0-ui`, `14:28` được đưa lên First Viewport như field chính. |
| 5 | **Độ ưu tiên “Nhật Chủ”** | Tín hiệu lớn nhất hoặc trong cụm kết luận đầu. | Không xuất hiện trong S00; bị trì hoãn cho section sau — trong khi S00 lại chiếm vị trí “mở màn”. |
| 6 | **Page chrome vs nội dung** | Tiêu đề khu vực gắn với nội dung đọc (“Tóm tắt…” / Executive). | “Kết Quả Bát Tự” + subtitle `chartId · name` lặp lại thông tin strip — hierarchy page shell kiểu SaaS admin. |
| 7 | **TOC active mặc định** | Gắn với điểm bắt đầu đọc kết quả (Tóm tắt / Summary). | Active “Ngữ cảnh” — dẫn user vào metadata, không vào kết luận. |
| 8 | **Progressive Disclosure** | Tóm tắt → chi tiết → kiến thức on demand. | S00 phơi toàn bộ field admin ngay từ đầu; disclosure đang đi ngược (chi tiết hệ thống trước, ý nghĩa sau). |

---

# GROUP 2 — Reading Flow

| # | Điểm khác | Canonical | UI hiện tại |
|---|-----------|-----------|-------------|
| 9 | **5 giây đầu — mắt dừng đâu?** | Ở Nhật Chủ / grade / khuyến nghị — trả lời “tôi là ai / mạnh yếu / làm gì”. | Ở avatar + họ tên + mã lá số + status “Hoàn tất (mock)” — trả lời “hồ sơ đã load”. |
| 10 | **Câu hỏi đầu tiên hệ thống trả lời** | Who / Strong-Weak / What matters / What next. | Which record? Which version? When analyzed? |
| 11 | **Hướng đọc** | Top → (TOC hỗ trợ) → xuống theo tầng ý nghĩa. | Top nav → page title → horizontal label/value strip → mới xuống Executive. |
| 12 | **Nhịp “đọc báo cáo” vs “soát hồ sơ”** | Giống digital publication / decision brief. | Giống CRM detail header trên ticket/case. |
| 13 | **Zoom S00 (`?page=s00`)** | (Canonical không có “zoom metadata card” làm sản phẩm.) | Một card metadata giữa biển trắng — reading flow chết: không có bước tiếp theo trong khung hình. |
| 14 | **Mobile first glance** | Vẫn phải thấy kết luận cốt lõi sớm. | Stack label/value admin chiếm gần hết first screen — không có signal quyết định. |
| 15 | **Cognitive path** | Kết luận → xác nhận → đào sâu. | Xác minh hệ thống → (scroll) → mới được kết luận. |

---

# GROUP 3 — Visual Hierarchy

| # | Điểm khác | Canonical | UI hiện tại |
|---|-----------|-----------|-------------|
| 16 | **Hero strategy** | Có điểm nhấn thị giác lớn cho kết luận (stem / grade / cụm Executive). | S00 cố tình “không Hero” theo Spec hẹp — nhưng vô tình **không có Hero nào thay thế ở first fold**, chỉ còn strip. |
| 17 | **Scale typography** | Chữ kết luận (Nhật Chủ / giá trị chính) vượt xa caption. | Trong S00, tên và mã chỉ lớn hơn label một bậc — không có “display” của lá số. |
| 18 | **Accent usage** | Accent dẫn mắt tới quyết định / identity. | Accent chủ yếu cho **nav active**, **avatar**, **status badge** — tín hiệu hệ thống, không tín hiệu mệnh lý. |
| 19 | **Card weight** | Card phục vụ nhóm ý nghĩa (identity, pillars, strength…). | S00 = một “info bar card” giống toolbar record. |
| 20 | **Competing titles** | Một tiêu đề khu vực đọc chính rõ. | “Kết Quả Bát Tự” + “S00 — Context Header (Zoom)” + labels field — nhiều khung chữ ngang hàng, không có một hero message. |
| 21 | **Badge semantics** | Badge hỗ trợ mức độ / trạng thái điều kiện lá số. | Badge “Hoàn tất (mock)” = pipeline status — đúng ops, sai product reading. |

---

# GROUP 4 — Information Density

| # | Điểm khác | Canonical | UI hiện tại |
|---|-----------|-----------|-------------|
| 22 | **“Nhiều thông tin nhưng không rối”** | Nhiều *tín hiệu có nghĩa* (stem, trụ, thân, dụng/kỵ, presence) xếp theo tầng. | S00 có nhiều *field* nhưng ít *ý nghĩa lá số* — mật độ ký tự cao, mật độ insight thấp. |
| 23 | **Giá trị mỗi pixel first fold** | Mỗi khối trả lời một câu hỏi quyết định. | Pixel đầu trang trả lời audit trail (version, analyzedAt). |
| 24 | **Cảm giác “trống nhưng nghèo”** | Whitespace bao quanh nội dung giàu. | Zoom S00: whitespace lớn bao quanh một card metadata — cảm giác template CRM trống. |
| 25 | **Secondary grids (Thập Thần / Thần Sát)** | Presence chips sau khi đã có kết luận — dense có kiểm soát. | Chưa phải lỗi S00 trực tiếp, nhưng Result hiện tại vẫn xếp “dashboard modules” sau strip — dễ lặp pattern card-grid thay vì reading chapters. |
| 26 | **Duplicate information** | Canonical tránh lặp vô ích giữa tầng. | `chartId` + `fullName` xuất hiện ở PageWrapper **và** S00 — tốn chỗ không tăng quyết định. |

---

# GROUP 5 — Whitespace

| # | Điểm khác | Canonical | UI hiện tại |
|---|-----------|-----------|-------------|
| 27 | **Chức năng khoảng trắng** | Tách *tầng đọc* (summary / pillars / analysis). | Tách *field trong form* và padding quanh card admin. |
| 28 | **Rhythm dọc** | Nhịp chapter: Hero → Bát Tự → Phân tích → … | Nhịp CRM: Title → Meta card → Section card → … |
| 29 | **Alignment** | Cột trụ / glance metrics căn theo ý nghĩa đọc. | Label-above-value grid căn theo schema database. |
| 30 | **Empty canvas trên Zoom** | Canonical first screen luôn “đầy ý nghĩa”, không đầy field. | Phần lớn viewport Zoom S00 là nền xám trống — whitespace trang trí, không whitespace chức năng. |
| 31 | **Card padding vs content worth** | Padding lớn đi kèm nội dung quyết định. | Padding lớn đi kèm 6–7 metadata fields — cảm giác over-spaced form. |

---

# GROUP 6 — Navigation

| # | Điểm khác | Canonical | UI hiện tại |
|---|-----------|-----------|-------------|
| 32 | **Top Nav** | Điều hướng *sản phẩm* (vào Result / Báo cáo…). | Giống — nhưng không cứu được first content sai tầng. |
| 33 | **TOC là mục lục đọc** | Mục theo chương nội dung (Tóm tắt → Bát Tự → …). | Thêm “Ngữ cảnh” lên đầu → TOC trở thành mục lục *kỹ thuật trang*, không phải mục lục *ý nghĩa lá số*. |
| 34 | **TOC active = lời hứa first fold** | Active “Tóm tắt” hứa hẹn kết luận. | Active “Ngữ cảnh” hứa hẹn hồ sơ/meta. |
| 35 | **Sidebar density** | Ít mục, gắn journey. | Nhiều mục (Ngữ cảnh, Tóm tắt, Tổng quan, …) — dễ biến Result thành dashboard mục lục dài. |
| 36 | **Nav không thay Content Hierarchy** | Canonical: nav phục vụ; hierarchy nằm trong main. | UI hiện tại: đã có Canonical-ish shell (top nav + TOC) nhưng **main vẫn CRM** — copy khung, chưa copy não. |

---

# GROUP 7 — Decision Support

| # | Điểm khác | Canonical | UI hiện tại |
|---|-----------|-----------|-------------|
| 37 | **Định nghĩa Portal** | Decision Support Portal cho người xem lá số. | Đang hành xử như Case/Record Viewer. |
| 38 | **What / Why / Next** | Xuất hiện sớm (khuyến nghị, dụng/kỵ, grade). | S00 không trả lời What/Why/Next; thậm chí chiếm chỗ của chúng trên first fold. |
| 39 | **Condition (Thân)** | Nhìn thấy sớm trong hành trình quyết định. | Không có trong S00; user phải vượt metadata mới tới. |
| 40 | **Actionable language** | “Nên bổ… / hạn chế…” gắn kết luận. | “Chi tiết hồ sơ” / “Hoàn tất (mock)” — action của hệ thống, không action của cuộc sống. |
| 41 | **Trust through meaning** | Tin vì hiểu lá số. | Tin vì status pipeline xanh — niềm tin ops, không niềm tin mệnh lý. |
| 42 | **S00 đúng Spec hẹp nhưng sai Product** | Context có thể tồn tại, nhưng **không được thay First Meaning**. | Spec strip được implement như *mở màn chính* — đúng chữ Spec, sai tinh thần Canonical + IA First Viewport. |

---

# GROUP 8 — Commercial Quality

| # | Điểm khác | Canonical | UI hiện tại |
|---|-----------|-----------|-------------|
| 43 | **Demo khách hàng 10 giây** | “Ồ — đây là tôi (Bính), đánh giá, bước tiếp.” | “Ồ — đây là ticket BZ-… đã hoàn tất.” |
| 44 | **Demo đối tác / investor** | Cảm giác product trí tuệ + commercial SaaS reading. | Cảm giác internal tool / back-office. |
| 45 | **Ảnh tạo niềm tin hơn** | `CANONICAL_PORTAL_UI.png` — vì first fold = chuyên môn Bát Tự. | `01_desktop_full.png` / `02_desktop_zoom_s00.png` — vì first fold = hồ sơ kỹ thuật. |
| 46 | **Premium signal** | Density có kiểm soát + hierarchy kết luận. | Clean component ≠ premium nếu nội dung mở đầu là audit fields. |
| 47 | **`(mock)` trên status** | Canonical bán niềm tin sản phẩm. | “Hoàn tất (mock)” phá commercial frame ngay first glance. |

---

# GROUP 9 — What Should NOT Be Copied

Từ `CANONICAL_PORTAL_UI.png` / tham chiếu — **không** copy máy móc:

| # | Không copy | Vì sao |
|---|------------|--------|
| 48 | **Bảng màu exact (blue/green cụ thể trên ảnh)** | Design System BTE đã có token; clone màu = fake Canonical. |
| 49 | **Font trên ảnh** | Dùng typography tokens của Design System. |
| 50 | **Icon set / minh họa trên ảnh** | Không import icon pack chỉ vì ảnh có; không trang trí thay hierarchy. |
| 51 | **Mọi card/shadow pixel-perfect** | Clone skin; không học reading. |
| 52 | **Cân Xương trong Identity Zone A** | IA Freeze v1.1 đã loại khỏi Zone A — ảnh có thể cũ hơn luật. |
| 53 | **Nhồi mọi widget cùng một màn “dashboard wallpaper”** | Canonical dạy tầng lớp, không dạy nhồi chart. |
| 54 | **Hard-code layout HTML của ảnh** | Phải map sang Component Library hiện có. |

---

# GROUP 10 — What MUST Be Learned

Bắt buộc học từ Canonical (không phải copy skin):

| # | Phải học | Ý nghĩa vận hành |
|---|----------|------------------|
| 55 | **Reading Flow** | First seconds = hiểu lá số, không hiểu database row. |
| 56 | **Information Hierarchy** | Kết luận → cấu trúc → phân tích → luận giải → kiến thức. |
| 57 | **Progressive Disclosure** | Không phơi admin meta như tầng 1. |
| 58 | **Hero Strategy** | Phải có điểm nhấn *ý nghĩa* trên first fold (Identity/Decision), không Hero trang trí, cũng không “anti-hero metadata”. |
| 59 | **Decision Support** | What / Why / Next phải sống sớm trong journey. |
| 60 | **Commercial Reading Experience** | Portal đọc như brief tư vấn, không như admin console. |
| 61 | **Whitespace chức năng** | Tách chương ý nghĩa, không “card nhỏ giữa sa mạc”. |
| 62 | **TOC = mục lục nội dung** | Không biến TOC thành index của technical chrome. |
| 63 | **Shell ≠ Soul** | Top nav + sidebar Canonical-ish vẫn FAIL nếu main content là CRM. |
| 64 | **Spec tuân thủ ≠ Product đúng** | Làm đúng checklist field S00 nhưng đặt sai vai trò trên journey vẫn REJECT. |

---

## Count

Tài liệu liệt kê **64 điểm so sánh / học hỏi cụ thể** (vượt yêu cầu tối thiểu 30), nhóm theo 10 Group PO yêu cầu.

---

# LESSONS LEARNED

## 1. Bạn đã hiểu sai điều gì?

Đã hiểu Canonical như bài toán **Component correctness** (strip, Badge, Avatar, field list, responsive stack) và **Spec field checklist**.

Thực tế Canonical là bài toán **Reading Experience**: trong vài giây đầu, người dùng phải *hiểu lá số để quyết định*, không phải *xác minh record kỹ thuật*.

Đã tối ưu “S00 là gì theo Spec”, chưa tối ưu “First Viewport làm gì theo triết lý Portal”.

## 2. Vì sao UI vừa rồi bị REJECT?

Không vì React/CSS kém.

Vì **first fold biến Portal thành CRM/Admin detail header**:

- Metadata trước, kết luận sau  
- TOC dẫn vào “Ngữ cảnh”  
- Visual accent cho status hệ thống  
- Khoảng trắng lớn quanh card ít giá trị quyết định  
- Không trả lời Who / Strong-Weak / What-Why-Next trong 5 giây  

Đúng kỹ thuật component — sai sản phẩm Decision Support.

## 3. Bạn sẽ thay đổi tư duy thiết kế như thế nào?

Trước khi vẽ/section:

1. Hỏi: **User question trong 5 giây là gì?**  
2. Hỏi: Khối này thuộc **Meaning** hay **System chrome**?  
3. Hỏi: Có đang làm Dashboard/CRM không?  
4. Chỉ sau đó mới map Component Library.

Spec section vẫn cần — nhưng **vai trò trong journey** quan trọng hơn checklist field.

## 4. Bạn sẽ thiết kế Portal khác Dashboard ở điểm nào?

| Dashboard / CRM | Portal Bát Tự |
|-----------------|---------------|
| Record identity trước | Chart meaning trước |
| Status pipeline nổi | Condition / Decision nổi |
| Label–value schema | Conclusion → evidence |
| Nhiều module ngang hàng | Tầng đọc tuần tự |
| TOC = danh mục widget | TOC = chương nội dung |
| Thành công = data hiển thị đủ | Thành công = quyết định nhanh hơn |

## 5. Bạn sẽ đảm bảo các Section sau không lặp lại lỗi này bằng cách nào?

Gate trước mọi section (kể cả khi Spec PASS):

1. **5-second test** — screenshot first fold: trả lời được Who / Strong-Weak / What-Why-Next chưa?  
2. **Anti-CRM test** — nếu bỏ hết Nhật Chủ/Thân/Decision mà trang vẫn “trông xong”, là đang làm sai.  
3. **Hierarchy test** — field hệ thống không được thắng visual weight của kết luận.  
4. **TOC test** — mục active có khớp ý nghĩa đọc không?  
5. **PO philosophy check** — viết 5 dòng *Design Intent* (reading) trước khi code; PO confirm intent trước implement.  
6. **STOP rule** — không implement section tiếp nếu intent chưa PASS (như lần này).

---

# STOP

```
Không thiết kế lại S00
Không React · CSS · HTML · Component · Wireframe · Mockup
Chờ Product Owner xác nhận đã hiểu đúng Canonical Portal
Chỉ sau xác nhận mới được phép thiết kế lại S00
```

---

## Related

- `UI_CHANGELOG.md` — UI-015 S00 → **REJECT (philosophy)**  
- `PORTAL_SCREEN_SPECIFICATIONS.md` — vẫn là Spec; cần đọc lại *vai trò journey*, không chỉ field list  
- `CANONICAL_PORTAL_INFORMATION_ARCHITECTURE.md` — First Viewport = S00 strip **+** S01 Zones A–C (S00 không được một mình thay First Meaning)
