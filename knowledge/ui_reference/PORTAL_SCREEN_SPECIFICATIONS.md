# BTE Platform V1.0

# Portal Screen Specifications

---

## Document Information

| Item | Value |
|------|-------|
| Document | Portal Screen Specifications |
| Version | **1.0 — PO Review** |
| Status | **AWAITING PRODUCT OWNER APPROVAL** |
| Scope | Result page sections S00 → Learning Panel |
| Depends On | `CANONICAL_PORTAL_INFORMATION_ARCHITECTURE.md` **v1.1 APPROVED / Architecture Freeze** |
| Also follows | `CANONICAL_PORTAL_UI.md`, `UI_DESIGN_PRINCIPLES.md` |
| Owner | Product Owner |
| Implementation | **NONE yet** — Specification only. No React / CSS / Component code until Spec PASS + section-by-section open |

---

## Purpose

Tài liệu đặc tả chính thức để triển khai từng màn hình / section của Portal Result.

- **Không** đổi thứ tự Section (IA đã Freeze).
- **Không** đổi Reading Flow / Decision Journey.
- **Không** viết React / CSS / HTML.
- Mọi UI sau này phải map 1:1 vào đặc tả này.

---

## Global Rules

1. Tuân thủ IA Freeze v1.1: `S00 → S01 → S02 → S03 → S04 → S05 → S06 → S07 → S08 → Learning Panel (on demand)`.
2. Chỉ dùng Design System + Component Library hiện có (khi triển khai sau này).
3. Progressive Disclosure: First Viewport = S00 strip + S01 Zones A–C.
4. Một section / một vòng: Design → Screenshot → PO Review → PASS → mới mở section tiếp.
5. Primary Components dưới đây = **loại component được phép dùng** (tên concept), không phải lệnh tạo component mới.

---

## Screen Flow (Frozen)

```
S00 Context Header
↓
S01 Identity & Decision Panel
↓
S02 Chart Overview
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
Learning Panel (Drawer / Accordion / Side Panel — on demand)
```

---

# S00 — Context Header

## 1. Business Goal

Xác nhận người dùng đang xem **đúng hồ sơ / đúng lần phân tích** trước khi đọc Identity & Decision.

S00 là **context strip**, không phải Navigation, không phải Hero, không phải Identity.

## 2. User Question

> “Tôi đang xem lá số nào? Đúng hồ sơ và phiên bản phân tích của tôi chứ?”

## 3. Required Data

| Field | Description |
|-------|-------------|
| `profileDisplayName` | Họ tên hồ sơ đang xem |
| `chartId` | Mã lá số |
| `createdAt` | Ngày / thời điểm lập lá số |
| `analysisStatus` | Trạng thái (Hoàn tất / Đang xử lý / Lỗi…) |
| `analysisVersion` | Phiên bản phân tích (engine / interpretation label) |
| `analyzedAt` | Thời điểm phân tích |

## 4. Optional Data

| Field | Description |
|-------|-------------|
| `avatar` / initials | Nhận diện nhanh |
| `gender` | Giới tính (ngắn) |
| `birthSummary` | Ngày·giờ sinh rút gọn (một dòng) |
| `ruleDatabaseVersion` | Version rule DB |
| Light actions | Link phụ (ví dụ “Chi tiết hồ sơ”) — **không** CTA lớn PDF/In |

## 5. Primary Components

- Context strip / bar (layout surface)
- Text (caption / body)
- Badge (status)
- Optional Avatar
- Optional text link (secondary)

## 6. Layout Rules

- Desktop: **một dải ngang**, chiều cao thấp (strip), luôn **phía trên S01**.
- Không dùng visual weight của Hero / Identity (không stem lớn, không Decision Support).
- Không lặp nội dung Zone A của S01 (Nhật Chủ / Ngũ Hành / Âm Dương).
- Metadata kỹ thuật dài → đẩy sang S02 nếu cần.

## 7. Responsive Rules

| Viewport | Rule |
|----------|------|
| Desktop | 1 hàng; fields có thể wrap nhẹ |
| Tablet | 1–2 hàng compact; ưu tiên tên · mã · status |
| Mobile | Compact block 2–3 dòng tối đa; không chiếm nửa màn hình |

## 8. Acceptance Criteria

- [ ] Luôn render trước S01 trong DOM/reading order.
- [ ] Người dùng xác nhận được đúng hồ sơ trong ≤ 3 giây.
- [ ] Không bị nhầm với Primary Nav hoặc Identity Panel.
- [ ] Status + chartId luôn visible trên Desktop strip.
- [ ] Không chứa Dụng/Hỷ/Kỵ, Thập Thần, Luận giải, Tứ Trụ.

## 9. Out of Scope

- Navigation / TOC
- Identity (Nhật Chủ…)
- Decision Support
- PDF / Print / Share primary CTAs (thuộc S02 nếu có)
- Engine / API wiring (chỉ định nghĩa field)

---

# S01 — Identity & Decision Panel

## 1. Business Goal

Giúp người dùng **đưa ra quyết định sơ bộ** về lá số — không phải “báo cáo tóm tắt kỹ thuật”.

Trả lời thương mại: tôi là ai → mạnh/yếu → quan trọng nhất / vì sao / làm gì tiếp.

## 2. User Question

> “Tôi là ai? Lá số mạnh hay yếu? Điều gì quan trọng nhất, vì sao, và tôi nên làm gì tiếp?”

## 3. Required Data

### Zone A — Identity

| Field | Description |
|-------|-------------|
| `dayMaster` | Nhật Chủ (Heavenly Stem của trụ Ngày) |
| `dayMasterElement` | Ngũ Hành Nhật Chủ |
| `yinYang` | Âm / Dương |

### Zone B — Condition

| Field | Description |
|-------|-------------|
| `strengthLabel` | Nhãn Thân Vượng / Nhược / Trung hòa… |
| `strengthLevel` | Mức độ ngắn (Mạnh / Yếu / …) |
| `overallGrade` | Đánh giá tổng quan (grade / verdict ngắn) |

### Zone C — Decision Support

| Field | Description |
|-------|-------------|
| `whatMattersMost` | Điều gì quan trọng nhất? |
| `whyItMatters` | Vì sao? |
| `whatToDoNext` | Tôi nên làm gì tiếp? |
| `usefulGod` | Dụng Thần (input cho What/Why) |
| `favorableGod` | Hỷ Thần |
| `unfavorableGod` | Kỵ Thần |

## 4. Optional Data

| Field | Description |
|-------|-------------|
| `avatar` | Avatar / initials cạnh Identity |
| `dayMasterHint` | Phụ đề ngắn (vd. “Hỏa · Dương”) |
| `pattern` | Cách Cục — khi Engine/mock có |
| `confidence` | Độ tin cậy Condition |
| `linkToInterpretation` | Lối sang S08 |

**Forbidden in Zone A:** Cân Xương Đoán Mệnh và mọi metric đo lường phụ cạnh tranh Nhật Chủ.

## 5. Primary Components

- Panel / Card surface (Identity & Decision container)
- Display text hierarchy (largest = Nhật Chủ)
- Badge (condition / grade)
- Structured Decision Support block (What / Why / Next) — có thể dùng Stack + Text + Card
- Optional Avatar
- Optional Chip/Badge cho Dụng·Hỷ·Kỵ như *input labels*, không thay What/Why/Next

## 6. Layout Rules

- Cùng First Viewport với S00 trên Desktop chuẩn: **S01 Zones A→B→C không yêu cầu scroll** để đọc hết quyết định cốt lõi.
- Thứ tự nội bộ cố định: **A → B → C**.
- Nhật Chủ = tín hiệu thị giác lớn nhất trong S01.
- Zone C phải trả lời đủ 3 câu What/Why/Next — **không** chỉ một dòng khuyến nghị.
- Dụng/Hỷ/Kỵ/Cách Cục hỗ trợ Zone C; không thay thế Zone C.
- Không nhúng Tứ Trụ / Thập Thần / Thần Sát / luận giải dài.

## 7. Responsive Rules

| Viewport | Rule |
|----------|------|
| Desktop | A (identity nổi) + B + C trong một panel liên tục; đủ trong fold cùng S00 |
| Tablet | A→B→C xếp gọn theo chiều dọc; vẫn cùng thứ tự |
| Mobile | Stack A rồi B rồi C; ưu tiên A+B trước fold nếu màn hình rất ngắn; C ngay bên dưới |

## 8. Acceptance Criteria

- [ ] Người mới trả lời được 4 câu hỏi thương mại trong ~5–15 giây (không cần scroll Desktop).
- [ ] Zone A không chứa Cân Xương.
- [ ] Zone C có đủ What / Why / Next (không chỉ recommendation one-liner).
- [ ] Không có Thần Sát / Thập Thần / Tứ Trụ chi tiết trong S01.
- [ ] Reading order khớp IA: sau S00, trước S02.

## 9. Out of Scope

- Chart structure (S03)
- Element Balance charts (S04)
- Full Strength narrative (S05)
- Interpretation long-form (S08)
- Learning content
- API / Engine calculation rules

---

# S02 — Chart Overview

## 1. Business Goal

Bổ sung **bối cảnh & thao tác** khi S00 chỉ là strip tối thiểu — không thay S00, không thay S01, không thay S03.

## 2. User Question

> “Tôi cần xem thêm thông tin hồ sơ hoặc thao tác (xuất / làm lại) không?”

## 3. Required Data

| Field | Description |
|-------|-------------|
| Extended profile fields không nằm trong S00 | Ví dụ nơi sinh, lịch âm đầy đủ… |
| Analysis metadata mở rộng | Rule DB version, interpretation version… |
| Structure teaser (optional one-liner) | Không phải Tứ Trụ đầy đủ |

## 4. Optional Data

| Field | Description |
|-------|-------------|
| Actions | Xuất PDF, In, Chia sẻ, Phân tích lại (có thể disabled đến Integration) |
| Cân Xương | Nếu Product muốn hiển thị — **ở đây hoặc Learning**, không ở S01-A |
| Links | Hồ sơ / lịch sử |

## 5. Primary Components

- Card / Section container
- Property grid / definition list
- Button group (secondary/ghost) cho actions
- Divider

## 6. Layout Rules

- Đứng **sau S01**, **trước S03**.
- Không lặp lại nguyên xi S00 (tránh duplicate chartId/status trừ khi cần “chi tiết”).
- Không thay thế Identity & Decision.
- Actions không được leo lên First Viewport nếu làm phình S00/S01.

## 7. Responsive Rules

| Viewport | Rule |
|----------|------|
| Desktop | Grid 2 cột cho metadata; actions một hàng |
| Tablet | Grid 2→1 |
| Mobile | Stack; actions full-width hoặc wrap |

## 8. Acceptance Criteria

- [ ] Không trùng vai trò S00 (context strip) hay S01 (decision).
- [ ] Không hiển thị matrix Tứ Trụ đầy đủ (thuộc S03).
- [ ] Actions (nếu có) rõ trạng thái enabled/disabled.
- [ ] Có thể compact nếu PO quyết định gộp phần lớn vào S00 — nhưng thứ tự IA không đổi.

## 9. Out of Scope

- Four Pillars matrix
- Decision Support What/Why/Next
- Report Engine PDF generation logic
- Authentication

---

# S03 — Four Pillars

## 1. Business Goal

Trình bày **xương sống cấu trúc** lá số: Năm · Tháng · Ngày · Giờ; củng cố Nhật Chủ đã thấy ở S01.

## 2. User Question

> “Bốn trụ ra sao? Nhật Chủ nằm ở đâu trong cấu trúc?”

## 3. Required Data

Per pillar (`year` | `month` | `day` | `hour`):

| Field | Description |
|-------|-------------|
| `label` | Năm / Tháng / Ngày / Giờ |
| `heavenlyStem` | Thiên Can |
| `earthlyBranch` | Địa Chi |
| `hiddenStems` | Tàng Can (list) |
| `naYin` | Nạp Âm |
| `twelveStage` | Trường Sinh |

Day pillar phải gắn nhận diện **Nhật Chủ** (khớp S01-A).

## 4. Optional Data

| Field | Description |
|-------|-------------|
| Ten God on pillar | Thập Thần theo trụ (preview) |
| Element color token | Hint ngũ hành (qua Design System — không hard-code theme mới) |
| Tooltip explanations | Thuật ngữ ngắn; chi tiết → Learning Panel |

## 5. Primary Components

- Section header
- 4× pillar panels (Card / article)
- Text hierarchy (stem/branch lớn hơn meta)
- Badge / Chip (hidden stems)
- Tooltip (optional)

## 6. Layout Rules

- Thứ tự cột cố định: Năm → Tháng → Ngày → Giờ.
- Trụ Ngày được nhấn mạnh (border / label “Nhật Chủ”) — không phá reading order.
- Không nhúng Decision Support hay luận giải dài.
- Không biến thành bảng Thập Thần toàn cục (S06).

## 7. Responsive Rules

| Viewport | Rule |
|----------|------|
| Desktop | 4 cột |
| Tablet | 2×2 |
| Mobile | 1 cột xếp dọc (Năm→…→Giờ) |

## 8. Acceptance Criteria

- [ ] Đủ 4 trụ với stem/branch tối thiểu.
- [ ] Trụ Ngày nhận diện được là Nhật Chủ và khớp S01.
- [ ] Không horizontal scroll trên mobile.
- [ ] Đứng sau S02, trước S04.

## 9. Out of Scope

- Element Balance chart (S04)
- Strength gauge full (S05)
- Full Ten Gods grid (S06)
- Interpretation prose

---

# S04 — Element Balance

## 1. Business Goal

Giúp người dùng hiểu **mức độ cân bằng** ngũ hành — *cân hay lệch, lệch về đâu* — không phải checklist kỹ thuật 5 hàng.

## 2. User Question

> “Ngũ hành của tôi cân bằng hay lệch? Lệch hướng nào?”

## 3. Required Data

| Field | Description |
|-------|-------------|
| `balanceVerdict` | Cân / Lệch nhẹ / Lệch mạnh… |
| `dominantElements` | Hành nổi (1–2) |
| `weakElements` | Hành yếu / thiếu (1–2) |
| `distribution` | Giá trị tương đối từng hành (score hoặc %) để hỗ trợ verdict |

## 4. Optional Data

| Field | Description |
|-------|-------------|
| Short note | 1–2 câu giải thích cân bằng |
| Link “Học Ngũ Hành” | Mở Learning Panel topic |
| Visual bars | Biểu diễn phân bố (ScoreBar / Progress) — phục vụ *balance*, không thay verdict |

## 5. Primary Components

- Section header + balance verdict (Badge / Text)
- ChartFrame or ScoreBar/ProgressBar for distribution
- Short note Text
- Optional link control to Learning Panel

## 6. Layout Rules

- Tiêu đề / framing = **Element Balance**, không “danh sách Five Elements”.
- Verdict cân/lệch phải đọc được trước khi đọc từng hành.
- Có thể đặt cạnh S05 trên Desktop (cùng hàng cơ chế) nhưng vẫn là section logic riêng, order S04 trước S05.
- Không luận giải dài (S08).

## 7. Responsive Rules

| Viewport | Rule |
|----------|------|
| Desktop | Có thể 50% width cạnh S05 |
| Tablet / Mobile | Full width; xếp trên S05 |

## 8. Acceptance Criteria

- [ ] User trả lời được “cân hay lệch?” mà không cần hiểu hết thuật ngữ.
- [ ] Không chỉ liệt kê 5 hành thiếu verdict cân bằng.
- [ ] Không chứa Decision Support What/Why/Next (đã ở S01-C).
- [ ] Order: sau S03, trước S05.

## 9. Out of Scope

- Useful/Hated god decision copy (S01-C / S08)
- Strength scale primary narrative (S05)
- Ten Gods / ShenSha grids
- Theme / new chart library

---

# S05 — Strength

## 1. Business Goal

Chi tiết hóa **Thân Vượng / Nhược** đã preview ở S01-B — tăng niềm tin vào Condition.

## 2. User Question

> “Kết luận Thân có vững không? Chi tiết mức độ ra sao?”

## 3. Required Data

| Field | Description |
|-------|-------------|
| `score` / `maxScore` | Điểm thân |
| `label` | THÂN VƯỢNG / NHƯỢC / … |
| `level` | Mức độ |
| `summary` | Mô tả ngắn các yếu tố chính |

## 4. Optional Data

| Field | Description |
|-------|-------------|
| `confidence` | Độ tin cậy |
| Factor list | Yếu tố ảnh hưởng (ngắn) |
| Scale labels | Nhược · Trung hòa · Vượng |

## 5. Primary Components

- Card / Section
- ProgressBar or ScoreBar
- Badge (label / level)
- Body text (summary)
- Optional factor list

## 6. Layout Rules

- Phải **khớp hướng** với S01-B (không mâu thuẫn mạnh/yếu).
- Desktop có thể cạnh S04; mobile dưới S04.
- Không thay Decision Support; không checklist Thần Sát.

## 7. Responsive Rules

| Viewport | Rule |
|----------|------|
| Desktop | Có thể cặp với S04 |
| Tablet / Mobile | Full width stack |

## 8. Acceptance Criteria

- [ ] Score + label + summary hiển thị khi status ready.
- [ ] Đồng bộ ngữ nghĩa với S01-B.
- [ ] Loading / empty / error có gate rõ.
- [ ] Order: sau S04, trước S06.

## 9. Out of Scope

- Recalculation rules / Engine
- Full interpretation
- Element balance verdict ownership (S04)

---

# S06 — Ten Gods

## 1. Business Goal

Secondary analysis: tín hiệu **Thập Thần** — hữu ích nhưng không bắt buộc cho quyết định First Viewport.

## 2. User Question

> “Thập Thần nào nổi bật hoặc vắng?”

## 3. Required Data

| Field | Description |
|-------|-------------|
| List of ten gods | id, name, presence (or count), optional strength |

## 4. Optional Data

| Field | Description |
|-------|-------------|
| Score / bar | Mức độ |
| Short description | Preview |
| Collapse state default | Nếu không có điểm nổi bật → mặc định thu gọn |

## 5. Primary Components

- Section / Card
- Presence grid or list (Chip / Badge / row)
- Optional ScoreBar
- Collapse / Accordion control (nếu áp dụng behaviour thu gọn)

## 6. Layout Rules

- Sau S05, trước S07; Desktop có thể cặp ngang với S07.
- Không leo vào First Viewport.
- Không thay S01 Decision Support.

## 7. Responsive Rules

| Viewport | Rule |
|----------|------|
| Desktop | 2 cột grid presence; có thể 50% cạnh S07 |
| Tablet | Full width |
| Mobile | 1 cột; collapse khuyến nghị khi ít tín hiệu |

## 8. Acceptance Criteria

- [ ] Presence/absence (hoặc count) đọc được nhanh.
- [ ] Không chặn reading flow chính.
- [ ] Có trạng thái thu gọn khi không có điểm nổi bật (theo behaviour).
- [ ] Order đúng IA.

## 9. Out of Scope

- Full relationship engine explanations
- Interpretation long-form
- Learning Pack full articles (→ Learning Panel)

---

# S07 — ShenSha

## 1. Business Goal

Secondary: **Thần Sát** đáng chú ý — tín hiệu phụ cát/hung.

## 2. User Question

> “Có Thần Sát nào tôi nên biết không?”

## 3. Required Data

| Field | Description |
|-------|-------------|
| ShenSha items | name, present/absent/unknown |

## 4. Optional Data

| Field | Description |
|-------|-------------|
| Tone (cát/trung/hung) | Nhãn ngắn |
| Note | Placeholder / giải thích ngắn |
| Legend | ✓ / × / ? |
| Default collapsed | Khi không có item quan trọng |

## 5. Primary Components

- Card / Section
- Presence grid
- Badge
- Legend text
- Collapse control

## 6. Layout Rules

- Sau S06, trước S08.
- Không First Viewport.
- Không chiếm không gian lớn nếu empty/unimportant → thu gọn.

## 7. Responsive Rules

| Viewport | Rule |
|----------|------|
| Desktop | Có thể cặp với S06 |
| Mobile | Stack; collapse ưu tiên |

## 8. Acceptance Criteria

- [ ] User phân biệt được có / không / chưa xác định.
- [ ] Empty/unimportant → không phình layout.
- [ ] Không chứa luận giải dài.
- [ ] Order đúng IA.

## 9. Out of Scope

- Pattern Engine full rules
- Identity / Decision
- Knowledge essays

---

# S08 — Interpretation

## 1. Business Goal

Đưa **ý nghĩa đời sống và khuyến nghị đầy đủ** — sâu hơn Zone C; kết thúc hành trình quyết định chính trước Learning.

## 2. User Question

> “Ý nghĩa đầy đủ là gì? Tôi nên làm gì tiếp — bản chi tiết?”

## 3. Required Data

| Field | Description |
|-------|-------------|
| `summary` | Tóm tắt luận giải |
| `bodySections` | Các đoạn luận (list) |
| `recommendations` | Khuyến nghị / hành động tiếp theo |

## 4. Optional Data

| Field | Description |
|-------|-------------|
| Cross-links | Neo về Dụng/Kỵ / S01-C |
| CTA | Xuất báo cáo / lưu (disabled đến Integration nếu cần) |
| Reading progress | Optional |

## 5. Primary Components

- Section container (reading width)
- Text blocks / paragraphs
- Optional Accordion for long parts
- Button (secondary) CTAs
- Divider

## 6. Layout Rules

- Sau secondary (S06/S07); trước Learning Panel (on demand).
- Chia đoạn ngắn — không một khối văn bản đặc.
- Mở rộng What/Why/Next của S01-C; không mâu thuẫn.
- Không nhét Knowledge Pack đầy đủ (→ Learning).

## 7. Responsive Rules

| Viewport | Rule |
|----------|------|
| Desktop | Max reading width; khoảng trắng tốt |
| Tablet / Mobile | Full width; typography đọc được; không horizontal scroll |

## 8. Acceptance Criteria

- [ ] Có summary + ít nhất một recommendation rõ.
- [ ] Dễ scan (đoạn ngắn / subheads).
- [ ] Đồng bộ hướng với S01-C.
- [ ] Không thay Context/Identity.

## 9. Out of Scope

- Interpretation Engine templates implementation
- PDF binary generation
- Auth / paywall
- Full glossary (Learning Panel)

---

# Learning Panel

## 1. Business Goal

Cung cấp **kiến thức / thuật ngữ theo yêu cầu** — Progressive Disclosure. Không phải section cuối bắt buộc trong reading flow chính.

## 2. User Question

> “Thuật ngữ này nghĩa là gì? Tôi muốn học thêm điểm nào?”

## 3. Required Data

| Field | Description |
|-------|-------------|
| `topics[]` | id, title, short explanation |
| `defaultOpen` | false |

## 4. Optional Data

| Field | Description |
|-------|-------------|
| Deep links | Tới Knowledge Pack / KR ids (sau này) |
| Context-sensitive topic | Mở đúng term từ S01/S03… |
| Search within panel | Optional V1.1+ |

## 5. Primary Components

- Drawer **or** Accordion **or** Side Learning Panel (chọn 1 pattern chính khi implement — Spec cho phép cả ba)
- Topic list + detail Text
- Close control
- Optional trigger links from sections (“Học thêm: Nhật Chủ”)

## 6. Layout Rules

- **Mặc định đóng.**
- Mở bằng TOC “Học thêm” hoặc link trong section.
- Không đẩy S08 xuống thành “phải đọc Knowledge mới xong”.
- Không dùng full-page blocking section như S09 cũ.

## 7. Responsive Rules

| Viewport | Rule |
|----------|------|
| Desktop | Drawer cạnh / side panel / accordion trong main |
| Tablet | Drawer hoặc accordion |
| Mobile | **Bottom sheet** hoặc full-screen overlay đóng được |

## 8. Acceptance Criteria

- [ ] Mặc định không chiếm reading flow.
- [ ] Mở/đóng rõ ràng; focus trap nếu overlay (a11y khi implement).
- [ ] Có ít nhất các topic nền: Nhật Chủ, Thân, Dụng Thần, Ngũ Hành / Element Balance.
- [ ] Không bắt buộc scroll hết trang để thấy Learning.

## 9. Out of Scope

- Full Knowledge Pack CMS
- Multi-language authoring
- Changing IA order back to trailing Knowledge section

---

# Cross-Cutting Requirements

## Loading / Empty / Error

Mỗi section (S00–S08) khi implement phải hỗ trợ gate:

- Loading
- Empty
- Error (message không leak secrets)

Learning Panel: empty topics → thông báo ngắn.

## Accessibility (spec-level)

- Thứ tự focus = reading order
- Section landmarks / headings
- Touch target đủ khi có control
- Không chỉ dựa vào màu để presence ✓/×

## Consistency

- Cùng Design System tokens
- Không invent theme/color system
- Copy tiếng Việt commercial, rõ ràng với người mới

---

# Review & Implementation Gate

```
Specification PO Review
        ↓
PASS / PASS WITH CHANGES / REJECT
        ↓ (only if PASS)
Open S00 UI design only
        ↓
Screenshot → Review → PASS
        ↓
Open S01
        ↓
…
        ↓
All sections PASS → Portal UI Freeze → Sprint 01.5 Integration
```

**Không** triển khai nhiều section cùng lúc.

---

# STOP

Portal Screen Specifications **v1.0** sẵn sàng cho Product Owner.

```
Không triển khai S00
Không React · CSS · Component
Chờ phê duyệt Specification
```
