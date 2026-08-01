# Sentence Engine

Sentence *reference* infrastructure for Pack 03.

## Runtime modules

| Module | Role |
|--------|------|
| `selector.py` | Select sentence-ref candidates by structural criteria |
| `ranking.py` | Deterministic ranking by score/priority |
| `resolver.py` | Resolve ref ids to `SentenceRef` shells |
| `composer.py` | Compose ordered `SentenceComposition` shells |
| `metadata.py` | Ref/candidate/composition models + metadata helper |
| `interface.py` | `SentenceEngineInterface` + default `SentenceEngine` facade |

## Hard rules

- No sentence library
- No natural language generation
- Outputs are reference ids and metadata shells only
