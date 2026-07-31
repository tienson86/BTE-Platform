# BTE Knowledge Consistency Framework

**Sprint:** 4F  
**Location:** `knowledge/consistency/`  
**Status:** Specification only (no runtime consistency engine)

---

## Purpose

Guarantee that every Knowledge Record is **semantically consistent** across definitions, terminology, ontology, relationships, cross-references, and dependencies.

---

## Folder tree

```text
knowledge/consistency/
├── README.md
├── consistency_rules.json
├── cross_record_validation.json
├── terminology_consistency.json
├── ontology_consistency.json
├── relationship_consistency.json
├── canonical_definition_rules.json
├── CONSISTENCY_REPORT.md
└── examples/
    └── consistency_findings_example.json
```

---

## Validation dimensions

| Dimension | Primary spec |
|-----------|----------------|
| Canonical Definition uniqueness | `canonical_definition_rules.json` + CON-001/002 |
| Terminology consistency | `terminology_consistency.json` |
| Ontology consistency | `ontology_consistency.json` |
| Relationship consistency | `relationship_consistency.json` |
| Cross references | `cross_record_validation.json` XR-003 |
| Dependency integrity | CON-010/011 + dependency specs |
| Duplicate definitions | CON-012 + XR-006 + DEF-005 |
| Contradictions | CON-013/014 + XR-007 + DEF-006 |

Master rule list: `consistency_rules.json` (CON-001…015).

---

## Pass policy

- **ERROR** count MUST be 0 for Consistency PASS.
- **WARNING** MAY remain (e.g. planned KR targets).
- No automated scanner ships in Sprint 4F; structural validation of this folder is required.

Report: [CONSISTENCY_REPORT.md](CONSISTENCY_REPORT.md)

---

## Related

- `knowledge/graph/` — ontology & graph constraints
- `knowledge/dependency/` — dependency levels
- `knowledge/index/` — canonical/alias/xref indexes
- `knowledge/manifest/` — discovery manifests
- `knowledge/quality/` — quality scorecards
- `knowledge/authoring/ANTI_PATTERNS.md` — common mistakes

---

## Out of scope

- Implementing a consistency checker binary
- Mutating Knowledge Records to “fix” findings
- Changing golden datasets or snapshots
