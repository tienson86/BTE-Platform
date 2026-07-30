# Citation Examples

**Module:** `knowledge/citation_rules`  
**Version:** V1.0.0  
**Status:** Official Foundation (Freeze Candidate)  

Examples below are **mechanical only**. They do not interpret classical doctrines.

---

## 1. Knowledge Record — single reference

```json
{
  "knowledge_id": "KNO-000001",
  "references": [
    {
      "reference_id": "REF-000001",
      "title": "Huang Di Nei Jing",
      "chapter": "TODO_REVIEW",
      "notes": "TODO_REVIEW"
    }
  ]
}
```

Human citation line:

```text
Huang Di Nei Jing (黃帝內經), REF-000001
```

---

## 2. Knowledge Record — multiple references

```json
{
  "knowledge_id": "KNO-000001",
  "references": [
    {
      "reference_id": "REF-000003",
      "title": "Yuan Hai Zi Ping",
      "chapter": "TODO_REVIEW",
      "notes": "TODO_REVIEW"
    },
    {
      "reference_id": "REF-000005",
      "title": "Di Tian Sui",
      "chapter": "TODO_REVIEW",
      "notes": "TODO_REVIEW"
    },
    {
      "reference_id": "REF-000006",
      "title": "Zi Ping Zhen Quan",
      "chapter": "TODO_REVIEW",
      "notes": "TODO_REVIEW"
    }
  ]
}
```

---

## 3. Reference usage — bibliography line (reports)

```text
Traditional attribution. Yuan Hai Zi Ping (淵海子平). TODO_REVIEW. REF-000003.
```

Uncertain bibliographic fields remain `TODO_REVIEW` until Academic Review.

---

## 4. Reference usage — short UI form

```text
Di Tian Sui [REF-000005]
```

---

## 5. Invalid examples (must fail validation)

Missing ID:

```json
{
  "title": "Yuan Hai Zi Ping",
  "chapter": "1"
}
```

Invented ID:

```json
{
  "reference_id": "REF-999999",
  "title": "Unknown Work"
}
```

Title-only Official citation:

```text
See Yuan Hai Zi Ping for details.
```

ID/title mismatch (WARNING):

```json
{
  "reference_id": "REF-000001",
  "title": "Yuan Hai Zi Ping"
}
```

(`REF-000001` is Huang Di Nei Jing in Foundation V1.0 SSOT.)

---

## 6. Citation lifecycle example

| Stage | Example action |
|-------|----------------|
| Draft | Author adds `REF-000003` with `chapter: TODO_REVIEW` |
| Technical Review | Validator confirms ID exists in `references.json` |
| Academic Review | Chapter/notes updated or left `TODO_REVIEW` with justification |
| Official | Citation retained; inventing new IDs forbidden |
| Deprecation | If REF is deprecated, consumers migrate to replacement ID |
