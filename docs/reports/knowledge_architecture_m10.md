# Knowledge System Architecture — Epic 03 Milestone 10

## Pipeline

```text
Knowledge Corpus (database/20_knowledge)
        ↓
Knowledge Retriever
        ↓
Reasoning Graph Engine
        ↓
Evidence Builder
        ↓
Prompt Builder (+ internal Citation Engine)
        ↓
LLM Adapter (DeterministicKnowledgeLLM by default)
        ↓
AI Response Validator
        ↓
Portal additive payload / POST /api/v1/discussion
```

## BTE Integration Boundaries

- Calculation engines unchanged
- `PUBLIC_PIPELINE_ORDER` unchanged
- `report` / `narrative` contracts unchanged
- Portal Discussion tab remains narrative-compatible
- Knowledge Expert attaches additively via `knowledge_expert`

## Stages

- `knowledge`
- `retriever`
- `reasoning_graph`
- `evidence_builder`
- `prompt_builder`
- `llm`
- `response_validator`
- `portal`
