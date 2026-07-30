# Knowledge Registry Discovery Model

**Component:** Knowledge Registry  
**Version:** V1.0.0  
**Status:** Frozen (Discovery Model Specification)

---

# 1. Purpose

This document defines discovery and search for Knowledge Modules and Knowledge Assets.

---

# 2. Discovery Goals

Discovery shall enable consumers and loaders to:

- find modules by identity, domain, status, and version;
- find assets by identity, type, module, and version;
- search by metadata facets and tags;
- list available versions;
- resolve KnowledgeReferences without physical-path knowledge.

---

# 3. Discovery Operations

Logical discovery operations include:

| Operation | Result |
|-----------|--------|
| Find Module | Module Registry Entry or not found |
| Find Asset | Asset Registry Entry or not found |
| List Modules | Filtered module collection |
| List Assets | Filtered asset collection |
| List Versions | Version history for module or asset |
| Search Knowledge | Ranked KnowledgeSearchResult set |
| Resolve Reference | Canonical KnowledgeReference target |

---

# 4. Search Model

Search Knowledge accepts a RegistryDiscoveryQuery containing any combination of:

- free-text metadata query
- module_id / asset_id filters
- domain / asset_type filters
- status filters
- version / version-range filters
- owner / consumer filters
- tag / locale filters
- dependency / compatibility filters

Results return:

- matched identities
- versions
- status
- summary metadata
- KnowledgeReferences

Search does not evaluate rule content.

---

# 5. Knowledge Index Usage

Discovery reads from the Knowledge Index.

Index freshness is tied to Catalog Revision.

Stale index states are invalid for production discovery until refreshed.

---

# 6. Visibility Rules

Discovery results respect:

- lifecycle status visibility policy
- security authorization policy
- consumer scope restrictions where declared

Draft content is not visible to production consumers by default.

---

# 7. Non-Goals

Discovery does not:

- execute knowledge
- select engine algorithms
- mutate registry state
- expose storage locations as required output

---

# 8. Acceptance Criteria

Discovery Model is accepted when operations, query facets, result contracts, index freshness, and visibility rules are complete.
