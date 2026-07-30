# Knowledge Mapping Standard

**Document:** KNOWLEDGE_MAPPING_STANDARD  
**Module:** knowledge/knowledge_canon  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define how Knowledge Assets map to Terminology, References, Rules, Sentences, and related Knowledge Assets.

---

## Mapping Targets

| Target | ID Pattern | Asset Field |
|--------|------------|-------------|
| Related Knowledge | `KNO-NNNNNN` | Relationships |
| Terminology | `TERM-NNNNNN` | Terminology Links |
| References | `REF-NNNNNN` | Reference Links |
| Rules | Rule IDs per module conventions | Rule Links |
| Sentences | Sentence IDs per module conventions | Sentence Links |

---

## Mapping Principles

1. **Explicit links only** — no implied mapping by filename
2. **Stable IDs only** — map to allocated identifiers
3. **Empty over fake** — do not invent target IDs
4. **Minimal necessary** — link what traceability requires
5. **Bidirectional when Official** — related Knowledge SHOULD reciprocate
6. **Frozen modules** — do not edit Reference or Terminology documents to force links

---

## Domain Guidance (Non-Normative)

| Knowledge Domain | Typical Terminology Domains | Typical Reference Use |
|------------------|-----------------------------|------------------------|
| five_elements / yin_yang | five_elements, basic | Classics foundations |
| heavenly_stems / earthly_branches / hidden_stems | matching stem/branch domains | Classics foundations |
| ten_gods | ten_gods | Zi Ping classics |
| strength / temperature / seasonal_qi | strength | Di Tian Sui / Qiong Tong / Zhen Quan |
| patterns / useful_gods | patterns, useful_gods | Zhen Quan / Di Tian Sui |
| combinations / clashes / punishments / harms / transformations | matching relation domains | Combination classics |
| shensha | shensha | San Ming Tong Hui et al. |
| luck_cycles | fortune | Luck-related sources |
| special_cases | glossary / basic | Mixed |

---

## Conflict Resolution

If two Official Knowledge Assets collide:

1. Prefer earlier Official ID when possible
2. Deprecate the later duplicate
3. Update Relationships and domain INDEX
4. Record decision in Revision History

---

## Framework Phase Note

V1.0.0 creates no populated mapping rows. These rules apply when content is added later.
