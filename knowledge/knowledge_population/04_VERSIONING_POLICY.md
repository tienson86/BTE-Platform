# 04 — Versioning Policy

Version: 1.0  
Status: **EPIC 3 · SPRINT A — Population Framework**  
Date: 2026-08-08  
Depends on: `01`, EPIC 2 `14`/`15`  

---

## 1. Purpose

Define how Knowledge Units are identified, versioned, superseded, and deprecated during population and maintenance.

---

## 2. Identity rules

| Rule | Detail |
|------|--------|
| Immutable id | `knowledge_unit_id` never changes once reserved |
| Catalog alignment | Prefer ids from EPIC 2 `16`; new ids require catalog amendment |
| Naming | `KU-{KIND}-{DOMAIN}-{SEQ}` per `15` |
| No reuse | Deprecated ids are never reassigned to different meaning |

Traces always store **id + version**.

---

## 3. Semantic versioning

Format: `MAJOR.MINOR.PATCH`

| Bump | When |
|------|------|
| **MAJOR** | Kind, evidence_kind, primary_intent, or ethics posture changes; conditions change enough to alter who receives advice |
| **MINOR** | Material wording/advice refinement; added secondary usage; tightened conditions without changing audience class |
| **PATCH** | Typos, formatting, non-semantic clarification |

Pre-publish Drafts may use `0.x.y` or `1.0.0-draft` — team convention fixed at first content sprint.

First Publish of a catalog row should be `1.0.0` unless Architect approves otherwise.

---

## 4. Lifecycle × version

| Event | Version action | Status |
|-------|----------------|--------|
| Create Draft | Set initial version | `draft` |
| Pass reviews → Approve | Keep version | `approved` |
| Publish | Keep version; set published_at | `published` |
| Typo fix on Published | PATCH; fast-track | new Published; old deprecated or retained per §6 |
| Meaning change | MINOR/MAJOR; full reviews | new version Draft → … → Published |
| Replace with better unit | New id or new MAJOR; `supersedes` links | old `deprecated` |

---

## 5. Supersession

| Field | Use |
|-------|-----|
| `supersedes` | This unit/version replaces target id@version |
| `superseded_by` | Set on retired unit pointing to successor |

Rules:

1. Production retrieval prefers latest Published not deprecated.  
2. Historical Narrative traces may reference old versions — keep readable.  
3. Do not silently edit Published meaning in place.

---

## 6. Deprecation policy

| Trigger | Action |
|---------|--------|
| Replaced by successor | Deprecate old; link supersession |
| Unsafe ethics finding | Immediate deprecate; emergency replacement wave |
| Catalog removal | Deprecate; do not delete history |
| Duplicate merge | Keep winner Published; deprecate loser |

Deprecated units:

- Excluded from new compositions  
- Retained for audit/trace  
- Never hard-deleted in population sprints  

---

## 7. Fast-track (typo-only)

Allowed only when Technical Reviewer attests **no semantic change**.

| Step | Required |
|------|----------|
| 1 | PATCH bump |
| 2 | Technical confirmation recorded |
| 3 | Commercial skim optional; Narrative skim if customer-facing string |
| 4 | Knowledge Review skipped only if attestation holds |
| 5 | Publish replacement; deprecate prior patch lineage as needed |

If attestation disputed → full path.

---

## 8. Wave / release versioning

| Object | Versioning |
|--------|------------|
| Individual KU | Semver above |
| Wave batch | Wave id `W-P0-1.1` etc. (`05`) + date |
| Population Framework docs | Document header version |
| Publish manifest | Manifest version per publish event |

Manifest must list: `knowledge_unit_id`, `version`, `wave_id`, `published_at`, `reviewers`.

---

## 9. Compatibility

| Change | Compatibility expectation |
|--------|---------------------------|
| PATCH/MINOR wording | Safe for same conditions |
| MAJOR condition change | Treat as new advice; update scenario tests |
| Kind change | Prefer new id if traces would confuse |

Additive catalog rows are always preferred over breaking renames.

---

## 10. Stop line

Versioning policy defined. No versions minted (no units).

---

END
