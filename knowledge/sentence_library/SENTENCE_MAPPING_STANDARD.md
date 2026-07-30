# Sentence Mapping Standard

**Document:** SENTENCE_MAPPING_STANDARD  
**Module:** knowledge/sentence_library  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define how Sentence IDs map to Knowledge Assets, Rules, and References.

---

## Mapping Targets

| Target | ID Pattern | Field |
|--------|------------|-------|
| Knowledge | `KNO-NNNNNN` | Knowledge Links |
| Rules | `RUL-NNNNNN` | Rule Links |
| References | `REF-NNNNNN` | Reference Links |

---

## Mapping Principles

1. **Rule/Knowledge first** — prefer grounding in `RUL-*` and `KNO-*`
2. **Explicit variables** — every `{placeholder}` appears in Variables
3. **Empty over fake** — do not invent IDs
4. **Condition alignment** — Conditions SHOULD match linked rule intent when Rule Links exist
5. **Frozen sources** — do not edit Knowledge Canon / Rule Database / Reference documents to force links

---

## Domain Guidance (Non-Normative)

| Sentence Domain | Typical Knowledge / Rule Domains |
|-----------------|----------------------------------|
| strength / temperature | strength, temperature, season |
| five_elements / stems / branches | foundations domains |
| ten_gods / patterns / useful_gods | matching doctrinal domains |
| combinations | combination / clash related domains |
| shensha | shensha |
| luck_cycles | luck cycles |
| special_cases | cross-domain |

---

## Conflict Resolution

If two Official sentences collide for the same condition set:

1. Prefer higher Confidence with stronger Evidence
2. Otherwise prefer earlier Official ID
3. Deprecate or narrow the losing sentence
4. Record decision in Revision History

---

## Framework Phase Note

V1.0.0 creates no populated mapping rows.
