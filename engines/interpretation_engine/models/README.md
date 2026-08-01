# Models

Legacy interpretation models coexist with Pack 03 architecture and output models.

## Pack 03 interpretation output models

| Model | Role |
|-------|------|
| `InterpretationResult` | Top-level output aggregate |
| `SectionResult` | Section shell |
| `ParagraphResult` | Paragraph shell |
| `SentenceResult` | Sentence *reference* shell |
| `Metadata` | Output metadata |
| `TraceInformation` | Execution trace identifiers |
| `VersionInfo` | Schema/engine/model versions |

## Hard rules

- No report rendering
- Sentence/paragraph/section outputs hold refs and structure only
- Legacy report models remain for backward compatibility
