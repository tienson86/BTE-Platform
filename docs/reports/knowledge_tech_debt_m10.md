# Remaining Technical Debt — Epic 03 Milestone 10

1. **Classical corpus content** — `database/20_knowledge` is still largely schema-only; curated rows needed for production retrieval quality.
2. **External LLM adapter** — production currently uses `DeterministicKnowledgeLLM`; swap-in client not configured.
3. **Portal Q&A UI** — Discussion tab still displays narrative shell only; no interactive Q&A controls yet (by design for no UI regression).
4. **RuleContext bridge** — Discussion derives context from public analyze fields rather than internal published RuleContext snapshot.
5. **Citation optional CSV columns** — chapter/page/citation_id are model-supported but not yet required CSV schema columns.
