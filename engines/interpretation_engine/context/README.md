# Context

Interpretation context contracts and Pack 03 lifecycle runtime.

## Runtime modules

| Module | Role |
|--------|------|
| `builder.py` | Fluent builder from Pack 02 `FinalResult` |
| `factory.py` | Create / clone Interpretation Context |
| `manager.py` | Lifecycle: create → initialize → expand → validate → finalize → dispose |
| `snapshot.py` | Immutable context snapshots |
| `history.py` | Append-only revision/snapshot history |
| `serializer.py` | JSON serialize/deserialize |
| `interpretation_context.py` | Pack 03 `InterpretationContext` (output) |
| `revision.py` | Lifecycle phase + revision records |

## Input / Output

- **Input:** Pack 02 `FinalAnalysisResult` / `FinalResult` only
- **Output:** Pack 03 `InterpretationContext` (`PackInterpretationContext` at package level)

Legacy BaZi-field `InterpretationContext` remains re-exported for backward compatibility.

No interpretation business logic.
