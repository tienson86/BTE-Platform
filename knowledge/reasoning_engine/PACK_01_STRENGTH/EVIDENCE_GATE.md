# Evidence Gate

| Field | Value |
|-------|-------|
| Document | EVIDENCE_GATE |
| Version | 1.0.0 |

---

# 1. Purpose

No knowledge unit proceeds into ranking unless evidence requirements are evaluated.

```text
Knowledge Unit
      ↓
Required Evidence Check
      ↓
PASS → eligible → Reasoning
FAIL → ineligible (reject)
PARTIAL → partially_supported (not a firm customer conclusion)
```

---

# 2. States

| State | Meaning | Customer Mode |
|-------|---------|---------------|
| `eligible` | All `required_facts` AVAILABLE with compatible polarity | May become a firm claim if salience/budget allow |
| `partially_supported` | Some required facts PARTIAL, or only optional facts present | Must not be written as a sure conclusion; qualify or Validation-only |
| `ineligible` | A required fact MISSING, or forbidden_condition true, or class mismatch | Reject |

`NOT_APPLICABLE` on a required fact → ineligible for that unit (the unit asked for a dimension that does not apply).

---

# 3. Rules

1. Drain units require drain AVAILABLE and not `inactive`.
2. Luck units require luck interaction AVAILABLE.
3. Deep-root units require published deep/multi-branch root, not “1 chi”.
4. Class-bound units require `strength_class` match unless `all` / `edge`.
5. `partially_supported` + purpose CONCLUSION → forbidden. Conclusion uses published classification only.
6. `partially_supported` + purpose RECOMMENDATION → drop from Customer Mode or demote to consideration in Validation.
7. Hidden stems MISSING does not make season/root units ineligible if those dimensions are AVAILABLE.

---

# 4. Absence is not a pass

Missing luck does not make a “luck has no effect” unit eligible.

Missing drain does not make “no leak, therefore Very Strong” eligible.

---

# 5. Output per unit

```text
gate_result
├── knowledge_id
├── state
├── missing_required[]
├── forbidden_hit[]
└── reason_code
```

---

END
