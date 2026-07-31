# Anti-Patterns

**Document:** ANTI_PATTERNS  
**Version:** 1.0.0  
**Status:** Specification

Common mistakes when writing Knowledge Records. Do not do these.

---

## Academic

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| Inventing classical quotations or `SRC-*` IDs | Bibliography integrity / honesty | Use real sources or `TODO_REVIEW` |
| Multiple competing “canonical” definitions | Consistency / compiler mapping | One definition + scoped notes |
| Smuggling engine scoring rules into definition | Wrong responsibility | Keep definition academic; rules in Rule KR / rule DB |
| Marking contested claims `confidence=high` | Traceability / golden gates | Lower confidence or `TODO_REVIEW` |
| Using alias phrases as Canonical Name | Terminology / indexes | Keep Canonical Name; list aliases |

---

## Identity & naming

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| Reusing or remapping `KR-*` | Immutable Record ID | New concept → new ID; deprecate old |
| Two files claiming the same Canonical Name | Unique canonical node | One KR; alias the rest |
| Spaces / unstable filenames | Tooling / indexes | `KR-NNNNNN_CANONICAL_KEY.md` |
| Local ID schemes (`FND-only` as public KR id) | Global ID policy | Planning IDs ≠ published `KR-*` |

---

## Relationships & ontology

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| Inventing edge type names (`SUPPORTS`, `based_on`) | Ontology integrity | Use approved codes (`SUPPORTED_BY`, …) |
| Dependency cycles on foundation edges | Graph constraint | Fix direction or split concepts |
| Duplicate relationship triples | Relationship integrity | One edge; merge notes |
| Everything is `RELATED_TO` | Weak graph semantics | Prefer precise types |
| Pack/Module as substitute for Concept identity | Ontology rules | Organizational nodes ≠ concept nodes |

---

## Examples & tests

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| Treating examples as golden expected outputs | Testing rules / immutability | Keep examples pedagogical |
| Editing snapshots so a KR “passes” | Golden dataset policy | Fix content or accept draft status |
| Example without parent `KR-*` | Traceability | Set parent record id |

---

## Process & governance

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| Self-approving official promotion | Separation of duties | Governance Owner + reviews |
| Publishing without freeze | Release / freeze policy | Freeze then release |
| Editing frozen academic text without `CR-*` | Freeze policy | Change request + re-review |
| Skipping technical review because “academic is fine” | Review workflow | Both required (unless waived with rationale) |
| Expanding one KR into two concepts | Maintainability | Split into two `KR-*` |

---

## Template misuse

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| Leaving `{{PLACEHOLDERS}}` in submitted drafts | Completeness | Replace or `TODO_REVIEW` |
| Editing shared template files as if they were records | Template integrity | Copy template → new file |
| Filling golden overlay without type template | Golden checklist | Complete type template first |
