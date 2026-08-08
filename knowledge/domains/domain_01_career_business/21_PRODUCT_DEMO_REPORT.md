# 21 — Product Demo Report · Career Selection Assessment

Version: 1.0  
Status: **DEMO CAPTURE — D1-GC-STRONG-EMP**  
Date: 2026-08-08  
Capability: CAP-D1-CA-SEL  
Chart profile: Strong employee · Useful God Thủy · Pattern Chính Quan  

---

## 1. Purpose

Show customer-visible lift when Career Selection Assessment is wired into production Result content (same Result Page; no new screen).

---

## 2. Before → After

### 2.1 Executive Summary / Identity slot

| | Content |
|--|---------|
| **Before (Wave 1.1 identity)** | Bạn là người mang Nhật chủ Giáp trong cấu trúc Chính Quan. Ở mức thân được nâng đỡ, đây là danh tính cốt lõi để bám suốt buổi tư vấn… |
| **After (Career direction)** | Họ nghề hợp bạn: ưu tiên các nhóm việc nuôi Dụng thần Thủy trong khung Chính Quan. Hãy nghĩ theo họ nghề (chuyên môn; điều phối; phục vụ; sáng tạo; vận hành) chứ không ép một chức danh duy nhất… |

**Customer-visible improvement:** Identity becomes a **work-direction** answer (career families), not only chart identity.

### 2.2 Recommendation / Action slot

| | Content |
|--|---------|
| **Before (Wave 1.1 RC)** | Hành động: Trước hết giữ mực — giảm tải… ưu tiên các việc nuôi Dụng thần Thủy trong 2–4 tuần tới… |
| **After (Career 90-day plan)** | Kế hoạch 90 ngày: Tháng 1 — giữ mực và chọn một việc nhỏ nuôi Dụng thần Thủy… Tháng 2 — sâu hơn một năng lực/vai trò… Tháng 3 — rà soát… |

**Customer-visible improvement:** Generic useful-god action becomes a **structured 90-day career plan**.

### 2.3 Career Assessment (new projection on same page)

| Field | After (customer-facing) |
|-------|-------------------------|
| Working environment | Ưu tiên nơi nuôi Thủy, trách nhiệm rõ, tự chủ vừa sức… |
| Preferred role | Vai trò có đầu ra rõ trong khung Chính Quan… |
| Leadership posture | Lãnh đạo vs chuyên gia theo Thủy / Chính Quan — không ép chức danh quản lý… |
| Employment posture | Làm thuê hay độc lập neo vào Thủy; thử kênh nhỏ trước… |
| Strengths | Lợi thế nghề gắn Chính Quan + thân được nâng đỡ khi đi đúng Thủy… |
| Risks + Mitigation | Rủi ro lệch Thủy / quá rộng → giữ biên, thử 2–4 tuần, giảm phần kỵ… |
| Development + Timing | Một năng lực cốt lõi + bước nhỏ trong 90 ngày… |

---

## 3. Analytical meaning preserved

| Guard | Evidence |
|-------|----------|
| Interpretation baseline sections kept | Enrich append-only |
| Score analytical code preserved | `analytical_recommendation = Thủy` while commercial rec specializes |
| No new Result route / layout | Portal maps into existing S01/S08 slots |

---

## 4. Trace (demo chart)

11 SEL units: `KU-CN-CA-000001` … `KU-AC-CA-000001` → Bundle `status=complete` → `narrative_result.career_selection_assessment` → Portal adapters.

---

## 5. Stop line

Demo captured for Product Review. Do not expand to Promotion Readiness.

---

END
