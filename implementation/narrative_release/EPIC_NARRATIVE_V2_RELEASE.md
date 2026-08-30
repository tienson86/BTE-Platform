# EPIC — NARRATIVE V2 RELEASE

Version: V1.0

Status: RELEASE PLAN

Owner: Product Owner

Module:

implementation/narrative_release/

---

# 1. Executive Summary

Epic này định nghĩa toàn bộ kế hoạch đưa Narrative V2 từ Shadow Mode sang Production.

Narrative Platform đã hoàn thành tại EPIC:

NARRATIVE V2 IMPLEMENTATION

Release Epic không xây thêm Runtime.

Release Epic không thêm Builder.

Release Epic không thay đổi Meaning.

Release Epic chỉ chịu trách nhiệm:

đưa Narrative Platform vào vận hành Production một cách an toàn.

---

# 2. Mission

Mục tiêu của Epic là:

Shadow

↓

Production

mà không ảnh hưởng khách hàng.

---

# 3. Release Objectives

Epic phải đạt:

✓ Portal Production Switch

✓ Dual Run Monitoring

✓ Pack05 Retirement

✓ Production Freeze

---

# 4. Out of Scope

Epic này không:

- sửa Astrology Engine
- sửa Rule Engine
- sửa Knowledge
- sửa Narrative Runtime
- thêm Builder
- thêm Language Assets

Narrative Platform được xem là hoàn chỉnh.

---

# 5. Release Philosophy

Release luôn theo nguyên tắc:

```
Certified

↓

Golden

↓

Shadow

↓

Production

↓

Monitoring

↓

Retirement

↓

Freeze
```

Không được bỏ bước.

---

# 6. Production Principles

Production phải luôn:

- an toàn;
- có thể rollback;
- có khả năng theo dõi;
- không làm gián đoạn khách hàng.

---

# 7. Release Roadmap

## N-REL-01

Portal Production Switch

---

## N-REL-02

Dual Run & Monitoring

---

## N-REL-03

Pack05 Retirement

---

## N-REL-04

Release Freeze

---

# 8. Release Gates

Narrative chỉ được Production khi:

✓ Technical PASS

✓ Product PASS

✓ Certification PASS

✓ Golden PASS

✓ Export PASS

---

# 9. Production Safety Rules

Không được Switch nếu:

- Golden FAIL
- Certification FAIL
- Regression FAIL
- Export Parity FAIL

---

# 10. Portal Switch Policy

Portal phải đọc:

NarrativeV2Presentation

Không được Compose.

Không được Rewrite.

Không được Join.

---

# 11. Dual Run Policy

Trong giai đoạn đầu:

Pack05

↓

Production

Narrative V2

↓

Shadow

↓

Monitoring

Sau khi ổn định:

Narrative V2

↓

Production

Pack05

↓

Shadow

---

# 12. Monitoring Policy

Theo dõi:

- Runtime failures
- Serialization failures
- Presentation mismatches
- Export parity
- Regression differences

Không ghi dữ liệu nhạy cảm.

---

# 13. Rollback Strategy

Nếu Production xảy ra lỗi:

Portal

↓

Pack05

↓

Rollback

Rollback phải thực hiện được nhanh chóng và không làm mất dữ liệu phân tích.

---

# 14. Pack05 Retirement Policy

Pack05 chỉ được Retirement khi:

✓ Narrative V2 Production ổn định

✓ Không còn Regression

✓ Product Owner phê duyệt

✓ Rollback window kết thúc

---

# 15. Freeze Policy

Sau Release Freeze:

- Không sửa Runtime
- Không sửa Presentation Contract
- Không sửa Export Contract

Mọi thay đổi tiếp theo thuộc phiên bản mới.

---

# 16. Runtime Ownership

Narrative Runtime là nguồn duy nhất tạo Narrative.

Portal chỉ Render.

PDF chỉ Render.

DOCX chỉ Render.

JSON chỉ Serialize.

---

# 17. Single Source of Truth

Nguồn duy nhất của mọi Consumer:

NarrativeV2Presentation

Không Consumer nào được tự sinh Narrative.

---

# 18. Release Metrics

Theo dõi:

- Successful analyses
- Shadow success rate
- Export parity
- Runtime stability
- Rollback count

---

# 19. Acceptance Criteria

Epic chỉ PASS khi:

✓ Portal dùng Narrative V2

✓ Pack05 không còn Production

✓ Golden Dataset ổn định

✓ Narrative Studio vẫn hoạt động

✓ Export Parity đạt 100%

---

# 20. Success Metrics

Thành công khi:

- Portal Production = Narrative V2
- PDF/DOCX/JSON dùng cùng Presentation
- Không còn phụ thuộc Pack05
- Không có Narrative Regression ngoài Golden

---

# 21. Sprint Deliverables

Mỗi Sprint phải có:

- Code
- Tests
- Runtime verification
- Screenshots
- Completion Report
- Rollback verification

---

# 22. Risk Matrix

| Rủi ro | Biện pháp |
|--------|-----------|
| Portal lỗi | Rollback về Pack05 |
| Regression | Golden compare |
| Export sai | Export parity |
| Runtime lỗi | Shadow monitor |

---

# 23. Release Governance

Không Sprint nào được bỏ qua:

- Product Review
- Certification
- Golden Verification

---

# 24. Release State Machine

```
Certified

↓

Golden

↓

Shadow

↓

Production

↓

Monitoring

↓

Pack05 Retired

↓

Freeze
```

Không được nhảy trạng thái.

---

# 25. Rollback Matrix

| Trạng thái | Có Rollback |
|------------|:-----------:|
| Shadow | ✓ |
| Production | ✓ |
| Monitoring | ✓ |
| Pack05 Retired | Chỉ khi chưa Freeze |
| Freeze | ✗ |

---

# 26. Version Policy

Release không thay đổi:

Narrative Version.

Release chỉ thay:

Deployment State.

---

# 27. Documentation Policy

Specification:

đóng băng.

Implementation:

đóng.

Release:

quản lý.

---

# 28. Release Reports

Tên chuẩn:

```
N_REL_01_REPORT.md

N_REL_02_REPORT.md

N_REL_03_REPORT.md

N_REL_04_REPORT.md
```

---

# 29. Exit Criteria

Epic kết thúc khi:

- Narrative V2 Production hoàn chỉnh
- Pack05 Retirement hoàn tất
- Freeze hoàn tất

---

# 30. Final Release Principle

Implementation tạo ra Platform.

Release đưa Platform đến khách hàng.

Không có Release tốt thì Platform tốt cũng không tạo ra giá trị.

Narrative V2 chỉ thực sự hoàn thành khi:

- khách hàng đang sử dụng Narrative V2 trong Production;
- Pack05 đã được Retirement an toàn;
- toàn bộ Consumer cùng đọc một `NarrativeV2Presentation`;
- hệ thống có thể vận hành, giám sát và rollback một cách tin cậy.

Đó là mục tiêu cuối cùng của EPIC Narrative V2 Release.

---

# 31. Release Decision Authority

Release Engineering không chỉ quy định **làm gì**, mà còn quy định **ai có quyền quyết định**.

Mọi thay đổi trạng thái của Narrative V2 đều phải có thẩm quyền rõ ràng.

Không được phép:

- tự động chuyển Production;
- tự động Retirement Pack05;
- tự động Freeze;
- tự động Certification.

Những quyết định này luôn cần sự phê duyệt của con người.

---

## Decision Authority Matrix

| Quyết định | Người có quyền | Ghi chú |
|------------|----------------|---------|
| Narrative Studio Review | Reviewer được chỉ định | Đánh giá chất lượng Narrative |
| Certification | Product Owner | Chỉ Product Owner được CERTIFY |
| Golden Promotion | Product Owner | Chỉ Narrative đã CERTIFIED mới được Promote |
| Portal Production Switch | Product Owner | Sau khi hoàn thành toàn bộ Release Gates |
| Rollback Production | Product Owner hoặc Technical Lead | Có thể kích hoạt ngay khi phát hiện lỗi nghiêm trọng |
| Pack05 Retirement | Product Owner | Chỉ sau khi Narrative V2 Production ổn định |
| Release Freeze | Product Owner | Đóng phiên bản Production |

---

## Automatic Decisions

Hệ thống được phép tự động:

- chạy Validation;
- chạy Test Suite;
- chạy Regression;
- tạo Hash;
- tạo Export;
- kiểm tra Golden Parity;
- sinh báo cáo Release.

Hệ thống **không được phép tự động**:

- CERTIFY;
- Promote lên Golden;
- Switch Production;
- Retirement Pack05;
- Freeze Release.

---

## Human Approval Principle

Các quyết định sau luôn cần phê duyệt trực tiếp:

- Narrative Certification
- Golden Promotion
- Production Switch
- Rollback
- Pack05 Retirement
- Release Freeze

Không AI, Script hay Automation nào được quyền thay thế người phê duyệt.

---

## Four-Eyes Principle

Đối với các thay đổi Production quan trọng, áp dụng nguyên tắc **Four-Eyes Principle**:

1. Technical Lead xác nhận hệ thống đạt yêu cầu kỹ thuật.
2. Product Owner xác nhận Narrative đạt yêu cầu sản phẩm.
3. Chỉ khi cả hai điều kiện đều đạt, Release mới được phép tiếp tục.

Điều này giảm rủi ro phát hành sai hoặc bỏ sót lỗi quan trọng.

---

## Emergency Rollback Authority

Trong trường hợp Production xảy ra lỗi nghiêm trọng:

- Technical Lead có quyền kích hoạt Rollback ngay để bảo vệ hệ thống.
- Product Owner phải được thông báo và xác nhận sau khi hệ thống đã được đưa về trạng thái an toàn.

Rollback luôn ưu tiên:

Ổn định hệ thống

↓

Bảo vệ khách hàng

↓

Điều tra nguyên nhân

Không được trì hoãn Rollback chỉ để chờ phê duyệt nếu khách hàng đang bị ảnh hưởng.

---

## Audit Trail

Mọi quyết định Release phải được lưu lại:

- Decision ID
- Quyết định
- Người thực hiện
- Người phê duyệt
- Thời gian
- Phiên bản Narrative
- Phiên bản Presentation
- Ghi chú

Audit Trail là append-only.

Không được chỉnh sửa lịch sử.

---

## Separation of Responsibilities

Để bảo đảm tính minh bạch:

- Developer triển khai kỹ thuật.
- Reviewer đánh giá Narrative.
- Product Owner quyết định phát hành.
- Technical Lead chịu trách nhiệm vận hành và Rollback.

Không một cá nhân nào tự mình thực hiện toàn bộ chuỗi:

Implementation

↓

Certification

↓

Production Switch

↓

Freeze

---

## Final Authority Principle

Release Engineering không chỉ bảo vệ hệ thống bằng công nghệ.

Release Engineering còn bảo vệ hệ thống bằng **quy trình và trách nhiệm rõ ràng**.

Một Narrative chỉ được phép đến tay khách hàng khi:

- chất lượng đã được kiểm chứng;
- quy trình đã được hoàn thành;
- người có thẩm quyền đã chính thức phê duyệt.

Đó là nguyên tắc quản trị cao nhất của EPIC Narrative V2 Release.