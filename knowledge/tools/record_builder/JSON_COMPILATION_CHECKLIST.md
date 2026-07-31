# JSON Compilation Checklist

**Document:** JSON_COMPILATION_CHECKLIST  
**Module:** `knowledge/tools/record_builder`  
**Version:** V1.0.0  

Complete in order. Do not skip gates.

---

## 0. Authorization

- [ ] Design Academic Review approved for this Planning ID  
- [ ] Ownership Resolved (not `TODO_REVIEW`)  
- [ ] Global `KNO-*` issued  
- [ ] Compilation authorized for target module path  
- [ ] Canon link-only concepts excluded from BaZi Official duplicate compile  

---

## 1. Input verification

- [ ] Design artifact path exists  
- [ ] Planning ID matches inventory  
- [ ] Required design sections present  
- [ ] No unauthorized academic invention markers ignored  
- [ ] Mapping sheet started (`RECORD_MAPPING_TEMPLATE.md`)  

---

## 2. Field mapping

- [ ] Identity mapped  
- [ ] Classification mapped  
- [ ] Definition mapped to string `definition`  
- [ ] Characteristics mapped to allowed keys only  
- [ ] Relationships mapped to typed slots  
- [ ] References mapped with `REF-*`  
- [ ] Metadata mapped  
- [ ] Validation object prepared  
- [ ] Revision history seeded  

---

## 3. Schema validation

- [ ] JSON parses  
- [ ] Validates against `knowledge_record.schema.json`  
- [ ] Module overlay validated (if applicable)  
- [ ] `schema_valid = true` only if actually passed  

---

## 4. Reference validation

- [ ] All `reference_id` resolve in Foundation library  
- [ ] Titles checked against library  
- [ ] `TODO_REVIEW` chapters/notes flagged  
- [ ] `reference_valid` set correctly  

---

## 5. Relationship validation

- [ ] All target `KNO-*` resolve (or Official blocked)  
- [ ] Relationship types present  
- [ ] No forbidden duplicate Canon ownership  
- [ ] `relationship_valid` set correctly  

---

## 6. Integrity validation

- [ ] Knowledge ID unique  
- [ ] Planning ID binding unique  
- [ ] Status/version patterns valid  
- [ ] `integrity_valid` set correctly  

---

## 7. Output validation

- [ ] Output path correct  
- [ ] Filename/slug convention OK  
- [ ] Compilation report filled  
- [ ] No extra academic text injected by tooling  
- [ ] Ready for write authorization (if Official)  

---

## Sign-off

| Role | Name | Date | Result |
|------|------|------|--------|
| Compiler operator | | | |
| Technical reviewer | | | |
| Academic reviewer | | | |
