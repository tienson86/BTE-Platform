# Validation Rules (Compiler)

**Document:** validation_rules  
**Module:** `knowledge/tools/record_builder`  
**Version:** V1.0.0  

---

## 1. Scope

Rules applied during Knowledge Record compilation.  
No records are validated in this preparation sprint.

---

## 2. Severity

| Level | Effect |
|-------|--------|
| ERROR | Block Official output |
| WARNING | Allowed in Draft only if policy permits |
| INFO | Reported; non-blocking |

---

## 3. Schema validation

- Validate against `knowledge/schema/knowledge_record.schema.json`
- Apply module overlay schema when the target module requires it
- Missing required keys = ERROR
- `additionalProperties` violations = ERROR
- Invalid `KNO-` / status / version patterns = ERROR

---

## 4. Reference validation

- Every `references[].reference_id` MUST exist in Foundation `references.json`
- `title` SHOULD match Foundation `title_english` (mismatch = WARNING)
- Invented `REF-*` = ERROR
- Empty `references` on Official academic claims = ERROR (Draft may WARNING)

---

## 5. Relationship validation

- Target `knowledge_id` MUST exist before Official (or be explicitly deferred with ERROR for Official)
- `relationship_type` MUST be non-empty
- Canon link-only concepts MUST NOT be duplicated as new BaZi Official records
- Circular dependencies require Academic justification (WARNING → Review)

---

## 6. Terminology validation

- Canonical labels SHOULD align with Foundation glossary
- Unknown terms = WARNING until Terminology registration

---

## 7. Integrity validation

- No duplicate `knowledge_id` across corpus
- Planning ID bound to at most one Knowledge ID
- `metadata.schema_version` MUST be `1.0.0` (base const)
- `validation.*` flags must reflect actual gate results (lying flags = ERROR)

---

## 8. Output validation

- Output path authorized (`knowledge_records/` for Official module writes)
- File name matches agreed slug convention
- Compilation report completed
- No academic fields filled by compiler heuristics

---

## 9. Gate order

1. Input verification  
2. Field mapping completeness  
3. Schema validation  
4. Reference validation  
5. Relationship validation  
6. Integrity validation  
7. Output validation  
