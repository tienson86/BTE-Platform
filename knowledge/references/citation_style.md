# Citation Style Guide

**Module:** `knowledge/references`  
**Version:** V1.0.0  

---

## 1. In-record citation (Knowledge Canon)

Preferred form:

```text
<title_english> (<title_original>), <reference_id>
```

Example:

```text
Huang Di Nei Jing (黃帝內經), REF-000001
```

---

## 2. Short citation

When space is limited:

```text
<title_english> [<reference_id>]
```

Example:

```text
Di Tian Sui [REF-000005]
```

---

## 3. JSON reference object

Knowledge Records SHALL cite library IDs:

```json
{
  "reference_id": "REF-000003",
  "title": "Yuan Hai Zi Ping",
  "chapter": "TODO_REVIEW",
  "notes": "TODO_REVIEW"
}
```

Rules:

- `reference_id` MUST exist in `references.json`
- Do not invent Reference IDs locally
- Unverified chapters MUST use `TODO_REVIEW`

---

## 4. Bibliography line

```text
<author>. <title_english> (<title_original>). <dynasty/estimated_year>. <edition>. REF-<id>.
```

If a field is `TODO_REVIEW`, omit invented values and keep the Reference ID.

---

## 5. Prohibited practices

- Citing by title only without Reference ID in Official records
- Reusing a Reference ID for a different work
- Encoding school/category inside the ID string
