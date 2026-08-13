# SECTION_MAPPING

| Field | Value |
|-------|-------|
| Maps | Theme blocks → customer features |

CLL section titles stay as they are. This file only says **which block feeds which section**.

---

## Identity Report

| Identity section (customer) | Block |
|-----------------------------|--------|
| Tôi là ai / WHO | `identity` |
| Mẫu vận hành | `identity` + operating stance |
| Điểm mạnh | `growth` (as strength-in-class) |
| Biên / điểm mù | `stress` (limit, not shame) |
| Áp lực | `stress` |
| Môi trường hợp | `environment` |
| Việc nên điều chỉnh | `action` |
| Tóm tắt danh tính | `memory` |

---

## Career Report

| Career section | Block |
|----------------|--------|
| Làm việc tốt nhất | `career` |
| Môi trường nghề | `environment` |
| Tư thế vai trò | `career` + `leadership` |
| Áp lực công việc | `stress` |
| Cân bằng trong việc | `action` (theme-gated) |
| Rủi ro nghề | `stress` + `career` never |
| Trọng tâm / tránh | `action` |
| Tóm tắt hướng sự nghiệp | `memory` (career dress) |

CONSERVING overlay: Career `memory` / `action` = stop-list, not output-week.

---

## Executive Consulting

| Executive section | Block |
|-------------------|--------|
| Bạn là ai | `identity` |
| Hệ vận hành | operating theme |
| Hỗ trợ / giới hạn | `growth` / `stress` |
| Insight | `memory` (insight dress) |
| Ưu tiên / tránh | `action` |
| Kết luận | `memory` |

TENSION_HOLDER overlay: insight + conclusion must keep **both** published lines.

---

## Future / optional features

| Feature | Blocks |
|---------|--------|
| Relationship (when sold) | `relationship` |
| Growth / development (adult) | `growth` |
| Parent / child (Product Context) | same blocks, audience rewrite — **not this library** |
| Share card | `memory` + `short` |

Do not invent Relationship doctrine. Block is a *stance slot* for when a claim plan exists.

---

## Leak gates

| From theme | Must not appear in |
|------------|-------------------|
| OPERATING_OUTPUT memory | BALANCE_DIRECTION or CONSERVING closes |
| “Vòng ra kết quả” as default | SELF_CARRY / STANDARDS / CONSERVING |
| “Bạn mạnh hơn khi…” | CONSERVING any section |
| Empty “khung lá số” | Any Memory |

---

END
