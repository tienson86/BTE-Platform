# Template Engine

Template *reference* infrastructure for Pack 03.

## Runtime modules

| Module | Role |
|--------|------|
| `loader.py` | Load template-ref descriptors (no bodies) |
| `resolver.py` | Resolve template ref ids to `TemplateRef` shells |
| `validator.py` | Validate refs and slot bindings |
| `renderer.py` | Produce `TemplateRenderShell` / bindings (no prose) |
| `metadata.py` | Ref/binding/render models + metadata helper |
| `interface.py` | `TemplateEngineInterface` + default `TemplateEngine` facade |

## Hard rules

- No templates / no template library
- No hard-coded template bodies
- Renderer output is structural shells only
