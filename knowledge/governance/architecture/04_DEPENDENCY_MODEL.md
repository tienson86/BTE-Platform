# Dependency Model

## Purpose

Define dependency relationships among all governance assets.

---

# Dependency Hierarchy

```
Reference

↓

Terminology

↓

Knowledge

↓

Rules

↓

Sentence Library

↓

Interpretation

↓

Report

↓

Golden Dataset
```

---

# Dependency Rules

References have no upstream dependency.

Terminology depends on References.

Knowledge depends on Terminology.

Rules depend on Knowledge.

Sentences depend on Rules.

Interpretation depends on Sentences.

Reports depend on Interpretation.

---

# Forbidden Dependencies

Reports SHALL NOT directly depend on References.

Sentence Library SHALL NOT bypass Rules.

Circular dependencies are prohibited.

---

# Dependency Validation

Every dependency SHALL be:

Registered

Traceable

Versioned

Validated