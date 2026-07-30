# BTE Reference Library

**Module:** Knowledge References  
**Version:** V1.0.0  
**Status:** Official Framework  
**Governance Alignment:** Governance V1.0 (frozen) — no Governance documents were modified by this module.

---

## Purpose

The Reference Library is the authoritative catalog of external and internal sources used by the BTE Knowledge Canon.

It provides:

- Stable Reference IDs
- Standardized bibliographic metadata
- Category indexes (Classics, Modern, Papers, Internal)
- Cross-reference mapping to Knowledge, Rules, and Sentences
- Quality and edge-case guidance for reference authors

This module is **documentation only**. It does not contain engine code, loaders, or runtime implementation.

---

## Scope

In scope:

- Reference records and metadata
- Templates and indexes
- Mapping registries
- Quality / edge-case guidance

Out of scope:

- Full academic transcription of classical works
- Governance policy changes
- Runtime validation services
- Modification of published Golden Datasets

---

## Directory Structure

```
knowledge/references/
├── README.md
├── REFERENCE_INDEX.md
├── REFERENCE_SPEC.md
├── REFERENCE_METADATA.yaml
├── CHANGELOG.md
├── QUALITY_GUIDE.md
├── EDGE_CASES.md
├── classics/
├── modern/
├── papers/
├── internal/
└── mapping/
```

---

## Reference ID Format

Every reference SHALL use a permanent sequential ID:

```
REF-000001
REF-000002
...
```

Rules:

- IDs are immutable once published.
- Numbers are zero-padded to six digits.
- One Reference ID maps to exactly one official record.
- Category is stored in metadata; it is not encoded in the ID string.

---

## Categories

| Category | Directory | Description |
|----------|-----------|-------------|
| Classic | `classics/` | Classical BaZi / calendar / fate texts |
| Modern | `modern/` | Modern books and monographs |
| Paper | `papers/` | Academic papers and journals |
| Internal | `internal/` | BTE-internal reference notes |

Category codes remain compatible with Governance Reference Standard (`CLASSIC`, `BOOK`, `PAPER`, `INTERNAL`, …) via the `category` metadata field.

---

## Mandatory Metadata

Every reference record MUST include:

| Field | Description |
|-------|-------------|
| Reference ID | `REF-NNNNNN` |
| Title | Primary display title |
| Chinese Title | Original / Chinese title when applicable |
| English Title | English title |
| Vietnamese Title | Vietnamese title |
| Author | Author or traditional attribution |
| Dynasty | Historical period when applicable |
| School | Doctrinal school |
| Language | Source language |
| Category | Classic / Modern / Paper / Internal |
| Reliability | Reliability level |
| Edition | Edition identifier |
| Translator | Translator if applicable |
| Publisher | Publisher if applicable |
| ISBN | ISBN if applicable |
| Year | Publication / compilation year |
| Status | Draft / Review / Official / Deprecated |
| Version | Document version |
| License | Rights / license note |
| Keywords | Search keywords |
| Summary | Short non-academic summary placeholder |
| Related References | Other `REF-*` IDs |
| Related Knowledge | Knowledge asset IDs |
| Related Rules | Rule IDs |
| Related Sentences | Sentence IDs |

---

## How to Add a Reference

1. Allocate the next free `REF-NNNNNN` in `REFERENCE_INDEX.md` and `REFERENCE_METADATA.yaml`.
2. Copy the category `TEMPLATE.md`.
3. Fill metadata only (no full academic content required for framework records).
4. Register mappings in `mapping/` as needed.
5. Update the category `INDEX.md`.
6. Follow `QUALITY_GUIDE.md` and `EDGE_CASES.md`.
7. Register through Governance Reference Registration procedures without editing frozen Governance V1.0 files.

---

## Related Module Documents

| Document | Role |
|----------|------|
| [REFERENCE_INDEX.md](REFERENCE_INDEX.md) | Master catalog |
| [REFERENCE_SPEC.md](REFERENCE_SPEC.md) | Formal specification |
| [REFERENCE_METADATA.yaml](REFERENCE_METADATA.yaml) | Machine-readable registry |
| [QUALITY_GUIDE.md](QUALITY_GUIDE.md) | Quality requirements |
| [EDGE_CASES.md](EDGE_CASES.md) | Edge-case handling |
| [CHANGELOG.md](CHANGELOG.md) | Module history |

Companion docs that may already exist in this folder (traceability / extraction / mapping standards) remain valid companions and are not replaced by this framework.

---

## Governance Note

Governance V1.0 is frozen.

This Reference Library framework **complies with** Governance Reference Standard, Reference Template, Reference Registration, and Reference Registry concepts.

This module **does not modify** any file under `knowledge/governance/`.
