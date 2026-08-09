# Ontology Reference Model

**Version:** 1.0.0  
**Status:** Canonical

---

## Structural vs semantic

| Kind | Examples | Question answered |
|------|----------|-------------------|
| Structural | contains, belongs_to, depends_on | How is knowledge organized and loaded? |
| Semantic | inherits, specializes, equivalent_to, overrides | What does knowledge mean and how does it refine meaning? |

Loaders and indexes primarily consume structural relations.  
Authoring tools, validators, and school/language overlays primarily consume semantic relations.

---

## Concept layers

```
KnowledgeObject
├── AnalyticalKnowledge
│   ├── Rule
│   ├── Pattern
│   ├── ElementalEntity
│   └── SchoolVariant
├── PresentationKnowledge
│   ├── InterpretationUnit
│   ├── ReportUnit
│   └── LanguageVariant
└── GovernanceKnowledge
```

---

## Semantic evolution strategy

1. **Additive evolution preferred** — new specialized concepts extend parents.
2. **Equivalence mapping** for multilingual and school synonyms.
3. **Deprecation over deletion** for released concepts.
4. **Migration manifests** required when inheritance parents change identity.
5. **Future domains** (Feng Shui, Qi Men, I Ching) attach under reserved taxonomy domains without rewriting BaZi core concepts.

---

## Compatibility

Ontology V1.0.0 does not rewrite existing rule packages.  
V1 records map into ontology classes through type/category projection defined with Knowledge Database V2 compatibility mapping.
