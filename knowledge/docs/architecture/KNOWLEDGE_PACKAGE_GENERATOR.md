# Knowledge Package Generator

| Field | Value |
|-------|-------|
| **Document** | KNOWLEDGE_PACKAGE_GENERATOR |
| **Version** | 1.0.0 |
| **Status** | Canonical Foundation reference |
| **Scope** | Specification only — no runtime |

Canonical files: `knowledge/generator/`

---

## 1. Role

The Knowledge Package Generator is the master specification used to produce every future Knowledge Package. It is not itself a package or a rule set.

```
Profile → Skeleton → Metadata → Manifest → Rules → Evidence → Reasoning
      → Examples → Tests → Validation → Documentation → RC → Released
```

---

## 2. Profile system

Required fields: `package_id`, `package_name`, `package_type`, `domain`, `taxonomy`, `ontology`, `target_rule_count`, `evidence_required`, `reasoning_required`, `example_required`, `validation_profile`, `quality_target`, `package_version`.

Inheritance: `GEN-PROFILE-COMMON` → `GEN-TYPE-*` → `GEN-INST-*`.

---

## 3. Quality

Bronze / Silver / Gold / Platinum, aligned with KD-4 plus evidence/reasoning completeness.

---

## 4. AI

Draft only. Human Technical + Domain + Release approval required. No engine or existing-package mutation.

---

## 5. Compatibility

Existing Knowledge Platform unchanged. Strength Core not modified. Engines, API, contracts untouched.

---

## 6. Related

- `knowledge/generator/KNOWLEDGE_PACKAGE_GENERATOR.md`
- `knowledge/package_spec/PACKAGE_SPECIFICATION.md`
- `knowledge/authoring/authoring_pipeline.md`
- `knowledge/reasoning/REASONING_FRAMEWORK.md`
