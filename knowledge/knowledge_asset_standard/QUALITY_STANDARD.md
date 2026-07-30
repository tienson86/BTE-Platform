# Quality Standard

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Quality Standard)

---

# 1. Purpose

This document defines measurable quality criteria for every Knowledge Asset.

---

# 2. Measurable Criteria

| Criterion | Focus |
|-----------|-------|
| Coverage | Declared categories, locales, and branches are populated |
| Consistency | No contradictory terms, priorities, mappings, or references |
| Traceability | Stable IDs and versioned references throughout |
| Maintainability | Clear ownership, metadata, and change history |
| Readability | Documentation and terminology are unambiguous |
| Extensibility | Additive extension without breaking V1.x contracts |
| Testability | Validation and golden datasets exist and pass |
| Integrity | Manifest and metadata match actual assets |

---

# 3. Quality Gates

Before publication:

1. Canonical model completeness
2. Type-specific schema completeness
3. Cross-reference integrity
4. Metadata / Manifest consistency
5. Validation dataset passage
6. Golden dataset passage where required
7. Review / approval passage

---

# 4. Defect Handling

Critical defects require quarantine or deprecation of the defective version, corrected republication, and consumer notification when compatibility is affected.

Runtime Engines shall not patch asset defects by hard-coding knowledge.

---

# 5. Acceptance Criteria

Quality standard is met when measurable criteria are evidenced and all mandatory gates pass.
