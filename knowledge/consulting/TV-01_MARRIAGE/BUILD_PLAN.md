# TV-01 — MARRIAGE CONSULTING
# BUILD_PLAN.md

Document ID: TV-01-BUILD

Version: 1.0

Status: FROZEN

---

# 1. Purpose

Tài liệu này định nghĩa kế hoạch triển khai (Build Plan) của TV-01.

Mọi Build Phase phải tuân thủ:

COMMON Framework

TV-01 Specifications

IMPLEMENTATION_CONTRACT.md

Build Plan

Build Plan là tài liệu điều phối Implementation.

---

# 2. Build Philosophy

Không triển khai toàn bộ TV-01 trong một lần.

Triển khai theo từng Build Phase.

Mỗi Phase phải:

PASS

↓

Freeze

↓

mới sang Phase tiếp theo.

---

# 3. Global Rules

Không sửa COMMON.

Không sửa Canonical Mathematics.

Không Duplicate Engine.

Không Hard-code.

Không Skip Validation.

Không Skip Tests.

---

# 4. Phase Overview

TV1-B01

Project Skeleton

TV1-B02

Runtime Integration

TV1-B03

Marriage Decision Policy

TV1-B04

Recommendation Integration

TV1-B05

Report Profile

TV1-B06

Public API

TV1-B07

UI Layout

TV1-B08

Testing

TV1-B09

Acceptance

---

# 5. TV1-B01

Objective

Thiết lập Skeleton.

Deliverables

Folders

Interfaces

Dependency Injection

Contracts

PASS

Build PASS

Type PASS

No Runtime

STOP

Không viết Business Logic.

---

# 6. TV1-B02

Objective

Kết nối Runtime.

Deliverables

Canonical

↓

Decision

PASS

Runtime PASS

Decision Pipeline PASS

STOP

Không viết Recommendation.

---

# 7. TV1-B03

Objective

Marriage Decision Policy.

Deliverables

Marriage Policy

Decision Profile

PASS

Decision PASS

STOP

Không viết Report.

---

# 8. TV1-B04

Objective

Recommendation.

Deliverables

Action Model

Recommendation Runtime

PASS

Recommendation PASS

STOP

Không viết Narrative.

---

# 9. TV1-B05

Objective

Report Profile.

Deliverables

Customer Story

Sections

PASS

Report PASS

STOP

Không viết UI.

---

# 10. TV1-B06

Objective

Public API.

Deliverables

REST Resources

Contracts

PASS

API PASS

STOP

Không viết Mobile.

---

# 11. TV1-B07

Objective

UI Layout.

Deliverables

Customer Journey

Responsive Layout

PASS

UI PASS

STOP

Không Refactor Runtime.

---

# 12. TV1-B08

Objective

Testing.

Deliverables

Golden Dataset

Regression

Snapshots

PASS

Tests PASS

STOP

Không thay Decision.

---

# 13. TV1-B09

Objective

Acceptance.

Deliverables

Acceptance Report

Commercial Checklist

PASS

TV-01 PASS

---

# 14. Decision Gates

Gate 1

B01

↓

B02

Gate 2

B02

↓

B03

...

Không PASS.

↓

Không Build tiếp.

---

# 15. Build Deliverables

Mỗi Phase đều phải tạo:

Completion Report

Screenshot

Tests

PASS Report

Không chỉ Code.

---

# 16. Completion Criteria

Mỗi Phase chỉ hoàn thành khi:

Build PASS

Type PASS

Tests PASS

Architecture PASS

Implementation Contract PASS

Acceptance PASS

---

# 17. Final Goal

TV-01 hoàn thành khi:

B01

↓

B09

đều PASS.

Không có ngoại lệ.

---

# 18. Status

BUILD PLAN

STATUS

FROZEN