# Compiler Package

Architecture skeleton for the Analysis Engine Compiler Layer.

## Public Modules

| Module | Interface / Model |
|--------|-------------------|
| `compiler.py` | `Compiler` |
| `loader.py` | `Loader` |
| `normalizer.py` | `Normalizer` |
| `transformer.py` | `Transformer` |
| `manifest.py` | `CompilerManifest` |
| `package_builder.py` | `PackageBuilder` |
| `build_context.py` | `BuildContext` |
| `build_result.py` | `BuildResult`, `BuildArtifact` |
| `interfaces.py` | ABC contracts |

Public interfaces only. No business logic. No compilation algorithms.
