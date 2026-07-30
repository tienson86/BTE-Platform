# Registry Identifier Standard

> **Document ID:** REG-ID-001
>
> **Version:** V1.0.0
>
> **Status:** Official
>
> **Document Type:** Identifier Standard

---

# 1. Purpose

This specification defines the identifier standard for all Registry Records managed by the BTE Registry.

Registry identifiers uniquely identify metadata records rather than the canonical business objects themselves.

---

# 2. Principles

Registry identifiers shall be:

- Globally Unique
- Immutable
- Machine Readable
- Human Readable
- Namespace Independent
- Version Independent

---

# 3. Identifier Format

```
REG-000001
```

General format

```
PREFIX-SEQUENCE
```

---

# 4. Registry Prefixes

| Prefix | Description |
|---------|-------------|
| REG | Generic Registry Record |
| GREG | Global Registry |
| KREG | Knowledge Registry |
| RREG | Rule Registry |
| SREG | Sentence Registry |
| TREG | Terminology Registry |
| DREG | Dataset Registry |
| PREG | Report Registry |
| REFREG | Reference Registry |

---

# 5. Registry Identity

Each Registry Record shall contain:

- Registry ID
- Object ID
- Namespace
- Object Type

Registry ID never changes.

---

# 6. Allocation Rules

Identifiers are allocated only by the Registry Service.

Manual assignment is prohibited.

---

# 7. Reserved Ranges

```
000001–099999

Core Registry

100000–499999

Domain Registry

500000–899999

Future Expansion

900000–999999

Testing
```

---

# 8. Validation

Validators verify:

- Duplicate Registry IDs
- Invalid prefixes
- Invalid sequence
- Namespace mismatch

---

# 9. Merge Policy

Merged Registry Records preserve:

- Original Registry ID
- Audit History
- Traceability

---

# 10. Compliance

Every Registry Record shall have exactly one immutable Registry ID.