# Pattern Knowledge Metadata Specification

**Module:** Pattern Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Metadata Specification)

---

# 1. Purpose

This document defines mandatory metadata and Manifest requirements for Pattern Knowledge.

---

# 2. Module Metadata

Mandatory fields:

- module_id
- domain
- version
- status
- owners
- consumers
- asset_inventory
- dependencies
- compatibility_matrix
- created / modified
- integrity_reference

---

# 3. Asset Metadata

Every asset shall include:

- author
- reviewer
- created
- modified
- version
- compatibility
- status
- references

---

# 4. Manifest Requirements

The Manifest shall index:

- all Rule Assets
- Decision Tables
- Mapping Tables
- Formula Library entries
- Priority Tables
- Terminology
- Reference Tables
- Examples
- Validation Datasets
- Golden Datasets
- Documentation
- Version Information
- Configuration profiles where declared

---

# 5. Dependency Metadata

Dependencies shall declare:

- Fundamental Knowledge compatibility range
- KMS / KAS compatibility
- Pattern Engine consumer compatibility range

---

# 6. Acceptance Criteria

Metadata and Manifest are accepted when complete, consistent, path-independent, and aligned with KAS.
