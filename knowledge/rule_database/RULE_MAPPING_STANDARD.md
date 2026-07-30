# Rule Mapping Standard

**Document:** RULE_MAPPING_STANDARD  
**Module:** knowledge/rule_database  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define how Rule IDs map to Knowledge Assets, Terminology, References, Sentences, and related rules.

---

## Mapping Targets

| Target | ID Pattern | Field |
|--------|------------|-------|
| Knowledge | `KNO-NNNNNN` | Knowledge Links |
| Terminology | `TERM-NNNNNN` | Terminology Links |
| References | `REF-NNNNNN` | Reference Links |
| Sentences | Sentence IDs | Sentence Links |
| Related Rules | `RUL-NNNNNN` | Related Rules |

---

## Mapping Principles

1. **Knowledge first** — prefer `KNO-*` links for doctrinal grounding
2. **Explicit over implied** — no filename-only mapping
3. **Empty over fake** — do not invent IDs
4. **Priority explicit** — conflicting related rules declare Priority
5. **Frozen sources** — do not edit Knowledge Canon / Terminology / Reference documents to force links
6. **Operational packs untouched** — do not rewrite existing `*_rules/` JSON in this phase

---

## Domain Guidance (Non-Normative)

| Rule Domain | Typical Knowledge Domains |
|-------------|---------------------------|
| strength / season / temperature | strength, seasonal_qi, temperature |
| patterns / useful_gods / ten_gods | patterns, useful_gods, ten_gods |
| combinations / clashes / transformations | combinations, clashes, transformations |
| shensha | shensha |
| luck_cycles | luck_cycles |
| special_cases | special_cases / cross-domain |

---

## Conflict Resolution

If two Official rules collide:

1. Prefer higher Priority when declared
2. Otherwise prefer earlier Official ID
3. Deprecate or narrow the losing rule
4. Record decision in Revision History

---

## Framework Phase Note

V1.0.0 creates no populated mapping rows.
