# COMMON — CONSULTING FRAMEWORK

# 11_VERSIONING_STANDARD.md

**Document ID:** COMMON-11

**Product:** BTE Platform

**Module:** Consulting Framework

**Document Type:** Versioning Standard

**Status:** DRAFT FOR PRODUCT OWNER REVIEW

**Version:** 1.0

---

# 1. Purpose

Tài liệu này định nghĩa Versioning Standard của toàn bộ BTE Consulting Framework.

Versioning không chỉ dùng để đánh số phiên bản.

Versioning có nhiệm vụ:

- đảm bảo Decision có thể tái lập;
- đảm bảo Explainability;
- đảm bảo Audit;
- đảm bảo Backward Compatibility;
- đảm bảo Reproducibility.

---

# 2. Versioning Philosophy

Version không đại diện cho Source Code.

Version đại diện cho:

Behavior.

Nếu Behavior thay đổi.

↓

Version phải thay đổi.

Nếu chỉ Refactor.

↓

Version không đổi.

---

# 3. Versioning Principle

Framework phải luôn trả lời được:

Decision này được tạo bằng:

- Mathematics nào?
- Engine nào?
- Policy nào?
- Rule Catalog nào?
- Narrative nào?
- Renderer nào?

---

# 4. Version Bundle

Mỗi Decision đều phải mang theo:

Version Bundle.

Version Bundle là tập hợp toàn bộ Version đã tham gia tạo Decision.

---

# 5. Version Bundle Structure

Version Bundle tối thiểu gồm:

Canonical Version

Decision Mathematics Version

Decision Engine Version

Decision Policy Version

Evidence Model Version

Finding Model Version

Recommendation Model Version

Narrative Version

Report Version

Presentation Version

Validation Version

---

# 6. Canonical Version

Canonical Version gồm:

Calendar

BaZi

Strength

Pattern

Useful God

Luck

Ten Gods

Shen Sha

Nếu một Canonical Engine thay đổi.

↓

Canonical Version thay đổi.

---

# 7. Mathematics Version

Decision Mathematics có Version riêng.

Ví dụ.

decision.math.v1

decision.math.v2

Không phụ thuộc Engine.

---

# 8. Decision Engine Version

Decision Engine có Version riêng.

Ví dụ.

decision.engine.v1

Không đồng bộ bắt buộc với Mathematics.

---

# 9. Policy Version

Mỗi Policy có Version riêng.

Ví dụ.

marriage.policy.v1

career.policy.v2

partner.policy.v3

Policy thay đổi.

↓

Version thay đổi.

---

# 10. Evidence Version

Evidence Model có Version riêng.

Không phụ thuộc:

Policy.

---

# 11. Finding Version

Finding Model có Version riêng.

---

# 12. Recommendation Version

Recommendation Model có Version riêng.

---

# 13. Narrative Version

Narrative Catalog có Version riêng.

Narrative thay đổi.

↓

Version thay đổi.

Decision không đổi.

---

# 14. Report Version

Report Model có Version riêng.

Renderer không ảnh hưởng Report Version.

---

# 15. Presentation Version

Presentation Model có Version riêng.

Theme thay đổi.

↓

Presentation Version không đổi.

Chỉ Renderer thay đổi.

---

# 16. Validation Version

Validation Rules có Version riêng.

Điều này giúp Audit lại Decision cũ.

---

# 17. Renderer Version

Renderer có Version riêng.

Ví dụ.

pdf.renderer.v2

web.renderer.v5

Không ảnh hưởng Decision.

---

# 18. Semantic Versioning

Khuyến nghị sử dụng:

MAJOR.MINOR.PATCH

Ví dụ.

1.0.0

1.1.0

1.1.3

---

# 19. MAJOR

MAJOR tăng khi:

Behavior thay đổi.

Decision có thể thay đổi.

---

# 20. MINOR

MINOR tăng khi:

Thêm tính năng.

Không thay đổi Decision cũ.

---

# 21. PATCH

PATCH tăng khi:

Fix bug.

Không làm thay đổi hành vi đã công bố.

Nếu Patch làm thay đổi Decision.

↓

Không được dùng PATCH.

Phải dùng MAJOR.

---

# 22. Behavior Versioning

Framework Version theo:

Behavior.

Không theo:

Git Commit.

Không theo:

Build Number.

---

# 23. Reproducibility

Version Bundle phải đủ để chạy lại đúng Decision.

Năm 2035.

↓

Input cũ.

↓

Version Bundle cũ.

↓

Decision cũ.

---

# 24. Backward Compatibility

Framework phải ưu tiên:

Backward Compatibility.

Không được Silent Upgrade.

---

# 25. Forward Compatibility

Version mới

không được phá dữ liệu cũ.

Nếu cần Migration.

↓

Migration phải Explicit.

---

# 26. Version Lock

Một Consultation chỉ dùng:

Một Version Bundle.

Không được:

Half v1

Half v2

---

# 27. Runtime Freeze

Version Bundle được khóa ngay khi bắt đầu Runtime.

Không được đổi giữa chừng.

---

# 28. Version Explainability

Mọi Decision đều phải biết:

Version Bundle nào tạo ra nó.

---

# 29. Version Traceability

Decision

↓

Version Bundle

↓

Modules

↓

Behavior

↓

Source

---

# 30. Version Audit

Audit phải trả lời được:

Decision này khác Decision kia vì:

Mathematics?

Policy?

Narrative?

Renderer?

---

# 31. Version Independence

Narrative thay đổi.

↓

Decision không đổi.

Theme thay đổi.

↓

Presentation không đổi.

Renderer thay đổi.

↓

Report không đổi.

---

# 32. Version Registry

Framework nên có:

Version Registry.

Lưu toàn bộ:

Module

Version

Release Date

Compatibility

Status

---

# 33. Deprecation

Version cũ không xóa ngay.

Đánh dấu:

Deprecated.

Sau đó mới Remove.

---

# 34. Migration

Nếu Behavior thay đổi.

↓

Migration Guide bắt buộc.

---

# 35. Version Anti-patterns

Sai.

Silent Update.

Sai.

Unknown Version.

Sai.

Narrative Version ghi đè Decision Version.

Sai.

Renderer thay Decision.

---

# 36. Compatibility Matrix

Framework phải công bố:

Decision Mathematics

↓

Decision Engine

↓

Policy

↓

Narrative

↓

Compatibility.

---

# 37. Decision Identity

Một Decision được xác định bởi:

Input

+

Version Bundle

+

Decision Result.

Không chỉ bởi Input.

---

# 38. Consultation Identity

Consultation ID

khác

Version Bundle.

Một Consultation luôn tham chiếu tới đúng Version Bundle.

---

# 39. Release Policy

Mọi Release phải ghi rõ:

Behavior Changes

Compatibility

Migration

Breaking Changes

---

# 40. Freeze Conditions

COMMON-11 chỉ được FREEZE khi:

- [ ] Có Version Bundle.
- [ ] Có Semantic Versioning.
- [ ] Có Behavior Versioning.
- [ ] Có Reproducibility.
- [ ] Có Backward Compatibility.
- [ ] Có Runtime Freeze.
- [ ] Có Version Registry.
- [ ] Có Migration Policy.
- [ ] Có Compatibility Matrix.

---

# 41. Final Statement

Version không dùng để biết hệ thống đang ở phiên bản nào.

Version dùng để biết:

**Decision này được tạo ra bằng hệ thống nào.**

Đó là nền tảng của Explainability và Audit.

---

# 42. Status

COMMON-11

STATUS:

FREEZE READY

Next:

COMMON-12

ACCEPTANCE_STANDARD.md