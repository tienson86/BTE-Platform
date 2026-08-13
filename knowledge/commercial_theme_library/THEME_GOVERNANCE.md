# THEME_GOVERNANCE

| Field | Value |
|-------|-------|
| Package | Commercial Theme Library V1.0 |
| Status | **FROZEN** |

---

## Owners

| Layer | Owner | This library |
|-------|-------|--------------|
| Theme IDs in CDR | Reasoning | Read-only |
| Knowledge / rules | Knowledge | Untouched |
| Paragraph craft | CLL | Untouched in V1.0 create |
| Theme *content* stances | This catalog | Product + Language |
| Audience | Product Context | Untouched |

---

## Add a theme

Allowed only when **all** are true:

1. At least two real charts would reuse it.  
2. It is not an alias of an existing canonical id.  
3. It does not encode a person or CASE.  
4. All 9 blocks can be filled without doctrine invention.  
5. CDR already publishes a signal it can bind to — **or** it is an overlay on published signals.  
6. Version bump (1.1 / 1.2).

Forbidden: adding `THEME_CASE_0001` or `THEME_<Name>`.

---

## Bind

| Do | Do not |
|----|--------|
| Select from published `primary_theme` + capacity + structure | Infer a theme to make copy nicer |
| Combine 1 operating + ≤2 overlays | Replace Truth with a marketing persona |
| Leave overlay off if unsupported | Force CONSERVING on a strong self-carry with no thin signal |

RC3 personas (P01–P10) may **review** a theme. They must not **author** a theme id.

---

## Change a stance

- Fix leak (e.g. output-cycle on BALANCE) = patch, keep id.  
- Change the job of a theme = new id + deprecate.  
- Never edit Knowledge packs or CDR to make a stance easier.

---

## Deprecate

Mark `deprecated` in THEME_INDEX. Keep id for compatibility. Do not delete.

---

## Version

| Version | Meaning |
|---------|---------|
| 1.0.0 | Initial catalog (this release) |
| 1.x | Add overlay or block stance |
| 2.0 | Model change (new layer) — requires Product |

---

END
