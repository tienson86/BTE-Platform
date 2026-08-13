# COMMERCIAL QA — CASE_0001 / CASE_0002 / CASE_0003

Date: 2026-08-13  
Method: Production pipeline → Commercial HTML/PDF  
Exports: `knowledge/report_v1_validation/exports/commercial_v2/`

---

## Gate

Customer PDF must read like **one consulting report**, not three engines.

| Check | 0001 | 0002 | 0003 |
|-------|:----:|:----:|:----:|
| Pipeline success | PASS | PASS | PASS |
| Cover consulting (not engine dump) | PASS | PASS | PASS (parent cover) |
| Identity chapter | PASS | PASS | PASS (development / parent) |
| Career chapter | PASS | PASS | **omitted** (correct) |
| Executive chapter | PASS | PASS | PASS (parent executive) |
| Legacy tables (Tứ Trụ / ngũ hành / thân / dụng thần / thần sát) | none | none | none |
| Rule IDs / theme IDs / hide markers | none | none | none |
| Customer appendix | none | none | none |
| Theme Library class | Người tự gánh | Người ra kết quả + FOLLOW_FRAME | Parent Context; adult class not on cover |
| Reads as one consultant | PASS | PASS | PASS |

---

## CASE_0001

| Item | Result |
|------|--------|
| Subject | Nguyễn Tiến Sơn |
| Theme | `OPERATING_SELF_CARRY` → **Người tự gánh** |
| Chapters | identity, career, executive |
| Opening | “Tôi là ai?” — tự gánh, tự đẩy tiến độ, việc khó vẫn còn mặt để xử lý |
| Voice | One consultant; no strength-score table; no pillar dump |
| Verdict | **Commercial consulting** |

---

## CASE_0002

| Item | Result |
|------|--------|
| Subject | Hoàng Thị Thu Phương |
| Theme | `OPERATING_OUTPUT` + overlay `FOLLOW_FRAME` → **Người ra kết quả** |
| Chapters | identity, career, executive |
| Opening | Identity around visible output / result — not CASE_0001 self-carry copy |
| Voice | Same report family as 0001, different consulting class |
| Verdict | **Commercial consulting** (generalization holds) |

---

## CASE_0003

| Item | Result |
|------|--------|
| Subject | 2015 child |
| Product Context | `life_stage=CHILD`, parent delivery |
| Cover | **Báo cáo đồng hành phụ huynh** |
| Identity | “Nhận diện phát triển” — phụ huynh đọc, không tự quyết người lớn |
| Career | **Not printed** |
| Executive | Parent priorities: học tập / tự tin / bảo toàn |
| Verdict | **Uses Parent Context** |

---

## Residual language (CLL, not Report Engine)

Executive close may still say “các miền đã có dữ liệu” / “luận vận trình chưa sẵn sàng” — Commercial Language Layer freeze. Not an engine dump. Not modified in this migration.

---

## Advisor Mode (not in the three customer cases)

Appendix appears only when `PACKAGE_D`, `reader_role=CONSULTANT`, or `options.advisor_mode`.  
CASE_0001/0002/0003 customer PDFs have **no appendix**.

END
