# Reference Quality Guide

**Document:** QUALITY_GUIDE  
**Module:** knowledge/references  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define quality requirements for Reference Library records so citations remain accurate, consistent, and Governance-compatible.

---

## Quality Principles

1. **Identity before content** — Metadata must be correct even when academic body text is still a placeholder.
2. **One ID, one work** — Do not split editions into conflicting IDs without an explicit edition-policy note.
3. **Verifiable claims** — Do not state historical conclusions without a future content review gate.
4. **Traceable links** — Related Knowledge / Rules / Sentences must use official IDs only.
5. **Stable language** — English documentation; original titles preserved in dedicated fields.

---

## Mandatory Completeness Checklist

Before moving a record from Placeholder/Draft to Review:

- [ ] Reference ID allocated in `REFERENCE_INDEX.md`
- [ ] Entry present in `REFERENCE_METADATA.yaml`
- [ ] All mandatory metadata fields populated (`N/A` / `Unspecified` allowed where defined)
- [ ] Category matches directory placement
- [ ] Keywords are meaningful or explicitly `None`
- [ ] Summary is present (placeholder sentence allowed)
- [ ] Related lists use only valid ID formats or are empty
- [ ] File name follows category naming convention
- [ ] No Governance files modified

---

## Metadata Quality Rules

| Field | Quality Rule |
|-------|--------------|
| Title | Prefer widely recognized English / romanized title |
| Chinese Title | Prefer traditional form when classical; note simplified separately if needed in notes |
| Author | Prefer historical attribution; mark uncertainty explicitly |
| Dynasty | Use conventional dynasty labels; `N/A` for modern/paper/internal when not applicable |
| School | Prefer mapped school from `mapping/reference_school.json` |
| Reliability | Do not mark `Primary` without editorial confidence |
| ISBN | Use `N/A` when pre-modern or unknown |
| License | State rights status; do not invent permissions |

---

## Content Depth Policy (Framework Phase)

For V1.0.0 framework records:

- Full academic chapters are **not required**.
- Structural outline headings MAY exist as placeholders.
- Authors MUST NOT invent long interpretive essays presented as verified doctrine.

When academic content is later added, it SHOULD follow Governance style and reference standards without altering Governance files.

---

## Cross-Reference Quality

- Prefer registry updates in `mapping/` when linking many assets.
- Keep document Related-* fields synchronized after registry edits.
- Broken or speculative IDs MUST NOT be marked Official.

---

## Reliability Levels

| Level | Use when |
|-------|----------|
| Primary | Canonical classical or authoritative edition family |
| Secondary | Reliable modern edition / commentary |
| Tertiary | Derivative summaries or tertiary citations |
| Unverified | Identity incomplete or contested |
| Internal | BTE-internal note only |

---

## Naming Conventions

### Classics files

```
NN_LATIN_SNAKE.md
```

Example: `01_YUAN_HAI_ZI_PING.md`

### Modern / Papers / Internal

Prefer:

```
REF-NNNNNN_SHORT_SLUG.md
```

until category-specific conventions are expanded.

---

## Review Gates

| Gate | Minimum |
|------|---------|
| Placeholder → Draft | ID + metadata table started |
| Draft → Review | Mandatory fields complete |
| Review → Official | Index + YAML + mapping consistency checked |
| Official → Deprecated | Replacement ID noted in Related References |

---

## Non-Goals

This guide does not:

- Change Governance V1.0
- Define engine scoring behavior
- Authorize silent edits to Golden expected outputs
